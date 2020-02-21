---
layout: post
tags:
- programming
- java
- opensource
categories:
- blog
title: Remember to synchronize when iterating streams from a synchronized Collection
---

When iterating collections created via `Collections.synchronizedList` for instance, you are required
to obtain a lock on the actual list before doing so. So you normally end up with code similar to:

```java
List list = Collections.synchronizedList(new ArrayList());
synchronized (list) {
  Iterator i = list.iterator(); // Must be in synchronized block
  while (i.hasNext())
      foo(i.next());
}
```

This requirement is [documented in the javadocs](https://docs.oracle.com/javase/9/docs/api/java/util/Collections.html#synchronizedList-java.util.List-).

Since lambdas and streams are being more widely used, it is important to remind
that when iterating via a stream we also need to obtain a lock on the synchronized
collection created.

```java
List list = Collections.synchronizedList(new ArrayList());
synchronized (list) {
  list.stream()
    .anyMatch(...)
}
```

Here's an [example from Zalando Nakadi Event Broker](https://github.com/zalando/nakadi/pull/786).

Happy hacking!
