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
		if [[ $Sampid == $(echo $file| rev | cut -d "_" -f 4- | rev ) ]]
			then
			# echo 2
			# Sampid=$(echo $file| cut -d "." -f 1 )
			fastqs[1]=$file
			# echo ${fastqs[*]}
			echo $Sampid
			echo $Sampid &>> Mergeinfo.txt
			/mnt/e/MU_WW/vsearch/bin/vsearch --fastq_mergepairs ${fastqs[0]} --reverse ${fastqs[1]} --fastqout $Sampid.merge.fq &>> Mergeinfo.txt #  --fastqout_notmerged_fwd $Sampid.nmfwd.fq --fastqout_notmerged_rev $Sampid.nmrev.fq 
			echo '  ' &>> Mergeinfo.txt
			mv ${fastqs[0]} ./Merged/${fastqs[0]}
			mv ${fastqs[1]} ./Merged/${fastqs[1]}
			# Sampid=$(echo $file | cut -d "." -f 1-4 )
			echo $Sampid
			echo $Sampid &>> derepinfo.txt
			# /mnt/e/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.all.derep.fa --sizeout --minuniquesize 1
			/mnt/e/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.derep.fa --sizeout --minuniquesize 100 &>> derepinfo.txt
			echo '   ' &>> derepinfo.txt
			# Sampid=$(echo $file| cut -d "_" -f 1-3 )
			echo $Sampid &>> MMinfo.txt
			# bowtie2 -x /mnt/e/MU_WW/SARS2/GP -f $Sampid.all.derep.fa -S $Sampid.all.sam --no-unal
			
			# bowtie2 -x /mnt/e/MU_WW/SARS2/GP -f $file -S $Sampid.sam --no-unal &>> BT2info.txt
			minimap2 -a /mnt/e/MU_WW/SARS2/GP.fasta $Sampid.derep.fa -o $Sampid.sam &>> MMinfo.txt
			echo '  ' &>> MMinfo.txt
			echo '||||||||||||||||||||||||||||||||||||||||'
			
		else
			Sampid=$(echo $file| rev | cut -d "_" -f 4- | rev)
			fastqs[0]=$file
			# echo 1
			# echo $Sampid
		fi
		
		echo 
		
	
	fi
done

mkdir RBD
mkdir NTD
mkdir S1S2
mkdir NY
mkdir rRNA
mkdir Mix

mv 26W_* ./NY/
mv 0TI_* ./NY/
mv 0WI_* ./NY/
mv 0RK_* ./NY/
mv 0RH_* ./NY/
mv 0PR_* ./NY/
mv 0OH_* ./NY/
mv 0OB_* ./NY/
mv 0NR_* ./NY/
mv 0NC_* ./NY/
mv 0JA_* ./NY/
mv 0HP_* ./NY/
mv 0CI_* ./NY/
mv 0BB_* ./NY/

mv 26W* ./NY/
mv TI* ./NY/
mv WI* ./NY/
mv RK* ./NY/
mv RH* ./NY/
mv PR* ./NY/
mv OH* ./NY/
mv OB* ./NY/
mv NR* ./NY/
mv NC* ./NY/
mv JA* ./NY/
mv HP* ./NY/
mv CI* ./NY/
mv BB* ./NY/
mv B* ./NY/
mv H* ./NY/

mv *12s* ./rRNA/
mv *16s* ./rRNA/
mv *12S* ./rRNA/
mv *16S* ./rRNA/

mv *RBD*NTD* ./Mix/
# mv NY*.* ./NY/
mv *RBD*.* ./RBD/
mv *NTD*.* ./NTD/
mv *S1S2*.* ./S1S2/
mv *S1S1*.* ./S1S2/

cd NY
# mkdir RBD
# mkdir NTD
# mkdir S1S2
	mkdir rRNA
	mkdir Mix
	mkdir S1S2
	mv *RBD*NTD* ./Mix/
	mv *S1S2*.* ./S1S2/
	mv *S1S1*.* ./S1S2/

	mv *12s* ./rRNA/
	mv *16s* ./rRNA/
	mv *12S* ./rRNA/
	mv *16S* ./rRNA/

	cd Mix
		python /mnt/e/MU_WW/SARS2/MixedSAMSplit.py
		mkdir RBD
		mkdir NTD
		mv *RBD.sam ./RBD/
		mv *NTD.sam ./NTD/
		cd RBD
			python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_NYMixRBD --alpha 1.6 --foldab .6 --mp 1
		cd ..
		cd NTD
			python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_NYMixNTD --alpha 1.6 --foldab .6 --mp 1
		cd ..
	cd ..
	cd S1S2
		python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_NY_S1S2 --alpha 1.6 --foldab .6 --mp 1
	cd ..

	# /mnt/e/MU_WW/rakudo/bin/raku /mnt/e/MU_WW/SARS2/rename.rk
	python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_NY_RBD --alpha 1.6 --foldab .6 --mp 1

	# cd S1S2
	# python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_NY_S1S2 --alpha 1.6 --foldab .6
	# cd ..
cd ..

cd Mix
	python /mnt/e/MU_WW/SARS2/MixedSAMSplit.py
	mkdir RBD
	mkdir NTD
	mv *RBD.sam ./RBD/
	mv *NTD.sam ./NTD/
	cd RBD
		python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_MixRBD --alpha 1.6 --foldab .6 --mp 1
	cd ..
	cd NTD
		python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_MixNTD --alpha 1.6 --foldab .6 --mp 1
	cd ..
cd ..
cd RBD
# /mnt/e/MU_WW/rakudo/bin/raku /mnt/e/MU_WW/SARS2/rename.rk
python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_RBD --alpha 1.6 --foldab .6 --mp 1
cd ..
cd NTD
# /mnt/e/MU_WW/rakudo/bin/raku /mnt/e/MU_WW/SARS2/rename.rk
python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_NTD --alpha 1.6 --foldab .6 --mp 1
cd ..
cd S1S2
# /mnt/e/MU_WW/rakudo/bin/raku /mnt/e/MU_WW/SARS2/rename.rk
python /mnt/e/MU_WW/SARS2/SAM_Refiner/SAM_Refiner.py -r /mnt/e/MU_WW/SARS2/GP.fasta --colID=${calid}_S1S2 --alpha 1.6 --foldab .6 --mp 1
cd ..
echo 'SAM processing done'

cd Merged
gzip *.fastq
