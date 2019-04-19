---
title: A couple of class diagrams of JupyterHub
time: '21:43:44'
author: kinow
tags:
    - python
    - jupyterhub
    - opensource
---

Started on a new project last Monday. One of the tasks in this project involves a new design
for the Web layer. And as the application is quite similar to [JupyterHub](https://jupyterhub.readthedocs.io/),
we are all learning more about its internal API and general system design.

This post contains only two class diagrams created with PyCharm. One is actually a SQLAlchemy
ORM diagram, below.

<p style='text-align: center;'>
<a href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/jupyterhub-sqlalchemy-graph.png">
<img style="display: inline; width: 100%;" class="ui image" src="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/jupyterhub-sqlalchemy-graph.png"  />
</a>
</p>

<!--more-->

And the class diagram (which I removed `object` and a tried to make it simpler to interpret).

<p style='text-align: center;'>
<a href="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/jupyterhub-class-diagram.png">
<img style="display: inline; width: 100%;" class="ui image" src="/assets/posts{{page.path | remove: ".md" | remove: "_posts" }}/jupyterhub-class-diagram.png"  />
</a>
</p>

I enjoyed the parts of the code and the part of the system design that I could read about so far.
But that's all for now, until I have more time to learn more about the project and the code.

_p.s. there are spawners and other implementation classes in other GitHub repositories... so a more complete diagram may come later on_

