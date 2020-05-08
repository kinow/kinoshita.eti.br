---
layout: post
tags:
- programming
categories:
- blog
title: Code coverage helps, but it is not enough
---

Today I talked to two QA Engineers about code coverage, and we all agreed that code coverage helps, but is
not enough. By coincidence today I had to fix a bug in tap4j that reminded me the same thing. My
cobertura (the coverage tool that I was using at moment) report said that my code was covered by my tests.
However, there was a bug in the covered code. 

If you are curious about the code you can see the issue here. Or if you really would like to know more
about code coverage, I suggest you to read this fantastic article written by Brian Marick in 99 with the
title ‘How to misuse code coverage’. 

Will finish this post quoting him:

>‘[…] they (code coverage tools) are only helpful if they’re used to enhance thought, not to replace it’.

Cheers
