---
layout: post
tags:
- python
- cylc
- graphql
title: A look at the first implementation of GraphQL in Cylc
---

For Cylc 8 we are adding an initial implementation of GraphQL, to replace the previous REST API.
Besides the technologies in the API's, another difference is that for the REST API, its main
consumer was a PyGTK GUI.

The new GraphQL API, on the other hand, will be used mainly by a Vue.js Web application. So a
few things need to be done in a different way due to the jump from Desktop GUI to Web GUI.

## Protobuf model

The current implementation is under review in a pull request at the moment. It includes
Python libraries for GraphQL, as it is expected, but also a Protobuf data model that
can be visualized in the figure below.

