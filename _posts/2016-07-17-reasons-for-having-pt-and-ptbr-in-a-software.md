---
date: 2016-07-17 14:14:03 +1300
layout: post
tags:
- skosmos
- vocabulary server
- translation
- semantic web
categories:
- blog
title: Reasons for having pt and pt-BR in a software
---

Some time ago I found some spare time to work on a different Open Source project:
[SKOSMOS](http://skosmos.org/). SKOSMOS is a web based SKOS browser and publishing
tool, used to create vocabularies using the SKOS ontology.

I decided to help with translation, but there was no Brazilian Portuguese option,
only Portuguese. I used a few arguments to suggest that having Brazilian Portuguese
would be a good thing.

Another Open Source project that I use in a side project is
[LanguageTool](https://www.languagetool.org/). LanguageTool is used for
proof-reading, and uses rules to find spelling and grammar errors.

Today I saw a message in the LanguageTool mailing list discussing whether having a Brazilian
Portuguese page would make sense, or if it would be better to have just Portuguese, and then
add rules for special cases.

<!--more-->

I started writing the reply to that message, then realised it was getting lengthy,
and repeating things I said before for the SKOSMOS project. So I decided to write this
blog post, so that I could link to it, update it, and also share with others
some arguments for having both Brazilian Portuguese and Portuguese
as options in their software.

### Words that are written very similarly, and with same meaning

As with British and American English words like centre and center, colour and color, that are
spelled quite the same and keeping the same etymology, the same happens with
some words in Brazilian and Portugal Portuguese.

* **actual** <sup>pt</sup> and **atual** <sup>pt-BR</sup>
* **acto** <sup>pt</sup> and **ato** <sup>pt-BR</sup>
* **contactar** <sup>pt</sup> and **contatar** <sup>pt-BR</sup>
* **comit&eacute;** <sup>pt</sup> and **comit&ecirc;** <sup>pt-BR</sup>

**Contatar** is an interesting example. It means to contact, to get in touch, and while
it is used in Portugal, it is rarely used in Brazil. Instead what is used is
**entrar em contato**, which would be translated to English as get in touch, or get
in contact.

Look at this example from this [news article](https://www.publico.pt/culturaipsilon/noticia/coleccao-de-arte-de-david-bowie-revelada-1738297)
from P&uacute;blico journal, 2016-07-14.

> Em 1998, foi convidado a juntar-se ao comité editorial do jornal Modern Painters e **contactou** com nomes como Jeff Koons, Hirst e Tracey Emin. <sup>pt</sup>

In Brazilian Portuguese, it would be written in ".. e **entrou em contato** com nomes ...".

The last item in the list, **comit&eacute;**, is a french word, with same meaning in Portuguese.
It can be used in Portugal (see the same [news article](https://www.publico.pt/culturaipsilon/noticia/coleccao-de-arte-de-david-bowie-revelada-1738297) used above),
but in Brazil only **comit&ecirc;** is used.

### Words that are written very similarly, but with different meaning

Whenever I meet a Portuguese, it is always fun to spend some time adjusting my
vocabulary. There are many [false cognates](https://en.wikipedia.org/wiki/False_cognate)
between Brazilian and Portugal Portuguese. 

* **bicha**: can be a queue in Portugal, but its only meaning in Brazil is a
[perjorative word](https://www.priberam.pt/DLPO/bicha)
* **puto**: you can use that for a boy in Portugal, like your son, but again,
is is [really bad word in Brazil](https://www.priberam.pt/DLPO/puto)
* **aspecto**: you can use it to describe the looks of a person in Portugal, in Brazil we normally use **apar&ecirc;ncia** instead
* **cara**: face in Portugal, dude in Brazil, specially in S&atilde;o Paulo
* **pastilha el&aacute;stica** is gum in Portugal, and means nothing in Brazil. A Brazilian would probably thing it is some kind of rubbery thing, or some part of a car.
Brazilians say **chiclete** instead, or **chicle**

### Words exclusive to each country

* **derrube** can be used in Portugal as noun. In Brazil it is only a way of conjugating the verb **derrubar**.
* **pipocar**, a verb in Brazil that means to chicken out
* **fixe**, in Portugal normally used as a noun, meaning cool, awesome. In Brazil is can only be a way of conjugating the verb **fixar**.
* **coima** in Portugal is a fine that you may have to pay for not having a ticket, or parking somewhere it is not legal. Not used in Brazil. Instead **multa** is used.
* **autoclisma** in Portugal is the toilet flush. It has no meaning in Brazil. The toilet flush is called **descarga** in Brazilian Portuguese.

### Different grammar rules for the gerund

Look at the following example for "I am studying".

* Eu estou a estudar <sup>pt</sup>
* Eu estou estudando <sup>pt-BR</sup>

Portugueses and Brazilians can understand each other, even though they have different rules
for when using the gerund. But as for writing, you would never see "Eu estou a estudar"
in Brazilian Portuguese. In Portugal you could find both forms.

Look at this example from [yesterday's news in Portugal](https://www.publico.pt/mundo/noticia/erdogan-lanca-purga-no-exercito-e-na-justica-turcos-festejam-fiasco-de-golpe-1738533):

> Houve caças **a sobrevoar** Istambul e bombas **a cair** na cidade da ponte que se
atravessa para sair da Ásia e chegar à Europa.

In Brazilian Portuguese, that would have been written as:

> Houve caças **sobrevoando** Istambul e bombas **caindo** na cidade da ponte que se
atravessa para sair da &Aacute;sia e chegar &agrave; Europa.

### Different grammar rules for Pronominal Colocation (positioning clitic pronouns)

I will use the definition found in this [blog post](http://polyglotses.blogspot.co.nz/2014/11/pronominal-colocation-in-portuguese.html)
for pronominal colocation: 

> The collocation of oblique unstressed pronouns (me, te, se, o, a, lhe, nos, vos, os, as, lhes) according to the verb.

I won't try to explain it here, as it would require probably several blog posts for that. But what
is important to know, is that the Portuguese used in Brazil and Portugal have different rules
for pronominal colocation.

Look at this example from one of the articles used before from the P&uacute;blico journal.

> Entre a madrugada de s&aacute;bado e o in&iacute;cio da madrugada de domingo, a pra&ccedil;a Taksim 
**encheu-se** v&aacute;rias vezes com turcos a apoiar Erdogan"

In Brazilian Portuguese, that is not incorrect. But it would have been written as follows.

> Entre a madrugada de s&aacute;bado e o in&iacute;cio da madrugada de domingo, a pra&ccedil;a Taksim 
**se encheu** v&aacute;rias vezes com turcos a apoiar Erdogan"

The **mes&oacute;clise**, for example, is not so rare in Portugal.
While in Brazil you *may* find that in some law or old text, it is really rare nowadays.

> Far-lhe-ei uma proposta irrecus&aacute;vel. <sup>pt</sup>

That would sound really awkward in Brazil. But could be written as.

> Farei uma proposta irrecus&aacute;vel. <sup>pt-BR</sup>

### Conclusion

Portuguese is a beautiful language. You can express a lot with words. But it is also
really complicated, with many peculiarities. Even though Brazilians and Portugueses can
understand each other, they say and write things in different ways. While English from UK
and America have words with different spelling, or different words for the same
meaning (like lift, ride, elevator), with Portuguese it is a bit more complicated.

We can take a look at this example from LanguageTool web site for Portuguese.

> Por favor v&ecirc; a lista de problemas comuns se experienciares problemas.
Descarrega vers&otilde;es anteriores ou builds di&aacute;rios.

A Brazilian can definitely understand it. But it does not sound correct. But in Brazilian Portuguese, it would
be written more or less as.

> Por favor veja a lista de problemas comuns se notar algum problema. Baixe vers&otilde;es
anteriores ou builds di&aacute;rios.

Here you can notice that there are different words for the same meaning, like download which is
**descarga** in Portugal, but it is **baixar** in Brazil (descarga in Brazil is the toilet
flush, by the way).

Also, you will never have the verb **ver** (to see) after the word **Por favor** (please),
and followed by the direct object (in this case, the list of problems).

And of course that there is much more. Portugal was invaded by Arabs around the year 700,
and got several words from the Arabic (e.g. a&ccedil;ude<sup>pt</sup>/assudd, a&ccedil;ougue/assok,
javali/jabali, laranja/naranj, xarope/sharab). 

But Brazil has influence of some of the more than [200 languages](https://pt.wikipedia.org/wiki/L%C3%ADnguas_ind%C3%ADgenas_do_Brasil)
that were spoken by natives. Some of these words are not used in Portugal,
like aguap&eacute;, **canjica**, fruits names like **maracuj&aacute;** and **jaboticaba**. There
are differences within the country, such as the use of the **tu** pronoun, common
only in the South, parts of the North and Northeast, and in a few other cities.

According to Wikipedia, there are about 260 million Portuguese speakers in the world.
Where 202 million are in Brazil. But Brazil is the only country in the whole Americas that
speak Portuguese, and its culture is quite different from other Latin America countries.
So it is normal that there are not only spelling differences between the Portuguese that
is spoken in Brazil, and the Portuguese spoken in other countries.

Does it mean every software needs two sections, two translation files? No. But if you have
a page with a few paragraphs, do not expect that it makes sense for both Brazilians and
Portugueses, Portugueses and Angolans, etc.

Consider the size of your public, and be aware that there are other differences, that are not
simply spelling.

Finally, if you would like to take a look at some Brazilian local expressions and slangs,
check out the [Speak Like A Brazilian](https://speaklikeabrazilian.com/) web site.
