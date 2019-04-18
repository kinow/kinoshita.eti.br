---
title: 'How does the Jenkins Credentials Plug-in store passwords?'
author: kinow
tags:
    - jenkins
    - security
category: 'blog'
time: '01:25:03'
---

[Jenkins Credentials Plug-in](https://wiki.jenkins-ci.org/display/JENKINS/Credentials+Plugin) manages credentials stored in Jenkins. These credentials can be used in many jobs and by plug-ins for executing SSH commands, authenticating to systems, or running other commands that need some sort of authentication or authorisation.

I recently used its API for the first time in the [BioUno figshare Plug-in](https://github.com/biouno/figshare-plugin) to store OAuth 1.0 credentials (consumer key, consumer secret, token key, token secret). This [blog post](http://biouno.org/2015/09/05/using_jenkins_credentials_plugin_to_create_the_biouno_figshare_plugin/) has more details about how we used the plug-in, but this post is specifically on how the passwords are stored by Jenkins.

## Secret and ciphers

Jenkins stores its configuration on disk as XML using the XStream library. Plug-in developers using the Credentials Plug-in API must use the **Secret** class to encrypt sensitive information.

The `Secret.fromString` method is responsible for creating a cipher from a given String. As in the Secret Javadoc,  *"this is not meant as a protection against code running in the same VM, nor against an attacker who has local file system access on Jenkins master"*. But at least makes things more complicated :-)

* [Secret Javadoc](http://javadoc.jenkins-ci.org/hudson/util/Secret.html)
* [Secret source code](https://github.com/jenkinsci/jenkins/blob/master/core/src/main/java/hudson/util/Secret.java)

{% geshi 'java' %}
public static Secret fromString(String data) {
    data = Util.fixNull(data);
    Secret s = decrypt(data);
    if(s==null) s=new Secret(data);
    return s;
}
{% endgeshi %}

The first line simply replaces a null string by an empty "", or keeps the current value of not null.

After that, the decrypt method is called.

{% geshi 'java' %}
public static Secret decrypt(String data) {
    if(data==null)      return null;
    try {
        byte[] in = Base64.decode(data.toCharArray());
        Secret s = tryDecrypt(KEY.decrypt(), in);
        if (s!=null)    return s;

        // try our historical key for backward compatibility
        Cipher cipher = getCipher("AES");
        cipher.init(Cipher.DECRYPT_MODE, getLegacyKey());
        return tryDecrypt(cipher, in);
    } catch (GeneralSecurityException e) {
        return null;
    } catch (UnsupportedEncodingException e) {
        throw new Error(e); // impossible
    } catch (IOException e) {
        return null;
    }
}
{% endgeshi %}

The `KEY.decrypt()` call will return a [`javax.crypto.Cipher`](http://docs.oracle.com/javase/8/docs/api/javax/crypto/Cipher.html). The Cipher class is handled in [CryptoConfidentialKey](https://github.com/jenkinsci/jenkins/blob/93dfe3377ec8d430818f5b9073f16c677343adb4/core/src/main/java/jenkins/security/CryptoConfidentialKey.java) in Jenkins API, where it defines the algorithm used to create the cipher: [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard).

Jenkins has also a [ConfidentialStore](https://github.com/jenkinsci/jenkins/blob/93dfe3377ec8d430818f5b9073f16c677343adb4/core/src/main/java/jenkins/security/ConfidentialStore.java#L63), that is required to create the cipher. This class must be initialized before someone tries to create or read a cipher. This extra step also increases security, though access to the JVM is still a problem.

It is a bit late, so it is all for today. In summary: the credentials plug-in gives you a central place to manage credentials, but it is up to plug-in developers to use it. Sensitive values can be encrypted with AES on disk. So it is important that your file permissions, ACL and system auditing processes are in place and well maintained and monitored.

Happy hacking!



