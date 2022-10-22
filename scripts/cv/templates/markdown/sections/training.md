{% extends "section.md" %}

{% block body %}

<table class="ui celled table">
{% for training in items %}
  <tr>
    <td>{{ training.title }}</td>
    <td>{{ training.school }}</td>
    <td>{% if training.location %}
        {{ training.location }}
      {% endif %}
    </td>
    <td>{{ training.year }}</td>
  </tr>
{% endfor %}
</table>
{% endblock body %}
