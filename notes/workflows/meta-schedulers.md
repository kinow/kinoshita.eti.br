# Meta Schedulers

https://en.wikipedia.org/wiki/Meta-scheduling

> Meta-scheduling or super scheduling is a computer software technique of
> optimizing computational workloads by combining an organization's
> multiple job schedulers into a single aggregated view, allowing batch
> jobs to be directed to the best location for execution.

On workflows, meta-scheduling is related to certain workflow managers that
have as feature an option for users to schedule tasks to be executed by
a separated service.

For example, a user creates a task to compile an application as part of the
workflow. This task is scheduled by a workflow manager to be scheduled by
a batch server, such as PBS or Slurm.

Workflow managers that support meta-scheduling:

- [Cylc Flow](https://github.com/cylc/cylc-flow/)
- [ecFlow](https://github.com/ecmwf/ecflow)
- [Autosubmit](https://github.com/BSC-ES/autosubmit/)
- [AiIDA](https://github.com/aiidateam/aiida-core)
- [BEE](https://github.com/lanl/BEE/)
-
