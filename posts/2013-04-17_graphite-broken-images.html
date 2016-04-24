---
title: 'Graphite: Broken images'
id: 1294
author: kinow
tags:
    - monitoring
    - python
category: 'blog'
time: '11:36:38'
---
<p>This morning I was setting up a <a href="http://graphite.wikidot.com/" title="Graphite">Graphite </a>server to collect metrics with <a href="https://github.com/etsy/statsd/" title="statsd">statsd</a>, <a href="http://logstash.net/" title="LogStash">LogStash </a>and <a href="https://github.com/jmxtrans/jmxtrans" title="jmxtrans">jmxtrans</a>. After following the instructions from @jgeurst, I've successfully installed Graphite.</p>

<p>I had previously installed another test box, so I decided to take a deeper look at the settings, write a <a href="https://puppetlabs.com/" title="Puppet">puppet</a> manifest and prepare this new box to become a production server. However, after browsing the webapp, all graphs were broken.</p>

<p>After googling a while, reading forums and bugs, I decided to open the <em>$GRAPHITE_HOME/webapp/graphite/render/views.py</em>, adding <em>log.rendering(...)</em> statements (not the most elegant solution, I know).</p>

<p>By following the program workflow I found out it was entering a block after checking if it should remotely render the image. This feature is turned on/off by <strong>REMOTE_RENDERING</strong> = True/False, in local_settings.py.</p>

<p>After setting this to <em>False</em> the problem was solved.</p>