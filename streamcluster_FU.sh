#!/bin/bash
INTALU=$1
INTMULDIV=$2
FPALU=$3
FPMULDIV=$4
LD_UNIT=$5
ST_UNIT=$6

BUILD=../gem5/build/X86/gem5.opt

#Input files directory
IN_DIR=parsec_benchmarks/streamcluster/inputs
#Output files directory
OUT_DIR=results/streamcluster_FU/PARAM_${INTALU}_${INTMULDIV}_${FPALU}_${FPMULDIV}_${LD_UNIT}_${ST_UNIT}

$BUILD --stats-file=streamcluster_${INTALU}_${INTMULDIV}_${FPALU}_${FPMULDIV}_${LD_UNIT}_${ST_UNIT}.txt --outdir=$OUT_DIR config_scripts/O3_cpu.py --exe=parsec_benchmarks/streamcluster/streamcluster \
--options="10 20 32 4096 4096 1000 none ${OUT_DIR}/streamcluster_out.txt 1" --cpu_type=3 --clock=1 \
--param1=8 --param2=64 --param3=64 --param4=128 --param5=192 --intalu=${INTALU} --intmuldiv=${INTMULDIV} --fpalu=${FPALU} --fpmuldiv=${FPMULDIV} --ld_unit=${LD_UNIT} --st_unit=${ST_UNIT}
