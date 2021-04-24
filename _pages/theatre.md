---
title: Theatre
layout: page
permalink: "/theatre/"
---

{%- assign plays = site.data.plays -%}
<div class="cards">
  {%- for play in plays -%}
  <div class="card">
    <div class="content">
      <p class="header">{{ play.title }}</p>
      <p class="meta">{{ play.date }}</p>
    </div>
    {%- if play.photo != nil and play.photo != blank -%}
    <div class="image">
      <img src="/assets/pages/theatre/{{ play.photo }}" alt="Play photo" />
    </div>
    {%- endif -%}
    <div class="content">
      {{ play.description | markdownify }}
    </div>
    <div class="extra content">
      <p class="meta">
        {{ play.location }}
      </p>
    </div>
  </div>
  {%- endfor -%}
</div>
