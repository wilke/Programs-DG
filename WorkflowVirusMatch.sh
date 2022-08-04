#! /bin/bash


echo '===================================================================='


if [ ! -d Merged ]
	then
		mkdir Merged
fi


Sampid=""

for file in *
do

	if [[ $file == *R1_001_trimmed.fastq.gz ]]
		then
		echo 0
		Sampid=$(echo $file | rev | cut -d "_" -f 4- | rev )
		echo $Sampid
		echo $Sampid &>>  $Sampid.mergestats.txt
		bash /mnt/g/MU_WW/BBTools/BBMap/bbmerge.sh qtrim=t in1=$file in2=${Sampid}_R2_001_trimmed.fastq.gz  out=$Sampid.merge.fq outu1=$Sampid.un1.fq outu2=$Sampid.un2.fq  &>> $Sampid.mergestats.txt
		echo '  ' &>> $Sampid.mergestats.txt
		mv $file ./Merged/$file
		mv ${Sampid}_R2_001_trimmed.fastq.gz ./Merged/${Sampid}_R2_001_trimmed.fastq.gz
		cat $Sampid.merge.fq $Sampid.un1.fq $Sampid.un2.fq > $Sampid.all.fq
		echo $Sampid
		fastp -g -x -y -Y 40 -l 40 --dont_eval_duplication -i $Sampid.all.fq -o $Sampid.all.pfiltered.fq &>> $Sampid.fastpinfo.txt
		# echo $Sampid &>>  ${Sampid}_derepinfo.txt
		python /mnt/g/MU_WW/Programs/derep.py $Sampid.all.pfiltered.fq $Sampid.derep1.fa 1 &>>  ${Sampid}_derepinfo.txt
		# bowtie2 -x /mnt/g/MU_WW/refseqs/Index/allviral -f $Sampid.derep1.fa -S $Sampid.All_vir.BT.sam --no-head --no-unal &>>  ${Sampid}_BTinfo.txt
		# minimap2 -a /mnt/g/MU_WW/refseqs/viral.all.genomic.fa $Sampid.derep1.fa -o $Sampid.all_vir.MM.sam -O 6,30 -E 3,1 --sam-hit-only &>>  ${Sampid}_MMinfo.txt
		bowtie2 -x /mnt/g/MU_WW/refseqs/Index/Huviral -f $Sampid.derep1.fa -S $Sampid.Hu_vir.BT.sam --no-head --no-unal &>>  ${Sampid}_BTinfo.txt
		minimap2 -a /mnt/g/MU_WW/refseqs/viral.Hu.genomic.fa $Sampid.derep1.fa -o $Sampid.Hu_vir.MM.sam -O 6,30 -E 3,1 --sam-hit-only &>>  ${Sampid}_MMinfo.txt
		# bowtie2 -x /mnt/g/MU_WW/refseqs/Index/Vertviral -f $Sampid.derep1.fa -S $Sampid.Vert_vir.BT.sam --no-head --no-unal &>>  ${Sampid}_BTinfo.txt
		# minimap2 -a /mnt/g/MU_WW/refseqs/viral.Vert.genomic.fa $Sampid.derep1.fa -o $Sampid.Vert_vir.MM.sam -O 6,30 -E 3,1 --sam-hit-only &>>  ${Sampid}_MMinfo.txt
		# kraken2 --db /mnt/g/MU_WW/K2_viral $Sampid.all.fq --report $Sampid.allv.k2report > $Sampid.allv.k2
		# python /mnt/g/MU_WW/kreport2krona.py -r $Sampid.allv.k2report -o $Sampid.allv.krona.txt
		# ktImportText $Sampid.allv.krona.txt -o $Sampid.allv.krona.html

		echo '||||||||||||||||||||||||||||||||||||||||'


		echo
	fi



	# if [[ $file == *.derep1.fa ]]
		# then
		# echo 0
		# Sampid=$(echo $file | cut -d "." -f 1  )
		# echo $Sampid

		# echo $Sampid &>> MMinfo.txt
		# # minimap2 -a /mnt/g/MU_WW/refseqs/Human_virus_refseq.fasta $file -o $Sampid.Hu_vir.sam --sam-hit-only &>> MMinfo.txt
		# # minimap2 -a /mnt/g/MU_WW/refseqs/viral.all.genomic.fa $file -o $Sampid.all_vir.sam --sam-hit-only &>> MMinfo.txt
		# bowtie2 -x /mnt/g/MU_WW/refseqs/Index/allviral -f $file -S $Sampid.All_vir.S.sam --no-head --no-unal &>> BTinfo.txt
		# bowtie2 -x /mnt/g/MU_WW/refseqs/Index/Huviral -f $file -S $Sampid.Hu_vir.S.sam --no-head --no-unal &>> BTinfo.txt
		# # echo '  ' &>> MMinfo.txt
		# # echo '  ' &>> BTinfo.txt
		# kraken2 --db /mnt/g/MU_WW/K2_viral $file --report $Sampid.allv.k2report > $Sampid.allv.k2
		# python /mnt/g/MU_WW/kreport2krona.py -r $Sampid.allv.k2report -o $Sampid.allv.krona.txt
		# ktImportText $Sampid.allv.krona.txt -o $Sampid.allv.krona.html

		# echo '  ' &>> MMinfo.txt
		# echo '||||||||||||||||||||||||||||||||||||||||'



		# echo

	# fi


	# if [[ $file == *.all.fq ]]
		# then
		# Sampid=$(echo $file | cut -d "." -f 1  )
		# echo $Sampid &>> derepinfo.txt
		# /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $file --output $Sampid.derep1.fa --sizeout --minuniquesize 1 &>> derepinfo.txt
		# # echo '   ' &>> derepinfo.txt
		# # echo $Sampid &>> MMinfo.txt
		# # minimap2 -a /mnt/g/MU_WW/refseqs/Human_virus_refseq.fasta $Sampid.derep1.fa -o $Sampid.Hu_vir.M.sam --sam-hit-only &>> MMinfo.txt
		# # minimap2 -a /mnt/g/MU_WW/refseqs/viral.all.genomic.fa $Sampid.derep1.fa -o $Sampid.all_vir.M.sam --sam-hit-only &>> MMinfo.txt
		# # bowtie2 -x /mnt/g/MU_WW/refseqs/Index/allviral -f $Sampid.derep1.fa -S $Sampid.All_vir.S.sam --no-head --no-unal &>> BTinfo.txt
		# # bowtie2 -x /mnt/g/MU_WW/refseqs/Index/Huviral -f $Sampid.derep1.fa -S $Sampid.Hu_vir.S.sam --no-head --no-unal &>> BTinfo.txt
		# # echo '  ' &>> MMinfo.txt
		# # echo '  ' &>> BTinfo.txt
		# kraken2 --db /mnt/g/MU_WW/K2_viral $file --report $Sampid.allv.k2report > $Sampid.allv.k2
		# python /mnt/g/MU_WW/kreport2krona.py -r $Sampid.allv.k2report -o $Sampid.allv.krona.txt
		# ktImportText $Sampid.allv.krona.txt -o $Sampid.allv.krona.html

		# echo '||||||||||||||||||||||||||||||||||||||||'

	# fi


done

python /mnt/g/MU_WW/Programs/remove_polyT.py
# python /mnt/g/MU_WW/Programs/krona_nounclass.py

