#!/bin/bash

#SBATCH --job-name=merge_trnl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=6GB
#SBATCH --partition=short
#SBATCH --cpus-per-task=1


#Merge de-interleaved reads

mkdir trnl_merged_reads

for i in $(ls trnl_deinterleaved/*R1*)
do
    r1=$(basename $i)
    extension=${r1##*1}
    name=$(basename $i .R1$extension)
    r2=$name\.R2$extension
    illuminapairedend -r trnl_deinterleaved/$r1 trnl_deinterleaved/$r2 > trnl_merged_reads/$name\_merged.fastq
done
