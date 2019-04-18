---
title: 'Extract images from a Word document'
id: 481
author: kinow
tags: 
    - visual basic
category: 'blog'
time: '16:10:26'
---
Some time ago I was asked by my boss to get all the images out of a Word document and save them in a separated directory. In this <a title="Extract images from word" href="http://www.gmayor.com/extract_images_from_word.htm">site</a> the author gives you several different ways of extracting images from a Word document. However what I wanted was a quick and dirt way of having these images extracted without macros or having to open and save the document in HTML format.

So I wrote this quick and dirt word images extractor. It has two versions, one where you need to pass the .doc file as parameter and another one that gives you an input dialog box to point out where is the file. You can get the VBScripts from <a title="http://github.com/kinow/word-images-extractor" href="http://github.com/kinow/word-images-extractor">http://github.com/kinow/word-images-extractor</a>.

<div class='row'>
<div class="ui container" style='text-align: center;'>
<figure>
<a href="assets['word-images-extractor']" rel="prettyPhoto" class="thumbnail" title="">
<img class="ui fluid image" src="assets['word-images-extractor']" alt="=" />
</a>
<figcaption></figcaption>
</figure>
</div>
</div>

Behind the scenes, this VBScript uses Word to save your .doc as .html and then copies the saved images into the same directory as your word file. So yes, you do have to have Word installed. If somebody gets interested in improving it, he/she could find a way of extracting multiple files at once. In this version some files are overridden. He/she could add to the beginning of the image name the word file name. Or it could be required to pass the output directory together with the input word file.

That's it, I hope it might be helpful to somebody as it was - and still is - to me. :-)

<a title="http://github.com/kinow/word-images-extractor" href="http://github.com/kinow/word-images-extractor">http://github.com/kinow/word-images-extractor</a>

Cheers