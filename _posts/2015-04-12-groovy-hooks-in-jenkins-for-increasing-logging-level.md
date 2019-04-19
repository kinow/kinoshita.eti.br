---
date: 2015-04-12 11:30:03 +1300
layout: post
tags:
- jenkins
- groovy
title: Groovy Hooks in Jenkins for increasing logging level
---

Yesterday, while debugging a problem we had in the [BioUno](http://biouno.org) update center, 
I realized that after [increasing the logging level in the WEB interface](https://wiki.jenkins-ci.org/display/JENKINS/Logging), 
the messages that I needed weren't being displayed in the logs.

It happened because some of the logging happened during Jenkins initialization, and before I could adjust the log level.

The solution was to use a [Groovy Hook Script](https://wiki.jenkins-ci.org/display/JENKINS/Groovy+Hook+Script). 
If you are familiar with Linux init scripts, the idea is quite similar. 

A Groovy script in the `$JENKINS_ROOT_DIR/init.groovy.d/` directory is executed during
Jenkins initialization. This way you can increase the global logger level with a script
as the following below.

```java
import java.util.logging.ConsoleHandler
import java.util.logging.LogManager
import java.util.logging.Logger
import java.util.logging.Level

def logger = Logger.getLogger("")
logger.setLevel(Level.FINEST)
logger.addHandler (new ConsoleHandler())
```

Happy logging!
