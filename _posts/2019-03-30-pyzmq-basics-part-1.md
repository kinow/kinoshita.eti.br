---
date: 2019-03-30 16:32:17 +1300
layout: post
tags:
- zmq
- python
- opensource
- programming
title: PyZMQ Basics - Part 1
---

<a href="https://www.deviantart.com/kinow/art/Old-man-1-657521623" style="float: left;">
<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/old-man-1.png" /></a>

I am working [on a project](https://cylc.github.io) that is adopting [ZeroMQ](http://zeromq.org/).
This post series is for self understanding of PyZMQ, a ZeroMQ
[`libzmq`](https://github.com/zeromq/libzmq) binding for Python.

## What is ZeroMQ?

ZeroMQ (or 0MQ, or ØMQ) is an Open Source library that provides building blocks for
communication in distributed applications. The communication can be between the threads
of a process, between process (inter-process), or via network protocols such as
TCP and UDP.

It is optimized for performance, and has been used in many applications, giving users
a solid foundation to be used in their projects.

<!--more-->

The maintainers of the project provide low level C++ projects such as `libzmq` (GPL v3),
`zyre`, `czmq`, etc. But the most important project to get started with is `libzmq`.

`libzmq` is the core of ZeroMQ, and the community maintains bindings to other languages.
There is a Python binding, [`pyzmq`](https://pyzmq.readthedocs.io/en/latest/),
as well as a Java `jzmq`, a Node.JS, PHP, etc.

## More than just sockets

At its core, ZeroMQ handles sockets for you, but what you get when you create
&ldquo;sockets&rdquo; in ZeroMQ, are actually ZeroMQ abstractions of sockets.

As example in this section, we will use two code snippets from the ZeroMQ documentation.

```python
# helloworld_server.py
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")
```

```python
# helloworld_client.py
#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    socket.send(b"Hello")

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))
```

You can start the server, and then start the client, and you should see
the server printing the messages received, and in the client terminal you
should see the loop iteration and the messages sent to the server as well.

With a normal socket, you would expect starting the client before the server
to fail, but it works with ZeroMQ. Because ZeroMQ uses an abstraction to
help developers, not exposing a bare socket.

It is important to note that **there are socket types in ZeroMQ**. We have, for
example, the _REPLY_ socket, and the _REQUEST_ socket. Our example uses both, 
a _REPLY_ socket in the server_, as it is replying to messages. And a _REQUEST_
socket in the client, which is used to send requests to the server.

When you run both scripts, the communication is happening through a socket, but at a higher
level, there is a protocol used by ZeroMQ to serialize messages. You can send
raw messages too, but that is not the vanilla way.

So you cannot use ZeroMQ to replace a web server listening on port 80, and expect
browsers or other HTTP clients to be able to talk to this server. You would need
to write a client for it.

## Combining Socket Types

Another powerful feature in ZeroMQ, is the possibility to combine different
socket types. The previous example uses the REQ-REP duo. With this combination,
the _REQ_ endpoint is expected to send a message to the other endpoint, the _REP_.
The latter then produces a reply message, or none.

But sending two _REQ_ messages, the second would return an error. So if you modified
the example from the previous section to send two messages, first a "Hello", and
then "World", you would get an error in your terminal.

```bash
Connecting to hello world server…
Sending request 0 ...
Traceback (most recent call last):
  File "helloworld_client.py", line 22, in <module>
    socket.send(b"World")
  File "/home/kinow/Development/python/anaconda3/lib/python3.7/site-packages/zmq/sugar/socket.py", line 392, in send
    return super(Socket, self).send(data, flags=flags, copy=copy, track=track)
  File "zmq/backend/cython/socket.pyx", line 725, in zmq.backend.cython.socket.Socket.send
  File "zmq/backend/cython/socket.pyx", line 772, in zmq.backend.cython.socket.Socket.send
  File "zmq/backend/cython/socket.pyx", line 247, in zmq.backend.cython.socket._send_copy
  File "zmq/backend/cython/socket.pyx", line 242, in zmq.backend.cython.socket._send_copy
  File "zmq/backend/cython/checkrc.pxd", line 25, in zmq.backend.cython.checkrc._check_rc
zmq.error.ZMQError: Operation cannot be accomplished in current state
```

That is because each combination of socket types has its own way to send and
receive messages. These combinations are called **Messaging Patterns**, and they
allow you to go beyond the basic TCP one-to-one communication model.

These patterns are like recipes, that you can use in your project. `libzmq` comes
with four patterns.

- Request-Reply: a set of clients connects to a set of servers, similar to Remote Procedure Call (RPC).
- Pub-Sub: a set of publishers connects to a set of subscribers, similar to messaging queues, and JMS.
- Pipeline: nodes are connected in fan-out/fan-in pattern, with multiple steps and loops, similar to parallel task distribution, map-reduce.
- Exclusive pair: two sockets are connected exclusively. This is used for connecting two threads in a process.

## Conclusion

For now I will continue reading about ZeroMQ and checking out the examples
to understand more about the messaging patterns. But the most important
gotchas from this part, are:

- ZeroMQ gives us an abstraction of sockets
- Sockets have types in ZeroMQ
- It provides recipes that can be used in a software architecture by combining socket types
- Each combination will have its own operation mode, limitations, etc

And finally, a useful quote from their documentation.

>Let's recap briefly what ZeroMQ does for you. It delivers blobs of data (messages) to nodes, quickly and efficiently. You can map nodes to threads, processes, or nodes. ZeroMQ gives your applications a single socket API to work with, no matter what the actual transport (like in-process, inter-process, TCP, or multicast). It automatically reconnects to peers as they come and go. It queues messages at both sender and receiver, as needed. It limits these queues to guard processes against running out of memory. It handles socket errors. It does all I/O in background threads. It uses lock-free techniques for talking between nodes, so there are never locks, waits, semaphores, or deadlocks.
