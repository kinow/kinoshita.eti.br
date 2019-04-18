---
title: "Securely using passwords with R"
author: kinow
tags: 
    - r
    - programming
    - security
time: '20:21:39'
---

It is quite common to have code that needs to interact with another system, database, or third party application, and need to use some sort of credentials to securely communicate.

Most of the code I wrote in **R**, or reviewed, had normally no borders (from a system analysis perspective) with other systems, or basically just interacted with the file system to retrieve NetCDF or JSON files.

However, after I saw a comment in *Reddit* [1] some time ago about this, I decided to check what others used. With **R Shiny** becoming more popular, and moving more R code to the web, I think this will become a common requirement for R code.

There is a blog post from **RevolutionAnalytics** [2] that does a nice summary of the options for that. The post is from 2015, but I do not think much changed now in 2017. From the blog post and comments, there are seven methods listed:

1. Put [credentials](https://github.com/ropensci/fishbaseapi/blob/80393023a958aee54e2daa58c337458db5480b84/config_template.yaml) in your source code
2. Put credentials in a file in your project, but do not share this file (*#3*, *#4*, and *#5* are similar to this one)
3. Put credentials in a [.Rprofile](https://csgillespie.github.io/efficientR/3-3-r-startup.html#rprofile) file
4. **Put credentials in a [.Renviron](https://csgillespie.github.io/efficientR/3-3-r-startup.html#renviron) file**
5. Put [credentials](https://github.com/ropensci/fishbaseapi/blob/80393023a958aee54e2daa58c337458db5480b84/config_template.yaml) in a JSON or YAML file
6. Put credentials in a secure store that you can access from R
7. Ask the user for the credentials when the script is executed (possibly not useful for R Shiny applications)

**My preferred way for R is the .Renviron (or a [dotEnv](https://github.com/gaborcsardi/dotenv)) file**. You basically store your password in this file, make sure you do not share this (a global gitignore could be helpful to prevent any accident) and read the variables when you start your code.

{% geshi 'r' %}
## Secrets
MYSQL_PASSWORD=secret
{% endgeshi %}

If you would like to increase the security, you can combine it with a variation of *#6*. You use a .Renviron file, and use an encryption service like [Amazon KMS](https://aws.amazon.com/kms/) (KMS stands for Key Management Service).

With [AWS KMS in R](https://github.com/cardcorp/AWR.KMS), you can encrypt your values, put them encrypted in your .Renviron, and even if someone gets hold of your .Renviron file, you have an extra layer of protection, as the attacker would require access to your cloud environment to decrypt it too.

{% geshi 'r' %}
## Secrets
MYSQL_PASSWORD=AQECAHga320J8WadplGCqqVAr4HNvDaFSQ+NaiwIBhmm6qDSFwAAAGIwYAYJKoZIhvcNAQcGoFMwUQIBADBMBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEE99+LoLdvYv8l41OhAAIBEIAfx49FFJCLeYrkfMfAw6XlnxP23MmDBdqP8dPp28OoAQ==
{% endgeshi %}

### References

- [1] [r/stats * Open source R applications and hiding database connection](https://www.reddit.com/r/rstats/comments/6aonwx/open_source_r_applications_and_hiding_database/)
- [2] [How to store and use webservice keys and authentication details with R](http://blog.revolutionanalytics.com/2015/11/how-to-store-and-use-authentication-details-with-r.html)

&hearts; Open Source
