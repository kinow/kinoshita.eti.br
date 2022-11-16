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


```
