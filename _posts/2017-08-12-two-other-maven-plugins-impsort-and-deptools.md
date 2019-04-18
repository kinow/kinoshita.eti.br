---
title: "Two other Maven Plug-ins: impsort and deptools"
author: kinow
tags: 
    - java
    - programming
    - opensource
    - maven
time: '22:16:03'
---

Last [week I wrote]({{pcurl('2017/08/06/checking-for-transitive-dependencies-use-with-maven-enforcer-plugin')}}) about the [ImmobilienScout24/illegal-transitive-dependency-check](https://github.com/ImmobilienScout24/illegal-transitive-dependency-check) rule for Maven Enforcer Plug-in. There are two other Maven Plug-ins that can be useful.

### mbknor/deptools

The [mbknor/deptools](https://github.com/mbknor/deptools) is another rule for the Maven Enforcer Plug-in. It will scan your project dependency tree, looking for transitive dependencies. Whenever it finds a transitive dependency, it will keep track of the versions. And if, because of the way your dependencies and transitive dependencies are organised, you end up with a version that is not the newest, the build will fail.

So, for example, if you have `commons-lang3` as transitive dependency of two other dependencies, but one is using 3.4 and the other 3.5. If for any reason you are using 3.4 instead of 3.5, you will have a build error.

Here's an example of the plug-in configuration.

```xml
<project>
  ...
  <build>
    <plugins>
      <plugin>
        <groupId>deptools.plugin</groupId>
        <artifactId>maven-deptools-plugin</artifactId>
        <version>1.3</version>
          <executions>
              <execution>
                  <phase>compile</phase>
                  <goals>
                      <goal>version-checker</goal>
                  </goals>
              </execution>
          </executions>
        </plugin>
    </plugins>
  </build>

  <pluginRepositories>
    <pluginRepository>
      <id>mbk_mvn_repo</id>
      <name>mbk_mvn_repo</name>
      <url>https://raw.githubusercontent.com/mbknor/mbknor.github.com/master/m2repo/releases</url>
    </pluginRepository>
  </pluginRepositories>
  ...
</project>
```

Running `mvn clean verify` will execute the Maven Enforcer Plug-in `enforce` goal, which will call the deptools check. As you may have noticed, you also need to download the plug-in from GitHub, as it is not released to Maven Central.

I do not use it for this reason, and also because I normally spend some time looking at the dependency tree anyway, but every now and then when I work on a new project I like quickly running it just to see what are the dependencies that are being shadowed by older versions.

### revelc/impsort-maven-plugin

I only found about this plug-in in the last [Apache News Round-up](https://blogs.apache.org/foundation/entry/the-apache-news-round-up31). Where it was mentioned that [Apache Accumulo uses](https://github.com/apache/accumulo/blob/401411619239e301ad14216b3b9c88ee947ab072/pom.xml#L999) this plug-in to standarize the order of imports in code.

```xml
<project>
  ...
  <build>
    <plugins>
      <plugin>
        <groupId>net.revelc.code</groupId>
        <artifactId>impsort-maven-plugin</artifactId>
        <version>1.0.0</version>
        <configuration>
          <groups>java.,javax.,org.,com.</groups>
          <staticGroups>java,*</staticGroups>
          <excludes>
            <exclude>**/thrift/*.java</exclude>
          </excludes>
        </configuration>
        <executions>
          <execution>
            <id>sort-imports</id>
            <goals>
              <goal>sort</goal><!-- runs at process-sources phase by default -->
            </goals>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
  ...
</project>
```

I am neutral on imports order, though in cases where you have several contributors submitting pull requests, it can probably be useful to reduce the number of interactions. In other words, if a user submits a pull request and you have an automated check, then the user would be automatically notified about changes that s/he needs to do in order for his pull request to be accepted.

### Conclusion

I am not using any of these two plug-ins, but wanted to save it somewhere in case I needed to use them in the future, and also to share with others. Besides most common plug-ins (PMD, CheckStyle, FindBugs), I normally use at least some Maven Enforcer Plug-in rules, and the [OWASP plug-in](https://www.owasp.org/index.php/OWASP_Dependency_Check).

While most of the time we spend writing code, preparing the infrastructure, and deploying and testing, I got bitten by some maven build bugs a few times, and had to spend days/weeks debugging some of these. So hope some of these posts save some hours of someone out there in a similar situation.

&hearts; Open Source
