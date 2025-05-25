---
title: "Running Cylc workflows on BSC MareNostrum5"
date: 2025-05-25T09:38:52+03:00
categories:
  - blog
tags:
  - opensource
  - cylc
  - workflows
  - python
  - programming
images:
  - '/assets/posts/2025-04-26-running-cylc-workflows-on-bsc-marenostrum5/as-cylc-ec-venn.drawio.png'
---

> TL;DR: Using the `communication method = poll` of Cylc 8 you can easily run
> Cylc 8 workflows on BSC MareNostrum5 HPC.

A couple of years ago I gave a talk about [“HPC workflows for climate models”](https://eflows4hpc.eu/event/hpc-workflows-for-climate-models/)
at an ESiWACE3 event. There, I tried to explain in an unbiased way the differences among the workflow
managers commonly used for climate and weather, including [Autosubmit](https://autosubmit.readthedocs.io/),
[ecFlow](https://ecflow.readthedocs.io/), and [Cylc](https://cylc.github.io/). I worked with
the three workflow managers, and developed Cylc while at NIWA in New Zealand, and currently I
develop Autosubmit at the Barcelona Supercomputing Center, BSC, in Barcelona Spain.

{{< showimage
    image="as-cylc-ec-venn.drawio.png"
    alt="Venn diagram from 'HPC workflows for climate models' talk"
    caption="Venn diagram from 'HPC workflows for climate models' talk"
    style="width: auto;"
>}}

The BSC MareNostrum5 HPC has a peculiarity where its computing nodes -- where
Slurm run the heavy, resource-demanding jobs -- are not allowed to communicate back
to the HPC login nodes. I have been working at the BSC for three years and so far I
never heard about any exceptions made.

This means workflow managers where there is any communication from tasks running
on computing nodes back to where the workflow scheduler runs time out, causing
workflow runtime errors. This is a problem as ecFlow depends on the tasks telling
the server that they have finished (running the bash tailer of the task), and in
Cylc this is also a problem as by default Cylc uses a communication mode that requires
the connectivity among the worker nodes and the scheduler.

At the BSC, some time ago, I saw another project with ecFlow that ran at the
MareNostrum5 HPC without the tailer, and used some custom code in order to tell
ecFlow that the task had been finished. While this worked, I asked someone from
ECMWF -- they maintain ecFlow -- and they told me it was discouraged to manage tasks
that way. The project at the BSC has now been refactored and is using Autosubmit.

Things are simpler with Cylc. As I explained in my talk, and also offline to others,
Cylc can in fact be used in an environment with networking constraints like
the BSC MareNostrum5. The documentation of Cylc explains how to use their
[**poll communication method**](https://cylc.github.io/cylc-doc/stable/html/reference/config/global.html#global.cylc[platforms][%3Cplatform%20name%3E]communication%20method).
It is the “Polling mode” that appears right at the center of the venn diagram
at the top of this blog post.

[Domingo Manubens-Gil](https://scholar.google.es/citations?user=SmfyaeoAAAAJ) left
the BSC before I joined, but I can see from Git and from previous deliverables
for European projects that he did a lot of great work for Autosubmit. Some of his
latest works include technical reports on the possibility to run Cylc workflows
on MareNostrum5. Which also confirms that Cylc workflows can run on BSC
MareNostrum5 HPC.

But as a good engineer, I doubt most things I read until I can actually try
it or have more solid proof. And Domingo's work was published before Cylc 8
had been released. So to make sure Cylc 8 workflows run on BSC MareNostrum5,
I tried the Cylc documentation “broadcast” tutorial, which you can find
[here](https://cylc.github.io/cylc-doc/stable/html/tutorial/furthertopics/broadcast.html#broadcast-tutorial).

Prerequisites:

* Create a platform for BSC MareNostrum5 using Slurm
* Configure `global.cylc` for the communication method
* Install Cylc somewhere on BSC MareNostrum5 (I used my personal folder for a quick demo)
* Update the broadcast tutorial to use the platform created

First, my `~/.cylc/flow/8/global.cylc`:

```ini {linenos=inline hl_lines=[9] style=emacs}
[platforms]
    [[mn5]]
        cylc path = /gpfs/scratch/bsc32/<ADD-A-VALID-BSC-USER>/cylc/venv/bin/
        hosts = mn
        install target = mn
        job runner = slurm
        retrieve job logs = True

        communication method = poll
        submission polling intervals = 10*PT1M, 10*PT5M
        execution polling intervals = 10*PT1M, 10*PT5M
```

And here's the diff for the Cylc broadcast tutorial [workflow](https://github.com/cylc/cylc-doc/blob/23f5c7aad5e9501aa8c3a28485822548b944d960/src/tutorial/furthertopics/broadcast.rst):

```diff {linenos=inline style=emacs}
diff --git a/flow.cylc b/flow.cylc
index d2d1ede..52702f8 100644
--- a/flow.cylc
+++ b/flow.cylc
@@ -1,3 +1,8 @@
+#!Jinja2
+
+{% set HPC_PROJECT  =   "bsc32" %}
+{% set HPC_USER     =   "<ADD-A-VALID-BSC-USER>" %}
+
 [scheduling]
     initial cycle point = 1012
     [[graph]]
@@ -5,11 +10,27 @@
         PT1H = announce[-PT1H] => announce
 
 [runtime]
+    [[MN5]]
+        platform = mn5
+        # Wallclock
+        execution time limit = PT05M
+        # NOTE: do not set walltime here or Cylc may keep one value
+        #       while you have another one in the HPC! See the config
+        #       flow.cylc[platforms][[mn5]][[[execution time limit]]]
+        [[[directives]]]
+            --account={{ HPC_PROJECT }}
+            --qos=gp_debug
+            --partition=standard
+            --ntasks=1
+            --cpus-per-task=1
+
     [[wipe_log]]
+        inherit = MN5
         # Delete any files in the workflow's "share" directory.
         script = rm "${CYLC_WORKFLOW_SHARE_DIR}/knights" || true
 
     [[announce]]
+        inherit = MN5
         script = echo "${CYLC_TASK_CYCLE_POINT} - ${MESSAGE}" >> "${FILE}"
         [[[environment]]]
             WORD = ni
```

Once you have configured your platform and workflow, you can `cd` into
the workflow source directory and run `cylc vip --no-detach`. Then observe
the logs locally and -- optionally -- in Slurm. You should see a few jobs
being launched by Cylc. The poll interval is used to control how often
Cylc poll the current jobs and verifies their remote statuses (something
that you cannot do with Autosubmit as these values are hard-coded right now).

You can issue the `cylc broadcast` commands from the Cylc documentation tutorial
to change the message printed in the log, and play with other commands such as
`cylc cat-log`, `cylc poll`, etc. They should work fine on MN5.

```bash {linenos=inline style=emacs}
$ tail -f knights 
10120102T0400Z - We are the knights who say "ni"!
10120102T0500Z - We are the knights who say "ni"!
10120102T0600Z - We are the knights who say "ni"!
10120102T0700Z - We are the knights who say "it"!
10120102T0800Z - We are the knights who say "it"!
10120102T0900Z - We are the knights who say "it"!
```

Regarding communication with the HPC platform, the only cons comparing
with Autosubmit are that platform configuring is not fully centralized,
and Cylc does not have an equivalent of Autosubmit's wrappers (so if
you use Cylc at the BSC MareNostrum5, you will probably face long queueing
times). On the other hand, you gain advanced cycling, and fine-grained
control of several settings (like log retrieval, another thing you cannot
turn off in Autosubmit).

```bash {linenos=inline style=emacs
$ sacct --starttime 2025-05-25
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode 
------------ ---------- ---------- ---------- ---------- ---------- -------- 
21445023     wipe_log.+        gpp      bsc32          2  COMPLETED      0:0 
21445023.ba+      batch                 bsc32          2  COMPLETED      0:0 
21445023.ex+     extern                 bsc32          2  COMPLETED      0:0 
21445050     announce.+        gpp      bsc32          2  COMPLETED      0:0 
21445050.ba+      batch                 bsc32          2  COMPLETED      0:0 
21445050.ex+     extern                 bsc32          2  COMPLETED      0:0 
21445069     announce.+        gpp      bsc32          2  COMPLETED      0:0 
21445069.ba+      batch                 bsc32          2  COMPLETED      0:0 
21445069.ex+     extern                 bsc32          2  COMPLETED      0:0 
21445083     announce.+        gpp      bsc32          2  COMPLETED      0:0 
```

(p.s.: remember to stop your workflow!)
