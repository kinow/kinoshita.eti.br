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

{% geshi 'shell' %}
$ docker run -ti -v "$(pwd -P)"/cylc:/opt/cylc cylc validate /opt/cylc/etc/examples/tutorial/oneoff/basic/
Valid for cylc-7.7.2
$ docker run -ti -v "$(pwd -P)"/cylc:/opt/cylc cylc register /opt/cylc/etc/examples/tutorial/oneoff/basic/
REGISTER /opt/cylc/etc/examples/tutorial/oneoff/basic/
$ docker run -ti -v "$(pwd -P)"/cylc:/opt/cylc cylc start --non-daemon --debug /opt/cylc/etc/examples/tutorial/oneoff/basic/
            ._.                                                       
            | |                 The Cylc Suite Engine [7.7.2]         
._____._. ._| |_____.           Copyright (C) 2008-2018 NIWA          
| .___| | | | | .___|  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
| !___| !_! | | !___.  This program comes with ABSOLUTELY NO WARRANTY;
!_____!___. |_!_____!  see `cylc warranty`.  It is free software, you 
      .___! |           are welcome to redistribute it under certain  
      !_____!                conditions; see `cylc conditions`.       
2018-07-30T12:10:32Z INFO - Suite starting: server=3714d1a17999:43040 pid=1
2018-07-30T12:10:32Z INFO - Cylc version: 7.7.2
2018-07-30T12:10:32Z INFO - Run mode: live
2018-07-30T12:10:32Z INFO - Initial point: 1
2018-07-30T12:10:32Z INFO - Final point: 1
2018-07-30T12:10:32Z INFO - Cold Start 1
2018-07-30T12:10:32Z DEBUG - [hello.1] -released to the task pool
2018-07-30T12:10:32Z DEBUG - BEGIN TASK PROCESSING
2018-07-30T12:10:32Z DEBUG - [hello.1] -waiting => queued
2018-07-30T12:10:32Z DEBUG - 1 task(s) de-queued
2018-07-30T12:10:32Z INFO - [hello.1] -submit-num=1, owner@host=localhost
2018-07-30T12:10:32Z DEBUG - [hello.1] -queued => ready
2018-07-30T12:10:32Z DEBUG - END TASK PROCESSING (took 0.00642895698547 seconds)
2018-07-30T12:10:32Z DEBUG - ['cylc', 'jobs-submit', '--debug', '--', '/opt/cylc/etc/examples/tutorial/oneoff/basic/log/job', '1/hello/01']
2018-07-30T12:10:33Z DEBUG - [client-connect] root@3714d1a17999:cylc-message privilege='full-control' 7b05596a-5971-4733-82de-28528f702ff0
2018-07-30T12:10:33Z INFO - [client-command] put_messages root@3714d1a17999:cylc-message 7b05596a-5971-4733-82de-28528f702ff0
2018-07-30T12:10:33Z DEBUG - [jobs-submit cmd] cylc jobs-submit --debug -- /opt/cylc/etc/examples/tutorial/oneoff/basic/log/job 1/hello/01
	[jobs-submit ret_code] 0
	[jobs-submit out]
	[TASK JOB SUMMARY]2018-07-30T12:10:32Z|1/hello/01|0|61
	[TASK JOB COMMAND]2018-07-30T12:10:32Z|1/hello/01|[STDOUT] 61
2018-07-30T12:10:33Z INFO - [hello.1] -(current:ready) submitted at 2018-07-30T12:10:32Z
2018-07-30T12:10:33Z INFO - [hello.1] -job[01] submitted to localhost:background[61]
2018-07-30T12:10:33Z DEBUG - [hello.1] -ready => submitted
2018-07-30T12:10:33Z INFO - [hello.1] -health check settings: submission timeout=None
2018-07-30T12:10:33Z DEBUG - BEGIN TASK PROCESSING
2018-07-30T12:10:33Z DEBUG - 0 task(s) de-queued
2018-07-30T12:10:33Z DEBUG - [hello.1] -forced spawning
2018-07-30T12:10:33Z DEBUG - END TASK PROCESSING (took 0.000992059707642 seconds)
2018-07-30T12:10:33Z INFO - [hello.1] -(current:submitted)> started at 2018-07-30T12:10:33Z
2018-07-30T12:10:33Z DEBUG - [hello.1] -submitted => running
2018-07-30T12:10:33Z INFO - [hello.1] -health check settings: execution timeout=None
2018-07-30T12:10:34Z DEBUG - BEGIN TASK PROCESSING
2018-07-30T12:10:34Z DEBUG - 0 task(s) de-queued
2018-07-30T12:10:34Z DEBUG - END TASK PROCESSING (took 0.000984191894531 seconds)
2018-07-30T12:10:43Z DEBUG - [client-connect] root@3714d1a17999:cylc-message privilege='full-control' 524d658e-9932-4135-9523-3c2ace3990cf
2018-07-30T12:10:43Z INFO - [client-command] put_messages root@3714d1a17999:cylc-message 524d658e-9932-4135-9523-3c2ace3990cf
2018-07-30T12:10:43Z INFO - [hello.1] -(current:running)> succeeded at 2018-07-30T12:10:43Z
2018-07-30T12:10:43Z DEBUG - [hello.1] -running => succeeded
2018-07-30T12:10:43Z INFO - Suite shutting down - AUTOMATIC
2018-07-30T12:10:44Z INFO - DONE
$
{% endgeshi %}

If you have a utility in your computer that requires a few dependencies, but that
can store the state/data in a mapped volume, the same kind of container may be
useful.
