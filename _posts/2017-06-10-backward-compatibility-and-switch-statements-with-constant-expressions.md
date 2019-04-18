---
title: "Backward compatibility and switch statement with constant expressions"
author: kinow
tags: 
    - java
    - programming
    - apache software foundation
    - opensource
time: '17:35:39'
---

Maintaining Open Source software can be challenging. Making sure you keep backward compatibility (not only binary) can be even more challenging. [Apache Commons Lang](https://commons.apache.org/proper/commons-lang/) 3.6 release is happening right now thanks to [Benedikt Ritter](http://www.benediktritter.de/), and it is on its fourth Release Candidate (i.e. RC4).

A previous RC2 was cancelled due to [IBM JDK 8 compatibility](http://commons.markmail.org/thread/57sqt2hkusegda73#query:+page:1+mid:dnwo5tjqo2e5bwuo+state:results), more specifically the lazy initialization of ArrayList's seems to be different in Oracle JDK and IBM JDK.

The RC3 was cancelled due to a [change](https://github.com/apache/commons-lang/commit/18e692478dcf91fdceb9b9fdca7c61a1111d63aa) that could affect users using a switch statement.

The change was in the *CharEncoding* class. The issue was that this class has some constants, that stopped being [constant expressions](http://docs.oracle.com/javase/specs/jls/se8/html/jls-15.html#jls-15.28).

<blockquote>A constant expression is an expression denoting a value of primitive type or a String that does not complete abruptly and is composed using only the following (...)</blockquote>

{% geshi 'java' %}
public class CharEncoding {
    // ...
    public static final String ISO_8859_1 = "ISO-8859-1";
    // ...
}
{% endgeshi %}

The code above contains a constant (*static final*) variable, that is a constant expression. So users can safely use it in switch statements, and the Java compiler won't complain about it.

{% geshi 'java' %}
public class CharEncoding {
    // ...
    public static final String ISO_8859_1 = StandardCharsets.ISO_8859_1.name();
    // ...
}
{% endgeshi %}

The code above is from the change that caused the regression. Any user that was using the ISO_8859_1 constant variable in a switch statement would get a compilation error (e.g. *case expressions must be constant expressions*) when updating to Apache Commons Lang 3.6. That is because the constant variable is not a constant expression.

I think I learned that some time ago, but if you asked me what was wrong with the change, and if it would break backward compatibility, I would probably fail to spot the issue. There are tools for that now (e.g. Clirr, japicmp) though they may miss some cases too.

Luckily in this case a user subscribed to the Apache Commons development mailing list spotted the issue and quickly reported it. It gets easier maintaining an Open Source project with the constructive feedback of users, like this one.

&hearts; Open Source
