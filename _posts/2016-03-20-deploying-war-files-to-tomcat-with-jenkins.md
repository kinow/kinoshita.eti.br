---
title: 'Deploying WAR files to Tomcat with Jenkins'
author: kinow
tags:
    - jenkins
    - tomcat
    - docker
category: 'blog'
time: '15:29:03'
---

**Table of Contents**

* [Deploying with custom scripts](#1-deploying-with-custom-scripts)
* [Deploying with a build tool](#2-deploying-with-a-build-tool)
* [Deploying with a build server](#3-deploying-with-a-build-server)
* [Final thoughts](#final-thoughts)

A co-worker asked me this week about how to deploy a WAR file to Tomcat with Jenkins. In my team we are
currently maintaining and deploying about 10 Java web systems, but we have no consistent way of deploying
the applications to Tomcat yet. In the past I used Ant, Maven, Cargo, Grunt, and Jenkins, so I
decided to write this short post to show a few different ways it can be achieved, &agrave; la
[Perl's TMTOWTDI](https://en.wikipedia.org/wiki/There's_more_than_one_way_to_do_it) motto.

<h2><a name="1-deploying-with-custom-scripts" style="color: #222222;">#1 Deploying with custom scripts</a></h2>

At first you may be tempted to write your own script to deploy to Tomcat with some Shell, Perl, Python
or Java. But I think I would choose this option only because either I needed some feature that is not
available in the other options, or in order to call other tasks or debug some problem.

Example:

{% geshi 'bash' %}
$ docker run -d -p 8888:8080 jeanblanchard/tomcat:8
$ git clone https://github.com/spring-projects/spring-petclinic.git && cd spring-petclinic && mvn package
$ curl --upload-file target/petclinic.war "http://admin:admin@localhost:8888/manager/text/deploy?path=/spring-petclinic&update=true"
OK - Deployed application at context path /spring-petclinic
{% endgeshi %}

<!-- more -->

### Pros

* Flexible option. You can customise the deployment and even call other tasks before, after or during the
deployment
* Easy to get it working, as you have few dependencies and no learning curve for learning about any tool

### Cons

* Susceptible to bugs ([DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself))
* You will have to spend time maintaining your scripts if Tomcat changes (e.g. from Tomcat 6 to 7,
the deploy URL changed adding a '/text' token)
* Integration with other tools, such as a build tool or build server may not be simple

<h2><a name="2-deploying-with-a-build-tool" style="color: #222222;">#2 Deploying with a build tool</a></h2>

For this example I will use Apache Maven, but you can achieve the same with Grunt, Ant, Gradle,
or Make. Each of these tools provide different mechanisms to call external tools, some providing
plug-ins that can be used to deploy a WAR file to Tomcat, like Maven and the
[Cargo plug-in](https://codehaus-cargo.github.io/cargo/Maven2+Plugin+Getting+Started.html).

But even with Maven you have a few options. For example.

* You can use Cargo Maven Plug-in. This plug-in contains several options and lets you abstract how
you interface with Tomcat 
* You can use Maven Exec Plug-in and call some command or script that deploys your application to
Tomcat. This script can use Tomcat web services to deploy the application, or execute commands remotely
via SSH in the server, copying the file and stop/starting the services
* You can even write your own plug-in, where it wouldn't be much different than option #1

Example:

{% geshi 'bash' %}
$ git clone https://github.com/spring-projects/spring-petclinic.git && cd spring-petclinic
{% endgeshi %}

Add the following to the pom.xml file, under the right XML tags, of course.

{% geshi 'xml' %}
<!-- from https://gist.github.com/mdread/5900034 -->
<plugins>
    <plugin>
        <groupId>org.codehaus.cargo</groupId>
        <artifactId>cargo-maven2-plugin</artifactId>
        <configuration>
            <container>
                <containerId>tomcat7x</containerId>
                <type>remote</type>
            </container>
            <configuration>
                <type>runtime</type>
                <properties>
                    <cargo.hostname>${cargo.hostname}</cargo.hostname>
                    <cargo.servlet.port>${cargo.servlet.port}</cargo.servlet.port>
                    <cargo.tomcat.manager.url>${cargo.tomcat.manager.url}</cargo.tomcat.manager.url>
                    <cargo.remote.username>${cargo.remote.username}</cargo.remote.username>
                    <cargo.remote.password>${cargo.remote.password}</cargo.remote.password>
                </properties>
            </configuration>
            <deployer>
                <type>remote</type>
            </deployer>
            <deployables>
                <deployable>
                    <groupId>${project.groupId}</groupId>
                    <artifactId>${project.artifactId}</artifactId>
                    <type>${project.packaging}</type>
                </deployable>
            </deployables>

        </configuration>
    </plugin>
</plugins>

<profiles>
    <profile>
        <id>prod</id>
        <properties>
            <deploy.env>prod</deploy.env>
            <cargo.hostname>srvprd001</cargo.hostname>
            <cargo.servlet.port>8080</cargo.servlet.port>
            <cargo.tomcat.manager.url>http://srvprd001:8080/manager</cargo.tomcat.manager.url>
            <cargo.remote.username>user</cargo.remote.username>
            <cargo.remote.password>pass</cargo.remote.password>
        </properties>
    </profile>
    <profile>
        <id>test</id>
        <properties>
            <deploy.env>dev</deploy.env>
            <cargo.hostname>srvtst001</cargo.hostname>
            <cargo.servlet.port>9090</cargo.servlet.port>
            <cargo.tomcat.manager.url>http://srvtst001:9090/manager</cargo.tomcat.manager.url>
            <cargo.remote.username>user</cargo.remote.username>
            <cargo.remote.password>pass</cargo.remote.password>
        </properties>
    </profile>
</profiles>
{% endgeshi %}

And finally start Tomcat and call the Cargo Maven plug-in.

{% geshi 'bash' %}
$ docker run -d -p 8888:8080 jeanblanchard/tomcat:8
$ mvn package org.codehaus.cargo:cargo-maven2-plugin:deploy -Ptest -Dcargo.hostname=localhost -Dcargo.servlet.port=8888 -Dcargo.tomcat.manager.url=http://localhost:8888/manager/text -Dcargo.remote.username=admin -Dcargo.remote.password=admin
{% endgeshi %}

What I like about this approach is that using profiles and environments with Maven, you can have pre-defined
variables per profile, but also overwrite them when necessary. For example in the previous command line,
the host, port, user and password are overwritten to match the default values from the Docker image used.

### Pros

* You are using a tool that is being used by other people. So bugs are fixed much faster and by
a lot of people, with different environments and use cases
* Normally, build tools provide some mechanism for you to parameterise your build, controlling flags
and allowing a more flexible process
* It is a lot easier to find examples and workarounds online

### Cons

* New features depend on how well maintained your build tool or plug-in is. For example, with the Maven Cargo
Plug-in, it took some time till Java 7 was fully supported (but you can submit pull requests/patches)
* There is a learning curve for either learning about the build tool or about its plug-ins and extension
points
* Sometimes you may have to dig into the build tool or plug-in source code to debug problems in your build,
such as JVM or some system library incompatibility

<h2><a name="3-deploying-with-a-build-server" style="color: #222222;">#3 Deploying with a build server</a></h2>

Deploying with a build server is not very different from approach #2. For this example I will use Jenkins,
as this is the build server I am most familiar with, and also the one that I am using at work.

Example:

Install the [Deploy Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Deploy+Plugin) in
Jenkins (it appears as "Deploy to container Plugin" in the plug-in selection screen), as well as the
git plug-in to check out the project.

In your job configuration, add a SCM step to clone the petclinic war project, and another step
to invoke a Maven top level target execute `mvn package`. Also add a post build step to deploy with the following
settings.

* WAR/EAR files: target/*.war
* Context-path: spring-petclinic
* Containers: add Tomcat 7.x
* * Manager user name: admin
* * Manager password: admin
* * Tomcat URL: http://localhost:8888

Instead of a screenshot, here is the config.xml file for my example job - easier to diff your job
configuration.

{% geshi 'xml' %}
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@2.4.3">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>https://github.com/spring-projects/spring-petclinic.git</url>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/master</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Maven>
      <targets>clean package</targets>
      <mavenName>3.3.9</mavenName>
      <usePrivateRepository>false</usePrivateRepository>
      <settings class="jenkins.mvn.DefaultSettingsProvider"/>
      <globalSettings class="jenkins.mvn.DefaultGlobalSettingsProvider"/>
    </hudson.tasks.Maven>
  </builders>
  <publishers>
    <hudson.plugins.deploy.DeployPublisher plugin="deploy@1.10">
      <adapters>
        <hudson.plugins.deploy.tomcat.Tomcat7xAdapter>
          <userName>admin</userName>
          <passwordScrambled>YWRtaW4=</passwordScrambled>
          <url>http://localhost:8888</url>
        </hudson.plugins.deploy.tomcat.Tomcat7xAdapter>
      </adapters>
      <contextPath>spring-petclinic</contextPath>
      <war>target/*.war</war>
      <onFailure>false</onFailure>
    </hudson.plugins.deploy.DeployPublisher>
  </publishers>
  <buildWrappers/>
</project>
{% endgeshi %}

When running this job, you should see in the end of the console output, something similar to this.

{% geshi 'bash' %}
[INFO] Building war: /tmp/1/jobs/deploy01/workspace/target/petclinic.war
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 20.590 s
[INFO] Finished at: 2016-03-20T19:13:51+13:00
[INFO] Final Memory: 36M/359M
[INFO] ------------------------------------------------------------------------
Deploying /tmp/1/jobs/deploy01/workspace/target/petclinic.war to container Tomcat 7.x Remote
  [/tmp/1/jobs/deploy01/workspace/target/petclinic.war] is not deployed. Doing a fresh deployment.
  Deploying [/tmp/1/jobs/deploy01/workspace/target/petclinic.war]
Finished: SUCCESS
{% endgeshi %}

You can chain several jobs, creating a pipeline with one job to build, one for functional tests, and
another job to deploy.

### Pros

* Since you are using Jenkins you can also chain other tools together, as well as other jobs, creating a build
pipeline (doable with the other two approaches, but just harder IMO)
* Like in option #2, you can use parameters and customise the behaviour of the tools used
* You can use Jenkins remote API or CLI to chain other tools or react to events in other systems
(harder to achieve with the other approaches)

### Cons

* There is a learning curve for learning Jenkins, as well as any plug-in or other tools that you may be using
* You have to maintain a new infrastructure with Jenkins
* When new versions of containers are released, Jenkins developers, and plug-in developers may have to update and
release an updated plug-in to be able to support these versions. You have to wait till that happens to use
the plug-in (or submit a patch/pull request)

<h2><a name="final-thoughts" style="color: #222222;">Final thoughts</a></h2>

Whenever I can, I try to avoid reinventing the wheel. The less code I write, and the more good quality
code that I reuse, the merrier for me. So approach #1 is my less favorite way of deploying WAR files to
Tomcat.

**My preferred approach for deploying WAR files to Tomcat, is a mix of #2 and #3**.

You configure the deploy tasks in your build tool, be it Maven, Grunt, Ant, or etc. And configure a job
in Jenkins to check out the code and deploy it, calling your build tool. 

Using the previous examples, you would configure profiles in your pom.xml, and also combine parameters
in Jenkins to define which profile to activate (as well as override parameters if necessary).

This way you give developers the power to choose how/where to deploy. In case they need to deploy to a
different environment, they can change the build scripts, commit, and wait for Jenkins to be ready to
deploy. Leaving the deployment environment configuration in Jenkins jobs would require developers to
request changes in jobs, which would slow down the development pipeline.

Furthermore, you can also overwrite values in the build tools, so you can still control it in the build
server too. And you are getting the best of both worlds, having Jenkins parameters, over 1000 plug-ins,
and being able to create a build workflow/pipeline.

But remember, that is my opinion. I hope you can assimilate everything you have read here, and choose
what will work best in your case.

Happy hacking!
