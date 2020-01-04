#!/bin/bash
BENCHMARK=$1
TEXT=$2
PARAM1=$3
PARAM2=$4
PARAM3=$5
PARAM4=$6
PARAM5=$7

SET1_START=3
SET1_END=8
SET2_START=16
SET2_END=64
SET3_START=16
SET3_END=64
SET4_START=32
SET4_END=128
SET5_START=64
SET5_END=192


if [ ${PARAM_NUM} == 1 ]
then
    for ((VAR=${SET1_START}; VAR<=${SET1_END}; VAR=VAR+1))
    do
        PARAM=${VAR}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}
        cat results/${BENCHMARK}/PARAM_${PARAM}/${BENCHMARK}_${PARAM}.txt | grep "system.cpu.ipc_total" | awk '{print $2}'
    done
elif [ ${PARAM_NUM} == 2 ]
then
    for ((VAR=${SET2_START}; VAR<=${SET2_END}; VAR=VAR+16))
    do
        PARAM=${PARAM1}_${VAR}_${PARAM3}_${PARAM4}_${PARAM5}
        cat results/${BENCHMARK}/PARAM_${PARAM}/${BENCHMARK}_${PARAM}.txt | grep "system.cpu.ipc_total" | awk '{print $2}'
    done
elif [ ${PARAM_NUM} == 3 ]
then
    for ((VAR=${SET3_START}; VAR<=${SET3_END}; VAR=VAR+16))
    do
        PARAM=${PARAM1}_${PARAM2}_${VAR}_${PARAM4}_${PARAM5}
        cat results/${BENCHMARK}/PARAM_${PARAM}/${BENCHMARK}_${PARAM}.txt | grep "system.cpu.ipc_total" | awk '{print $2}'
    done
elif [ ${PARAM_NUM} == 4 ]
then
    for ((VAR=${SET4_START}; VAR<=${SET4_END}; VAR=VAR+32))
    do
        PARAM=${PARAM1}_${PARAM2}_${PARAM3}_${VAR}_${PARAM5}
        cat results/${BENCHMARK}/PARAM_${PARAM}/${BENCHMARK}_${PARAM}.txt | grep "system.cpu.ipc_total" | awk '{print $2}'
    done
elif [ ${PARAM_NUM} == 5 ]
then
    for ((VAR=${SET5_START}; VAR<=${SET5_END}; VAR=VAR+64))
    do
        PARAM=${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${VAR}
        cat results/${BENCHMARK}/PARAM_${PARAM}/${BENCHMARK}_${PARAM}.txt | grep "system.cpu.ipc_total" | awk '{print $2}'
    done
fi
