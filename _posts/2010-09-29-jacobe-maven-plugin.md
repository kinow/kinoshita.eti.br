---
date: 2010-09-29 16:43:25 +1300
layout: post
tags:
- java
title: Jacobe Maven Plugin
---

When I started working in the <a title="TestLink java api" href="http://code.google.com/p/testlink-api-java-client/">TestLink java api</a> with Daniel Padilla, he mentioned in some of his mails a tool called Jacobe. After I googled for this tool I found it in <a title="TIOBE" href="http://www.tiobe.com">TIOBE</a>'s website. <a title="TIOBE Jacobe" href="http://www.tiobe.com/index.php/content/products/jacobe/Jacobe.html">Jacobe</a> is a tool of TIOBE that beautifies your Java code, according to some rules that you can specify in one configuration file.

This is what Jacobe does, basically.

<img class="ui fluid image" src="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/jacobe_big.jpg">

Jacobe itself is an executable but TIOBE provides an Ant task that lets you call Jacobe from an Ant build file. But wait a minute! What about Maven? Yeah, exactly. Jacobe lacked of Maven support. I talked to the guys from TIOBE and they kindly let me implement a Maven Plugin for Jacobe.

The plugin source code is hosted at <a title="maven-jacobe-plugin sf.net" href="https://sourceforge.net/projects/maven-jacobe">SourceForge.net</a>, and you can find a quick Introduction about it in <a title="http://maven-jacobe.sourceforge.net/" href="http://maven-jacobe.sourceforge.net/">http://maven-jacobe.sourceforge.net/</a>. The maven plugin version 1.0 artifact was released on Wednesday to <a title="Sonatype releases repository - TIOBE Jacobe" href="https://oss.sonatype.org/content/repositories/releases/com/tiobe/jacobe/maven-jacobe-plugin/">Sonatype's release repository</a> and Sonatype already enabled <a title="Maven central repo - TIOBE Jacobe" href="http://repo1.maven.org/maven2/com/tiobe/jacobe/maven-jacobe-plugin/">Maven Central Repository</a> synchronization. However it may take some time for them update the repository index.

Cheers.
