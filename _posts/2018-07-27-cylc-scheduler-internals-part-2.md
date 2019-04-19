---
date: 2018-07-27 00:25:37 +1300
layout: post
tags:
- cylc
- python
- opensource
title: Cylc Scheduler Internals - Part 2
---

This is part 2, in a series of posts about [Cylc](https://cylc.github.io/cylc)
internals. The [part 1]({% post_url 2018-07-14-cylc-scheduler-internals-part-1 %})
had the beginning of the workflow. And here we will have the continuation, from
the moment the method `configure()` is called.

*NB: this is a post to remember things, not really expecting to give someone enough
information to be able to hack the Cylc Scheduler (though you can and would have fun!).*

<img style="display: inline; width: 100%;" class="ui image" src="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/cylc-scheduler_configure.png"  />

<!--more-->

The `configure` method is responsible for configuring the Suite Server Program. Which
means it will interact with the configuration singletons to retrieve the necessary
configuration for the program.

It also interacts with other objects that store state, and also creates basic data structures
and objects required for a suite program (e.g. Queues).

This is also where the **contact file** is created, as well as the HTTP server.

You can download the <a href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/cylc-scheduler_configure-src.png">source file</a> for the diagram used in this post, and edit it
with [draw.io](https://draw.io).
