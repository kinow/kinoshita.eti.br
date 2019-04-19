---
title: A simple cylc suite
time: '18:59:13'
author: kinow
tags:
    - cylc
    - python
    - opensource
---

I have been writing more suites for [cylc](https://cylc.github.io/cylc/) lately, and found
an example that has proved to be useful for debugging certain parts of the code.

It is an extremely simple suite, similar to what is in cylc's documentation. It
sleeps for N seconds, and prints a message.

<!--more-->

What makes it extra simpler, is that it cycles through integers, and has
a limit of 1 maximum active points.

It is essentially the same as running the command in your shell session. With
the difference that it will run through all cylc's internal, only once, and
allow you to debug and diagnostic parts nor related to cycling and graphs
(as for these parts you would probably need a more elaborate example).

```python
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
```

I also combine this suite with the following `global.rc`.

```python
[editors] 
    terminal = vim 
    gui = gvim -f

[communication]
    base port = 44444
    method = http
    maximum number of ports = 1
```

With "base port" set to 44444, and the maximum number of ports to 1, I will
be able to run only one task. But that way I can configure Wireshark and other
tools to default to 44444/HTTP, for ease of debugging.

Then initialize the suite with something like: `cylc start --non-daemon --debug /home/kinow/Development/python/workspace/example-suite/`

Happy cycling!

