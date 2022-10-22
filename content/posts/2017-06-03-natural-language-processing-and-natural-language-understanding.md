---
categories:
- blog
date: "2017-06-03T00:00:00Z"
tags:
- natural language processing
- programming
title: Natural Language Processing and Natural Language Understanding
---

I used [**Natural Language Processing**](https://en.wikipedia.org/wiki/Natural_language_processing) (NLP) tools in a few projects in the past years. But only recently, while involved with a [chatbot](https://en.wikipedia.org/wiki/Chatbot) project, I noticed the term [**Natural Language Understanding**](https://en.wikipedia.org/wiki/Natural_language_understanding) (NLU).

NLU can be seen as a subfield of NLP. NLP englobes all techniques used for parsing text and extracting some knowledge about it. It could be finding out what are the common entities in the text, calculating the likelihood of a certain word being a preposition or a verb, sentiment analysis, or even spell checking sentences.


<div class='row'>
<div class="ui fluid container">
<figure>
<a  href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/nlp-nlu.png" rel="prettyPhoto" class="thumbnail" title="NLP, NLU, and NLG">
<img style="height: 400px;" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/nlp-nlu.png" alt="NLP, NLU, and NLG" />
</a>
</figure>
</div>
</div>

When you are processing a language, it does not mean you are understanding the language. You may simply have rules, statistics, or some heuristics built to extract the information you need for some work.

NLU, on the other hand, implies that a system will try to understand the text. A text such as *"Given the price of mandarin lately, how likely is it to increase as much as the bananas?"*, could be parsed with NLP tools such as OpenNLP, CoreNLP, spaCy, etc.

However, you would have annotated text, entities, sentiment, perhaps coreference, but you still would not be able to build a machine that simply understands it. You can - with some effort - build rule based systems, apply semantics and ontologies, or use information retrieval techniques.

But it is still extremely hard to build a system to understand all the ways it could be said, slightly modified, such as *"are mandarins getting as expensive as bananas?"*, or take into consideration context information like localization or time *"were mandarins getting as expensive as bananas around the Pacific Islands five years ago?"*.

There are other subfields in NLP, such as [**Natural Language Generation**](https://en.wikipedia.org/wiki/Natural_language_generation) (NLG). Techniques from both NLU and NLG are used in chat bots, to parse the language and also to generate text based on the conversation.

NLP is an extremely interesting topic. 2001: A Space Odissey, Star Trek, The Foundation Series, and other science fiction books and movies. These all have intelligente computer systems that interact with humans. But should we tried to re-create these right now, even with all the work on machine learning, we would still have very funny (and perhaps dangerous) results.

<div class='row'>
<div class="ui fluid container">
<figure>
<a  href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/spock-nlp.png" rel="prettyPhoto" class="thumbnail" title="NLP and Spock">
<img style="height: 300px;" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/spock-nlp.png" alt="NLP and Spock" />
</a>
</figure>
</div>
</div>

&hearts; NLP
