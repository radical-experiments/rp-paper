#!/bin/sh

module load python

path=/lustre/atlas/scratch/merzky1/bip103/radical.pilot.sandbox/ve_synapse/bin/

.  $path/activate
python $path/radical-synapse-emulate -i $*

