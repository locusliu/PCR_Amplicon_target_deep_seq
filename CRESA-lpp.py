#!/usr/bin/env python
# --*-- coding=utf-8 --*--

"""
 *                             _ooOoo_
 *                            o8888888o
 *                            88" . "88
 *                            (| -_- |)
 *                            O\  =  /O
 *                         ____/`---'\____
 *                       .'  \\|     |//  `.
 *                      /  \\|||  :  |||//  \
 *                     /  _||||| -:- |||||-  \
 *                     |   | \\\  -  /// |   |
 *                     | \_|  ''\---/''  |   |
 *                     \  .-\__  `-`  ___/-. /
 *                   ___`. .'  /--.--\  `. . __
 *                ."" '<  `.___\_<|>_/___.'  >'"".
 *               | | :  `- \`.;`\ _ /`;.`/ - ` : | |
 *               \  \ `-.   \_ __\ /__ _/   .-` /  /
 *          ======`-.____`-.___\_____/___.-`____.-'======
 *                             `=---='
 *          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 *                     佛祖保佑        永无BUG
"""
##----INTRO-----------##
AppName = 'CRESA'
AppAuthor = 'Pengpeng LiU'
AppDate = 'May 05, 2016'
AppFullName = 'CRISPR_Editing_Sequencing_Analysis'
AppPurpose = 'This program is for CRISPR sequencing analysis.'

##----START-----------##
import time, sys
print '\n------------------------------------------'
StartTime = AppAuthor + ':' + ' <BEGIN@'+ time.strftime("%Y-%m-%d %X", time.localtime())+ '>'
print '|python ' + sys.argv[0] + ' ' + sys.argv[1] + ' ' + sys.argv[2] + '\n|' + StartTime
print '|Check python 2.7 and package: os, commands, pysam, numpy.'
print '|Check bwa version 0.7.10, fastqc v0.11.2'

##----PREPARE---------##
import os, commands, pysam
import numpy as np

##----MAIN------------##
#-Input----#
def FUN_Input():
	OneInput_D_ = '../Input/' + AppName.split('.')[0] + '_' + sys.argv[1] + '/' + sys.argv[2] + '.Input'; OneInputFile_ = open(OneInput_D_, 'r').readlines()
	BasicInput_D_ = '../Input/' + AppName.split('.')[0] + '_' + sys.argv[1] + '/' + sys.argv[1] + '.Input'; BasicInputFile_ = open(BasicInput_D_, 'r').readlines()
	InputFile_ = [x_.split('\n')[0] for x_ in BasicInputFile_ if len(x_.split()) != 0] + [x_.split('\n')[0] for x_ in OneInputFile_ if len(x_.split()) != 0]
	AllKey_ = [x.split('<>')[0] for x in InputFile_]
	AllValue_ = [x.split('<>')[1:] for x in InputFile_]
	Input_ = dict(zip(AllKey_, AllValue_))
	return Input_

def FUN_Input2(BatchID_, SamplName_):
	OneInput_D_ = '../Input/' + AppName.split('.')[0] + '_' + BatchID_ + '/' + SamplName_ + '.Input'; OneInputFile_ = open(OneInput_D_, 'r').readlines()
	BasicInput_D_ = '../Input/' + AppName.split('.')[0] + '_' + BatchID_ + '/' + BatchID_ + '.Input'; BasicInputFile_ = open(BasicInput_D_, 'r').readlines()
	InputFile_ = [x_.split('\n')[0] for x_ in BasicInputFile_ if len(x_.split()) != 0] + [x_.split('\n')[0] for x_ in OneInputFile_ if len(x_.split()) != 0]
	AllKey_ = [x.split('<>')[0] for x in InputFile_]
	AllValue_ = [x.split('<>')[1:] for x in InputFile_]
	Input_ = dict(zip(AllKey_, AllValue_))
	return Input_

#Input_ = FUN_Input2('151103', 'E1')

#-Basic----#

#-Function-#
#--common--
def fun_MakeDir(Path_):
	Path_ = Path_.strip(); Path_ = Path_.rstrip("\\")
	if not os.path.exists(Path_):
		os.makedirs(Path_)
	return Path_

def fun_AllAP(F_, Suffi_ = ''):
	AllFileName_ = os.listdir(F_)
	All_AP_ = [F_ + x_ for x_ in AllFileName_ if x_[0] != '.']
	AllSuffi_AP_ = All_AP_ if Suffi_ == '' else [x_ for x_ in All_AP_ if x_.endswith(Suffi_)] 
	return AllSuffi_AP_

def fun_Write(File_, File_D_):
	Out_ = open(File_D_, 'w')
	Out_.writelines(File_)
	Out_.close()

def fun_PrintTime(OrderStartTime_ = '', OrderName_ = '', Symbol_ = '+'):
	if OrderStartTime_ == '' and OrderName_ == '' and Symbol_ == '+':
		Time_ = time.strftime("%X", time.localtime())
		return Time_
	else:
		OrderStartTime_ = '+'*(13 - len(Symbol_)) if OrderStartTime_ == '' else '<' + OrderStartTime_ + '>' + '-'*(3 - len(Symbol_))
		Time_ = '|' + Symbol_ + OrderStartTime_ + '<' + time.strftime("%X", time.localtime()) + '>: ' + OrderName_
		print Time_

def fun_Md5Sum(File_D_):
	Md5Sum_ = commands.getstatusoutput('md5sum ' + File_D_)[1].split()[0]
	return Md5Sum_

def fun_Dict2StrList(Dict_):
	KeySort_ = Dict_.keys(); KeySort_.sort()
	StrList_ = [str(x_) + ':' + str(Dict_[x_]) + '\n' for x_ in KeySort_]
	return StrList_

def fun_CountRepea(List_):
	UniquEleme_ = set(List_)
	CountRepeaInfor_ = []
	for UE_ in UniquEleme_:
		CountRepeaInfor_.append(str(UE_) + ':' + str(List_.count(UE_)) + '\t')
	return CountRepeaInfor_

def fun_AddWrite(File_, File_D_):
	Out_ = open(File_D_, 'a')
	Out_.writelines(File_)
	Out_.close()

def fun_ThousSign(Numbe_):
	return str(format(int(Numbe_), ','))

def fun_FileSize(File_D_):
	import os
	FileSize_ = os.path.getsize(File_D_)
	Unit_ = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
	UnitOrder_ = 0
	while len(str(FileSize_)) >= 5:
		FileSizePrevi_ = FileSize_
		UnitOrderPrevi_ = UnitOrder_
		FileSize_ = round(FileSize_/1024.0, 1)
		UnitOrder_ += 1
	return str(FileSizePrevi_) + ' ' + Unit_[UnitOrderPrevi_]

def fun_LineLengt(File_D_, LineNumbe_):
	import os
	File_ = open(File_D_)
	Index_ = 0
	for Line_ in File_:
		LineLengt_ = len(Line_.rstrip())
		Index_ += 1
		if Index_ > LineNumbe_ - 1:
			break
	return LineLengt_

#--
def FuN_RunComma(Log_F_, CommaName_, Progr_O_ = ''):
	if Progr_O_ != '':
		fun_Write(Progr_O_, Log_F_ + CommaName_ + '.sh')
		Bash_O_ = 'bash '+ Log_F_ + CommaName_ + '.sh'
		RunBash_O_ = '@' + time.strftime("%Y-%m-%d %X", time.localtime()) + '\n' + CommaName_ + ':\n' + Bash_O_ + '\n'
		fun_AddWrite(RunBash_O_, Log_F_ + 'Command.txt')		
		os.system(Bash_O_ + ' > ' + Log_F_ + CommaName_ + '.log 2>&1')	
	else:
		RunComma_O_ = '@' + time.strftime("%Y-%m-%d %X", time.localtime()) + '\n' + CommaName_ + '\n'
		fun_AddWrite(RunComma_O_, Log_F_ + 'Command.txt')

def FuN_RunStatu(Log_F_, CommaName_, Finis_ = 0):
	RunStatu_D_ = Log_F_ + CommaName_
	if Finis_ == 0:
		fun_Write('', RunStatu_D_)
	else:
		os.system('rm ' + RunStatu_D_)

def FuN_OrderStart(Log_F_):
	OrderStart_ = '\nCommand START@' + time.strftime("%Y-%m-%d %X", time.localtime()) + '\n'
	fun_AddWrite(OrderStart_, Log_F_ + 'Command.txt')

def FuN_OrderEnd(Input_, SamplName_, Log_F_):
	OrderEnd_ = 'Command  END@' + time.strftime("%Y-%m-%d %X", time.localtime()) + '\n\n'
	fun_AddWrite(OrderEnd_, Log_F_ + 'Command.txt')
	EndTime_ = AppAuthor + ':' + ' <END  @' + time.strftime("%Y-%m-%d %X", time.localtime())+ '>\n'
	DoneFile_ = [StartTime + '\n'] + fun_Dict2StrList(Input_) + [EndTime_] + ['DONE!']
	fun_Write(DoneFile_, Log_F_ +  'DONE@' + time.strftime("%Y-%m-%d %X", time.localtime()) + '.txt')

#--Workflow Standard--
def FUn_FastQC(Input_, Log_F_, FastQC_F_, Type_, SinglOrPairRead1_D_, PairRead2_D_ = ''):
	PairRead2_D_ = ' ' + PairRead2_D_ if PairRead2_D_ != '' else ''
	FastQC_O_ = Input_['FastQC'][0] + ' -q --extract -o ' + FastQC_F_ + ' ' + SinglOrPairRead1_D_ + PairRead2_D_ 
	FuN_RunComma(Log_F_, 'FastQC_QualiyControl.' + Type_, FastQC_O_)
	fun_PrintTime('', 'FUn_FastQC(Type:' + Type_ + ')', '+++')

def Fun_FastQCStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_FastQCStand')
	FastQC_F_ = fun_MakeDir(Outpu_ + 'FastQC/')
	Type_ = 'Raw'
	SinglOrPairRead1_D_ = Input_['FastqLeft_D'][0]
	PairRead2_D_ = Input_['FastqRight_D'][0]
	FUn_FastQC(Input_, Log_F_, FastQC_F_, Type_, SinglOrPairRead1_D_, PairRead2_D_)
	fun_PrintTime(StartTime_, 'Fun_FastQCStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_FastQCStand', 1)

def FUn_BwaMap(Input_, SamplName_, Log_F_, BwaMapMap_D_, Refer_D_, SinglOrPairRead1_D_, PairRead2_D_ = ''):
	#Pa: Pair; Si: Single
	SinglOrPair_ = ['Pa', 'Si'][PairRead2_D_ == '']
	#BM_MA: Bwa Map _ Map
	BwaMapMap_O_ = Input_['Bwa'][0] + ''' mem -t 10 -R "@RG\\tID:''' + SamplName_ + '.BwaMap_' + SinglOrPair_ + '''\\tLB:Bwa''' + '''\\tPL:''' + Input_['Platf'][0] + '''\\tSM:''' + SamplName_ + '" ' + Refer_D_ + ' '+ SinglOrPairRead1_D_ + ' ' + PairRead2_D_ + ' > '+ BwaMapMap_D_
	FuN_RunComma(Log_F_, 'BwaMap_Map.' + ['Single', 'Pair'][SinglOrPair_ == 'Pa'], BwaMapMap_O_)
	fun_PrintTime('', 'FUn_BwaMap(SinglOrPair:' + SinglOrPair_ + ')', '+++')

def Fun_BwaMapStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_BwaMapStand')
	Refer_D_ = Input_['ProceServe_F'][2] + Input_['BatchID'][0] + '/Refer/' + Input_['FirstReferName'][0]
	SinglOrPairRead1_D_ = Input_['FastqLeft_D'][0]
	PairRead2_D_ = Input_['FastqRight_D'][0]
	BwaMapMap_D_ = fun_MakeDir(Outpu_ + 'BwaMap/') + 'Ma' + ['Pa', 'Si'][PairRead2_D_ == ''] + '.sam'
	FUn_BwaMap(Input_, SamplName_, Log_F_, BwaMapMap_D_, Refer_D_, SinglOrPairRead1_D_, PairRead2_D_)
	fun_PrintTime(StartTime_, 'Fun_BwaMapStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_BwaMapStand', 1)

def FUn_SamToolsSamToBam(Input_, Log_F_, Sam_D_, Bam_D_):
	SamToolsSamToBam_O_ = Input_['SamTools'][0] + ' view -bhS ' + Sam_D_ + ' -o ' + Bam_D_
	FuN_RunComma(Log_F_, 'SamTools_SamToBam', SamToolsSamToBam_O_)
	fun_PrintTime('', 'FUn_SamToolsSamToBam()', '+++')

def Fun_SamToolsSamToBamStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_SamToolsSamToBamStand')
	#SaToBa: Sam To Bam
	PairRead2_D_ = Input_['FastqRight_D'][0]
	BwaMapMap_D_ = Outpu_ + 'BwaMap/Ma' + ['Pa', 'Si'][PairRead2_D_ == ''] + '.sam'
	Bam_D_ = fun_MakeDir(Outpu_ + 'SamTools/') + 'SaToBa.bam'
	FUn_SamToolsSamToBam(Input_, Log_F_, BwaMapMap_D_, Bam_D_)
	fun_PrintTime(StartTime_, 'Fun_SamToolsSamToBamStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_SamToolsSamToBamStand', 1)

def FUn_InserSizeStandDevia(Input_, Bam_D_):
	InserSize_ = [int(x_) for x_ in commands.getstatusoutput(Input_['SamTools'][0] + ' view ' + Bam_D_ + '|head -100000|cut -f 9')[1].split() if x_ != '0']
#	InserSize_ = [int(x_) for x_ in commands.getstatusoutput(Input_['SamTools'][0] + ' view ' + Bam_D_ + '|cut -f 9')[1].split() if x_ != '0']
	InserSizeMean_ = round(np.mean([abs(x_) for x_ in InserSize_]), 1)
	StanDevia_ = round(np.std(InserSize_), 1)
	fun_PrintTime('', 'FUn_InserSizeStandDevia()', '+++')
	return 'Insert Size Mean:\t' + str(InserSizeMean_) + '\nStandard Deviation:\t' + str(StanDevia_)

def FUn_RawDataInfor(RawDataInfor_D_, Input_, SamplName_, ReferName_, Bam_D_, SinglOrPairRead1_D_, PairRead2_D_):
	RawDataInfor_ = 'Name:\t' + SamplName_ + '\nProcess:\t' + Input_['Proce'][0] + '\nReference:\t' + ReferName_ + '\nFastq1:\t' + os.path.basename(SinglOrPairRead1_D_) + '\nSize1:\t' + fun_FileSize(SinglOrPairRead1_D_) + '\nReadLength1:\t' + str(fun_LineLengt(SinglOrPairRead1_D_, 2)) + '\nmd5sum1:\t' + fun_Md5Sum(SinglOrPairRead1_D_) + '\nFastq2:\t' + os.path.basename(PairRead2_D_) + '\nSize2:\t' + fun_FileSize(PairRead2_D_) + '\nReadLength2:\t' + str(fun_LineLengt(PairRead2_D_, 2)) + '\nmd5sum2:\t' + fun_Md5Sum(PairRead2_D_) + '\n' + FUn_InserSizeStandDevia(Input_, Bam_D_) + '\n'
	fun_Write(RawDataInfor_, RawDataInfor_D_)
	fun_PrintTime('', 'FUn_RawDataInfor()', '+++')

def Fun_RawDataInforStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_RawDataInforStand')	
	FuN_RunComma(Log_F_, 'Fun_RawDataInforStand()')
	RawDataInfor_D_ = fun_MakeDir(Outpu_ + 'Summa/') + 'RawDataInfor.txt'
	ReferName_ = Input_['FirstReferName'][0]
	Bam_D_ = Outpu_ + 'SamTools/SaToBa.bam'
	SinglOrPairRead1_D_ = Input_['FastqLeft_D'][0]
	PairRead2_D_ = Input_['FastqRight_D'][0]
	FUn_RawDataInfor(RawDataInfor_D_, Input_, SamplName_, ReferName_, Bam_D_, SinglOrPairRead1_D_, PairRead2_D_)
	fun_PrintTime(StartTime_, 'Fun_RawDataInforStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_RawDataInforStand', 1)

def FUn_BamToolsHighQuali(Input_, Log_F_, Bam_D_, BamHighQuali_D_, MapQuali_):
	BamToolsHighQuali_O_ = Input_['BamTools'][0]+ ' filter -in ' + Bam_D_ + ''' -mapQuality ">=''' + MapQuali_ + '''" -out ''' + BamHighQuali_D_
	FuN_RunComma(Log_F_, 'BamTools_HighQualiy.' + MapQuali_, BamToolsHighQuali_O_)
	fun_PrintTime('', 'FUn_BamToolsHighQuali(MapQuali:' + MapQuali_ + ')', '+++')

def Fun_BamToolsHighQualiStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_BamToolsHighQualiStand')
	#SaToBa: Sam To Bam	
	Bam_D_ = Outpu_ + 'SamTools/SaToBa.bam'
	for MapQuali_ in Input_['MapQuali']:
		#BT_HiQ: BamTools _ High Quality (Score)
		BamHighQuali_D_ = fun_MakeDir(Outpu_ + 'BamTools/') + 'HiQ' + MapQuali_ + '.bam'
		FUn_BamToolsHighQuali(Input_, Log_F_, Bam_D_, BamHighQuali_D_, MapQuali_)
	fun_PrintTime(StartTime_, 'Fun_BamToolsHighQualiStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_BamToolsHighQualiStand', 1)

def FUn_BwaAlignInfor(BwaAlignInfor_D_, Input_, Outpu_, Bam_D_, SinglOrPairRead1_D_):
	BwaAlignInfor_ = 'Name\tReference\tAlignment Type\tSequenced Reads#\tUnique Aligned Reads#\tUnique Alignment Ratio\tNot Unique Aligned Reads#\tAligned Read#\tQuality Score\tHigh Quality Reads#\tAlignment Ratio\tLow Quality Reads#\n'
	for MapQuali_ in Input_['MapQuali']:
		BamHighQuali_D_ = Outpu_ + 'BamTools/HiQ' + MapQuali_ + '.bam'
		SequeRead_ = int(commands.getstatusoutput('cat '+ SinglOrPairRead1_D_ + '|wc -l')[1])/[2, 4][Input_['FastqRight_D'][0] == '']
#		Total Reads means: all left reads + all right reads
		UniquAlignRead_ = int(commands.getstatusoutput(Input_['SamTools'][0]+ ' view '+ BamHighQuali_D_ + '''| awk '$0!~/SA:Z/{print $0}'| wc -l''')[1])
		UniquAlignRatio_ = str(round(UniquAlignRead_/float(SequeRead_), 4)*100) + '%'
		AlignRead_ = int(commands.getstatusoutput(Input_['SamTools'][0] + ' view -c ' + Bam_D_)[1])
		HighQualiRead_ = int(commands.getstatusoutput(Input_['SamTools'][0] + ' view -c ' + BamHighQuali_D_)[1])
		HighQualiAlignRatio_ = str(round(HighQualiRead_/float(AlignRead_), 4)*100) + '%'
		BwaAlignInfor_ = BwaAlignInfor_ + Input_['SamplName'][0] + '\t' + Input_['FirstReferName'][0] + '\t' + ['Pa', 'Si'][Input_['FastqRight_D'] == ''] + '\t' + format(SequeRead_, ',') + '\t' + format(UniquAlignRead_, ',') + '\t' + UniquAlignRatio_ + '\t' + format((SequeRead_ - UniquAlignRead_), ',') + '\t' + format(AlignRead_, ',') + '\t' + MapQuali_ + '\t' + format(HighQualiRead_, ',') + '\t'+ HighQualiAlignRatio_+ '\t' + format((AlignRead_ - HighQualiRead_), ',') + '\n'
	fun_Write(BwaAlignInfor_, BwaAlignInfor_D_)
	fun_PrintTime('', 'FUn_BwaAlignInfor(MapQuali:' + MapQuali_ + ')', '+++')

def Fun_BwaAlignInforStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_BwaAlignInforStand')
	FuN_RunComma(Log_F_, 'Fun_BwaAlignInforStand()')
	BwaAlignInfor_D_ = Outpu_ + 'Summa/BwaAlignInfor.txt'
	Bam_D_ = Outpu_ + 'SamTools/SaToBa.bam'
	SinglOrPairRead1_D_ = Input_['FastqLeft_D'][0]
	FUn_BwaAlignInfor(BwaAlignInfor_D_, Input_, Outpu_, Bam_D_, SinglOrPairRead1_D_)
	fun_PrintTime(StartTime_, 'Fun_BwaAlignInforStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_BwaAlignInforStand', 1)

def FUn_SamToolsSortIndex(Input_, Log_F_, Bam_D_, BamSortIndex_D_):
	SamToolsSort_O_ = Input_['SamTools'][0] + ' sort ' + Bam_D_ + ' ' + BamSortIndex_D_.split('.bam')[0]
	SamToolsIndex_O_ = Input_['SamTools'][0] + ' index ' + BamSortIndex_D_ 
	FuN_RunComma(Log_F_, 'SamTools_Sort', SamToolsSort_O_)
	FuN_RunComma(Log_F_, 'SamTools_Index', SamToolsIndex_O_)
	fun_PrintTime('', 'FUn_SamToolsSortIndex()', '+++')

def Fun_SamToolsSortIndexStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_SamToolsSortIndexStand')
	#SaToBa: Sam To Bam; SoIn: Sort Index
	Bam_D_ = Outpu_ + 'SamTools/SaToBa.bam'
	BamSortIndex_D_ = Outpu_ + 'SamTools/SoIn.bam'
	FUn_SamToolsSortIndex(Input_, Log_F_, Bam_D_, BamSortIndex_D_)
	fun_PrintTime(StartTime_, 'Fun_SamToolsSortIndexStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_SamToolsSortIndexStand', 1)

def FUn_SamToolsMultiPileUp(Input_, Log_F_, Refer_D_, BamSortIndex_D_, MultiPileUp_D_):
	SamToolsMultiPileUp_O_ = Input_['SamTools'][0] + ' mpileup' + ['', ' -BQ0 -d10000000'][int(Input_['UnlimRead'][0])] + ' -f ' + Refer_D_ + ' ' + BamSortIndex_D_ + ' > ' + MultiPileUp_D_
	FuN_RunComma(Log_F_, 'SamTools_MultiplePileUp' + ['', '.Unlimit'][int(Input_['UnlimRead'][0])], SamToolsMultiPileUp_O_)
	fun_PrintTime('', 'FUn_SamToolsMultiPileUp()', '+++')

def Fun_SamToolsMultiPileUpStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_SamToolsMultiPileUpStand')
	Refer_D_ = Input_['ProceServe_F'][2] + Input_['BatchID'][0] + '/Refer/' + Input_['FirstReferName'][0]
	BamSortIndex_D_ = Outpu_ + 'SamTools/SoIn.bam'
	MultiPileUp_D_ = Outpu_ + 'SamTools/MuPiUp' + ['', 'Un'][int(Input_['UnlimRead'][0])] + '.mpu'
	FUn_SamToolsMultiPileUp(Input_, Log_F_, Refer_D_, BamSortIndex_D_, MultiPileUp_D_)
	fun_PrintTime(StartTime_, 'Fun_SamToolsMultiPileUpStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_SamToolsMultiPileUpStand', 1)

def FUn_VarScan2IndelReadCountConseCallsSnp(Input_, Log_F_, VarScan2_F_, MultiPileUp_D_, BaseQuali_):
	UnlimRead_ = ['', 'Un'][int(Input_['UnlimRead'][0])]
	#VS2_InBaQ: VarScan2 _ Indel Base Quality	
	VarScan2Indel_D_ = VarScan2_F_ + UnlimRead_ + 'InBaQ' + BaseQuali_ + '.txt'
	VarScan2Indel_O_ = Input_['VarScan2'][0] + ' pileup2indel ' + MultiPileUp_D_ + ' --min-var-freq 0.0001 --min-avg-qual ' + BaseQuali_ + ' --p-value 0.05 > ' + VarScan2Indel_D_
	FuN_RunComma(Log_F_, 'VarScan2_IndelBaseQuality.' + BaseQuali_, VarScan2Indel_O_)
	#VS2_ReCoBaQ: VarScan2 _ Read Count Base Quality
	VarScan2ReadCount_D_ = VarScan2_F_ + UnlimRead_ + 'ReCoBaQ' + BaseQuali_ + '.txt'
	VarScan2ReadCount_O_ = Input_['VarScan2'][0] + ' readcounts ' + MultiPileUp_D_ + ' --min-base-qual ' + BaseQuali_ + ' --output-file ' + VarScan2ReadCount_D_
	FuN_RunComma(Log_F_, 'VarScan2_ReadCountBaseQuality.' + BaseQuali_, VarScan2ReadCount_O_)
	#VS2_CoCaBaQ: VarScan2 _ Consensus Calls Base Quality
	VarScan2ConseCalls_D_ = VarScan2_F_ + UnlimRead_ + 'CoCaBaQ' + BaseQuali_ + '.txt'
	VarScan2ConseCalls_O_ = Input_['VarScan2'][0] + ' pileup2cns ' + MultiPileUp_D_ + ' --min-var-freq 0.0001 --min-avg-qual ' + BaseQuali_ + ' --p-value 0.05 > ' + VarScan2ConseCalls_D_
	FuN_RunComma(Log_F_, 'VarScan2_ConsenusCallsBaseQuality.' + BaseQuali_, VarScan2ConseCalls_O_)
	#VS2_SnBaQ: VarScan2 _ SNP Base Quality
	VarScan2Snp_D_ = VarScan2_F_ + UnlimRead_ + 'SnBaQ'  + BaseQuali_ + '.txt'
	VarScan2Snp_O_ = Input_['VarScan2'][0] + ' pileup2snp ' + MultiPileUp_D_ + ' --min-var-freq 0.0001 --min-avg-qual ' + BaseQuali_ + ' --p-value 0.05 > ' + VarScan2Snp_D_
	FuN_RunComma(Log_F_, 'VarScan2_SnpBaseQuality.' + BaseQuali_, VarScan2Snp_O_)
	fun_PrintTime('', 'FUn_VarScan2IndelReadCountConseCallsSnp(BaseQuali:' + BaseQuali_ + ['', ', UnlimRead:' + UnlimRead_][int(Input_['UnlimRead'][0])] + ')', '+++')

def Fun_VarScan2IndelReadCountConseCallsSnpStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_VarScan2IndelReadCountConseCallsSnpStand')
	VarScan2_F_ = fun_MakeDir(Outpu_ + 'VarScan2/')
	MultiPileUp_D_ = Outpu_ + 'SamTools/MuPiUp' + ['', 'Un'][int(Input_['UnlimRead'][0])] + '.mpu'
	for BaseQuali_ in Input_['BaseQuali']:
		FUn_VarScan2IndelReadCountConseCallsSnp(Input_, Log_F_, VarScan2_F_, MultiPileUp_D_, BaseQuali_)
	fun_PrintTime(StartTime_, 'Fun_VarScan2IndelReadCountConseCallsSnpStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_VarScan2IndelReadCountConseCallsSnpStand', 1)

#Refer data and result pick
def FUn_ReferIndelInfor(ReferIndeliInfor_D_, Input_, SamplName_, Outpu_):
	ReferIndeliInfor_ = 'BatchID\tRefer\tReferDir\tSampleName\tProcess\tRawDataInforDir\tAlignmentInforDir\tUnlimit\tBaseQuality\tVarScan2IndelDir\n'
	Refer_D_ = Input_['ProceServe_F'][2] + Input_['BatchID'][0] + '/Refer/' + Input_['FirstReferName'][0]
	BwaAlignInfor_D_ = Outpu_ + 'Summa/BwaAlignInfor.txt'
	RawDataInfor_D_ = Outpu_ + 'Summa/RawDataInfor.txt'
	for BaseQuali_ in Input_['BaseQuali']:
		VarScan2Indel_D_ = Outpu_ + 'VarScan2/InBaQ' + BaseQuali_ + ['', 'Un'][int(Input_['UnlimRead'][0])] + '.txt'
		ReferIndeliInfor_ = ReferIndeliInfor_ + Input_['BatchID'][0] + '\t' + Input_['FirstReferName'][0] + '\t' + Refer_D_ + '\t' + SamplName_ + '\t' + Input_['Proce'][0] + '\t' + RawDataInfor_D_ + '\t' + BwaAlignInfor_D_ + '\t' + Input_['UnlimRead'][0] + '\t' + BaseQuali_ + '\t' + VarScan2Indel_D_ + '\n'
	fun_Write(ReferIndeliInfor_, ReferIndeliInfor_D_)
	fun_PrintTime('', 'FUn_ReferIndelInfor()', '+++')

def Fun_ReferIndelInforStand(Input_, SamplName_, Outpu_, Log_F_):
	StartTime_ = fun_PrintTime()
	FuN_RunStatu(Log_F_, 'Fun_ReferIndelInforStand')
	FuN_RunComma(Log_F_, 'Fun_ReferIndelInforStand()')
	ReferIndeliInfor_D_ = Outpu_ + 'Summa/ReferIndeliInfor.txt'
	FUn_ReferIndelInfor(ReferIndeliInfor_D_, Input_, SamplName_, Outpu_)
	fun_PrintTime(StartTime_, 'Fun_ReferIndelInforStand()', '++')
	FuN_RunStatu(Log_F_, 'Fun_ReferIndelInforStand', 1)

#--main----
#Input_ = FUN_Input2('150706And', 'D15-5269-1486L')

def FUN_MAIN(Input_):
#--Standard Workflow--
	if (Input_['WorkfStand'][0] == '1'):
		StartTime_ = fun_PrintTime()
		SamplName_ = Input_['SamplName'][0]
		Outpu_ = fun_MakeDir(Input_['Proje_AP'][0] + 'Outpu/' + AppName.split('.')[0] + '_' + Input_['BatchID'][0] + '/' + SamplName_) + '/'
		Log_F_ = fun_MakeDir(Outpu_ + 'Log/')
		FuN_OrderStart(Log_F_)
		Fun_FastQCStand(Input_, SamplName_, Outpu_, Log_F_)
		Fun_BwaMapStand(Input_, SamplName_, Outpu_, Log_F_)
		Fun_SamToolsSamToBamStand(Input_, SamplName_, Outpu_, Log_F_)
		Fun_SamToolsSortIndexStand(Input_, SamplName_, Outpu_, Log_F_)
		Fun_RawDataInforStand(Input_, SamplName_, Outpu_, Log_F_)
		Fun_BamToolsHighQualiStand(Input_, SamplName_, Outpu_, Log_F_)
		Fun_BwaAlignInforStand(Input_, SamplName_, Outpu_, Log_F_)
		Fun_SamToolsMultiPileUpStand(Input_, SamplName_, Outpu_, Log_F_)
		Fun_VarScan2IndelReadCountConseCallsSnpStand(Input_, SamplName_, Outpu_, Log_F_)
		Fun_ReferIndelInforStand(Input_, SamplName_, Outpu_, Log_F_)
		FuN_OrderEnd(Input_, SamplName_, Log_F_)
		fun_PrintTime(StartTime_, 'Workflow Standard')

#-Process--#
Input = FUN_Input()
FUN_MAIN(Input)


 
print '|' + AppAuthor + ':' + ' <END  @' + time.strftime("%Y-%m-%d %X", time.localtime()) + '>'
print '------------------------------------------\n'

fun_AddWrite('\n' + sys.argv[0] + ' ' + sys.argv[1] + ' ' + sys.argv[2] + '\n', 'nohup.out2')

##----TEST------------##
#bwa index -a bwtsw hg38.fa
