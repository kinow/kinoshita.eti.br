---
title: Cyclic Workflows with Prefect
layout: post
categories:
- blog
tags:
- opensource
note: |
    This post is a sequel to last month's [Cyclic Workflows with Cylc and StackStorm](/2021/10/01/cyclic-workflows-with-cylc-and-stackstorm.html)
---

<img
src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/prefect.svg"
alt="Prefect logo"
class="center-aligned"
/>

Last month I wrote about
[Cyclic Workflows with Cylc and StackStorm](/2021/10/01/cyclic-workflows-with-cylc-and-stackstorm.html)
and how few workflow managers support cyclic workflows.

I was surprised today while reading Prefect documentation to see this paragraph:

> Most workflow frameworks act as if looping is impossible (stressing the Acyclic part of the DAG),
> but it's actually trivial to implement. We simply dynamically unroll the loop, similar to how RNN
> gradients are sometimes computed.

<img
src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/Example-of-Unrolled-RNN-on-the-forward-pass.png"
alt="Example of Unrolled RNN on the forward-pass (image from https://machinelearningmastery.com/rnn-unrolling/)"
class="center-aligned"
/>

<small>Image source: <a href="https://machinelearningmastery.com/rnn-unrolling/">A Gentle Introduction to RNN Unrolling
</a></small>

The API for cyclic workflows of Prefect appears to be limited when compared with Cylc and
StackStorm, but they have a lot of integrations, and good documentation.

I had to re-work the example from the previous post a bit, as using `prep` as entry point
resulted in `prep` present in every cycle. Their dependency and constraints algorithm is
probably re-executing the whole cycle, or there may be another way to have optional tasks
that I couldn't find.

```python
#!/bin/bash
# file: workflow.py
import prefect
from prefect import task, Flow
from prefect.engine.signals import LOOP
import time

INTERVAL=1


@task
def prep():
    cycle = prefect.context.get("task_loop_count", 1)
    logger = prefect.context.get("logger")
    time.sleep(INTERVAL)
    logger.info(f"prep.{cycle} says hi!")

@task
def foo():
    cycle = prefect.context.get("task_loop_count", 1)
    if cycle == 1:
        prep.run()
    logger = prefect.context.get("logger")
    time.sleep(INTERVAL)
    logger.info(f"foo.{cycle} says hi!")
    bar.run()
    raise LOOP()

@task
def bar():
    cycle = prefect.context.get("task_loop_count", 1)
    logger = prefect.context.get("logger")
    time.sleep(INTERVAL)
    logger.info(f"bar.{cycle} says hi!")


with Flow("hello-flow") as flow:
    foo()

flow.run()
#flow.visualize() # need to pip install prefect['viz']
```

Running the workflow is really simple (simpler than both
Cylc and StackStorm): `python workflow.py`

```bash
(venv) kinow@ranma:/tmp$ python workflow.py 
[2021-11-08 21:37:20+1300] INFO - prefect.FlowRunner | Beginning Flow run for 'hello-flow'
[2021-11-08 21:37:20+1300] INFO - prefect.TaskRunner | Task 'foo': Starting task run...
[2021-11-08 21:37:21+1300] INFO - prefect.foo | prep.1 says hi!
[2021-11-08 21:37:22+1300] INFO - prefect.foo | foo.1 says hi!
[2021-11-08 21:37:23+1300] INFO - prefect.foo | bar.1 says hi!
[2021-11-08 21:37:24+1300] INFO - prefect.foo | foo.2 says hi!
[2021-11-08 21:37:25+1300] INFO - prefect.foo | bar.2 says hi!
[2021-11-08 21:37:26+1300] INFO - prefect.foo | foo.3 says hi!
[2021-11-08 21:37:27+1300] INFO - prefect.foo | bar.3 says hi!
[2021-11-08 21:37:28+1300] INFO - prefect.foo | foo.4 says hi!
[2021-11-08 21:37:29+1300] INFO - prefect.foo | bar.4 says hi!
...
```

I had seen the RNN graph unrolling algorithm mentioned in their documentation
while working on [decyclify](https://github.com/kinow/decyclify). I believe more
workflow managers will start supporting cyclic workflows soon. It adds some
complexity to the code, but so it does add dependency management, good logging,
configuration, distributed execution, and so on.

<img
src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/graph-unroll.png"
alt="Decyclify algorithm (image from https://github.com/kinow/decyclify)"
class="center-aligned"
/>

I am not sure if the way I linked tasks is following best practices for Prefect. There
may be better ways so that Prefect can handle restarting workflows, for instance. But
if you want to run cyclic workflows, now you have —at least— three options.
