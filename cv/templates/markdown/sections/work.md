{% extends "section.md" %}

{% block body %}
<table class="ui celled table">
{% for i in items %}
<tr>
  <td><strong>{{ i.place }}</strong>, {{ i.title }}</td>
  <td>{{ i.dates }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
