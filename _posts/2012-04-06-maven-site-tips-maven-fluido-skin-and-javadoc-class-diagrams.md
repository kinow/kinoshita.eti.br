---
layout: post
tags:
- java
categories:
- blog
title: 'Maven site tips: Maven Fluido Skin and Javadoc class diagrams'
---

<p>I have been using Maven sites for a while, and am very happy with it. I didn't like to have to update my projects after Maven 3, but that was all right, Maven 3 brought many new cool things. However, there were two things that annoyed me: lack of a nice and modern skin, and browsing Javadoc of complex code. The thought of creating a custom Maven skin even crossed my mind, but I never had time to read about it.</p>

<p>But the world is full of good and talented people! Like the guys from <a title="99soft" href="http://www.99soft.org/">99soft</a>. They created <a title="Maven Fluido Skin" href="http://maven.apache.org/skins/maven-fluido-skin/">Maven Fluido Skin</a>, and donated it to <a title="Apache Software Foundation" href="http://apache.org/">Apache Software Foundation</a>. It's built on top of <a title="Twitter Bootstrap" href="http://twitter.github.com/bootstrap/">Twitter's Bootstrap</a> and available from Maven central repository. In order to use it in your Maven project, all that you have to do is add the following settings into your src/site/site.xml:</p>

```xml
<skin>
    <groupId>org.apache.maven.skins</groupId>
    <artifactId>maven-fluido-skin</artifactId>
    <version>1.2.1</version>
</skin>
```

<p>Here's a list of some projects using Maven Fluido Skin (hopefully, in the near future <a title="Apache Commons" href="http://commons.apache.org/">Apache Commons</a> and other projects will adopt this skin as default too :-)):</p>

<!--more-->

<p><ul>
	<li><a title="Maven Fluido Skin" href="http://maven.apache.org/skins/maven-fluido-skin/">Maven Fluido Skin</a></li>
	<li><a title="tap4j" href="http://www.tap4j.org">tap4j</a></li>
	<li><a title="TestLink Java API" href="http://testlinkjavaapi.sf.net">TestLink Java API</a></li>
</ul></p>

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/fluido_skin_300_135.png">

<p>Regarding the Javadoc browsing, there's a nice trick too: add class diagrams. I have seen a new Javadoc template in Apache Commons mailing list, but it was a work in progress, so for now I will stick with class diagrams. These diagrams are generated when you execute the javadoc or the site goals, using <a title="Graphviz" href="http://www.graphviz.org/">graphviz</a>. And there is more. You can click on the diagram classes, as they have a link to the Java class that they reference to.</p>

<p>You can find instructions for setting up the diagram generation in <a href="http://maven.apache.org/maven-1.x/plugins/javadoc/faq.html#classdiagrams">Apache Maven web site</a>, or looking at <a href="https://github.com/kinow/tap4j/blob/master/pom.xml">examples</a> (I prefer the latter). But basically, you will need graphviz installed, and something like the following XML snippet in your project pom.xml.</p>

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-javadoc-plugin</artifactId>
    <version>2.7</version>
    <configuration>
        <doclet>gr.spinellis.umlgraph.doclet.UmlGraphDoc</doclet>
        <docletArtifact>
            <groupId>gr.spinellis</groupId>
            <artifactId>UmlGraph</artifactId>
            <version>4.4</version>
        </docletArtifact>
        <additionalparam>
            -inferrel -inferdep -quiet -hide java.*
            -collpackages java.util.* -qualify
            -postfixpackage -nodefontsize 9
            -nodefontpackagesize 7
            -edgefontname "Trebuchet MS"
            -nodefontabstractname "Trebuchet MS"
            -nodefontclassabstractname
            "Trebuchet MS"
            -nodefontclassname "Trebuchet MS"
            -nodefontname
            "Trebuchet MS"
            -nodefontpackagename "Trebuchet MS"
            -nodefonttagname
            "Trebuchet MS" 
        </additionalparam>
    </configuration>
</plugin>
```

<p>Here's how a diagram looks like (source: <a href="http://tap4j.org/apidocs/index.html">http://tap4j.org/apidocs/index.html</a>):</p>

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/javadoc_graphviz_300_135.png">

<p>Have fun! :-) and remember to check if your CI machine has graphviz installed too, otherwise you will have 404 in your Javadoc pages ;-)</p>

<p>Cheers</p>
