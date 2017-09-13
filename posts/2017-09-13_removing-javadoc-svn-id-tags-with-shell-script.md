---
title: Removing Javadoc SVN $Id$ Tags With Shell Script
time: '16:49:26'
---

Subversion supports [Keyword Substitution](http://svnbook.red-bean.com/en/1.4/svn.advanced.props.special.keywords.html), which performs substitution of some keywords such as Author, Date, and **Id**. The **Id** is the date time and user, showing when the file was last modified.

It used to be common to all Apache Commons components to have a line as follows in the header of each file.

{% geshi 'java' %}
/**
 * SomeClass class.
 *
 * @version $Id$
 */
public class SomeClass {
    
}
{% endgeshi %}

Then the generated Javadoc would contain the date of when the class was altered. Although useful, with proper versioning, it becomes obsolete. It is much more important to know what is the version of the class, not the last time it was modified or by whom. In case you have a problem with the file, you can always check the history of the file (e.g. use `git log`, or `git bisect` &hellip;).

Apache Commons components that are migrated to git need to have these lines removed, as git does not support these Subversion Keywords. And as every time I decide to remove these lines I come up with some sort of shell script snippet, I decided to document this last one, so that it can save me some time and, perhaps, also save some time for somebody else.

{% geshi 'shell' %}

{% endgeshi %}

That's all. Happy scripting!

&heats; Open Source
