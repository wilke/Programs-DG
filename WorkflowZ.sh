#! /bin/bash


echo '===================================================================='
# if [ ! -d Merged ]
	# then
		# mkdir Merged
# fi
echo $calid
Sampid=""
gzip -d *.gz
####   CURRENTLY FOR WGS from paired fastq
for file in *
do
	if [[ $file == *.fastq ]]
		then
		## MiSeq/paired WGS
		Sampid=$(echo $file | cut -d "_" -f 1 )
		echo $file
		if [[ $file == ${Sampid}_1.fastq && -f ${Sampid}_2.fastq ]]
			then
			echo ${Sampid}_2.fastq

			echo 0
			echo $Sampid
			echo $Sampid &>> Mergeinfo.txt
			bash /mnt/g/MU_WW/BBTools/BBMap/bbmerge.sh qtrim=t in1=$file in2=${Sampid}_2.fastq  out=$Sampid.merge.fq outu1=$Sampid.un1.fq outu2=$Sampid.un2.fq &>> Mergeinfo.txt
			echo '  ' &>> Mergeinfo.txt
			# mv $file ./Merged/$file
			# mv ${Sampid}_R2_001.fastq.gz ./Merged/${Sampid}_2.fastq.gz
			cat $Sampid.merge.fq $Sampid.un1.fq $Sampid.un2.fq > $Sampid.all.fq
			echo $Sampid &>> Colstats.txt
			fastx_collapser -i $Sampid.all.fq -o $Sampid.collapsed.fa &>> Colstats.txt
			echo $Sampid &>> MMinfo.txt
			minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta $Sampid.collapsed.fa -o $Sampid.wg.sam --sam-hit-only &>> MMinfo.txt
		# elif [[ $file == ${Sampid} ]]
			# then
			# echo $file
			# echo 'singles'
			# echo $Sampid
			# echo $Sampid &>> Colstats.txt
			# fastx_collapser -i $file -o $Sampid.collapsed.fa &>> Colstats.txt
			# echo $Sampid &>> MMinfo.txt
			# minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta $Sampid.collapsed.fa -o $Sampid.wg.sam --sam-hit-only &>> MMinfo.txt
		fi

		echo '||||||||||||||||||||||||||||||||||||||||'
	fi
done

python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 1 --max_covar 2 --AAcentered 1 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --mp 3 --chim_rm 0 --deconv 0

echo 'SAM processing done'
