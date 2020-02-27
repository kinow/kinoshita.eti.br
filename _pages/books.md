---
title: Books
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
    {%- assign books = site.data.books | sort_natural: "author" -%}
    {%- for book in books -%}
    <tr>
      {%- if book.link -%}
      <td><a href="{{ book.link }}">{{ book.title }}</a></td>
      {%- else -%}
      <td>{{ book.title }}</td>
      {%- endif -%}
      <td>{{ book.author }}</td>
    </tr>
    {%- endfor -%}
  </tbody>
</table>

And here's my [Amazon wish list](http://www.amazon.com/gp/registry/wishlist/?ie=UTF8&cid=A1O606WLPSNDOF).
