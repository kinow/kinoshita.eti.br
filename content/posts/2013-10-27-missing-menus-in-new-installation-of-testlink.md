---
categories:
- blog
date: "2013-10-27T00:00:00Z"
tags:
- testlink
title: Missing menus in new installation of TestLink 1.9.8
---

I recently installed TestLink 1.9.8 and noticed that the menus and some other parts 
of the UI we missing. Looking at <code>/var/log/testlink/userlog1.log</code> (the location 
may change depending on your settings) I realized that there was something wrong 
with my PHP installation. There were log messages like the below.

    include_once(ADORecordSet_ext_empty.class.php): failed to open stream: No such file or directory - in /home/kinow/php/workspace/testlink-1.9.8/lib/functions/common.php - Line 92
    [13/Sep/18 12:51:09][WARNING][2o0h173pdgg5fjqh1pukr83og2][GUI]
    E_WARNING
    include_once(): Failed opening 'ADORecordSet_ext_empty.class.php' for inclusion (include_path='.:/usr/share/php:/usr/share/pear:.:/home/kinow/php/workspace/testlink-1.9.8/lib/functions/:/home/kinow/php/workspace/testlink-1.9.8/lib/issuet
    ...
    
I found a post in a forum (but unfortunately I forgot to save the link) that suggested 
these ADORecordSet were being caused by the module **php5-adodb**. Removing the module, and 
cleaning the templates cache directory (<code>$TESTLINK_HOME/gui/templates_c/*</code>) 
fixed the issue for me.

Hope that helps.
Happy testing!
