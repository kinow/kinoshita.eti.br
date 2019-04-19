---
title: "Finding Base64 implementations in Apache Software Foundation projects"
author: kinow
tags: 
    - java
    - programming
    - opensource
    - apache software foundation
time: '20:23:03'
format: markdown
---

<p style='text-align: center;'>
<a href="https://kinow.deviantart.com/art/Grey-Warbler-702099183?ga_submit_new=10%3A1504263729">
<img style="display: inline" class="ui image" src="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/GreyWarbler.png" alt="NZ Grey Warbler (riroriro)" title="NZ Grey Warbler (riroriro)" />
</a>
<br/>
<small><a href="http://nzbirdsonline.org.nz/species/grey-warbler">New Zealand Grey Warbler (riroriro)</a></small>
</p>

Some time ago while working in one of the many projects in the Apache Software Foundation (Apache Commons FileUpload if I remember well), I noticed that it had a Base64 implementation. What called my attention was that the project not using the [Apache Commons Codec](https://github.com/apache/commons-codec/blob/c18b1923b3c1f897c7935d94fb9e443eabfff897/src/main/java/org/apache/commons/codec/binary/Base64.java) Base64 implementation.

While Apache Commons' mission is to create components that can be re-used across ASF projects, and also by other projects not necessarily under the ASF, it is understandable that some projects prefer to keep its dependencies to a minimum. It is normally a good software engineering practice to carefully manage your dependencies.

But would Apache Commons FileUpload be the only project in the ASF with its own Base64 implementation?

### What is Base64?

Simply put, Base64 is a way to encode bytes to strings. It utilises a table, to convert parts of the binary input to certain numbers. These numbers match an entry in the table used by the Base64 implementation. There are several Base64 implementations, though some are obsolete now.

The input text &ldquo;*this is base64!*&rdquo; results in &ldquo;*dGhpcyBpcyBiYXNlNjQh*&rdquo;. It can be decoded and will result in the same input text. An image can also be encoded. Or a ZIP file. This is helpful for data transfer and storage.

Apache Commons Codec is well known to provide a Bse64 implementation, and used in several projects, both Open Source and in the industry. Its implementation is based on the [RFC-2045](https://www.ietf.org/rfc/rfc2045.txt).

Java 8 contains a Base64 implementation, so that may very well replace Apache Commons Coded use in some projects, though that may take some time. The Java 8 implementation supports the RFC-2045, RFC-4648, and [has also](https://docs.oracle.com/javase/8/docs/api/java/util/Base64.html) support to the URL and MIME formats.

### Searching for other Base64 implementations

Using GitHub search, I looked for other Base64 implementations in the ASF projects. Here's the result table with only the custom implementations found after going through some 15 pages in more than 100 pages with hits for &ldquo;base64&rdquo;.

| Project &amp; link to implementation        | JVM           | Base64 implementation |
| ------------- |:-------------:| -----:|
| [Apache ActiveMQ Artemis](https://github.com/apache/activemq-artemis/blob/master/artemis-commons/src/main/java/org/apache/activemq/artemis/utils/Base64.java) | 8 | RFC-3548, based on http://iharder.net/base64 |
| [Apache AsterixDB Hyracks (Incubator)](https://github.com/apache/incubator-asterixdb-hyracks/blob/3f849969f01effc9b6e7f22462ceb4b2bedabdc4/hyracks/hyracks-util/src/main/java/org/apache/hyracks/util/bytes/Base64Parser.java) | 8 | ? |
| [Apache Calcite Avatica](https://github.com/apache/calcite-avatica/blob/4db1fb9c66db8ccebc9e96ce678154ec69c557f0/core/src/main/java/org/apache/calcite/avatica/util/Base64.java) | 7 | RFC-3548, based on http://iharder.net/base64 |
| [Apache Cayenne](https://github.com/apache/cayenne/blob/bd1b109a943307a83078399c7a4d6aa53631a065/cayenne-server/src/main/java/org/apache/cayenne/util/Base64Codec.java) | 8 | RFC-2045 (based on codec)|
| [Apache Chemistry](https://github.com/apache/chemistry-opencmis/blob/trunk/chemistry-opencmis-commons/chemistry-opencmis-commons-impl/src/main/java/org/apache/chemistry/opencmis/commons/impl/Base64.java) | 7 | RFC-3548, based on http://iharder.net/base64 |
| [Apache Commons FileUpload](https://github.com/apache/commons-fileupload/blob/422caf46e5b7a950c639b8ba9fe41e16279b3aa9/src/main/java/org/apache/commons/fileupload/util/mime/Base64Decoder.java) | 6 | ? |
| [Apache Commons Net](https://github.com/apache/commons-net/blob/trunk/src/main/java/org/apache/commons/net/util/Base64.java) | 6 | RFC-2045 (copy of codec?) |
| [Apache Directory Kerby](https://github.com/apache/directory-kerby/blob/b7da10e3815a8ab84ab7ff4fa3572c92bfa9aef5/kerby-common/kerby-util/src/main/java/org/apache/kerby/util/Base64.java) | 7 | RFC-2045 (copy of codec?) |
| [Apache Felix](https://github.com/apache/felix/blob/a4755e768329a29252b1d7d8e52537941768606d/webconsole-plugins/upnp/src/main/java/org/apache/felix/webconsole/plugins/upnp/internal/Base64.java) | 5 (?) | RFC-2045 (copy of codec?) |
| [Apache HBase](https://github.com/apache/hbase/blob/a66d491892514fd4a188d6ca87d6260d8ae46184/hbase-common/src/main/java/org/apache/hadoop/hbase/util/Base64.java) | 8 | RFC-3548, based on http://iharder.net/base64 |
| [Apache Jackrabbit](https://github.com/apache/jackrabbit/blob/adb1e79ae26aba5d068be56e5e9eb562344e5bb9/jackrabbit-jcr-commons/src/main/java/org/apache/jackrabbit/util/Base64.java) | 8 (?) | ? |
| [Apache James](https://github.com/apache/james-project/blob/bab5ff434c407b98432cdc9af00b0263184de26a/server/protocols/protocols-smtp/src/test/java/org/apache/james/smtpserver/Base64.java) | 6 | RFC-2045 via javax.mail.internet.MimeUtility |
| [Apache James Mime4J](https://github.com/apache/james-mime4j/blob/cb48082fb7cbbfb111c926cc8ae953d7261c235c/core/src/main/java/org/apache/james/mime4j/codec/Base64OutputStream.java) | 5 | RFC-2045 (based on codec) |
| [Apache OFBiz](https://github.com/apache/ofbiz-framework/blob/29b815f1b969653da96995fed25e2cc52f25879d/framework/base/src/main/java/org/apache/ofbiz/base/util/Base64.java) | 8 | RFC-2045 |
| [Apache Pivot](https://github.com/apache/pivot/blob/d9a21718f182d3c667b18b0f2c62f6ec1cd0e6dd/core/src/org/apache/pivot/util/Base64.java) | 6 | RFC-2045 |
| [Apache Qpid](https://github.com/apache/qpid-broker-j/blob/1c20cc32b17c58391b0aefcd00f74bc1b4253db9/broker-core/src/main/java/org/apache/qpid/server/util/Strings.java#L132) | 8 | ? uses javax.xml.bind.DatatypeConverter#parseBase64Binary() |
| [Apache Shiro](https://github.com/apache/shiro/blob/8acc82ab4775b3af546e3bbde928f299be62dc23/lang/src/main/java/org/apache/shiro/codec/Base64.java) | 6 | RFC-2045 (based on commons) |
| [Apache Tomcat](https://github.com/apache/tomcat/blob/trunk/java/org/apache/tomcat/util/codec/binary/Base64.java) | 8 | RFC-2045 (copy of codec?) |
| [Apache TomEE](https://github.com/apache/tomee/blob/8fc8d8011c5155e7f47ebc162cb88124bf4ca06e/container/openejb-core/src/main/java/org/apache/openejb/util/Base64.java) | 7 | RFC-2045 |
| [Apache TomEE (Site-NG)](https://github.com/apache/tomee-site-ng/blob/8dbf7c5a4bdc6cd5249e00ff85d78a24fd76c7af/container/openejb-core/src/main/java/org/apache/openejb/util/Base64.java) | 6 | RFC-2045 |
| [Apache Trafodion (Incubator)](https://github.com/apache/incubator-trafodion/blob/b36003cf824bae6b0faf8b03c313f189991d5be1/core/rest/src/main/java/org/trafodion/rest/util/Base64.java) | 7 | RFC-3548, based on http://iharder.net/base64 |
| [Apache Wave (Incubator)](https://github.com/apache/incubator-wave/blob/master/wave/src/main/java/org/waveprotocol/wave/model/util/CharBase64.java) | 7 | RFC-3548 (?), based on http://iharder.net/base64 |

### Notes and conclusions

* **Projects using Java 8 can likely remove its own implementation in favour of the new JVM 8 implementation**.
* Some projects were already using [Java 8 Base64 implementation](https://docs.oracle.com/javase/8/docs/api/java/util/Base64.Decoder.html).
* Some projects were using Apache Commons Codec.
* Some projects were using the Base64 implementation from http://iharder.net/base64, which claims to be very fast. It could be interesting to further investigate it. Perhaps projects where Base64 is used a lot, there could be a significant performance increase by using this version.
* Even though most of these projects are not using Apache Commons Codec, some have either copied or based their implementations on Apache Commons Codec. Perhaps shading would be more effective? Or maybe adding it as a dependency&hellip;
* I guess the Base64 implementations could be hidden from external users with /\*protected\*/, private scope. As they are probably not part of Apache Commons Net, or Apache Cayenne public API. Which will be solved eventually after Java 9&hellip;
* Some implementations do not make it clear which RFC or standard they are following. Some derived the reference work (e.g. Apache Wave (Incubator) modified the iharder removing features&hellip;).
* It could be that some of these projects that contain many dependencies like Cayenne and Pivot may even have Commons Codec in the class path as a transitive dependency. If so, it could be interesting to add it as a dependency and remove its own implementation, or simply use Java 8's.
* Some implementations like HBase and Trafodion were not using the latest version from http://iharder.net/base64. In the case of HBase and Trafodion, several invalid inputs have been fixed from 2.2.1 to 2.3.7.

### Future work

* I will try to investigate which of these projects that have a custom Base64 implementation and are using Java 8 can be updated to throw away its own version (時間があるときでしょう!).
* The implementation from [http://iharder.net/base64](http://iharder.net/base64) promises to be very fast, and Apache ActiveMQ Artemis adopted it. We could consider adding a similar *fast* version to Apache Commons Codec. This could be a reason for keeping its own Base64 implementation.
* Java 8 Base64 provides Base64, MIME, and URL formats for encode and decoding. Perhaps we could add more formats to Apache Commons Codec too. Even [custom formats](https://github.com/apache/commons-codec/pull/3). This could be a reason for keeping Apache Commons Codec's implementation.

Happy encoding!

&hearts; Open Source
