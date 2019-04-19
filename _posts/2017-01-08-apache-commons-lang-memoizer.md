---
date: 2017-01-08 18:34:03 +1300
layout: post
tags:
- java
- programming
- apache software foundation
title: 'Apache Commons Lang: Memoizer'
---

The current release of [Apache Commons Lang](https://commons.apache.org/proper/commons-lang/)
is **3.5**. The upcoming release, probably 3.6,
will include a new feature, added in a
[pull request](https://github.com/apache/commons-lang/pull/203):
**a Memoizer implementation**. Check out the ticket [LANG-740](https://issues.apache.org/jira/browse/LANG-740)
for more about the implementation being added to [lang].

The book [Java Concurrency in Practice](http://jcip.net/) introduces readers to the Memoizer,
and has also a [public domain implementation available for download](http://jcip.net/listings/Memoizer.java)
(besides that, the book has also lots of other interesting topics!).

In summary, Memoizer is a simple cache, that will store the result of
a computation. It receives a Computable object, responsible for doing something
that will be stored by the Memoizer. Here's a simple code to illustrate how that
will work in your Java code.

```java
// Computation to be stored in the cache
Computable<String, String> getFormattedCurrentDate = new Computable<String, String>() {
    @Override
    public String compute(String fmt) throws InterruptedException {
        return new SimpleDateFormat(fmt).format(new Date());
    }
};

// Our memoizer
Memoizer<String, String> dateCache = new Memoizer<>(getFormattedCurrentDate);

// To illustrate its use
for (int i = 0; i < 10; i++) {
    try {
        // S -> Millisecond
        System.out.println(dateCache.compute("HH:mm:ss:S Z dd/MM/YYYY"));
        // Regardless of this sleep call, we get the same result every iteration
        Thread.sleep(1500);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}
```

The computable created (*getFormattedCurrentDate*) will be called only once, and stored in
a map. The parameter passed in the *#compute()* method will be used as key in the map.
So choose your parameter wisely :-) The output of the example will be similar to the following one.

```shell
19:15:57:854 +1300 08/01/2017
19:15:57:854 +1300 08/01/2017
19:15:57:854 +1300 08/01/2017
19:15:57:854 +1300 08/01/2017
19:15:57:854 +1300 08/01/2017
19:15:57:854 +1300 08/01/2017
19:15:57:854 +1300 08/01/2017
19:15:57:854 +1300 08/01/2017
19:15:57:854 +1300 08/01/2017
19:15:57:854 +1300 08/01/2017
```

In the example above I used a *for-loop* to illustrate what will happen. Even though we call
the memoizer *#compute()* method several times, followed by
*Thread#sleep()*; only one result, the first to be computed, will be returned.

So that's all for today. Hope you learned something about this new class, that must
be available in the next release of Apache Commons Lang.

Happy hacking!

ps: [lang] uses Java 7, so that is why we do not have a functional instead of the Comparable
