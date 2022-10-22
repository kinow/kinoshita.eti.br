---
categories:
- blog
date: "2016-09-03T00:00:00Z"
tags:
- programming
- jenkins
- software quality
title: Performance problems in Jenkins TAP Plug-in &mdash; part 1
---

[JENKINS-17887](https://issues.jenkins-ci.org/browse/JENKINS-17887) reports performance problems in the [Jenkins TAP Plug-in](https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin). It also lists a series of suggestions on how to improve the Jenkins TAP Plug-in performance. On this initial post, we will get a general idea of how the plug-in performs for large projects.

[BioPerl](http://bioperl.org/) has over 21K tests. That should be enough for giving an initial idea of CPU, memory and disk usage for the plug-in.


```shell
git clone https://github.com/bioperl/bioperl-live.git
cd bioperl-live
sudo cpanm  -vv --installdeps --notest .
sudo cpanm Set::Scalar Graph::Directed XML::LibXML XML::SAX \
    SVG XML::Parser::PerlSAX Convert::Binary::C XML::SAX::Writer \
    XML::DOM::XPath Spreadsheet::ParseExcel XML::SAX::Writer \
    XML::DOM HTML::TableExtract XML::Simple Test::Pod DBI
prove -r t/ -a tests.tar.gz

All tests successful.
Files=325, Tests=21095, 94 wallclock secs ( 2.47 usr  0.55 sys + 88.29 cusr  3.85 csys = 95.16 CPU)
Result: PASS
```

When the test results are parsed, the plug-in also copies TAP files over to the master, in a folder called *tap-master-files*.

The BioPerl tests are not really big, just **1.7M**. It gets doubled as there will be the workspace copy, and the tap-master-files directory copy, so **3.4M**.

But several objects get created in memory, and persisted into the build.xml job file. BioPerl generates a build.xml file with **11M**. So **less than 15M**. But the build.xml contains objects that are read via XStream by Jenkins and into the memory.

The build page with the graph, and the other two test result pages are rendering in more than 10 seconds in my computer. But the CPU load is OK, so a closer look at the memory use would probably be more interesting.

{{< showimage
  image="JENKINS-17887-yourkit1.png"
  alt="JENKINS-17887 YourKit profiler"
  caption="JENKINS-17887 YourKit profiler"
  style=""
>}}

The image shows one of the screens in YourKit profiler, where it is possible to see that **org.tap4j.plugin.model.TapTestResultResult** has over 6 million objects.

One build.xml for the BioPerl project gets over 80K entries for the TestResult object.

```shell
grep "org.tap4j.model.TestResult" builds/1/build.xml -o | wc -l
84522
```

This happens because each TAP file may contain multiple test results (lines with test results). Each of these test results gets turned into a Java object and loaded by the plug-in. So when loading the test result pages, Jenkins needs to wait until all these objects have been parsed, deserialized and read into the memory.

The next post will continue on code improvements, and another benchmark.

Happy profiling!
