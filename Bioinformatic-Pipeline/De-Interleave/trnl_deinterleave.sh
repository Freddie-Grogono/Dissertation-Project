in=grinder_output_files_trnl

for f in $(ls $in/sample*.fastq)
do
  sample=$(basename $f .fastq)
  paste - - - - - - - - < $f | tee >(cut -f 1-4 | tr '\t' '\n' > $in/deinterleaved/$sample.R1.fastq) \
  | cut -f 5-8 | tr '\t' '\n' > $in/deinterleaved/$sample.R2.fastq
done