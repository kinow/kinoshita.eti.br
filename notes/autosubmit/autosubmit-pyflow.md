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
        with Family(start_date, START_DATE=start_date) as fsd:
            for member in members:
                with Family(member) as m:
                    ini = Task('INI', START_DATE=start_date, MEMBER=member)
                    ini.triggers = s.REMOTE_SETUP.complete
                    for chunk in chunks:
                        with Family(str(chunk)) as c:
                            sim = Task('SIM', START_DATE=start_date, MEMBER=member, CHUNK=str(chunk))
                            if chunk == 1:
                                dependency = Trigger(f'{ini.fullname} eq complete')
                            else:
                                dependency = Trigger(f'{m.fullname}/{str(chunk - 1)}/SIM eq complete')
                            sim.add_node(dependency)

                            gsv = Task('GSV', START_DATE=start_date, MEMBER=member, CHUNK=str(chunk))
                            gsv.triggers = Trigger(f'{sim.fullname} eq complete')

                            app = Task('APPLICATION', START_DATE=start_date, MEMBER=member, CHUNK=str(chunk))
                            app.triggers = Trigger(f'{gsv.fullname} eq complete')

s.replace_on_server(host='localhost', port=3141)
```

Screenshots of the suite loaded in `ecflow_ui`:

![image](https://user-images.githubusercontent.com/304786/204066040-0e60a3ca-4262-4374-9819-35d19bef9cc8.png)

![image](https://user-images.githubusercontent.com/304786/204066051-47712270-df66-4841-996e-9881925d789e.png)

![image](https://user-images.githubusercontent.com/304786/204066077-1e9afd83-bd32-4c0e-b9c7-bc518714b97d.png)

![image](https://user-images.githubusercontent.com/304786/204084149-e2d04192-29bd-4b56-846f-95ba557bfd06.png)

