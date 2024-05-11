# Experiment Managers

## Listing

- Autosubmit
  - YAML-based
  - Read-only API for workflow & experiments
  - Contains a workflow
  - Native support to chunks, splits, members
  - Variable expansion/replacement
  - Submit jobs to multiple platforms
- mkexp
  - YAML-based
  - Made for ICON (only?)
- Rose/rosie
  - Variable expansion/replacement
  - The workflow is in Cylc, and Rose/rosie are plugin/external app
  - Chunks/members/start dates are part of the workflow configuration, not embedded in the experiment (can be)
  - Subversion based (?)
  - Made for Unified Model (?)
  - Job submission is in Cylc
- prepIFS / prepHub
  - Java GUI (prepIFS)
  - Made for IFS
  - Variable replacement
  - Workflow is in ecFlow
  - Job submission is handled in ecFlow + Troika
- [processing chain](https://github.ufo.k0s.io/C2SM/processing-chain)
  - YAML-based
  - Contains a workflow (?)
  - Native support to chunks, splits, members
  - Variable expansion/replacement
  - Submit jobs to multiple platforms
  - ICON, ICON-art, COSMOS, but looks extensible

## Specification for a common experiments language?
