---
categories:
- blog
date: "2020-03-26T00:00:00Z"
tags:
- jenkins
- jupyter
- python
title: Jenkins Active Choices with Jupyter Notebooks
---

[Jenkins Active Choices](https://plugins.jenkins.io/uno-choice/) provides interactive and reactive parameters for the Jenkins UI.
It is used by DevOps but also by researchers in industry and academia. Some days ago I ran an experiment where I tried
to reproduce similar behaviour of the plug-in with Jupyter Notebooks and [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/).

The experiment was a success, and I am convinced one could achieve the same in Jupyter Notebooks. Jenkins could be used as
workflow manager, or the parameters could be submitted to a different workflow manager or another system.

<a href="https://twitter.com/kinow/status/1234053592203481090" alt="Link to Tweet">
<img alt="Tweet" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/Screenshot_2020-03-26_17-45-04.png" />
</a>

You can see more in the following links:

- Viewer link: [https://nbviewer.jupyter.org/github/kinow/notebooks/blob/master/python/ipywidgets/active-choices-with-notebooks.ipynb](https://nbviewer.jupyter.org/github/kinow/notebooks/blob/master/python/ipywidgets/active-choices-with-notebooks.ipynb)
- Notebook link: [https://github.com/kinow/notebooks/blob/master/python/ipywidgets/active-choices-with-notebooks.ipynb](https://github.com/kinow/notebooks/blob/master/python/ipywidgets/active-choices-with-notebooks.ipynb)
