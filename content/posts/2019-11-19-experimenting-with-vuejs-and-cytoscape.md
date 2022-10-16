---
categories:
- blog
date: "2019-11-19T00:00:00Z"
tags:
- javascript
- vuejs
- cylc
- cytoscape
- graph
title: Experimenting with Vuejs and Cytoscape
---

The project I work on at work had a GUI interface with Python and PyGTK, which is now being
ported to the web. We have adopted Vuejs as the JS framework, and have been building the
components required for our UI over the past months. The project is hosted
[on GitHub](https://github.com/cylc/cylc-ui) licensed under GPLv3.

In Cylc 7, an important visualization was the workflow graph. The screen shot below is from
the design sketches done by another contributor from the UK, showing how it should look in
Cylc 8.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/cylc8-sketch.png" />

The first library we decided to try is Cytoscape, a well-known graph library, with use cases
in research, corporate, and other fields. One limitation of Cytoscape is that the way it renders
the graph nodes is limited.

Limited, meaning that you won't be able to easily add HTML, images, SVG, animation, etc. Though
not impossible.

<!--more-->

This post contains links to Codepen pens with the progress from a basic example with
a simple component that displays an SVG, to a final example where we had the component
data being updated periodically, and the graph also being updated through Vuejs'
reactivity.

This is the [first pen](https://codepen.io/kinow/pen/OJJELJe), which displays just a
Cylc Job icon. The icon is an SVG, with the background colour varying according to the
job status. It is transparent by default, red if the status is "failed", blue if
"succeeded", etc.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/graph1.png" />

No biggie, we simply have here a simplified version of the
[Cylc Job component](https://github.com/cylc/cylc-ui/blob/c9920f21ffdc96e82038cc480f11adba28310ff5/src/components/cylc/Job.vue).
This pen is using Vue and Vuetify.

In the next [pen](https://codepen.io/kinow/pen/YzzvKwR?editors=1010) we have a few more JS scripts, namely Cytoscape,
Dagre, and the Cytoscape Dagre libraries. While Cytoscape is able to both parse the graph data, supports graph
algorithms, and also is able to organize the graph layout, Dagre is focused on the last part. So delegating the
layout part to Dagre is just to have an example that is easier to visualize, but not really a requirement.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/graph2.png" />

The data used for this example is a direct copy-and-paste from a GraphQL response from
a running workflow in Cylc 8. Plus a `computed` variable to give just the data needed for the
graph component.

So the first pen had a component and basic libraries. The second pen the test data, and a few more libraries.
I prefer to break down problems and slowly build up a solution this way. Feel free to skip to the end of this
post if you just want the final working pen.

The third [pen](https://codepen.io/kinow/pen/oNNJreG?editors=1010) has one more JS library,
the Node HTML Label extension for Cytoscape. With this extension, we are able to use HTML
to display the graph node.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/graph3.png" />

So there is a new component too, a `network` component, which takes a list of components and renders
a Cytoscape graph. Similar to `VueCytoscape` - which did not provide any improvement to our current
use case, so we are not using it.

One trick part was how to put the contents of the Job component inside the node HTML label
in the graph. Basically, it is necessary to mount the component, and then access its `$el`
which is an `HTMLElement`.

```js
cy1.nodeHtmlLabel([
  {
    query: 'node',
    tpl: function (data) {
      const JobClass = Vue.extend(Job)
      const theJob = new JobClass({
        propsData: {
          status: data.status
        }
      }).$mount()
      return theJob.$el.outerHTML
    }
  }
])
```

While it does put the SVG within the node, we don't have reactivity.

After going for a walk and reading some chapters of Peter F. Hamilton's Reality Dysfunction,
it occurred to me that instead of creating a new Vuejs component in the graph, it should be possible
to let Vuejs create and manage the component, and just "link" the node HTML label with the component.
That's in the [next pen](https://codepen.io/kinow/pen/eYYbwXB?editors=1010).

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/graph4.png" />

Instead of creating the instance in the node HTML label `tpl` function, we are now creating Job
components with Vuejs, assigning them "refs", and then just grabbing the HTML to render in the
node.

```js
cy1.nodeHtmlLabel([
  {
    query: 'node',
    tpl: function (data) {
      const jobForThisNode = window.vm.$refs[data.id][0]
      if (Object.hasOwnProperty.call(jobForThisNode, '$el')) {
        return jobForThisNode.$el.outerHTML
      }
      return ''
    }
  }
])
```

Slightly better. Now the `tpl` function has less responsibility, and there is a better separation
of concerns. However, there is still the issue of the Vuejs reactivity. In [another pen](https://codepen.io/kinow/pen/abbPeqj)
I added a function to return a random Job status, and used it within a `setInterval` to
randomly change the job statuses every three seconds.

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/graph5.gif" />

That brings us to the [last pen](https://codepen.io/kinow/pen/XWWOrvW) (whew). It looked like a good
approach to leave the component creation and lifecycle managed by Cylc, and trying to link the node
HTML label and the component. But simply setting the HTML content of the Job component would not work.

So instead, for node HTML template I've used a simple div, and for its `id` attribute used the
node ID (unique in a workflow, returned by the GraphQL query).

<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/graph6.gif" />

There is a new component in this pen too, a `GraphNode`, which wraps a `Job` component, but adds
some extra functionality, like observing when the prop changes.

```js
const GraphNode = Vue.component('graph-node', {
  name: 'GraphNode',
  components: {
    job: Job
  },
  props: {
    node: {
      type: Object,
      required: true
    }
  },
  watch: {
    node: {
      immediate: true,
      deep: true,
      handler (newValue, oldValue) {
        const nodeElem = document.getElementById(newValue.id)
        const vm = this
        if (nodeElem) {
          Vue.nextTick(function () {
            nodeElem.innerHTML = vm.$mount().$el.outerHTML
          })
        }
      }
    }
  },
  template: `<span>
  <job :status="node.state" />
</span>`
})
```

The `node` passed is a node of the GraphQL response. With a `watch` that runs immediately upon
the component initialization (`immediate: true`) and that reacts to changes in the object
attributes (`deep: true`, for `node.state = anotherValue`), we get the desired behaviour.

The component is not perfect. It does not match our design sketch, I am not sure if there are
no cases where Cytoscape and Vuejs would get "out of sync" with each other (probably not as
both are using the same data, but still...), and I am not sure what the performance would look
like with hundreds or thousands of nodes for larger Cylc workflows.

But this is a good example of i) using Vuejs with Cytoscape, ii) displaying SVG in Cytoscape nodes,
and iii) updating the Cytoscape data based on Vuejs reactivity. And we will probably use some of what
was learned here for building the new web interface for Cylc 8.

Stay tuned!
