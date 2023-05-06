Notes about testing Covalent after some discussion in the Workflows Community
Slack channel. These notes are about loops / cycles in Covalent. Unfortunately
looping and cycling sometimes have different meanings (e.g. in Cylc, in ecFlow,
in Autosubmit, in Prefect, in StackStorm, and in many other WfMS' contexts).
So some empirical testing is required in order to understand how well it works
in Covalent, in comparison with other solutions (especially Cylc, where cycling
is one of its main features).

## A task calling itself

```
a -> a
```

That's possible in Covalent.

```py
import covalent as ct

@ct.electron
def a(n=-1):
    return n + 1

@ct.lattice
def run_experiment():
    r1 = a()
    r2 = a(r1)
    return r2

dispatch_id = ct.dispatch(run_experiment)()
result = ct.get_result(dispatch_id, wait=True)
print(result)
```

Produces:

![](./Screenshot&#32;from&#32;2023-05-06&#32;22-55-24.png)

## Cycles

Similar to the previous case, but now the first time `a` runs, that is `a` in cycle `0` (or `1`).
Once `a` is done, a new instance of `a` starts in the next integer cycle. Essentially:

```
a.1 -> a.2 -> a.3 -> ... -> a.N # (or a.INF)
```

That doesn't seem to be possible with Covalent. Here's the example I intuitively
wrote after reading the Covalent documentation:

```py
import covalent as ct
from time import sleep

@ct.electron
def a(cycle=0):
    # TODO: how to get current task name in covalent?
    print(f'This is task "a" cycle "{cycle}"')
    return cycle + 1

@ct.lattice
def run_experiment():
    cycle_result = a()
    while True:
        # The idea is for a to call itself, and then update
        # its cycle point. Looks like the returned object is
        # important, and mutating cycle_result is probably not
        # a good idea/practice (more likely a bug/error).
        cycle_result = a(cycle_result)
        sleep(2)
    return cycle_result

dispatch_id = ct.dispatch(run_experiment)()
result = ct.get_result(dispatch_id, wait=False)
print(result)
```

Running this code results in no output in the console, and nothing in the Covalent UI.
Covalent UI seems to require the `get_result` call to complete in order to display
the workflow (maybe the postprocess task tells the UI about the run finished?).

Too many assumptions, so now logging an issue in their repository: https://github.com/AgnostiqHQ/covalent/discussions/1630

## Notes

### Starting the UI

The UI seems to start only when using the PyPI release, and not with the editable version
from Git: https://github.com/AgnostiqHQ/covalent/issues/1629

### Networking note

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

