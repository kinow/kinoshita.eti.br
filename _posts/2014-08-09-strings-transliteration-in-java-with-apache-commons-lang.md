---
layout: post
tags:
- java
- apache software foundation
- bioinformatics
categories:
- blog
title: Strings transliteration in Java with Apache Commons Lang
---

[Rosalind](http://rosalind.info) is a website with a curated set of exercices for bioinformatics, organized hierarchily. 
In some of these examples you are required to replace characters (nucleotides) by other characters. It is a rather common 
task for developers, like when you need to replace special characters in user's names.

There are different ways of describing it, such as translate, replace, or **[transliterate](http://en.wikipedia.org/wiki/Transliteration)**. The latter being my favorite definition. 

In Python I know that there are several different ways of transliterating strings 
\[[1](https://pypi.python.org/pypi/transliterate)\]\[[2](http://blog.lebowtech.com/blog/programming/python/transliterate-with-python.html)\]. But in Java I always ended up using a Map or a Enum and writing my own method in some *Util* class for that.

Turns out that [Apache Commons Lang](http://commons.apache.org), which I use in most of my projects, 
provided this feature. What means that I will be able to reduce the length of my code, what also means 
less code to be tested (and one less place to look for bugs).

```java
String s = StringUtils.replaceChars("ATGCATGC", "GTCA", "CAGT"); // "TACGTACG"
System.out.println(s);
```

What the code above does, is replace G by C, T by A, C by G and A by T. This process is part of finding the 
[DNA reverse complement](http://www.bioinformatics.org/sms/rev_comp.html). But you can also use this for replacing 
special characters, spaces by _, and so it goes.

Happy hacking!
