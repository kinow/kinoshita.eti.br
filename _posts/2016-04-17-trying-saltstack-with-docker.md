---
title: 'Trying SaltStack with Docker'
author: kinow
tags:
    - jenkins
    - docker
    - saltstack
category: 'blog'
time: '22:06:03'
---

Some weeks ago I started learning [SaltStack](http://saltstack.com/) for a project at work. But I couldn't
find a good Docker image for that and I had to ask the Ops team for some VM's. We
are having a rainy weekend in Auckland, so I decided to have another look at the
[Jenkins SaltStack Plug-in](https://wiki.jenkins-ci.org/display/JENKINS/saltstack-plugin).

But now since I was at home, I couldn't use the VM's that I had access to at
work. So decided to look again at Docker or Vagrant images. After playing
with a few images, I found [bbinet/salt-master](https://hub.docker.com/r/bbinet/salt-master/).
It not only sets up a master, but also provides an easy way to enable the cherrypy
API (necessary for the Jenkins plug-in).

This post describes the steps that I took to have a running Salt Master with the API
enabled. First you need to create some directories and files to use with the image.

```shell
shell$ mkdir ~/master && cd ~/master
shell$ mkdir -p config/master.d/
shell$ vim config/master.d/api.conf
```

The api.conf contains the SaltStack API configuration. You can change port, user
and other settings if necessary. Just remember to add a credential in Jenkins
for the plug-in.

```shell
# File: api.conf
external_auth:
  pam:
    saltapiuser:
      - .*
      - '@runner'
      - '@wheel'
      - '@jobs'
rest_cherrypy:
  port: 8000
  host: 0.0.0.0
  disable_ssl: True
  static: /opt/molten
  static_path: /assets
  app: /opt/molten/index.html
  app_path: /molten
```

The image also conveniently provides a script that is executed before the
entry point (if provided). So we can also create a user for the API automatically
when the image is created.

```shell
shell$ vim config/before-exec.sh
```

```shell
#!/bin/bash
# File: before-exec.sh
useradd saltapiuser
echo -e "nosecret\nnosecret\n" | passwd saltapiuser
exit 0
```

Also make the script executable.

```shell
chmod +x config/before-exec.sh
```

And finally start the container.

```shell
docker run --name salt-master -v $PWD/config:/config \
    -p 4505:4505 -p 4506:4506 -p 443:443 -p 8000:8000 \
    bbinet/salt-master
```

Once the container is running, you can go to http://localhost:8000 and
log in as saltapiuser:nosecret, and also configure your plug-in
in Jenkins.

Happy hacking!

