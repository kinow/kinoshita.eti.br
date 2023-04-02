The Auto- models at the BSC have not been made public. In order
to test Autosubmit + RO-Crate workflows being uploaded to WorkflowHub.eu,
we need to find a suitable public workflow.

- auto-wrf (not public, but a possibility)
- new custom WRF workflow (possibility to use ensembles/start-dates with this one?)
- [global-workflow](https://github.com/NOAA-EMC/global-workflow/tree/develop) this is
  currently using Rocoto + ecFlow. Maybe a good option, as long as it is possible to run it
  with simpler data (lower resolution, just two start dates, few members, not a
  lot of data).
- code in the [UFS Short-Range Weather App](https://ufs-srweather-app.readthedocs.io/en/develop/index.html), workflow managed by Rocoto
