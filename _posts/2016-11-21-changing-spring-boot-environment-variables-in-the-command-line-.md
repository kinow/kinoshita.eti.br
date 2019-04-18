---
title: 'Changing Spring Boot environment variables in the command line'
author: kinow
tags:
    - shell script
    - java
    - spring
category: 'blog'
time: '21:26:03'
---

This week while helping developers and testers to experiment with a backend application,
some of them found useful to learn a simple trick to change Spring Boot properties
when you can run the application locally (our testers build, compile, change the code, how cool
is that?).

Here's how it works. Say you have the following settings in your application's
**application.properties**:

{% geshi 'shell' %}
my.application.database.username=sa
my.application.database.password=notasimplepassword
{% endgeshi %}

And that you want to change these parameters in order to, for instance, create an application
error, so that you can code and test what happens to the frontend application in that situation.

You replace *dots* by *underscores*, and put all your words in upper case. So the variables
above would be: MY_APPLICATION_DATABASE_USERNAME and MY_APPLICATION_DATABASE_PASSWORD.

Furthermore, you do not need to edit your application.properties file, if you are on Linux or
Mac OS. You can start the application and override environment variables at the same time
with the following syntax.

{% geshi 'shell' %}
$ MY_APPLICATION_DATABASE_USERNAME=olivei MY_APPLICATION_DATABASE_PASSWORD=7655432222a mvn clean spring-boot:run
{% endgeshi %}

This way your application will start with the new values.

Happy hacking!

**--EDIT--**

As pointed by Stéphane Nicoll (thanks!), you could change the property values
without having to use the upper case syntax.

{% geshi 'shell' %}
mvn -Dmy.application.database.username=anotheruser clean spring-boot:run
{% endgeshi %}

And he even included a link to [docs](http://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#boot-features-external-config)! ♥ the Internet and Open Source!

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr"><a href="https://twitter.com/kinow">@kinow</a> you can also specify them as command-line arguments (no need for the upper case thing)<a href="https://t.co/zBKpgcXN1C">https://t.co/zBKpgcXN1C</a><br><br>or `-Drun.arguments`</p>&mdash; Stéphane Nicoll (@snicoll) <a href="https://twitter.com/snicoll/status/800965565120708608">November 22, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
