---
title: "Loading JavaScript in Jenkins Active Choices parameters"
date: 2025-08-02T21:59:52+03:00
categories:
  - blog
tags:
  - opensource
  - java
  - programming
  - security
images:
  - '/assets/posts/2025-08-02-loading-javascript-in-jenkins-active-choice-parameters/no-security-result.png'
---

**Be aware that what's described here may introduce a security risk to your
environment, and you must only do it if you really know what you are doing.
You will be breaking a few security fixes of Jenkins, such as**:

- SECURITY-440 https://github.com/jenkinsci/active-choices-plugin/commit/720af532b0a2c69465824af5735be2859d7c3492
- Jenkins XSS prevention https://wiki.jenkins-ci.org/JENKINS/Jelly-and-XSS-prevention.html

Some years ago, the Jenkins Active Choices plug-in had a security bug
reported as a Groovy script could have malicious code that would trigger
an XSS attack in Jenkins (i.e. run some arbitrary JS code in Jenkins).
The plug-in got removed from the update site until we fixed it, and the
solution was to sanitize the output of the Groovy script used to render
the Jenkins parameters.

That broke a feature of the plug-in, where users could load third-party
JavaScript files, like jQuery, D3.js, [CSS Doodle](https://css-doodle.com/),
etc. This post shows how one could create a version of the plug-in that
renders Jenkins parameters that load and execute any JavaScript code provided.

I tested it using [a commit](https://github.com/jenkinsci/active-choices-plugin/commit/daa5837519e23377431335613661b057fe102275)
from the `master` branch of the plug-in:

```bash {linenos=inline hl_lines=[9] style=emacs}
commit daa5837519e23377431335613661b057fe102275 (HEAD -> master, upstream/master, upstream/HEAD)
Author: Bruno P. Kinoshita <kinow@users.noreply.github.com>
Date:   Thu Jul 31 20:38:20 2025 +0200

    Update CHANGES.md
```

You will have to clone the repository of the plug-in,
<https://github.com/jenkinsci/active-choices-plugin>,
and then you can start by disabling escaping text in Jelly:

```bash {linenos=inline hl_lines=[9] style=emacs}
$ find src/main/ -name "*.jelly" | xargs \
  sed -i -E "s/escape-by-default='true'/escape-by-default='false'/g"
```

There's one more change in `DynamicReferenceParameter/formattedHtml.jelly`
that you will have to apply:

```diff {linenos=inline hl_lines=[9] style=emacs}
diff --git a/src/main/resources/org/biouno/unochoice/DynamicReferenceParameter/formattedHtml.jelly b/src/main/resources/org/biouno/unochoice/DynamicReferenceParameter/formattedHtml.jelly
index a853766..c047cf1 100644
--- a/src/main/resources/org/biouno/unochoice/DynamicReferenceParameter/formattedHtml.jelly
+++ b/src/main/resources/org/biouno/unochoice/DynamicReferenceParameter/formattedHtml.jelly
@@ -1,4 +1,4 @@
-<?jelly escape-by-default='true' ?>
+<?jelly escape-by-default='false' ?>
 <j:jelly xmlns:j="jelly:core">
   <j:invokeStatic var="paramName" className="org.biouno.unochoice.util.Utils" method="createRandomParameterName">
     <j:arg type="java.lang.String" value="choice-parameter" />
@@ -6,6 +6,6 @@
   </j:invokeStatic>
   <j:set var="paramName" value="${paramName}" scope="parent" />
   <div id='formattedHtml_${paramName}'>
-    <j:out value="${it.getChoicesAsString()}"/>
+    ${h.rawHtml(it.getChoicesAsString())}
   </div>
-</j:jelly>
\ No newline at end of file
```

You will also need to disable escaping and sanitizing in the
Java code:

```diff {linenos=inline hl_lines=[9] style=emacs}
diff --git a/src/main/java/org/biouno/unochoice/AbstractCascadableParameter.java b/src/main/java/org/biouno/unochoice/AbstractCascadableParameter.java
index 9494779..b46f126 100644
--- a/src/main/java/org/biouno/unochoice/AbstractCascadableParameter.java
+++ b/src/main/java/org/biouno/unochoice/AbstractCascadableParameter.java
@@ -164,7 +164,7 @@ public abstract class AbstractCascadableParameter extends AbstractScriptablePara
             for (String value : array) {
                 value = value.trim();
                 if (StringUtils.isNotBlank(value)) {
-                    list.add(Util.escape(value));
+                    list.add(value);
                 }
             }
             return list.toArray(new String[0]);
diff --git a/src/main/java/org/biouno/unochoice/AbstractScriptableParameter.java b/src/main/java/org/biouno/unochoice/AbstractScriptableParameter.java
index 102f694..6444239 100644
--- a/src/main/java/org/biouno/unochoice/AbstractScriptableParameter.java
+++ b/src/main/java/org/biouno/unochoice/AbstractScriptableParameter.java
@@ -306,7 +306,7 @@ public abstract class AbstractScriptableParameter extends AbstractUnoChoiceParam
             String valueText = ObjectUtils.toString(entry.getValue(), "");
             if (Utils.isSelected(valueText)) {
                 String keyText = ObjectUtils.toString(entry.getKey(), "");
-                defaultValues.add(Utils.escapeSelectedAndDisabled(keyText));
+                defaultValues.add(keyText);
             }
         }
         if (defaultValues.isEmpty()) {
diff --git a/src/main/java/org/biouno/unochoice/model/GroovyScript.java b/src/main/java/org/biouno/unochoice/model/GroovyScript.java
index 385aafa..c78c0a9 100644
--- a/src/main/java/org/biouno/unochoice/model/GroovyScript.java
+++ b/src/main/java/org/biouno/unochoice/model/GroovyScript.java
@@ -188,9 +188,9 @@ public class GroovyScript extends AbstractScript {
         try {
             Object returnValue = secureScript.evaluate(cl, context, null);
             // sanitize the text if running script in sandbox mode
-            if (secureScript.isSandbox()) {
-                returnValue = resolveTypeAndSanitize(returnValue);
-            }
+//            if (secureScript.isSandbox()) {
+//                returnValue = resolveTypeAndSanitize(returnValue);
+//            }
             return returnValue;
         } catch (Exception re) {
             if (this.secureFallbackScript != null) {
@@ -198,9 +198,9 @@ public class GroovyScript extends AbstractScript {
                     LOGGER.log(Level.FINEST, "Fallback to default script...", re);
                     Object returnValue = secureFallbackScript.evaluate(cl, context, null);
                     // sanitize the text if running script in sandbox mode
-                    if (secureFallbackScript.isSandbox()) {
-                        returnValue = resolveTypeAndSanitize(returnValue);
-                    }
+//                    if (secureFallbackScript.isSandbox()) {
+//                        returnValue = resolveTypeAndSanitize(returnValue);
+//                    }
                     return returnValue;
                 } catch (Exception e2) {
                     LOGGER.log(Level.WARNING, "Error executing fallback script", e2);
```

Now, build the project, but skip the tests since we have at least
one security test that may fail with these changes.

```bash {linenos=inline hl_lines=[9] style=emacs}
$ mvn clean install -DskipTests
```

Your modified `.hpi` file should be ready to be installed in a Jenkins
server. Or you can run it locally.

```bash {linenos=inline hl_lines=[9] style=emacs}
$ find . -name uno-choice.hpi
./target/uno-choice.hpi
$ mvn hpi:run
```

Finally, create your project embedding JavaScript. For instance,
create a FreeStyle project with a DynamicReferenceParameter,
rendering as formatted HTML.

Here's a sample Groovy script that should render an image.

```bash {linenos=inline hl_lines=[9] style=emacs}
return """
<script type="module">
  import 'https://esm.sh/css-doodle'
</script>
<css-doodle>
  @grid: 18 / 100vmax / #0a0c27;
  --hue: calc(180 + 1.5 * @x * @y);
  background: hsl(var(--hue), 50%, 70%);
  margin: -.5px;
  transition: @r(.5s) ease;
  clip-path: polygon(@pick(
    '0 0, 100% 0, 100% 100%',
    '0 0, 100% 0, 0 100%',
    '0 0, 100% 100%, 0 100%',
    '100% 0, 100% 100%, 0 100%'
  ));
</css-doodle>
"""
```

{{< showimage
    image="no-security-configuration.png"
    alt="Job configuration"
    caption="Job configuration"
    style="width: auto;"
>}}

{{< showimage
    image="no-security-result.png"
    alt="Result showing a CSS Doodle"
    caption="Result showing a CSS Doodle"
    style="width: auto;"
>}}

Once again, this may lead to security issues if you allow users with
admin permissions over jobs, or if you pipelines that load external
Groovy code, and if these contain malicious code.

But if you have an internal server with code that is developed internally,
and meticulously reviewed, the risk might be mitigated in your case, and
you may want to be able to use JavaScript in your parameters -- like
we all used to be able to do before.

Someday, we may have a new permission in the plug-in, and a flag that
allow admins to enable this per-project. Maybe that, combined with the
Jenkins In-Process Script Approval might be enough for the plug-in to
work as before, without being marked as a risk by the Jenkins CERT/security
team.

(Also, as always, remember to back up and use a testbed server!)