---
date: 2017-03-26 11:14:03 +1300
layout: post
tags:
- c++
- krita
- programming
- opensource
title: Simulating less memory with ulimit
---

These days I was trying to reproduce [a bug in Krita](https://bugs.kde.org/show_bug.cgi?id=376382)
where it would crash when a user copied group layers between windows. It appeared that the user was
getting a segmentation fault due to the user's computer running out of memory.

I could not reproduce the issue, but my computer has 16 GB. The first thing that came to my mind was
to create a virtual machine with less memory to reproduce the issue. But I decided to spend some time
looking for a [simpler way](http://wiki.c2.com/?LazinessImpatienceHubris) of doing it.

Searching the web I found some suggestions that `ulimit` could work. After playing for a while with
`ulimit` and `htop`, and verifying the amount of memory necessary to open two files in two windows
in Krita, I came up with the following settings.

```shell
# 2550 mb in kb
ulimit -v 2550000

# 2 gb in kb
ulimit -m 2000000

# Confirm limits
ulimit -a

gdb $HOME/Development/cpp/workspace/krita_install/bin/krita
```

Then after copying a few layers from one window to another, I successfully reproduced the issue,
and could include a backtrace in the Krita issue tracking system.

&hearts; Open Source
