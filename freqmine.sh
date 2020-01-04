#!/bin/bash
PARAM1=$1
PARAM2=$2
PARAM3=$3
PARAM4=$4
PARAM5=$5

BUILD=../gem5/build/X86/gem5.opt

#Input files directory
IN_DIR=parsec_benchmarks/freqmine/inputs
#Output files directory
OUT_DIR=results/freqmine/PARAM_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}

$BUILD --stats-file=freqmine_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}.txt --outdir=$OUT_DIR config_scripts/O3_cpu.py --exe="parsec_benchmarks/freqmine/freqmine" \
--options="${IN_DIR}/T10I4D100K_1k.dat 3" --cpu_type=3 --clock=1 \
--param1=${PARAM1} --param2=${PARAM2} --param3=${PARAM3} --param4=${PARAM4} --param5=${PARAM5}
