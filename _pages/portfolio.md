---
title: Portfolio
layout: page
permalink: "/portfolio/"
gallery:
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
    - title: Sepia dry and sepia oil figurative drawing
      src: /assets/pages/art/thumbs/thumb-251.png
      link: /2021/02/20/figure-drawing-with-sepia-line-of-action
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
    images:
    - title: Lola
      src: /assets/pages/art/thumbs/thumb-lola.png
      link: /2020/10/11/lola
    - title: A baby
      src: /assets/pages/art/thumbs/thumb-baby-02.png
      link: /2019/12/30/a-baby
---

{%- for section in page.gallery -%}

## {{ section.title }}

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
