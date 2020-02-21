---
layout: post
tags:
- gis
categories:
- blog
title: Plotting Auckland with OSMnx
---

<img style="height: 400px;" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/figure_1.png" alt="Auckland" />

A couple of days ago I saw [a thread in reddit](https://www.reddit.com/r/gis/comments/5lnjxs/creating_squaremile_figureground_diagrams_of/)
about OSMnx. It is a utilty for interacting with the OpenStreeMap (OSM)
API, manipulate it in pure Python and using libraries like NetworkX (a Python graph package).

With it you can do things like <q>visualize cul-de-sacs or one-way streets, plot shortest-path routes, or calculate stats like intersection density, average node connectivity, or betweenness centrality</q>. Or simply
plot the OSM data as in the graph above.

The source code is hosted at GitHub: [https://github.com/gboeing/osmnx](https://github.com/gboeing/osmnx).

<!--more-->

<blockquote cite="https://github.com/gboeing/osmnx">OSMnx is a Python 2+3 package that lets you download spatial geometries and construct, project, visualize, and analyze street networks from OpenStreetMap's APIs. Users can download and construct walkable, drivable, or bikable urban networks with a single line of Python code, and then easily analyze and visualize them.</blockquote>

The only issue I found while creating the map for Auckland using the example from the project
README, was that the script would exit with the following error: **"ValueError: Geometry must be a shapely Polygon or MultiPolygon"**.

After looking at the list of dependencies and finding that everything seemed to be OK,
I started looking at the project issues. And thankfully someone else had found the
[same issue](https://github.com/gboeing/osmnx/issues/16)
and the maintainer of the project answered how to fix it.

The issue was that the OSM API returns two [entries for Auckland](https://nominatim.openstreetmap.org/search?format=json&limit=10&dedupe=0&polygon_geojson=1&q=Auckland,%20New%20Zealand)
, where the first one is a Point, and the
second is the one that we want (a Polygon). The application defaults to using the first element,
so in order to change it you have to give a *which_result* argument.

```python
#!/usr/bin/env python3

import osmnx as ox
G = ox.graph_from_place('Auckland, NZ', network_type='drive', which_result=2)
ox.plot_graph(ox.project_graph(G))
```

And after that, and after waiting a few minutes, you should get your map :-)

Happy hacking!
