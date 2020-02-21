---
layout: post
tags:
- git
categories:
- blog
title: 'git clone fails with fatal: Unable to find remote helper for ''https'''
---

<p>I've been working in a client site without Internet connection, and behind a troll proxy. There is an internal yum repository, but many dependencies are missing.</p>

<p>There weren't git-all, git or git-core packages there, so I had to download and install from sources. I didn't pay attention to the <code>./configure</code> output and proceeded with <code>make</code> and <code>make install</code>.</p>

<p>Git was installed and ready to rock, but in my first <code>git clone https://</code> (SSH ports are blocked) I received: <strong>fatal: Unable to find remote helper for 'https'</strong>.</p>

<p>Turns out that I was missing libcurl-devel, though I did have curl. After installing libcurl-devel and installing from sources again all worked fine.</p>
