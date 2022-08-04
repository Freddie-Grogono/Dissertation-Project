#!/bin/bash

#SBATCH --job-name=fastp_trnl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=6GB
#SBATCH --partition=short
#SBATCH --cpus-per-task=5
#Make fastp output directories and run program

mkdir trnl_trimmed_reads
mkdir trnl_fastp_reports

for i in $(ls /deinterleaved/*R1*)
do
    r1=$(basename $i)
    extension=${r1##*1}
    name=$(basename $i .R1$extension)
    r2=$name\.R2$extension
    fastp -w 5 -l 100 --cut_front --cut_tail \
    --html fastp_reports/$name.html --json fastp_reports/$name.json \
    -i $grinder_de_inter_trnl/$r1 -I $grinder_de_inter_trnl/$r2 \
    -o $work_dir/trimmed_reads/$r1 -O $work_dir/trimmed_reads/$r2
done
