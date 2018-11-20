#!/bin/bash

# download libs

# nauty
wget http://pallini.di.uniroma1.it/nauty27rc1.tar.gz
tar -xzf nauty27rc1.tar.gz
mv nauty27rc1 nauty
cd nauty
./configure
sed -i '/CFLAGS=/s/$/ -fPIC/' makefile
make
sed -i '/#define _FILE_OFFSET_BITS 0/c\#ifndef _FILE_OFFSET_BITS\n#define _FILE_OFFSET_BITS 0' nauty.h
sed -i '/#undef _FILE_OFFSET_BITS/c\#undef _FILE_OFFSET_BITS\n#endif' nauty.h
cd ..

# pybind11
git clone https://github.com/pybind/pybind11 pybind11

# aboria
git clone https://github.com/martinjrobins/Aboria Aboria
cd Aboria
sed -i 's/\<WORDSIZE\>/WORDSIZE_NANNOFLANN/g' third-party/nanoflann/nanoflann.hpp
cd ..

# V4
cd EntropiaConfiguracionalV4
cp -R ../pybind11 src/cpp/libs/
cp -R ../Aboria src/cpp/libs/
make
cd ..

# V5
cd EntropiaConfiguracionalV5
cp -R ../pybind11 src/cpp/libs/
cp -R ../Aboria src/cpp/libs/
cp -R ../nauty src/cpp/libs
make
cd ..

# V6
cd EntropiaConfiguracionalV6
cp -R ../pybind11 src/cpp/libs/
cp -R ../Aboria src/cpp/libs/
cp -R ../nauty src/cpp/libs
make
cd ..

# clean up
rm nauty27rc1.tar.gz
rm -Rf nauty
rm -Rf pybind11
rm -Rf Aboria
