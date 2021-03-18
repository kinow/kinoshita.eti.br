---
title: Portfolio
layout: page
permalink: "/portfolio/"
gallery:
  - title: Logos
    images:
      - title: Apache OpenNLP
        src: /assets/pages/art/thumbs/thumb-opennlp-1.png
        link: /2017/04/21/apache-opennlp-logo/
      - title: Frege Programming Language
        src: /assets/pages/art/thumbs/thumb-frege-2.png
        link: /2016/08/24/revamping-frege-logo-part-2
      - title: TupiLabs
        src: /assets/pages/art/thumbs/thumb-tupilabs-1.png
      - title: Yandê
        src: /assets/pages/art/thumbs/thumb-yande-1.png
  - title: Paintings
    images:
      - title: Green Skull
        src: /assets/pages/art/thumbs/thumb-green-skull-full.png
        link: /2020/04/03/green-skull
      - title: Royal Spoonbill
        src: /assets/pages/art/thumbs/thumb-royal-spoonbill.png
        link: /2020/04/01/royal-spoonbill
  - title: Editorial Illustration
    images:
    - title: Alonzo and Lambda
      src: /assets/pages/art/thumbs/thumb-alonzo_and_lambda_by_kinow-d5tqvau.png
      link: /2020/03/27/alonzo-and-lambda
  - title: Figurative Drawing
    images:
    - title: Auckland CBD Life Drawing 2021-02-22
      src: /assets/pages/art/thumbs/thumb-251.png
      link: /2021/02/20/auckland-cbd-life-drawing-2021-02-20
    - title: Auckland CBD Life Drawing 2021-01-18
      src: /assets/pages/art/thumbs/thumb-196.png
      link: /2021/01/18/auckland-cbd-life-drawing-2021-01-18
  - title: Observational Drawing
    images:
    - title: Simone
      src: /assets/pages/art/thumbs/thumb-simone.png
      link: /2020/04/01/simone
    - title: Rocky
      src: /assets/pages/art/thumbs/thumb-rocky.png
      link: /2020/09/23/rocky
    - title: Obachan
      src: /assets/pages/art/thumbs/thumb-obachan.png
      link: /2020/03/31/obachan
    - title: Old hands
      src: /assets/pages/art/thumbs/thumb-old-hands.png
      link: /2020/04/03/old-hands
    - title: O Corvo
      src: /assets/pages/art/thumbs/thumb-o-corvo.png
      link: /2020/04/01/o-corvo
    - title: Stink bug
      src: /assets/pages/art/thumbs/thumb-stink-bug-smaller.png
      link: /2020/04/03/stink-bug
  - title: Sketchbook
    notes: |
      Mainly cretacolor pencils, bic, pentel brush, staedtler pigment
      liners, mixed media (gouache, watercolor, pastels), and digital
      with Krita, GIMP, Blender, and Clip Studio Paint.
    images:
    - title: Lola
      src: /assets/pages/art/thumbs/thumb-lola.png
      link: /2020/10/11/lola
    - title: A baby
      src: /assets/pages/art/thumbs/thumb-baby-02.png
      link: /2019/12/30/a-baby
    - title: Grumman F-14 Tomcat
      src: /assets/pages/art/thumbs/thumb-plane1.png
      link: /2020/03/28/plane1
---

{%- for section in page.gallery -%}

## {{ section.title }}

<div class="note">{{ section.notes }}</div>

<div class="gallery">
  {%- for image in section.images -%}
  <figure>
    <img src="{{ image.src | relative_url }}" alt="{{ image.title }}">
    <figcaption>
      <span class="title">{{ image.title }}</span>
      <a href="{{ image.link | relative_url }}">View</a>
    </figcaption>
  </figure>
  {%- endfor -%}
</div>

{%- endfor -%}
