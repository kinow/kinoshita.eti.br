---
date: 2017-03-14 21:22:03 +1300
layout: post
tags:
- docker
categories:
- blog
title: Order of containers in Docker Compose
---

In Docker Compose you are able to control the startup order of the containers via
the *depends_on* statement. This is documented in [Controlling startup order in Compose](https://docs.docker.com/compose/startup-order/).

If you have a simple setup, with Tomcat and Postgres, sometimes Postgres will start first, but Compose
will initialize Tomcat before Postgres has fully booted. When that happens, you may receive 401, 404, or other
application errors.

You can fix it by combining *depends_on* with a *healthcheck*. For example:

```shell
# File: docker-compose.yml
version: '2.1'
services:
  db:
    container_name: twpg
    build:
      context: .
      dockerfile: Dockerfile.postgres
    restart: always
    ports:
      - "5432:5432"
    healthcheck:
      test: "pg_isready -h localhost -p 5432 -q -U postgres"
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    container_name: twtc
    build:
      context: .
      dockerfile: Dockerfile.tomcat
    restart: always
    depends_on:
      db:
        condition: service_healthy
    links:
      - db
    ports:
      - "80:8080"
```

In the example docker-compose.yml, there are two containers, *db* and *web*. web is running
a Tomcat, and db is running Postgres. Web depends on db (see depends_on), and uses a condition
*service_healthy*. Which indicates it depends that that container is healthy.

The *healthcheck* entry under the db container settings define how to check whether Postgres
is running or not. In this case, we are using *pg_isready*, which is available in the
vanilla Postgres 9 container.

It will try 5 times, with a 10 seconds interval, and will time out after 5 seconds. You may
have to tune these parameters for your application.

This code snippet is from a
[pull request submitted to Foxoncz/docker-thingworx](https://github.com/Foxoncz/docker-thingworx/pull/3/files).

&hearts; Open Source
