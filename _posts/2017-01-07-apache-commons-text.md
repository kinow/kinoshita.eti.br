---
title: 'Apache Commons Text'
author: kinow
tags:
    - java
    - programming
    - apache software foundation
category: 'blog'
time: '20:39:03'
---

There is a new component in Apache Commons: Apache Commons Text. The 1.0 release might be announced
in the next weeks. The current site is still in the [Commons Sandbox](http://commons.apache.org/sandbox/commons-text/),
but it will change with the 1.0 release. The promotion from the sandbox
[happened a few days ago](http://markmail.org/message/dm7xwv5wc6z7wme3) in
the project mailing list.

Here's the project description: **Apache Commons Text is a library focused on algorithms working on strings**.

There was [a thread on the mailing list](http://markmail.org/message/3k7m2zrzboji333r)
some time ago (Oct/2014) when we first discussed the component idea. Since then
many people contributed porting code from
[Apache Commons Lang](http://commons.apache.org/proper/commons-lang/),
[Apache Lucene](http://lucene.apache.org/), donating code from existing projects, and with new ideas.

**It is important to be aware that certain parts of Apache Commons Lang are
being marked as deprecated, and will be removed in the future, after Apache Commons Text
1.0 is out**. For example: [StringUtils](https://commons.apache.org/proper/commons-lang/apidocs/org/apache/commons/lang3/StringUtils.html),
and [RandomStringUtils](https://commons.apache.org/proper/commons-lang/apidocs/org/apache/commons/lang3/RandomStringUtils.html).

That will happen probably in a 4.x release of Apache Commons Lang, if everything
goes well with Apache Commons Text :-)

And there are already future features in
[branches too](https://github.com/apache/commons-text/branches/all).
It was decided that these features
needed further work, so they will probably be included in next releases.

So that's a little bit of background on the new component that will be released soon.
If you have code using Apache Commons Lang, you might be interested in staying
tuned to release announcements in the mailing list!

And should you have suggestions and would like to contribute, feel free to join and start
a thread in the [mailing list](https://commons.apache.org/mail-lists.html),
open a [JIRA issue](https://issues.apache.org/jira/browse/TEXT), or submit a
[pull request](https://github.com/apache/commons-text/pulls).

Happy hacking!