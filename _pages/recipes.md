---
title: 'Recipes'
layout: page
permalink: "/recipes/"
note: "Our cooking recipes. Some are in English. Some are in Portuguese."
---

{%- assign recipes = site.data.recipes | sort_natural: "title" -%}
{%- for recipe in recipes -%}
## {{ recipe.title }}

**Ingredients**

<ul>
{%- for ingredient in recipe.ingredients -%}
<li>{{ ingredient }}</li>
{%- endfor -%}
</ul>

**Instructions**

<ul>
{%- for instruction in recipe.instructions -%}
<li>{{ instruction }}</li>
{%- endfor -%}
</ul>

{%- endfor -%}
