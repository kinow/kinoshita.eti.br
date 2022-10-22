---
categories:
- blog
date: "2019-11-09T00:00:00Z"
tags:
- javascript
- vuejs
title: Dynamic breadcrumbs with Vue Router nested routes and Vuetify Breadcrumb component
---

Vue Router supports nested routes, which allow developers to create a hierarchical navigation structure.
This is handy if you want to create breadcrumbs based on this hierarchy dynamically.

Here's how you should create your nested routes:

```js
const routes = [
  { path: '/', component: { template: `<h1>Home View</h1>` } },
  {
    path: '/users',
    component: {
      render (c) {
        return c('router-view')
      }
    },
    meta: { breadCrumb: 'Users' },
    children: [
      {
        path: '',
        component: {
          template: `
            <div>
              <h1>Users View</h1>
              <router-link to="/users/1">View User 1</router-link>
            </div>
          `
        }
      },
      {
        path: ':id',
        component: {
          render (c) {
            return c('router-view')
          }
        },
        meta: { breadCrumb: 'View User' },
        children: [
          {
            path: '',
            component: {
              template: `
                <div>
                  <h1>User View</h1>
                  <router-link to="/users/1/edit">Edit User</router-link>
                </div>
              `
            }
          },
          {
            path: 'edit',
            component: {
              template: `<h1>Edit User</h1>`
            },
            meta: { breadCrumb: 'Edit User' }
          }
        ]
      }
    ]
  }
]
```

<!--more-->

The tricky part is that you need to remember that the parent breadcrumb must not have a component rendering anything,
but instead simply use `<router-view></router-view>` instead, to display the children routes. And have a child route
with the `path: '''`.

So if you have `/users` as the parent breadcrumb, it won't have any template, except for the call to `<router-view>`.
Then its child route that is bound to the path `''` will be rendered and replace the `<router-view>` call.

The last thing necessary is some code to compute the breadcrumbs, and prepare the data structure required for the
[Vuetify Breadcrumb component](https://vuetifyjs.com/en/components/breadcrumbs). I've used
[this example by Pratheek Hegde](https://medium.com/@pratheekhegde/displaying-application-breadcrumbs-in-vue-js-85456dc8a370)
with some modifications. You may want to tweak it to your application.

```js
  computed: {
    crumbs: function() {
      let pathArray = this.$route.path.split("/")
      pathArray.shift()
      let breadcrumbs = pathArray.reduce((breadcrumbArray, path, idx) => {
        breadcrumbArray.push({
          path: path,
          to: breadcrumbArray[idx - 1]
            ? "/" + breadcrumbArray[idx - 1].path + "/" + path
            : "/" + path,
          text: this.$route.matched[idx].meta.breadCrumb || path,
        });
        return breadcrumbArray;
      }, [])
      return breadcrumbs;
    }
  }
``` 

{{< showimage
  image="breadcrumbs.png"
  alt=""
  caption=""
  style=""
>}}

Working example can be found [here](https://codepen.io/kinow/pen/vYYrWeG).
