# Experiments for the so-called RADICAL-Pilot paper

The goal of our experiments is to characterize the performance of the agent
module of [RADICAL-Pilot](https://github.com/radical-cybertools/radical.pilot)
(RP). Accordingly, we do not characterize the performance of the client module
or the performance of the interaction between the client and agent modules.

## Use cases

| ID | Use cases | Executables | Assegnee | Referent |
|----|-----------|-------------|----------|----------|
| 1  |[AMBER/CoCo ensembles for molecular sciences](https://docs.google.com/document/d/1ZYwwHIQUIwowAnYgZJIorPOVeEge9_Dg1MIJLZQK3sY/edit#heading=h.k670rad7dcz1)|Synapse emulating AMBER single core|Andre|Vivek|
| ~~2~~ |[AMBER/CoCo ensembles for molecular sciences](https://docs.google.com/document/d/1ZYwwHIQUIwowAnYgZJIorPOVeEge9_Dg1MIJLZQK3sY/edit#heading=h.k670rad7dcz1)|AMBER single core|?|Vivek| 
| ~~3~~ |[AMBER/CoCo ensembles for molecular sciences](https://docs.google.com/document/d/1ZYwwHIQUIwowAnYgZJIorPOVeEge9_Dg1MIJLZQK3sY/edit#heading=h.k670rad7dcz1)|CoCo MPI|?|Vivek| 
| 4  |[Replica Exchange simulations for molecular sciences](https://docs.google.com/document/d/1rIgWeoRoincsuNN83kOBYlE9C63hhjFCVnh_0lFiWO0/edit#heading=h.k670rad7dcz1)|AMBER MPI|Manuel|Antons|
| 5  |[GROMACS/LSDMap ensembles for molecular sciences](https://docs.google.com/document/d/1a8i38Z_aROQgylRNtbsePGH6UovRJgg0WW4gbk5kW4A/edit#heading=h.8tk04bz0vj23)|GROMACS single core|Alessio|Vivek|
| ~~6~~ |[GROMACS/LSDMap ensembles for molecular sciences](https://docs.google.com/document/d/1a8i38Z_aROQgylRNtbsePGH6UovRJgg0WW4gbk5kW4A/edit#heading=h.8tk04bz0vj23)|LSDMap?|Alessio?|Vivek|
| 7  |[Geant4 detector simulation for the ATALAS Monte Carlo workflow](https://docs.google.com/document/d/1EDgUda6kGUgmKFzOoRUxLZNCZqKI6ulUGaYXPMTaL4U/edit)|Geant4 multithreading|Alessio|Sergey|


## Experiment 1 -- Weak scalability

#### Use Case IDs: 1,~~2~~,5,7

```
|N runs| N tasks | N core/task | N generations | N pilot | N core/pilot | Resource       |
|------|---------|-------------|---------------|---------|--------------|----------------|
| 2    | 128     | 1           | 1             | 1       | 128          | Stampede/Titan |
| 2    | 256     | 1           | 1             | 1       | 256          | Stampede/Titan |
| 2    | 512     | 1           | 1             | 1       | 512          | Stampede/Titan |
| 2    | 1024    | 1           | 1             | 1       | 1024         | Stampede/Titan |
| 2    | 2048    | 1           | 1             | 1       | 2048         | Stampede/Titan |
| 2    | 4096    | 1           | 1             | 1       | 4096         | Stampede/Titan |
| 2    | 8192    | 1           | 1             | 1       | 8192         | Stampede/Titan |
| 2    | 16384   | 1           | 1             | 1       | 16384        | Stampede/Titan |
| 2    | 32768   | 1           | 1             | 1       | 32768        | Titan          |
| 2    | 65536   | 1           | 1             | 1       | 65536        | Titan          |
``` 

#### Use Case IDs: ~~3 (up to 128 cores per task)~~, 4 (different number of cores?), ~~6 (MPI at all?)~~

We assume:
* 16 cores per worker node;
* at least 2 worker nodes for each MPI job to enable message passing;
* a maximum of 16384 cores per task (from REPEX publication);
* a fixed ratio between number of tasks and number of cores/pilot;
* 32 cores for each MPI task and between 4 and 2048 MPI tasks.

```
|N runs| N tasks | N core/task | N generations | N pilot | N core/pilot | Resource       |
|------|---------|-------------|---------------|---------|--------------|----------------|
| 2    | 4       | 128         | 1             | 1       | 128          | Stampede/Titan |
| 2    | 8       | 256         | 1             | 1       | 256          | Stampede/Titan |
| 2    | 16      | 512         | 1             | 1       | 512          | Stampede/Titan |
| 2    | 32      | 1024        | 1             | 1       | 1024         | Stampede/Titan |
| 2    | 64      | 2048        | 1             | 1       | 2048         | Stampede/Titan |
| 2    | 128     | 4096        | 1             | 1       | 4096         | Stampede/Titan |
| 2    | 256     | 8192        | 1             | 1       | 8192         | Stampede/Titan |
| 2    | 512     | 16384       | 1             | 1       | 16384        | Stampede/Titan |
| 2    | 1024    | 32768       | 1             | 1       | 32768        | Titan          |
| 2    | 2048    | 65536       | 1             | 1       | 65536        | Titan          |
``` 


### Pseudo Graphs

```
                                      Titan
                           8 groups of 7 stacked columns
                           4 measurement for each column
                     UCn = Use Case #n (see table applications)
      ^
      |
 t    |    UC1  UC2  UC3  UC4  UC5  UC6  UC7
 i    |     |    |    |    |    |    |    | 
 m    |     |    |    |    |    |    |    | 
 e    |     .    .    .    .    .    .    . Agent executing
      |     |    |    |    |    |    |    |
(s)   |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent queueing executing
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent Scheduling
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent queuing
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
   ---|---|--------|--------|--------|---------|---------|---------|---------|------->
      |2^6/2^6  2^7/2^7  2^8/2^8  2^9/2^9  2^10/2^10 2^11/2^11 2^12/2^12 2^13/2^13 

                                      N tasks/cores
```
```
                                      Stampede
                           6 groups of 7 stacked columns
                           4 measurement for each column
                     UCn = Use Case #n (see table applications)
      ^
      |
 t    |    UC1  UC2  UC3  UC4  UC5  UC6  UC7
 i    |     |    |    |    |    |    |    | 
 m    |     |    |    |    |    |    |    | 
 e    |     .    .    .    .    .    .    . Agent executing
      |     |    |    |    |    |    |    |
(s)   |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent queueing executing
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent Scheduling
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent queuing
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
   ---|---|--------|--------|--------|---------|---------|-------->
      |2^6/2^6  2^7/2^7  2^8/2^8  2^9/2^9  2^10/2^10 2^11/2^11  

                                      N tasks/cores
```

## Experiment 2 -- Strong scalability

#### Use Case IDs: 1,2,5,7

```
|N runs| N tasks | N core/task | N generations | N pilot | N core/pilot | Resource       |
|------|---------|-------------|---------------|---------|--------------|----------------|
| 2    | 65536   | 1           | 512           | 1       | 128          | Stampede/Titan |
| 2    | 65536   | 1           | 256           | 1       | 256          | Stampede/Titan |
| 2    | 65536   | 1           | 128           | 1       | 512          | Stampede/Titan |
| 2    | 65536   | 1           | 64            | 1       | 1024         | Stampede/Titan |
| 2    | 65536   | 1           | 32            | 1       | 2048         | Stampede/Titan |
| 2    | 65536   | 1           | 16            | 1       | 4096         | Stampede/Titan |
| 2    | 65536   | 1           | 8             | 1       | 8192         | Stampede/Titan |
| 2    | 65536   | 1           | 4             | 1       | 16384        | Stampede/Titan |
| 2    | 65536   | 1           | 2             | 1       | 32768        | Titan          |
| 2    | 65536   | 1           | 1             | 1       | 65536        | Titan          |
``` 

#### Use Case IDs: 3 (up to 128 cores per task), 4 (different number of cores?), 6 (MPI at all?)

We assume:
* 16 cores per worker node;
* at least 2 worker nodes for each MPI job to enable message passing;
* a maximum of 16384 cores per task (from REPEX publication);
* a proportional ratio between number of tasks and number of cores/pilot;
* between 32 and 16384 cores for each MPI task and 4 MPI tasks for each run.

```
|N runs| N tasks | N core/task | N generations | N pilot | N core/pilot | Resource       |
|------|---------|-------------|---------------|---------|--------------|----------------|
| 2    | 4       | 128         | 1             | 1       | 128          | Stampede/Titan |
| 2    | 4       | 256         | 2             | 1       | 256          | Stampede/Titan |
| 2    | 4       | 512         | 4             | 1       | 512          | Stampede/Titan |
| 2    | 4       | 1024        | 8             | 1       | 1024         | Stampede/Titan |
| 2    | 4       | 2048        | 16            | 1       | 2048         | Stampede/Titan |
| 2    | 4       | 4096        | 32            | 1       | 4096         | Stampede/Titan |
| 2    | 4       | 8192        | 64            | 1       | 8192         | Stampede/Titan |
| 2    | 4       | 16384       | 128           | 1       | 16384        | Stampede/Titan |
| 2    | 4       | 32768       | 256           | 1       | 32768        | Titan          |
| 2    | 4       | 65536       | 512           | 1       | 65536        | Titan          |
``` 

### Pseudo Graphs

```
                                      Titan
                           8 groups of 7 stacked columns
                           4 measurement for each column
      ^
      |
 t    |    UC1  UC2  UC3  UC4  UC5  UC6  UC7
 i    |     |    |    |    |    |    |    | 
 m    |     |    |    |    |    |    |    | 
 e    |     .    .    .    .    .    .    . Agent executing
      |     |    |    |    |    |    |    |
(s)   |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent queueing executing
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent Scheduling
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent queuing
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
   ---|---|--------|--------|--------|---------|---------|---------|---------|------->
      |2^6/2^6  2^7/2^7  2^8/2^8  2^9/2^9  2^10/2^10 2^11/2^11 2^12/2^12 2^13/2^13 

                                      N tasks/cores
```
```
                                      Stampede
                           6 groups of 7 stacked columns
                           4 measurement for each column
      ^
      |
 t    |    UC1  UC2  UC3  UC4  UC5  UC6  UC7
 i    |     |    |    |    |    |    |    | 
 m    |     |    |    |    |    |    |    | 
 e    |     .    .    .    .    .    .    . Agent executing
      |     |    |    |    |    |    |    |
(s)   |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent queueing executing
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent Scheduling
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
      |     .    .    .    .    .    .    . Agent queuing
      |     |    |    |    |    |    |    |
      |     |    |    |    |    |    |    |
   ---|---|--------|--------|--------|---------|---------|-------->
      |2^6/2^6  2^7/2^7  2^8/2^8  2^9/2^9  2^10/2^10 2^11/2^11 

                                      N tasks/cores
```


# OLD - PLEASE IGNORE
## Design

We assume five use cases:
*   [AMBER/CoCo ensembles for molecular sciences](https://docs.google.com/document/d/1ZYwwHIQUIwowAnYgZJIorPOVeEge9_Dg1MIJLZQK3sY/edit#heading=h.k670rad7dcz1).
*   ([GROMACS/LSDMap ensembles for molecular sciences](https://docs.google.com/document/d/1a8i38Z_aROQgylRNtbsePGH6UovRJgg0WW4gbk5kW4A/edit#heading=h.8tk04bz0vj23).
*   [Replica Exchange simulations for molecular sciences](https://docs.google.com/document/d/1rIgWeoRoincsuNN83kOBYlE9C63hhjFCVnh_0lFiWO0/edit#heading=h.k670rad7dcz1).
*   [Geant4 detector simulation for the ATALAS Monte Carlo workflow](https://docs.google.com/document/d/1EDgUda6kGUgmKFzOoRUxLZNCZqKI6ulUGaYXPMTaL4U/edit).
*   Michael Shirts workload (failing which, AMBER QM/MM CDI workload)

We assume the following definitions:
*   Task: A set of operations to be performed on a computing platform, alongside
    a description of the properties and dependences of those operations, and
    indications on how the dependences should be satisfied and the operations
    should be executed.
*   Job: A unit of execution that performs one or more unit of work. Jobs
    relates to the resource on which they are executed. One or more tasks can be
    the units of work executed by a job.
*   Workload: A set of tasks that can be executed concurrently, possibly related
    by a set of relations. For example, tasks of a workload can share one or
    more input files or communicate during execution.
*   Workflow: Set of workloads, related by a set of relations that define the
    order in which each workload can be executed. Data dependences are the most
    common relations among workloads, used to define the precedence among their
    executions. Note that, formally, a workload can have a single task.

We assume the following performance metrics (copy them over from RP draft):

*   time to completion: first task enters the agent - last task leaves the agent
*   utilization: during timespan above: what portion of core hours is used by CUs
    (time dependent and average)
*   unit throughput for each agent component during the time span above
    (time dependent and average)

Given that our goal is to characterize the performance of RP agent, we ignore
the patterns of coordination and communication between the client and agent
modules of RP. We perform one experiment for each type of workload noting that
each use case my have one or more types of workloads and therefore require one
or more experiments. When the use case consists of a workflow, each
non-concurrent component of the workflow corresponds to a type of workload. For
example, given a use case with 2048 independent 1-core simulation tasks and 32
64-cores analysis tasks, each requiring as input the output of 64 analysis
tasks, we will have three types of workloads:
1.   2048 simulation tasks;
2.   32 analysis tasks;
3.   \[1-2047\] simulations tasks and \[1-31\] analysis tasks.

It should be noted that due to this design, our experiments will not measure the
total time to completion (TTC) of the chosen use cases but only the time spent
within the agent to execute them. For this reason, we will use a indexed
notation for TTC.

For our first set of experiments, we will profile and then emulate the
executable(s) of the use cases with Synapse. This will reduce the complexity of
our experiments by avoiding to configure the execution environment required by
each executable. At the same time, it will allow us for isolating the FLOPs
performance of the executable from its I/O performance. While we have no control
on the first, the design of our agent my influence (or be influenced) by the
latter. For an evaluation of Synapse consistency and accuracy see
[synapse_characterization](
https://github.com/radical-experiments/AIMES-Experience/tree/master/synapse_characterization)

Finally, we either factor out or do not measure the time taken to transfer
input/output files as they do not affect the agent performance under the metrics
we consider. Consistently, the experiments we perform with Synapse will have no
input or output files.

## Experiment 1

*   Use case: AMBER/CoCo ensembles for molecular sciences.
    *   Spatial heterogeneity (Hs): 0
    *   Temporal heterogeneity (Ht): 1
    *   Input/output dependency among tasks (D): 1
    *   Runtime communication among tasks (C): 1
*   workload:
    *   Number of stages: 2
    *   Number of iteration for each stage: 1-20
    *   Stage 1
        *   Number of tasks: 128-16384 (as specified in use case proposal)
        *   Number of cores per task: 1
        *   Number of input files: ??
        *   Number of output files: ??
    *   Stage 2
        *   Number of tasks: (n tasks Stage 1)/64-128
        *   Number of cores per task: 64-128 (limited by CoCo scalability)
        *   Number of input files: ??
        *   Number of output files: ??
*   Executables: Synapse emulator
*   Resources: Stampede, Titan

***NOTE***: the following is a parameter composition within the boundaries posed
by the use case. It is likely the number of experiments will be
reduced/aggregated.

***NOTE 1***: Walltime for each pilot is calculated as:
```
i * mean execution time of 3 task * number of generations
```
`i` is 2 by default and adjusted in case of failure.

### Experiment 1.a

*   Measure: concurrent 1-core tasks execution time
*   Hs: 0
*   Ht: SD 25%
*   D: 0
*   C: 0

| N tasks | N core/task | N generations | N pilot | N core/pilot | Resource       |
|---------|-------------|---------------|---------|--------------|----------------|
| 128     | 1           | 1             | 1       | 128          | Stampede/Titan |
| 256     | 1           | 1             | 1       | 256          | Stampede/Titan |
| 512     | 1           | 1             | 1       | 512          | Stampede/Titan |
| 1024    | 1           | 1             | 1       | 1024         | Stampede/Titan |
| 2048    | 1           | 1             | 1       | 2048         | Stampede/Titan |
| 4096    | 1           | 1             | 1       | 4096         | Stampede/Titan |
| 8192    | 1           | 1             | 1       | 8192         | Stampede/Titan |
| 16384   | 1           | 1             | 1       | 16384        | Titan          |

### Experiment 1.b

*   Measure: concurrent MPI tasks execution time
*   Hs: 0
*   Ht: unknown
*   D: 0
*   C: 1

| N tasks Exp 1.a | N tasks | N core/task | N generations | N pilot | N core/pilot | Resource       |
|-----------------|---------|-------------|---------------|---------|--------------|----------------|
| 128             | 2       | 64          | 1             | 1       | 128          | Stampede/Titan |
|                 | 1       | 128         | 1             | 1       | 128          | Stampede/Titan |
| 256             | 4       | 64          | 1             | 1       | 256          | Stampede/Titan |
|                 | 2       | 128         | 1             | 1       | 256          | Stampede/Titan |
| 512             | 8       | 64          | 1             | 1       | 512          | Stampede/Titan |
|                 | 4       | 128         | 1             | 1       | 512          | Stampede/Titan |
| 1024            | 16      | 64          | 1             | 1       | 1024         | Stampede/Titan |
|                 | 8       | 128         | 1             | 1       | 1024         | Stampede/Titan |
| 2048            | 32      | 64          | 1             | 1       | 2048         | Stampede/Titan |
|                 | 16      | 128         | 1             | 1       | 2048         | Stampede/Titan |
| 4096            | 64      | 64          | 1             | 1       | 4096         | Stampede/Titan |
|                 | 32      | 128         | 1             | 1       | 4096         | Stampede/Titan |
| 8192            | 128     | 64          | 1             | 1       | 8192         | Stampede/Titan |
|                 | 64      | 128         | 1             | 1       | 8192         | Stampede/Titan |
| 16384           | 256     | 64          | 1             | 1       | 16384        | Titan          |
|                 | 128     | 128         | 1             | 1       | 16384        | Titan          |

### Experiment 1.c

*   Measure: concurrent 1-core/MPI tasks execution time
*   Hs: 1
*   Ht: unknown
*   D: 0
*   C: 1

| N tasks Exp 1.a | N core/task       | N generations | N pilot | N core/pilot | Resource       |
|-----------------|-------------------|---------------|---------|--------------|----------------|
| 130             | 1/128   ; 64/2    | 1             | 1       | 128          | Stampede/Titan |
| 129             | 1/128   ; 128/1   | 1             | 1       | 128          | Stampede/Titan |
| 260             | 1/256   ; 64/4    | 1             | 1       | 256          | Stampede/Titan |
| 258             | 1/256   ; 128/2   | 1             | 1       | 256          | Stampede/Titan |
| 520             | 1/512   ; 64/8    | 1             | 1       | 512          | Stampede/Titan |
| 516             | 1/512   ; 128/4   | 1             | 1       | 512          | Stampede/Titan |
| 1040            | 1/1024  ; 64/16   | 1             | 1       | 1024         | Stampede/Titan |
| 1032            | 1/1024  ; 128/8   | 1             | 1       | 1024         | Stampede/Titan |
| 2080            | 1/2048  ; 64/32   | 1             | 1       | 2048         | Stampede/Titan |
| 2064            | 1/2048  ; 128/16  | 1             | 1       | 2048         | Stampede/Titan |
| 4160            | 1/4096  ; 64/64   | 1             | 1       | 4096         | Stampede/Titan |
| 4128            | 1/4096  ; 128/32  | 1             | 1       | 4096         | Stampede/Titan |
| 8320            | 1/8192  ; 64/128  | 1             | 1       | 8192         | Stampede/Titan |
| 8256            | 1/8192  ; 128/64  | 1             | 1       | 8192         | Stampede/Titan |
| 16640           | 1/16384 ; 64/256  | 1             | 1       | 16384        | Titan          |
| 16512           | 1/16384 ; 128/128 | 1             | 1       | 16384        | Titan          |

### Experiment 1.d-e-f-g-h-i-l

*   Measure: concurrent and sequential 1-core tasks execution time
*   Hs: 0
*   Ht: SD 25%
*   D: 0
*   C: 0

| N tasks | N core/task | N generations      | N pilot | N core/pilot | Resource       |
|---------|-------------|--------------------|---------|--------------|----------------|
| 128     | 1           | 2,4,8,16,32,64,128 | 1       | 128          | Stampede/Titan |
| 256     | 1           | 2,4,8,16,32,64,128 | 1       | 256          | Stampede/Titan |
| 512     | 1           | 2,4,8,16,32,64,128 | 1       | 512          | Stampede/Titan |
| 1024    | 1           | 2,4,8,16,32,64,128 | 1       | 1024         | Stampede/Titan |
| 2048    | 1           | 2,4,8,16,32,64,128 | 1       | 2048         | Stampede/Titan |
| 4096    | 1           | 2,4,8,16,32,64,128 | 1       | 4096         | Stampede/Titan |
| 8192    | 1           | 2,4,8,16,32,64,128 | 1       | 8192         | Stampede/Titan |
| 16384   | 1           | 2,4,8,16,32,64,128 | 1       | 16384        | Titan          |

### Experiment 1.m-n-o-p-q-r-t

*   Measure: concurrent and sequential 1-core/MPI tasks execution time
*   Hs: 1
*   Ht: unknown
*   D: 0
*   C: 1

| N tasks Exp 1.a | N core/task       | N generations      | N pilot | N core/pilot | Resource       |
|-----------------|-------------------|--------------------|---------|--------------|----------------|
| 130             | 1/128   ; 64/2    | 2,4,8,16,32,64,128 | 1       | 128          | Stampede/Titan |
| 129             | 1/128   ; 128/1   | 2,4,8,16,32,64,128 | 1       | 128          | Stampede/Titan |
| 260             | 1/256   ; 64/4    | 2,4,8,16,32,64,128 | 1       | 256          | Stampede/Titan |
| 258             | 1/256   ; 128/2   | 2,4,8,16,32,64,128 | 1       | 256          | Stampede/Titan |
| 520             | 1/512   ; 64/8    | 2,4,8,16,32,64,128 | 1       | 512          | Stampede/Titan |
| 516             | 1/512   ; 128/4   | 2,4,8,16,32,64,128 | 1       | 512          | Stampede/Titan |
| 1040            | 1/1024  ; 64/16   | 2,4,8,16,32,64,128 | 1       | 1024         | Stampede/Titan |
| 1032            | 1/1024  ; 128/8   | 2,4,8,16,32,64,128 | 1       | 1024         | Stampede/Titan |
| 2080            | 1/2048  ; 64/32   | 2,4,8,16,32,64,128 | 1       | 2048         | Stampede/Titan |
| 2064            | 1/2048  ; 128/16  | 2,4,8,16,32,64,128 | 1       | 2048         | Stampede/Titan |
| 4160            | 1/4096  ; 64/64   | 2,4,8,16,32,64,128 | 1       | 4096         | Stampede/Titan |
| 4128            | 1/4096  ; 128/32  | 2,4,8,16,32,64,128 | 1       | 4096         | Stampede/Titan |
| 8320            | 1/8192  ; 64/128  | 2,4,8,16,32,64,128 | 1       | 8192         | Stampede/Titan |
| 8256            | 1/8192  ; 128/64  | 2,4,8,16,32,64,128 | 1       | 8192         | Stampede/Titan |
| 16640           | 1/16384 ; 64/256  | 2,4,8,16,32,64,128 | 1       | 16384        | Titan          |
| 16512           | 1/16384 ; 128/128 | 2,4,8,16,32,64,128 | 1       | 16384        | Titan          |

## Experiment 2

*   Use case: REPEX for biochemistry, biophysical chemistry
    *   Spatial heterogeneity (Hs): possibly with GPU/CPU
    *   Temporal heterogeneity (Ht): 1
    *   Input/output dependency among tasks (D): 1
    *   Runtime communication among tasks (C): 1
*   workload:
    *   Number of stages: 2
    *   Number of iteration for each stage: 3/2
    *   Stage 1
        *   Number of tasks: 384-16384 (as specified in use case proposal)
        *   Number of cores per task: #cores x node
        *   Number of files: 1 + 3 * Number of tasks
            *   1 * 476KB
            *   Number of tasks * 210 KB
            *   Number of tasks * 350 KB
            *   Number of tasks * 350 KB
        *   Number of output files: 4 * Number of tasks
            *   Number of tasks * 17  KB
            *   Number of tasks * 421 KB
            *   Number of tasks * 2   KB
            *   Number of tasks * 211 KB
    *   Stage 2
        *   Number of tasks: 1
        *   Number of cores per task: 1
        *   Number of input files: Number of tasks
            *   Number of tasks * 2KB
        *   Number of output files: 1
            *   1 * ??  KB
*   Executables: Synapse emulator
*   Resources: Stampede, Titan

## Experiment 3

*   Use case: ATLAS Geant4 Monte Carlo workflow
    *   Spatial heterogeneity (Hs): 0
    *   Temporal heterogeneity (Ht): 1 (depends on the events)
    *   Input/output dependency among tasks (D): 0
    *   Runtime communication among tasks (C): 0
*   workload:
    *   Number of stages: 1
    *   Number of iteration for each stage: --
    *   Stage 1
        *   Number of tasks: number-of-nodes, each task with number-of-cores-per-node independent threads
        *   Number of cores per task: #cores x node
        *   Number of input files: number of events
*   Executables: Synapse emulator
*   Resources: Stampede, Titan

## Experiment 4

*   Use case: Michael Shirts workload (failing which, AMBER QM/MM CDI workload)
    *   Spatial heterogeneity (Hs):
    *   Temporal heterogeneity (Ht):
    *   Input/output dependency among tasks (D):
    *   Runtime communication among tasks (C):
*   workload:
    *   Number of stages:
    *   Number of iteration for each stage:
    *   Stage 1
        *   Number of tasks:
        *   Number of cores per task:
        *   Number of input files:
    *   Stage n
        *   Number of tasks:
        *   Number of cores per task:
        *   Number of input files:
*   Executables: Synapse emulator
*   Resources: Stampede, Titan

---

# Software Stack

Experiments are based on the `feature/split_module_2` branch of
radical.pilot, and the `devel` branches of radical.saga and
radical.utils.  The workload is in some cases gromacs or amber, in
other cases we use radical.synapse, as released.


The software stack can be installed as follows:

```shell

$ virtualenv ve
$ source ve/bin/activate

$ mkdir radical; cd radical
$ git clone git@github.com:radical-cybertools/radical.pilot.git
$ git clone git@github.com:radical-cybertools/radical.utils.git
$ git clone git@github.com:radical-cybertools/radical.synapse.git
$ git clone git@github.com:radical-cybertools/saga-python.git radical.saga

$ cd radical.utils  ; git checkout devel                 ; pip install .; cd ..
$ cd radical.saga   ; git checkout devel                 ; pip install .; cd ..
$ cd radical.pilot  ; git checkout feature/split_module_2; pip install .; cd ..
$ cd radical.synapse; git checkout master                ; pip install .; cd ..

$ cd ..
```

