---
layout: post
tags:
- javascript
- vuejs
categories:
- blog
title: Using Lumino with Vue
---

[Lumino](https://github.com/jupyterlab/lumino) is the engine that powers the GUI of
[JupyterLab](https://github.com/jupyterlab/jupyterlab/). It used to be called Phosphor JS,
but some time ago there was a misunderstanding and the author gave up maintaining it.
Then JupyterLab decided to fork it under this new name.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/demo.gif" />

The documentation is still lacking, but it works as expected, and there is already a
community supporting it. We decided to use it in [Cylc UI](https://github.com/cylc/cylc-ui)
to have tabbed panels like JupyterLab.

[This project](https://github.com/kinow/vue-lumino) contains the part of the code of
Cylc UI that integrated Lumino and Vue. It was a suggestion from one of the maintainers
of JupyterLab, that got involved in an issue of Cylc UI. You can find this project linked
too in the Lumino project `README` file.

<!--more-->

Lumino handles the DOM directly, while Vue deals with a virtual DOM. So integrating
both can be a bit tricky. And there are probably more than one way of doing it. So
I am not claiming the route we went is the best.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/01.png" />

The main component for this integration is called `Lumino`. It has an array in its
`data` section that holds one entry for each widget that must be added to the Lumino
`BoxPanel`. The array can contain anything, like booleans or numbers. It holds the
ID of each widget added. This ID is the actual HTML element ID, and is used in the code
by even listeners to activate, delete, and maintain the state of the Lumino widgets and
the Vue components.

<img class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/02.png" />

The `BoxPanel` goes into a `div` created in the component template, exclusively for
Lumino.

As Lumino stars working with the DOM before Vue has had time to move things
from the virtual DOM, we need to compensate by asking Vue to wait before 

<img class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/03.png" />

The final step in the integration are wrappers for Vue components. These wrappers
represent the component, but are actually used to attach the component's HTML element
to the widget HTML element.

The `.appendChild` function in JS takes care of moving nodes within the DOM. And Vue
is smart enough to remove the element correctly. It should also take care of event
listeners automagically, but for safety I prefer to add and remove event listeners
myself.

<img class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/04.png" />

Through even listeners, and controlling when something from the virtual DOM
can access something from the DOM, and tricking Lumino into creating empty widgets
that later receive the HTML element from the wrapped Vue component, we get it
working with Vue in the same as Lumino works with JupyterLab.

[https://github.com/kinow/vue-lumino](https://github.com/kinow/vue-lumino)
