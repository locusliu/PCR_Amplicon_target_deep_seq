#!/bin/bash
# indexing
minimap2 tcap.fasta -d tcap.mmi

# mapping
minimap2 -a minimap2/tcap.mmi MB_unedited/Consensus_ROI/reads_of_insert.fastq | samtools view -bhS | samtools sort  > MB_unedited/output/MB_unedited_minimap2.sorted.bam

# convert sam to bam and remove low mapped reads
minimap2 -a minimap2/tcap.mmi MB_edited/Consensus_ROI/reads_of_insert.fastq | samtools view -bhS -q 30 | samtools sort  > MB_edited/output/MB_edited.highQ.sorted.bam

# Bam file indexing
samtools index MB_edited/output/MB_edited.highQ.sorted.bam

# launch IGV to visualize mapped reads
/usr/lib/jvm/java-8-oracle/jre/bin/java  -jar '/home/usr/bin/igv.jar'

# ------filter reads by length (800~1200bp)-------------------------------------------------------------------------------------------------------------------------------------------

#sorting reads by length
awk 'NR%4==1{a=$0} NR%4==2{b=$0} NR%4==3{c=$0} NR%4==0&&length(b)<1200&&length(b)>700{print a"\n"b"\n"c"\n"$0;}' ~/rawdata/cas9_deep_seq/MMEJ/PacBioData/MB_unedited/Consensus_ROI/reads_of_insert.fastq > ~/rawdata/cas9_deep_seq/MMEJ/PacBioData/MB_unedited/MB_edited_800_1200.fastq

#Alignment, converting and sorting
minimap2 -a minimap2/tcap.mmi MB_unedited/MB_edited_800_1200.fastq | samtools view -bhS -q 30 | samtools sort  > MB_unedited/output/MB_edited_800_1200.highQ.sorted.bam

#bam file indexing
samtools index MB_unedited/output/MB_edited_800_1200.highQ.sorted.bam

# launch IGV to visualize mapped reads
/usr/lib/jvm/java-8-oracle/jre/bin/java  -jar '/home/usr/bin/igv.jar'
