## Autosubmit 4

Jobs configuration:

```yaml
JOBS:
  LOCAL_SETUP:
    FILE: templates/local_setup.sh
    PLATFORM: LOCAL
    RUNNING: once
  SYNCHRONIZE:
    FILE: templates/synchronize.sh
    DEPENDENCIES: LOCAL_SETUP
    PLATFORM: LOCAL
    RUNNING: once
  REMOTE_SETUP:
    FILE: templates/remote_setup.sh
    DEPENDENCIES: SYNCHRONIZE
    WALLCLOCK: '01:00'
    RUNNING: once
  INI:
    FILE: templates/ini.sh
    DEPENDENCIES: REMOTE_SETUP
    RUNNING: member
    WALLCLOCK: '00:05'
  SIM:
    FILE: templates/sim.sh
    DEPENDENCIES: INI SIM-1
    RUNNING: chunk
    WALLCLOCK: '00:05'
  GSV:
    FILE: templates/gsv.sh
    DEPENDENCIES: SIM
    RUNNING: chunk
    WALLCLOCK: '00:05'
  APPLICATION:
    FILE: templates/application.sh
    DEPENDENCIES: GSV
    RUNNING: chunk
    WALLCLOCK: '00:05'
```

Exp variables

```yaml
experiment:
  DATELIST: 20220401 20220402
  MEMBERS: "fc0"
  CHUNKSIZEUNIT: month
  CHUNKSIZE: 4
  NUMCHUNKS: 2
  CHUNKINI: ''
  CALENDAR: standard
```

Plot:

![image](https://user-images.githubusercontent.com/304786/204065990-319fde71-56d2-4396-9363-b304014956d5.png)

## PyFlow 3

```py
from pyflow import *

with Suite('a000') as s:
    local_setup = Task('LOCAL_SETUP')
    synchronize = Task('SYNCHRONIZE')
    synchronize.triggers = s.LOCAL_SETUP.complete
    remote_setup = Task('REMOTE_SETUP')
    remote_setup.triggers = s.SYNCHRONIZE.complete

    start_dates = ['20220401', '20220402']
    members = ['fc0']
    chunks = [1, 2]

    for start_date in start_dates:
        with Family(name=start_date, START_DATE=start_date) as fsd:
            for member in members:
                with Family(member, MEMBER=member) as m:
                    ini = Task('INI')
                    ini.triggers = s.REMOTE_SETUP.complete
                    for chunk in chunks:
                        with Family(str(chunk), CHUNK=str(chunk)) as c:
                            sim = Task('SIM')
                            if chunk == 1:
                                dependency = Trigger(f'{ini.fullname} eq complete')
                            else:
                                dependency = Trigger(f'{m.fullname}/{str(chunk - 1)}/SIM eq complete')
                            sim.add_node(dependency)

                            gsv = Task('GSV')
                            gsv.triggers = Trigger(f'{sim.fullname} eq complete')

                            app = Task('APPLICATION')
                            app.triggers = Trigger(f'{gsv.fullname} eq complete')

# s.replace_on_server(host='localhost', port=3141)
print(s)
```

Screenshots of the suite loaded in `ecflow_ui`:

![image](https://user-images.githubusercontent.com/304786/204066040-0e60a3ca-4262-4374-9819-35d19bef9cc8.png)

![image](https://user-images.githubusercontent.com/304786/204066051-47712270-df66-4841-996e-9881925d789e.png)

![image](https://user-images.githubusercontent.com/304786/204066077-1e9afd83-bd32-4c0e-b9c7-bc518714b97d.png)

![image](https://user-images.githubusercontent.com/304786/204084149-e2d04192-29bd-4b56-846f-95ba557bfd06.png)

## ecFlow suite definition

```
suite a000
  edit ECF_JOB_CMD 'bash -c 'export ECF_PORT=%ECF_PORT%; export ECF_HOST=%ECF_HOST%; export ECF_NAME=%ECF_NAME%; export ECF_PASS=%ECF_PASS%; export ECF_TRYNO=%ECF_TRYNO%; export PATH=/home/bdepaula/mambaforge/envs/pyflow/bin:$PATH; ecflow_client --init="$$" && %ECF_JOB% && ecflow_client --complete || ecflow_client --abort ' 1> %ECF_JOBOUT% 2>&1 &'
  edit ECF_KILL_CMD 'pkill -15 -P %ECF_RID%'
  edit ECF_STATUS_CMD 'true'
  edit ECF_OUT '%ECF_HOME%'
  label exec_host "default"
  task LOCAL_SETUP
  task SYNCHRONIZE
    trigger LOCAL_SETUP eq complete
  task REMOTE_SETUP
    trigger SYNCHRONIZE eq complete
  family 20220401
    edit START_DATE '20220401'
    family fc0
      edit MEMBER 'fc0'
      task INI
        trigger ../../REMOTE_SETUP eq complete
      family 1
        edit CHUNK '1'
        task SIM
          trigger /a000/20220401/fc0/INI eq complete
        task GSV
          trigger /a000/20220401/fc0/1/SIM eq complete
        task APPLICATION
          trigger /a000/20220401/fc0/1/GSV eq complete
      endfamily
      family 2
        edit CHUNK '2'
        task SIM
          trigger /a000/20220401/fc0/1/SIM eq complete
        task GSV
          trigger /a000/20220401/fc0/2/SIM eq complete
        task APPLICATION
          trigger /a000/20220401/fc0/2/GSV eq complete
      endfamily
    endfamily
  endfamily
  family 20220402
    edit START_DATE '20220402'
    family fc0
      edit MEMBER 'fc0'
      task INI
        trigger ../../REMOTE_SETUP eq complete
      family 1
        edit CHUNK '1'
        task SIM
          trigger /a000/20220402/fc0/INI eq complete
        task GSV
          trigger /a000/20220402/fc0/1/SIM eq complete
        task APPLICATION
          trigger /a000/20220402/fc0/1/GSV eq complete
      endfamily
      family 2
        edit CHUNK '2'
        task SIM
          trigger /a000/20220402/fc0/1/SIM eq complete
        task GSV
          trigger /a000/20220402/fc0/2/SIM eq complete
        task APPLICATION
          trigger /a000/20220402/fc0/2/GSV eq complete
      endfamily
    endfamily
  endfamily
endsuite
```
