---
categories:
- blog
date: "2012-10-16T00:00:00Z"
tags:
- jenkins
- c++
- test anything protocol
title: Adding coverage reports in Jenkins with GoogleTest and gcovr
---

After the [last post]({% post_url 2012-10-11-jenkins-testlink-and-gtest-in-5-minutes-or-so %}) about
[GoogleTest](http://code.google.com/p/googletest/) and [TestLink](http://www.teamst.org) using
[Jenkins TestLink Plug-in](https://wiki.jenkins-ci.org/display/JENKINS/TestLink+Plugin), I received an e-mail
asking about [coverage](http://en.wikipedia.org/wiki/Code_coverage) with GoogleTest and
[Jenkins](http://www.jenkins-ci.org). I've just updated the
[Makefile](https://github.com/kinow/gtest-tap-listener/blob/master/samples/Makefile) in the samples
directory, of the [GoogleTest TAP listener project](https://github.com/kinow/gtest-tap-listener),
to output coverage data.

Basically, you have to add the compiler flags `-fprofile-arcs -ftest-coverage` and link the executable with
`-lgcov`. Take a look at the project's Makefile and you'll notice how simple it is. In order to have Jenkins
interpreting your coverage report, you'll have to convert it to [cobertura](http://cobertura.sourceforge.net)
XML. There is a Python utility that can be used for this: [gcovr](https://software.sandia.gov/trac/fast/wiki/gcovr).
Download it and copy it to somewhere where Jenkins can execute it (e.g.: `/usr/local/bin`).

Now, if you've followed the instructions from the previous post, you should have a job that reports your GoogleTest
tests from Jenkins to TestLink using the plug-in, and is downloading the source code from GitHub. Add an extra build
step (Shell) to execute `gcovr`.

<!--more-->

```shell
gcovr -x -r samples/src > coverage.xml
```

<img class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/screenshot_0031.png">

This should produce a file coverage.xml in your build workspace. The last step is add cobertura post build step.
Of course you'll need [Jenkins Cobertura Plug-in](https://wiki.jenkins-ci.org/display/JENKINS/Cobertura+Plugin)
(quick tip: if you are using the newest Jenkins, you can install it without restarting, it works well).
Simply add the cobertura post build step and make sure to use an include pattern that matches your output file from
gcovr (e.g.: **/coverage.xml).

Voil&agrave; , you should now have coverage reports in Jenkins that looks like the image below.

<img class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/screenshot_0011.png">

<img class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/screenshot_0021.png">

A final note, is that we used an example project bundled with GoogleTest TAP Listener, and is not very useful,
as it has no other classes being tested. In a real world project, you'll have many classes that you want to coverage,
while other you'd prefer to omit from the report. You can do so by using the `-e` gcovr flag. For more, try
`gcovr --help`.

Hope that helps, have fun!
