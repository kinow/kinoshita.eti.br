---
categories:
- blog
date: "2016-12-19T00:00:00Z"
tags:
- jenkins
- software quality
title: 'PermGen errors and java.lang.ClassCastException: com.sun.crypto.provider.AESCipher
  cannot be cast to javax.crypto.CipherSpi running Jenkins plug-in tests with PowerMock'
---

Recently while working on a Jenkins plugin some tests were failing with PermGen errors.
Even though it worked in my notebook at home (with Java 8, thus no Permgen), it failed
in a CloudBees hosted Jenkins job, and also on my Mac (with Java 7) at work.

As I could not change the settings in the CloudBees hosted Jenkins, I decided to spent some
time investigating why these tests would require so much memory. Then I found
[this blog post about PowerMock](https://angus.nyc/2015/fixing-common-powermock-problems/).

I was not using the *@PrepareForTest* annotation, but after adding it the issue was gone. So I
assume it either prevents PowerMock from trying to dynamically load several classes, or instructs
it to unload classes after the tests. But in anyway after adding it the issue was gone.

Then I got the following exception.

```shell
WARNING: Failed to instantiate Key[type=hudson.security.csrf.DefaultCrumbIssuer$DescriptorImpl, annotation=[none]]; skipping this component
com.google.inject.ProvisionException: Guice provision errors:

1) Error injecting constructor, java.lang.ClassCastException: com.sun.crypto.provider.AESCipher cannot be cast to javax.crypto.CipherSpi
  at hudson.security.csrf.DefaultCrumbIssuer$DescriptorImpl.<init>(DefaultCrumbIssuer.java:127)

1 error
    at com.google.inject.internal.ProviderToInternalFactoryAdapter.get(ProviderToInternalFactoryAdapter.java:52)
```

And then thanks to [this issue](https://github.com/powermock/powermock/issues/294) I understood
that PowerMock was mocking *javax.crypto* classes. Turns out it is quite easy to tell
PowerMock to ignore certain classes from being mocked, with the *@PowerMockIgnore* annotation.

```java
// snip
@RunWith(PowerMockRunner.class)
@PowerMockIgnore({"javax.crypto.*" })
public class TestAbstractUnoChoiceParameter {
//
}
// snip
```

Added a couple of notes to this [Jenkins Wiki page](https://wiki.jenkins-ci.org/display/JENKINS/Mocking+in+Unit+Tests)
so that users facing similar issues can try these possible workarounds.

Hope that helps someone!
