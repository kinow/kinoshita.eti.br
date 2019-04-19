---
title: "When you don't realize you need a Comparable"
author: kinow
tags: 
    - apache software foundation
    - java
    - opensource
    - programming
time: '23:07:39'
---

[In 2012, I wrote]({% post_url 2012-10-20-replacing-a-hashset-with-a-bitset %}) about how you always learn something
new by following the [Apache dev mailing lists](http://www.apache.org/foundation/mailinglists.html).

After about five years, I am still learning, and still getting impressed by the knowledge of other
developers. Days ago I was massaging some code in [a pull request](https://github.com/apache/jena/pull/237)
and a developer suggested me to simplify my code.

<!--more-->

The suggestion was to make a class a [Comparable type](https://docs.oracle.com/javase/7/docs/api/java/lang/Comparable.html)
to both simplify the code, and also have a better design. I immediately agreed, and looking back in hindsight,
it was the most logical choice. Yet, I simply did not think about that.

```java
// What the code was
case VSPACE_SORTKEY :
    int cmp = 0;
    String c1 = nv1.getCollation();
    String c2 = nv2.getCollation();
    if (c1 != null && c2 != null && c1.equals(c2)) {
        // locales are parsed. Here we could think about caching if necessary
        Locale desiredLocale = Locale.forLanguageTag(c1);
        Collator collator = Collator.getInstance(desiredLocale);
        cmp = collator.compare(nv1.getString(), nv2.getString());
    } else {
        cmp = XSDFuncOp.compareString(nv1, nv2) ;
    }
    return cmp;
}
```

```java
// What the code is now
case VSPACE_SORTKEY :
    return ((NodeValueSortKey) nv1).compareTo((NodeValueSortKey) nv2);
}
```

This moved the logic to a method in the `NodeValueSortKey` class. This reduced the complexity
of the class with the `switch` statement. And it also made it easier to write unit tests.

If you are not involved in Open Source projects yet, I keep my suggestion from five years ago.
Find a project related to something you like, and start reading the code, lurk in the
mailing list or watch GitHub repositories.

You can always learn more!

&hearts; Open Source
