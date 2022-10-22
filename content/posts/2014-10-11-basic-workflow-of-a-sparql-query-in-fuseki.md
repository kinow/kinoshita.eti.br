---
categories:
- blog
date: "2014-10-11T00:00:00Z"
tags:
- sparql
- jena
title: Basic workflow of a SPARQL query in Fuseki
---

Before using any library or tool in a customer project, specially when it is an Open Source one, 
there are many things that I like to look at before deploying it. Basically, I look at the 
features, documentation, community, open issues (in special blockers or criticals), the time 
to release fixes and new features and, obviously, the license.

At the moment I'm using [Apache Jena](http://jena.apache.org) to work with ontologies, SPARQL 
and data matching and enrichment for a customer. 

Jena is fantastic, and similar tools include [Virtuoso](http://www.w3.org/wiki/VirtuosoUniversalServer), 
[StarDog](http://stardog.com/), [GraphDB](http://www.ontotext.com/products/ontotext-graphdb-owlim/), 
[4Store](http://4store.org/) and others. From looking at the code and its community and documentation, 
Jena seems like a great choice. 

I'm still investigating if/how we gonna need to use inference and reasoners, looking 
at the issues, and learning my way through its code base. The following is my initial mapping 
of what happens when you submit a SPARQL query to Fuseki.

<img src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/drawing1.png" alt="Fuseki SPARQL query work flow" />

My understanding is that Fuseki is just a web layer, handling a bunch of validations, logging, 
error handling, and relying on the ARQ module, that is who actually handles the requests. 
I also think a new Fuseki server is baking in the project git repo, so stay tuned for an 
updated version of this graph soon.

Happy hacking!
