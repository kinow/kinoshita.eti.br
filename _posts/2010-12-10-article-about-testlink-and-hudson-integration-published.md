---
title: 'Article about TestLink and Hudson integration published'
id: 512
author: kinow
tags: 
    - jenkins
    - testlink
    - articles
    - software quality
category: 'articles'
time: '10:52:22'
---
Since September I've been working on a project to integrate TestLink and Hudson. The project consists basically in a Hudson Plug-in that uses <a title="TestLink java api" href="http://testlinkjavaapi.sourceforge.net/">TestLink Java API</a> to retrieve information of Automated Test Cases created in <a title="TestLink" href="http://www.teamst.org">TestLink</a>. You can read more about the plug-in in the following address: <a title="TestLink Hudson Plug-in" href="http://wiki.hudson-ci.org/display/HUDSON/TestLink+Plugin">http://wiki.hudson-ci.org/display/HUDSON/TestLink+Plugin</a>.

I wrote an article in conjunction with <a title="Anderson dos Santos" href="http://andersonxp.tumblr.com/">Anderson dos Santos</a> about this Plug-in. The article was published by <a title="Testing Experience" href="http://www.testingexperience.com/">Testing Experience</a> in its December issue. The issue's topic is Open Source Tools. You can download the whole magazine from <a title="Testing Experience" href="http://www.testingexperience.com/">Testing Experience website</a> (I highly recommend downloading the magazine, there are some great articles there!).
<p style="text-align: center;"><a href="{{ assets.cover12_12_10 }}"><img class="size-full wp-image-515  aligncenter" title="cover12_12_10" src="{{ assets.cover12_12_10 }}" alt="" width="212" height="300" /></a></p>
Since we wrote the article we changed only the way we parsed the test reports. Instead of parsing only TAP report files, we decided implement TAP, JUnit and TestNG parsers. In the future we plan adding more parsers to others *nits and Selenium report files.

The plug-in is being used to automate acceptance tests in a CRM system that was developed by <a title="Sysmap Solutions" href="http://www.sysmap.com.br">Sysmap Solutions</a>. I will write about the automation process, experiences learned and mistakes to be avoided in future projects as soon as we finish writing the automated tests and setting up the Selenium Farm.

In the following days I'll be writing more tutorials, guides and recording some video tutorials. In February of the next year this automation solution will be presented in the <a title="Belgium Testing Days" href="http://www.belgiumtestingdays.com/">Belgium Testing Days</a> event.
<p style="text-align: center;"><a href="{{ assets.btd2011_speakers_banner_1 }}"><img class="size-full wp-image-519  aligncenter" title="btd2011_speakers_banner_1" src="{{ assets.btd2011_speakers_banner_1 }}" alt="" width="200" height="100" /></a></p>

Cheers