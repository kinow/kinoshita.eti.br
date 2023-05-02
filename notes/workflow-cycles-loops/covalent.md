Before starting Covalent.

WIP

## Networking note

```bash
(venv) (base) kinow@ranma:~/Development/python/workspace/covalent$ netstat -tlnp
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp6       0      0 ::1:631                 :::*                    LISTEN      -  
```

After:

```bash
(venv) (base) kinow@ranma:~/Development/python/workspace/covalent$ covalent start
Covalent server has started at http://localhost:48008
(venv) (base) kinow@ranma:~/Development/python/workspace/covalent$ netstat -tlnp
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:50513         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 127.0.0.1:42479         0.0.0.0:*               LISTEN      43457/python        
tcp        0      0 0.0.0.0:35807           0.0.0.0:*               LISTEN      43452/python        
tcp        0      0 0.0.0.0:35723           0.0.0.0:*               LISTEN      43463/python        
tcp        0      0 0.0.0.0:34885           0.0.0.0:*               LISTEN      43472/python        
tcp        0      0 127.0.0.1:33103         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 0.0.0.0:36511           0.0.0.0:*               LISTEN      43454/python        
tcp        0      0 127.0.0.1:41047         0.0.0.0:*               LISTEN      43460/python        
tcp        0      0 127.0.0.1:41783         0.0.0.0:*               LISTEN      43466/python        
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:44383           0.0.0.0:*               LISTEN      43457/python        
tcp        0      0 0.0.0.0:8787            0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 127.0.0.1:35941         0.0.0.0:*               LISTEN      43454/python        
tcp        0      0 127.0.0.1:35849         0.0.0.0:*               LISTEN      43463/python        
tcp        0      0 127.0.0.1:36469         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 127.0.0.1:36573         0.0.0.0:*               LISTEN      43472/python        
tcp        0      0 127.0.0.1:43067         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 0.0.0.0:42785           0.0.0.0:*               LISTEN      43460/python        
tcp        0      0 127.0.0.1:43619         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 127.0.0.1:35405         0.0.0.0:*               LISTEN      43470/python        
tcp        0      0 127.0.0.1:46113         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 127.0.0.1:37303         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 127.0.0.1:45677         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 127.0.0.1:45701         0.0.0.0:*               LISTEN      43452/python        
tcp        0      0 0.0.0.0:45691           0.0.0.0:*               LISTEN      43470/python        
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:38959         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 0.0.0.0:46875           0.0.0.0:*               LISTEN      43466/python        
tcp        0      0 127.0.0.1:39911         0.0.0.0:*               LISTEN      43442/python        
tcp        0      0 127.0.0.1:48008         0.0.0.0:*               LISTEN      43441/python        
tcp6       0      0 :::35807                :::*                    LISTEN      43452/python        
tcp6       0      0 :::35723                :::*                    LISTEN      43463/python        
tcp6       0      0 :::34885                :::*                    LISTEN      43472/python        
tcp6       0      0 :::36511                :::*                    LISTEN      43454/python        
tcp6       0      0 ::1:631                 :::*                    LISTEN      -                   
tcp6       0      0 :::44383                :::*                    LISTEN      43457/python        
tcp6       0      0 :::8787                 :::*                    LISTEN      43442/python        
tcp6       0      0 :::42785                :::*                    LISTEN      43460/python        
tcp6       0      0 :::45691                :::*                    LISTEN      43470/python        
tcp6       0      0 :::46875                :::*                    LISTEN      43466/python 
```

