---
layout: post
tags:
- apache software foundation
- functional programming
categories:
- blog
title: Ranges in Apache Commons Functor
---

This is a long post. So here is a <strong>TL;DR</strong>:
<ul>
	<li>Apache Commons Functor has no Double or Float Range (yet)</li>
	<li>Apache Commons Functor IntegerRange and LongRange treat the low value as inclusive, and the high value as exclusive. How does that compare to other languages/APIs? (you will have to read to see some comparison)</li>
	<li>Perl has support for characters ranges, perhaps we could implement it in Functor too?</li>
	<li>In case we implemented a CharacterRange, it would have to be inclusive for both low and high limits. With 'z' being the last character, there wouldn't have a way to include Z with the current approach. Or we would have to make the CharacterRange a special one. What would go against <a title="Liskov Substitution Principle" href="http://en.wikipedia.org/wiki/Liskov_substitution_principle">Liskov Substitution Principle</a>.</li>
	<li>You can see a comparison table with Apache Commons Functor, other Java API's and other programming languages for ranges clicking <a href="#ctable" title="Comparison table">here</a>.</li>
	<li>It would be nice to have a clear distinction in Functor documentation among a Sequence, a Generator and a Range. While I was gathering material for this post, I found places using range, others using sequence, and in Apache Commons Functor, an IntegerRange is a Generator.</li>
</ul>
Now, if you have some spare time or curiosity, keep reading :-)

<!--more-->

This post is about ranges in <a title="Apache Commons Functor" href="http://commons.apache.org/sandbox/functor/">Apache Commons Functor</a> but first let me explain the context. I am working on <a title="nebular Java Fuzzy API" href="http://nebular.sourceforge.net/">nebular</a>, an open source fuzzy logic API. This API is written in pure Java, and has <a title="Matlab Fuzzy Toolbox" href="http://www.mathworks.com/products/fuzzy-logic/index.html">Matlab Fuzzy Toolbox</a> as reference for the initial release. Nebular will use functional programming to let the user to model his/her membership functions. The API chosen for functional programming is Apache Commons Functor.

Yesterday I finished to port <a title="Matlab sigmf membership function" href="http://www.mathworks.com/help/toolbox/fuzzy/sigmf.html">sigmf</a> function to nebular, including some tests that compare nebular's output to Matlab sigmf function. However, here comes the issue with ranges, sequences and generators. The idea is to plot a graph similar to the one below.

<img class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/sigmf_300_160.gif">

The x axis contains values from 0 to 10, increasing by 0.1. In Matlab, I would execute the following command to produce the x vector.

```python
x = 0:0.1:10;
```

The : is the range operator in Matlab. It would create a vector with 101 elements. Yup, 101. That's because in Matlab the low and high value used creating the range are inclusive. Now let's look at how I create similar vector in Apache Commons Functor.

```java
IntegerRange range = new IntegerRange(0, 11, 1 /* step */);
```

So now one can realize two things: there is no Double or Float Range, and the high value in the range is exclusive. It means that in order to create an array (I will use vector and array interchangeably here for simplicity) with Functor from 0 to 10, including both values, you have to create a range using 0 and 11.
<h2>Comparing with other Java functional programming API's</h2>
There are other API's to include functional programming features to Java code. In this comparison I will include <a title="Google Guava" href="http://code.google.com/p/guava-libraries/">Google Guava</a>, <a title="fun4J" href="http://www.fun4j.org/">fun4j</a>, <a title="Functional Java" href="http://functionaljava.org/">functionaljava</a>, <a title="lambdaj" href="http://code.google.com/p/lambdaj/">lambdaj</a> and <a title="op4j" href="http://www.op4j.org/">op4j</a> (got the list from the fun4f project page).
<h3>Google Guava</h3>
Google Guava provides the Range and Ranges classes. The Ranges contains several static methods for creating Range's, that can be used as collections. The Ranges class contains methods for creating Range's with open, closed, openClosed and closedOpen intervals.

```java
public static void main(String[] args) {
    Range<Integer> values = Ranges.closed(0, 10);
    System.out.print("[ ");
    for(Integer value : values.asSet(DiscreteDomains.integers())) {
        System.out.print(value + " ");
    }
    System.out.print("]");
}
```
```python
[ 0 1 2 3 4 5 6 7 8 9 10 ]
```

The Google Guava API does not provide a way to create ranges of floats. And I will have to find some time to read about the asSet method and on discrete domains. I am much more comfortable putting Apache Commons Functor API in my code for creating ranges. Specially since it makes the code more readable and easy to understand, helping to receive contributions in nebular from newcomers.
<h3>fun4j</h3>
fun4j contains classes to model functions, lambdas and bind LISP code to Java. However it has no objects for ranges.
<h3>functionaljava</h3>
Although there is the <a title="Functional Java Seq class" href="http://code.google.com/p/functionaljava/source/browse/trunk/src/main/fj/data/Seq.java?r=358">Seq</a> class, I don't know if that can be used for Ranges. So I will have to skip functionaljava :-(
<h3>lambdaj</h3>
Couldn't find a way to create ranges with lambdaj. Not sure if they support it or not.
<h3>op4j</h3>
Same as lambdaj, couldn't find a way to create ranges with op4j. Not sure if they support it or not.
<h2>Comparing with other programming languages</h2>
So let's see how we could generate a similar array using other programming languages.
<h3>Python</h3>
Python is one of my favorite languages, and has some functional programming features [1]. However it has no built-in mechanism for ranges with floats, only with integers. The functions that I know in Python use low value as inclusive, and high value as exclusive. The built in range functions in 2.7 looks like the following.

```python
x = range(0, 11, 1) #inclusive/exclusive
print x;
```

```python
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

Or you could write something like (remember Perl's motto, TIMTOWTDI [2])

```python
x = [x * 0.1 for x in range(0, 101)]; #inclusive/exclusive

print len(x);
print x;
```

```python
101
[0.0, 0.1, 0.2, 0.30000000000000004, 0.4, ..., 10.0]
```

There are API's in Python too, like numpy, that has arange. However it is complicated specify a range to give similar array as the one produced by Matlab.

```python
from numpy import arange;
x = arange(0, 10.1, .1); #inclusive/exclusive
print len(x);
print x;
```
```python
101
[ 0. 0.1 0.2 ... 10.0]
```

<h3>Perl</h3>
As we mentioned Perl in last section, let's see how it works in Perl. First of all, I won't use many modules here. Probably Perl is the language with more modules, or at least with a plethora of modules in <a title="CPAN" href="http://www.cpan.org">CPAN</a> (wait to see <a title="CJAN" href="http://www.cjan.org">CJAN</a> ;). There are books on Perl and Functional programming [3], and Perl has a built in mechanism for ranges. I used Perl 5 built in range operator and List::Gen range function. Both use the low and high value inclusive. It's important to point out that Larry Wall and the programmers behind Perl are always keeping an eye on usability, ease of use, and Larry's laziness. So that's why Perl is a good language for comparisons of this type.

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

print "[ ";
for(0..10) { #inclusive/inclusive
    print $_, " ";
}
print " ]"
```
```python
[ 0 1 2 3 4 5 6 7 8 9 10 ]
```

Or to use floats, we could use <a title="List::Gen" href="http://search.cpan.org/dist/List-Gen/">List::Gen</a> module.

```perl
#!/usr/bin/perl

use strict;
use warnings;
use feature 'say';
use List::Gen;

my $range = range 0, 10, 0.1; #inclusive/inclusive

print "[ ";
print $_, " " for @$range;
print " ]"
```
```python
[ 0 0.1 0.2 0.3 0.4 ... 10 ]
```

Perl also has support to range of characters. Look at the examples from Perldoc.

```perl
@alphabet = ("A" .. "Z"); # inclusive/inclusive... how would it work if the last argument was not inclusive?
```

That would be cool if Functor had this feature too ;-)
<h3>Scala</h3>
Scala is a language that runs on the Java Virtual Machine, it has some functional programming features as anonymous functions, higher order functions, among others. It has a built in mechanism for ranges with integers or floats. It uses the low value as inclusive, and the high value as exclusive, however when using floats you may have trouble if you don't pay attention to float precision.

```java
object Test {
    def main(args: Array[String]) {
        var range = 0.0 until 10.0 by 0.1;
        println(range);
    }
}
```

```python
NumericRange(0.0, 0.1, 0.2, ..., 9.99999999999998)
```
<h3>Matlab</h3>
Why, yes sir, we will compare Matlab too. It has built in operator for ranges, and both values, low and high, are inclusive.

```matlab
x=0:0.1:10;
display(x);
x =
Columns 1 through 9
0 0.1000 ...
... 10.0000
```

<h3>PHP</h3>

Although famous for its web applications, PHP can be an interesting language for scripting or creating handy utilities. I may be wrong, but I believe the scm_bot in Jenkins project, that posts messages to JIRA when someone commits to a SCM with a special string, is written in PHP. It has a built in function for ranges in 5.3, and both values are inclusive.

```php
$range = range(0, 10, 0.1);
echo "[ ";
foreach($range as $number) {
    echo $number . " ";
}
echo "]";
```

```python
[ 0 0.1 0.2 0.3 ... 9.9 10 ]
```
<h3>Haskell</h3>
Haskell has gained more attention lately with web frameworks. It has features such as monads, functors and high order function. And also has a built-in range operator. Both, left and right values of the range are inclusive in Haskell's range operator.

```python
[0 .. 10]
```

```python
[0,1,2,3,4,5,6,7,8,9,10]
```

Unfortunately I don't know Haskell so well, and couldn't make it work with floats, nor find out whether it is possible or not :-(
<h3>lua</h3>
While lua has no built-in support to ranges, if you search for lua and range functions or operators, probably you will find an entry in lua's Wiki with a range function, contributed by a user. The function implemented uses the low and high value inclusively and has support for both integer and floats.

```lua
-- http://lua-users.org/wiki/RangeIterator
function range(from, to, step)
    step = step or 1
    return function(_, lastvalue)
    local nextvalue = lastvalue + step
    if step > 0 and nextvalue <= to or step < 0 and nextvalue >= to or
        step == 0
    then
        return nextvalue
    end
    end, nil, from - step
end

function f() return 0, 10, 0.1 end

io.write("[ ");
for i in range(f()) do
    io.write(i, " ")
end
io.write("]");
```
```python
[ 0 0.1 0.2 0.3 ...  9.9 10 ]
```
<h3>LISP</h3>
Lisp is probably one of the oldest programming languages with functional features. Every time I read something about functional programming and collections it reminds me of Lisp recursion with lists. In Lisp you can use loop to iterate over a range of integers or floats, and both values are included for integers, for float, there is some precision problem that I couldn't overcome. For integers the following code would do.

```lisp
>(loop for i from 0 to 10 do (print i))
0
1
2
...
10
NIL
```

And for floats.

```lisp
>(loop for i from 0.0 to 10.0 by 0.1 do (print i))
0.0
0.1
0.2
...
9.900002
NIL
```

Again, issues with precision.

<h3>Clojure</h3>
Although Clojure is quite similar to LISP, I had some trouble setting up an example for this. My first try was with loop, but as it didn't work, I used dorun. It uses the low value as inclusive, and the high value as exclusive. Strange, I thought it would have similar behavior to the loop in LISP. But I only know the very basics of each language, and the explanation is beyond my knowledge. Anyway, it's interesting I guess.

```python
(dorun (for [i (range 0 10 1)] (println i)))
0
1
...
9
nil
```
<h2><a name="ctable">Comparison Table</a></h2>
To simplify the understanding, here is a comparison table.

<div style="overflow: scroll">
<table class="ui table"><colgroup><col width="180"/><col width="130"/><col width="134"/><col width="99"/><col width="99"/><col width="99"/><col width="99"/><col width="99"/><col width="135"/><col width="99"/><col width="99"/><col width="99"/><col width="99"/><col width="99"/><col width="99"/><col width="99"/><col width="99"/><col width="99"/></colgroup><tr class="ro1"><th style="text-align:left;width:1.6252in; " class="Default"> </th><th style="text-align:left;width:1.1728in; " class="Default"><p>Apache Commons Functor</p></th><th style="text-align:left;width:1.2047in; " class="Default"><p>Google Guava</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>fun4j</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>functionaljava</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>lambdaj</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>op4j</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>Python</p></th><th style="text-align:left;width:1.2161in; " class="Default"><p>Python  numpy.arange</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>Perl</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>Perl List::Gen</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>Scala</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>Matlab</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>PHP</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>Haskell</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>lua (Wiki contrib)</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>LISP</p></th><th style="text-align:left;width:0.8925in; " class="Default"><p>Clojure</p></th></tr><tr class="ro1"><td style="text-align:left;width:1.6252in; " class="Default"><p>Integer range</p></td><td style="text-align:left;width:1.1728in; " class="Default"><p>YES</p></td><td style="text-align:left;width:1.2047in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:1.2161in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td></tr><tr class="ro1"><td style="text-align:left;width:1.6252in; " class="Default"><p>Float range</p></td><td style="text-align:left;width:1.1728in; " class="Default"><p>NO</p></td><td style="text-align:left;width:1.2047in; " class="Default"><p>NO</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>NO</p></td><td style="text-align:left;width:1.2161in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>NO</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>NO?</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>NO?</p></td></tr><tr class="ro1"><td style="text-align:left;width:1.6252in; " class="Default"><p>Includes low limit</p></td><td style="text-align:left;width:1.1728in; " class="Default"><p>YES</p></td><td style="text-align:left;width:1.2047in; " class="Default"><p>YES/NO</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:1.2161in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td></tr><tr class="ro1"><td style="text-align:left;width:1.6252in; " class="Default"><p>Includes high limit</p></td><td style="text-align:left;width:1.1728in; " class="Default"><p>NO</p></td><td style="text-align:left;width:1.2047in; " class="Default"><p>YES/NO</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>N/A</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>NO</p></td><td style="text-align:left;width:1.2161in; " class="Default"><p>NO</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>NO</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>YES?</p></td><td style="text-align:left;width:0.8925in; " class="Default"><p>NO</p></td></tr></table>
</div>

<hr class="space" />

<p>That's it, I will ping some guys from Apache dev-list to see what they think about the bullets in TL;DR. After writing this post I realized I need to change this blog's layout to give more space for code and tables :-(</p>

<p>Cheers</p>

- [1] <a href="http://docs.python.org/howto/functional.html">http://docs.python.org/howto/functional.html</a>
- [2] <a href="http://c2.com/cgi/wiki?ThereIsMoreThanOneWayToDoIt">http://c2.com/cgi/wiki?ThereIsMoreThanOneWayToDoIt</a>
- [3] <a href="http://perl.plover.com/yak/fp/">http://perl.plover.com/yak/fp/</a>
