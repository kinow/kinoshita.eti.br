---
title: 'A comparison of TAP (Test Anything Protocol) and SubUnit'
id: 654
author: kinow
tags: 
    - test anything protocol
    - software quality
category: 'blog'
time: '02:04:45'
---

<p>
    I have been playing with <a href="http://www.testanything.org">TAP</a> for some time and even implemented a <a
        href="http://www.tap4j.org">Java API</a> to let <a href="http://www.testng.org">TestNG</a>, <a
        href="http://www.junit.org">JUnit</a> and other Test Frameworks to produce and consume TAP. TAP is a standard
    format for test output that first appeared with Perl 1 in 1987. It is human and machine readable, easy to be
    serialized, language independent and extensible<sup><a href="#1">1</a></sup> through the use of <a
        href="http://www.yaml.org">YAML</a>.
</p>

<p>
    Some days ago while I was designing a plug-in to show TAP test results in <a href="http://www.jenkins-ci.org">Jenkins</a>
    I stumbled across a message in <a href="http://jenkins.361315.n4.nabble.com/Jenkins-dev-f387835.html">Jenkins
        dev-list</a> where Max Magee and Nick Wiesmueller were discussing about a way of showing more details about the test
    executions. I thought that the TAP Plug-in would fit perfectly, until one of the users, <a
        href="https://launchpad.net/~lifeless">Robert Collins</a>, mentioned <a href="https://launchpad.net/subunit">SubUnit</a>.
</p>

<p>
    Shame on me, but I hadn't heard of SubUnit until that message. Max Magee and I exchanged some messages after that,
    talking about a initial design and analysis for the TAP Plug-in<sup><a href="#2">2</a></sup>. Here is the initial
    idea:
<p>
<ul>
    <li>The plug-in will be able to parse one or more test formats (maybe SubUnit, TAP and the formats available in
        xUnit?).</li>
    <li>The test results will be displayed the same way JUnit tests are displayed in Jenkins (I think Jenkins
        supports JUnit format by default, but you can use objects and create test results data, independently of the
        test framework that you are using).</li>
    <li>There will be a table containing the Test Name, Description and Status and an expandable section.</li>
    <li>Inside this expandable section will be available all the details about the test.</li>
    <li>In case there are images within the test details, they should be displayed as a lightbox gallery.<sup><a
            href="#3">3</a></sup></li>
</ul>
<p>
    Although I have worked with TAP and spent some good time writing the tap4j port for Java, I am not convinced it is
    the best solution for this issue yet. Hence I am posting this initial comparison between TAP and SubUnit hoping that
    more people will contribute with the design of this solution. My goal is not only having a super cool plug-in for
    Jenkins, but ease integration of test results in different tools and collaborate with both TAP and SubUnit. Another
    objective that I have in mind is improving the way that test results are displayed in Jenkins and enabling it to be
    an alternative for tools like <a href="http://sourceforge.net/projects/smolder/">Smolder</a>, <a
        href="https://launchpad.net/testrepository">TestRepository</a> or <a href="https://launchpad.net/tribunal">Tribunal</a>.
    Because I believe the tasks done by these tools could be all done in my favorite CI Server, and it would increase
    the productivity of Build &amp; Release professionals :-))
</p>

<!--more-->
<h2>
    Comparison table<sup><a href="#4">4</a></sup>
</h2>
<p>I believe tables are a good way to compare different technologies. However if anybody has any recommendation on a
    different way of doing it, I would be glad to give it a try. In case there are missing items or other suggestion,
    please, do not hesitate in getting in touch.</p>
<table class='table table-bordered table-hover table-striped'>
    <tbody>
        <tr>
            <th></th>
            <th class="center">TAP</th>
            <th class="center">SubUnit</th>
        </tr>
        <tr>
            <th>Human and Machine readable format</th>
            <td class="center">Yes</td>
            <td class="center">Yes</td>
        </tr>
        <tr>
            <th>Language independent</th>
            <td class="center">Yes</td>
            <td class="center">Yes</td>
        </tr>
        <tr>
            <th>Programming languages supported<sup><a href="#5">5</a></sup></th>
            <td class="center">Perl, Python, PHP, Java, C, C++, C#, Lua, Shell, Ruby, Javascript, Pascal,
                PostgreSQL, Haskell, Lisp, Forth, Limbo</td>
            <td class="center">Python, C, C++ and Shell</td>
        </tr>
        <tr>
            <th>Since</th>
            <td class="center">1987</td>
            <td class="center">2006</td>
        </tr>
        <tr>
            <th>Grouping tests in some category/tag style</th>
            <td class="center">Proposal<sup><a href="#6">6</a></sup><sup><a href="#7">7</a></sup></td>
            <td class="center">Yes</td>
        </tr>
        <tr>
            <th>Extensible</th>
            <td class="center">Yes, YAML</td>
            <td class="center">N/A?</td>
        </tr>
        <tr>
            <th>Documentation</th>
            <td class="center">Good, but old.</td>
            <td class="center">Few examples, blogs or Wikis for beginners.</td>
        </tr>
        <tr>
            <th>Used in real-world?</th>
            <td class="center">Yes, an enormous number of modules in <a href="http://www.cpan.org/">CPAN</a> use it
            </td>
            <td class="center">Yes (e.g.: <a href="http://www.samba.org/">Samba</a>)
            </td>
        </tr>
        <tr>
            <th>Format specification</th>
            <td class="center">Draft at <a
                href="http://testanything.org/wiki/index.php/TAP_at_IETF:_Draft_Standard">IETF</a></td>
            <td class="center">Information on Python Package Index <sup><a href="#8">8</a></sup></td>
        </tr>
        <tr>
            <th>Show time of tests</th>
            <td class="center">Yes, with YAML</td>
            <td class="center">Yes, natively</td>
        </tr>
        <tr>
            <th>Use custom test status</th>
            <td class="center">No</td>
            <td class="center">No</td>
        </tr>
        <tr>
            <th>Attach files to test result</th>
            <td class="center">Yes, Base64 encoded in YAML</td>
            <td class="center">Yes, Base64 encoded in test output</td>
        </tr>
    </tbody>
</table>

<h2>Examples</h2>

TAP: 
{%geshi 'shell'%}
1..1
not ok 1 Wrong length 
    ---
    wanted: 5
    found: 4
    time: 2011-02-01 00:09:01-07
    extensions: 
        files: 
            1.txt:
                name: 1.txt 
                file-type: text/plain 
                file-size: 43 
                content: c2FtcGxl ...{%endgeshi%}

SubUnit (using Python + nose): 
{%geshi 'shell'%}
time: 2011-05-23 22:49:38.856075Z
test: my_test.SampleTestCase.runTest 
failure: my_test.SampleTestCase.runTest 
[ 
    Traceback (most recent call last): File "/media/windows/dev/java/qa_workspace/python_nose_tests/src/my_test.py", line
    11, in runTest self.assertEqual(len(s), 4, 'Wrong length') AssertionError: Wrong length 
] 
time: 2011-05-2322:49:38.858163Z{%endgeshi%}

<h2>Final considerations</h2>

<p>Although I posted this comparison in my blog my intention is turning it to the community somehow, probably putting it in
Wikipedia. Perhaps my thoughts here were biased by my proximity with TAP, however I am open to suggestions, ideas or
critics (as a proof that I am open to SubUnit, I included it to the list of 'Other test protocols' in TAP Wiki, as there
was only TST :-))</p>

<p>Initially I wrote this post as a draft and sent it to Max, Nick, Cesar Fernandes and to Robert Collins for 
revisions (hadn't heard back from Robert, unfortunately). Later I plan sending it to the TAP
development team and for the guys responsible for the Automake GSoC TAP/SubUnit project. Then decide which protocol
stick with to develop the TAP Plug-in (or SubUnit :-)). When this analysis is finished I will write an alpha version of
this plug-in to send to the Jenkins dev-list, let me know if you would like to give it a try too. I believe that the
easiest way to spread TAP or SubUnit as the de facto standard is using it, and asking for maintainers of test frameworks
such as TestNG and JUnit to add support for these formats in theirs tools or make it the default output format.

<hr/>

<p><strong>Edit</strong></p>

<p>As pointed by Renormalist, some tools that generate TAP also use another kind of diagnostics for extending the
    test protocol. In this approach, in the next line after a test result the first character is a '#' followed by a
    message. A test result may have several comment lines with diagnostic information. The comments in this case, belong
    to the test result above it. Perl Test::More module produces diagnostics in this way by default. Below you find an
    example of these diagnostics.</p>

{%geshi 'shell'%}
1..1 
not ok 1 - There's a foo user 
# Failed test 'There's a foo user' 
# at /home/kinow/perl/workspace/tests_with_testmore/main.pl line 2. 
# Since there's no foo, check that /etc/bar is set up right 
# Looks like you failed 1 test of 1.{%endgeshi%}

<sup><a name="1"></a>1</sup>
Available in TAP version 13, http://testanything.org/wiki/index.php/YAMLish.

<sup><a name="2"></a>2</sup>
During this article I use TAP Plug-in to refer to the plug-in to display detailed test result, though after talking with
Max we agreed that perhaps it would be a good idea implement it in some generic manner, not specific to TAP. We also
agreed it would be good check other plug-ins like
<a href="https://wiki.jenkins-ci.org/display/JENKINS/xUnit+Plugin">xUnit</a>
to see if we can extend it or use some code as basis.

<sup><a name="3"></a>3</sup>
Still got think more about it. Probably the images will be enclosed in the TAP Stream (or another format) Base64
encoded. Perhaps we would have to decode each attachment in the test result and display it according to its mimetype
(zips, pdf, etc). But a lightbox gallery for attachments would be awesome!

<sup><a name="4"></a>4</sup>
For the first version of this comparison table I added the items that I could think of, and other items retrieved from
the comparison done in Automake GSoC discussion list about the choice between TAP and SubUnit.

<sup><a name="5"></a>5</sup>
Here we considered languages that have at least one producer for the the protocol.

<sup><a name="6"></a>6</sup>
Test Blocks proposal,
<a href="http://testanything.org/wiki/index.php/Test_Blocks">http://testanything.org/wiki/index.php/Test_Blocks</a>
.

<sup><a name="7"></a>7</sup>
Test Groups proposal,
<a href="http://testanything.org/wiki/index.php/Test_Groups">http://testanything.org/wiki/index.php/Test_Groups</a>
.

<sup><a name="8"></a>8</sup>
Python Package Index for python-subunit 0.0.6,
<a href="http://pypi.python.org/pypi/python-subunit/0.0.6">http://pypi.python.org/pypi/python-subunit/0.0.6. This
    was the only one that I could find, but there may have another specification somewhere else.</a>

<h2>Referecens</h2>

* Jenkins dev-list discussion where the TAP Plug-in idea was sent to
<a href="http://jenkins.361315.n4.nabble.com/Re-Additional-Test-Result-Display-Idea-tt3510669.html">http://jenkins.361315.n4.nabble.com/Re-Additional-Test-Result-Display-Idea-tt3510669.html</a>
* Another discussion in Jenkins dev-list about Test Result refactoring
<a href="http://jenkins.361315.n4.nabble.com/Review-requested-Test-Result-Refactoring-tt978100.html">http://jenkins.361315.n4.nabble.com/Review-requested-Test-Result-Refactoring-tt978100.html</a>
* Test Anything Protocol Wiki -
<a href="http://www.testanything.org">http://www.testanything.org</a>
* Perl Wikipedia Article, History section -
<a href="http://en.wikipedia.org/wiki/Perl#History">http://en.wikipedia.org/wiki/Perl#History</a>
* automake - Interfacing with a test protocol like TAP or subunit (GSoC)
<a href="http://www.google-melange.com/gsoc/proposal/review/google/gsoc2011/slattarini/1">http://www.google-melange.com/gsoc/proposal/review/google/gsoc2011/slattarini/1</a>

