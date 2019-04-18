---
title: 'Running BDD tests from TestLink in Jenkins'
id: 1204
author: kinow
tags: 
    - testlink
    - jenkins
    - software quality
category: 'jenkins'
time: '14:26:08'
---
<p>Last night and this morning I spent some time working on running <a href="http://en.wikipedia.org/wiki/Behavior-driven_development" title="BDD">BDD</a> tests that were created in <a href="http://www.teamst.org" title="TestLink">TestLink</a> in <a href="http://jenkins-ci.org" title="Jenkins CI">Jenkins</a>, using <a href="https://wiki.jenkins-ci.org/display/JENKINS/TestLink+Plugin" title="Jenkins TestLink Plugin">testlink-plugin</a>.</p>

<p>Similar integration has already been proposed in <a href="http://www.sqaopen.net/blog/en/?tag=jinfeng" title="JinFeng - by Olivier Renault">JinFeng</a>, by Olivier Renault. Basically, you write BDD stories in TestLink (a story goes into the Test Case summary), Jenkins retrieves these stories and executes them using a skeleton project.</p>

<div class='row'>
<div class="ui container" style='text-align: center;'>
<figure>
<a href="{{assets.tl_bdd}}" rel="prettyPhoto" class="thumbnail" title="TestLink BDD">
<img class="ui fluid image" src="{{assets.tl_bdd}}" alt="TestLink BDD" />
</a>
<figcaption>TestLink BDD</figcaption>
</figure>
</div>
</div>

<p>There are many ways to use BDD. In some of them you write code like Java, Ruby or Perl, and in others you write a DSL. I started working with JBehave, but for this integration, I preferred to use a <a href="http://en.wikipedia.org/wiki/Domain-specific_language" title="DSL">DSL</a> - as TestLink doesn't maintain source code, only test cases -, so I switched to <a href="http://www.easyb.org" title="easyb">easyb</a>.</p>

<!--more-->

<p>There are many pros and cons in this integration, and a lot of work to do in the existing BDD tools, in TestLink and in the testlink-plugin too. I will write more about it in details later, but here's a short list of things I've noted to work on the integration:</p>

<ul>
	<li>easyb reports have to be converted to TestNG, TAP or JUnit formats, or a new results seeking strategy will have to created for testlink-plugin</li>
	<li>TestLink doesn't store the stories correctly. In my test job in Jenkins, I had to use some Perl one liners to strip HTML and sanitize the string (take a look below)</li>
</ul>

{% geshi 'shell' %}echo $TESTLINK_TESTCASE_SUMMARY | perl -pe 's|\&lt;br \/\&gt;|\n|g' | perl -pe 's|\&lt;br\/\&gt;|\n|g' | perl -pe 's|\&lt;\/div\&gt;|\n|g' | sed -e 's/&lt;[a-zA-Z\/][^&gt;]*&gt;//g' | perl -MHTML::Entities -le 'while(&lt;&gt;) {print decode_entities($_);}' | perl -pe 's|^\s+||' | perl -pe 's|\xA0||g' &gt; &quot;$TESTLINK_TESTCASE_EASYB_FILENAME.story&quot;{% endgeshi %}

<div class='row'>
<div class="ui container" style='text-align: center;'>
<figure>
<a href="{{assets.jenkins_bdd}}" rel="prettyPhoto" class="thumbnail" title="Jenkins BDD">
<img class="ui fluid image" src="{{assets.jenkins_bdd}}" alt="Jenkins BDD" />
</a>
<figcaption>Jenkins BDD</figcaption>
</figure>
</div>
</div>

<p>I'm working on a <a href="{{ pcurl('2012/10/25/a-quick-view-on-wordpress-mantis-and-jenkins-plug-in-api') }}" title="A quick view on WordPress, Mantis and Jenkins plug-in API">Plug-in API proposal</a> for TestLink, and I can already imagine a few places where we could use a plug-in and that would help in the BDD integration.</p>

<p>A test case could use a plug-in to retrieve its content from a git repository, for instance. So the BDD could be stored/versioned in GitHub, and written in any language. And it would be displayed by the plug-in as if it was the Test Case summary in TestLink.</p>

<p>You can get the idea of the integration from the screen shots in this post. The source code for the skeleton project is available in this repository - <a href="https://github.com/kinow/easyb-sandbox" title="https://github.com/kinow/easyb-sandbox">https://github.com/kinow/easyb-sandbox</a>. I used the examples from <a href="http://www.easyb.org/storyexmpls.html" title="http://www.easyb.org/storyexmpls.html">easyb website</a>.</p>