---
title: Cyclic Workflows with Cylc and StackStorm
layout: post
categories:
- blog
tags:
- opensource
- cylc
note: |
    Most workflow managers focus on the DAG. Very few support cyclic workflows.
---

If you look for a workflow manager that supports Directed Cyclic Graphs, you may be surprised
to see it is rarely mentioned.

I have seen only two workflow managers that support cyclic workflows.
[Cylc](https://cylc.github.io/) and [StackStorm](https://stackstorm.com/). I won't
enter into details about these two tools, but I must note that I worked on Cylc
during my employment with NIWA, in New Zealand.

In this post I will only show a very simple workflow called `five` first using
Cylc, and then the same workflow with StackStorm.

## Cylc

First let's take a look at the source code of this workflow with Cylc 8 and plot it.

```ini
[scheduling]
  cycling mode = integer
  initial cycle point = 1
  [[queues]]
     [[[default]]]
       limit = 1
  [[graph]]
    R1 = "prep => foo"
    P1 = "foo[-P1] => foo => bar"

[runtime]
  [[root]]
      script="sleep 5"
  [[prep]]
  [[foo]]
  [[bar]]
```

The part `"foo[-P1] => foo => bar"` is where the recursion occurs, creating
a cycle in the workflow.

<img
  src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/five-graph-cylc.png"
  alt="workflow five plot - cylc"
  class="center-aligned"
/>

Installing Cylc requires just `pip install cylc-flow`. After that, with the workflow
installed, we are ready to run it.

```bash
cylc install -c ~/cylc-src/five --flow-name five
cylc play --no-detach five/run1
```

The workflow will run forever, incrementing the cycle points, and triggering the tasks
in the `five` workflow source. So you will have `foo.1` (foo in the first cycle point),
that triggers both `bar.1` and also `foo.2` (foo in the second cycle point) and so it
goes.

## StackStorm

StackStorm requires more work to get everything up and running. Luckily they provide
a Docker Compose installation. So after the servers have been started with Docker
we are ready to create a “pack” (a neat way to organize separate installation files).

```bash
mkdir -p /opt/stackstorm/packs/kinow/
touch /opt/stackstorm/packs/kinow/pack.yaml
```

```yaml
---
name : kinow
description: kinow
version: 1.0.0
author: kinow
email: kinow@localhost
```

And install the new pack.

```bash
st2 pack install file:///opt/stackstorm/packs/kinow
```

Now we create a new workflow and an action to run the workflow — I think
this step is optional, and you could have just an action but I was following
one section of the docs that had it this way.

```bash
mkdir -p /opt/stackstorm/packs/kinow/actions/workflows
touch /opt/stackstorm/packs/kinow/actions/five.yaml
touch /opt/stackstorm/packs/kinow/actions/workflows/five.yaml
```

```yaml
---
name: five
pack: kinow
description: five
runner_type: orquesta
entry_point: workflows/five.yaml
enabled: true
```

And now create the action in StackStorm, so we can run it via command line
or with the UI.

```bash
st2 action create /opt/stackstorm/packs/kinow/actions/five.yaml 
```

And here's the `five` workflow source for StackStorm, producing something very
similar (if no identical) to the graph produced by Cylc 8.

```yaml
version: 1.0
description: five
tasks:
  prep:
    action: core.local cmd="sleep 5"
    next:
      - when: <% succeeded() %>
        do:
          - foo
  foo:
    action: core.local cmd="sleep 5"
    next:
      - when: <% succeeded() %>
        do:
          - foo
          - bar
  bar:
    action: core.local cmd="sleep 5"
```

Note that `foo` is calling itself, creating a cycle in the workflow. And to run the
workflow:

```bash
st2 run kinow.five
```

The StackStorm UI does not appear to support showing the graph of the workflow
static or dynamically. But there is a community contributed UI called
[rehearsal](https://github.com/trstruth/rehearsal/) that plots an Orquesta
workflow given its source.

<img
  src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/five-graph-stackstorm-rehearsal.png"
  alt="workflow five plot - stackstorm"
  class="center-aligned"
/>

## Final notes

Both Cylc and StackStorm support Directed Cyclic Graphs in workflows, which is
really rare amongst workflow managers (or workflow standards, as I think WDL/CWL
also do not support cyclic workflows yet.)

There are many pros and cons for each tool but that will have to be for a future
post. To finish this post here's a screenshot of the StackStorm UI, followed by
one of the Cylc 8 UI. Both showing the workflow `five`.

<img
  src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/stackstorm-ui.png"
  alt="stackstorm ui"
  class="center-aligned"
/>

<img
  src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/cylc-ui.png"
  alt="stackstorm ui"
  class="center-aligned"
/>
