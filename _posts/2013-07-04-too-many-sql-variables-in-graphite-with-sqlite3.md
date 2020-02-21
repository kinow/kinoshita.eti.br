---
layout: post
tags:
- monitoring
- python
categories:
- blog
title: Too many SQL variables exception in Graphite with SQLite3
---

Having run [Graphite](http://graphite.wikidot.com/) for a while, today I found a rather annoying issue. We were using 
[events](https://code.launchpad.net/~lucio.torre/graphite/add-events/+merge/69142), and everything was working perfectly fine so far. But for the 24 last hours, 
the graph was blank. 

Actually, in the dashboard, the graph was *missing*, being displayed as a gray box. 
Enabling the web inspector in Google Chrome I got the graph URL. Opening the link in 
a new tab gave me the exception message: **too many SQL variables** (<sup>1</sup>).

After some research, I found out this was a bug in SQLite. After trying to hack the code, 
and being concerned about using a patched version of Graphite and having to update it 
later, I decided to switch database. 

But to avoid losing the graphs, users and other settings, including the events, I 
migrated the SQLite database to a MySQL server. This MySQL server was already installed in 
the server machine, since this machine hosted a [Zabbix](http://www.zabbix.com/) server too.

Here are the steps required to migrate your database from SQLite to MySQL (<sup>2</sup>).

* Download **sqlite3_mysql** python script from [http://www.redmine.org/boards/2/topics/12793](http://www.redmine.org/boards/2/topics/12793)
* Stop Apache/Nginx
* mysql -u user -p -e "create database redmine graphite set utf8;" 
* sqlite3 graphite.db .dump | sqlite3-to-mysql.py | mysql -uroot -pyourpass graphite
* Start Apache again

After tail'ing the Graphite webapp log file, 

```shell
tail f- storage/log/webapp/error.log
```

I noticed the Python MySQLdb wasn't installed.

```python
ImproperlyConfigured: Error loading MySQLdb module: No module named MySQLdb
```

My server was an Ubuntu 13.04, so I installed the module simply with the following 
command.

```shell
apt-get install python-mysqldb
```

Hope that helps!

<p><small><sup>1</sup> You may have to enable *DEBUG* in your Django settings for seeing the exception in your browser</small></p>
<p><small><sup>2</sup> Zabbix needed some minor tweaks in order to use [MariaDB](https://mariadb.org/), but probably you can give it a try too</small></p>
