---
layout: post
tags:
- testlink
- jenkins
- software quality
categories:
- blog
title: Running BDD tests from TestLink in Jenkins
---

Last night and this morning I spent some time working on running
[BDD](http://en.wikipedia.org/wiki/Behavior-driven_development) tests that were created in
[TestLink](http://www.teamst.org) in [Jenkins](http://jenkins-ci.org), using
[testlink-plugin](https://wiki.jenkins-ci.org/display/JENKINS/TestLink+Plugin).

Similar integration has already been proposed in [JinFeng](http://www.sqaopen.net/blog/en/?tag=jinfeng),
by Olivier Renault. Basically, you write BDD stories in TestLink (a story goes into the Test Case summary),
Jenkins retrieves these stories and executes them using a skeleton project.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/tl_bdd.png">

There are many ways to use BDD. In some of them you write code like Java, Ruby or Perl, and in others you write a DSL. I started working with JBehave, but for this integration, I preferred to use a <a href="http://en.wikipedia.org/wiki/Domain-specific_language" title="DSL">DSL</a> - as TestLink doesn't maintain source code, only test cases -, so I switched to <a href="http://www.easyb.org" title="easyb">easyb</a>.

<!--more-->

There are many pros and cons in this integration, and a lot of work to do in the existing BDD tools, in TestLink and in the testlink-plugin too. I will write more about it in details later, but here's a short list of things I've noted to work on the integration:

<ul>
	<li>easyb reports have to be converted to TestNG, TAP or JUnit formats, or a new results seeking strategy will have to created for testlink-plugin</li>
	<li>TestLink doesn't store the stories correctly. In my test job in Jenkins, I had to use some Perl one liners to strip HTML and sanitize the string (take a look below)</li>
</ul>

```shell
echo $TESTLINK_TESTCASE_SUMMARY | perl -pe 's|\&lt;br \/\&gt;|\n|g' | perl -pe 's|\&lt;br\/\&gt;|\n|g' | perl -pe 's|\&lt;\/div\&gt;|\n|g' | sed -e 's/&lt;[a-zA-Z\/][^&gt;]*&gt;//g' | perl -MHTML::Entities -le 'while(&lt;&gt;) {print decode_entities($_);}' | perl -pe 's|^\s+||' | perl -pe 's|\xA0||g' &gt; &quot;$TESTLINK_TESTCASE_EASYB_FILENAME.story&quot;
```

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/jenkins_bdd.png">

I'm working on a [Plug-in API proposal]({% post_url 2012-10-25-a-quick-view-on-wordpress-mantis-and-jenkins-plug-in-api %})
for TestLink, and I can already imagine a few places where we could use a plug-in and that would help in the
BDD integration.

A test case could use a plug-in to retrieve its content from a git repository, for instance. So the BDD could be
stored/versioned in GitHub, and written in any language. And it would be displayed by the plug-in as if it was
the Test Case summary in TestLink.

You can get the idea of the integration from the screen shots in this post. The source code for the skeleton project
is available in this repository - [https://github.com/kinow/easyb-sandbox](https://github.com/kinow/easyb-sandbox).
I used the examples from [easyb website](http://www.easyb.org/storyexmpls.html).
