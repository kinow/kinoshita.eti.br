---
title: Finding "ryukokosho" in Taiwan
layout: post
categories:
- languages
tags:
- language
- japanese
- chinese
---

Last week a friend told me he was looking for a place in Taiwan called “Ryukokosho”.
Or maybe “Ryoko kosho”. From what I understood, he was looking for a mosquito species.

The species name is “[Anopheles tessellatus](https://en.wikipedia.org/wiki/Anopheles_tessellatus)”,
and one of its synonyms is “[kinoshitai Koidzumi](http://www.mosquitocatalog.org/taxon_descr.aspx?ID=20899)” — pure
coincidence that _kinoshitai_!

That synonym entry appears to have been found at the following location:
**Ryukokosho**, Taihoku (Taipei), Formosa [Taiwan, ROC] (LU). So how to find
Ryukokosho if Google Maps cannot find it, and Google brings only a handful of
entries with the species synonyms, and no maps or other GIS data?

<!--more-->

### It is in Taiwan

Both “Ryukokosho” and “Ryoko kosho” sound Japanese, and not really Chinese.
The reason is that between 1895 and 1945 Taiwan was under Japanese rule, and some
places got different names. Even now, many words from Chinese are still pronounced
in Japan with the Japanese reading of the Chinese characters.

From that location, it is possible to immediately identify that it is somewhere in
Taiwan.

We can probably tell that it is an old entry, as Taiwan is being identified as
“Formosa”. I remember Taiwan being called “Ilha Formosa” in textbooks in Brazil
when I was in high school.

_Formosa_ in Portuguese means pretty, beautiful. It was the name given
to the island of Taiwan [by Portuguese explorers](https://en.wikipedia.org/wiki/Taiwan).

### It is in Taipei

Another hint at the date of the synonym entry is the next part, Taihoku.
The capital of Taiwan is Taipei, written as 「台北」. Reading those two
characters in Japanese, a possible way to read it would be Tai-Hoku.

Taipei was officially [renamed to Taihoku](https://en.wikipedia.org/wiki/Taipei)
in 1895 when Japan annexed Taiwan.

Curiously, Taihoku [is still in use](https://languagelog.ldc.upenn.edu/nll/?p=40072)
in Japan. But so is Taipei.

### Now, where is Ryukokosho?

This was the tricky part. The name of many [places in Japan](https://en.wikipedia.org/wiki/Place_names_in_Japan)
have the last part representing the kind of place it is. For example:

- -ken for prefecture, as in Kumamoto-ken
- -shi for the city, as in Kumamoto-shi
- -ku for the wad of a city, as in Tokyo-ku
- -mura for village, as in Kamikuishiki-mura
- -hoku or kita- for North, as in Hokkaido, Taihoku, or Kita-ku
- -shima or -jima for island, as in Iwo-Jima

Looking at -sho, and -kosho, nothing came to my mind. With some help of Jisho.org,
it looked like it could be this old character for "manor; villa", 「庄」, read as
shou or shō.

Many words when translated to English lose their vowels, like Toukyou that becomes
Tokyo, and Kyouto becomes Kyoto. So maybe shou lost its u, and became sho?

I asked a co-worker from China, that once told me her village was near Taiwan.
A few minutes later she gave me the following place name in
Chinese characters 「龍匣口」.

Surprised, I asked her how she found that name so quickly. She told me she wrote
"ryoko" in a dictionary to translate from Japanese to Chinese. I assume the dictionary
gave her some possible character combinations, and she picked the one made
more sense.

Searching for this in English wasn't really helpful. Then after searching Wikipedia,
I found this link in Chinese for the Longxiakou village: https://zh.m.wikipedia.org/wiki/龍匣口

### Longxiakou

If you translate the Wikipedia page from Mandarin into English, the first paragraph
says:

>Longxiakou is an old place name in Taipei City . It is located in the middle of present-day
>Zhongzheng District. It includes all of Aiguoli, Nanmenli, Longguangli, and Longfuli, and
>the northeast half of Xia'anli, Longxingli and The north part of Sanyuan Street in Yonggongli,
>a small part of the northeast end of Yingxueli, the northern half of Nanfuli, the west of
>Xinyingli and the south of Dongmenli.

So now we have a good source to identify the location of the mosquito!

>It is located in the middle of present-day
>Zhongzheng District

<img
  class="fluid"
  src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/zhongzheng-district.png"
  alt="Google Map for Zhongzheng District"
  aria-label="Google Map for Zhongzheng District"
  />

Unfortunately, names like Aiguoli don't seem to match the name in Chinese (愛國里), or at least
Google Maps is not able to locate them.

The map above should at least be a good starting point for someone looking for Ryukokosho.

I found [this one](https://www.facebook.com/IntoChengNan/photos/a.357412827975944/508448539539038/?type=3&theater)
on FaceBook, but without knowing Chinese, the only part I could confirm is that
the light brown area at the top contains the words 「南門」 (South gate?) and 「龍匣口」 (Longxiakou).

The text also talks about the village in the past.

<img
  class="fluid"
  src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/longxiakou-map-facebook.png"
  alt="Map with Longxiakou Village"
  aria-label="Map with Longxiakou Village"
  />

Using QGIS 3, the Georeferencer plug-in, and quickly adding some points manually,
then finally adjusting raster transparency, the final map looks like this.

<img
  class="fluid"
  src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/longxiakou-georeferenced.png"
  alt="Longxiakou village georeferenced on OSM map"
  aria-label="Longxiakou village georeferenced on OSM map"
  />

If you would like to import the QGIS files, or have a look at the points I used,
browse the files over [here](https://github.com/kinow/kinoshita.eti.br/tree/master/assets/posts/2020-08-16-finding-ryukokosho-in-taiwan). 
