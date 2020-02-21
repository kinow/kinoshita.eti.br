---
layout: post
tags:
- programming
- python
- opensource
categories:
- blog
title: Enabling Markdown Extension Tables For Piecrust
---

[PieCrust](https://github.com/ludovicchabant/PieCrust2) is a Python static site generator.
It allows users to write content in Markdown. But if you try adding a table, the content by
default will be generated as plain text.

You have to enable [Markdown extension tables](https://pythonhosted.org/Markdown/extensions/tables.html).
PieCrust will [load it](https://github.com/ludovicchabant/PieCrust2/blob/6462e052045552d2ba164f4965370d84ddb54946/piecrust/formatting/markdownformatter.py#L29)
when creating the Markdown instance.

```yaml
# config.yml
markdown:
  extensions:
    - tables
```

Et, voil&agrave;! Happy blogging!

&hearts; Open Source
