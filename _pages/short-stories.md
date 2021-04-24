---
title: Short Stories
layout: page
---
{%- assign reading_resources = site.data.short-stories | sort_natural: "author" -%}
<div class="cards" markdown="0">
  {%- for reading_resource in reading_resources -%}
    {%- if reading_resource.link -%}
      {%- capture title -%}<a href="{{ reading_resource.link }}">{{ reading_resource.title }}</a>{%- endcapture -%}
    {%- else -%}
      {%- assign title = reading_resource.title -%}
    {%- endif -%}
  <div class="card">
    <div class="content">
      <p class="title">{{ title }}</p>
    </div>
    <div class="content">
      <p class="meta">{{ reading_resource.author }}</p>
    </div>
  </div>
  {%- endfor -%}
</div>
