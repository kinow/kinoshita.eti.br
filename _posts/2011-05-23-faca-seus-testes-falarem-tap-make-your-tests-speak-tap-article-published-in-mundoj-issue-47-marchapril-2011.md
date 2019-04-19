---
date: 2011-05-23 19:19:04 +1300
layout: post
tags:
- test anything protocol
- software quality
- articles
title: Faça seus Testes Falarem TAP (Make your Tests Speak TAP) article published
  in MundoJ, issue 47, March/April 2011
---

This is my first article for a Brazilian magazine! :-D It was published in this month's issue of <a href="http://www.mundoj.com.br">MundoJ</a> magazine (previously called MundoJava).

<img class="ui left floated image" src="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/ed47p.jpg">

In this article Cesar Fernandes de Almeida, <a href="http://andersonxp.tumblr.com/">Anderson dos Santos</a> and I discuss how to make your Java tests output <a href="http://www.testanything.org">TAP</a> (Test Anything Protocol) Streams. This test protocol has been used by Perl developers since Perl's first version (1983~) but hasn't been used by many Java developers yet, unfortunately. We hope it incentives other Java developers to use TAP for their tests. There is an alternative to TAP too, <a href="https://launchpad.net/subunit">SubUnit</a>, which was pointed out for me by <a href="https://launchpad.net/~lifeless">Robert Collins</a> in the <a href="http://jenkins.361315.n4.nabble.com/Jenkins-dev-f387835.html">Jenkins dev-list</a> few weeks ago. Now I am preparing a comparison between TAP and SubUnit as an analysis before developing a plug-in for Jenkins to show detailed test results (such as exception, images, raw test, error line, etc). 

Throughout the article we explain how to use <a href="http://www.tap4j.org">tap4j</a> to generate TAP Streams with <a href="http://www.testng.org">TestNG</a>, however it is possible to use the same approach to generate TAP Streams with <a href="http://www.junit.org">JUnit</a>.

Now I will translate the article to send it to <a href="http://search.cpan.org/~patl/">Patrick LeBoutillier</a>, who contributed to this article answering patiently my questions by mail and writing <a href="http://search.cpan.org/~patl/metatap-0.01/">metatap</a>, a utility that lets you check if a TAP Stream is valid, according to the program parameters. This utility is being used in tap4j for integration tests between Perl and Java.

Unfortunately I'm not allowed to redistribute the article, not even an English version of it :-(

Cheers :)
