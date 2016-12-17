{% extends "section.md" %}

{% block body %}
<table class="ui celled table">
{% for item in items %}
<tr>
  <td>{{ item.title }}</td>
  <td markdown="1">
{{ item.details }}
  </td>
</tr>
{% endfor %}
</table>
{% endblock body %}
