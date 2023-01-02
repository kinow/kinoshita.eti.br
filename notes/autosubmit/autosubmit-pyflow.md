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

![image](https://user-images.githubusercontent.com/304786/210076708-0313573b-f70c-4434-a5dd-b7a9bd08bd82.png)

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
  edit ECF_FILES '/home/kinow/Development/python/workspace/autosubmit/scratch/files'
  edit ECF_HOME '/home/kinow/Development/python/workspace/autosubmit/scratch/out'
  edit ECF_JOB_CMD 'bash -c 'export ECF_PORT=%ECF_PORT%; export ECF_HOST=%ECF_HOST%; export ECF_NAME=%ECF_NAME%; export ECF_PASS=%ECF_PASS%; export ECF_TRYNO=%ECF_TRYNO%; export PATH=/home/kinow/mambaforge/envs/pyflow/bin:$PATH; ecflow_client --init="$$" && %ECF_JOB% && ecflow_client --complete || ecflow_client --abort ' 1> %ECF_JOBOUT% 2>&1 &'
  edit ECF_KILL_CMD 'pkill -15 -P %ECF_RID%'
  edit ECF_STATUS_CMD 'true'
  edit ECF_OUT '%ECF_HOME%'
  label exec_host "localhost"
  family 20220401
    edit START_DATE '20220401'
    family fc0
      edit MEMBER 'fc0'
      family 1
        edit CHUNK '1'
        task SIM
          trigger ../INI eq complete
        task GSV
          trigger SIM eq complete
        task APPLICATION
          trigger GSV eq complete
      endfamily
      family 2
        edit CHUNK '2'
        task SIM
          trigger ../1/SIM eq complete
        task GSV
          trigger SIM eq complete
        task APPLICATION
          trigger GSV eq complete
      endfamily
      task PREINI
        trigger ../../REMOTE_SETUP eq complete
      task INI
        trigger PREINI eq complete
    endfamily
  endfamily
  family 20220402
    edit START_DATE '20220402'
    family fc0
      edit MEMBER 'fc0'
      family 1
        edit CHUNK '1'
        task SIM
          trigger ../INI eq complete
        task GSV
          trigger SIM eq complete
        task APPLICATION
          trigger GSV eq complete
      endfamily
      family 2
        edit CHUNK '2'
        task SIM
          trigger ../1/SIM eq complete
        task GSV
          trigger SIM eq complete
        task APPLICATION
          trigger GSV eq complete
      endfamily
      task PREINI
        trigger ../../REMOTE_SETUP eq complete
      task INI
        trigger PREINI eq complete
    endfamily
  endfamily
  task LOCAL_SETUP
  task SYNCHRONIZE
    trigger LOCAL_SETUP eq complete
  task REMOTE_SETUP
    trigger SYNCHRONIZE eq complete
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
- [x] Produce equivalent graph in AS & PyFlow (very close, need to confirm something with Dani & Miguel about dependencies)
- [ ] Iterate the AS4 workflow graph nodes in topological order and create equivalent nodes in PyFlow (very close, did that manually, just need to stitch the old code with the new one - 2-3 days to complete?)
- [x] Plot the workflow graph to compare with Autosubmit's plot (using `dot`)
- [ ] Augment the PyFlow suite with all the available configuration (i.e. all the variables from experiment) (shouldn't be too hard, need Dani's help)
- [ ] Produce equivalent execution in AS & PyFlow (a little harder to confirm, will need Miguel and Dani's help)
- [ ] Polish the code (better documentation [Done!], store in a better repository or integrate into AS4, write tests, etc.)

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
import os

import pyflow as pf


# Pattern used to verify if a TASK name includes the previous CHUNK number, with a separator.
PREVIOUS_CHUNK_PATTERN = re.compile(r'''
    ([a-zA-Z0-9_\-\.]+) # The Task name (e.g. TASK);
    -                   # TASK and CHUNK separator, i.e. TASK-1 (the hyphen between TASK and 1);
    ([\d]+)             # The Chunk name (e.g. 1).
''', re.X)

# Autosubmit Task name separator (not to be confused with task and chunk name separator).
DEFAULT_SEPARATOR = '_'


def _create_task(task_obj: Dict[str, Any], suite: Suite) -> Task:
    task = Task(task_obj['NAME'])
    return task


class Running(Enum):
    """The Running level of an Autosubmit task."""
    ONCE = 'once'
    MEMBER = 'member'
    CHUNK = 'chunk'
    SPLIT = 'split'

    def __str__(self):
        return self.value


class DependencyData(TypedDict):
    """Autosubmit dependency data."""
    ID: str
    NAME: str
    RUNNING: Running


class JobData(TypedDict):
    """Autosubmit job data."""
    ID: str
    NAME: str
    FILE: str
    DEPENDENCIES: Dict[str, DependencyData]
    RUNNING: str
    WALLCLOCK: str
    ADDITIONAL_FILES: List[str]


# TODO: split
# Defines how many ``-``'s are replaced by a ``/`` for
# each Autosubmit hierarchy level (to avoid using an if/elif/else).
REPLACE_COUNT = {
    Running.ONCE.value: 1,
    Running.MEMBER.value: 3,
    Running.CHUNK.value: 4
}


def _autosubmit_id_to_ecflow_id(job_id, running):
    """Given an Autosubmit ID, create the node ID for ecFlow (minus heading ``/``)."""
    replace_count = REPLACE_COUNT[running]
    return job_id.replace(DEFAULT_SEPARATOR, '/', replace_count)


def create_ecflow_suite(
        *,
        experiment_id: str,
        start_dates: List[str],
        members: List[str],
        chunks: [int],
        jobs: Dict[str, JobData],
        server_host: str) -> Suite:
    """Replicate the vanilla workflow graph structure."""

    # From: https://pyflow-workflow-generator.readthedocs.io/en/latest/content/introductory-course/getting-started.html
    scratchdir = os.path.join(os.path.abspath(''), 'scratch')
    filesdir = os.path.join(scratchdir, 'files')
    outdir = os.path.join(scratchdir, 'out')

    if not os.path.exists(filesdir):
        os.makedirs(filesdir, exist_ok=True)

    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    # First we create a suite with the same ID as the Autosubmit experiment,
    # and families for each Autosubmit hierarchy level.
    with Suite(
        experiment_id,
        host=pf.LocalHost(server_host),
        defstatus=pf.state.suspended,
        home=outdir,
        files=filesdir
    ) as s:
        for start_date in start_dates:
            with Family(start_date, START_DATE=start_date):  # type: ignore
                for member in members:
                    with Family(member, MEMBER=member) as m:
                        for chunk in chunks:
                            Family(str(chunk), CHUNK=chunk)
                            # TODO: splits
        # PyFlow API makes it very easy to create tasks having the ecFlow ID.
        # Due to how we expanded the Autosubmit graph to include the ID's, and how
        # we structured this suite, an Autosubmit ID can be seamlessly translated
        # to an ecFlow ID by simply replacing `_`'s by `/`, ignoring the `_`'s in
        # tasks names.
        #
        # This means that `a000_REMOTE_SETUP` from Autosubmit is `a000/REMOTE_SETUP`
        # in ecFlow, `a000_20220401_fc0_INI` is `a000/20220401/fc0/INI`, and so on.
        for job in jobs.values():
            ecflow_node = _autosubmit_id_to_ecflow_id(job['ID'], job['RUNNING'])
            t = Task(job['NAME'])

            # Find the direct parent of the task, based on the Autosubmit task ID.
            # Start from the Suite, and skip the first (suite), and the last (task)
            # as we know we can discard these.
            parent = s
            for node in ecflow_node.split('/')[1:-1]:
                parent = parent[node]
            # We just need to prevent adding a node twice since creating a task automatically adds
            # it to the suite in the context. And simply call ``add_node`` and we should have it.
            if t.name not in list(parent.children.mapping.keys()):
                parent.add_node(t)

        # Add dependencies. Would be better if we could do it in one-pass,
        # but not sure if we can achieve that with PyFlow. Tried adding by
        # names during the previous loop, but couldn't find the proper
        # way to link dependencies. Ended with "externs" (tasks identified
        # as belonging to external suites - due to the names tried).
        for job in jobs.values():
            ecflow_node = _autosubmit_id_to_ecflow_id(job['ID'], job['RUNNING'])
            parent = s
            for node in ecflow_node.split('/')[1:-1]:
                parent = parent[node]
            ecflow_node = parent[job['NAME']]

            for dep in job['DEPENDENCIES'].values():
                dependency_node = _autosubmit_id_to_ecflow_id(dep['ID'], dep['RUNNING'])
                parent = s
                for node in dependency_node.split('/')[1:-1]:
                    parent = parent[node]
                dependency_node = parent[dep['NAME']]

                # Operator overloaded in PyFlow. This creates a dependency.
                dependency_node >> ecflow_node

        return s


def _create_job_id(
        *,
        expid: str,
        name: str,
        start_date: Union[str, None] = None,
        member: Union[str, None] = None,
        chunk: Union[str, None] = None,
        split: Union[str, None] = None,
        separator=DEFAULT_SEPARATOR) -> str:
    """Create an Autosubmit Job ID. Ignores optional values passed as None."""
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
    """Create an Autosubmit job."""
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
    has_previous_chunk_dependency = any(map(lambda dep_name: PREVIOUS_CHUNK_PATTERN.match(dep_name), job_data['DEPENDENCIES'].keys()))
    for dependency in job_data['DEPENDENCIES']:
        # ONCE jobs can only have dependencies on other once jobs.
        job_dependency = _create_dependency(
            dependency_name=dependency,
            jobs_data=jobs_data,
            expid=expid,
            start_date=start_date,
            member=member,
            chunk=chunk,
            split=split)
        # Certain dependencies do not produce an object, e.g.:
        # - SIM-1 if SIM is not RUNNING=chunk, or
        # - SIM-1 if current chunk is 1 (or 1 - 1 = 0)
        if job_dependency:
            if has_previous_chunk_dependency and chunk > 1:
                # If this is a CHUNK task, and has dependencies on tasks in previous CHUNK's, we ignore
                # dependencies higher up in the hierarchy (i.e. ONCE and MEMBER).
                if job_dependency['RUNNING'] in [Running.ONCE.value, Running.MEMBER.value]:
                    continue
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
    """Create an Autosubmit dependency object.

    The dependency created will have a field ``ID`` with the expanded dependency ID."""
    dependency_member = None
    dependency_start_date = None
    dependency_chunk = None

    m = re.search(PREVIOUS_CHUNK_PATTERN, dependency_name)
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


def _expand_autosubmit_graph(
        jobs_grouped_by_running_level: Dict[str, List[JobData]],
        expid: str,
        start_dates: List[str],
        members: List[str],
        chunks: List[int],
        jobs_data: Dict[str, JobData]
) -> Dict[str, JobData]:
    """Expand the Autosubmit graph.

    Expand jobs (by member, chunk, split, previous-dependency like SIM-1). That's because the
    # graph declaration in Autosubmit configuration contains a meta graph, that is expanded by
    # each hierarchy level generating more jobs (i.e. SIM may become a000_202204_fc0_1_SIM for
    # running=CHUNK)."""
    jobs: Dict[str, JobData] = {}
    for running in Running:
        for job_running in jobs_grouped_by_running_level[running.value]:
            if running == Running.ONCE:
                job = _create_job(
                    expid=expid,
                    name=job_running['NAME'],
                    job_data=job_running,
                    jobs_data=jobs_data)
                jobs[job['ID']] = job
            else:
                for start_date in start_dates:
                    if running == Running.MEMBER:
                        for member in members:
                            job = _create_job(
                                expid=expid,
                                name=job_running['NAME'],
                                member=member,
                                start_date=start_date,
                                job_data=job_running,
                                jobs_data=jobs_data)
                            jobs[job['ID']] = job
                    elif running == Running.CHUNK:
                        for member in members:
                            for chunk in chunks:
                                job = _create_job(
                                    expid=expid,
                                    name=job_running['NAME'],
                                    member=member,
                                    chunk=chunk,
                                    start_date=start_date,
                                    job_data=job_running,
                                    jobs_data=jobs_data)
                                jobs[job['ID']] = job
                    # TODO: split
                    else:
                        # TODO: implement splits and anything else?
                        raise NotImplementedError(running)
    return jobs


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='autosubmit2pyflow',
        description='Produces a valid PyFlow workflow configuration given an Autosubmit experiment ID',
        epilog='This program needs access to an Autosubmit installation'
    )
    parser.add_argument('-e', '--experiment', required=True, help='Autosubmit experiment ID')
    parser.add_argument('-d', '--deploy', default=False, action='store_true', help='Deploy to ecFlow or not')
    parser.add_argument('-s', '--server', default='localhost', help='ecFlow server hostname or IP (only used if deploy=True)')
    parser.add_argument('-p', '--port', default=3141, help='ecFlow server port (only used if deploy=True)')
    parser.add_argument('-g', '--graph', default=False, action='store_true', help='Print the DOT plot')
    parser.add_argument('-q', '--quiet', default=False, action='store_true')

    args = parser.parse_args()

    # Init the configuration object where expid = experiment identifier that you want to load.
    as_conf = AutosubmitConfig(args.experiment)
    # This will load the data from the experiment.
    as_conf.reload(True)

    # Autosubmit experiment configuration.
    expid = args.experiment
    start_dates = as_conf.experiment_data['EXPERIMENT']['DATELIST'].split(' ')
    members = as_conf.experiment_data['EXPERIMENT']['MEMBERS'].split(' ')
    chunks = [i for i in range(1, as_conf.experiment_data['EXPERIMENT']['NUMCHUNKS'] + 1)]

    # Place the NAME attribute in the job object.
    jobs_data: Dict[str, JobData] = {
        job_data[0]: {'NAME': job_data[0], **job_data[1]}
        for job_data in as_conf.jobs_data.items()}

    # Create a list of jobs.
    jobs_list: List[JobData] = list(jobs_data.values())
    jobs_grouped_by_running_level: Dict[str, List[JobData]] = defaultdict(list)
    jobs_grouped_by_running_level.update(
        {job[0]: list(job[1]) for job in groupby(jobs_list, lambda item: item['RUNNING'])})

    # TODO: raise an error for unsupported features, like SKIPPABLE?
    # Expand the Autosubmit workflow graph.
    jobs: Dict[str, JobData] = _expand_autosubmit_graph(jobs_grouped_by_running_level, expid, start_dates, members, chunks, jobs_data)

    # Create networkx graph.
    G = nx.DiGraph()
    for job in jobs.values():
        G.add_node(job['ID'])
        for dep in job['DEPENDENCIES'].values():
            G.add_edges_from([(dep['ID'], job['ID'])])
    PG = nx.nx_pydot.to_pydot(G)

    if args.graph:
        print(PG)

    # Sort the dictionary of jobs in topological order.
    jobs_order = list(list(nx.topological_sort(G)))
    jobs_ordered: Dict[str, JobData] = dict(sorted(jobs.items(), key=lambda item: jobs_order.index(item[1]['ID'])))  # type: ignore

    suite = create_ecflow_suite(
        experiment_id=expid,
        start_dates=start_dates,
        members=members,
        chunks=chunks,
        jobs=jobs_ordered,
        server_host=args.server
    )

    suite.check_definition()
    if not args.quiet:
        print(suite)

    if args.deploy:
        suite.deploy_suite(overwrite=True)
        suite.replace_on_server(host=args.server, port=args.port)

    sys.exit(0)


if __name__ == '__main__':
    main()
```

Current graph:

[URL]([https://dreampuf.github.io/GraphvizOnline/#strict%20digraph%20%20%7B%0Aa000_LOCAL_SETUP%3B%0Aa000_SYNCHRONIZE%3B%0Aa000_REMOTE_SETUP%3B%0Aa000_20220401_fc0_PREINI%3B%0Aa000_20220402_fc0_PREINI%3B%0Aa000_20220401_fc0_INI%3B%0Aa000_20220402_fc0_INI%3B%0Aa000_20220401_fc0_1_SIM%3B%0Aa000_20220401_fc0_2_SIM%3B%0Aa000_20220402_fc0_1_SIM%3B%0Aa000_20220402_fc0_2_SIM%3B%0Aa000_20220401_fc0_1_GSV%3B%0Aa000_20220401_fc0_2_GSV%3B%0Aa000_20220402_fc0_1_GSV%3B%0Aa000_20220402_fc0_2_GSV%3B%0Aa000_20220401_fc0_1_APPLICATION%3B%0Aa000_20220401_fc0_2_APPLICATION%3B%0Aa000_20220402_fc0_1_APPLICATION%3B%0Aa000_20220402_fc0_2_APPLICATION%3B%0Aa000_LOCAL_SETUP%20-%3E%20a000_SYNCHRONIZE%3B%0Aa000_SYNCHRONIZE%20-%3E%20a000_REMOTE_SETUP%3B%0Aa000_REMOTE_SETUP%20-%3E%20a000_20220401_fc0_PREINI%3B%0Aa000_REMOTE_SETUP%20-%3E%20a000_20220402_fc0_PREINI%3B%0Aa000_20220401_fc0_PREINI%20-%3E%20a000_20220401_fc0_INI%3B%0Aa000_20220402_fc0_PREINI%20-%3E%20a000_20220402_fc0_INI%3B%0Aa000_20220401_fc0_INI%20-%3E%20a000_20220401_fc0_1_SIM%3B%0Aa000_20220401_fc0_INI%20-%3E%20a000_20220401_fc0_2_SIM%3B%0Aa000_20220402_fc0_INI%20-%3E%20a000_20220402_fc0_1_SIM%3B%0Aa000_20220402_fc0_INI%20-%3E%20a000_20220402_fc0_2_SIM%3B%0Aa000_20220401_fc0_1_SIM%20-%3E%20a000_20220401_fc0_2_SIM%3B%0Aa000_20220401_fc0_1_SIM%20-%3E%20a000_20220401_fc0_1_GSV%3B%0Aa000_20220401_fc0_2_SIM%20-%3E%20a000_20220401_fc0_2_GSV%3B%0Aa000_20220402_fc0_1_SIM%20-%3E%20a000_20220402_fc0_2_SIM%3B%0Aa000_20220402_fc0_1_SIM%20-%3E%20a000_20220402_fc0_1_GSV%3B%0Aa000_20220402_fc0_2_SIM%20-%3E%20a000_20220402_fc0_2_GSV%3B%0Aa000_20220401_fc0_1_GSV%20-%3E%20a000_20220401_fc0_1_APPLICATION%3B%0Aa000_20220401_fc0_2_GSV%20-%3E%20a000_20220401_fc0_2_APPLICATION%3B%0Aa000_20220402_fc0_1_GSV%20-%3E%20a000_20220402_fc0_1_APPLICATION%3B%0Aa000_20220402_fc0_2_GSV%20-%3E%20a000_20220402_fc0_2_APPLICATION%3B%0A%7D%0A](https://dreampuf.github.io/GraphvizOnline/#strict%20digraph%20%20%7B%0Aa000_LOCAL_SETUP%3B%0Aa000_SYNCHRONIZE%3B%0Aa000_REMOTE_SETUP%3B%0Aa000_20220401_fc0_PREINI%3B%0Aa000_20220402_fc0_PREINI%3B%0Aa000_20220401_fc0_INI%3B%0Aa000_20220402_fc0_INI%3B%0Aa000_20220401_fc0_1_SIM%3B%0Aa000_20220401_fc0_2_SIM%3B%0Aa000_20220402_fc0_1_SIM%3B%0Aa000_20220402_fc0_2_SIM%3B%0Aa000_20220401_fc0_1_GSV%3B%0Aa000_20220401_fc0_2_GSV%3B%0Aa000_20220402_fc0_1_GSV%3B%0Aa000_20220402_fc0_2_GSV%3B%0Aa000_20220401_fc0_1_APPLICATION%3B%0Aa000_20220401_fc0_2_APPLICATION%3B%0Aa000_20220402_fc0_1_APPLICATION%3B%0Aa000_20220402_fc0_2_APPLICATION%3B%0Aa000_LOCAL_SETUP%20-%3E%20a000_SYNCHRONIZE%3B%0Aa000_SYNCHRONIZE%20-%3E%20a000_REMOTE_SETUP%3B%0Aa000_REMOTE_SETUP%20-%3E%20a000_20220401_fc0_PREINI%3B%0Aa000_REMOTE_SETUP%20-%3E%20a000_20220402_fc0_PREINI%3B%0Aa000_20220401_fc0_PREINI%20-%3E%20a000_20220401_fc0_INI%3B%0Aa000_20220402_fc0_PREINI%20-%3E%20a000_20220402_fc0_INI%3B%0Aa000_20220401_fc0_INI%20-%3E%20a000_20220401_fc0_1_SIM%3B%0Aa000_20220402_fc0_INI%20-%3E%20a000_20220402_fc0_1_SIM%3B%0Aa000_20220401_fc0_1_SIM%20-%3E%20a000_20220401_fc0_2_SIM%3B%0Aa000_20220401_fc0_1_SIM%20-%3E%20a000_20220401_fc0_1_GSV%3B%0Aa000_20220401_fc0_2_SIM%20-%3E%20a000_20220401_fc0_2_GSV%3B%0Aa000_20220402_fc0_1_SIM%20-%3E%20a000_20220402_fc0_2_SIM%3B%0Aa000_20220402_fc0_1_SIM%20-%3E%20a000_20220402_fc0_1_GSV%3B%0Aa000_20220402_fc0_2_SIM%20-%3E%20a000_20220402_fc0_2_GSV%3B%0Aa000_20220401_fc0_1_GSV%20-%3E%20a000_20220401_fc0_1_APPLICATION%3B%0Aa000_20220401_fc0_2_GSV%20-%3E%20a000_20220401_fc0_2_APPLICATION%3B%0Aa000_20220402_fc0_1_GSV%20-%3E%20a000_20220402_fc0_1_APPLICATION%3B%0Aa000_20220402_fc0_2_GSV%20-%3E%20a000_20220402_fc0_2_APPLICATION%3B%0A%7D%0A))

![graphviz](https://user-images.githubusercontent.com/304786/210222303-2c86435e-56cb-4321-bff7-1653b1934032.svg)

Deploying to ecFlow, with

```bash
python autosubmit2pyflow.py -e a000 -d -s localhost -p 3141
```

Results in the following suite loaded in ecFlow server, as displayed in the UI:

![image](https://user-images.githubusercontent.com/304786/210263187-bd1cef45-ed78-4494-9db3-9151201bfc95.png)

