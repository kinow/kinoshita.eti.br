---
title: "How to remove the signature from e-mails with NLP?"
author: kinow
tags: 
    - python
    - programming
    - natural language processing
    - opensource
time: '13:59:33'
---

Some time ago I stumbled across [EmailParser](https://github.com/mynameisvinn/EmailParser), a Python utility to remove e-mail signatures. Here's a sample input e-mail from the project documentation.

{% geshi 'text' %}
Wendy – thanks for the intro! Moving you to bcc.
 
Hi Vincent – nice to meet you over email. Apologize for the late reply, I was on PTO for a couple weeks and this is my first week back in office. As Wendy mentioned, I am leading an AR/VR taskforce at Foobar Retail Solutions. The goal of the taskforce is to better understand how AR/VR can apply to retail/commerce and if/what is the role of a shopping center in AR/VR applications for retail.
 
Wendy mentioned that you would be a great person to speak to since you are close to what is going on in this space. Would love to set up some time to chat via phone next week. What does your availability look like on Monday or Wednesday?
 
Best,
Joe Smith
 
Joe Smith | Strategy & Business Development
111 Market St. Suite 111| San Francisco, CA 94103
M: 111.111.1111| joe@foobar.com
{% endgeshi %}

And here's what it looks like afterwards.

{% geshi 'text' %}
Wendy – thanks for the intro! Moving you to bcc.
 
Hi Vincent – nice to meet you over email. Apologize for the late reply, I was on PTO for a couple weeks and this is my first week back in office. As Wendy mentioned, I am leading an AR/VR taskforce at Foobar Retail Solutions. The goal of the taskforce is to better understand how AR/VR can apply to retail/commerce and if/what is the role of a shopping center in AR/VR applications for retail.
 
Wendy mentioned that you would be a great person to speak to since you are close to what is going on in this space. Would love to set up some time to chat via phone next week. What does your availability look like on Monday or Wednesday?
{% endgeshi %}

As you can see, it removed all the lines after the main part of the message (i.e. after the three paragraphs). Here's what the Python code looks like.

{% geshi 'python' %}
>>> from Parser import read_email, strip, prob_block
>>> from spacy.en import English 

>>> pos = English()  # part-of-speech tagger
>>> msg_raw = read_email('emails/test1.txt')
>>> msg_stripped = strip(msg_raw)  # preprocessing text before POS tagging

# iterate through lines, write to file if not signature block
>>> generate_text(msg_stripped, .9, pos_tagger, 'emails/test1_clean.txt') 
{% endgeshi %}

What got me interested about this utility was the use of NLP. I couldn't imagine how someone could use NLP for that. And I liked the simplicity of the approach, which is not perfect, but can be useful someday.

After the imports in the code, it creates a [Part of Speech](https://en.wikipedia.org/wiki/Part_of_speech) tagger using [spaCy](https://spacy.io/) NLP library, reads the e-mail from a file, and sripts and creates an array with each paragraph of the message.

The magic happens in the `generate_text` function, which receives the **array of paragraphs**, a **threshold**, the **POS tagger**, and the **output destination**. Here's what the function does.

{% geshi 'text' %}
for each message
    if probability ( signature block | message ) < threshold
        write to output file
{% endgeshi %}

And the formula for calculating the probability is quite simple too.

{% geshi 'text' %}
1. For a given paragraph (message block), find all the sentences in it.
2. Then for each word (token) in the sentence, count the number of times a non-verb appears.
3. Return the proportion of non-verbs per sentence, i.e. number of non-verbs / number of sentences.
{% endgeshi %}

In summary, it discards blocks that do not contain enough verbs to be considered a message block, being treated as signature blocks instead.

Never thought about using an approach like this. It may definitely be helpful when doing data analysis, information retrieval, or scraping data from the web. Not necessarily with e-mails and signatures, but you got the gist of it.

&hearts; Open Source
