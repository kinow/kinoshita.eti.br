---
date: 2018-08-12 17:55:44 +1300
layout: post
tags:
- apache software foundation
- java
- apache commons
- image processing
- opensource
title: Use of Logging in Java Image Processing libraries
---

For [IMAGING-154](https://issues.apache.org/jira/browse/IMAGING-154) I was trying to think in a solution
for the [existing `Debug`](https://github.com/apache/commons-imaging/blob/d2ec76bd10f30c39ae5180ede1254908e76045f0/src/main/java/org/apache/commons/imaging/util/Debug.java)
class. This class was the issue of discussion during a
[previous 1.0 release vote thread](https://markmail.org/thread/ak3hcka7piykxixz#query:+page:1+mid:ppgxbhjx3opqlixj+state:results).

<!--more-->

Initially I tried simply changing the class a bit, and make it configurable, so that we could keep it -
as there is a valid use case for having a class that collects information during the image processing
algorithms were applied.

And for me, the next step would naturally be to remove the use of `System.out`, as the `Debug` class
would now have a `PrintStream` that could be `System.out` or something else.

That's when I realized in the current version of Apache Commons Imaging (n&eacute;e Sanselan) uses
`System.out` when debugging, but also when it wants to enable a
[&ldquo;_verbose_&rdquo; mode](https://github.com/apache/commons-imaging/blob/d2ec76bd10f30c39ae5180ede1254908e76045f0/src/main/java/org/apache/commons/imaging/formats/gif/GifImageParser.java#L798)
in some classes.

I am using this post to collect a few cases, and check what other image processing images
are doing with regards to logging.

**Library**|**Logger**
:-----:|:-----:
Java ImageIO|No logging (exceptions only)
im4java|No logging (exceptions only)
opencv JNI|No logging (exceptions only)
GeoSolutions ImageIO-Ext|java.util.logging
Catalano|java.util.logging
Apache PDFBox JBIG2|Custom Logger
ImageJ2|SciJava Logger
Fiji|SLF4J + logback
OpenJPEG|Custom Logger
imgscalar|System.out
Apache Commons Imaging|System.out
Sanselan|System.out
Marvin|System.out
Processing|System.out
