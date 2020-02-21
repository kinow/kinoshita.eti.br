---
date: 2017-01-03 11:40:03 +1300
layout: post
tags:
- c++
- krita
- programming
- opensource
categories:
- blog
title: Contributing to Krita
---

As I mentioned in the [last post]({% post_url 2017-01-02-debugging-an-application-that-freezes-the-x-server %}),
I have been learning Qt and using C and C++ again.
Since I used C and C++ more during university (about 10 years ago, phew), decided
to read real code.

I used Photoshop, Illustrator, and Fireworks a lot when I was younger and had more
time to spend drawing. But some time ago I switched to Inkscape for vector graphics,
which I use at work for presentations. So it was only natural to try Krita now.

Since I was going to try Krita, I thought why not check out and build from source, and then
in case I found any bugs, contribute back? Or maybe from time to time triage issues,
find low hanging ones, and send a patch?

Well, turns out the Krita project has a great community, and it is super easy to send
contributions. So far I submitted three patches, some were included in 3.x releases.

* <a href="https://bugs.kde.org/show_bug.cgi?id=366741">https://bugs.kde.org/show_bug.cgi?id=366741</a>
* <a href="https://bugs.kde.org/show_bug.cgi?id=364208">https://bugs.kde.org/show_bug.cgi?id=364208</a>
* <a href="https://bugs.kde.org/show_bug.cgi?id=374451">https://bugs.kde.org/show_bug.cgi?id=374451</a>

While the patches are rather small, they are suggestions on how to fix memory
segmentation faults, or strange behaviours in the interface. For these issues,
I had to learn more about Qt components, signals and emitting events, and,
of course, work with pointers, arrays, Qt data structures, etc. In other words,
lots of (geek) fun!

In other words, by contributing to Krita, I am not only helping the project
and giving a little back to the community, but also refreshing my memory on
C and C++, and slowly learning Qt - which is not very hard if you worked with
Swing/AWT, Delphi, Visual Basic, Gtk, etc.

What are you waiting to contribute to Krita? The developers that maintain the
project answer tickets and questions posted to [reddit](https://reddit.com/r/krita)
in a good time, and are extremely easy to work with.

Read more [here](http://www.davidrevoy.com/article193/guide-building-krita-on-linux-for-cats) how to build from source, and
[here](https://krita.org/en/get-involved/developers/) on how to submit patches.

Happy hacking!
