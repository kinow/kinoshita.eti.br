---
layout: post
tags:
- c++
- krita
- programming
- opensource
categories:
- blog
title: 'Fixing Qt warning "QLayout: Attempting to add QLayout "" to QWidget "", which
  already has a layout"'
---

If you ever started Krita 3.x in your command line, and had a look at the console output,
you may noticed the following warning.

>QLayout: Attempting to add QLayout "" to QWidget "", which already has a layout

Krita recently [announced the release of 3.1.3-alpha-2](https://krita.org/en/item/krita-3-1-3-alpha-released/),
and while testing I saw this warning and
decided to investigate why this warning happens.

There was already
[a similar question posted on StackOverflow](http://stackoverflow.com/a/25451334). And the
best answer's initial paragraph gave me a hint of what to look for.

>When you assign a widget as the parent of a QLayout by passing it into the constructor, the layout is automatically set as the layout for that widget. In your code you are not only doing this, but explicitly calling setlayout(). This is no problem when when the widget passed is the same. If they are different you will get an error because Qt tries to assign the second layout to your widget which has already had a layout set.

So, somewhere in Krita code, there was a a QWidget being created, and layouts
were being added to it more than once. To find where the issue was happening was quite easy. A breakpoint at
[main.cc](https://github.com/KDE/krita/blob/9e2b8c5b07deccd4a616ad7930a91e8cc784a85b/krita/main.cc#L141)
where the application is initialized, then step through a few times, until the message appeared in the
console.

Further investigation led me to the History docker (the one that shows undo steps)
[constructor](https://github.com/KDE/krita/blob/9e2b8c5b07deccd4a616ad7930a91e8cc784a85b/plugins/dockers/historydocker/HistoryDock.cpp#L33).

```c++
    QVBoxLayout *vl = new QVBoxLayout(page); // layout being set to page
    m_undoView = new KisUndoView(this);
    vl->addWidget(m_undoView);
    QHBoxLayout *hl = new QHBoxLayout(page); // layout being set to page again
    hl->addSpacerItem(new QSpacerItem(10, 1,  QSizePolicy::Expanding, QSizePolicy::Fixed));
    m_bnConfigure = new QToolButton(page);
    m_bnConfigure->setIcon(KisIconUtils::loadIcon("configure"));
    connect(m_bnConfigure, SIGNAL(clicked(bool)), SLOT(configure()));
    hl->addWidget(m_bnConfigure);
    vl->addItem(hl);

    setWidget(page);
    setWindowTitle(i18n("Undo History"));
```

Here the QWidget created receives both QHBoxLayout and QVBoxLayout. Again, searching the Internet
a little bit, then came across this post with a good example of a QWidget with
QHBoxLayout and QVBoxLayout. Here's what the constructor looks after the
[patch](https://bugs.kde.org/show_bug.cgi?id=378313)
has been [applied](https://github.com/KDE/krita/commit/1d2343c0cacfb0b105fbe86c2bcef975a09b1041).

```c++
    QVBoxLayout *vl = new QVBoxLayout(page); // layout being set to page
    m_undoView = new KisUndoView(this);
    vl->addWidget(m_undoView);
    QHBoxLayout *hl = new QHBoxLayout();
    hl->addSpacerItem(new QSpacerItem(10, 1,  QSizePolicy::Expanding, QSizePolicy::Fixed));
    m_bnConfigure = new QToolButton(page);
    m_bnConfigure->setIcon(KisIconUtils::loadIcon("configure"));
    connect(m_bnConfigure, SIGNAL(clicked(bool)), SLOT(configure()));
    hl->addWidget(m_bnConfigure);
    vl->addItem(hl);
    vl->addLayout(hl); // horizontal layout added to the vertical layout

    setWidget(page);
    setWindowTitle(i18n("Undo History"));
```

That's it. Learned something new in Qt. Not as important and useful as learning about
[signals and slots](http://doc.qt.io/qt-4.8/signalsandslots.html), but now I can focus
on other warnings in the console output of Krita.

And you? Have you tested [Krita 3.1.3 alpha](https://krita.org/en/item/krita-3-1-3-alpha-released/) already?
What are you waiting for? :-)

&hearts; Open Source
