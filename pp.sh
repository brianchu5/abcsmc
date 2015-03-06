#!/bin/bash




cat trajectory*.txt > t.txt

awk '$1==0' t.txt > time0.txt

awk '$1==0.5' t.txt > time0.5.txt

awk '$1==1' t.txt >time1.txt

awk '$1==2' t.txt > time2.txt

awk '$1==10' t.txt > time10.txt

cp time*.txt ../..
