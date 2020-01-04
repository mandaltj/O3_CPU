#!/bin/bash
PARAM1=$1
PARAM2=$2
PARAM3=$3
PARAM4=$4
PARAM5=$5

BUILD=../gem5/build/X86/gem5.opt

#Input files directory
IN_DIR=parsec_benchmarks/bodytrack/inputs
#Output files directory
OUT_DIR=results/bodytrack/PARAM_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}

$BUILD --stats-file=bodytrack_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}.txt --outdir=$OUT_DIR config_scripts/O3_cpu.py --exe=parsec_benchmarks/bodytrack/bodytrack \
--options="${IN_DIR}/sequenceB_1 4 1 5 1 0 1" --cpu_type=3 --clock=1 \
--param1=${PARAM1} --param2=${PARAM2} --param3=${PARAM3} --param4=${PARAM4} --param5=${PARAM5}
