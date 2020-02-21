---
date: 2017-12-02 22:51:00 +1300
layout: post
tags:
- programming
- java
- apache software foundation
categories:
- blog
title: Watch out for Locales when using NumberFormat with currencies
---

In Java you have the [NumberFormatException](https://docs.oracle.com/javase/9/docs/api/java/text/NumberFormat.html)
to help you formatting and parsing numbers for any locale. Said that, here's some code.

```shell
BigDecimal negative = new BigDecimal("-1234.56");

DecimalFormat nf = (DecimalFormat) NumberFormat.getCurrencyInstance(Locale.UK);
String formattedNegative = nf.format(negative);

System.out.println(formattedNegative);
```

The output for this code is **-£1,234.56**. That's expected, as the locale is set to
UK, so the currency symbol used is for British Pounds. And as the number is negative, you
get that minus sign as a prefix. For Japanese locale you'd get **-￥1,235**, and for Brazilian
locale you'd get **-R$ 1.234,56**.

So far so good. 

What about the following code, with nothing different except for the locale set to **US**.

```shell
BigDecimal negative = new BigDecimal("-1234.56");

DecimalFormat nf = (DecimalFormat) NumberFormat.getCurrencyInstance(Locale.US); // <--- US now
String formattedNegative = nf.format(negative);

System.out.println(formattedNegative);
```

Some could intuitively expect **-$1,234.56**. However, **the output is actually ($1,234.56)**.

There are different prefixes and suffixes. But in some locales the prefix can be empty, or, as
in the case of the US locale, it can be quite different than what you could expect.

Learned about this peculiarity from NumberFormat while working on [VALIDATOR-433](https://issues.apache.org/jira/browse/VALIDATOR-433) for Apache Commons Validator.

Happy hacking!
