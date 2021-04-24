---
title: Books
layout: page
---
{%- assign reading_resources = site.data.books | sort_natural: "author" -%}
<div class="reading-resources" markdown="0">
  {%- for reading_resource in reading_resources -%}
    {%- if reading_resource.link -%}
      {%- capture title -%}<a href="{{ reading_resource.link }}">{{ reading_resource.title }}</a>{%- endcapture -%}
    {%- else -%}
      {%- assign title = reading_resource.title -%}
    {%- endif -%}
  <div class="reading-resource">
    <p class="title">{{ title }}</p>
    <p class="author">{{ reading_resource.author }}</p>
  </div>
  {%- endfor -%}
</div>
