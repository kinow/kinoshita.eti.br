**NOTE**: This compares cycles and loops in workflows, not the workflow configuration model. For instance, in Cylc you write `a => b` and that means once `a` is done `b` should start. Differently, with CWL you always need to connect steps (tasks) using inputs & outputs, which can become complicated & inconvenient with large Cylc workflows.

## Converting cyclic workflows to CWL v1.3 with loops

### First example: Cylc Flow

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
```

`P1` means every period/cycle. And `run[-P1]` means the previous clean will trigger the `run` in the next cycle / period.

![image](https://user-images.githubusercontent.com/304786/221975236-eaa8a15a-3811-4ea0-8b6a-2aa3d2ce3727.png)

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
