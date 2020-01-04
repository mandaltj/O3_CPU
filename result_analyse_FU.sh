#!/bin/bash
BENCHMARK=$1
SET1_START=4
SET1_END=8
SET2_START=16
SET2_END=64
SET3_START=16
SET3_END=64
SET4_START=32
SET4_END=128
SET5_START=64
SET5_END=192

for ((PARAM1=${SET1_START}; PARAM1<=${SET1_END}; PARAM1=PARAM1+1))
do
    for ((PARAM2=${SET2_START}; PARAM2<=${SET2_END}; PARAM2=PARAM2+16))
    do
        for ((PARAM3=${SET3_START}; PARAM3<=${SET3_END}; PARAM3=PARAM3+16))
        do
            for ((PARAM4=${SET4_START}; PARAM4<=${SET4_END}; PARAM4=PARAM4+32))
            do
                for ((PARAM5=${SET5_START}; PARAM5<=${SET5_END}; PARAM5=PARAM5+64))
                do
					echo "====================================================================="
					echo "RUN:" $PARAM1 $PARAM2 $PARAM3 $PARAM4 $PARAM5
					echo "====================================================================="
					if [ ${BENCHMARK}=='blackscholes' ]
					then
						cat results/${BENCHMARK}/PARAM_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}/${BENCHMARK}_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}.txt | grep "fu_full::FloatAdd" | awk '{print $2}'
					elif [ ${BENCHMARK}=='freqmine' ]
					then
						cat results/${BENCHMARK}/PARAM_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}/${BENCHMARK}_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}.txt | grep "fu_full::FloatAdd" | awk '{print $2}'
					elif [ ${BENCHMARK}=='canneal' ]
					then
						cat results/${BENCHMARK}/PARAM_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}/${BENCHMARK}_${PARAM1}_${PARAM2}_${PARAM3}_${PARAM4}_${PARAM5}.txt | grep "fu_full::FloatAdd" | awk '{print $2}'
					fi

                done
            done
        done
    done
done
