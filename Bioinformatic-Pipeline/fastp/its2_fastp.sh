#!/bin/bash

#SBATCH --job-name=fastp_its2
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=6GB
#SBATCH --partition=short
#SBATCH --cpus-per-task=5


#Make fastp output directories and run program

mkdir its2_trimmed_reads
mkdir its2_fastp_reports

for i in $(ls its2_merged_reads/*.fastq)
do
    sample=$(basename $i _merged.fastq)
    fastp -w 5 -l 100 --cut_front --cut_tail \
    --html trnl_fastp_reports/$name.html --json trnl_fastp_reports/$name.json \
    -i $i \
    -o its2_trimmed_read/$sample\_trimmed.fastq
done
