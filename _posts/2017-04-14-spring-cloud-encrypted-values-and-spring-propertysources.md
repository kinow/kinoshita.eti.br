---
date: 2017-04-14 11:21:03 +1300
layout: post
tags:
- java
- programming
- opensource
categories:
- blog
title: Spring Cloud encrypted values and Spring PropertySources
---

As I could not find any documentation for that, I decided to write it as a note to myself
in case I use the
[encryption and decryption](https://cloud.spring.io/spring-cloud-config/spring-cloud-config.html#_encryption_and_decryption)
with Spring Cloud again.

In Spring and Spring Boot, you normally have multiple sources of properties, like multiple
properties files, environment properties and variables, and so it goes. In the Spring API,
these are represented as
[PropertySource](http://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/context/annotation/PropertySource.html)'s.

In a Spring Boot application, you would be used to overriding certain properties
by defining environments and using an application-production.properties file, or
overriding values with environment properties.

This is common in
[Spring Boot applications deployed to Amazon Elastic Beanstalk](https://aws.amazon.com/blogs/devops/deploying-a-spring-boot-application-on-aws-using-aws-elastic-beanstalk/).

Some time ago another team at work found that overriding did not always work when you have
encrypted values in your properties files. Even if you specified new values in the
Amazon Elastic Beanstalk application configuration.

Yesterday, while debugging the issue and reading Spring Cloud source code, I found its
[EnvironmentDecryptApplicationInitializer](https://github.com/spring-cloud/spring-cloud-commons/blob/9675df02f6a2c01766711f7dee3c4d2818b7d716/spring-cloud-context/src/main/java/org/springframework/cloud/bootstrap/encrypt/EnvironmentDecryptApplicationInitializer.java#L44).

It basically iterates through all loaded property sources, looking for values that start with
{cipher}. Then it calls the
[Spring Security TextEncryptor](http://docs.spring.io/spring-security/site/docs/current/apidocs/org/springframework/security/crypto/encrypt/TextEncryptor.html)
defined in the application.

Finally, it creates a new property source, called decrypted, with the decrypted values. So when
your application looks for a property called XPTO, and if it has been encrypted, it will
find the value in the decrypted propery source, regardless of whether you tried to override it or
not.

```shell
# Property sources listed in Eclipse IDE

[
  servletConfigInitParams,
  servletContextInitParams,
  systemProperties,
  systemEnvironment,
  random,
  applicationConfigurationProperties,
  springCloudClientHostInfo,
  defaultProperties
]

# When using encrypted values

[
  decrypted, <-------- created by Spring Cloud, with decrypted values. Prepended to the list of property sources
  servletConfigInitParams,
  servletContextInitParams,
  systemProperties,
  systemEnvironment,
  random,
  applicationConfigurationProperties,
  springCloudClientHostInfo,
  defaultProperties
]
```

So in case you have encrypted values in your Spring application (and you are using Spring Cloud, 
of course) remember that these values will have higher priority, and can only be overriden by other
encrypted values.

&hearts; Open Source
