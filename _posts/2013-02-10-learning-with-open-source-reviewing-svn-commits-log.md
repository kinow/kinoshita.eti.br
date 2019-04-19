---
title: 'Learning with Open Source: Reviewing SVN commits log'
id: 1270
author: kinow
tags:
    - apache software foundation
    - functional programming
    - java
category: 'open source'
time: '13:02:45'
---
<p>Last year I became an <a href="http://www.apache.org" title="Apache">Apache</a> committer, and dedicated most of my time learning the <a href="http://incubator.apache.org/learn/theapacheway.html" title="The Apache Way">Apache way</a>, reading different mailing lists and getting used to the things a committer is supposed to know (voting process, keeping everything in the mailing list, and so it goes) and getting used to <a href="http://commons.apache.org/functor" title="Apache Commons Functor">[functor]</a> API.</p>

<p>In 2013 I hope I can help in the release of [functor], since Java and <a href="http://reddit.com/r/functionalprogramming">functional programming</a> are getting a lot more of attention recently, probably due to the <a href="http://openjdk.java.net/projects/lambda/" title="Project Lambda">project lambda</a>. But I also want to start contributing with the other components from commons (like <a href="http://commons.apache.org/math/" title="Apache Commons Math">math</a>, <a href="http://commons.apache.org/io/" title="Apache Commons IO">io</a>, <a href="http://commons.apache.org/jcs/" title="Apache Commons JCS">jcs</a>) and other top level projects (<a href="http://hadoop.apache.org/" title="Apache Hadoop">hadoop</a>, <a href="http://nutch.apache.org/" title="Apache Nutch">nutch</a>, <a href="http://lucene.apache.org/" title="Apache Lucene">lucene</a>).</p>

<h4>Reviewing SVN commits log</h4>

<p><a href="https://issues.apache.org/jira/browse/FUNCTOR-14" title="Apache Commons Functor - Issue 14">FUNCTOR-14</a> was created to enhance the <a href="http://commons.apache.org/functor/apidocs/org/apache/commons/functor/generator/package-summary.html">generators API</a> in [functor]. I'd worked on <a href="http://svn.apache.org/viewvc/commons/proper/functor/branches/generators-FUNCTOR-14/">a branch</a> for this issue, but needed some review in order to be able to merge it with the trunk. That's where you can see why Open Source is so awesome. Another Apache member, Matt Benson, created <a href="http://svn.apache.org/viewvc/commons/proper/functor/branches/FUNCTOR-14-mm/">another branch</a> to work on the project structure, but also to review the generator API.</p>

<p style='text-align: center'><a href="{{assets.feather_small}}"><img src="{{assets.feather_small}}" alt="Apache Software Foundation" width="203" height="61" class="alignnone size-full wp-image-1125" /></a></p>

<!--more-->

<p>Matt merged my branch, but also reviewed all my work. I'm no big fan of pair programming with two keyboards and all (as I've seen in some "<em>Agile</em>" companies round here in Brazil). But this kind or pair programming is, IMO, one of the most powerful techniques for learning how to code.</p>

<p>However, that would be very easy if one simply waited for someone to review his work, and then forget about everything once it's merged into trunk. Now it's hammer time!</p>

<p>I'm reviewing Matt's changes to my branch and, before I jump in and write some more code, I decided to write this post to keep everything that was changed. That's because I learn better when I write things down.</p>

<ul>
<li><a href="http://svn.apache.org/viewvc?view=revision&revision=1439133">r1439133</a> - use primitives where warranted; simplify some loops</li>
<li><a href="http://svn.apache.org/viewvc?view=revision&revision=1439134">r1439134</a> - file org/layout</li>
<li><a href="http://svn.apache.org/viewvc?view=revision&revision=1439135">r1439135</a> - tighten comparable</li>
<li><a href="http://svn.apache.org/viewvc?view=revision&revision=1439140">r1439140</a> - tighten comparable</li>
<li><a href="http://svn.apache.org/viewvc?view=revision&revision=1439153">r1439153</a> - start to merge commonalities among NumericRanges, including a few small bugfixes</li>
<li><a href="http://svn.apache.org/viewvc?view=revision&revision=1439626">r1439626</a> - per http://en.wikipedia.org/wiki/Interval_%28mathematics%29, 'unbounded' is not synonymous with 'open'; both 'open' and 'closed' are 'bounded.'  If this can be proven incorrect I'm only too happy to retract this commit.</li>
<li><a href="http://svn.apache.org/viewvc?view=revision&revision=1439633">r1439633</a> - keywords</li>
<li><a href="http://svn.apache.org/viewvc?view=revision&revision=1439637">r1439637</a> - fix predicated generators' implementations/tests</li>
</ul>

<p>I learned that I have to pay more attention to generics, follow the principle of using primitives where warranted, and thoroughly analyse loops and ifs. Ah, and that I don't know how to use <a href="http://svnbook.red-bean.com/en/1.4/svn.advanced.props.special.keywords.html" title="SVN Keywords">SVN keywords</a> :-)</p>
