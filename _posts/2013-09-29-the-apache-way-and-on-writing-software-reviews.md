---
date: 2013-09-29 14:53:53 +1300
layout: post
tags:
- apache software foundation
title: The Apache Way and on writing software reviews
---

The [Apache Way](http://www.apache.org/foundation/how-it-works.html) is the philosophy behind 
Apache Software Foundation and is shared by all of its projects. It is composed by a set of principles:

* Collaborative software development
* Commercial-friendly standard license
* Consistently high quality software
* **Respectful, honest, technical-based interaction**
* Faithful implementation of standards
* Security as a mandatory feature

I have been part of [Apache Commons](http://commons.apache.org) for a while, and haven't 
really contributed much yet. Maybe because I had lots of projects related to 
[TupiLabs](http://tupilabs.com) as well as my own wedding this year. But I can 
assure that *respectful, honest, technical-based interaction* is quite right (not to discredit the 
other items, of course).

Even though there are critics of the Apache Way ([1]("#1"), [2]("#2"), [3]("#3")), it still stands as an important 
pillar for the Apache Software Foundation, and its principles help to create stable and 
production ready software, such as [Apache Hadoop](http://hadoop.apache.org), 
[Apache Httpd](http://httpd.apache.org), [Apache Commons Lang](http://commons.apache.org/lang), 
among [others](http://projects.apache.org).

There are many reviews and comparisons on Apache software (as well as on 
other software, like JavaScript libraries, Java Web Frameworks, Ruby Web servers and so on). 
Sometimes, though, these reviews or comparisons can be biased or not well founded. In 
cases like this, the developers of the tools may be frustrated, or users can be 
misled and choose the software based on wrong assertions.

I have just returned from honey moon, ready to start writing code again, but 
first I had to read all the unread messages in my inbox. Some were e-mails from [Apache 
mailing lists](https://www.apache.org/foundation/mailinglists.html). [One of these e-mails](http://markmail.org/thread/uoh5m55mh4qjybaw) 
had Phil Steitz comments on a post by Daniel Wu. 

Instead of publishing his performance benchmark results of 
[Apache Commons Pool](http://commons.apache.org/pool), Daniel posted his 
code to the commons-dev mailing list. Phil Steitz, one of Apache Commons Pool 
committers replied with questions and a few points that Daniel could use to 
enrich his benchmark tests.

This kind of behavior happens a lot within Apache (at least in the mailing lists that 
I follow), and it produces a lot of benefits for different parts. 

* The person writing a review or comparison can get the programmer opinion before actually 
publishing anything. 
* The programmer can see how other people were testing his/her code.
* All other commons-pool committers and maintainers, the mailing list readers, and 
people that found the mailing list archives will be able to read the conversation 
history.
* No misguided benchmark results were published (and lots of wrong decisions were avoided).

I keep loving the Apache Way and the resulting community and code around it. There are 
always lots of things to learn, the Open Source projects communities are healthy and you will always find 
people willing to share their experience and time teaching you.

♥ Open Source

 * * *

<sup><a name="1">1</a> 
<a href="http://www.infoworld.com/d/open-source-software/has-apache-lost-its-way-225267?page=0,2">
http://www.infoworld.com/d/open-source-software/has-apache-lost-its-way-225267?page=0,2</a></sup>

<sup><a name="2">2</a> 
<a href="http://footle.org/2011/11/23/apache-considered-harmful/">
http://footle.org/2011/11/23/apache-considered-harmful/</a></sup>

<sup><a name="3">3</a> 
<a href="http://www.itworld.com/it-managementstrategy/227477/has-open-source-outgrown-apache-way">
http://www.itworld.com/it-managementstrategy/227477/has-open-source-outgrown-apache-way</a></sup>
