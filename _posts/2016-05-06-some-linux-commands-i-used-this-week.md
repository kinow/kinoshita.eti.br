---
title: 'Some Linux commands I used this week'
author: kinow
tags:
    - linux
category: 'blog'
time: '23:26:03'
---

These are some commands I used on Linux servers this week. Adding them here in case someone else
find them interesting, and also due to my bad memory :-)

## Listing latest installed packages in SLES

{% geshi 'shell' %}
rpm -qa --last
{% endgeshi %}

This will display the last packages installed. Useful when there are packages being updated, and you
need to confirm what changed, and when.

## Listing packages in SLES and origin repository

{% geshi 'shell' %}
rpm -qa --qf '%-30{DISTRIBUTION} %{NAME}\n'| sort
{% endgeshi %}

The output will have two columns. The first containing the repository name, and the second column with
the package name. For example.

{% geshi 'shell' %}
devel:languages:R:base / SLE_11_SP2 R-base
devel:languages:R:base / SLE_11_SP2 R-base-devel
home:flacco:sles / SLE_11_SP3 php53-phar
home:happenpappen / SLE_11_SP2 nodejs
{% endgeshi %}

## Grep for content in XML tags

Be it for web services, or for finding things in Jenkins XML files. Being able to grep the tag attribute
or tag name might be useful. Look at the following example that uses the 
[books XML provided by Microsoft for testing](https://msdn.microsoft.com/en-us/library/ms762271%28v=vs.85%29.aspx).

{% geshi 'shell' %}
grep -oP "(?<=<genre>).*?(?=</genre>)" books.xml | sort | uniq
{% endgeshi %}

Which will outputs the following.

{% geshi 'shell' %}
Computer
Fantasy
Horror
Romance
Science Fiction
{% endgeshi %}

## Find Python site packages directory

Sometimes you have Anaconda, but also the system installation, and maybe even other Python distributions.
Knowing where Python is looking for site packages can be helpful to confirm the package exists, and also
to inspect its sources.

{% geshi 'shell' %}
python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"
{% endgeshi %}

An example of the output of the script.

{% geshi 'shell' %}
/usr/lib/python2.7/dist-packages
{% endgeshi %}

## Force no-cache via curl for a list of files

Useful when you have a proxy like squid caching some requests from an application and you
want to flush the cache and get the latest content (which will be cached again, but then
you can fix it once confirmed).

{% geshi 'shell' %}
curl --silent -H 'Cache-Control: no-cache' http://systemcachingvalues.local/somedoc.html
{% endgeshi %}

## Find to which servers a Linux process is talking to

You have to find the pid of the process that you would like to investigate (e.g. 6364) and have
[strace](http://linux.die.net/man/1/strace) installed.

{% geshi 'shell' %}
strace -p 6364 -f -e trace=network -o output.txt
{% endgeshi %}

The command above creates output.txt with the trace information. Then you can grep for
the IP addresses with the following regex.

{% geshi 'shell' %}
grep -E -o "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" output.txt
{% endgeshi %}

Which will output something similar to the following example.

{% geshi 'shell' %}
127.0.1.1
127.0.1.1
127.0.1.1
192.168.20.4
10.10.0.12
...
{% endgeshi %}

And finally, you can call dig to get the server name, and also remove duplicates.

{% geshi 'shell' %}
grep -E -o "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" output.txt | xargs -l dig +noall +answer +nocmd -x | awk '{ print $5}' | sort | uniq
{% endgeshi %}

Which gives you the following.

{% geshi 'shell' %}
ec2-52-13-43-205.compute-1.amazonaws.com.
ec2-52-32-244-147.compute-1.amazonaws.com.
ec2-52-44-11-85.compute-1.amazonaws.com.
ec2-52-55-36-20.us-west-2.compute.amazonaws.com.
ec2-52-11-19-24.us-west-2.compute.amazonaws.com.
ec2-52-2-21-13.compute-1.amazonaws.com.
ec2-54-33-249-49.us-west-2.compute.amazonaws.com.
ec2-54-180-165-17.us-west-2.compute.amazonaws.com.
ec2-54-2-177-91.compute-1.amazonaws.com.
ec2-54-8-163-15.compute-1.amazonaws.com.
syd11s01-in-f124.1e110.net.
syd11s02-in-f5.1e110.net.
syd12s02-in-f3.1e110.net.
...
{% endgeshi %}

That's all for today.

Happy hacking!
