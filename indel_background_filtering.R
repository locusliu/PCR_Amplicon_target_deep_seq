setwd("F:/Wolfelab/eric data/12-19-2016/indel")
library(dplyr)
library(stats)
library(base)
background_filter<-function(NegCtrl1,NegCtrl2,NegCtrl3,Treat){
  NegCtrl1_raw<-read.table(NegCtrl1,header = TRUE)
  NegCtrl1_1<-NegCtrl1_raw[, c(1:6)]
  NegCtrl1_max<-aggregate(Reads1 ~ Chrom, NegCtrl1_raw, max)
  NegCtrl1_2<-dplyr::left_join(NegCtrl1_1,NegCtrl1_max,by="Chrom")
  NegCtrl1_3<-dplyr::mutate(NegCtrl1_2,NegCtrl1_rate=Reads2/Reads1.y)
  NegCtrl1_3$CPRC<-with(NegCtrl1_3, paste(Chrom, Position, Ref, Cons, sep="_"))
  NegCtrl1<-data.frame("CPRC"=NegCtrl1_3$CPRC,"NegCtrl1_rate"=NegCtrl1_3$NegCtrl1_rate)
  
  NegCtrl2_raw<-read.table(NegCtrl2,header = TRUE)
  NegCtrl2_1<-NegCtrl2_raw[, c(1:6)]
  NegCtrl2_max<-aggregate(Reads1 ~ Chrom, NegCtrl2_raw, max)
  NegCtrl2_2<-dplyr::left_join(NegCtrl2_1,NegCtrl2_max,by="Chrom")
  NegCtrl2_3<-dplyr::mutate(NegCtrl2_2,NegCtrl2_rate=Reads2/Reads1.y)
  NegCtrl2_3$CPRC<-with(NegCtrl2_3, paste(Chrom, Position, Ref, Cons, sep="_"))
  NegCtrl2<-data.frame("CPRC"=NegCtrl2_3$CPRC,"NegCtrl2_rate"=NegCtrl2_3$NegCtrl2_rate)
  
  NegCtrl3_raw<-read.table(NegCtrl3,header = TRUE)
  NegCtrl3_1<-NegCtrl3_raw[, c(1:6)]
  NegCtrl3_max<-aggregate(Reads1 ~ Chrom, NegCtrl3_raw, max)
  NegCtrl3_2<-dplyr::left_join(NegCtrl3_1,NegCtrl3_max,by="Chrom")
  NegCtrl3_3<-dplyr::mutate(NegCtrl3_2,NegCtrl3_rate=Reads2/Reads1.y)
  NegCtrl3_3$CPRC<-with(NegCtrl3_3, paste(Chrom, Position, Ref, Cons, sep="_"))
  NegCtrl3<-data.frame("CPRC"=NegCtrl3_3$CPRC,"NegCtrl3_rate"=NegCtrl3_3$NegCtrl3_rate)
  
  NegCtrl1_NegCtrl2<-dplyr::full_join(NegCtrl1,NegCtrl2,by="CPRC")
  NegCtrl1_NegCtrl2_NegCtrl3<-dplyr::full_join(NegCtrl1_NegCtrl2,NegCtrl3,by="CPRC")
  NegCtrl1_NegCtrl2_NegCtrl3[is.na(NegCtrl1_NegCtrl2_NegCtrl3)]<-0
  NegCtrl1_NegCtrl2_NegCtrl3_total<-dplyr::mutate(NegCtrl1_NegCtrl2_NegCtrl3,average_rate=(NegCtrl1_rate+NegCtrl2_rate+NegCtrl3_rate)/3)
  
  Treat_raw<-read.table(Treat,header = TRUE)
  Treat_1<-Treat_raw[, c(1:6)]
  Treat_max<-aggregate(Reads1 ~ Chrom, Treat_raw, max)
  Treat_2<-dplyr::left_join(Treat_1,Treat_max,by="Chrom")
  Treat_3<-dplyr::mutate(Treat_2,Treat_rate=Reads2/Reads1.y)
  Treat_3$CPRC<-with(Treat_3, paste(Chrom, Position, Ref, Cons, sep="_"))
  
  Treat_NegCtrl1_NegCtrl2_NegCtrl3<-dplyr::full_join(Treat_3,NegCtrl1_NegCtrl2_NegCtrl3_total,by="CPRC")
  Treat_NegCtrl1_NegCtrl2_NegCtrl3[is.na(Treat_NegCtrl1_NegCtrl2_NegCtrl3)]<-0
  Treat_indel_rate<-dplyr::mutate(Treat_NegCtrl1_NegCtrl2_NegCtrl3,Treat_indel_percentage=Treat_rate-average_rate)
  Treat_indel<-aggregate(Treat_indel_percentage ~ Chrom, Treat_indel_rate, sum)
  Treat_indel$Treat_indel_percentage[Treat_indel$Treat_indel_percentage<0]<-0
  
  
  Treat_summary<-merge(Treat_max,Treat_indel)
  
  return(Treat_summary)
  
}


