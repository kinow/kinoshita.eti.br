{% extends "section.md" %}

{% block body %}

<table class="ui celled table">
{% for school in items %}
  <tr>
    <td>
      {% if school.degree %}
        <strong>{{ school.degree }}</strong>
      {% endif %}
      {{ school.school }}
    </td>
    <td>{{ school.dates }}</td>
  </tr>
{% endfor %}
</table>
{% endblock body %}
