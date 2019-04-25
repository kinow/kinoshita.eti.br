---
date: 2018-08-18 18:27:37 +1300
layout: post
note: 'NB: this is a post to remember things, not really expecting to give someone
  enough information to be able to hack the Cylc Scheduler (though you can and would
  have fun!).'
tags:
- cylc
- python
- opensource
title: Cylc Scheduler Internals - Part 3
---

This is the part 3, in a series of posts about [Cylc](https://cylc.github.io/cylc)
internals. The [part 1]({% post_url 2018-07-14-cylc-scheduler-internals-part-1 %})
had the beginning of the workflow. [part 2]({% post_url 2018-07-27-cylc-scheduler-internals-part-2 %})
documented from the moment the method `configure()` is called. This post will
continue right after the `continue()` method returns, going on with the next method: `run()`.

<p style='text-align: center;'>
<a href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/cylc-scheduler_run.png">
<img style="display: inline; width: 100%;" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/cylc-scheduler_run.png"  />
</a>
</p>

<!--more-->

At this point, the Suite Server program must have been initialized, with the
objects that it requires, and with everything configured. So this method is the one
that starts the whole work on the tasks &amp; proxies.

The runahead points, i.e. what are the next available cycle points, are calculated
and scheduled. In the scheduling, tasks are queued for execution.

Most of the interesting action takes place when `process_task_pool()` is called,
and in the `submit_task_jobs()`. The latter is a method from `TaskJobManager`, and
it is here where - in this case - my shell command is executed through a temporary
shell script file.

The graph was created from the initial execution of a suite that was starting from
scratch (they can also be reinitialized). If there are multiple tasks waiting,
or if a suite was restarted, the diagram would look considerably different.

You can download the
<a href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/cylc-scheduler_run-src.xml">source file</a>
for the diagram used in this post, and edit it with [draw.io](https://draw.io).
