---
title: 'Add a header to a file with Shell script (sed)'
author: kinow
tags:
    - shell script
category: 'blog'
time: '01:55:03'
---

Today I was re-generating the documentation for a REST API written in PHP, with
Laravel. To generate the documentation, one would have to call a Laravel command first.
That command would create a Markdown page. And since in this project I am using Jekyll
for the project site, the final step was adding a header to the file, so that Jekyll
can recognize that content as a blog post.

Laravel allows you to add custom commands to your project, so I decided to write a command
that would call the other command that generates the documentation, and add an extra step
of adding the header to the Markdown file.

Here's the shell script part, that allows you to add a header to a file, in place (i.e.
it will alter and save the change your file).

```shell
sed -i 1i"----\nlayout: page\ntitle: API Installation\n----\n\n" ./docs/documentation/api/api.md
```

Here the first argument to sed, *-i* is for in place. Then that strange *1i*
means that it will insert something before the first line, once. Then we have our header,
and finally the file.

Happy hacking!
