---
title: "Checking for transitive dependencies use with Maven Enforcer Plug-in"
author: kinow
tags: 
    - java
    - programming
    - opensource
    - maven
time: '17:35:39'
---

[Maven Enforcer Plug-in](http://maven.apache.org/enforcer/maven-enforcer-plugin/) &ldquo;provides goals to control certain environmental constraints such as Maven version, JDK version and OS family along with many more built-in rules and user created rules&rdquo;. There are several libraries that provide custom rules, or you can write your own.

One of these libraries is [ImmobilienScout24/illegal-transitive-dependency-check](https://github.com/ImmobilienScout24/illegal-transitive-dependency-check), &ldquo;an additional rule for the maven-enforcer-plugin that checks for classes referenced via transitive Maven dependencies&rdquo;.

With the following example:

```xml
<project>
  ...
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-enforcer-plugin</artifactId>
        <version>1.3.1</version>
        <dependencies>
          <dependency>
            <groupId>de.is24.maven.enforcer.rules</groupId>
            <artifactId>illegal-transitive-dependency-check</artifactId>
            <version>1.7.4</version>
          </dependency>
        </dependencies>
        <executions>
          <execution>
            <id>enforce</id>
            <phase>verify</phase>
            <goals>
              <goal>enforce</goal>
            </goals>
            <configuration>
              <rules>
                <illegalTransitiveDependencyCheck implementation="de.is24.maven.enforcer.rules.IllegalTransitiveDependencyCheck">
                  <reportOnly>false</reportOnly>
                  <useClassesFromLastBuild>true</useClassesFromLastBuild>
                  <suppressTypesFromJavaRuntime>true</suppressTypesFromJavaRuntime>
                  <listMissingArtifacts>false</listMissingArtifacts>
                </illegalTransitiveDependencyCheck>
              </rules>
            </configuration>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
  ...
</project>
```

Running `mvn clean verify` will execute the Maven Enforcer Plug-in `enforce` goal, which will call the illegal transitive dependency check.

And the build will fail if your code is using (i.e. importing) any class that is not available in your first-level dependencies. For example, if in your pom.xml you added `commons-lang3` and `commons-configuration`, the latter which includes `commons-lang` **2.x**, and you used `org.apache.commons.lang.StringUtils` instead of `org.apache.commons.lang3.StringUtils`, the build would fail.

In order to fix the build, you have to either add the transitive dependency to your pom.xml file, or correct your import statements. This is specially useful to prevent future issues due to other dependencies being added or updated, and changing the version of the transitive dependency.

Bonus points if you combine that with continuous integration and some service like Travis-CI.

&hearts; Open Source
