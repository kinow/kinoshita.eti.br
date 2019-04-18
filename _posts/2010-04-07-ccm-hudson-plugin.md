---
title: 'CCM Hudson Plugin'
id: 251
author: kinow
tags: 
    - jenkins
    - software quality
category: 'jenkins'
time: '16:59:24'
---
CCM is a tool developed by Jonas Blunck (<a href="http://www.blunck.se/">http://www.blunck.se</a>). It's able to calculate the cyclomatic complexity (McCabe) of a .NET Project or Solution.

<div class='row'>
<div class="ui container" style='text-align: center;'>
<figure>
<a href="{{assets.hudson}}" rel="prettyPhoto" class="thumbnail" title="">
<img class="ui fluid image" src="{{assets.hudson}}" alt="=" />
</a>
<figcaption></figcaption>
</figure>
</div>
</div>

I developed <a title="TestLink Hudson Plug-In" href="http://wiki.hudson-ci.org/display/HUDSON/TestLink+Plugin">TestLink Hudson Plug-in</a>, a <a href="http://www.hudson-ci.org">Hudson </a>Plug-in that lets you invoke CCM from hudson and have the results displayed in the console output. I chose CCM as CC tool for .NET instead of SourceMonitor after it gave me a CC value of 4 for a method I was sure was supposed to have 5.

Cheers