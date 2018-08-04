---
title: Creating a Docker container to run as a command
time: '22:00:36'
author: kinow
tags:
    - cylc
    - docker
    - opensource
---

For the past two weeks at work I have been assigned to work on PHP projects. Though I used
PHP some time ago - especially with Code Igniter and Laravel - I have not used it in a few
years. And have been doing mostly Java nowadays.

The complete project setup was done by co-workers. I had a PHP project, using Symfony, several
bundles and libraries, and Postgres. But it required just running a few commands to set up
AWS settings, and then fire up Docker Compose.

Besides Docker Compose starting a web container, and another Postgres container, we used the
web container to run [Composer](https://getcomposer.org/). In the past, I would see the PHP
project mapped as a folder in the running container, and then composer would be executed
in the host.

I noticed then that I could do the same to an image I created in 2016 to run
[Cylc](https://cylc.github.io/cylc/). The [previous version](https://github.com/kinow/docker/blob/d1cc1771ac53b8efd37b5e4c4401b74ebd294a2b/cylc/Dockerfile)
would be used to start a container in a terminal, then run some commands
while maintaining the state within the container.

The [new version](https://github.com/kinow/cylc-docker)
now maps a volume to the version of cylc, installs the dependencies, and
then allows the state to be maintained solely in the mapped volume.

Furthermore, the entrypoint of the image is the `cylc` command. Which means that
you do not have to execute a terminal in order to run commands to the container
(or change the command/entrypoint).

{% geshi 'shell' %}
...
VOLUME "/opt/cylc" "/tmp" "/run" "/var/run" # we have the state stored only in /opt/cylc
WORKDIR "/opt/cylc"
ENV PATH /opt/cylc/bin:$PATH
WORKDIR /opt/cylc
ENTRYPOINT ["cylc"] # here's the trick!
{% endgeshi %}

It uses the same approach from the PHP image I am using for Composer, with a few
additional improvements from the [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) documentation.

If you have a utility in your computer that requires a few dependencies, but that
can store the state/data in a mapped volume, the same kind of container may be
useful.
