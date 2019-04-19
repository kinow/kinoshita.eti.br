---
title: 'Cypher, Gremlin and SPARQL: Graph dialects'
author: kinow
tags:
    - graphs
    - neo4j
    - gremlin
    - sparql
category: 'blog'
time: '10:14:33'
---

When I was younger and my older brother was living in Germany, I asked him if he 
had learned German. He said that he did, and explained that there are several 
dialects, and he was quite proud for some people told him that he was using the 
Bavarian dialect correctly.

Even though [Cypher](http://www.neo4j.org/learn/cypher), 
[Gremlin](http://gremlindocs.com/) and [SPARQL](http://en.wikipedia.org/wiki/SPARQL) 
are all query languages, I think we can consider them dialects of a common graph language. 
Cypher is the query language used in [neo4j](http://www.neo4j.org/), a graph database. 
Gremlin is part of the [Tinkerpop](http://www.tinkerpop.com/), an open source project 
that contains graph server, graph algorithms, graph language, among other sub-projects. 
And last but not least, SPARQL is used to query [RDF documents](http://en.wikipedia.org/wiki/Resource_Description_Framework).

Let's use the example of the Matrix movie provided by neo4j to take a look at the 
three languages.

## Cypher

First we create the graph.

```SQL
create (matrix1:Movie {id : '603', title : 'The Matrix', year : '1999-03-31'}),
 (matrix2:Movie {id : '604', title : 'The Matrix Reloaded', year : '2003-05-07'}),
 (matrix3:Movie {id : '605', title : 'The Matrix Revolutions', year : '2003-10-27'}),

 (neo:Actor {name:'Keanu Reeves'}),
 (morpheus:Actor {name:'Laurence Fishburne'}),
 (trinity:Actor {name:'Carrie-Anne Moss'}),

 (matrix1)<-[:ACTS_IN {role : 'Neo'}]-(neo),
 (matrix2)<-[:ACTS_IN {role : 'Neo'}]-(neo),
 (matrix3)<-[:ACTS_IN {role : 'Neo'}]-(neo),
 (matrix1)<-[:ACTS_IN {role : 'Morpheus'}]-(morpheus),
 (matrix2)<-[:ACTS_IN {role : 'Morpheus'}]-(morpheus),
 (matrix3)<-[:ACTS_IN {role : 'Morpheus'}]-(morpheus),
 (matrix1)<-[:ACTS_IN {role : 'Trinity'}]-(trinity),
 (matrix2)<-[:ACTS_IN {role : 'Trinity'}]-(trinity),
 (matrix3)<-[:ACTS_IN {role : 'Trinity'}]-(trinity)
```

<code>Added 6 labels, created 6 nodes, set 21 properties, created 9 relationships, returned 0 rows in 2791 ms</code>

And execute a simple query.

```SQL
MATCH (a:Actor { name:"Keanu Reeves" })
RETURN a
```

<code>(9:Actor {name:"Keanu Reeves"})</code>

## Gremlin

Again, let's start by creating our graph.

```sql
g = new TinkerGraph();
matrix1 = g.addVertex(["_id":603,"title":"The Matrix", "year": "1999-03-31"]);
matrix2 = g.addVertex(["_id":604,"title":"The Matrix Reloaded", "year": "2003-05-07"]);
matrix3 = g.addVertex(["_id":605,"title":"The Matrix Revolutions", "year": "2003-10-27"]);

neo = g.addVertex(["name": "Keanu Reeves"]);
morpheus = g.addVertex(["name": "Laurence Fishburne"]);
trinity = g.addVertex(["name": "Carrie-Anne Moss"]);

neo.addEdge("actsIn", matrix1); 
neo.addEdge("actsIn", matrix2); 
neo.addEdge("actsIn", matrix3); 
morpheus.addEdge("actsIn", matrix1); 
morpheus.addEdge("actsIn", matrix2); 
morpheus.addEdge("actsIn", matrix3); 
trinity.addEdge("actsIn", matrix1); 
trinity.addEdge("actsIn", matrix2); 
trinity.addEdge("actsIn", matrix3); 
```

And execute a simple query.

```sql
g.V.has('name', 'Keanu Reeves').map
```

<code>gremlin> g.V.has('name', 'Keanu Reeves').map
==>{name=Keanu Reeves}
gremlin></code>

Quite similar to neo4j.

## SPARQL

Let's load our example (thanks to [Kendall G. Clark](https://twitter.com/kendall)). I used 
[Fuseki](http://jena.apache.org/documentation/serving_data/) to run these queries.

```xml
@prefix :          <http://example.org/matrix/> .

 :m1 a :Movie; :title "The Matrix"; :year "1999-03-31".
 :m2 a :Movie; :title "The Matrix Reloaded"; :year "2003-05-07".
 :m3 a :Movie; :title "The Matrix Revolutions"; :year "2003-10-27".
 
 :neo a :Actor; :name "Keanu Reeves".
 :morpheus a :Actor; :name "Laurence Fishburne".
 :trinity a :Actor; :name "Carrie-Anne Moss".
 
 :neo :hasRole [:as "Neo"; :in :m1].
 :neo :hasRole [:as "Neo"; :in :m2].
 :neo :hasRole [:as "Neo"; :in :m2].
 :morpheus :hasRole [:as "Morpheus"; :in :m1].
 :morpheus :hasRole [:as "Morpheus"; :in :m2].
 :morpheus :hasRole [:as "Morpheus"; :in :m2].
 :trinity :hasRole [:as "Trinity"; :in :m1].
 :trinity :hasRole [:as "Trinity"; :in :m2].
 :trinity :hasRole [:as "Trinity"; :in :m2].
```

And finally the SPARQL query.

```sql
SELECT ?a WHERE {
   ?a a <http://example.org/matrix/Actor> .
   ?a <http://example.org/matrix/name> ?name .
   FILTER(?name  = "Keanu Reeves")
}
```

Returning the Keanu Reeves actor instance.

<pre>-----------------------------------
| a                               |
===================================
| &lt;http://example.org/matrix/neo&gt; |
-----------------------------------</pre>

SPARQL supports inference (or I must say that OWL, RDFS and the reasoners do), 
but it is easier to define the depth of a search in the graph using neo4j. As for 
Gremlin, it has native support to Groovy and Java. There is a common denominator 
for these three languages, but what makes them really powerful are their unique features. 

I hope you enjoyed, and that this post gave you a quick overview of some of the existing 
graph languages. Make sure you ponder the pros and cons of each server/language, and 
make the best decision for your project. Take a look at [other graph query languages](http://en.wikipedia.org/wiki/Graph_database#APIs_and_Graph_Query.2FProgramming_Languages) too.

Happy hacking!

---

This post has been updated as suggested by [@kendall](https://twitter.com/kendall) (Thank you!).
You can check the diff at [GitHub](https://github.com/kinow/kinoshita.eti.br/commits/master/site/_content/posts/2014-09-09_cypher-gremlin-and-sparql-graph-dialects.html)
