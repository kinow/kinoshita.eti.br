---
date: 2009-03-06 12:10:07 +1300
layout: post
tags:
- java
categories:
- blog
title: Displaying Japanese characters in Java Swing
---

It's not as complicated as I first thought.

Had to use this technique to develop an Swing application for the JLPT certification exam.

```java
public static void main(String[] args) {
	JFrame frame = new JFrame();
	frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	Container container = frame.getContentPane();
	JLabel japanese = new JLabel( "Kino\u304D\u306E" );
	japanese.setToolTipText( "This is Japanese" );
	Font f = new Font("Arial Unicode MS", Font.BOLD, 16);
	japanese.setFont(f);
	container.add( japanese );
	frame.pack();
	frame.setLocationRelativeTo(null);
	frame.setVisible(true);
}
```

All you have to do is to use the hexadecimal representation of the characters instead of using plain text. And here is the result.

{{ page.date }}

<img class="ui image" src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/kino.png" alt="=" />

Banzai!
