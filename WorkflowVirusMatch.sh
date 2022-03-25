#! /bin/bash


echo '===================================================================='


if [ ! -d Merged ]
	then
		mkdir Merged
fi

gzip -d *.gz
Sampid=""
fastqs=()

for file in *
do

	# if [[ $file == *.fastq ]]
		# then
		# echo 0
		# echo $Sampid
		# if [[ $Sampid == $(echo $file| rev | cut -d "_" -f 4- | rev ) ]]
			# then
			# echo 2
			# fastqs[1]=$file
			# echo $Sampid
			# echo $Sampid &>> Mergeinfo.txt
			# /mnt/g/MU_WW/vsearch/bin/vsearch --fastq_mergepairs ${fastqs[0]} --reverse ${fastqs[1]} --fastqout $Sampid.merge.fq --fastqout_notmerged_fwd $Sampid.nmfwd.fq --fastqout_notmerged_rev $Sampid.nmrev.fq &>> Mergeinfo.txt #  
			# echo '  ' &>> Mergeinfo.txt
			# mv ${fastqs[0]} ./Merged/${fastqs[0]}
			# mv ${fastqs[1]} ./Merged/${fastqs[1]}
			# cat $Sampid.merge.fq $Sampid.nmfwd.fq $Sampid.nmrev.fq > $Sampid.all.fq
			# echo $Sampid
			# echo $Sampid &>> derepinfo.txt
			# /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.all.fq --output $Sampid.derep1.fa --sizeout --minuniquesize 1 &>> derepinfo.txt
			# echo '   ' &>> derepinfo.txt
			# echo $Sampid &>> MMinfo.txt
			# minimap2 -a /mnt/g/MU_WW/refseqs/Human_virus_refseq.fasta $Sampid.derep1.fa -o $Sampid.Hu_vir.M.sam --sam-hit-only &>> MMinfo.txt
			# minimap2 -a /mnt/g/MU_WW/refseqs/viral.all.genomic.fa $Sampid.derep1.fa -o $Sampid.all_vir.M.sam --sam-hit-only &>> MMinfo.txt
			# bowtie2 -x /mnt/g/MU_WW/refseqs/Index/allviral -f $Sampid.derep1.fa -S $Sampid.All_vir.S.sam --no-head --no-unal &>> BTinfo.txt
			# bowtie2 -x /mnt/g/MU_WW/refseqs/Index/Huviral -f $Sampid.derep1.fa -S $Sampid.Hu_vir.S.sam --no-head --no-unal &>> BTinfo.txt
			# echo '  ' &>> MMinfo.txt
			# echo '  ' &>> BTinfo.txt
			# kraken2 --db /mnt/g/MU_WW/K2_viral $Sampid.derep1.fa --report $Sampid.allv.k2report > $Sampid.allv.k2
			# python /mnt/g/MU_WW/kreport2krona.py -r $Sampid.allv.k2report -o $Sampid.allv.krona.txt
			# ktImportText $Sampid.allv.krona.txt -o $Sampid.allv.krona.html
			
			# echo '||||||||||||||||||||||||||||||||||||||||'
			
		# else
			# Sampid=$(echo $file| rev | cut -d "_" -f 4- | rev )
			# fastqs[0]=$file
			# echo 1
			# echo $Sampid
		# fi
		
		# echo 
	# fi
	
	
	
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
	
	
	if [[ $file == *.all.fq ]]
		then
		Sampid=$(echo $file | cut -d "." -f 1  )
		echo $Sampid &>> derepinfo.txt
		# /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $file --output $Sampid.derep1.fa --sizeout --minuniquesize 1 &>> derepinfo.txt
		# echo '   ' &>> derepinfo.txt
		# echo $Sampid &>> MMinfo.txt
		# minimap2 -a /mnt/g/MU_WW/refseqs/Human_virus_refseq.fasta $Sampid.derep1.fa -o $Sampid.Hu_vir.M.sam --sam-hit-only &>> MMinfo.txt
		# minimap2 -a /mnt/g/MU_WW/refseqs/viral.all.genomic.fa $Sampid.derep1.fa -o $Sampid.all_vir.M.sam --sam-hit-only &>> MMinfo.txt
		# bowtie2 -x /mnt/g/MU_WW/refseqs/Index/allviral -f $Sampid.derep1.fa -S $Sampid.All_vir.S.sam --no-head --no-unal &>> BTinfo.txt
		# bowtie2 -x /mnt/g/MU_WW/refseqs/Index/Huviral -f $Sampid.derep1.fa -S $Sampid.Hu_vir.S.sam --no-head --no-unal &>> BTinfo.txt
		# echo '  ' &>> MMinfo.txt
		# echo '  ' &>> BTinfo.txt
		kraken2 --db /mnt/g/MU_WW/K2_viral $file --report $Sampid.allv.k2report > $Sampid.allv.k2
		python /mnt/g/MU_WW/kreport2krona.py -r $Sampid.allv.k2report -o $Sampid.allv.krona.txt
		ktImportText $Sampid.allv.krona.txt -o $Sampid.allv.krona.html
		
		echo '||||||||||||||||||||||||||||||||||||||||'
		
	fi
	
	
done

python /mnt/g/MU_WW/SARS2/DecapSams.py

