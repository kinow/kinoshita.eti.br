---
layout: post
tags:
- programming
- java
- opensource
- eclipse
categories:
- blog
title: Using formatter exclusions with Eclipse
---

Sometimes when you are formatting your code in Eclipse, you may want to prevent
some parts of the code from being formatted. Especially when using Java 8 lambdas
and optionals.

Here's some code before being formatted by Eclipse's default formatter rules.

<small>Code adapted from: blog post <a href="http://javadeau.lawesson.se/2016/10/java-8-streams-in-hibernate-and-beyond.html"><i>Java d'eau &dash; Java 8: Streams in Hibernate and Beyond</i></a></small>

```java
session.createQuery("SELECT h FROM Hare h", Hare.class)
    .stream()
    .filter(h -> h.getId() == 1)
    .map(Hare::getName)
    .forEach(System.out::println);
```

Then after formatting.

```java
session.createQuery("SELECT h FROM Hare h", Hare.class).stream().filter(h -> h.getId() == 1).map(Hare::getName)
                .forEach(System.out::println);
```

Which doesn't look very appealing, ay? You can change this behaviour at least in two ways.
The first by telling the formatter to ignore this block, through a special formatter tag in your code.

First you need to enable this feature in Eclipse, as it is disabled by default. This setting is found in
the preferences *Java* &rarr; *Code Style* &rarr; *Formatter* &rarr; *Edit* &rarr; *Off/On Tags*.

<p style='text-align: center;'>
<img style="display: inline" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/formatter-tags.png" alt="A screen shot of Eclipse formatter settings" title="Enabling formatter tags in Eclipse" />
<br/>
<small>Enabling formatter tags in Eclipse</small>
</p>

Then formatting the following code won't change a thing in the block surrounded by the formatter tags.

```java
/* @Formatter:off */
session.createQuery("SELECT h FROM Hare h", Hare.class)
    .stream()
    .filter(h -> h.getId() == 1)
    .map(Hare::getName)
    .forEach(System.out::println);
/* @Formatter:on */
```

But having to type these tags can become annoying, and cause more commits and pull requests to be
unnecessarily created. So an alternative approach can be to change the formatter
[behaviour globally](https://stackoverflow.com/a/34492247/1762101).

This can be done in Eclipse in another option under the formatter options, *Java* &rarr; *Code Style*
&rarr; *Formatter* &rarr; *Edit* &rarr; *Line Wrapping* &rarr; *Function Calls* &rarr;
*Qualified invocations*.

You will have to choose *&ldquo;Wrap all elements, except first element if not necessary&rdquo;*
under *Line wrapping policy*. And also check *&ldquo;Force split, even if line shorter than
maximum line width&rdquo;*.

<p style='text-align: center;'>
<img style="display: inline" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/global-setting.png" alt="A screen shot of Eclipse formatter settings" title="Enabling custom formatter behaviour globally" />
<br/>
<small>Enabling custom formatter behaviour globally</small>
</p>

Once it is done, your code will look like the following no matter what.

```java
session.createQuery("SELECT h FROM Hare h", Hare.class)
    .stream()
    .filter(h -> h.getId() == 1)
    .map(Hare::getName)
    .forEach(System.out::println);
```

Happy coding!

&hearts; Open Source
