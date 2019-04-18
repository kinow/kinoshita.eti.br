---
title: 'Integrating Nutch 2.x, MySQL and Solr'
id: 991
author: kinow
tags: 
    - apache software foundation
    - web crawling
time: '00:02:31'
---
<p>Right now we are working on a new project using <a href="http://nutch.apache.org" title="Apache Nutch">Apache Nutch</a> 2.x, <a href="http://hadoop.apache.org" title="Apache Hadoop">Apache Hadoop</a>, <a href="http://solr.apache.org" title="Apache Solr">Apache Solr</a> 4 and a lot of other cool tools/modules/API's/etc. After following the instructions found on <a href="http://nlp.solutions.asia/?p=180" title="http://nlp.solutions.asia/?p=180">http://nlp.solutions.asia/?p=180</a>, I've successfully connected Apache Nutch, MySQL and Apache Solr.</p>

<p><img src="{{ assets.mysql_hadoop_solr_nutch }}" alt="mysql_hadoop_solr_nutch" title="mysql_hadoop_solr_nutch" width="800" class="aligncenter size-medium wp-image-994" /></p>

<p>In summary:</p>

<ul>
<li>Create a database to hold your data</li>
<li>Use SQLDataStore and add configuration for your MySQL server</li>
<li>Update Apache Nutch configuration</li>
<li>Update Solr schema</li>
</ul>

<p>Now our Apache Nutch uses MySQL as data store (the place where it keeps the result of the crawling process, such as URL,  text content, metadata, and so on). That's grand, but there is one part missing in the Solr Schema provided in the blog post.</p> 

<p>Due to <a href="https://issues.apache.org/jira/browse/SOLR-3432" title="SOLR-3432">SOLR-3432</a>, after following the tutorial and replacing the schema, we couldn't delete the whole index anymore. After following the instructions in the bug comments, and adding the following entry in schema.xml it worked again.</p>

<!--more-->

{%geshi 'xml' %}<field name="_version_" type="long" indexed="true" stored="true"/>{%endgeshi%}

<p>Restart Apache Solr and run the following command and your index will be reset.</p>

{%geshi 'shell' %}curl http://localhost:8983/solr/collection1/update?commit=true -H "Content-Type: text/xml" --data-binary "<delete><query>*:*</query></delete>"{%endgeshi%}

<p>Hope it helps if you are creating a similar set up. In the next posts we will explain how to set up Apache Nutch 2.x branch in Eclipse. It is very helpful for writing and debugging plug-ins.</p>

<p>Laters! -B</p>