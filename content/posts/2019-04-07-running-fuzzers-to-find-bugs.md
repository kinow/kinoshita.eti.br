---
categories:
- blog
date: "2019-04-07T00:00:00Z"
note: The comparison does not focus so much on how fuzzers work, which one is best
  than the other, etc. It looks only into its advertised features, whether it is maintained
  by a group or individual ([bus factor](https://en.wikipedia.org/wiki/Bus_factor)
  is always important), and the license.
tags:
- opensource
- security
- programming
- fuzzing
title: Running fuzzers to find bugs
---

Fuzzifying is a technique used in automated tests to find bugs in programs with unexpected data. fuzzer is the name given to the program used for running these tests. Some fuzzers also generate random data used for the tests.

{{< showimage
  image="stink-bug-smaller.png"
  alt=""
  caption=""
  style=""
>}}

<!--more-->

This technique is useful as programmers do not always write the code worrying about what if a user inputs binary data into a field that is expecting the name of a user? Crashes in programs due to unexpected data are used in security attacks.

Google offers [OSS-Fuzz](https://github.com/google/oss-fuzz), a project that offers infrastructure for any Open Source project that is considered important to be tested. This project is extremely useful, as running fuzzers is something that normally takes days or weeks. So you would need either a server or leave your computer running for a long time. And if you use SSD disks, it may reduce the life span of your disk.

_NOTE: In this [Wikipedia page](https://en.wikipedia.org/wiki/Fuzzing) you can read more about fuzzers, and the types of fuzzers. Or [this other article from Johan Engelen](https://johanengelen.github.io/ldc/2018/01/14/Fuzzing-with-LDC.html) which has a great introduction, and also talks about LLVM libFuzzer project, not mentioned in this post._

## Comparing a few fuzzers

The most well-known fuzzer is probably [`afl`](http://lcamtuf.coredump.cx/afl/), or american fuzzy lop. If you would like to run it against your project, you have to create a small utility that accepts the test parameters and calls your program - unless your program contains an interface compatible with what the fuzzer expects.

But there are fuzzers with integration with build tools, other fuzzers that use neural networks, some are created specifically to run against a certain tool or programming language.

Most of these fuzzers listed here appeared in issues in projects that I monitor, such as projects from Jenkins, Apache Software Foundation, Mozilla, and others. I use `afl` whenever I need to fuzz a project. But knowing only one tool (or programming language FWIW) is not normally a good idea, so in this post I will compare a few fuzzers.

### afl

[http://lcamtuf.coredump.cx/afl/](http://lcamtuf.coredump.cx/afl/)

>American fuzzy lop is a security-oriented fuzzer that employs a novel type of compile-time instrumentation and genetic algorithms to automatically discover clean, interesting test cases that trigger new internal states in the targeted binary. This substantially improves the functional coverage for the fuzzed code.

Probably the most famous. Used to find issues in programming languages, browsers, and many famous projects. Applies genetic algorithms for the data generation.

Licensed under the Apache License, maintained by one person. Code shared as a `.tar.gz` via the author website.

### GramTest

[https://github.com/codelion/gramtest](https://github.com/codelion/gramtest)

>This tool allows you to generate test cases based on arbitrary user defined grammars. The input grammar is given in BNF notation. Potential applications include fuzzing and automated testing.

Learned about GramTest in an [Apache Commons Validator](https://issues.apache.org/jira/browse/VALIDATOR-410) issue. It is interesting that you can define how your program expects the inputs to be via a BNF grammar.

```html
# file: csv.bnf
<CSV>       ::= [<header>] <record> {<crlf> <record>}  [ <crlf> ]
<header>    ::= <name> { <comma> <name>}
<record>    ::= <field> { <comma> <field>}
<name>      ::= <field>
<field>     ::= <escaped> | <nonescaped>
<escaped>   ::= <dquote> (<textdata> | <comma> | <cr> | <lf>) <dquote>
<nonescaped> ::= (<textdata>)
<comma>     ::= ","
<cr>        ::= "\r"
<dquote>    ::= """
<lf>        ::= "\n"
<crlf>      ::= <cr> <lf>
<textdata>  ::= <text> [<textdata>]
<text> ::= Ŝ | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

The grammar is then used to generate the random data fed into the program under test.

The project has two contributors in GitHub, 60 stars, and is licensed under the Apache License.

### RamFuzz

[https://github.com/dekimir/RamFuzz](https://github.com/dekimir/RamFuzz)

>RamFuzz is a fuzzer for individual method parameters in unit tests. A unit test can use RamFuzz to generate random parameter values for methods under test. The values are logged, and the log can be replayed to repeat the exact same test scenario. But random parameter values aren't limited to just fundamental types: RamFuzz can also automatically produce random objects of any class from the user's code.

Learned about this one after [a post on Hacker News](https://news.ycombinator.com/item?id=15795961). It appears to be limited to C++, as it parses the source code to create random objects and data (i.e. it reads the class, structs, variables, etc).

Has one contributor, 267 stars, and is licensed under the Apache License.

### Javan Warty Pig

[https://github.com/cretz/javan-warty-pig](https://github.com/cretz/javan-warty-pig)

>Javan Warty Pig, or JWP, is an AFL-like fuzzer for the JVM. It uses bytecode instrumentation to trace execution. It is written in Java and requires Java 8+.

Java only. You write a test in Java, importing the classes from `jwp.fuzz.*` in order to create the test scenarios.

One maintainer, 31 stars, licensed under the MIT License.

### Kelinci

[https://github.com/isstac/kelinci](https://github.com/isstac/kelinci)

>Interface to run AFL on Java programs.

Learned about this one from an [Apache Commons Imaging](https://issues.apache.org/jira/browse/IMAGING-215) issue. You must install `afl` first, then the documentation guides you through the steps to create the Java layer with Kelinci. That will trigger `afl` for your Java program.

Two contributors, 92 stars, licensed under the Apache License.

### sandsifter

[https://github.com/Battelle/sandsifter](https://github.com/Battelle/sandsifter)

>The sandsifter audits x86 processors for hidden instructions and hardware bugs, by systematically generating machine code to search through a processor's instruction set, and monitoring execution for anomalies. Sandsifter has uncovered secret processor instructions from every major vendor; ubiquitous software bugs in disassemblers, assemblers, and emulators; flaws in enterprise hypervisors; and both benign and security-critical hardware bugs in x86 chips.

Useful for searching bugs in the processor, not so much for common libraries and applications I reckon.

One contributor, 201 stars, licensed under the BSD-3 license.

### jFuzz

[https://ntrs.nasa.gov/search.jsp?R=20100024457](https://ntrs.nasa.gov/search.jsp?R=20100024457)

>jFuzz is a concolic whitebox fuzzer, built on the NASA Java PathFinder, an explicit-state Java model checker, and a framework for developing reliability and analysis tools for Java. Starting from a seed input, jFuzz automatically and systematically generates inputs that exercise new program paths. jFuzz uses a combination of concrete and symbolic execution, and constraint solving. Time spent on solving constraints can be significant. We implemented several well-known optimizations and name-independent caching, which aggressively normalizes the constraints to reduce the number of calls to the constraint solver. We present preliminary results due to the optimizations, and demonstrate the effectiveness of jFuzz in creating good test inputs. The source code of jFuzz is available as part of the NASA Java PathFinder. jFuzz is intended to be a research testbed for investigating new testing and analysis techniques based on concrete and symbolic execution. The source code of jFuzz is available as part of the NASA Java PathFinder. 

I could not easily find the code. It looks like I would have to search by the code of PathFinder. And I could not find any of these in NASA's GitHub. But appears to have good features, and to be built for Java.

Would be nice to see some of its features compared (and maybe contributed) to other tools.

### KiF

[https://dl.acm.org/citation.cfm?id=1326313](https://dl.acm.org/citation.cfm?id=1326313)

>Our paper describes a stateful protocol fuzzer for SIP. The main contribution of our paper is a flexible, adaptive fuzzer capable  to  track  the  state  of  the  targeted  application  and device.  One of the components of our work is quite generic and reusable for any protocol for which an underlying gram-mar is known.  The second one is dependent on the domain specifics  (SIP).  To  the  best  of  our  knowledge,  this  is  the first SIP fuzzer capable to go beyond the simple generation of random input data.  Our method is based on a learning algorithm where real network traces are used to learn and train an attack automata.

Could not find the source code (common for some papers unfortunately). It seems to have a grammar too, like GramTest.

### zzuf

[https://github.com/samhocevar/zzuf](https://github.com/samhocevar/zzuf)

>zzuf is a transparent application input fuzzer. It works by intercepting file operations and changing random bits in the program's input. zzuf's behaviour is deterministic, making it easy to reproduce bugs.

Has an extensive list of bugs found in many applications, like `afl`. Few bugs in the website, but the git repository appears to be actively maintained. It appears to modify the existing input (e.g. your normal test data).

Eight contributors, 261 stars, licensed under the _Do What The F*ck You Want To Public License_.

## Conclusion

There are several different fuzzers, many more than the ones listed here. I will keep using `afl` for now, with plans to use it against [Cylc](https://cylc.github.io). But might try GramTest and its BNF grammar, as well as zzuf as Cylc has an extensive test battery. Adjusting the settings for how much the data is modified in zzuf could lead to interesting test failures, but I wonder if it will be able to distinguish failures from crashes.

## Other links

- [Wikipedia page on Fuzzing](https://en.wikipedia.org/wiki/Fuzzing)
- [Fuzzing D code with LDC, Programming blog of Johan Engelen. D, C++, LLVM, LDC, ... ](https://johanengelen.github.io/ldc/2018/01/14/Fuzzing-with-LDC.html)
- [Fuzzing Adobe Reader for exploitable vulns (fun != profit), kciredor's information security blog](https://kciredor.com/fuzzing-adobe-reader-for-exploitable-vulns-fun-not-profit.html)
- [The Fuzzing Project, by Hanno Böck](https://fuzzing-project.org/)
