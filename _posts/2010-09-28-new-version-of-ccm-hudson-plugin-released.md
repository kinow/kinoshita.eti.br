---
date: 2010-09-28 08:55:53 +1300
layout: post
tags:
- software quality
- jenkins
title: New version of CCM Hudson Plugin released
---

Yesterday I released a new version of <a title="CCM Hudson Plugin" href="http://wiki.hudson-ci.org/display/HUDSON/CCM+Plugin">CCM Hudson Plugin</a>. In this version, 1.0.1, there are two bugs fixed (7522 and 7531). For a more detailed background on these two issues check out <a title="Hudson JIRA" href="http://issues.hudson-ci.org">Hudson JIRA</a>.

<div class='row'>
<div class="ui container" style='text-align: center;'>
<figure>
<a href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/clipart-man-spraying-giant-bug-with-aerosol-can-300x189.png" rel="prettyPhoto" class="thumbnail" title="">
<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/clipart-man-spraying-giant-bug-with-aerosol-can.png" alt="=" />


Both bugs were reported by <a title="Sven Borman" href="http://nl.linkedin.com/pub/sven-borman/0/b16/814/">Sven Borman</a>. The <a title="CCM Hudson Plugin BUG 7522" href="http://issues.hudson-ci.org/browse/HUDSON-7522">first BUG</a> referred to a problem executing <a title="CCM Hudson Plugin" href="http://wiki.hudson-ci.org/display/HUDSON/CCM+Plugin">CCM Hudson Plugin</a> in distributed environments. Although I've read the documentation for <a title="Making Hudson plugins behave in distribitued environments" href="http://wiki.hudson-ci.org/display/HUDSON/Making+your+plugin+behave+in+distributed+Hudson">making plugins behave in distributed environments</a> I forgot to use the Callable interfaces to execute some parts of the code in the Slave and then serialize the result back to the master node.

And the <a title="CCM Hudson Plugin BUG 7531" href="http://issues.hudson-ci.org/browse/HUDSON-7531">latter BUG</a> was a problem executing the command in a Windows 2003 environment. In the beginning I thought there would be something wrong in the BUG description. Bug after setting up a Virtual Machine with Windows 2003 I noticed that the command without double quotes didn't work correctly in the Windows 2003. Although it worked in Windows XP, Vista and Windows 7.

Nice catch Sven! Cheers.
