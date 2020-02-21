---
layout: post
tags:
- test anything protocol
- java
- software quality
categories:
- blog
title: Getting the maximum from TestNG with TAP
---

<p>Strangely enough, today I decided start to write about <a href="http://www.testanything.org">TAP</a> (Test Anything Protocol) and received a mail from a <a href="http://www.linkedin.com">Linkedin</a> Group with a white paper about data integration in information systems. Well, let me first explain what is TAP, or Test Anything Protocol. This protocol was created in the beginning of Perl to log test results and is still being used by Perl and other languages (<a href="https://github.com/sebastianbergmann/phpunit/">PHPUnit</a> can output TAP too, for instance).</p>

<p>Now, if you already know about TAP and YAML, or if you are like me and like trying things out before reading a long text, then go to the <a href="#hammertime">hands on part</a> of this post.</p>

<p>An output in TAP, or a TAP stream, is written in pure text in a human readable way. Like follows:</p>

```shell
TAP version 13
1..2
ok 1 Test 1
not ok 2 Missing test parameter: url
```

<!--more-->

<p>What does the TAP Stream above tells you? It tells you that you are using <span style="font-family: courier, sans-serif">TAP version 13</span> (duh, I know), you have a test plan with 2 tests (<span style="font-family: courier, sans-serif">1..2</span>) where the first test passed successfully (<span style="font-family: courier, sans-serif">ok 1</span>) and the second test failed (<span style="font-family: courier, sans-serif">not ok 2</span>). Besides the test status, you also have a description that tells you that the second test failed for missing a test parameter.</p>

<p>And that's it. Really? I don't need to learn anything else? Sorry, I was kidding, but I promise it is not like learning complex dynamic systems or how to find the equilibrium point in a differential equation :-). And I am not going to get in details about all the details of TAP, probably you should check <a href="http://www.testanything.org">http://www.testanything.org</a>, the home of Test Anything Protocol, for complete specification, history and links.</p>

<p>The last thing I need explain to you before putting <a href="http://www.testng.org">TestNG</a> in the story, is <a href="http://yaml.org/">YAML</a>. YAML stands for YAML Ain't Markup Language. It is a data serialization standard, just like <a href="http://www.json.org/">JSON</a>. The main difference you will find between both APIs is that YAML can be a little more human friendly while JSON requires more symbols like {, }, [, ] and ". And it is said too that you can parse JSON with YAML, but the contrary is not always true. Let's see how YAML looks like.</p>

```shell
---
name: Bruno
age: 26
country: Brazil
...
```

<p>TAP utilizes YAML to have '<i><a href="http://testanything.org/wiki/index.php/TAP_diagnostic_syntax">diagnostics</a></i>' of tests. This is the name used in TAP, but probably you will prefer think about it as a way to extend TAP by adding YAML to each test result.</p>

```shell
TAP version 13
1..2
ok 1 Test 1
not ok 2 Missing test parameter: url
---
     file:        selenium_sample_test.t
     line:        12
     description: Missing test parameter: url
     found:       null
     wanted:      string
     extensions:
       screenshot:     /var/tmp/selenium/cath-xp/748344874_screenshot.jpg
...
```

<h2><a name="hammertime">So it's hammer time!</a></h2>

<p>Ok! So you got here either because you couldn't wait to see how you were going to use TAP, YAML and TestNG together, or because you read all the text (if you didn't, I recommend you try reading it later). I will assume here you are familiar with Java and can create a project in your favorite IDE, import libraries and set up a basic test project. I am an Eclipse and Maven user, so all these things are pretty easy for me ;-). Here is my sample test.</p>

```java
package br.eti.kinoshita.testngtap;

import org.testng.Assert;
import org.testng.annotations.Test;

public class SampleTest
{

	@Test
	public void sampleTest()
	{
		Assert.assertTrue( System.currentTimeMillis() > 1984 );
	}
	
}
```

<p>This is a test that only checks if the current time in ms is greater than 1984. If so, it will follow the normal flow and output XML and HTML. Now I challenge you! How can you make this test output TAP? Drum roll... with two simple steps: a) add <a href="http://tap4j.sourceforge.net">tap4j</a> library into your project and b) add a <a href="http://testng.org/doc/documentation-main.html#testng-listeners">Listener</a> to your test.</p>

```java
package br.eti.kinoshita.testngtap;

import org.testng.Assert;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;

import br.eti.kinoshita.tap4j.ext.testng.TestTAPReporter;

@Listeners(TestTAPReporter.class)
public class SampleTest
{

	@Test
	public void sampleTest()
	{
		Assert.assertTrue( System.currentTimeMillis() > 1984 );
	}
	
}
```

<p>Did you find the difference between the last code and the previous one? No? Come on, what about line 9? Yeah, that is the TAP listener. You can find more information about tap4j and TestNG integration <a href="http://tap4j.sourceforge.net/testng_support.html">here</a>. Run this test again and take a look at the output directories of TestNG. You will find some .tap files. These files contain the result of your tests alongside the diagnostic information about them. But wait! You may be asking yourself what is the point in outputting TestNG in another format? Well, apart of having integration with TAP and being able to share your test results with programs that are compatible with TAP (like Perl programs, or Smolder), you can also add customized information to your TAP Stream, transforming it into a perfect evidence for your automated tests, for instance. Look at the following code.</p>

```java
package br.eti.kinoshita.testngtap;

import java.lang.reflect.Method;

import org.testng.Assert;
import org.testng.ITestContext;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;

import br.eti.kinoshita.tap4j.ext.testng.TAPAttribute;
import br.eti.kinoshita.tap4j.ext.testng.TestTAPReporter;

@Listeners(TestTAPReporter.class)
public class SampleTest
{

	@Test
	public void sampleTest( ITestContext injectedCtx, Method injectedMethod)
	{
		
		TAPAttribute attribute = new TAPAttribute(injectedMethod, 1984);
		
		// Setting an attribute in the test context for this method.
		injectedCtx.setAttribute("myBirthdayYear", attribute);
		
		Assert.assertTrue( System.currentTimeMillis() > 1984 );
	}
	
}
```

<p>ITestContext and Method are injected by TestNG during execution. Then you create a TAPAttribute object and add this attribute to the test context, along with an identifier for this attribute. After that you run your test again and take another look at the TAP streams that were generated. You will have two files, br.eti.kinoshita.testngtap.SampleTest.tap and br.eti.kinoshita.testngtap.SampleTest#sampleTest.tap. The first is a TAP Stream for your test class and the latter is a TAP stream for the method of your test class (it generates one TAP Stream for each method). With tap4j listeners you have support to generate TAP per method, per class, per suite or per group (thanks to Cesar Fernandes Almeida). Here is the output for the test class in TAP.</p>

```shell
1..1
ok 1 - br.eti.kinoshita.testngtap.SampleTest#sampleTest
  ---
  message: TestNG Test sampleTest
  severity: '~'
  source: br.eti.kinoshita.testngtap.SampleTest#sampleTest
  datetime: '2011-03-09T23:32:42'
  file: br.eti.kinoshita.testngtap.SampleTest
  line: '~'
  name: sampleTest
  extensions:
    myBirthdayYear: 1984
  got: '~'
  expected: '~'
  display: '~'
  dump: '{param1=org.testng.TestRunner@ff2413, param2=public void br.eti.kinoshita.testngtap.SampleTest.sampleTest(org.testng.ITestContext,java.lang.reflect.Method)}'
  error: '~'
  backtrace: '~'
  ...
```

<p>Each attribute is added as an YAML entry under the 'extensions' entry. You have just gave voice to your TestNG tests. Now they can speak! They can add information to your test results. Perhaps you may be thinking: "Cool, but I don't know where am I going to use it, so I'm going stop reading this bible-like post and will find something more interesting on <a href="http://www.reddit.com">reddit</a>". Hold on, not so fast buddy.</p>

<p>I started using TAP after I had to lead a test automation project with my company. We were using <a href="http://www.teamst.org">TestLink</a> and <a href="http://www.hudson-ci.org">Hudson</a> (and now <a href="http://www.jenkins-ci.org">Jenkins</a>), and in TestLink's forum I read the <a href="http://www.teamst.org/index.php/news-mainmenu-2/13-development/86-testlink-automation-with-tap-successful-story">case of an user</a> who successfully automated his tests with TestLink and TAP. One thing leads to another, and here we are now, with a plug-in that integrates both tools in a simple way.</p>

<p>In this example, we are using <a href="http://testng.org/doc/selenium.html">Selenium and TestNG</a>. But one particularity is that after we take the screen shot in Selenium we use TAP to output the screen shot of that test within the rest of the test report. So TestNG, with a little help of tap4j, generates a TAP Stream that contains a reference for this screenshot file. You can find a sample code that executes Selenium with TestNG and outputs TAP with Selenium screen shots. This strategy is being used in <a href="http://wiki.jenkins-ci.org/display/JENKINS/TestLink+Plugin">TestLink Jenkins Plug-in</a> to execute and update automated tests. We are planning start using TAP in other projects, and build a plug-in for Jenkins that will set Jenkins as an alternative for <a href="http://search.cpan.org/~wonko/Smolder-1.51/bin/smolder">Smolder</a>.</p>

<p>Now I believe that you are ready to have new ideas about how integrate your test data with different systems in your organization environment and take the maximum from TestNG with TAP.</p>

<p>Valeu! Cheers!</p>
