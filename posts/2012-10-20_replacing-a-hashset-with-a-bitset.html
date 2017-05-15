---
title: 'Replacing a HashSet with a BitSet'
id: 1111
author: kinow
tags: 
    - apache software foundation
    - java
    - opensource
    - programming
time: '19:51:39'
---
<p>I always read the messages in the <a href="http://www.apache.org/foundation/mailinglists.html" title="Apache mailing lists">Apache dev mailing lists</a>, including Apache Commons <a href="http://commons.apache.org/mail-lists.html" title="Apache Commons mailing lists">dev mailing list</a>. And you should too. There are always interesting discussions. Sometimes you participate, other times you only watch what's happening, but in the end <strong>you always learn something new</strong>.</p>

<p>A few days ago, I found <a href="https://issues.apache.org/jira/browse/LANG-839" title="LANG-839">an issue</a> where it was being proposed to replace an unnecessary <a href="http://docs.oracle.com/javase/6/docs/api/java/util/HashSet.html" title="HashSet">HashSet</a> in <a href="http://commons.apache.org/lang/api-release/org/apache/commons/lang3/ArrayUtils.html" title="ArrayUtils">ArrayUtils</a>#removeElements() by a <a href="http://docs.oracle.com/javase/6/docs/api/java/util/BitSet.html" title="BitSet">BitSet</a>. Here's how the code looked like: </p>

{% geshi 'java' %}
HashSet<Integer> toRemove = new HashSet<Integer>();
for (Map.Entry<Character, MutableInt> e : occurrences.entrySet()) {
    Character v = e.getKey();
    int found = 0;
    for (int i = 0, ct = e.getValue().intValue(); i < ct; i++) {
        found = indexOf(array, v.charValue(), found);
        if (found < 0) {
            break;
        }
        toRemove.add(found++);
    }
}
return (char[]) removeAll((Object)array, extractIndices(toRemove));
{% endgeshi %}

<p style="text-align: center"><a href="{{assets.feather_small}}"><img src="{{ assets.feather_small}}" alt="" title="Apache Software Foundation" width="203" height="61" class="aligncenter size-full wp-image-1125" /></a></p>

<p>The HashSet created at line 1, in the code above, was used to store the array index of the elements that should be removed. And at line 13 there is a call to removeAll method, passing the indexes to be removed. And here's how the new code looks like: </p>

{% geshi 'java' %}
BitSet toRemove = new BitSet();
for (Map.Entry<Character, MutableInt> e : occurrences.entrySet()) {
    Character v = e.getKey();
    int found = 0;
    for (int i = 0, ct = e.getValue().intValue(); i < ct; i++) {
        found = indexOf(array, v.charValue(), found);
        if (found < 0) {
            break;
        }
        toRemove.set(found++);
    }
}
return (char[]) removeAll(array, toRemove);
{% endgeshi %}

<p>The first difference is at line 1. Instead of a HashSet, it is now using a BitSet. And at line 10, instead of adding a new element to the HashSet, now it "sets" a bit in the set (the bit at the specified position is now true). But there are important changes at line 13. The method removeAll was changed, and now the array doesn't require a cast anymore. And the it is not necessary to cast the elements from HashSet anymore, as now the bit in the index position of the set is set to true. So the extractIndices method could be removed.</p>

<p>The code got simpler. But that's not all. At <a href="http://www.apache.org" title="Apache Software Foundation">Apache Software Foundation</a> you can find a lot of talented developers - that's why I got so excited after joining them. Besides simplifying the code, the developer responsible for these changes (<strong>sebb</strong>) also pointed out that the new code <strong>consumes less memory and is faster</strong>. Ah! And he also wrote <strong>unit tests</strong>
