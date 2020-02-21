---
layout: post
tags:
- jenkins
- java
- programming
- opensource
categories:
- blog
title: Troubleshooting a Jenkins Plug-in compatibility issue
---

This post is probably different from others. I will give a TL;DR, but will then
give you a copy of
[a comment of a Jenkins JIRA issue](https://issues.jenkins-ci.org/browse/JENKINS-42655?focusedCommentId=291470&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-291470).
Hope you have fun reading it,
specially if you maintain Jenkins servers or plug-ins.

TL;DR: there was an issue in Jenkins Job DSL Plug-in, that caused jobs created to
have an invalid script. The fix had not been released, but was already in the
master branch in GitHub.

<p style="text-align: center; color: #DDDDDD;">&diams;</p>

*Well, that was fun bug reproduced, I believe I know why that's happening. Not so complicated to fix... but no fast way to fix it. Here's the issue analysis (grab a coffee to read it).*

* *Downloaded jenkins.war (2.32.3.war)*
* *mkdir /tmp/123*
* *JENKINS_HOME=/tmp/123 java -jar jenkins.war*
* *Entered secret into form and submitted*
* *Installed suggested plugins (boy that takes a while)*
* *Created temp user*
* *Installed (without restart) active-choices-plugin 1.5.3*
* *Installed (without restart) job-dsl-plugin*
* *Manually stopped Jenkins, and started it again with same command #3*
* *Log in with user, all looking good*
* *Created Freestyle job JENKINS-42655 (see attached config.xml)*
* *Executed job, and found new job JENKINS-42655-1*
* *Never opened the job configuration, clicked on the "Generated Items link to JENKINS-42655-1" to open in a new tab*
* *Clicked on Build with Parameters*
* *Looked at logs, and noticed the security-script-plugin exceptions*
* *Went to "Manage Jenkins" / "In-process Script Approval" and approved scripts*
* *Went back to the JENKINS-42655-1 build with parameters screen, and everything worked as expected*

**Hummm. Issue more or less reproduced. Let's investigate more.*

* *Restarted Jenkins again*
* *Changed the JENKINS-42655 seed job configuration to use a different script*
* *Copied the config.xml file to another location*
* *Went to build with parameters, and now it was broken again*
* *Saved the job manually*
* *Copied the config.xml file to yet another location*
* *Went to build with parameters, and now it worked as reported in this issue*

*Now comes the interesting part. Looking at the diff. Attaching a screen shot so that others can have fun looking at it too. I installed Kompare as it has some cool features such as disabling diff for white spaces, blank lines, etc. The whole file changes as you save it. But if you ignore the number of white spaces... Then you can see that the Job DSL Plug-in is creating a &lt;script&gt; tag, as we used to do before 1.5 I think.*

<div class='row'>
<div class="ui fluid container">
<figure>
<a  href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/JENKINS-42655-diff.png" rel="prettyPhoto" class="thumbnail" title="Screen shot">
<img style="height: 400px;" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/JENKINS-42655-diff.png" alt="Screen shot" />


*Now we use the script-security-plugin. So we need to wrap that around the script-security-plugin's tags. Will report an issue for job-dsl-plugin, and will probably submit a pull request in the next days too. There's not much left we can change in the plug-in code for that Piotr Tempes, so I'm afraid you will have to:*

* *keep saving the job*
* *perhaps work on the fix for Job DSL if you feel like doing it (as you could probably be faster than me in submitting the PR)*
* *use an older version of the active-choices-plugin that doesn't use security-script-plugin, though you could be bitten by other old bugs*
* *write some script to replace the &lt;script&gt; tag and wrap it by the secureScript (doing what the pull request will do automatically later)*

*Sorry for not being able to quickly provide any workaround, nor to cut a quick bugfix release.*

*Cheers*
*Bruno*

<p style="text-align: center; color: #DDDDDD;">&diams;</p>

ps: When I started getting involved in Open Source, I always felt extremely happy when
people would spend their time troubleshooting my issues, or just educating me on how to
behave in an Open Source community, or even how I should have troubleshooted initially
the issue myself. So whenever I have time, I try to write detailed and polite replies. The
person posting the comment is my past. The person posting the comment is my future :-)
[Kindness begets kindness](http://revistaepoca.globo.com/Revista/Epoca/0,,EMI96818-15230,00.html).

&hearts; Open Source
