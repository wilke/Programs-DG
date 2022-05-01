#! /bin/bash


echo '===================================================================='


# for dir in */
# do
	# # # if [[ $file == *.merge.fq ]]
		# # # then
		# # # Sampid=$(echo $file | cut -d "." -f 1 )
		# # # echo $Sampid
		# # # # samtools fasta $file > $Sampid.fasta
		# # # # /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $file --output $Sampid.derep1.fa --sizeout --minuniquesize 1 --minseqlength 100
		# # # fastx_collapser -i $file -o $Sampid.derep1.fa
		# # # # minimap2 -a aichi_virus_1.fasta $Sampid.derep1.fa -o $Sampid.derep1.sam
		# # # # python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --collect 0 --seq 1 --indel 0 --covar 0 --nt_call 0 -S $Sampid.nomin.sam --min_count 0 --min_samp_abund 0 --min_col_abund 0 # --ntabund 0 --AAreport 0 -S $Sampid.wgs.sam
	# # # fi
	
	# wwtp=$(echo $dir | rev | cut -c 2- | rev)
	# echo $wwtp
	# cd $dir
	# gzip -d *.gz
	# for file in *
	# do
		# # echo $file
		# # # # if [ -d $file ]
			# # # # then
			# # # # echo $file
			# # # # cd $file
			# # # # python /mnt/g/MU_WW/Programs/SRAsurvey.py
			# # # # # for subdirfile in *
			# # # # # do
				# # # # # if [[ $subdirfile == *.derepmin1.fa* ]]
					# # # # # then
					# # # # # echo $subdirfile
					# # # # # # Sampid=$(echo $subdirfile | cut -d "." -f 1 )
					# # # # # # minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta $subdirfile -o $Sampid.wgs.sam
					# # # # # # python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.fasta --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 1 --min_count 0 --min_samp_abund 0 --ntabund 0 --AAreport 0 -S $Sampid.wgs.sam # --colID 20210829_NTD --alpha 1.6 --foldab .6

				# # # # # fi
			# # # # # done
			# # # # # python /mnt/g/MU_WW/Programs/Variant_extractor_NSP12_P323P.py
			# # # # cd ..
			
		# if [[ $file == *R1_001.fastq ]]
			# then
			# Sampid=$(echo $file| rev | cut -d "_" -f 3- | rev)
			# echo $Sampid
			# /mnt/g/MU_WW/vsearch/bin/vsearch --fastq_mergepairs $file --reverse ${Sampid}_R2_001.fastq --fastqout_notmerged_fwd $Sampid.nmfwd.fq --fastqout_notmerged_rev $Sampid.nmrev.fq --fastqout $Sampid.merge.fq &>> Mergeinfo.txt
			# cat $Sampid.merge.fq $Sampid.nmfwd.fq $Sampid.nmrev.fq > $Sampid.all.fq
			# # # # # # echo $Sampid
			# # # # # # echo $Sampid &>> derepinfo.txt
			# /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.all.fq --output $Sampid.derep1.fa --sizeout --minuniquesize 1 &>> derepinfo.txt # --minseqlength 125
			# # # # # # /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.derep.fa --sizeout --minuniquesize 100 &>> derepinfo.txt
			# # # # # echo '   ' &>> derepinfo.txt
			
			# # # # # # echo $Sampid &>> MMinfo.txt
			# minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta $Sampid.derep1.fa -o $Sampid.sam # &>> MMinfo.txt
			# # # # # minimap2 -a /mnt/g/MU_WW/refseqs/Mito/Animal_mito_plus.fasta $Sampid.derep10.fa -B 12 -A 1 -s 100 -C 2 --cs --secondary=no -o $Sampid.M.sam
			# # # # # # # echo '  ' &>> MMinfo.txt
			# # # # # bowtie2 -x /mnt/g/MU_WW/refseqs/Mito/MitoX -f $Sampid.derep10.fa -S $Sampid.S.sam --no-head --mp 5,5 --score-min L,0,-0.1
			# # # # echo '||||||||||||||||||||||||||||||||||||||||'
		# fi
		# # # # fi
		# # # if [[ $file == *.derep.fa* ]]
			# # # then
				# # # echo $file
				# # # Sampid=$(echo $file | rev | cut -d "." -f 3- | rev)
				# # # echo $Sampid
				# # # # minimap2 -a /mnt/g/MU_WW/SARS2/GP.fasta $file -o $Sampid.S.sam
				# # # # python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.fasta --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 1 --min_count 0 --min_samp_abund 0 --ntabund 0 --AAreport 0 -S $Sampid.wgs.sam
		# # # fi
	# done
	# # bash /mnt/g/MU_WW/Programs/Workflow.sh
	# python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 0 --nt_call 1 --min_count 1 --min_samp_abund 0 --ntabund 0 --AAreport 1 --ntcover 1 --chim_rm 0 --deconv 0
	# # python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --chim_rm 0 --deconv 1 --colID $wwtp # -r /mnt/g/MU_WW/SARS2/GP.fasta --collect 1 --alpha 1.6 --foldab .6 --mp 4 --indel 0 --nt_call 0 
	# # rm *covars.tsv
	# # # # python /mnt/g/MU_WW/Programs/Variant_extractor_NSP12_P323P.py
	# # # python /mnt/g/MU_WW/Programs/SRAsurvey.py
	# # # gzip *.fa
	# cd ..
	
# done

for file in *
do
	if [[ $file == *.merge.fq ]]
		then
		Sampid=$(echo $file | cut -d "." -f -1 )
		echo $Sampid
		#/mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $file --output $Sampid.derep1.fa --sizeout --minuniquesize 1 &>> derepinfo.txt 
		# minimap2 -a /mnt/g/MU_WW/SARS2/SARS2.fasta $file -o $Sampid.SARS2.WG.sam --sam-hit-only --secondary no
		minimap2 -a /mnt/g/MU_WW/SARS2/GP.fasta $file -o $Sampid.SARS2.S.test.sam --sam-hit-only --secondary no
		# python /mnt/g/MU_WW/Programs/SAM2Fasta.py $Sampid.RBD.sam
		# /mnt/g/MU_WW/vsearch/bin/vsearch --rereplicate $Sampid.RBD.fasta --output $Sampid.RBD.rerep.fa
		# python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 1 --indel 0 --covar 0 --nt_call 1 --read 0 -S $Sampid.SARS2.WG.sam --min_count 1 --min_samp_abund 0 --min_col_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0
		# python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --wgs 1 --collect 0 --seq 1 --indel 0 --covar 0 --nt_call 1 --read 0 -S $Sampid.SARS2.S.sam --min_count 1 --min_samp_abund 0 --min_col_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0
		# ragtag.py scaffold /mnt/g/MU_WW/SARS2/RBD.fa $Sampid.RBD.rerep.fa -o $Sampid -f 50
		# megahit -r $file -o $Sampid.MH
	fi
	
done

# python Contigpull.py

# python /mnt/g/MU_WW/Programs/Consensus.py
# python /mnt/g/MU_WW/Programs/DecapSams.py
# python /mnt/g/MU_WW/Programs/rRNA_collect.py
# python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID RBD --min_count 1 --min_samp_abund 0.0001 --wgs 0 --collect 1 --ntabund .00001 --covar 0 --AAreport 1 --mp 1  --alpha 1.6 --foldab .6

# python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/SARS2.gb --wgs 1 --collect 0 --seq 0 --indel 0 --covar 0 --nt_call 0 --read 1 --min_count 1 --min_samp_abund 0 --min_col_abund 0 --ntabund 0 --ntcover 1 --AAreport 1 --chim_rm 0 --deconv 0 --mp 3