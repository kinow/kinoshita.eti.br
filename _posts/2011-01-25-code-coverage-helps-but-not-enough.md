---
title: 'Code coverage helps, but it''s not enough'
id: 523
author: kinow
tags: 
    - software quality
time: '19:41:59'
---
Today I talked to two QA Engineers about code coverage and we all agreed that code coverage helps, but is not enough. And by coincidence today I had to fix a bug in <a title="tap4j - Test Anything Protocol API for Java" href="http://tap4j.sourceforge.net/">tap4j</a> that reminded me the same thing. My <a title="Cobertura homepage" href="http://cobertura.sourceforge.net/">cobertura</a> (the coverage tool that I was using at moment) report said that my code was covered by my tests. However there was a <em>bug in the covered code</em>.
<p style="text-align: center;"><a title="tap4j Cobertura report" href="http://tap4j.sourceforge.net/cobertura/index.html"><img class="size-medium wp-image-525  aligncenter" title="Cobertura code coverage" src="{{assets.coverage}}" alt="Cobertura code coverage" width="300" height="165" /></a></p>
If you are curious about the code you can see this issue <a title="tap4j BUG #3165200" href="http://sourceforge.net/tracker/?func=detail&amp;aid=3165200&amp;group_id=351793&amp;atid=1470124">here</a>. However if you really would like to know more about code coverage, I suggest you to read this <a title="How to misuse code coverage - Brian Marick" href="http://www.exampler.com/testing-com/writings/coverage.pdf">fantastic article</a> written by Brian Marick in 99 with the title "How to misuse code coverage".

I will finish this post now quoting him:

<blockquote>"they (code coverage tools) are only helpful if they're used to enhance thought, not to replace it".</blockquote>

Cheers :-)
