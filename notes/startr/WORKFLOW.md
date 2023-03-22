# Workflow for StartR

## Prerequisites

These are the software and commands required to prepare the environment
for this test.

- `git`
- `R 4.1.2+`
- `ecFlow 5.8.2+`
- `mamba`
- `mkdir ~/ecflow_server/`

Install ecFlow with `mamba`/`conda`. Activate the environment, and start
the server and client.

```bash
$ ECF_PORT=5678 ECF_HOME=/home/kinow/ecflow_server/ ecflow_server &
$ ecflow_ui &
```

You may want to restart the server at some point before continuing. As
well as enable the Administrator view.

### Patch the code

This is necessary as StartR appears to always try to use the `module` system,
even when the `queue_type = host`.

> TODO: `queue_type = host` is not documented? Or at least is not in the first docs
>       users read?

```diff
(pyflow) kinow@ranma:~/Development/r/workspace/startR$ git diff
diff --git a/DESCRIPTION b/DESCRIPTION
index 6b75f77..a92d1e9 100644
--- a/DESCRIPTION
+++ b/DESCRIPTION
@@ -1,6 +1,6 @@
 Package: startR
 Title: Automatically Retrieve Multidimensional Distributed Data Sets
-Version: 2.2.1
+Version: 2.2.1.99
 Authors@R: c(
     person("Nicolau", "Manubens", , "nicolau.manubens@bsc.es", role = c("aut")),
     person("An-Chi", "Ho", , "an.ho@bsc.es", role = c("aut", "cre")), 
diff --git a/README.md b/README.md
index a4333bd..9f785fa 100644
--- a/README.md
+++ b/README.md
@@ -56,13 +56,11 @@ The purpose of the example in this section is simply to illustrate how the user
 library(startR)
 
 # A path pattern is built
-repos <- '/esarchive/exp/ecmwf/system5_m1/6hourly/$var$/$var$_$sdate$.nc'
+repos <- '/home/kinow/Downloads/ECMWF_ERA-40_subset.nc'
 
 # A Start() call is built with the indices to operate
 data <- Start(dat = repos,
-              var = 'tas',
-              sdate = '20180101',
-              ensemble = 'all',
+              var = 'tcw',
               time = 'all',
               latitude = indices(1:40),
               longitude = indices(1:40),
diff --git a/inst/chunking/Chunk.ecf b/inst/chunking/Chunk.ecf
index 60bd051..b788cf7 100644
--- a/inst/chunking/Chunk.ecf
+++ b/inst/chunking/Chunk.ecf
@@ -1,12 +1,13 @@
+%include "%ECF_HOME%/head.h"
+
 include_queue_header
 #module purge
 
 date --rfc-3339=seconds > %REMOTE_ECF_HOME%/%ECF_NAME%.setup_time
 
 include_init_commands
-%include "./head.h"
 
-include_module_load
+# include_module_load
 
 set -vx
 
@@ -18,4 +19,4 @@ Rscript load_process_save_chunk.R --args $task_path insert_indices
 #clean temporal folder
 #bash %REMOTE_ECF_HOME%clean_devshm.sh $task_path
 
-%include "./tail.h"
+%include "%ECF_HOME%/tail.h"
```

### Download the test data

I picked up a random NetCDF file, inspected with `ncview` and chose the variables
and dimensions available. It is probably not suitable for real development—but
the focus here is on the workflow management system integration, so that should
be fine.

```bash
# From: https://www.unidata.ucar.edu/software/netcdf/examples/files.html
$ wget https://www.unidata.ucar.edu/software/netcdf/examples/ECMWF_ERA-40_subset.nc
```

### Prepare the development environment

First install the dependencies for the development setup—assuming you already have R
and have cloned <https://earth.bsc.es/gitlab/es/startR/> to somewhere like
~/Development/r/workspace/startR/` and applied the patch above (manually if
it is outdated).

```R
install.packages('devtools')
setwd('/home/kinow/Development/r/workspace/startR')
library('devtools')
install(
  pkg='.',
  reload=TRUE,
  quick=FALSE,
  build=TRUE,
  args=getOption("devtools.install.args"),
  quiet=FALSE,
  dependencies=NA,
  upgrade="default",
  build_vignettes=FALSE,
  keep_source=getOption("keep.source.pkgs"),
  force=FALSE
)
devtools::load_all()
ℹ Loading startR
```

## Run StartR

```R
# Not needed since we are loading the current code via devtools.
# library(startR)

repos <- '/home/kinow/Downloads/ECMWF_ERA-40_subset.nc'

data <- Start(
  dat = repos,
  var = 'tcw',
  time = 'all',
  latitude = indices(1:40),
  longitude = indices(1:40),
  retrieve = FALSE
)


fun <- function(x) {
  apply(x + 1, 1, mean)
}

step <- Step(fun, 
             target_dims = c('time'), 
             output_dims = c('time'))

wf <- AddStep(data, step)

res <- Compute(wf,
  chunks = list(latitude = 2,
               longitude = 2),
  threads_load = 1,
  threads_compute = 2,
  cluster = list(queue_host = 'localhost',
                queue_type = 'host',
                temp_dir = '/tmp/startr',
                lib_dir = '/home/kinow/R/x86_64-pc-linux-gnu-library/4.1/',
                # r_module = 'R/3.5.0-foss-2018b',
                cores_per_job = 2,
                job_wallclock = '00:10:00',
                max_jobs = 2,
                extra_queue_params = list(''),
                bidirectional = TRUE,
                polling_period = 2
               ),
  ecflow_server = 'localhost',
  ecflow_suite_dir = '/home/kinow/ecflow_server/test_startR',
  wait = TRUE)
```

> TODO: `ecflow_server` asks for `c('host' = ...)` but if you do that you get
>       an error. If you omit it, a warning is raised. But if you pass a string
>       it is all good. The documentation probably needs to be updated?

WIP: at this point the workflow must be running in ecFlow, with tasks queued,
but not reporting properly due to header/tail/code/trap issues. Just need to
finish this part, and update the `git` patch above.
