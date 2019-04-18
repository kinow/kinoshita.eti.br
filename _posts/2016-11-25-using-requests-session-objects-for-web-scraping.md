---
title: 'Using Requests Session Objects for web scraping'
author: kinow
tags:
    - python
category: 'blog'
time: '01:24:03'
---

I had to write a Python script some months ago, that would retrieve Solar energy
data from a web site. It was basically a handful of HTTP calls, parse the response
that was mainly in JSON, and store the results as JSON and CSV for processing later.

Since it was such a small task, I used the [Requests](http://docs.python-requests.org)
module instead of a complete web scraper. The HTTP requests had to be made with a
time out, and also pass certain headers. I started customizing each call, until
I learned about the Requests [Session Objects](http://docs.python-requests.org/en/master/user/advanced/).

You create a session, as in ORM/JPA, where you can define a context, with certain properties
and control an orthogonal behavior.

{% geshi 'python' %}
import requests

def get(session, url):
    """Utility method to HTTP GET a URL"""
    response = session.get(url, timeout=None)
    return response

def post(session, url, data):
    """Utility method to HTTP POST a URL with data parameters"""
    response = session.post(url, data=data, timeout=None)
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    return response

with requests.Session() as s:
    # x-test header will be sent with every request
    s.headers.update({'x-test': 'true'})

    data = {'user': user, 'password': password, 'rememberne': 'false'}
    r = post(s, 'https://portal.login.url', data)

    r = get(s, 'https://portal.home.url')
{% endgeshi %}

Besides the session object, that gives you ability to add headers to all requests,
you won't have to worry about redirects. The library by default takes care
[of that](https://github.com/kennethreitz/requests/blob/dfad00a6e84bc75b12468ca29ccf4f971c813fc8/requests/sessions.py#L110)
with a [default limit of up to 30](https://github.com/kennethreitz/requests/blob/dfad00a6e84bc75b12468ca29ccf4f971c813fc8/requests/models.py#L54).

Happy hacking!
