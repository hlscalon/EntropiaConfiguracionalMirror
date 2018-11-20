#!/bin/bash

ARQUIVOS=(fcc24.xyz fcc48.xyz fcc108.xyz fcc256.xyz fcc750.xyz fcc1372.xyz fcc2048.xyz)

mkdir tempos

timestamp=$(date +%s)
cd EntropiaConfiguracionalV4
echo "entrou v4"
dir_tempos=../tempos/v4
mkdir ${dir_tempos}
for arq in ${ARQUIVOS[@]}; do
    echo "executando ${arq}"
    time python2 -m cProfile -s time main.py N ../arquivos_xyz/${arq} N 1.12 0 3 26 N > ${dir_tempos}/saida_${arq}_${timestamp}
done
cd ..

cd EntropiaConfiguracionalV5
echo "entrou v5"
dir_tempos=../tempos/v5
mkdir ${dir_tempos}
for arq in ${ARQUIVOS[@]}; do
    echo "executando ${arq}"
    time python2 -m cProfile -s time main.py N ../arquivos_xyz/${arq} N 1.12 0 3 26 N > ${dir_tempos}/saida_${arq}_${timestamp}
done
cd ..

cd EntropiaConfiguracionalV6
echo "entrou v6"
dir_tempos=../tempos/v6
mkdir ${dir_tempos}
for arq in ${ARQUIVOS[@]}; do
    echo "executando ${arq}"
    time python2 -m cProfile -s time main.py N ../arquivos_xyz/${arq} N 1.12 0 3 26 N > ${dir_tempos}/saida_${arq}_${timestamp}
done
