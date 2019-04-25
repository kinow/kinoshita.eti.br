---
date: 2018-07-10 00:47:13 +1300
layout: post
tags:
- cylc
- python
- opensource
title: ImportError when debugging cylc in Eclipse
---

Since I started reading cylc's source code in Eclipse to create some
sequence diagrams, I have not been able to debug it properly without
hitting errors in some part of the program execution.

The error message was **_&ldquo;ImportError: cannot import name _remove_dead_weakref&rdquo;_**,
which was a bit enigmatic as I never heard about that function, but it seemed to be
something internal, or at least not from the project code base. And searching the Internet
did not help much.

<!--more-->

Here is the complete console output in Eclipse.

```shell
pydev debugger: starting (pid: 15124)
timeout 10 ps -opid,args 13640  # return 1

            ._.                                                       
            | |            The Cylc Suite Engine [7.7.1-37-g09c8a]    
._____._. ._| |_____.           Copyright (C) 2008-2018 NIWA          
| .___| | | | | .___|  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
| !___| !_! | | !___.  This program comes with ABSOLUTELY NO WARRANTY;
!_____!___. |_!_____!  see `cylc warranty`.  It is free software, you 
      .___! |           are welcome to redistribute it under certain  
      !_____!                conditions; see `cylc conditions`.       
2018-07-10T01:00:47+12 INFO - Suite starting: server=localhost:44444 pid=15124
2018-07-10T01:00:47+12 INFO - Cylc version: 7.7.1-37-g09c8a
2018-07-10T01:00:47+12 INFO - Run mode: live
2018-07-10T01:00:47+12 INFO - Initial point: 1
2018-07-10T01:00:47+12 INFO - Final point: None
2018-07-10T01:00:47+12 INFO - Cold Start 1
2018-07-10T01:00:47+12 DEBUG - [hello.1] -released to the task pool
2018-07-10T01:00:47+12 DEBUG - BEGIN TASK PROCESSING
2018-07-10T01:00:47+12 DEBUG - [hello.1] -waiting => queued
2018-07-10T01:00:47+12 DEBUG - 1 task(s) de-queued
2018-07-10T01:00:47+12 INFO - [hello.1] -submit-num=1, owner@host=localhost
2018-07-10T01:00:47+12 DEBUG - [hello.1] -queued => ready
2018-07-10T01:00:47+12 DEBUG - END TASK PROCESSING (took 0.023609161377 seconds)
2018-07-10T01:00:48+12 DEBUG - ['cylc', 'jobs-submit', '--debug', '--', '/home/kinow/Development/python/workspace/example-suite/log/job', '1/hello/01']
2018-07-10T01:00:48+12 ERROR - [jobs-submit cmd] cylc jobs-submit --debug -- /home/kinow/Development/python/workspace/example-suite/log/job 1/hello/01
	[jobs-submit ret_code] 1
	[jobs-submit err]
	Traceback (most recent call last):
	  File "/home/kinow/Development/python/workspace/cylc/bin/cylc-jobs-submit", line 52, in <module>
	    from cylc.batch_sys_manager import BatchSysManager
	  File "/home/kinow/Development/python/workspace/cylc/lib/cylc/batch_sys_manager.py", line 114, in <module>
	    from cylc.task_message import (
	  File "/home/kinow/Development/python/workspace/cylc/lib/cylc/task_message.py", line 26, in <module>
	    from logging import getLevelName, WARNING, ERROR, CRITICAL
	  File "/home/kinow/Development/python/anaconda2/lib/python2.7/logging/__init__.py", line 26, in <module>
	    import sys, os, time, cStringIO, traceback, warnings, weakref, collections
	  File "/home/kinow/Development/python/anaconda2/lib/python2.7/weakref.py", line 14, in <module>
	    from _weakref import (
	ImportError: cannot import name _remove_dead_weakref
2018-07-10T01:00:48+12 ERROR - [jobs-submit cmd] cylc jobs-submit --debug -- /home/kinow/Development/python/workspace/example-suite/log/job 1/hello/01
	[jobs-submit ret_code] 1
	[jobs-submit out] 2018-07-10T01:00:48+12|1/hello/01|1
2018-07-10T01:00:48+12 INFO - [hello.1] -(current:ready) submission failed at 2018-07-10T01:00:48+12
2018-07-10T01:00:48+12 ERROR - [hello.1] -submission failed
2018-07-10T01:00:48+12 DEBUG - [hello.1] -ready => submit-failed
2018-07-10T01:00:48+12 DEBUG - BEGIN TASK PROCESSING
2018-07-10T01:00:48+12 DEBUG - 0 task(s) de-queued
2018-07-10T01:00:48+12 DEBUG - END TASK PROCESSING (took 0.00175499916077 seconds)
2018-07-10T01:00:49+12 WARNING - suite stalled
```

As the current diagram I am working on has quite a few `if`'s and `else`'s, I decided
to investigate why this error was occurring. Then, after some elimination I found that
it was due to the missing Anaconda 2 entry in my `$PATH` environment variable.

I had this variable configured in a custom script I load whenever I decide to use
Anaconda 2. And reproducing the same behaviour in Eclipse was easy.


<p style='text-align: center;'>
<img style="display: inline" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/screenshot1.png" alt="A screen shot of Eclipse with source code" title="Locating the bug" />
<br/>
<small>Locating the bug</small>
</p>

Et voil&agrave;! Eclipse was happily debugging again!

<p style='text-align: center;'>
<img style="display: inline" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/screenshot2.png" alt="A screen shot of Eclipse with source code" title="Locating the bug" />
<br/>
<small>Locating the bug</small>
</p>

So if you have a similar problem, try comparing your environment variables and check if you
have some entries missing, and try adding them in Eclipse Debug configuration.

Happy cycling!
