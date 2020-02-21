---
date: 2016-11-05 23:27:03 +1300
layout: post
tags:
- shell script
categories:
- blog
title: Checking the operating system type in shell script
---

Last week I learned about a tool called [ShellCheck](https://github.com/koalaman/shellcheck), a tool
for static analysis of shell scripts. It reports errors like missing double quotes, use of deprecated
syntax, etc.

I decided to check some projects I contribute to, and the first issue I found was in
[Apache Jena](https://jena.apache.org):

```shell
kinow@localhost:~/Development/java/jena/jena/apache-jena/bin$ shellcheck arq

In arq line 8:
    case "$OSTYPE" in
          ^-- SC2039: In POSIX sh, OSTYPE is not supported.
```

So, in summary, the `OSTYPE` variable should not be available in POSIX shell. The case in question, where
`OSTYPE` is being used, checks for the Darwin OS type (i.e. Mac OS). Knowing how things get weird when you
use different operating systems, I decided to check and learn how `OSTYPE` works. Here's what I found.

* In Ubuntu, with /bin/bash, OSTYPE works fine (linux-gnu)
* In Ubuntu, with /bin/sh, OSTYPE is not set
* In Mac OS, with /bin/sh, OSTYPE is set (darwin15)

I checked the shells to make sure they were not pointing to symbolic links - some distributions
use a different default shell, and replace /bin/bash and/or /bin/sh by a link to another
shell. Looks like Mac OS has a POSIX shell that behaves different than Ubuntu's.

Instead of trying to find a way to use `OSTYPE`, I decided to spend some time looking at
how other projects do the same thing. And the best example I could find was
[git](https://git.kernel.org/cgit/git/git.git/tree/config.mak.uname).

Instead of relying on `OSTYPE`, git uses `uname`.

I will spend some time during the next days working on a proposal to replace the `OSTYPE`
from Apache Jena scripts, but then may have to submit more changes for the other issues
found by ShellCheck.

Happy hacking!
