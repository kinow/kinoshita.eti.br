---
title: 'Debugging an application that freezes the X server'
author: kinow
tags:
    - c++
    - krita
    - opensource
    - programming
category: 'blog'
time: '00:39:03'
---

Some time ago, I decided to start writing C++ again, and picked Krita for that.
Krita is written in C++ and Qt. The [bug I was working on](https://bugs.kde.org/show_bug.cgi?id=366741)
involved a memory issue when changing the UI.

The problem was that this UI change would result in, not only Krita, but the whole
X server freezing. My set up was basically Ubuntu 16.04.1 LTS, with Eclipse, Qt5,
and the latest version of Krita checked out via git.

Initially I spent some time looking at the logs, tracing the binary, even downloaded
some Qt utility tools to look at the events and what was happening with the application
when it froze.

However, eventually I realized I was going to spend more time on this part of the
issue, rather than on the memory bug. So decided to look for a work-around.

Thankfully someone else blogged about a similar issue and saved me a lot of time :-)
Here's how I did it, following the instructions in
[this blog post](http://www.geany.org/manual/gtk/gtk-faq/x462.html).

```shell
$ sudo apt-get install xnest -y
$ cd krita_install/
$ Xnest :10
$ twm -display :10
$ export DISPLAY=:10
$ ./krita
```

That's it. You should have Krita running in a separate window, with Xnest, and within
this window the twm window manager running. So when it freezes, at least you can still
debug your application in Eclipse or whatever IDE you prefer.

Happy hacking!