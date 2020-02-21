---
date: 2017-05-28 19:50:39 +1300
layout: post
tags:
- apache software foundation
- java
- opensource
- programming
categories:
- blog
title: Some links related to Apache Commons Text
---

[Apache Commons Text](http://commons.apache.org/proper/commons-text/) is one of the most recent new components in Apache Commons. It "is a library focused on algorithms working on strings". I recently collected some links
under a bookmark folder that are in some way related to the project. In case you are interested,
check some of the links below.

* [Morgan Wahl Text is More Complicated Than You Think Comparing and Sorting Unicode PyCon 2017](https://www.youtube.com/watch?v=bx3NOoroV-M) <iframe width="560" height="315" src="https://www.youtube.com/embed/bx3NOoroV-M?rel=0" frameborder="0" allowfullscreen></iframe>
    * Q: test [text] to check if our methods are OK with some examples in this talk)
    * Q: Canonical Decomposition, and code points comparisons; are we doing it? Are we doing it right?
    * Q: Do we have casefolding?
    * Q: Do we have multi-level sort?
    * Q: CLDR
* [Łukasz Langa Unicode what is the big deal PyCon 2017](https://www.youtube.com/watch?v=7m5JA3XaZ4k) <iframe width="560" height="315" src="https://www.youtube.com/embed/7m5JA3XaZ4k?rel=0" frameborder="0" allowfullscreen></iframe>
    * Q: Quite sure we have an issue to guess the encoding for a text.... there is a GPL library for that? Under Mozilla perhaps?
* [Jiaqi Liu Fuzzy Search Algorithms How and When to Use Them PyCon 2017](https://www.youtube.com/watch?v=kTS2b6pGElE) <iframe width="560" height="315" src="https://www.youtube.com/embed/kTS2b6pGElE?rel=0" frameborder="0" allowfullscreen></iframe>
    * Q: Does OpenNLP have N-GRAM's? Would it make sense to have that in [text]?
    * Q: Where can we find some tokenizers? OpenNLP?
* [Lothaire's Books](http://www-igm.univ-mlv.fr/~berstel/Lothaire/) like "Combinatorics on Words" and "Algebraic Combinatorics".
* Java tutorial lesson ["Working with Text"](https://docs.oracle.com/javase/tutorial/i18n/text/)
* Mitzi Morris' [Text Processing in Java book](https://www.amazon.com/Text-Processing-Java-Mitzi-Morris/dp/0988208725)
* [StringSearch](http://johannburkard.de/software/stringsearch/) java library.
    * <blockquote>"The Java language lacks fast string searching algorithms. StringSearch provides implementations of the Boyer-Moore and the Shift-Or (bit-parallel) algorithms. These algorithms are easily five to ten times faster than the na&iuml;ve implementation found in java.lang.String".</blockquote>
* [Jakarta Oro](https://jakarta.apache.org/oro/) (attic)
    * <blockquote>The Jakarta-ORO Java classes are a set of text-processing Java classes that provide Perl5 compatible regular expressions, AWK-like regular expressions, glob expressions, and utility classes for performing substitutions, splits, filtering filenames, etc. This library is the successor to the OROMatcher, AwkTools, PerlTools, and TextTools libraries originally from ORO, Inc. Despite little activity in the form of new development initiatives, issue reports, questions, and suggestions are responded to quickly.</blockquote>
    * Discontinued, but is there anything useful in there? The attic has always interesting things after all...
* [TextProcessing blog](http://textprocessing.org/) - A Text Processing Portal for Humans
* [twitter-text](https://github.com/twitter/twitter-text), the Twitter Java (multi-language actually...) text processing library.
* Python's [text modules](https://docs.python.org/3/library/text.html)

&hearts; Open Source
