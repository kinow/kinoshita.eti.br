---
title: 'Using Apache Commons Functor functional interfaces with Java 8 lambdas'
id: 1217
author: kinow
tags:
    - apache software foundation
    - java
    - functional programming
time: '15:08:14'
category: 'functional programming'
---
<p><a href='http://commons.apache.org/sandbox/functor/'>Apache Commons Functor</a> (hereon [functor]) is an <a href='http://commons.apache.org/'>Apache Commons</a> component that provides a functional programming API and several patterns implemented (visitor, generator, aggregator, etc). <a href="http://openjdk.java.net/projects/lambda/" title="Java 8 lambda">Java 8</a> has several nice new features, including lambda expressions and <a href="http://datumedge.blogspot.com.br/2012/06/java-8-lambdas.html">functional interfaces</a>. In Java 8, lambdas or lambdas expressions are <a href="http://tronicek.blogspot.com.br/2007/12/closures-closure-is-form-of-anonymous_28.html">closures</a> that can be evaluated and behave like anonymous methods.</p>

<p>Functional interfaces are interfaces with only one method. These interfaces can be used in lambdas and save you a lot of time from writing anonymous classes or even implementing the interfaces. [functor] provides several functional interfaces (thanks to <a href="https://issues.apache.org/jira/browse/FUNCTOR-20">Matt Benson</a>). It hasn't been released yet, but there are some new examples in the project site, in the <a href="http://svn.apache.org/viewvc/commons/proper/functor/trunk/" title="[functor] SVN trunk">trunk of the SVN</a>. I will use one of these examples to show how [functor] functional interfaces can be used in conjunction with Java 8 lambdas.</p>

<p>After the example with [functor] in Java 8, I will explain how I am running Java 8 in Eclipse (it's kind of a <a href="http://www.speaklikeabrazilian.com/expression/define?e=Gambiarra" title="Gambiarra">gambiarra</a>, but works well).</p>

<!--more-->

## Example using Apache Commons Functor

<p>Here is a simple example with one Predicate.</p>

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4);

UnaryPredicate<Integer> isEven = new UnaryPredicate<Integer>() {
    public boolean test(Integer obj) {
        return obj % 2 == 0;
    }
};

for( Integer number : numbers ) {
    if (isEven.test(number)) {
        System.out.print(number + " ");
    }
}
```

<p>It prints only the the even numbers, those that pass by the predicate test.</p>

## Example with Java 8 lambdas

<p>This modified version is using Java 8 lambdas</p>

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4);

UnaryPredicate<Integer> isEven = (Integer obj) -> { return obj % 2 == 0; };
 
for( Integer number : numbers ) {
    if (isEven.test(number)) {
        System.out.print(number + " ");
    }
}
```

<p>The behaviour is the same. <strong>UnaryPredicate</strong> is a functional interface. Its only method is <code>boolean test(A obj);</code>. And when used in a lambda expression you just have to provide the right number of arguments and implement the closure code.</p>

<p>The difference in the two code snippets are the way that the UnaryPredicate for even numbers is created. Below you can see the two ways of creating this predicate, with and without Java 8 lambdas.</p>

```java
// pre-java-8
UnaryPredicate isEven = new UnaryPredicate() {
    public boolean test(Integer obj) {
        return obj % 2 == 0;
    }
};

// with lambda-8
UnaryPredicate isEven = (Integer obj) -> { return obj % 2 == 0; };
```

<h3>Java 8 in Eclipse</h3>

<p>Eclipse 8 doesn't support Java 8, so you have to create a new builder in order to have Eclipse compiling your project's sources. For a complete step-by-step guide on how to set up Eclipse Juno and Java 8, please refer to <a href="http://tuhrig.de/?p=921" title="http://tuhrig.de/?p=921">http://tuhrig.de/?p=921</a>. I will summarize the steps here, and will show how to include [functor] jar to the project classpath.</p>

<ul>
	<li>Download the JDK from <a href="http://jdk8.java.net/lambda" title="http://jdk8.java.net/lambda">http://jdk8.java.net/lambda</a> and install it (I installed in <em>/opt/java/jdk1.8.0</em>)</li>
	<li>Create a new Java project in Eclipse (<em>try-lambdas</em> in my case)</li>
	<li>Disable the default <strong>Java Builder</strong> from your Eclipse project, as it doesn't work with Java 8</li>
	<li>Create a new builder. When prompted with a screen that lets you browse for a program, select Java 8 javac (for me it was <em>/opt/java/jdk1.8.0/bin/javac</em>)</li>
	<li>Add the arguments below to your builder: <br />
```shell
-classpath %CLASSPATH%;commons-functor-1.0-SNAPSHOT-jar-with-dependencies.jar;.
-source 8
-d ${workspace_loc:/lambdas}/bin
${workspace_loc:/Java8}/src/lambdas/*.java
```
</li>
</ul>

<p>You have to include [functor]'s jar, as well as its dependencies. For the sake of convenience, I used <a href="http://maven.apache.org/plugins/maven-assembly-plugin/" title="maven-assembly-plugin">maven-assembly-plugin</a> to generate a jar with dependencies for [functor]. The code and the jar are available from this <a href="https://github.com/kinow/try-lambdas" title="try-lambdas GitHub repository">GitHub repository</a>. Or if you prefer generate your own [functor] jar with dependencies, check out the code from the repository as below.</p>

```shell
svn checkout https://svn.apache.org/repos/asf/commons/sandbox/functor/trunk/ commons-functor
```

<p>And finally include the following to [functor] <em>pom.xml</em> before running <code>mvn clean assembly:assembly</code>.</p>

```xml
<plugin>
  <artifactId>maven-assembly-plugin</artifactId>
  <version>2.3</version>
  <configuration>
    <descriptorRefs>
      <descriptorRef>jar-with-dependencies</descriptorRef>
    </descriptorRefs>
  </configuration>
</plugin>
```

<p>Thanks for your time, hope you enjoyed it! :-)</p>
