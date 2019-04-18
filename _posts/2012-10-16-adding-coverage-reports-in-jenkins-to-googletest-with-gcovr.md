---
title: 'Adding coverage reports in Jenkins to GoogleTest with gcovr'
id: 1103
author: kinow
tags: 
    - jenkins
    - c++
    - test anything protocol
category: 'jenkins'
time: '16:09:33'
---
<p>After the <a href="{{ pcurl('/2012/10/11/jenkins-testlink-and-gtest-in-5-minutes-or-so')}}" title="Jenkins, TestLink and GTest in 5 minutes (or so)">last post</a> about <a href="http://code.google.com/p/googletest/" title="GoogleTest">GoogleTest</a> and <a href="http://www.teamst.org" title="TestLink">TestLink</a> using <a href="https://wiki.jenkins-ci.org/display/JENKINS/TestLink+Plugin" title="Jenkins TestLink Plug-in">Jenkins TestLink Plug-in</a>, I received an e-mail asking about <a href="http://en.wikipedia.org/wiki/Code_coverage" title="Code Coverage">coverage</a> with GoogleTest and <a href="http://www.jenkins-ci.org" title="Jenkins CI">Jenkins</a>. I've just updated the <a href="https://github.com/kinow/gtest-tap-listener/blob/master/samples/Makefile">Makefile</a> in the samples directory, of the <a href="https://github.com/kinow/gtest-tap-listener" title="GTest TAP Listener">GoogleTest TAP listener project</a>, to output coverage data.</p>

<p>Basically, you have to add the compiler flags <em>-fprofile-arcs -ftest-coverage</em> and link the executable with -lgcov. Take a look at the project's Makefile and you'll notice how simple it is. In order to have Jenkins interpreting your coverage report, you'll have to convert it to <a href="http://cobertura.sourceforge.net" title="Cobertura">cobertura</a> XML. There is a Python utility that can be used for this: <a href="https://software.sandia.gov/trac/fast/wiki/gcovr" title="gcovr">gcovr</a>. Download it and copy it to somewhere where Jenkins can execute it (e.g.: <em>/usr/local/bin</em>).</p>

<p>Now, if you've followed the instructions from the previous post, you should have a job that reports your GoogleTest tests from Jenkins to TestLink using the plug-in, and is downloading the source code from GitHub. Add an extra build step  (Shell) to execute <em>gcovr</em>.</p>

<!--more-->

{% geshi 'shell' %}gcovr -x -r samples/src > coverage.xml{% endgeshi %}

<p><a href="{{assets.screenshot_0031}}"><img src="{{assets.screenshot_0031}}" alt="" title="Calling gcovr in Jenkins" width="1016" height="608" class="aligncenter size-full wp-image-1107" /></a></p>

<p>This should produce a file coverage.xml in your build workspace. The last step is add cobertura post build step. Of course you'll need <a href="https://wiki.jenkins-ci.org/display/JENKINS/Cobertura+Plugin" title="Jenkins Cobertura Plug-in">Jenkins Cobertura Plug-in</a> (quick tip: if you are using the newest Jenkins, you can install it without restarting, it works well). Simply add the cobertura post build step and make sure to use an include pattern that matches your output file from gcovr (e.g.: **/coverage.xml).</p>

<p>Voil&agrave; , you should now have coverage reports in Jenkins that looks like the image below.</p>

<p><a href="{{assets.screenshot_0011 }}"><img src="{{assets.screenshot_0011}}" alt="" title="Coverage Reports" width="1016" height="608" class="aligncenter size-full wp-image-1105" /></a></p>

<p><a href="{{assets.screenshot_0021}}"><img src="{{assets.screenshot_0021}}" alt="" title="Coverage Reports" width="1016" height="608" class="aligncenter size-full wp-image-1106" /></a></p>

<p>A final note, is that we used an example project bundled with GoogleTest TAP Listener, and is not very useful, as it has no other classes being tested. In a real world project, you'll have many classes that you want to coverage, while other you'd prefer to omit from the report. You can do so by using the <em>-e</em> gcovr flag. For more, try <em>gcovr --help</em>.</p>

<p>Hope that helps, have fun!</p>