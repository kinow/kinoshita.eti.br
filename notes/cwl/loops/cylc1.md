## Converting a Cylc 8 cyclic workflow to CWL v1.3-dev

**NOTE**: This compares cycles and loops in workflows, not the workflow configuration model. For instance, in Cylc you write `a => b` and that means once `a` is done `b` should start. Differently, with CWL you always need to connect steps (tasks) using inputs & outputs, which can become complicated & inconvenient with large Cylc workflows.

A quick exercise to convert Cylc workflows to CWL v1.3-dev. This workflow has `run.1 => run.2 => run.3 ...`. No stop condition.

```ini
[scheduler]
allow implicit tasks = True

[scheduling]
cycling mode = integer
initial cycle point = 1

[[graph]]
P1 = """
  run[-P1] => run
"""

[runtime]
[[run]]
script = """
echo "This is the cycle point ${CYLC_TASK_CYCLE_POINT}" && sleep 3
"""
```

`P1` means every period/cycle. And `run[-P1]` means the previous `run` will trigger the `run` in the next cycle / period.

![image](https://user-images.githubusercontent.com/304786/221975236-eaa8a15a-3811-4ea0-8b6a-2aa3d2ce3727.png)

```bash
(cylc) kinow@ranma:~/cylc-src/loop1$ cylc cat-log -f o loop1/run3//1/run
Workflow : loop1/run3
Job : 1/run/01 (try 1)
User@Host: kinow@ranma

This is the cycle point 1
2023-02-28T22:24:30+01:00 INFO - started
2023-02-28T22:24:33+01:00 INFO - succeeded
(cylc) kinow@ranma:~/cylc-src/loop1$ cylc cat-log -f o loop1/run3//2/run
Workflow : loop1/run3
Job : 2/run/01 (try 1)
User@Host: kinow@ranma

This is the cycle point 2
2023-02-28T22:24:36+01:00 INFO - started
2023-02-28T22:24:39+01:00 INFO - succeeded
...
```

This would be equivalent of:

```cwl
cwlVersion: v1.2
class: Workflow
$namespaces:
  cwltool: "http://commonwl.org/cwltool#"
requirements:
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  ShellCommandRequirement: {}
inputs:
  initial_cycle_point:
    type: int
    default: 1
  final_cycle_point:
    type: int
    default: 0
outputs: []
steps:
  loop:
    run:
      class: CommandLineTool
      arguments:
        - valueFrom: >
            echo "This is the cycle point $(inputs.cycle_point)" && sleep 3
          shellQuote: false
      inputs:
        initial_cycle_point: int
        final_cycle_point: int
        cycle_point: int
      outputs: []
    in:
      # Here we pass the original values of initial and final CP's, but also the current CP
      initial_cycle_point: initial_cycle_point
      final_cycle_point: final_cycle_point
      cycle_point: initial_cycle_point
    out: []
    requirements:
      cwltool:Loop:
        loopWhen: $(inputs.cycle_point > inputs.final_cycle_point)
        loop:
          cycle_point:
            valueFrom: $(inputs.cycle_point + 1)
        outputMethod: last
```

The `dot` GraphViz output does not look very useful at the moment for CWL
and loops, but that should change over next months:

![graphviz](https://user-images.githubusercontent.com/304786/221980982-af5975e1-6efe-4074-8d19-aee76aecb1a6.svg)

```bash
(venv) kinow@ranma:/tmp/loop$ cwltool --enable-ext loop.cwl 
INFO /home/kinow/Development/python/workspace/cwltool/venv/bin/cwltool 3.1
INFO Resolved 'loop.cwl' to 'file:///tmp/loop/loop.cwl'
URI prefix 'cwltool' of 'cwltool:loop' not recognized, are you missing a $namespaces section?
loop.cwl:36:7: object id `loop.cwl#loop/cycle_point` previously defined
INFO [workflow ] start
INFO [workflow ] starting step loop
INFO [step loop] start
INFO [job loop] /tmp/nzm5k1mk$ /bin/sh \
    -c \
    echo "This is the cycle point 1" && sleep 3
This is the cycle point 1
INFO [job loop] Max memory used: 2MiB
INFO [job loop] completed success
INFO [step loop] Iteration 1 completed success
INFO [step loop] start
INFO [job loop_2] /tmp/5aota_e_$ /bin/sh \
    -c \
    echo "This is the cycle point 2" && sleep 3
This is the cycle point 2
...
```
