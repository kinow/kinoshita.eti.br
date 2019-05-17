---
layout: post
tags:
- python
- cylc
- graphql
title: A look at the first implementation of GraphQL in Cylc
note: This is based on a WIP pull request, and what is being described
  here may be outdated by the time the pull request has been reviewed
  and merged. But it should still give you an idea of what
  we are working on.
---

<img class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/fancy-hands2.png" style="float: right; width: 40%;" />

For Cylc 8 we are adding an initial implementation of GraphQL, to replace the previous REST API.
Besides the technologies in the API's, another difference is that for the REST API, its main
consumer was a PyGTK GUI.

The new GraphQL API, on the other hand, will be used mainly by a Vue.js Web application. So a
few things need to be done in a different way due to the jump from Desktop GUI to Web GUI.

<!--more-->

{% include toc.html %}

## Protobuf model

The current implementation is under review in a pull request at the moment. It includes
Python libraries for GraphQL, as it is expected, but also a Protobuf data model that
can be visualized in the figure below.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/cylc-graphql-protobuf.png" />

## State management

In Cylc, the `Scheduler` object is responsible for managing Tasks in a Workflow. It does so in its
_main loop_, which is similar to the main loops in game engines. It runs periodically checking the
state of several objects, and updates them.

A new class `JobPool` is being added in Cylc 8 to maintain a pool of jobs and their states. This `JobPool`
is used by the `Scheduler` to update the jobs, similarly to how it does for tasks.

Every time the main loop runs, it calls a method (`Scheduler.update_data_structure`) to update the data
structures used by Cylc, including the data structures used by the GraphQL engine in Cylc. Other methods
that are responsible for updating the state of Tasks are now updating the state of Jobs too.

The method `update_data_structure` uses `WsDataMgr`, another new object being added. `WsDataMgr`
is where the Workflow Tasks, their parent Tasks, Task Families, and other objects required for
the Workflow such as Prerequisites and Conditions are calculated, and organized into dictionaries.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/graphql.svg.png.jpg" />

These dictionaries are kept in memory, updated periodically by `Scheduler`, and accessed by the
PyZMQ layer.

## PyZMQ layer

After the initial run of the main loop, we are ready to serve GraphQL data from our workflow
in Cylc. That is done by the `SuiteRuntimeServer`, a PyZMQ server. It got a new method
`pb_entire_workflow` that populates the `PbEntireWorkflow` object, and serializes it back to the client.

This method will be used by another project that uses [Python Graphene](https://github.com/graphql-python/graphene)
and [Tornado](https://github.com/tornadoweb/tornado) for the backend, and
[Vue.js](https://github.com/vuejs/vue) for the frontend. 

## Conclusion

Cylc uses a SQLite database for part of the workflow state (e.g. recovery) but for
the GraphQL we are not really accessing any database directly.

So the implementation in Cylc is probably different than what most blogs and tutorials
use as example.

It is still early work, and many things may change, but Cylc 8 is getting near its first alpha release
with GraphQL. Check out [https://github.com/cylc/cylc-flow](https://github.com/cylc/cylc-flow) for more.

The following references are useful to track the rationale behind this work in Cylc:

- [cylc-flow#2900 - PoC - GraphQL endpoint Design & Implementation](https://github.com/cylc/cylc-flow/issues/2900)
- [cylc-flow#3122 - UI Server graphql protobuf feed](https://github.com/cylc/cylc-flow/pull/3122)
- [cylc-uiserver#34 -  WS-UIS data and GraphQL integration](https://github.com/cylc/cylc-uiserver/pull/34)
