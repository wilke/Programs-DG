#! /bin/bash


echo '===================================================================='


for file in *
do
	if [[ $file == *merge.fq ]]
		then
		echo 0

		Sampid=$(echo $file | cut -d "." -f 1 )
		echo $Sampid
		# /mnt/g/MU_WW/vsearch/bin/vsearch --fastq_mergepairs $file --reverse ${Sampid}_R2_001.trimmed.fastq --fastqout_notmerged_fwd $Sampid.nmfwd.fq --fastqout_notmerged_rev $Sampid.nmrev.fq --fastqout $Sampid.merge.fq &>> Mergeinfo.txt
		# cat $Sampid.merge.fq $Sampid.nmfwd.fq $Sampid.nmrev.fq > $Sampid.all.fq
		# # echo $Sampid
		# # echo $Sampid &>> derepinfo.txt
		/mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.derep10.fa --sizeout --minuniquesize 10 --minseqlength 125 &>> derepinfo.txt
		# # /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.derep.fa --sizeout --minuniquesize 100 &>> derepinfo.txt
		# echo '   ' &>> derepinfo.txt
		
		# # echo $Sampid &>> MMinfo.txt
		# minimap2 -a /mnt/d/MU_WW/SARS2/GP.fasta $Sampid.derep10.fa --secondary=no -o $Sampid.sam # &>> MMinfo.txt
		minimap2 -a /mnt/g/MU_WW/refseqs/Mito/Animal_mito_plus.fasta $Sampid.derep10.fa -B 12 -A 1 -s 100 -C 2 --cs --secondary=no -o $Sampid.M.sam
		# # # echo '  ' &>> MMinfo.txt
		bowtie2 -x /mnt/g/MU_WW/refseqs/Mito/MitoX -f $Sampid.derep10.fa -S $Sampid.S.sam --no-head --mp 5,5 --score-min L,0,-0.1
		echo '||||||||||||||||||||||||||||||||||||||||'

		echo 
		
	
	fi
done
python /mnt/g/MU_WW/Programs/DecapSams.py
python /mnt/g/MU_WW/Programs/rRNA_collect.py
# python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID PACBIO_2021-08-04 --alpha 1.6 --foldab .6

