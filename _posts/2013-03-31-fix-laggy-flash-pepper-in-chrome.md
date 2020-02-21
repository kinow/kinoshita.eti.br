---
layout: post
tags:
- linux
categories:
- blog
title: Fix laggy Flash (Pepper) in Chrome
---

<p>My chrome died twice this morning. Checking the system logs I found some segmentation errors. Since it was not so recent version, I updated to the latest version of Chrome. But after that my Flash player was laggy/slowly, and I couldn't listen to <a href="http://tunein.com/radio/Live-Ireland-Channel-1-s17895/#" title="Live Ireland Channel 1">Live Ireland Channel 1</a> no more :-( (I listen to either this radio or r/electrohouse on reddit.tv while I'm programming... I know, I'm a bit weird).</p>

<p>If you are having the same problem, here's the list of actions that I did to fix it.</p>

<p>TL;DR: Disable the Pepper Flash, as well as the Gnash or other flash libraries installed, download flash plug-in from <a href="http://get.adobe.com/flashplayer/" title="http://get.adobe.com/flashplayer/">http://get.adobe.com/flashplayer/</a> and enable it.</p>

<ul>
	<li>Went to chrome:plugins and disabled the Pepper Flash.</li>
	<li>Now I was back at using the Gnash flash plug-in previously installed. Now, although I could watch to Youtube videos, my radio wasn't playing yet.</li>
	<li>Disabled all Flash plug-ins, went to <a href="http://get.adobe.com/flashplayer/" title="http://get.adobe.com/flashplayer/">http://get.adobe.com/flashplayer/</a> and got the latest version (tar.gz, since I'm using Debian).</li>
	<li>Copied the libflashplayer.so to <em>/opt/google/chrome/plugins</em></li>
	<li>Re-enabled the Shockwave Flash plug-in (you have to expand the details section, in order to be able to choose which version you want to enable</li>
</ul>

<p>And now I'm happily writing this blog and code, listening to Salonika - Dublin City Ramblers.</p>

<p>Cheers</p>
