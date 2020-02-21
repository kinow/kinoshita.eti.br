---
layout: post
tags:
- java
categories:
- blog
title: Invoking Testopia XML-RPC or JSON methods using Java
---

Most <a href="http://www.teamst.org" title="TestLink">TestLink</a> [1] users are aware that there is an external API, maybe for the external API token being displayed in the user profile section. Today after a meeting with <a href="http://twitter.com/peterflorijn" title="Peter Florijn">Peter Florijn</a> [2], I realized that the same may not be true for <a href="http://www.mozilla.org/projects/testopia/" title="Testopia">Testopia</a>  [3] users.

I am quite new to Testopia, and there are many features that I haven't used yet. But if I understand it correctly, the database is interfaced by several Perl scripts that are, by its turns, exposed as Web Service (most of them). The web services are available via a JSON and a XML-RPC API (what is very useful, TestLink supports supports only XML-RPC).

The communication between different programming languages and the external API's is accomplished by a client API. In TestLink you have <a href="http://testlinkjavaapi.sourceforge.net/" title="TestLink Java API">testlink-java-api</a> [4] and <a href="http://code.google.com/p/testlink-api-java-client/" title="TestLink API Java Client">testlink-api-java-client</a> [5].

Testopia has a Java client too, available in <a href="http://bzr.mozilla.org/bugzilla/extensions/testopia/2.2-bugzilla-3.2/files/head:/testopia/contrib/drivers/java/" title="Testopia source repository">Testopia source repository</a> [6] and can be used to integrate your existing Java code with Testopia.

<!--more-->

<img src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/testopia_java_300_120.png">

Peter and I have been working on <a href="https://wiki.jenkins-ci.org/display/JENKINS/Testopia+Plugin" title="Jenkins Testopia Plug-in">Jenkins Testopia Plug-in</a> [7], released few weeks ago and with its new version being released at this very moment. It's been fun to write this new plug-in, and we are using a type of Scrum to manage the project, what makes it even more interesting.

During the project feature definition and initial structure, we created a new implementation, motivated by the following reasons (in no special order):

<ul>
<li>Provide an API for Maven developers</li>
<li>Publish this new API to Maven central repository (so Gradle, Ivy and Maven users could use it too)</li>
<li>Use a non DDD (Domain Driven Design) approach, as it helps debugging serialization issues in Jenkins (only one element talks to Testopia. So we put this element in Jenkins master, and don't have to worry about calls to objects methods serialized to slaves)</li>
<li>Test doubles, so we could increase test coverage without the need of a Testopia instance running</li>
</ul>

We haven't released this API to Maven central yet, as we still have to polish the code, add tests and more methods. But you can already start playing with this API, the code is at GitHub, <a href="http://www.github.com/kinow/testopia-java-driver" title="Testopia Java Driver">http://www.github.com/kinow/testopia-java-driver</a> [8], and here's a Snippet of code to get you started with the API.

```java
TestopiaAPI api = new URL("http://localhost/bugzilla-4.2.1/xmlrpc.cgi");
api.login("root", "pass");
TestRun testCaseRun = api.getTestRun(1);
TestCase[] testCases = api.getTestCases(this.getTestRunId());
for(TestCase testCase : testCases) {
  Status status = Status.BLOCKED;
  testCase.setStatusId(status.getValue());
  api.update(testCase, testCase.getRunId(), testCase.getBuildId(), testCase.getEnvId());
}
```

Have fun!

- [1] http://www.teamst.org
- [2] http://twitter.com/peterflorijn
- [3] http://www.mozilla.org/projects/testopia/
- [4] http://testlinkjavaapi.sourceforge.net/
- [5] http://code.google.com/p/testlink-api-java-client/
- [6] http://bzr.mozilla.org/bugzilla/extensions/testopia/2.2-bugzilla-3.2/files/head:/testopia/contrib/drivers/java/
- [7] https://wiki.jenkins-ci.org/display/JENKINS/Testopia+Plugin
- [8] http://www.github.com/kinow/testopia-java-driver
