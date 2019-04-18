---
title: 'Jenkins, TestLink and GTest in 5 minutes (or so)'
id: 1075
author: kinow
tags: 
    - jenkins
    - testlink
    - c++
    - software quality
category: 'jenkins'
time: '23:44:59'
---
<p>This is a 5 minutes guide on creating a job for a C++ project in <a href="http://www.jenkins-ci.org" title="Jenkins CI">Jenkins</a> with <a href="http://code.google.com/p/googletest" title="GoogleTest">GoogleTest</a> and reporting the test results back to <a href="http://www.teamst.org" title="TestLink">TestLink</a>, with <a href="https://wiki.jenkins-ci.org/display/JENKINS/TestLink+Plugin" title="Jenkins TestLink Plug-in">testlink-plugin</a>. </p>

<h2>The test project with GoogleTest</h2>

<p>For this simple guide we will use the samples that come with <a href="https://github.com/kinow/gtest-tap-listener" title="GTest TAP Listener">GTest TAP Listener</a>. You can get the code from GitHub with <code>git clone git://github.com/kinow/gtest-tap-listener.git</code>. Take a look at <em>gtest-tap-listener/samples/src/</em>, there you will find two C++ files: <em>gtest_main.cc</em> and <em>gtest_testHelloWorld.cc</em>.</p>

<p><em>gtest_main.cc</em> has the <a href="http://code.google.com/p/googletest/wiki/Primer#Writing_the_main()_Function" title="GTest main function">main function</a>, and executes the test suite. And <em>gtest_testHelloWorld.cc</em> has the test cases and tests. Take note of the test case and tests names.</p>

<p><a href="{{ assets.screenshot_001 }}"><img src="{{ assets.screenshot_001 }}" alt="" title="gtest_testHelloWorld.cc" width="546" height="482" class="aligncenter size-full wp-image-1083" /></a></p>

<!--more-->

<h2>Configure TestLink</h2>

<p>OK. Now create a project in TestLink or use an existing one. And the same goes for Test Suite, Test Cases and Test Plan. The only think you have to take care is to add a custom field, and use the GTest test case names. Take a look at the picture below to have a better idea.</p>

<p><a href="{{ assets.screenshot_003 }}"><img src="{{ assets.screenshot_003 }}" alt="" title="Custom Field" width="686" height="351" class="aligncenter size-full wp-image-1085" /></a></p>

<p><a href="{{ assets.screenshot_002 }}"><img src="{{ assets.screenshot_002 }}" alt="" title="Test Case with Custom Field" width="705" height="564" class="aligncenter size-full wp-image-1086" /></a></p>

<p>If you have trouble configuring TestLink, take a look at <a href="http://tupilabs.com/books/jenkins-testlink-plugin-tutorial/en/ch04s02.html" title="Chapter 4.2">this chapter</a> of <a href="http://tupilabs.com/books/jenkins-testlink-plugin-tutorial/en/" title="Jenkins TestLink Plug-in Tutorial">Jenkins TestLink Plug-in Tutorial</a>.</p>

<h2>Configure Jenkins</h2>

<p>Almost there, now the only step: <strong>configure Jenkins</strong>! Install Jenkins TestLink Plug-in, go to the global configuration and add your TestLink installation. Don't forget the devKey in order to let Jenkins access TestLink.</p>

<p>Now create a job, configure Git Plugin to get the code from <em>git://github.com/kinow/gtest-tap-listener.git</em>. Add a build step to <em>Invoke TestLink</em>. There will be three sections: <strong>TestLink Configuration</strong>, <strong>Test Execution</strong> and <strong>Result Seeking Strategy</strong>.</p>

<p><a href="{{ assets.screenshot_004 }}"><img src="{{ assets.screenshot_004 }}" alt="" title="Job Configuration" width="925" height="678" class="aligncenter size-full wp-image-1088" /></a></p>

<p>Under TestLink Configuration, fill in your TestLink configuration, test project, test plan, any build name of your choice (you can try gtest-build-$BUILD_ID ;) and the name (not the label) of your custom field. In Test Execution, a <code>make --directory=samples</code> will build the project, and then finally you can run <code>./gtest-tap-listener-samples</code>. This executes <strong>GTest using a TAP listener to output TAP</strong>.</p>

<p>As your test execution generated some TAP files, let's use a <em>Result Seeking Strategy</em> that reads TAP files: <strong>TAP file name</strong>. Just use <code>samples/*.tap</code> as <em>Include Pattern</em> and put your custom field name as <em <Key Custom Field</em>.</em></p>

<p>Run your build, and voil&agrave;  :-)</p>

<p><a href="{{ assets.screenshot_2012_10_11 }}"><img src="{{ assets.screenshot_2012_10_11 }}" alt="" title="Screenshot from 2012-10-11 23:39:03" width="1024" height="603" class="aligncenter size-large wp-image-1092" /></a></p>

<p>As an exercise, you can try to use Jenkins TestLink Plug-in to display your TAP results. This blog post has been created after <a href="https://issues.jenkins-ci.org/browse/JENKINS-15486" title="JENKINS-15486">JENKINS-15486</a>.</p>

<h2>Other resources</h2>

<ul>
	<li><a href="http://www.testanything.org" title="TAP">http://www.testanything.org</a></li>
	<li><a href="https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin" title="Jenkins TAP Plug-in">https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin</a></li>
</ul>