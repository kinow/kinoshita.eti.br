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
  PREINI:
    FILE: templates/ini.sh
    DEPENDENCIES: REMOTE_SETUP
    RUNNING: member
    WALLCLOCK: '00:05'
  INI:
    FILE: templates/ini.sh
    DEPENDENCIES: PREINI
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

![image]![image](https://user-images.githubusercontent.com/304786/210076708-0313573b-f70c-4434-a5dd-b7a9bd08bd82.png)

## PyFlow 3 (outdated)

This was the initial prototype, manually creating a PyFlow suite from looking at the previous experiment configuration.
Skip to the next section to the up to date solution.

```py
import os
from pwd import getpwuid

from pyflow import *
import pyflow as pf

scratchdir = os.path.join(os.path.abspath(''), 'scratch')
filesdir = os.path.join(scratchdir, 'files')
outdir = os.path.join(scratchdir, 'out')

if not os.path.exists(filesdir):
    os.makedirs(filesdir, exist_ok=True)

if not os.path.exists(outdir):
    os.makedirs(outdir, exist_ok=True)

passwd = getpwuid(os.getuid())

server_host = 'localhost'
server_port = 3141

with Suite('a000', files=filesdir, home=outdir, defstatus=pf.state.suspended) as s:
    local_setup = Task('LOCAL_SETUP', script='templates/local_setup.sh')
    synchronize = Task('SYNCHRONIZE', script='templates/synchronize.sh')
    synchronize.triggers = s.LOCAL_SETUP.complete
    remote_setup = Task('REMOTE_SETUP', script='templates/remote_setup.sh')
    remote_setup.triggers = s.SYNCHRONIZE.complete

    start_dates = ['20220401', '20220402']
    members = ['fc0']
    chunks = [1, 2]

    for start_date in start_dates:
        with Family(name=start_date, START_DATE=start_date) as fsd:
            for member in members:
                with Family(member, MEMBER=member) as m:
                    ini = Task('INI', script='templates/ini.sh')
                    ini.triggers = s.REMOTE_SETUP.complete
                    for chunk in chunks:
                        with Family(str(chunk), CHUNK=str(chunk)) as c:
                            sim = Task('SIM', script='templates/sim.sh')
                            if chunk == 1:
                                dependency = Trigger(f'{ini.fullname} eq complete')
                            else:
                                dependency = Trigger(f'{m.fullname}/{str(chunk - 1)}/SIM eq complete')
                            sim.add_node(dependency)

                            gsv = Task('GSV', script='templates/gsv.sh')
                            gsv.triggers = Trigger(f'{sim.fullname} eq complete')

                            app = Task('APPLICATION', script='templates/application.sh')
                            app.triggers = Trigger(f'{gsv.fullname} eq complete')

print(s)
s.deploy_suite(overwrite=True)
# s.replace_on_server(server_host, server_port)
```

Screenshots of the suite loaded in `ecflow_ui`:

![image](https://user-images.githubusercontent.com/304786/204066040-0e60a3ca-4262-4374-9819-35d19bef9cc8.png)

![image](https://user-images.githubusercontent.com/304786/204066051-47712270-df66-4841-996e-9881925d789e.png)

![image](https://user-images.githubusercontent.com/304786/204066077-1e9afd83-bd32-4c0e-b9c7-bc518714b97d.png)

![image](https://user-images.githubusercontent.com/304786/204084149-e2d04192-29bd-4b56-846f-95ba557bfd06.png)

*After adding the scripts from a vanilla Autosubmit workflow:*

![image](https://user-images.githubusercontent.com/304786/204587724-58e51b86-1724-4435-aa79-dc6851cb2e9c.png)

### ecFlow suite definition

Exported from PyFlow configuration.

```
suite a000
  defstatus suspended
  edit ECF_FILES '/home/bdepaula/Development/python/workspace/pyflow/scratch/files'
  edit ECF_HOME '/home/bdepaula/Development/python/workspace/pyflow/scratch/out'
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

## `autosubmit2pyflow.py`

**NOTE**: Work in progress.

This script reads Autosubmit experiments configuration using the
[`autosubmitconfigparser`](https://pypi.org/project/autosubmitconfigparser/)
library, expands the workflow graph, plots and creates a PyFlow suite.

The goal is to produce the PyFlow workflow using Autosubmit experiment configuration,
creating a compatible workflow.

To Do:

- [x] Read configuration
- [x] Expand workflow graph, including dependencies (i.e. instead of `INI -> SIM`, we need the actual tasks like `a000_INI -> a000_20200401_SIM`, etc.)
- [x] Iterate the workflow in topological order (i.e. from bottom down, in-order - lexical?)
- [ ] Produce equivalent graph in AS & PyFlow (very close, need to confirm something with Dani & Miguel about dependencies)
- [x] Plot the workflow graph to compare with Autosubmit's plot (using `dot`)
- [ ] Augment the PyFlow suite with all the available configuration (i.e. all the variables from experiment) (shouldn't be too hard, need Dani's help)
- [ ] Produce equivalent execution in AS & PyFlow (a little harder to confirm, will need Miguel and Dani's help)
- [ ] Polish the code (better documentation, store in a better repository or integrate into AS4, write tests, etc.)

```py
import argparse
import sys
from collections import defaultdict
from enum import Enum
from itertools import groupby
from typing import List, Dict, Any, TypedDict, Union
import re

import networkx as nx
from autosubmitconfigparser.config.configcommon import AutosubmitConfig
from pyflow import *


def _create_task(task_obj: Dict[str, Any], suite: Suite) -> Task:
    task = Task(task_obj['NAME'])
    return task


class Running(Enum):
    ONCE = 'once'
    MEMBER = 'member'
    CHUNK = 'chunk'
    SPLIT = 'split'

    def __str__(self):
        return self.value


class DependencyData(TypedDict):
    ID: str
    NAME: str
    RUNNING: Running


class JobData(TypedDict):
    ID: str
    NAME: str
    FILE: str
    DEPENDENCIES: Dict[str, DependencyData]
    RUNNING: str
    WALLCLOCK: str
    ADDITIONAL_FILES: List[str]


def create_ecflow_suite(*,
                        experiment_id: str,
                        start_dates: List[str],
                        members: List[str],
                        chunks: [int],
                        jobs: Dict[str, Dict[str, JobData]],
                        by_running: Dict[str, List[JobData]]) -> Suite:
    """Replicate the vanilla workflow graph structure."""
    with Suite(experiment_id) as s:
        for task_obj in by_running['by_running']['once']:
            _create_task(task_obj, s)

        # start_dates = ['20220401', '20220402']
        # members = ['fc0']
        # chunks = [1, 2]

        for start_date in start_dates:
            with Family(start_date, START_DATE=start_date):  # type: ignore
                for member in members:
                    with Family(member) as m:
                        for task_obj in jobs['member']:
                            task = Task(task_obj['NAME'], START_DATE=start_date, MEMBER=member)  # type: ignore
                            ini.triggers = s.REMOTE_SETUP.complete
                        for chunk in chunks:
                            with Family(str(chunk)):
                                sim = Task('SIM', START_DATE=start_date, MEMBER=member,
                                           CHUNK=str(chunk))  # type: ignore
                                if chunk == 1:
                                    dependency = Trigger(f'{ini.fullname} eq complete')
                                else:
                                    dependency = Trigger(f'{m.fullname}/{str(chunk - 1)}/SIM eq complete')
                                sim.add_node(dependency)

                                gsv = Task('GSV', START_DATE=start_date, MEMBER=member,
                                           CHUNK=str(chunk))  # type: ignore
                                gsv.triggers = Trigger(f'{sim.fullname} eq complete')

                                app = Task('APPLICATION', START_DATE=start_date, MEMBER=member,
                                           CHUNK=str(chunk))  # type: ignore
                                app.triggers = Trigger(f'{gsv.fullname} eq complete')
        return s


DEFAULT_SEPARATOR = '_'


def _create_job_id(
        *,
        expid: str,
        name: str,
        start_date: Union[str, None] = None,
        member: Union[str, None] = None,
        chunk: Union[str, None] = None,
        split: Union[str, None] = None,
        separator=DEFAULT_SEPARATOR) -> str:
    if not expid or not name:
        raise ValueError('You must provide valid expid and job name')
    return separator.join([token for token in filter(None, [expid, start_date, member, chunk, split, name])])


def _create_job(
        *,
        expid: str,
        name: str,
        start_date: Union[str, None] = None,
        member: Union[str, None] = None,
        chunk: Union[int, None] = None,
        split: Union[str, None] = None,
        separator=DEFAULT_SEPARATOR,
        job_data: JobData,
        jobs_data: Dict[str, JobData]) -> JobData:
    chunk_str = None if chunk is None else str(chunk)
    job_id = _create_job_id(
        expid=expid,
        name=name,
        member=member,
        chunk=chunk_str,
        split=split,
        separator=separator,
        start_date=start_date)
    job = {'ID': job_id, **job_data.copy()}
    job['DEPENDENCIES'] = {}
    for dependency in job_data['DEPENDENCIES']:
        # once jobs can only have dependencies on other once jobs
        job_dependency = _create_dependency(
            dependency_name=dependency,
            jobs_data=jobs_data,
            expid=expid,
            start_date=start_date,
            member=member,
            chunk=chunk,
            split=split)
        # certain dependencies do not produce an object, e.g.
        # - SIM-1 if SIM is not RUNNING=chunk, or
        # - SIM-1 if current chunk is 1 (or 1 - 1 = 0)
        if job_dependency:
            job['DEPENDENCIES'][dependency] = job_dependency
    return job


def _create_dependency(
        dependency_name: str,
        jobs_data: Dict[str, JobData],
        expid: str,
        start_date: Union[str, None] = None,
        member: Union[str, None] = None,
        chunk: Union[int, None] = None,
        split: Union[str, None] = None) -> Union[DependencyData, None]:
    """Create a ``DependencyData`` object.

    The dependency created will have a field ``ID`` with the expanded dependency ID."""
    dependency_member = None
    dependency_start_date = None
    dependency_chunk = None

    m = re.search('([a-zA-Z0-9_\-\.]+)-([\d]+)', dependency_name)
    if m:
        if chunk is None:
            # We ignore if this syntax is used outside a running=chunk (same behaviour as AS?).
            return None
        dependency_name = m.group(1)
        previous_chunk = int(m.group(2))
        if chunk - previous_chunk < 1:
            # We ignore -1 when the chunk is 1 (i.e. no previous chunk).
            return None
        dependency_chunk = str(previous_chunk)
    dependency_data = jobs_data[dependency_name]
    if dependency_data['RUNNING'] == Running.MEMBER.value:
        # if not a member dependency, then we do not add the start date and member (i.e. it is a once dependency)
        dependency_member = member
        dependency_start_date = start_date
    elif dependency_data['RUNNING'] == Running.CHUNK.value:
        dependency_member = member
        dependency_start_date = start_date
        if dependency_chunk is None:
            dependency_chunk = str(chunk)
    # TODO: split
    dependency_id = _create_job_id(
        expid=expid,
        name=dependency_name,
        member=dependency_member,
        chunk=dependency_chunk,
        start_date=dependency_start_date)
    return {'ID': dependency_id, **dependency_data}


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='autosubmit2pyflow',
        description='Produces a valid PyFlow workflow configuration given an Autosubmit experiment ID',
        epilog='This program needs access to an Autosubmit installation'
    )
    parser.add_argument('-e', '--experiment', required=True, help='Autosubmit experiment ID')
    parser.add_argument('-s', '--server', default='localhost', help='ecFlow server hostname or IP')
    parser.add_argument('-p', '--port', default=3141, help='ecFlow server port')
    parser.add_argument('-d', '--deploy', default=False, help='Whether to deploy to ecFlow or not')
    parser.add_argument('-q', '--quiet', default=False, action='store_true')

    args = parser.parse_args()

    # Init the configuration object where expid = experiment identifier that you want to load
    as_conf = AutosubmitConfig(args.experiment)
    # This will load the data from the experiment
    as_conf.reload(True)

    # experiment configuration
    expid = args.experiment
    start_dates = as_conf.experiment_data['EXPERIMENT']['DATELIST'].split(' ')
    members = as_conf.experiment_data['EXPERIMENT']['MEMBERS'].split(' ')
    chunks = [i for i in range(1, as_conf.experiment_data['EXPERIMENT']['NUMCHUNKS'] + 1)]

    # place the NAME attribute in the job object
    jobs_data: Dict[str, JobData] = {
        job_data[0]: {'NAME': job_data[0], **job_data[1]}
        for job_data in as_conf.jobs_data.items()}

    # Create a list of jobs
    jobs_list: List[JobData] = list(jobs_data.values())
    jobs_grouped_by_running_level: Dict[str, List[JobData]] = defaultdict(list)
    jobs_grouped_by_running_level.update(
        {job[0]: list(job[1]) for job in groupby(jobs_list, lambda item: item['RUNNING'])})

    # Expand jobs (by member, chunk, split, previous-dependency like SIM-1)
    # That's because the graph declaration in Autosubmit configuration contains
    # a meta graph, that is expanded by each hierarchy level generating
    # more jobs (i.e. SIM may become a000_202204_fc0_1_SIM for running=chunk).
    jobs: List[JobData] = []
    for running in Running:
        for job_running in jobs_grouped_by_running_level[running.value]:
            if running == Running.ONCE:
                jobs.append(_create_job(
                    expid=expid,
                    name=job_running['NAME'],
                    job_data=job_running,
                    jobs_data=jobs_data))
            else:
                for start_date in start_dates:
                    if running == Running.MEMBER:
                        for member in members:
                            jobs.append(_create_job(
                                expid=expid,
                                name=job_running['NAME'],
                                member=member,
                                start_date=start_date,
                                job_data=job_running,
                                jobs_data=jobs_data))
                    elif running == Running.CHUNK:
                        for member in members:
                            for chunk in chunks:
                                jobs.append(_create_job(
                                    expid=expid,
                                    name=job_running['NAME'],
                                    member=member,
                                    chunk=chunk,
                                    start_date=start_date,
                                    job_data=job_running,
                                    jobs_data=jobs_data))
                    # TODO: split
                    else:
                        # TODO: implement splits and anything else?
                        raise NotImplementedError(running)

    # Create networkx graph
    G = nx.DiGraph()
    for job in jobs:
        G.add_node(job['ID'])
        for dep in job['DEPENDENCIES'].values():
            G.add_edges_from([(dep['ID'], job['ID'])])
    # Create topological sort.
    jobs_ordered = list(list(nx.topological_sort(G)))

    # print(jobs_ordered)
    # print()
    # print([f'{job["ID"]}, deps: {job["DEPENDENCIES"]}' for job in jobs])
    # print(as_conf.experiment_data)
    print(jobs_ordered)
    PG = nx.nx_pydot.to_pydot(G)
    print(PG)
    if 'bla' not in args:
        return

    # TODO: job splits
    # TODO: raise an error for unsupported features, like SKIPPABLE?
    suite = create_ecflow_suite(experiment_id=expid, start_dates=start_dates, members=members, chunks=chunks)

    if not args.quiet:
        print(suite)

    if args.deploy:
        suite.replace_on_server(host=args.hostname, port=args.port)

    sys.exit(0)


if __name__ == '__main__':
    main()

```

Current graph:

[URL](https://dreampuf.github.io/GraphvizOnline/#strict%20digraph%20%20%7B%0Aa000_LOCAL_SETUP%3B%0Aa000_SYNCHRONIZE%3B%0Aa000_REMOTE_SETUP%3B%0Aa000_20220401_fc0_PREINI%3B%0Aa000_20220402_fc0_PREINI%3B%0Aa000_20220401_fc0_INI%3B%0Aa000_20220402_fc0_INI%3B%0Aa000_20220401_fc0_1_SIM%3B%0Aa000_20220401_fc0_2_SIM%3B%0Aa000_20220402_fc0_1_SIM%3B%0Aa000_20220402_fc0_2_SIM%3B%0Aa000_20220401_fc0_1_GSV%3B%0Aa000_20220401_fc0_2_GSV%3B%0Aa000_20220402_fc0_1_GSV%3B%0Aa000_20220402_fc0_2_GSV%3B%0Aa000_20220401_fc0_1_APPLICATION%3B%0Aa000_20220401_fc0_2_APPLICATION%3B%0Aa000_20220402_fc0_1_APPLICATION%3B%0Aa000_20220402_fc0_2_APPLICATION%3B%0Aa000_LOCAL_SETUP%20-%3E%20a000_SYNCHRONIZE%3B%0Aa000_SYNCHRONIZE%20-%3E%20a000_REMOTE_SETUP%3B%0Aa000_REMOTE_SETUP%20-%3E%20a000_20220401_fc0_PREINI%3B%0Aa000_REMOTE_SETUP%20-%3E%20a000_20220402_fc0_PREINI%3B%0Aa000_20220401_fc0_PREINI%20-%3E%20a000_20220401_fc0_INI%3B%0Aa000_20220402_fc0_PREINI%20-%3E%20a000_20220402_fc0_INI%3B%0Aa000_20220401_fc0_INI%20-%3E%20a000_20220401_fc0_1_SIM%3B%0Aa000_20220401_fc0_INI%20-%3E%20a000_20220401_fc0_2_SIM%3B%0Aa000_20220402_fc0_INI%20-%3E%20a000_20220402_fc0_1_SIM%3B%0Aa000_20220402_fc0_INI%20-%3E%20a000_20220402_fc0_2_SIM%3B%0Aa000_20220401_fc0_1_SIM%20-%3E%20a000_20220401_fc0_2_SIM%3B%0Aa000_20220401_fc0_1_SIM%20-%3E%20a000_20220401_fc0_1_GSV%3B%0Aa000_20220401_fc0_2_SIM%20-%3E%20a000_20220401_fc0_2_GSV%3B%0Aa000_20220402_fc0_1_SIM%20-%3E%20a000_20220402_fc0_2_SIM%3B%0Aa000_20220402_fc0_1_SIM%20-%3E%20a000_20220402_fc0_1_GSV%3B%0Aa000_20220402_fc0_2_SIM%20-%3E%20a000_20220402_fc0_2_GSV%3B%0Aa000_20220401_fc0_1_GSV%20-%3E%20a000_20220401_fc0_1_APPLICATION%3B%0Aa000_20220401_fc0_2_GSV%20-%3E%20a000_20220401_fc0_2_APPLICATION%3B%0Aa000_20220402_fc0_1_GSV%20-%3E%20a000_20220402_fc0_1_APPLICATION%3B%0Aa000_20220402_fc0_2_GSV%20-%3E%20a000_20220402_fc0_2_APPLICATION%3B%0A%7D%0A)

![graphviz](https://user-images.githubusercontent.com/304786/210077573-39f5d2fe-958f-4d12-99a0-0d5c0b8866e3.svg)

