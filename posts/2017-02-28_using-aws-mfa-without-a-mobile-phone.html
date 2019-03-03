---
title: 'Using AWS MFA without a mobile phone'
author: kinow
tags:
    - go
    - aws
    - security
category: 'blog'
time: '00:47:03'
---

If you use AWS, the chances are that you use MFA - Multi-factor Authentication - to authenticate.
I don't like to install apps in my mobile phone, unless I need to, so having bought a new phone
recently, I decided to find a replacement for Google Authenticator.

There are several command line utilities, browser extensions, libraries, and tools (free and paid)
that implement the TOTP - time-based one-time password -, the standard
[required by Amazon](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html)
for MFA authentication.

I decided to use a Go tool for the first time: [gauth](https://github.com/pcarrier/gauth). Note that you
won't be able to use it from home, in case you don't bring your laptop home. You can have one MFA device
linked to your AWS account, so you may have to remove an existing one. Follow these instructions with care :^)

### Install Go

{% geshi 'shell' %}
sudo apt update && sudo apt upgrade -y
cd tmp/ && wget https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz
tar -zxvf go1.*.tar.gz
sudo mv go /usr/local
vim ~/.bashrc
{% endgeshi %}

Add the following at the bottom of the file.

{% geshi 'shell' %}
GOROOT=/usr/local/go
GOPATH="$HOME/go"
PATH="$GOPATH/bin:$GOROOT/bin:$PATH"
{% endgeshi %}

And you can test it with `. ~/.bashrc && go version`.

### Install gauth

Given your environment is correctly set up, you should be able to use the following command to install
gauth, and have it available in your *$PATH*.

{% geshi 'shell' %}
go get github.com/pcarrier/gauth
{% endgeshi %}

Edit *~/.config/gauth.csv* adding a value for the AWS MFA key.

### Getting the AWS MFA key

To get the value that you must place in your *gauth.csv* file, you must add a new MFA device. When asked to scan a QR code, look for an option to enter the manual value. That will give you a long string. That's the value you are looking for.

### Extra: Auto copy-paste from command line

If you would like to quickly copy and paste, try creating an alias as described
[on this gist](https://gist.github.com/ehime/9fd8810442daf64686a34f885e18be01).

I used these instructions, and can now run one command line, that will put the next MFA code in my
clipboard. Then just paste into my browser, and that's that!

Happy hacking!

### References

* [gauth: replace Google Authenticator](https://github.com/pcarrier/gauth)
* [Enabling a Virtual Multi-factor Authentication (MFA) Device](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html)
* [How to Install Go 1.7 on Ubuntu 16.04 & 14.04](http://tecadmin.net/install-go-on-ubuntu/)
* [Use pbcopy on Ubuntu](http://garywoodfine.com/use-pbcopy-on-ubuntu/)
