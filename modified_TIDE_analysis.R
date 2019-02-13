require("Biostrings")
require("sangerseqR")
B<-c("A","C","G","T") #four bases, in the order that is always used by sangerseqR package
patched.readsangerseq<-function(filename)
  #This is a slightly modified version of readsangerseq() in the sangerseqR package
  #It fixes a problem with reading some .ab1 files, which appear to have an aberrant last 
  #character in the sequence strings, which sangerseq() cannot cope with. It returns a sangerseq object.
{ require(sangerseqR)
  fc <- file(filename, open = "rb")#use "rb" to open a binary file. Then the bytes of the file won't be encoded when you read them.
  rawdata <- readBin(fc, what = "raw", n = 1.2 * file.info(filename)$size)
  close(fc)
  filetype <- suppressWarnings(rawToChar(rawdata[1:4]))
  if (filetype == ".scf") {
    seq <- read.scf(filename)
  }
  else if (filetype == "ABIF") {
    seq <- read.abif(filename)
    l<-nchar(seq@data$PBAS.1)
    if(! substr(seq@data$PBAS.1,l,l) %in% LETTERS) { #if last character is not uppercase text
      seq@data$PBAS.1<-substr(seq@data$PBAS.1,1,l-1)
    }
    l<-nchar(seq@data$PBAS.2)
    if(! substr(seq@data$PBAS.2,l,l) %in% LETTERS) { #if last character is not uppercase text
      seq@data$PBAS.2<-substr(seq@data$PBAS.2,1,l-1)
    }
  }
  else stop("Invalid File.")
  return(sangerseq(seq))
}
control<-patched.readsangerseq(control_file)
sample<-patched.readsangerseq(experimental_file)
#extract primary sequences as called by sequencer:
sequence_ctr <- primarySeq(control)
sequence_mut <- primarySeq(sample)
#adjust seqend to shortest sequence if necessary:
seqend<-min(seqend,length(sequence_ctr), length(sequence_mut))
#extract control data:
if (control@primarySeqID == "From scf file") {
  if(peakPosMatrix(control)[1,1]==0){peakPosMatrix(control)[1,1] <- 1}
  peak_ctr_loc <- peakPosMatrix(control)[,1]
} else if (control@primarySeqID == "From ab1 file") { 
  if(peakPosMatrix(control)[1,1]==1){peakPosMatrix(control)[1,1] <- 2}
  peak_ctr_loc <- peakPosMatrix(control)[,1]-1 #for some reason sangerseq() added 1, so we substract it again
}

peak_ctr_height <- traceMatrix(control)[peak_ctr_loc,] #matrix with a column for each base 
peak_ctr_height <- peak_ctr_height[1:seqend,]
peak_ctr_height[is.na(peak_ctr_height)]<-0 #set NAs to 0
colnames(peak_ctr_height)<-B

#extract experimental data:
if (sample@primarySeqID == "From scf file") {
  if(peakPosMatrix(sample)[1,1]==0){peakPosMatrix(sample)[1,1] <- 1}
  peak_mut_loc <- peakPosMatrix(sample)[,1]
} else if (sample@primarySeqID == "From ab1 file") { 
  if(peakPosMatrix(sample)[1,1]==1){peakPosMatrix(sample)[1,1] <- 2}
  peak_mut_loc <- peakPosMatrix(sample)[,1]-1 #sangerseq() added 1, we substract it again
}

peak_mut_height <- traceMatrix(sample)[peak_mut_loc,] #matrix with a column for each base 
peak_mut_height <- peak_mut_height[1:seqend,]
peak_mut_height[is.na(peak_mut_height)]<-0 #set NAs to 0
colnames(peak_mut_height)<-B


#control for wrongly not/extra annotated peaks
ctr_loc1 <- ctr_loc2 <- NA
ctr_loc1<- peak_ctr_loc[1:seqend]
ctr_loc2<- peak_ctr_loc[2:seqend]

mut_loc1 <- mut_loc2 <- NA
mut_loc1<- peak_mut_loc[1:seqend]
mut_loc2<- peak_mut_loc[2:seqend]


