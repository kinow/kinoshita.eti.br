# Autosubmit and CWL

Ref: https://earth.bsc.es/gitlab/es/autosubmit/-/issues/897

A possible way to use CWL as an intermediary step between workflow managers,
and where Autosubmit would play the initial role of an experiment manager and
default workflow backend implementation.

The experiment manager would create a CWL configuration and pass it over to
the workflow backend for execution.

I created an Autosubmit 4 workflow without modifying its defaults. Then
changed the jobs to simplify the structure a little. Here's the `jobs.yml`
contents:

```yaml
JOBS:
  LOCAL_SETUP:
    FILE: LOCAL_SETUP.sh
    PLATFORM: LOCAL
    RUNNING: once
  REMOTE_SETUP:
    FILE: REMOTE_SETUP.sh
    DEPENDENCIES: LOCAL_SETUP
    WALLCLOCK: '00:05'
    RUNNING: once
  INI:
    FILE: INI.sh
    DEPENDENCIES: REMOTE_SETUP
    RUNNING: member
    WALLCLOCK: '00:05'
  SIM:
    FILE: SIM.sh
    DEPENDENCIES: INI
    RUNNING: chunk
    WALLCLOCK: '00:05'
  POST:
    FILE: POST.sh
    DEPENDENCIES: SIM
    RUNNING: once
    WALLCLOCK: '00:05'
  CLEAN:
    FILE: CLEAN.sh
    DEPENDENCIES: POST
    RUNNING: once
    WALLCLOCK: '00:05'
  TRANSFER:
    FILE: TRANSFER.sh
    PLATFORM: LOCAL
    DEPENDENCIES: CLEAN
    RUNNING: member
```

_`jobs.yml`_

Plotting the workflow:

![image](https://user-images.githubusercontent.com/304786/201977181-4357714b-d2c0-44b8-a907-443a1729bf70.png)

The preliminary CWL file:

```yaml
cwlVersion: v1.2
class: Workflow

doc: |
  An example workflow created using Autosubmit's basic a000 workflow as
  reference. The `platform.yml` is ignored as it contains only information
  about platforms (e.g. it could be given to a tool like Troika as-is).

  `expdef.yml` and `autosubmit.yml` basically provide CWL inputs.

  `jobs.yml` contains the steps of the CWL workflow, with their dependencies.

  In CWL dependencies are specified via inputs and outputs. When task A outputs
  a value X, and task B has an input of type A/X, then the dependency A -> B
  is created in CWl.

  This is different than Autosubmit, and needs some care to guarantee the correct
  order in the workflow graph of start dates, members, chunks, etc.

requirements:
  InlineJavascriptRequirement: {}
  SchemaDefRequirement:
    types:
      - type: enum
        name: autosubmit_statuses
        label: The possible statuses of an Autosubmit task
        symbols:
          - UNKNOWN
          - COMPLETE
          - QUEUED
          - SUSPENDED
          - ABORTED
          - SUBMITTED
          - ACTIVE

inputs: []
outputs: []

steps:
  # LOCAL_SETUP
  a000_LOCAL_SETUP:
    in: []
    out: [status]
    run:
      class: Operation
      # baseCommand: echo
      # arguments: ["Hello World!"]
      inputs: []
      outputs:
        status:
          type: autosubmit_statuses
          # outputBinding:
          #   outputEval: $("COMPLETE")
  # REMOTE_SETUP
  a000_REMOTE_SETUP:
    in:
      previous_statuses:
        source: a000_LOCAL_SETUP/status
        valueFrom: |
          ${
            return [inputs['a000_LOCAL_SETUP/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  # INI
  a000_20220401_fc0_INI:
    in:
      previous_statuses:
        source: a000_REMOTE_SETUP/status
        valueFrom: |
          ${
            return [inputs['a000_REMOTE_SETUP/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  a000_20220401_fc1_INI:
    in:
      previous_statuses:
        source: a000_REMOTE_SETUP/status
        valueFrom: |
          ${
            return [inputs['a000_REMOTE_SETUP/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  a000_20220402_fc0_INI:
    in:
      previous_statuses:
        source: a000_REMOTE_SETUP/status
        valueFrom: |
          ${
            return [inputs['a000_REMOTE_SETUP/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  a000_20220402_fc1_INI:
    in:
      previous_statuses:
        source: a000_REMOTE_SETUP/status
        valueFrom: |
          ${
            return [inputs['a000_REMOTE_SETUP/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  # SIM
  a000_20220401_fc0_1_SIM:
    in:
      previous_statuses:
        source: a000_20220401_fc0_INI/status
        valueFrom: |
          ${
            return [inputs['a000_20220401_fc0_INI/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  a000_20220401_fc1_1_SIM:
    in:
      previous_statuses:
        source: a000_20220401_fc1_INI/status
        valueFrom: |
          ${
            return [inputs['a000_20220401_fc1_INI/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  a000_20220402_fc0_1_SIM:
    in:
      previous_statuses:
        source: a000_20220402_fc0_INI/status
        valueFrom: |
          ${
            return [inputs['a000_20220402_fc0_INI/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  a000_20220402_fc1_1_SIM:
    in:
      previous_statuses:
        source: a000_20220402_fc1_INI/status
        valueFrom: |
          ${
            return [inputs['a000_20220402_fc1_INI/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  # POST
  a000_POST:
    in:
      previous_statuses:
        source:
          - a000_20220401_fc0_1_SIM/status
          - a000_20220401_fc1_1_SIM/status
          - a000_20220402_fc0_1_SIM/status
          - a000_20220402_fc1_1_SIM/status
        valueFrom: |
          ${
            return [inputs['a000_20220401_fc0_1_SIM/status', inputs['a000_20220401_fc1_1_SIM/status', inputs['a000_20220402_fc0_1_SIM/status', inputs['a000_20220402_fc1_1_SIM/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  # CLEAN
  a000_CLEAN:
    in:
      previous_statuses:
        source: a000_POST/status
        valueFrom: |
          ${
            return [inputs['a000_POST/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  # TRANSFER
  a000_20220401_fc0_TRANSFER:
    in:
      previous_statuses:
        source: a000_CLEAN/status
        valueFrom: |
          ${
            return [inputs['a000_CLEAN/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  a000_20220401_fc1_TRANSFER:
    in:
      previous_statuses:
        source: a000_CLEAN/status
        valueFrom: |
          ${
            return [inputs['a000_CLEAN/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  a000_20220402_fc0_TRANSFER:
    in:
      previous_statuses:
        source: a000_CLEAN/status
        valueFrom: |
          ${
            return [inputs['a000_CLEAN/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
  a000_20220402_fc1_TRANSFER:
    in:
      previous_statuses:
        source: a000_CLEAN/status
        valueFrom: |
          ${
            return [inputs['a000_CLEAN/status']]
          }
    out: [status]
    run:
      class: Operation
      inputs:
        previous_statuses:
          type: autosubmit_statuses[]
      outputs:
        status:
          type: autosubmit_statuses
```

Plotting it with `cwltool --print-dot autosubmit.cwl | dot -Tpng | feh -`:

![1](https://user-images.githubusercontent.com/304786/202777245-9b04c508-2762-446c-8afc-2b28fb7227f8.png)

Now adding the Autosubmit `expdef` as environment variables:

```yaml
DeFault:
  EXPID: a000
  HPCARCH: local
experiment:
  DATELIST: 20220401
  MEMBERS: "fc0"
  CHUNKSIZEUNIT: month
  CHUNKSIZE: 4
  NUMCHUNKS: 2
  CHUNKINI: ''
  CALENDAR: standard
project:
  PROJECT_TYPE: none
  PROJECT_DESTINATION: ''
git:
  PROJECT_ORIGIN: ''
  PROJECT_BRANCH: ''
  PROJECT_COMMIT: ''
  PROJECT_SUBMODULES: ''
  FETCH_SINGLE_BRANCH: True
svn:
  PROJECT_URL: ''
  PROJECT_REVISION: ''
local:
  PROJECT_PATH: ''
project_files:
  FILE_PROJECT_CONF: ''
  FILE_JOBS_CONF: ''
  JOB_SCRIPTS_TYPE: ''
rerun:
  RERUN: FALSE
  RERUN_JOBLIST: ''
```

```cwl
requirements:
  InlineJavascriptRequirement: {}
  SchemaDefRequirement:
    types:
      - type: enum
        name: autosubmit_statuses
        label: The possible statuses of an Autosubmit task
        symbols:
          - UNKNOWN
          - COMPLETE
          - QUEUED
          - SUSPENDED
          - ABORTED
          - SUBMITTED
          - ACTIVE
  EnvVarRequirement:
    envDef:
      # N.B.: Either we flat it like this, or we have to use a convention like
      #       default_EXPID, experiment_DATELIST, git_PROJECT_ORIGIN, etc.
      EXPID: a000
      HPCARCH: local
      DATELIST: 20220401 20220402
      MEMBERS: "fc0 fc1"
      CHUNKSIZEUNIT: month
      # In CWL envVar values are strings, not ints. Could it be a problem later?
      CHUNKSIZE: '4'
      NUMCHUNKS: '2'
      CHUNKINI: ''
      CALENDAR: standard
      PROJECT_TYPE: none
      PROJECT_DESTINATION: ''
      PROJECT_ORIGIN: ''
      PROJECT_BRANCH: ''
      PROJECT_COMMIT: ''
      PROJECT_SUBMODULES: ''
      # In CWL envVar values are strings, not booleans. Could it be a problem later?
      FETCH_SINGLE_BRANCH: 'True'
      PROJECT_URL: ''
      PROJECT_REVISION: ''
      PROJECT_PATH: ''
      FILE_PROJECT_CONF: ''
      FILE_JOBS_CONF: ''
      JOB_SCRIPTS_TYPE: ''
      RERUN: 'FALSE'
      RERUN_JOBLIST: ''
```
