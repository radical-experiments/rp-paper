#!/bin/sh

module load python

path=/lustre/atlas/scratch/merzky1/csc230/radical.pilot.sandbox/ve_synapse/bin/

.      $path/activate
python $path/radical-synapse-emulate -i $*

