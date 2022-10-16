---
categories:
- blog
date: "2009-03-22T00:00:00Z"
tags:
- c++
title: Code to change your message in MSN messenger
---

I've always wanted to know how does the code to show what was I listening to looked like. I found it after installing XMPlay and XMPlay MSN Plug-in. The plug-in zip had the plug-in itself and its source code. And what a neat source code (-:.

Basically, you just send a message to the MSN UI API with a defined data structure. And to remove the message, just send again with an empty string.

```c
/*
Bruno de Paula Kinoshita
original src code:
XMPlay MSN Plugin (c) 2005-2006 Elliott Sales de Andrade
*/

#include <cstdlib>
#include <iostream>
#include <windows.h>

using namespace std;

typedef struct {
BOOL showCues;
BOOL keepOnClose;
} MSNStuff;
static MSNStuff msnConf;

void setNowPlaying( char *title)
{
    wchar_t *lpMsn;
    int strLen = 20;
    HWND xmpwin;
    HWND msnui=0;
    
    lpMsn = (wchar_t*)calloc(1024,1024);
    // stuff for MSN before...
    memcpy(lpMsn, L&quot;\&#92;&#48;Music\&#92;&#48;1\&#92;&#48;{0}\&#92;&#48;&quot;, 17*2);
    // actual title...
    strLen=MultiByteToWideChar(false?CP_UTF8:CP_ACP,0,title,-1,lpMsn+17,492)-1;Â  /* 1024/2 - 20 */
    // stuff for MSN after...
    memcpy(lpMsn + 17 + strLen, L&quot;\&#92;&#48;&quot;, 3*2);
    strLen += 20;
    
    COPYDATASTRUCT msndata;
    msndata.dwData = 0x547;
    msndata.lpData = (void*)lpMsn;
    msndata.cbData = strLen * 2;
    
    while ( msnui = FindWindowEx(NULL, msnui, &quot;MsnMsgrUIManager&quot;, NULL) )
        SendMessage(msnui, WM_COPYDATA, (WPARAM)xmpwin, (LPARAM)&amp;msndata);
}

int main(int argc, char *argv[])
{
    char *title;
    
    if ( argc == 1 )
        title = &quot;&quot;;
    else
        title = argv[1];
    
    setNowPlaying ( title );
    
    return EXIT_SUCCESS;
}
```
