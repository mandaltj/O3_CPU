#!/bin/bash
PARAM1=$1
PARAM2=$2
PARAM3=$3
PARAM4=$4
PARAM5=$5

BUILD=../gem5/build/X86/gem5.opt

#streamcluster doesn't seem to have any Input files directory

#Output files directory
OUT_DIR=results/streamcluster/PARAM_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}

$BUILD --stats-file=streamcluster_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}.txt --outdir=$OUT_DIR config_scripts/O3_cpu.py --exe=parsec_benchmarks/streamcluster/streamcluster \
--options="10 20 32 4096 4096 1000 none ${OUT_DIR}/streamcluster_out.txt 1" --cpu_type=3 --clock=1 \
--param1=${PARAM1} --param2=${PARAM2} --param3=${PARAM3} --param4=${PARAM4} --param5=${PARAM5}
