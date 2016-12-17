{% extends "section.md" %}

{% block body %}

<table class="ui celled table">
{% for item in items %}
  <tr>
    <td>{{ item.title }}</td>
    <td>{{ item.date }}</td>
  </tr>
{% endfor %}
</table>
{% endblock body %}
