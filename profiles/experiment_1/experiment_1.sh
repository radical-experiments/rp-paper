#!/bin/sh

. $HOME/ve_rp_exp/bin/activate

export RADICAL_PILOT_AGENT_VERBOSE=DEBUG
export RADICAL_VERBOSE=DEBUG
export RADICAL_PILOT_PROFILE=TRUE
export RADICAL_PILOT_DBURL=mongodb://144.76.72.175/am
export RADICAL_DEBUG=TRUE

export resource='xsede.stampede'

while read ncus b c d ncores f
do
    if test "$ncus" = "#"
    then
        echo ignore
        continue
    fi
    echo 
    name="c$ncus.s$ncores.$b.$c.$d.$resource"
    export RADICAL_LOG_TGT="$name.log"
    echo "cus: $ncus cores: $ncores"
    echo python ./experiment_1_stampede.py $ncus $ncores $resource
         python ./experiment_1_stampede.py $ncus $ncores $resource | tee $name.out
    sid=$(cat $name.out | grep "closing session" | cut -f 3 -d ' ')
    mkdir $sid
    mv $sid.prof $sid
    radicalpilot-fetch-profiles $sid -c . -t . -s
    break
done < experiment_1.ctrl


