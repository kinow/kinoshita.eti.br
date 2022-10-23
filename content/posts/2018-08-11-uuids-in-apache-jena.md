---
categories:
- blog
date: "2018-08-11T00:00:00Z"
tags:
- apache software foundation
- java
- jena
- opensource
title: UUID's in Apache Jena
---

In this post I won't talk about what are UUID's, or how they work in Java.
[Here](https://www.baeldung.com/java-uuid)'s a great article on that. Or access the always reliable [Wikipedia article](https://en.wikipedia.org/wiki/Universally_unique_identifier)
about it. _(or if you would rather, read the [RFC 4122](http://www.ietf.org/rfc/rfc4122.txt))_

I found out that Jena had UUID implementations after writing a 
[previous post]({% post_url 2018-05-29-what-happens-when-you-create-a-new-dataset-in-apache-jena-fuseki %}).
And then decided to look into which UUID's Jena has, and where these UUID's
were used. This way I would either understand why Jena needed UUID's, or
just be more educated in case I ever stumbled with a change in Jena that
required related work.

<!--more-->

### Jena Core's _org.apache.jena.shared.uuid_

This package is small and simply contains: _factories_,

{{< showimage
  image="zatoichi_crying.png"
  alt="Zatoichi Crying"
  caption="Zatoichi Crying"
  style="float: right; height: 300px;"
>}}

- `UUIDFactory`: interface for a factory of UUID's
- `UUID_V1_Gen`: a factory for `UUID_V1`
- `UUID_V4_Gen`: a factory for `UUID_V4`

and _UUID implementations_,

- `JenaUUID`: abstract base class for UUID implementations
- `UUID_nil`: a special UUID, _nil_, filled with zeroes
- `UUID_V1`: UUID V1
- `UUID_V4`: UUID V4

and a _utility class_

- `LibUUID`: with methods to create a `Random` and to create `byte[]` seeds.

`JenaUUID` contains a method to return a `JenaUUID` as a Java's `UUID`. And is used
in the command line utility `juuid`, for transaction ID's, and when a new
dataset is created. For the new dataset, Fuseki will create files in a temporary
location. The name of the temporary location is created using an instance of
`JenaUUID`.

#### _UUID_V1_ and _UUID_V4_

Jena's `UUID_V1` is an implementation of Version 1 (_time based_),
variant 2 (_DCE_). Which means it uses MAC address and
timestamp to generate the universal unique ID's.

It uses `NetworkInterface.getNetworkInterfaces()` to retrieve the MAC
address of the node running Jena. When using localhost, the MAC
address is not available, so it resorts to using a random number.

----

And Jena's `UUID_V4` is an implementation of Version 4(_random_),
variant 2 (_DCE_). Which means it uses random numbers to generate
the universal unique ID's.

The factory for V4 will have a random for the most significant bits,
and for the least significant bits of the UUID (also including version
and variant). The random for the factory is created by `LibUUID#makeRandom()`.
This method returns a `SecureRandom` with two seeds, one being random, and
the other created with `LibUUID#makeSeed()`.

`UUID_V4` uses a `SecureRandom` created locally but with the seed also set by
`LibUUID#makeSeed()`. The seed returned by this method may use the
MAC address, but will also use the `os.version`, `user.name`, `java.version`,
number of active threads, total memory, free memory, and the hash code
of a newly created `Object`.

### Transaction ID UUID (_TxnIdUuid_) &mdash; uses JenaUUID

Jena contains two implementations of `TxnId` (transaction identifiers),

- `TxnIdSimple`: transaction IDs are created with a counter within each JVM
- `TxnIdUuid`: transaction IDs are created using `JenaUUID`.

The first thing that called my eye in this class was the inconsistency with the
name - which is quite normal in large projects such as Jena.

As `TxnIdUuid` calls `JenaUUID#generate()`, it will use the default factory,
`UUID_V1_Gen`. Then it will call `asUUID` to return a Java `UUID` object but
with the same UUID.

### Create a new dataset in Fuseki (_ActionDatasets_) &mdash; uses JenaUUID

When you create a new dataset in Fuseki, as explained in the
[previous post]({% post_url 2018-05-29-what-happens-when-you-create-a-new-dataset-in-apache-jena-fuseki %}),
Fuseki will create some temporary files and folders. For at least one folder, it will
use an instance of `JenaUUID`, in `ActionDatasets#execPostContainer()`.

### Blank node IDs (_BlankNodeId_) &mdash; uses Java's UUID

Blank nodes in Jena need an identifier too. It is possible to configure Jena
to either return a JVM bound counter (similarly to how `TxnIdSimple` works),
or otherwise blank nodes identifiers will be generated with
`java.util.UUID.randomUUID()`.

_**I wonder why the transaction ID's use Jena's `JenaUUID`s, but the blank
node IDs use Java's UUID**_? They are [compatible](https://github.com/apache/jena/blob/7b011c30b6bf54db44b5b14408f103009adbdd67/jena-core/src/test/java/org/apache/jena/shared/uuid/TestUUID_JRE.java) anyway.

Other methods related to blank nodes also use Java's `UUID`,

- `BlankNodeAllocatorFixedSeedHash`
- `BlankNodeAllocatorHash#freshSeed()`.

### SPARQL functions, and _NodeFunctions_ &mdash; uses Java's UUID

SPARQL 1.1 contains functions [`UUID`](https://www.w3.org/TR/sparql11-query/#func-uuid) and
[`STRUUID`](https://www.w3.org/TR/sparql11-query/#func-struuid). Apache Jena provides
these two functions, and users can use them in queries such as

```sql
SELECT (UUID() AS ?uuid) (StrUUID() AS ?strUuid) WHERE { }
```

(but before users would have to call extra functions in a different namespace).

The function implementations use `NodeFunctions` methods `struuid` and `uuid`. Both methods in
`NodeFunctions` use Java's `UUID`, and not `JenaUUID`.

### Files and directories for databases / datasets &mdash; uses Java's UUID

Files and directories created in Jena use Java's `UUID`,

- `BufferAllocatorMapped#getNewTemporaryFile()`
- `TDBBuilder#create` methods and `ComponentIdMgr` constructor
- `AbstractDataBag#getNewTemporaryFile()`.

### Conclusion

In Jena there are places where instances of `JenaUUID` are used to produce a
UUID, and other places where Java's `UUID` is used.

Java's `UUID` provides a variant 2 version 4 (random DCE), which is equivalent to
`UUID_V4`. But there is no equivalent of `UUID_V1`, the default used in Jena.

And even though `UUID_V4` and `UUID` are compatible, I believe Jena's version is using
a seed with so many JVM and operating system related settings (`os.version`, free memory, etc)
in order to have a unique seed per node running Jena, independent of whether there
are multiple JVM's in the same node.

But to be honest, I am still not sure which one I would have to use, nor if there are
cases where I should pick one over the other...

_EDIT: Apache Jena's lead dev [replied](https://markmail.org/thread/vnys264p4c6lkc6l#query:+page:1+mid:raa7gaxconcnqbzp+state:results) with a bit of history about the project too (:_
