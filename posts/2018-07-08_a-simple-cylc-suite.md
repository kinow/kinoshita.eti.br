---
title: A simple cylc suite
author: kinow
tags:
    - cylc
    - opensource
---

I have been writing more suites for [cylc](https://cylc.github.io/cylc/) lately, and found
an example that has proved to be useful for debugging certain parts of the code.

It is an extremely simple suite, similar to what is in cylc's documentation. It
sleeps for N seconds, and prints a message.

What makes it extra simpler, is that it cycles through integers, and has
a limit of 1 maximum active points.

It is essentially the same as running the command in your shell session. With
the difference that it will run through all cylc's internal, only once, and
allow you to debug and diagnostic parts nor related to cycling and graphs
(as for these parts you would probably need a more elaborate example).

{% geshi 'python' %}
[scheduling]
    cycling mode = integer
    initial cycle point = 1
    max active cycle points = 1
    [[dependencies]]
        [[[P1]]]
            graph = "hello"
[runtime]
    [[hello]]
        script = "sleep 10; echo PING"
{% endgeshi %}

Happy cycling!

