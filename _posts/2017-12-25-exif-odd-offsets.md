---
date: 2017-12-25 21:43:33 +1300
layout: post
tags:
- programming
- java
- apache software foundation
- opensource
categories:
- blog
title: Exif Odd Offsets
---

A file format like JPEG may contain metadata in JFIF, [Exif](https://en.wikipedia.org/wiki/Exif),
or a vendor proprietary format. The Exif format is based - or uses parts of - on the TIFF format.

Within an Exif metadata block, you should see directories, with several entries. The entries have fields
like description, value, and also an offset. The offset indicates the offset to the next entry.

The Exif specification defines that **implementers must make sure to keep the offset an even number,
within 4 bytes**.

I recently worked on [IMAGING-205](https://issues.apache.org/jira/browse/IMAGING-205), a ticket
about odd offsets in files with Exif metadata. This issue was exactly to address that when files
were rewritten with Apache Commons Imaging, even though the image initially had no odd offsets,
after the entries were rearranged, we could have odd offsets.

The fix was simply checking for odd offsets, adding +1, and later it would be put within the
4 bytes limit.

<p style='text-align: center;'>
<img style="display: inline" class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/screenshot.png" alt="A screen shot of Eclipse with source code" title="Locating the bug" />
<br/>
<small>Locating the bug</small>
</p>

One interesting point, however, is that this is in the standard, but not all software that read
and write Exif follow the specification. So it is quite common to find images with odd offsets.

Which means you could take a picture with your phone, that contains some Exif metadata, and
be surprised to analyze it with `exiftool` and get warnings about odd offsets. Most viewers
handle odd and even offsets, so it should work for most cases, unless you have a strict reader/viewer.

Happy hacking!

&heart; Open Source
