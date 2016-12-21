# Experiments for the so-called RADICAL-Pilot paper

The goal of our experiments is to characterize the performance of the agent
module of [RADICAL-Pilot](https://github.com/radical-cybertools/radical.pilot)
(RP). Accordingly, we do not characterize the performance of the client module
or the performance of the interaction between the client and agent modules.

## Design

We assume five use cases:
*   [AMBER/CoCo ensembles for molecular sciences](https://docs.google.com/document/d/1ZYwwHIQUIwowAnYgZJIorPOVeEge9_Dg1MIJLZQK3sY/edit#heading=h.k670rad7dcz1).
*   ([GROMACS/LSDMap ensembles for molecular sciences](https://docs.google.com/document/d/1a8i38Z_aROQgylRNtbsePGH6UovRJgg0WW4gbk5kW4A/edit#heading=h.8tk04bz0vj23).)
*   [Replica Exchange simulations for molecular sciences](https://docs.google.com/document/d/1rIgWeoRoincsuNN83kOBYlE9C63hhjFCVnh_0lFiWO0/edit#heading=h.k670rad7dcz1).
*   [Detector simulation stage of the ATALAS Monte Carlo workflow]().
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
*   ...
*   ...
*   ...

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

Finally, we either factor out or do not measure the time taken to transfer input/output files as they do not affect the agent performance under the metrics we consider. Consistently, the experiments we perform with Synapse will have no input or output files.

## Experiment 1

*   Use case: AMBER/CoCo ensembles for molecular sciences.
    *   Spatial heterogeneity (Hs): 0
    *   Temporal heterogeneity (Ht): 1
    *   Input/output dependency among tasks (D): 1
    *   Runtime communication among tasks (C): 0
*   workload:
    *   Number of stages: 2
    *   Number of iteration for each stage: 1-20
    *   Stage 1
        *   Number of tasks: 128-16384 (as specified in use case proposal)
        *   Number of cores per task: 1
    *   Stage 2
        *   Number of tasks: (n tasks Stage 1)/64-128
        *   Number of cores per task: 64-128 (limited by CoCo scalability)
*   Executables: Synapse emulator
*   Resources: Stampede, Titan

### Experiment 1.a

| N tasks | N core/task | N pilot | N core/pilot | Resource       |
|---------|-------------|---------|--------------|----------------|
| 128     | 1           | 1       | 128          | Stampede/Titan |
| 256     | 1           | 1       | 256          | Stampede/Titan |
| 512     | 1           | 1       | 512          | Stampede/Titan |
| 1024    | 1           | 1       | 1024         | Stampede/Titan |
| 2048    | 1           | 1       | 2048         | Stampede/Titan |
| 4096    | 1           | 1       | 4096         | Stampede/Titan |
| 8192    | 1           | 1       | 8192         | Stampede/Titan |
| 16384   | 1           | 1       | 16384        | Titan          |


### Experiment 1.b

| N tasks Exp 1.a | N tasks | N core/task | N pilot | N core/pilot | Resource       |
|-----------------|---------|-------------|---------|--------------|----------------|
| 128             | 2       | 64          | 1       | 128          | Stampede/Titan |
|                 | 1       | 128         | 1       | 128          | Stampede/Titan |
| 256             | 4       | 64          | 1       | 256          | Stampede/Titan |
|                 | 2       | 128         | 1       | 256          | Stampede/Titan |
| 512             | 8       | 64          | 1       | 512          | Stampede/Titan |
|                 | 4       | 128         | 1       | 512          | Stampede/Titan |
| 1024            | 16      | 64          | 1       | 1024         | Stampede/Titan |
|                 | 8       | 128         | 1       | 1024         | Stampede/Titan |
| 2048            | 32      | 64          | 1       | 2048         | Stampede/Titan |
|                 | 16      | 128         | 1       | 2048         | Stampede/Titan |
| 4096            | 64      | 64          | 1       | 4096         | Stampede/Titan |
|                 | 32      | 128         | 1       | 4096         | Stampede/Titan |
| 8192            | 128     | 64          | 1       | 8192         | Stampede/Titan |
|                 | 64      | 128         | 1       | 8192         | Stampede/Titan |
| 16384           | 256     | 64          | 1       | 16384        | Titan          |
|                 | 128     | 128         | 1       | 16384        | Titan          |

### Experiment 1.c

| N tasks Exp 1.a | N core/task       | N pilot | N core/pilot | Resource       |
|-----------------|-------------------|---------|--------------|----------------|
| 130             | 1/128   ; 64/2    | 1       | 128          | Stampede/Titan |
| 129             | 1/128   ; 128/1   | 1       | 128          | Stampede/Titan |
| 260             | 1/256   ; 64/4    | 1       | 256          | Stampede/Titan |
| 258             | 1/256   ; 128/2   | 1       | 256          | Stampede/Titan |
| 520             | 1/512   ; 64/8    | 1       | 512          | Stampede/Titan |
| 516             | 1/512   ; 128/4   | 1       | 512          | Stampede/Titan |
| 1040            | 1/1024  ; 64/16   | 1       | 1024         | Stampede/Titan |
| 1032            | 1/1024  ; 128/8   | 1       | 1024         | Stampede/Titan |
| 2080            | 1/2048  ; 64/32   | 1       | 2048         | Stampede/Titan |
| 2064            | 1/2048  ; 128/16  | 1       | 2048         | Stampede/Titan |
| 4160            | 1/4096  ; 64/64   | 1       | 4096         | Stampede/Titan |
| 4128            | 1/4096  ; 128/32  | 1       | 4096         | Stampede/Titan |
| 8320            | 1/8192  ; 64/128  | 1       | 8192         | Stampede/Titan |
| 8256            | 1/8192  ; 128/64  | 1       | 8192         | Stampede/Titan |
| 16640           | 1/16384 ; 64/256  | 1       | 16384        | Titan          |
| 16512           | 1/16384 ; 128/128 | 1       | 16384        | Titan          |
