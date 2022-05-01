#! /bin/bash


echo '===================================================================='
fastqs=()
if [ ! -d Merged ]
	then
		mkdir Merged
fi
echo $calid
Sampid=""
####   CURRENTLY FOR WGS from paired fastq
for file in *
do
	if [[ $file == *.merged.R1.001.fastq.gz ]]
		then
		## MiSeq/paired WGS
		# Sampid=$(echo $file | rev | cut -d "_" -f 3- | rev)
		Sampid=$(echo $file | cut -d "." -f 1 )
		echo $file
		if [ -f ${Sampid}.merged.R2.001.fastq.gz ] # _R2_001.fastq.gz ]
			then
			echo ${Sampid}.merged.R2.001.fastq.gz # _R2_001.fastq.gz
			echo 0
			echo $Sampid
			echo $Sampid &>> Mergeinfo.txt
			bash /mnt/g/MU_WW/BBTools/BBMap/bbmerge.sh qtrim=t in1=$file in2=${Sampid}.merged.R2.001.fastq.gz  out=$Sampid.merge.fq outu1=$Sampid.un1.fq outu2=$Sampid.un2.fq &>> Mergeinfo.txt
			echo '  ' &>> Mergeinfo.txt
			# mv $file ./Merged/$file
			# mv ${Sampid}_R2_001.fastq.gz ./Merged/${Sampid}_R2_001.fastq.gz
			cat $Sampid.merge.fq $Sampid.un1.fq $Sampid.un2.fq > $Sampid.all.fq
			# cutadapt -g file:/mnt/g/MU_WW/SARS2/Wisconsin/QIAseqDIRECTSARSCoV2_for_plus.fasta -e .2 -q 20,20 --trim-n -m 30 --report minimal -o $Sampid.cut1.fq $Sampid.all.fq &>> Cutinfo.txt
			# cutadapt -a file:/mnt/g/MU_WW/SARS2/Wisconsin/QIAseqDIRECTSARSCoV2_rev_plus.fasta -e .2 -q 20,20 --trim-n -m 30 --report minimal -o $Sampid.cut2.fq $Sampid.cut1.fq &>> Cutinfo.txt
			# cutadapt -q 20,20 --trim-n -m 30 --report minimal -o $Sampid.cut.fq $Sampid.cut2.fq &>> Cutinfo.txt
			echo $Sampid
			/mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.all.fq --output $Sampid.collapsed.fa --sizeout --minuniquesize 1
			echo $Sampid &>> MMinfo.txt
			minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta $Sampid.collapsed.fa -o $Sampid.wg.sam --sam-hit-only &>> MMinfo.txt
			echo '  ' &>> MMinfo.txt
			echo '||||||||||||||||||||||||||||||||||||||||'
		fi
	 fi
 done

python3 /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 1 --max_covar 2 --AAcentered 1 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --mp 1 --chim_rm 0 --deconv 0

echo 'SAM processing done'
