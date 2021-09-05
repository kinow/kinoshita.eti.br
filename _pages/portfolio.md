---
title: Portfolio
layout: page
permalink: "/portfolio/"
gallery:
  - title: Digital Drawing
    notes: |
      Inkspace, Clip Studio Paint, Krita, GIMP.
    images:
      - title: Low poly in Inkscape
        src: /assets/pages/art/thumbs/thumb-low-poly-01.png
        link: /2021/03/11/low-poly-in-inkscape
      - title: Rooster
        src: /assets/pages/art/thumbs/thumb-FRANGO.png
        link: /2021/02/07/rooster
  - title: Editorial Illustration
    notes: |
      Graphite, ink brush, colored pencils, Inkscape, Krita, Clip Studio Paint
    images:
      - title: Alonzo and Lambda for r/functionalprogramming subreddit
        src: /assets/pages/art/thumbs/thumb-alonzo_and_lambda_by_kinow-d5tqvau.png
        link: /2020/03/27/alonzo-and-lambda
      - title: Bezerra da Silva for Speak Like A Brazilian
        src: /assets/pages/art/thumbs/thumb-bezerra-03.png
        link: /2021/03/27/bezerra-da-silva
  - title: Logos
    notes: |
      Inkscape, Blender, or Adobe Illustrator.
    images:
      - title: Apache OpenNLP
        src: /assets/pages/art/thumbs/thumb-opennlp-1.png
        link: /2017/04/21/apache-opennlp-logo
      - title: Frege Programming Language
        src: /assets/pages/art/thumbs/thumb-frege-2.png
        link: /2016/08/24/revamping-frege-logo-part-2
      - title: TupiLabs
        src: /assets/pages/art/thumbs/thumb-tupilabs-1.png
        link: /2012/02/02/tupilabs-logo
      - title: Yandê
        src: /assets/pages/art/thumbs/thumb-yande-1.png
        link: /2021/03/07/yande-paes-logo
  - title: Paintings
    notes: |
      Watercolors, gouache, colored pencils, and digital (Krita, Clip Studio Paint).
    images:
      - title: Green Skull
        src: /assets/pages/art/thumbs/thumb-green-skull-full.png
        link: /2020/04/03/green-skull
      - title: Royal Spoonbill
        src: /assets/pages/art/thumbs/thumb-royal-spoonbill.png
        link: /2020/04/01/royal-spoonbill
      - title: Tufted Titmouse
        src: /assets/pages/art/thumbs/thumb-tufted-titmouse.png
        link: /2021/04/05/tufted-titmouse
      - title: Random Traffic Light
        src: /assets/pages/art/thumbs/thumb-random-traffic-light.png
        link: /2021/04/06/random-traffic-light
  - title: Figurative Drawing
    notes: |
      Charcoal, sepia, graphite, ink brush.
    images:
    - title: Auckland CBD Life Drawing 2021-01-18
      src: /assets/pages/art/thumbs/thumb-196.png
      link: /2021/01/18/auckland-cbd-life-drawing-2021-01-18
    - title: Auckland CBD Life Drawing 2021-02-01
      src: /assets/pages/art/thumbs/thumb-230.png
      link: /2021/02/01/auckland-cbd-life-drawing-2021-02-01#1
    - title: Auckland CBD Life Drawing 2021-02-01
      src: /assets/pages/art/thumbs/thumb-231.png
      link: /2021/02/01/auckland-cbd-life-drawing-2021-02-01#2
    - title: Auckland CBD Life Drawing 2021-02-01
      src: /assets/pages/art/thumbs/thumb-232.png
      link: /2021/02/01/auckland-cbd-life-drawing-2021-02-01#3
    - title: Auckland CBD Life Drawing 2021-02-01
      src: /assets/pages/art/thumbs/thumb-233.png
      link: /2021/02/01/auckland-cbd-life-drawing-2021-02-01#4
    - title: Auckland CBD Life Drawing 2021-02-01
      src: /assets/pages/art/thumbs/thumb-234.png
      link: /2021/02/01/auckland-cbd-life-drawing-2021-02-01#5
    - title: Figurative drawing Line of Action 2021-02-22
      src: /assets/pages/art/thumbs/thumb-251.png
      link: /2021/02/20/figurative-drawing-line-of-action-2021-02-20
    - title: Figurative drawing Line of Action 2021-03-11
      src: /assets/pages/art/thumbs/thumb-255.png
      link: /2021/03/11/figurative-drawing-line-of-action-2021-03-11
  - title: Observational Drawing
    notes: |
      Charcoal, graphite, ink brush.
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