---
categories:
- blog
date: "2020-04-11T00:00:00Z"
note: Notes taken while reading a piece of Apache Jena's source code.
tags:
- apache software foundation
- apache jena
- stream processing
- open source
- java
title: Notes on Apache Jena StreamRDFWriter
---

[Apache Jena](https://jena.apache.org/) project is like a box full of interesting things—at least if you love programming. One of its many features, is **stream processing**.

The graphs in Jena may contain very large datasets, with giga- or terabytes. Some queries may be very large, and then sending the whole result would be simply impracticable.

Instead, the data will go through ARQ. ARQ is a query engine for Jena that supports SPARQL. There is one piece of code there that I found interesting while reviewing a small pull request: [`org.apache.jena.riot.system.StreamRDFWriter`](https://github.com/apache/jena/blob/cbdba5edb47041a4181a00bd7660e5d4c212530a/jena-arq/src/main/java/org/apache/jena/riot/system/StreamRDFWriter.java).

It is responsible for writing graph data in a streaming fashion. (See [stream processing](https://en.wikipedia.org/wiki/Stream_processing) for programming models and more.)

## Stream factories

`StreamRDFWriter` holds several implementations (as `static` members) of `StreamRDFWriterFactory`. The factory has one responsibility only, to create streams (`StreamRDF`), for a certain format and context.

{{< showimage
  image="01.png"
  alt=""
  caption=""
  style=""
>}}

<!--more-->

## Streams writer registry

All these factories and streams, the writer also needs a `registry`. It is used to access the writers required for streams using certain languages.

So if you have your graph dataset, and need to retrieve triples as thrift, you will interrogate the registry asking for a factory of that language (Turtle, N-Triples, RDF-Thrift, etc) or format (Flat Turtle, N-Quads, N-Triples-ASCII, RDF-Thrift, etc).

{{< showimage
  image="02.png"
  alt=""
  caption=""
  style=""
>}}

## Writing data to streams

Each writer has one responsibility too—I really like the design of certain modules in Jena.

{{< showimage
  image="03.png"
  alt=""
  caption=""
  style=""
>}}

The action, however, happens somewhere else. In the `StreamRDFOps` and in the `Iterator` implementations is where the stream processing really takes place.

{{< showimage
  image="04.png"
  alt=""
  caption=""
  style=""
>}}

But this goes beyond the `StreamRDFWriter`. So that's all for today.
