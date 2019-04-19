---
date: 2011-10-23 22:10:02 +1300
layout: post
tags:
- testlink
- java
- software quality
title: 'Practical test doubles: adding stubs to TestLink Java API'
---

<p><em>"<strong>Test Double</strong> is a generic term for any case where you replace a production object for testing purposes"</em> [<a href="#1">1</a>]. There are different types of Test Doubles: <strong>Dummy</strong>, <strong>Fake</strong>, <strong>Stubs</strong>, <strong>Spies</strong> and <strong>Mocks</strong>. In this post we will see a practical example of adding stubs to <a href="testlinkjavaapi.sourceforge.net" title="TestLink Java API">TestLink Java API</a>.</p>

<p>Stubs are objects that return canned answers to calls during tests [1]. This is useful specially when you have a system that communicates with different resources such as databases, web services, XML-RPC services and so on.</p>

<p>TestLink Java API is a small Java project created to act as an interface between <a href="http://www.teamst.org" title="TestLink">TestLink</a> XML-RPC API and a client program written in Java.</p> 

<!--more-->

<h2>Starting on the wrong foot</h2>

<p>You know when sometimes you start a project just to suppress certain necessity and then write down a long <em>TODO</em> list? Well, sooner or later you will have to start working on those items. When I wrote the first version of the API I was writing Jenkins TestLink Plug-in, and had a priority project that depended on both tools to be deployed to a customer's site. Due to the deadlines and priorities, the tests in TestLink Java API were made to run directly against a test instance of TestLink.</p>

<p>After that the code was open sourced and, as was expected, bugs, features and enhancements started to be requested by users. You can imagine many drawbacks in this approach, such as newcomers to the project would need to install a test instance of TestLink with equal set up parameters, and to not mention how hard it would be to have Continuous Integration in a service provider like <a href="http://www.cloudbees.com" title="CloudBees">CloudBees</a>, where I wouldn't have TestLink installed.</p>

<h2>On the right foot now...</h2>

<p>So the main issue regarding the project build was the direct access to the TestLink XML-RPC API. A neat solution for it was to use Stubs during tests. The idea was to create a stubs capable of, given a call to TestLink XML-RPC, it would then answer with a canned XML.</p>

<p>I thought I would have to dig into <a href="http://www.mortbay.org/" title="Jetty">Jetty</a>, <a href="http://winstone.sourceforge.net/" title="Winstone">Winstone</a> or some small web server by myself and include it to the project, but fortunately somebody else [<a href="#2">2</a>] has passed by it and blogged about his experience with some sample code.</p>

<p>The approach used in TestLink Java API was quite similar to the one described in [<a href="#2">2</a>]. I used <a href="http://www.wireshark.org/" title="WireShark">WireShark</a> to save the XML returned by TestLink XML-RPC API and when I create an instance of the web server, it knows which XML it must return to the caller object. Below you can see <em>BaseTest</em>, a class used as base for new tests.</p>

<script src="https://gist.github.com/1308128.js"> </script>

<p>Now anybody can simply execute <em>mvn clean test</em> to build the project. It won't connect to any instance of TestLink, and all the tests will be executed in less then one minute. When there is a new release of TestLink, I will need to update my XML files generated with Wireshark (I will automate it with Python or Perl) and then test and work on the differences.</p>

<p>This approach can be used to test web services, XML-RPC servers and any similar environment. Hope it helps somebody else too. Cheers! :D</p>

<p><a name="1">[1]</a> <a href="http://martinfowler.com/bliki/TestDouble.html">http://martinfowler.com/bliki/TestDouble.html</a></p>

<p><a name="2">[2]</a> <a href="http://olafsblog.sysbsb.de/lightweight-testing-of-webservice-http-clients-with-junit-and-jetty/trackback/">http://olafsblog.sysbsb.de/lightweight-testing-of-webservice-http-clients-with-junit-and-jetty</a></p>
