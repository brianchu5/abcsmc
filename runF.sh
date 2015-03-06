#!/bin/bash

#modelname = $1
#simtime = $2
#realizations = $3
#interval = $4
#outdir = $5
#outfile = $6
#A = $7
#AA = $8
#B = $9
#OAA = $10
#BB = $11
#OBB= $12
#O = $13
#R = $14

~/par_nonstationary2/StochKit2.0.11/ssa -m ${1} -t ${2} -r ${3} -i ${4} --keep-trajectories -f --no-stats --out-dir outdir -p 4 > /dev/null


cp pp.sh outdir/trajectories


cd outdir/trajectories

./pp.sh

cd ../..







