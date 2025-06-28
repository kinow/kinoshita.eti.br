---
title: "Migrating the Jena editor from CodeMirror 5 to 6"
date: 2025-06-25T09:38:52+03:00
categories:
  - blog
tags:
  - opensource
  - javascript
  - programming
images:
  - '/assets/posts/2025-06-28-migrating-the-jena-editor-from-codemirror-5-to-6/01.png'
---

On October last year, Dependabot's bot sent Apache Jena [a pull request](https://github.com/apache/jena/pull/2789)
to update CodeMirror (a code editor component for web) to from our current 5.x version
to 6.0.1. The build failed, as there were breaking changes in the CodeMirror
API going from 5.x to 6.x.

CodeMirror developers wrote a nice documentation for users to
[migrate and update their code](https://codemirror.net/docs/migration/).

After following their documentation, unfortunately there were still build
errors. Several months later, I found myself on a Saturday afternoon in
a room struggling with the first heat wave in Barcelona this year, and
decided to cool down by writing some code under the ceiling fan.

## Turtle (ttl)

The first problem I had was that the turtle language syntax was not
available. The solution for that problem was to use the
[codemirror-lang-turtle](https://www.npmjs.com/package/codemirror-lang-turtle).

{{< showimage
    image="01.png"
    alt="Using new turtle library codemirror-lang-turtle"
    caption="Using new turtle library codemirror-lang-turtle"
    style="width: auto;"
>}}

## `cm.scrollTo` and `cm.getScrollInfo` are gone

I could not find anything in the `codemirror/view` repository (searched
code and issues), nor on the CodeMirror website. But after testing a bit
the new code, I realized that dispatching the change to update the text
content resulted in the new text appearing in the editor without any
issues to the scroll bar.

So I just removed those lines (for now, at least).

{{< showimage
    image="02.png"
    alt="Delete scroll-bar-related code"
    caption="Delete scroll-bar-related code"
    style="width: auto;"
>}}

## No `.on` to watch for `change` events in CodeMirror view element

Previously, we had some code that called `.on('change', ...)` on the
`cm` object, to listen for the events and sync it with our Vue elements.

That one would have been very hard (or at least very boring) problem to fix,
but thankfully [somebody else had already found it](https://discuss.codemirror.net/t/listen-to-change-event/5095).
The user message was also showing that I would have to call that method directly
on `EditorView`, and not on the `cm` instance (must be quite interesting
how they hook that up, global objects and all).

{{< showimage
    image="03.png"
    alt="Using EditorView.updateListener instead of on('change', ...)"
    caption="Using EditorView.updateListener instead of on('change', ...)"
    style="width: auto;"
>}}

## e2e test cannot locate `.CodeMirror-code`

The tests in Jena UI are written with Cypress, which works similarly to
Selenium. Elements are located by selectors like CSS classes. The only remaining
test failure was due to an element selected by `.CodeMirror-code` that was
not found.

So I fired the UI in offline mode -- something I have always available when I
work in frontend projects -- and checked the new CSS class: `.cm-content`.
Changed that, and the test passed! 🎉

{{< showimage
    image="04.png"
    alt="Last fix, using the right CSS class"
    caption="Last fix, using the right CSS class"
    style="width: auto;"
>}}

Now the code is ready for review, and hopefully it will work well when it is
included in a future release of Jena -- fingers crossed for that! 🤞
