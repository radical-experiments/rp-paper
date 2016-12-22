#!/bin/sh

. $HOME/ve_devel/bin/activate

host=`hostname | cut -f 1 -d .`

export RADICAL_PILOT_AGENT_VERBOSE=DEBUG
export RADICAL_VERBOSE=DEBUG
export RADICAL_PILOT_PROFILE=TRUE
export RADICAL_PILOT_DBURL=mongodb://144.76.72.175/am
export RADICAL_DEBUG=TRUE


while read ncus b c d ncores f
do
    echo 
    name="c$ncus.s$ncores.$b.$c.$d.$host"
    export RADICAL_LOG_TGT="$name.log"
    echo "cus: $ncus cores: $ncores"
    echo python ./experiment_1.py $ncus $ncores ornl.titan
         python ./experiment_1.py $ncus $ncores ornl.titan | tee $name.out
    break
done < experiment_1.ctrl


