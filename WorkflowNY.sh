#! /bin/bash


echo '===================================================================='

calid=$(echo $PWD | rev | cut -d "/" -f 1 | rev)
fastqs=()
if [ ! -d Merged ]
	then
		mkdir Merged
fi

gzip -d *.gz
echo $calid
Sampid=""

for file in *
do
	if [[ $file == *.fastq ]]
		then
		echo 0
		echo $Sampid
		if [[ $Sampid == $(echo $file| cut -d "_" -f 1 ) ]]
			then
			# echo 2
			# Sampid=$(echo $file| cut -d "." -f 1 )
			fastqs[1]=$file
			# echo ${fastqs[*]}
			echo $Sampid
			echo $Sampid &>> Mergeinfo.txt
			/mnt/g/MU_WW/vsearch/bin/vsearch --fastq_mergepairs ${fastqs[0]} --reverse ${fastqs[1]} --fastqout $Sampid.merge.fq &>> Mergeinfo.txt #  --fastqout_notmerged_fwd $Sampid.nmfwd.fq --fastqout_notmerged_rev $Sampid.nmrev.fq 
			echo '  ' &>> Mergeinfo.txt
			mv ${fastqs[0]} ./Merged/${fastqs[0]}
			mv ${fastqs[1]} ./Merged/${fastqs[1]}
			# Sampid=$(echo $file | cut -d "." -f 1-4 )
			echo $Sampid
			echo $Sampid &>> derepinfo.txt
			# /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.all.derep.fa --sizeout --minuniquesize 1
			/mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.derep.fa --sizeout --minuniquesize 100 &>> derepinfo.txt
			echo '   ' &>> derepinfo.txt
			# Sampid=$(echo $file| cut -d "_" -f 1-3 )
			echo $Sampid &>> MMinfo.txt
			# bowtie2 -x /mnt/g/MU_WW/SARS2/GP -f $Sampid.all.derep.fa -S $Sampid.all.sam --no-unal
			
			# bowtie2 -x /mnt/g/MU_WW/SARS2/GP -f $file -S $Sampid.sam --no-unal &>> BT2info.txt
			minimap2 -a /mnt/g/MU_WW/SARS2/GP.fasta $Sampid.derep.fa -o $Sampid.sam &>> MMinfo.txt
			echo '  ' &>> MMinfo.txt
			echo '||||||||||||||||||||||||||||||||||||||||'
			
		else
			# Sampid=$(echo $file| rev | cut -d "_" -f 5- | rev)
			Sampid=$(echo $file| cut -d "_" -f 1 )
			fastqs[0]=$file
			# echo 1
			# echo $Sampid
		fi
		
		echo 
		
	
	fi
done

# /mnt/g/MU_WW/rakudo/bin/raku /mnt/g/MU_WW/SARS2/rename.rk

python /mnt/g/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_iSEQ --alpha 1.6 --foldab .6


echo 'SAM processing done'

cd Merged
gzip *.fastq
