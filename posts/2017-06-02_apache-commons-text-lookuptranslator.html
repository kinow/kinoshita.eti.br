---
title: "Apache Commons Text LookupTranslator"
author: kinow
tags: 
    - apache software foundation
    - java
    - opensource
    - programming
time: '22:50:39'
---

[Apache Commons Text](http://commons.apache.org/proper/commons-text/) includes several algorithms for text processing. Today's post is about one of the classes available since the 1.0 release, the [LookupTranslator](http://commons.apache.org/proper/commons-text/apidocs/org/apache/commons/text/translate/LookupTranslator.html).

It is used to translate text using a lookup table. Most users won't necessarily be - knowingly - using this class. Most likely, they will use the [StringEscapeUtils](http://commons.apache.org/proper/commons-text/apidocs/org/apache/commons/text/StringEscapeUtils.html), which contains methods to escape and unescape CSV, JSON, XML, Java, and EcmaScript.

{% geshi 'java' %}
String original = "He didn't say, \"stop!\"";
String expected = "He didn't say, \\\"stop!\\\"";
String result   = StringEscapeUtils.escapeJava(original);
{% endgeshi %}

StringEscapeUtils uses CharSequenceTranslator's, including LookupTranslator. You can use it directly too, to escape other data your text may contain, special characters not supported by some third party library or system, or even a simpler case.

In other words, you would be creating your own StringEscapeUtils. Let's say you have some text where numbers must never start with the zero digital, due to some restriction in the way you use that data later.

{% geshi 'java' %}
Map<String, String> lookupTable = new HashMap<>();
lookupTable.put("a", "");
final LookupTranslator escapeNumber0 = new LookupTranslator(new String[][] { {"0", ""} });
String escaped = escapeNumber0.translate("There are 02 texts waiting for analysis today...");
{% endgeshi %}

That way the resulting text would be "There are 2 texts waiting for analysis today", allowing you to proceed with the rest of your analysis. This is a very simple example, but hopefully you grokked how LookupTranslator works.

&hearts; Open Source
