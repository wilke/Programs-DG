#! /bin/bash


echo '===================================================================='
fastqs=()
if [ ! -d Merged ]
	then
		mkdir Merged
fi
# gzip -d *.gz
echo $calid
Sampid=""
####   CURRENTLY FOR WGS from paired fastq
for file in *
do
	if [[ $file == *_001.fastq.gz ]]
		then
		
		## MiSeq/paired WGS
		echo 0
		echo $Sampid
		if [[ $Sampid == $(echo $file | rev | cut -d "_" -f 3- | rev) ]]
			then
			# echo 2
			# Sampid=$(echo $file| cut -d "." -f 1 )
			fastqs[1]=$file
			# echo ${fastqs[*]}
			echo $Sampid
			# echo $Sampid &>> Mergeinfo.txt
			#/mnt/g/MU_WW/vsearch/bin/vsearch --fastq_mergepairs ${fastqs[0]} --reverse ${fastqs[1]} --fastqout $Sampid.merge.fq --fastqout_notmerged_fwd $Sampid.nmfwd.fq --fastqout_notmerged_rev $Sampid.nmrev.fq &>> Mergeinfo.txt #  
			bash /mnt/g/MU_WW/BBTools/BBMap/bbmerge.sh in1=${fastqs[0]} in2=${fastqs[1]}  out=$Sampid.merge.fq outu1=$Sampid.un1.fq outu2=$Sampid.un2.fq &>> $Sampid.mergestats.txt
			# echo '  ' &>> Mergeinfo.txt
			mv ${fastqs[0]} ./Merged/${fastqs[0]}
			mv ${fastqs[1]} ./Merged/${fastqs[1]}
			# Sampid=$(echo $file | cut -d "." -f 1-4 )
			cat $Sampid.merge.fq $Sampid.un1.fq $Sampid.un2.fq > $Sampid.all.fq
			echo $Sampid
			# echo $Sampid &>> derepinfo.txt
			# /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.all.derep.fa --sizeout --minuniquesize 1
			#/mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.all.fq --output $Sampid.derep1.fa --sizeout --minuniquesize 1 &>> derepinfo.txt
			fastx_collapser -i $Sampid.all.fq -o $Sampid.collapsed.fa &>> $Sampid.colstats.txt
			# echo '   ' &>> derepinfo.txt
			# Sampid=$(echo $file| cut -d "_" -f 1-3 )
			echo $Sampid &>> MMinfo.txt
			# bowtie2 -x /mnt/g/MU_WW/SARS2/GP -f $Sampid.all.derep.fa -S $Sampid.all.sam --no-unal
			
			# bowtie2 -x /mnt/g/MU_WW/SARS2/GP -f $file -S $Sampid.sam --no-unal &>> BT2info.txt
			minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta $Sampid.collapsed.fa -o $Sampid.wg.sam --sam-hit-only &>> MMinfo.txt
			echo '  ' &>> MMinfo.txt
			echo '||||||||||||||||||||||||||||||||||||||||'
			
		else
			Sampid=$(echo $file | rev | cut -d "_" -f 3- | rev)
			fastqs[0]=$file
			# echo 1
			# echo $Sampid
		fi
		
		
		# ##### SRA WGS
		# Sampid=$(echo $file| cut -d "." -f 1)
		# echo $Sampid
		# # /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.derepmin1.fa --sizeout --minuniquesize 1 &>> derepinfo.txt
		# minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta $file -o $Sampid.wgs.sam &>> MMinfo.txt
		
		echo 
		
	
	fi
done

python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 0 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --mp 1 --chim_rm 0 --deconv 0

echo 'SAM processing done'

# cd Merged
# gzip *.fastq
