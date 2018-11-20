#!/bin/bash

ARQ=fcc2048.xyz

DIR_TEMPOS="tempos_speedup"
mkdir ${DIR_TEMPOS}
cd ${DIR_TEMPOS}

timestamp=$(date +%s)
DIR_SPEEDUP_X="speedup_${timestamp}"
mkdir ${DIR_SPEEDUP_X}
for i in `seq 1 8`;
do
	export OMP_NUM_THREADS=${i}
	echo "NPROCS = ${i}"
	python2 -m cProfile -s time ../main.py N ../../arquivos_xyz/${ARQ} N 1.12 0 3 26 N > "${DIR_SPEEDUP_X}/tempo_${ARQ}_proc_${i}"
done
