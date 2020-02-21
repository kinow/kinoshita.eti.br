---
date: 2018-12-24 15:43:43 +1300
layout: post
tags:
- php
- skosmos
- semantic web
- vocabulary server
categories:
- blog
title: How the Skosmos Widget Wiki plugin works
---

Skosmos can be extended through plugins, or widgets (a widget is a plugin for Skosmos).
You can read more about how [plugins work in Skosmos here](https://github.com/NatLibFi/Skosmos/wiki/Plugins).

This post is a note-to-self, explaining how the **Skosmos Widget Wiki plugin** works. This
is a plugin - or widget - that displays Wikipedia information when the concept supports it.

Here's an image of the plugin in action. Or you can go to
[a live instance of Skosmos](http://finto.fi/yso-paikat/en/page/p107650)
that has the plugin enabled.


<img class="ui fluid image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/skosmos-widget-wiki-screenshot.png" />


<!--more-->

### Under the hood

The plugin exposes a JavaScript callback via its `plugin.json` file. In the callback, it
receives a `data` object, with the following properties.

- `uri`, the concept identifier, e.g. _http://www.yso.fi/onto/yso/p107650"_
- `prefLabels`, the concepts preferred labels, e.g. _"Central Asia"@en_, _"Keski-Aasia"@fi_
- `pageType`, defaults to `page`
- `json-ld`, which contains the JSON-LD `@context`, as well as a `graph` property

If the `pageType` is not `page`, or if there are no preferred labels, or if there is no
JSON-LD data, the plugin is not activated.

When the plugin is activated, it will iterate through all entries in the graph, looking
for one which `uri` starts with `wd:` (for wikidata). Here's what the `wikidata` object
will look like.

```javascript
{
  "uri": "wd:Q27275",
  "type": "http://wikiba.se/ontology#Item",
  "schema:description": [
    {
      "lang": "ko",
      "value": "아시아의 중앙부."
    },
    {
      "lang": "pt-br",
      "value": "região entre o leste do mar Cáspio e o centro-oeste da China, entre o norte do Irã e o Afeganistão, e o sul da Sibéria"
    },
    {
      "lang": "en",
      "value": "core region of the Asian continent"
    },
    //...
  ],
  "schema:name": [
    {
      "lang": "ko",
      "value": "중앙아시아"
    },
    //...
  ],
  "label": [
    {
      "lang": "ko",
      "value": "중앙아시아"
    },
    //...
  ],
  "prefLabel": [
    {
      "lang": "ko",
      "value": "중앙아시아"
    },
    //...
  ],
  "wdt:P31": [
    {
      "uri": "wd:Q82794"
    },
    {
      "uri": "wd:Q3502482"
    }
  ],
  "wdt:P625": {
    "type": "http://www.opengis.net/ont/geosparql#wktLiteral",
    "value": "Point(63.9 45.3)"
  }
}
```

Now the plugin will iterate the `graph` object once again, looking for entries
which the object type is `schema:Article`, and the `schema:isPartOf` ends with
`.wikipedia.org/`. These entries are aggregated into a list, `wikiArticlesList`.

This list is then iterated, building a reverse dictionary `keyLangUriValue`
with the language as key, and the URI as value. `keyLangUriValue` will look
something like the next example.

```javascript
{
  "ace": "https://ace.wikipedia.org/wiki/Asia_Teung%C3%B6h",
  "af": "https://af.wikipedia.org/wiki/Sentraal-Asi%C3%AB",
  "am": "https://am.wikipedia.org/wiki/%E1%88%98%E1%8A%AB%E1%8A%A8%E1%88%88%E1%8A%9B_%E1%8A%A5%E1%88%B5%E1%8B%AB",
  //...
}
```

Now comes the penultimate step. The plugin has access to some global variables,
including `languageOrder`, which contains the list of languages available in the
vocabulary used by the concept (actually the current vocabulary configuration).

For each of these languages, we grab the language code, and try to find it in
`keyLangUriValue`. Oh, the languages are ordered, and first comes the one we are
currently using! Important to mention it.

So once it locates one match in `keyLangUriValue`, the plugin then crafts the
URL (e.g. _https://en.wikipedia.org/api/rest_v1/page/html/Central_Asia_).

If there is no match, the plugin will render a 404 message. But when there is a
match, and the REST URL was created, it uses JQuery to submit an Ajax request.

Upon a success after querying the Wikipedia public REST API, the plugin will
use JQuery, an existing template.html plus Handlebars to render the template
under the `.concept-info` element. It also customizes a scroll bar, and there
are stylesheets applied for theming.

And that's how the plugin works under the hood!
