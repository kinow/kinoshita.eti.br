---
title: Short Stories
layout: page
---
<table>
  <colgroup>
    <col width="50%" />
    <col width="50%" />
  </colgroup>
  <thead style="">
    <tr>
      <th>Title</th>
      <th>Author</th>
    </tr>
  </thead>
  <tbody>
    {%- assign stories = site.data.short-stories | sort_natural: "author" -%}
    {%- for story in stories -%}
    <tr>
      {%- if story.link -%}
      <td><a href="{{ story.link }}">{{ story.title }}</a></td>
      {%- else -%}
      <td>{{ story.title }}</td>
      {%- endif -%}
      <td>{{ story.author }}</td>
    </tr>
    {%- endfor -%}
  </tbody>
</table>
