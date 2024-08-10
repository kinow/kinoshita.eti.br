---
title: "Using Docker to run Cypress with Maven"
date: 2024-08-11T00:02:52+03:00
categories:
  - programming
tags:
  - containers
  - opensource
  - programming
images:
  - '/assets/posts/2024-04-28-logo-java-ring/dev-multitask-100-videos-1.png'
---

Apache Jena runs Cypress tests from Maven, which makes running everything
containerized a bit more difficult. To make it more complicated, we also
used `wait-on` and `concurrently` to orchestrate how the tests and API
test process are launched.

The solution found was to combine the [official Maven docker image](https://hub.docker.com/_/maven),
with the [`cypress/included` image](https://hub.docker.com/r/cypress/included),
in a multi-stage build.

<div class="popout">

```dockerfile
# A multi-stage image with Cypress and Java+Maven for Jena... ALv2...
# To build it:
# `docker build -t jena/build:latest .`
#
# To run it:
# `docker run --entrypoint "" --rm -ti jena/build:latest /bin/bash`

FROM maven:3.9.8-eclipse-temurin-21-jammy AS maven

# The Maven stage. Nothing to see here, we simply copy artefacts
# from this stage onto the next one.
# Docs: https://hub.docker.com/_/maven

FROM cypress/included:13.13.1

# The image with Cypress and everything else included. Compatible
# with temurin jammy, so we can just copy Maven and Java, and set
# the $PATH.
# Docs: https://hub.docker.com/r/cypress/included
#
# NOTE: The Cypress image must match our Cypress version in package.json.
#       This is due to how Cypress loads the binary from the cache. It'll
#       expect a binary at `/root/.cache/Cypress/$version/Cypress/`. With
#       the `$version` coming from the version from the package.json file.

COPY --from=maven /usr/share/maven/ /usr/share/maven/ 
COPY --from=maven /opt/java/ /opt/java

ENV PATH="/usr/share/maven/bin:/opt/java/openjdk/bin:$PATH"

ENTRYPOINT [""]
CMD ["mvn"]
```

</div>

Using the image created with the `Dockerfile` above, one can test Jena
Fuseki UI with containers with:

<div class="popout">

```bash
docker run \
  --sysctl net.ipv6.conf.all.disable_ipv6=1 \
  --rm -ti --name jena-build \
  -v "/home/kinow/Development/java/workspace/jena":/usr/src/mymaven \
  -w /usr/src/mymaven \
  jena/build:latest \
  mvn clean test install --projects jena-fuseki2/jena-fuseki-ui
```

</div>

Without the option to disable IPV6 `wait-on` got stuck even after the endpoint
was ready and available.

Based on [this gist](https://gist.github.com/kinow/c227a7f0ea1c509a36f57beb02e9d8e3).
