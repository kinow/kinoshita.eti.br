---
title: 'Content negotiation with Spring Boot and React'
author: kinow
tags:
    - java
    - spring
category: 'blog'
time: '20:07:03'
---

A few days ago I had a bug in a system built with Spring Boot and React. The frontend application
was using a REST client in React, built in a similar way to what is found in the documentation, and
also in blogs.

{% geshi 'javascript' %}
import rest from 'rest';
const Rest = () => rest.wrap(mime);
{% endgeshi %}

However, for one of the Spring Boot application endpoints, the React component was not working. The
response seemed to be OK in the Network tab, of the browser developer tools. But the component was
failing and complaining when parsing the response.

Turns out that the frontend was sending the request with the header `Accept: text/plain, application/json`.
And Spring Boot was just using its [default content negotiation](https://spring.io/blog/2013/05/11/content-negotiation-using-spring-mvc)
and returning what the frontend requested: a text plain version of, what looked like, JSON.

The quick fix was to request the content as JSON in React.

{% geshi 'javascript' %}
import rest from 'rest';
import mime from 'rest/interceptor/mime';
const Rest = () => rest.wrap(mime , { mime: 'application/json' } );
{% endgeshi %}

Now we will revisit the backend to return the JSON content, as content, regardless of what
the user asks :-)

Happy hacking!
