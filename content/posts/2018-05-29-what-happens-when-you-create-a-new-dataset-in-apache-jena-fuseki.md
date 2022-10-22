---
categories:
- blog
date: "2018-05-29T00:00:00Z"
tags:
- jena
- apache software foundation
- java
- sparql
- opensource
title: What happens when you create a new dataset in Apache Jena Fuseki
---

<a href="{% post_url 2018-05-27-what-happens-when-you-upload-a-turtle-file-in-apache-jena-fuseki %}">Last post</a>
was about what happens when you upload a Turtle file to Apache Jena Fuseki. And now today's post will be about
what happens when you create a new dataset in Apache Jena Fuseki.

In theory, that happens before you upload a Turtle file, but this post series won't follow a logical order.
It will be more based on what I find interesting.

Oh, the dataset created is **an in-memory dataset**. Here's a simplified sequence diagram. Again,
these articles are more brain-dumps, used by myself for later reference.

<img style="display: inline; width: 100%;" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/sequence-diagram.png"  />

<!--more-->

### ActionDatasets#execPostContainer() (Fuseki Core)

`ActionDatasets`, as per the name, handles HTTP requests related to datasets. Such as when you
create a new dataset. It is also an HTTP action. The concept in Jena, as far as I could tell,
is similar to Jenkins' actions, but simpler, without the UI/Jelly/Groovy part.

This class also has a few static fields, which hold system information. One variable is actually
called `system`. (wonder how well it works if you try to deploy Jena Fuseki with multiple JVM's
[<sup>1</sup>](https://markmail.org/message/xpfcgccuwgycdopw) [<sup>2</sup>](https://afs.github.io/rdf-delta/ha-fuseki.html)).

Its first task is to create an *UUID*, using `JenaUUID` (from Jena Core). This class looks
very interesting, [wonder how it works]({% post_url 2018-08-11-uuids-in-apache-jena %}).

Then it creates a `DatasetDescriptionRegistry`, which is a registry to keep track
of the datasets created. There is also some validation of parameters and state check, and then
the transaction is started (`system.begin()`).

### Model / (Core)

I used `Model` and `ModelFactory` before when working with ontologies and Prot&eacute;g&eacute;.
`ActionDatasets` will create a `Model`.

<blockquote>    An RDF Model.

    An RDF model is a set of Statements.  Methods are provided for creating
    resources, properties and literals and the Statements which link them,
    for adding statements to and removing them from a model, for
    querying a model and set operations for combining models.
</blockquote>

It also gets a `StreamRDF` from the model (i.e. `model.getGraph()`), which will be used
later by the `RDFParser`.

### ActionDatasets#assemblerFromForm() (Fuseki)

In `#assemblerFromForm()`, it will create a template, and then use
`RDFParser` to parse the template and load into `SteamRFF`. The template looks like this:

```sparql
# Licensed under the terms of http://www.apache.org/licenses/LICENSE-2.0

@prefix :        <#> .
@prefix fuseki:  <http://jena.apache.org/fuseki#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix tdb:     <http://jena.hpl.hp.com/2008/tdb#> .
@prefix ja:      <http://jena.hpl.hp.com/2005/11/Assembler#> .

## ---------------------------------------------------------------
## Updatable in-memory dataset.

<#service1> rdf:type fuseki:Service ;
    # URI of the dataset -- http://host:port/aaa
    fuseki:name                        "aaa" ;
    fuseki:serviceQuery                "sparql" ;
    fuseki:serviceQuery                "query" ;
    fuseki:serviceUpdate               "update" ;
    fuseki:serviceUpload               "upload" ;
    fuseki:serviceReadWriteGraphStore  "data" ;     
    fuseki:serviceReadGraphStore       "get" ;
    fuseki:dataset                     <#dataset> ;
    .

# Transactional, in-memory dataset. Initially empty.
<#dataset> rdf:type ja:DatasetTxnMem .
```

### Persisting the dataset

Jena Fuseki will create a local copy of the template, using RIOT's `RDFDataMgr`. For my environment, running from
Eclipse, the file location was */home/kinow/Development/java/jena/jena/jena-fuseki2/jena-fuseki-core/run/system_files/902154aa-2bb6-11b2-8053-024232e7b374*.

Fuseki now will look for exactly one Service Name statement (http://jena.apache.org/fuseki#name). The
name will be validated for things like blank space, empty, '/', etc.

Once the validation passes, then it will persist the file in somewhere like
/home/kinow/Development/java/jena/jena/jena-fuseki2/jena-fuseki-core/run/configuration/aaa.ttl. But
not without checking first it the file existed.

As this is a brand new file, the `Model` instance will be written on the file now.

### DatasetAccessPoint (ARQ)

Funny, when I wrote it I immediately put this class under Fuseki Core, but it is actually
in ARQ. **Why not in Fuseki?**. Looks like ARQ has a Web layer too.

Fuseki's `FusekiBuilder#buildDataAccessPoint()` creates the `DataAccessPoint`. The `DataAccessPoint`'s
Javadocs say: &ldquo;A name in the URL space of the server&rdquo;.

* `DataService` contains operations, and endpoints
* Services are added to endpoints, such as an endpoint for the `Quads_RW`, the `REST_Quads_RW` from previous post
* The name and the data service are used to create the `DataAccessPoint`

The current `HttpAction` in the request contains a reference to Fuseki's
`DataAccessPointRegistry`. Fuseki's `DataAccessPointRegistry` extends Atlas'
`Registry`, which uses a `ConcurrentHashMap` (again, how does it work with multiple JVM's?).

The new `DataAccessPoint` is registered with Fuseki's registry (not the other registry).

And then, finally, the transaction is committed, the response is prepared (a 200 OK in `text/plain`).
And a `null` is returned, which means empty response.

And here's some of the logs produced during this experiment.

```shell
[2018-05-28 21:11:43] Config     INFO  Load configuration: file:///home/kinow/Development/java/jena/jena/jena-fuseki2/jena-fuseki-core/run/configuration/ds2.ttl
[2018-05-28 21:11:43] Config     INFO  Load configuration: file:///home/kinow/Development/java/jena/jena/jena-fuseki2/jena-fuseki-core/run/configuration/p1.ttl
[2018-05-28 21:11:43] Config     INFO  Register: /ds2
[2018-05-28 21:11:43] Config     INFO  Register: /p1
[2018-05-28 21:11:43] Server     INFO  Started 2018/05/28 21:11:43 NZST on port 3030
[2018-05-28 21:11:52] Admin      INFO  [1] GET http://localhost:3030/$/server
[2018-05-28 21:11:52] Admin      INFO  [1] 200 OK (11 ms)
[2018-05-28 21:12:41] Admin      INFO  [2] GET http://localhost:3030/$/server
[2018-05-28 21:12:41] Admin      INFO  [2] 200 OK (3 ms)
[2018-05-28 21:22:33] Admin      INFO  [3] POST http://localhost:3030/$/datasets
[2018-05-28 21:46:25] Admin      INFO  [3] Create database : name = /aaa
[2018-05-28 22:16:17] Admin      INFO  [3] 200 OK (3,224.390 s)
[2018-05-28 22:16:18] Admin      INFO  [4] GET http://localhost:3030/$/server
[2018-05-28 22:16:18] Admin      INFO  [4] 200 OK (8 ms)
```

So that's that.

Happy hacking !
