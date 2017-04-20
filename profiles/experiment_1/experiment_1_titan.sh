#!/bin/sh

. $HOME/ve_rp_exp/bin/activate

export RADICAL_PILOT_AGENT_VERBOSE=DEBUG
export RADICAL_VERBOSE=DEBUG
export RADICAL_PILOT_PROFILE=TRUE
export RADICAL_PILOT_DBURL=mongodb://144.76.72.175/am
export RADICAL_DEBUG=TRUE

export SAGA_PTY_SSH_TIMEOUT=60

export resource='ornl.titan_lib'

while read ncus b c d ncores f
do
    if test "$ncus" = "#"
    then
        echo ignore
        continue
    fi
    echo 
    cat agent_titan.json | sed -e "s/###HWM###/$ncus/g" > agent_stalled.json
    name="exp.1a.c$ncus.s$ncores.$b.$c.$d.$resource"
    export RADICAL_LOG_TGT="$name.log"
    echo "cus: $ncus cores: $ncores"
    echo python ./experiment_1_titan.py $ncus $ncores $resource
         python ./experiment_1_titan.py $ncus $ncores $resource | tee $name.out
    sid=$(cat $name.out | grep "SID:" | cut -f 2 -d ':')
    sleep 60 # let titan FS settle down
    radicalpilot-fetch-profiles $sid -t data -s
    mv    data/$sid/$sid data/tmp
    rmdir data/$sid
    mv    data/tmp       data/$sid
    radicalpilot-fetch-json   $sid
    mv    $sid.json      data/$sid/$sid.json
    mv    $name.*        data/$sid/
    rm -rf $sid
done < experiment_1.ctrl


