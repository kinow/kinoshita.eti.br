---
date: 2018-07-22 13:22:14 +1300
layout: post
tags:
- python
- pandas
- opensource
title: Multithreaded code and Pandas
---

<a href="https://www.deviantart.com/kinow/art/Woman-looking-01-743551195"><img style="float: left; height: 300px;" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/woman-looking-01.png" alt="Woman looking" /></a>

Pandas provides high-performance data structures in Python. I think in Java there are
similar data structures in projects like Apache Commons Collections,
Google Guava, and also Trove.

In the Java libraries thread-safety is always a must-have feature. Probably as it is quite
common for a Java program to have more than one thread, especially if the code runs in some
sort of web container.

I recently learned that Pandas, on the other hand, does not guarantee any thread-safety.
I found that while reading an
[issue about race condition in the `IndexEngine`](https://github.com/pandas-dev/pandas/issues/21150),
and after preparing a pull request for that.

<!--more-->

```python
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

x = pd.date_range('2001', '2020')
with ThreadPoolExecutor(2) as p:
    assert all(p.map(lambda x: x.is_unique, [x]*2))
```

When you create an index like that, it will delegate most of the hard work to the `IndexEngine`.
Inside the `IndexEngine`, the values passed for the index are stored, and then an empty
`Hashtable` is created (as well as several flags for the state of the object, such as
`unique`, which defines whether the index has unique elements or not).

Once a user calls a method like `is_unique`, then the flags are updated, the `Hashtable`
mapping is populated, and while doing so, if not all elements are unique, the flag for
`unique` is set to `false`, or `true` otherwise. But if the user does not need that
operation, we will avoid populating the mapping until we really need it.

I believe it is done that way for performance. However, at the cost that the state is shared
among calls, which makes it harder to use this API in a multithreaded environment - though
still possible by moving the synchronization to your caller code.

Some Apache software also do the same, asking users to synchronize, serialize, or handle
certain corner cases on their side. There is a huge cost associated with maintaining an Open
Source project that promises thread-safety.

But maybe [Dask](http://dask.pydata.org/en/latest/) provides an alternative to use Pandas
with multiple threads. But I have not used that yet.

&hearts; Open Source

_NB: even though Pandas is not thread-safe, it does not mean you should not use it. Just use
with care when using multiple threads_
