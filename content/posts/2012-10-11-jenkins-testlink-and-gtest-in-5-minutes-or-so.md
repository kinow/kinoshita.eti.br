---
categories:
- blog
date: "2012-10-11T00:00:00Z"
tags:
- jenkins
- testlink
- c++
- software quality
title: Jenkins, TestLink and GTest in 5 minutes (or so)
---

This is a 5 minutes guide on creating a job for a C++ project in <a href="http://www.jenkins-ci.org" title="Jenkins CI">Jenkins</a> with <a href="http://code.google.com/p/googletest" title="GoogleTest">GoogleTest</a> and reporting the test results back to <a href="http://www.teamst.org" title="TestLink">TestLink</a>, with <a href="https://wiki.jenkins-ci.org/display/JENKINS/TestLink+Plugin" title="Jenkins TestLink Plug-in">testlink-plugin</a>. 

## The test project with GoogleTest

For this simple guide we will use the samples that come with <a href="https://github.com/kinow/gtest-tap-listener" title="GTest TAP Listener">GTest TAP Listener</a>. You can get the code from GitHub with `git clone git://github.com/kinow/gtest-tap-listener.git`. Take a look at `gtest-tap-listener/samples/src/`, there you will find two C++ files: `gtest_main.cc` and `gtest_testHelloWorld.cc`.

`gtest_main.cc` has the <a href="http://code.google.com/p/googletest/wiki/Primer#Writing_the_main()_Function" title="GTest main function">main function</a>, and executes the test suite. And `gtest_testHelloWorld.cc` has the test cases and tests. Take note of the test case and tests names.

{{< showimage
  image="screenshot_001.png"
  alt=""
  caption=""
  style=""
>}}

<!--more-->

## Configure TestLink

OK. Now create a project in TestLink or use an existing one. And the same goes for Test Suite, Test Cases and Test Plan. The only think you have to take care is to add a custom field, and use the GTest test case names. Take a look at the picture below to have a better idea.

{{< showimage
  image="screenshot_003.png"
  alt=""
  caption=""
  style=""
>}}

{{< showimage
  image="screenshot_002.png"
  alt=""
  caption=""
  style=""
>}}

If you have trouble configuring TestLink, take a look at <a href="http://tupilabs.com/books/jenkins-testlink-plugin-tutorial/en/ch04s02.html" title="Chapter 4.2">this chapter</a> of <a href="http://tupilabs.com/books/jenkins-testlink-plugin-tutorial/en/" title="Jenkins TestLink Plug-in Tutorial">Jenkins TestLink Plug-in Tutorial</a>.

## Configure Jenkins

Almost there, now the only step: <strong>configure Jenkins</strong>! Install Jenkins TestLink Plug-in, go to the global configuration and add your TestLink installation. Don't forget the devKey in order to let Jenkins access TestLink.

Now create a job, configure Git Plugin to get the code from `git://github.com/kinow/gtest-tap-listener.git`. Add a build step to `Invoke TestLink`. There will be three sections: <strong>TestLink Configuration</strong>, <strong>Test Execution</strong> and <strong>Result Seeking Strategy</strong>.

{{< showimage
  image="screenshot_004.png"
  alt=""
  caption=""
  style=""
>}}

Under TestLink Configuration, fill in your TestLink configuration, test project, test plan, any build name
of your choice (you can try gtest-build-$BUILD_ID ;) and the name (not the label) of your custom field.
In Test Execution, a `make --directory=samples` will build the project, and then finally you can run
`./gtest-tap-listener-samples`. This executes **GTest using a TAP listener to output TAP**.

As your test execution generated some TAP files, let's use a `Result Seeking Strategy` that reads TAP files:
<strong>TAP file name</strong>. Just use `samples/*.tap` as `Include Pattern` and put your custom field
name as `Key Custom Field`.</em>

Run your build, and voil&agrave;  :-)

{{< showimage
  image="screenshot_2012_10_11.png"
  alt=""
  caption=""
  style=""
>}}

As an exercise, you can try to use Jenkins TestLink Plug-in to display your TAP results. This blog post has been
created after [JENKINS-15486](https://issues.jenkins-ci.org/browse/JENKINS-15486).

## Other resources

- [http://www.testanything.org](http://www.testanything.org)
- [https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin](https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin)
