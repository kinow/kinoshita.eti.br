---
date: 2018-04-28 18:20:28 +1300
layout: post
tags:
- jena
- apache software foundation
- java
- sparql
- opensource
title: Learning more about SPARQL and Jena internals
---

<p style='text-align: center;'>
<a href="https://kinow.deviantart.com/art/O-Corvo-742473382"><img style="display: inline; width: 600px;" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/ocorvo.jpg" alt="O Corvo" /></a>
<br/>
<small><a href="https://kinow.deviantart.com/art/O-Corvo-742473382">O Corvo</a></small>
</p>

Recently a [pull request](https://github.com/apache/jena/pull/114/) for Apache Jena
that I started three years ago got merged. Even though it has been three years since
that pull request, there are still many parts of the project code base that I am
not familiar with.

And not only the code, but there are also many concepts about SPARQL, other standards
used in Jena, and internals about triple stores.

The following list contains some presentations and posts that I am reading right now,
while I try to improve my knowledge of SPARQL and Jena internals.

* [The Semantics of SPARQL](https://www.slideshare.net/olafhartig/the-semantics-of-sparql)
    - Slides with information from Query parsing to Algebra and evaluating the Query
* [SPARQL Order Matters](https://wiki.blazegraph.com/wiki/index.php/SPARQL_Order_Matters)
	- Short but great post from Blazegraph about order in SPARQL queries with JOIN's
	and LEFT JOIN's
* [Jena ARQ Query Performance](https://gregheartsfield.com/2012/08/26/jena-arq-query-performance.html)
	- Old post, but still very useful. Related to the post above, as it also talks about
	query performances due to the order of statements
* [Predicates: LHS vs RHS](http://oracle.readthedocs.io/en/latest/sql/indexes/predicates-lhs-vs-rhs.html)
	- Oracle post for SQL, but this part applies to SPARQL, at least terminology-wise. LHS
	and RHS appear in [some SPARQL related tickets](https://issues.apache.org/jira/browse/JENA-1534)
	/documentation too
