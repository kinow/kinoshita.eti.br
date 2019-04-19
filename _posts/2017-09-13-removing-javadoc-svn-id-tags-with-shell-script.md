---
date: 2017-09-13 16:49:26 +1300
layout: post
tags:
- programming
- shell script
- opensource
- apache software foundation
title: Removing Javadoc SVN Id Tags with Shell Script
---

Subversion supports [Keyword Substitution](http://svnbook.red-bean.com/en/1.4/svn.advanced.props.special.keywords.html), which performs substitution of some keywords such as _Author_, _Date_, and **_Id_**. The **_Id_** is the date, time, and user that last modified the file.

It used to be common to all Apache Commons components to have a line as follows in the header of each Java class.

```java
/**
 * SomeClass class.
 *
 * @version $Id$
 */
public class SomeClass {
    
}
```

Then the generated Javadoc would contain the date of when the class was altered. Although useful, with proper versioning, it becomes obsolete. It is much more important to know what is the version of the software, not the last time it was modified or by whom. In case you have a problem with that specific file, you can always check the history of the file using `git log`, or `git bisect`, or &hellip;

Apache Commons components that are migrated to git need to have these lines removed. git does not support these Subversion Keywords so it is never properly rendered. And as every time I have to remove these lines I come up with some shell script snippet, I decided to document the last one I wrote, so that it can save me some time &dash; and perhaps for somebody else too?

```shell
find . -name "*.java" -exec sed -i '/^.*\*\s*@version\s*\$Id\$.*$/d' {} \;
```

And then [push a commit](https://github.com/apache/commons-collections/commit/29d2e93966e7fb99a888a58ab43480e485dcdfc6) with the change :-) In case you know some regex, you can change it and use the same command syntax to remove comments, specific configuration lines, etc.

That's all. Happy scripting!

&hearts; Open Source
