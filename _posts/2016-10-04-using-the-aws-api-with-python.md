---
date: 2016-10-04 21:15:03 +1300
layout: post
tags:
- python
- aws
title: Using the AWS API with Python
---

Amazon Web Services provides a series of cloud services. When you access the web interface, most - if not all - of the actions you do there are actually translated into API calls.

They also provide SDK's in several programming languages. With these SDK's you are able to call the same API used by the web interface. Python has [boto](https://github.com/boto/boto3) (or boto3) which lets you to automate several tasks in AWS.

But before you start using the API, you will need to [set up your access key](https://web.archive.org/web/20160818112016/http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html).

It is likely that with time you will have different roles, and may have different permissions with each role. You have to configure your local environment so that you can either use the command line Python utility (installed via `pip install awscli`) or with boto.

The awscli is a dependency for using boto3. After you install it, you need to run `aws configure`. It will create the <em>~/.aws/config</em> and <em>~/.aws/credentials</em> files. You can tweak these files to support multiple roles.

I followed the tutorials, but got all sorts of different issues. Then after debugging some locally installed dependencies, in special awscli files, I found that the following settings work for my environment.

```shell
# File: config
[profile default]
region = ap-southeast-2

[profile profile1]
region = ap-southeast-2
source_profile = default
role_arn = arn:aws:iam::123:role/Developer

[profile profile2]
region = ap-southeast-2
source_profile = default
role_arn = arn:aws:iam::456:role/Sysops
mfa_serial = arn:aws:iam::789:mfa/user@domain.blabla
```

and

```shell
# File: credentials
[default]
aws_access_key_id = YOU_KEY_ID
aws_secret_access_key = YOUR_SECRET
```

And once it is done you can, for example, confirm it is working with some S3 commands in Python.

```python
#!/usr/bin/env python3

import os
import boto3

session = boto3.Session(profile_name='profile2')
s3 = session.resource('s3')

found = False

name = 'mysuperduperbucket'

for bucket in s3.buckets.all():
    if bucket.name == name:
        found = True

if not found:
    print("Creating bucket...")
    s3.create_bucket(Bucket=name)

file_location = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'samplefile.txt'
s3.meta.client.upload_file(Filename=file_location, Bucket=name, Key='book.txt')
```

The AWS files in this example are using MFA too, the multi-factor authentication. So the first time you run this code you may be asked to generate a token, which will be cached for a short time.

That's it for today.

Happy hacking!
