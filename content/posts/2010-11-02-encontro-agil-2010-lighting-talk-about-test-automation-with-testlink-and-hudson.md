---
categories:
- blog
date: "2010-11-02T00:00:00Z"
tags:
- jenkins
- testlink
- software quality
- presentations
title: Encontro Ágil 2010 - Lighting talk about Test Automation with TestLink and
  Hudson
---

On November 6th (next Saturday) <a title="Anderson Santos" href="http://andersonxp.tumblr.com/">Anderson Santos</a> and I will present a Test Automation solution built on <a title="TestLink" href="http://www.teamst.org/">TestLink</a> and <a title="Hudson" href="http://www.hudson-ci.org">Hudson</a> at <a title="Encontro &Aacute;gil 2010" href="http://www.encontroagil.com.br/">Encontro &Aacute;gil 2010</a>. This meeting is for intended for the Agile community and will be hold at <a title="IME-USP" href="www.ime.usp.br">IME-USP</a> (Instituto de Matem&aacute;tica e Estat&iacute;stica - Universidade de S&aacute;o Paulo).

<hr class="space" />
<div class='row'>
<div class="ui container" style='text-align: center;'>
<figure>
<a href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/header2.png" rel="prettyPhoto" class="thumbnail" title="">
<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/header2.png" alt="=" />


In our demonstration we will be using TestLink 1.9 HEAD version, Hudson 1.366 and <a title="TestLink Hudson Plug-in" href="http://wiki.hudson-ci.org/display/HUDSON/TestLink+Plugin">TestLink Hudson Plug-in</a> 2.0-SNAPSHOT. This TestLink Hudson Plug-in version is still not released as we are finishing to code the integration between the plug-in and TAP through <a title="tap4j" href="http://tap4j.sourceforge.net/">tap4j</a>, an implementation of <a title="Test Anything Protocol" href="http://www.testanything.org">TAP - Test Anything Protocol</a>.

What is nice about this solution is that we aren't trying to use TestLink as an Automation Tool. But yes, as a Test Management Tool (what TestLink is by nature). And the choice of the Test Execution Tool is up to you, as long as you generate TAP Stream (basically, files containing a log of tests executed). We only enable you to have these tests updated on your TestLink installation, this way you can plan a Test Cycle with both Manual and Automated Tests in one single tool.
<p style="text-align: center;"><a href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/ta_w_tl_hudson2.jpg"><img class="size-medium wp-image-495  aligncenter" title="Test Automation with TestLink and Hudson" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/ta_w_tl_hudson2-300x225.png" alt="" width="300" height="225" /></a></p>
And lastly but not less important, this week <a title="Testing Experience Magazine" href="http://www.testingexperience.com/">Testing Experience Magazine</a> accepted a proposal of article for the next issue on Open Source Tools about this solution. So we are working very hard to release TestLink Hudson Plug-in new version and spread this Test Automation Solution through the Testing/Quality community.

Cheers
