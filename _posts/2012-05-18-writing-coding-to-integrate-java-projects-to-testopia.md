---
title: 'Writing code to integrate Java projects to Testopia'
id: 953
author: kinow
tags: 
    - java
category: 'blog'
time: '17:16:25'
---
<em>Peter Florijn</em> and I are writing a <a href="http://www.jenkins-ci.org" title="Jenkins CI">Jenkins</a> plug-in to <em>integrate several test tools into Jenkins</em>, something similar to what is done in <a href="https://wiki.jenkins-ci.org/display/JENKINS/TestLink+Plugin" title="Jenkins TestLink Plug-in">TestLink plug-in</a>. It's still an idea being explored, and the whole project is subjected to changes without warning. The code is at <a href="https://github.com/kinow/testthemall" title="https://github.com/kinow/testthemall">https://github.com/kinow/testthemall</a>.

The first tool that we are integrating is not <a href="http://www.teamst.org" title="TestLink">TestLink</a>, but <a href="http://www.mozilla.org/projects/testopia/" title="Mozilla Testopia">Mozilla Testopia</a>. As part of the process to integrate these tools, many Java API's to interface the existing external APIs will be created, like it was done in TestLink with <a href="https://sourceforge.net/projects/testlinkjavaapi/" title="TestLink Java API">TestLink Java API</a>.

<p style="text-align: center"><img src="{{ assets.Jenkins1_300_224 }}" alt="" title="Jenkins CI" height="128" class="aligncenter size-medium wp-image-978" /><img src="{{assets.testopia_128_128}}" alt="" title="Testopia" width="128" height="128" class="aligncenter size-full wp-image-979" /></p>

Installing Testopia is very easy and straightforward. <a href="http://blog.marcweigand.de/2011/02/20/how-to-setup-bugzilla-with-testopia-on-a-new-debian-squeeze-60/" title="http://blog.marcweigand.de/2011/02/20/how-to-setup-bugzilla-with-testopia-on-a-new-debian-squeeze-60/">This</a> was the best guide that I could find, and worked without errors at my Debian Squeeze. I only had to move the directories from <code>/var/www</code> to my home directory (I use my PHP Eclipse workspace as Apache home).

Testopia has a XML-RPC APi, just like TestLink, however it lacks an user friendly documentation and examples. I migrated the Java driver from Ant to Maven, for the sake of commodity. But the XML-RPC server is complaining that I have to log-in before listing the test cases of a test plan.

If you are interested in using Java and Testopia, here's the link for the java project with Maven support: <a href="https://github.com/kinow/testopia-java-driver" title="https://github.com/kinow/testopia-java-driver">https://github.com/kinow/testopia-java-driver</a>. I will update the project with examples, more tests and will try to clean up the code. Probably I will use either GitHub pages or a Wiki somewhere to document how to use Testopia and Java. 

Stay tuned!

Cheers,