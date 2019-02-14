# PCR_Amplicon_target_deep_seq
#This project contain some shell or python scripts used for target-deep-seq analysis.

#The CRESA-lpp.py script is for reference sequence indexing and mapping by BWA, SAM files are converted and sorted by Samtools. Indels and SNPs are called by VarScan2. The outputs for each sample should be indel and snp txt files.

#The indel types and frequencies are then cataloged in a text output format at each base. For each treatment group, the average background lesion frequencies (based on lesion type, position and frequency) of the triplicate-negative control group are subtracted to obtain the nuclease-dependent lesion frequencies by the indel_background_filtering.R Script.

#The Tcap_pacbio_analysis.sh shell script is used for TCAP pacbio long reads sequencing analysis. 


