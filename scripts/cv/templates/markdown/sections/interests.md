{% extends "section.md" %}

{% block body %}

<table class="ui celled table">
{% for item in items %}
  <tr>
    <td>{{ item }}</td>
  </tr>
{% endfor %}
</table>
{% endblock body %}
