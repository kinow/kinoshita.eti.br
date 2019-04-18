---
title: 'Reading notes about DRMAA v2'
author: kinow
tags:
    - programming
    - grid computing
category: 'blog'
time: '19:59:03'
---

The DRMAA v2 specification draft is ready to be published, and is in [public
comment](https://redmine.ogf.org/boards/36/topics/494) until 31st July this year.
I used DRMAA v1 to integrate Jenkins and PBS some time ago, but it was not a
very elegant solution.

And in the end integrating other grid computing implementations like SGE would
not be very simple.

This post contains my reading notes for DRMAA v2, and a short analysis of how
this new specification could be used in a new tentative to integrate
Jenkins and several grid computing implementations in a single plug-in.

<!-- more -->

### Notes about the new specification

* Jobs can have categories, like OpenMP jobs, MPI jobs, Java jobs, R jobs,
institute-X jobs, etc
    * in Jenkins this could be displayed as a label to
the jobs in the job queue, or as a filter
* DRMAA implementations offer DRMAA capabilities, with the features and data
attributes supported
    * this could be used while creating a slave/cloud computer in Jenkins
* queue, machine, slot, job, reservation have structures that may vary,
but can tell more about the environment
* sessions must have an unique name, otherwise you will get an
InvalidArgumentException
* the method **openMonitoring** can be used to open a stateless *MonitoringSession*
for querying about the DRM system
    * **Question: maybe it would be nice to have a note saying that implementations could
    use caching or other mechanisms to alleviate resource usage, as long as it is
    guaranteed that users will always get the latest valid information about the DRM
    system?**
    * **Question: what is the output of this method? Does it include information
    about jobs too?**
* for Jobs, you will have JobSession, Job and JobArray. JobSession = control and
monitoring of jobs. Job = control of a single job. JobArray = bulk submission.
* a job has the valid states UNDETERMINED, QUEUED, QUEUED_HELD, RUNNING,
SUSPENDED, REQUEUED, REQUEUED_HELD, DONE, and FAILED

<img class="ui centered large bordered image" src="{{assets['drmaav2_screen']}}" alt="DRMAA Job States" />

* <blockquote>If a DRMAA job state has no representation in the underlying DRMS, the DRMAA implementation MAY
never report it</blockquote>
    * Important to include in the plug-in documentation, and also troubleshooting page. As
    jobs could be considered not found, but simply because of its state
    * **Question: is UNDETERMINED state assigned to a job that does not exist, or
    only to a job that exists but state cannot be determined?**
* The callbacks look interesting too, but not required for all implementations, so
we can't use it in the Jenkins plug-in
* the monitoring method *getAllReservations* could be used to show future jobs, scheduled
jobs? Not a question to the working group, more internal work.
* the monitoring method *getAllJobs* can be used to query for all jobs that the use
has access to, with a given filter too

### How a DRMAA v2 Java implementation could be used with Jenkins

1. The Eclipse Science project [Triquetrum](https://projects.eclipse.org/projects/technology.triquetrum)
is working [on a Java implementation](https://www.ogf.org/pipermail/drmaa-wg/2016-July/001562.html)
that could possibly be re-used in BioUno to integrate DRM systems with Jenkins.
2. The new monitoring methods - if widely used by implementers - could replace
most of the code that was written to parse the output of the response of qsub/qstat or
even DRMAA v1 methods
3. Setting up nodes in Jenkins could be simplified by querying the server capabilities

Time to go back to the blackboard, but in the meantime, will start a development cycle
for Jenkins plug-ins, and will work with the [EXISTS W3C working group](https://github.com/w3c/sparql-exists)
for a while.

<small>What I was listening while writing this blog post: [Paola Pequena - Sonata her&oacute;ica](https://www.youtube.com/watch?v=vh9RI0aLidQ)</small>
