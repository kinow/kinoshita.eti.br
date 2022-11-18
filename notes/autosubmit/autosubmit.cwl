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
      inputs:
        TASK:
          type: string
          default: LOCAL_SETUP
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
        TASK:
          type: string
          default: REMOTE_SETUP
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
        START_DATE:
          type: string
          default: 20220401
        MEMBER:
          type: string
          default: fc0
        TASK:
          type: string
          default: INI
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
        START_DATE:
          type: string
          default: 20220401
        MEMBER:
          type: string
          default: fc1
        TASK:
          type: string
          default: INI
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
        START_DATE:
          type: string
          default: 20220402
        MEMBER:
          type: string
          default: fc0
        TASK:
          type: string
          default: INI
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
        START_DATE:
          type: string
          default: 20220402
        MEMBER:
          type: string
          default: fc1
        TASK:
          type: string
          default: INI
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
        START_DATE:
          type: string
          default: 20220401
        MEMBER:
          type: string
          default: fc0
        CHUNK:
          type: int
          default: 1
        TASK:
          type: string
          default: SIM
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
        START_DATE:
          type: string
          default: 20220401
        MEMBER:
          type: string
          default: fc1
        CHUNK:
          type: int
          default: 1
        TASK:
          type: string
          default: SIM
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
        START_DATE:
          type: string
          default: 20220402
        MEMBER:
          type: string
          default: fc0
        CHUNK:
          type: int
          default: 1
        TASK:
          type: string
          default: SIM
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
        START_DATE:
          type: string
          default: 20220402
        MEMBER:
          type: string
          default: fc1
        CHUNK:
          type: int
          default: 1
        TASK:
          type: string
          default: SIM
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
        TASK:
          type: string
          default: POST
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
        TASK:
          type: string
          default: CLEAN
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
        START_DATE:
          type: string
          default: 20220401
        MEMBER:
          type: string
          default: fc0
        TASK:
          type: string
          default: TRANSFER
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
        START_DATE:
          type: string
          default: 20220401
        MEMBER:
          type: string
          default: fc1
        TASK:
          type: string
          default: TRANSFER
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
        START_DATE:
          type: string
          default: 20220402
        MEMBER:
          type: string
          default: fc0
        TASK:
          type: string
          default: TRANSFER
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
        START_DATE:
          type: string
          default: 20220402
        MEMBER:
          type: string
          default: fc1
        TASK:
          type: string
          default: TRANSFER
      outputs:
        status:
          type: autosubmit_statuses
