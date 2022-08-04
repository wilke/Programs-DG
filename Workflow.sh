#! /bin/bash


echo '===================================================================='

calid=$(echo $PWD | rev | cut -d "/" -f 1 | rev)
fastqs=()
if [ ! -d Merged ]
	then
		mkdir Merged
fi

# gzip -d *.gz
echo $calid
Sampid=""

for file in *
do
	if [[ $file == *_R1_001.fastq.gz ]]
		then
		echo 0
		Sampid=$(echo $file | rev | cut -d "_" -f 3- | rev )
		echo $Sampid
		echo $file
		bash /mnt/g/MU_WW/BBTools/BBMap/bbmerge.sh in1=$file in2=${Sampid}_R2_001.fastq.gz  out=$Sampid.merge.fq &>> $Sampid.mergestats.txt # outu1=$Sampid.un1.fq outu2=$Sampid.un2.fq
		mv $file ./Merged/$file
		mv ${Sampid}_R2_001.fastq.gz ./Merged/${Sampid}_R2_001.fastq.gz
		# Sampid=$(echo $file | cut -d "." -f 1-4 )
		echo $Sampid
		# /mnt/g/MU_WW/vsearch/bin/vsearch --derep_fulllength $Sampid.merge.fq --output $Sampid.derep.fa --sizeout --minuniquesize 100 &>> $Sampid.derepinfo.txt
		python /mnt/g/MU_WW/Programs/derep.py $Sampid.merge.fq $Sampid.derep.fa 100 &>>  ${Sampid}_derepinfo.txt
		if [[ $Sampid == *RBD* || $Sampid == *Mix* ]]
			then
			cutadapt -g ^GTGATGAAGTCAGACAAATCGC -e .3 -o $Sampid.derep.cut1.fa $Sampid.derep.fa &>> $Sampid.CutInfo.txt
			cutadapt -a CAGACACTTGAGATTCTTGACAT'$' -e .3 -o $Sampid.derep.cut.fa $Sampid.derep.cut1.fa &>> $Sampid.CutInfo.txt
			minimap2 -a /mnt/g/MU_WW/SARS2/GP.fasta $Sampid.derep.cut.fa -o $Sampid.sam &>> $Sampid.MMinfo.txt
		else
			minimap2 -a /mnt/g/MU_WW/SARS2/GP.fasta $Sampid.derep.fa -o $Sampid.sam &>> $Sampid.MMinfo.txt
		fi

		echo '||||||||||||||||||||||||||||||||||||||||'

	fi
done

rm *.fasta
rm *.fa
rm *.fq
mkdir RBD
mkdir preRBD
mkdir NTD
mkdir S1S2
mkdir NY
mkdir rRNA
mkdir Mix
mkdir NulOmi
mkdir 828

# # mv 26W_* ./NY/
# # mv 0TI_* ./NY/
# # mv 0WI_* ./NY/
# # mv 0RK_* ./NY/
# # mv 0RH_* ./NY/
# # mv 0PR_* ./NY/
# # mv 0OH_* ./NY/
# # mv 0OB_* ./NY/
# # mv 0NR_* ./NY/
# # mv 0NC_* ./NY/
# # mv 0JA_* ./NY/
# # mv 0HP_* ./NY/
# # mv 0CI_* ./NY/
# # mv 0BB_* ./NY/

mv *12s* ./rRNA/
mv *16s* ./rRNA/
mv *12S* ./rRNA/
mv *16S* ./rRNA/

mv 26W* ./NY/
mv TI* ./NY/
mv WI_* ./NY/
mv RK* ./NY/
mv RH* ./NY/
mv PR* ./NY/
mv OH* ./NY/
mv Oh* ./NY/
mv OB* ./NY/
mv NR* ./NY/
mv NC* ./NY/
mv JA* ./NY/
mv HP* ./NY/
mv CI* ./NY/
mv BB_* ./NY/
# mv B* ./NY/
# mv H* ./NY/

# mv *O-RBD* ./NulOmi/
mv *alt* ./NulOmi/
mv *Alt* ./NulOmi/
mv *ALT* ./NulOmi/


mv *RBD*NTD* ./Mix/
mv *NTD*S1S2* ./Mix/
mv NY*.* ./NY/
mv *preRBD*.* ./preRBD/
mv *PreRBD*.* ./preRBD/
mv *RBD*.* ./RBD/
mv *NTD*.* ./NTD/
mv *S1S2*.* ./S1S2/
mv *S1S1*.* ./S1S2/
mv *828_*.* ./828/

cd NY
	mkdir rRNA
	mkdir Mix
	mkdir S1S2
	mkdir NulOmi
	mkdir NTD
	mkdir preRBD
	mkdir RBD
	mkdir 828
	mv *alt* ./NulOmi/
	mv *Alt* ./NulOmi/
	mv *ALT* ./NulOmi/
	mv *RBD*NTD* ./Mix/
	mv *NTD*S1S2* ./Mix/
	mv *NTD*.* ./NTD/
	mv *S1S2*.* ./S1S2/
	mv *S1S1*.* ./S1S2/
	mv *preRBD*.* ./preRBD/
	mv *PreRBD*.* ./preRBD/
	mv *RBD*.* ./RBD/
	mv *828_*.* ./828/

	mv *12s* ./rRNA/
	mv *16s* ./rRNA/
	mv *12S* ./rRNA/
	mv *16S* ./rRNA/

	cd Mix
		python /mnt/g/MU_WW/Programs/MixedSAMSplit.py
		mkdir RBD
		mkdir NTD
		mkdir S1S2
		mv *RBD.sam ./RBD/
		mv *NTD.sam ./NTD/
		mv *S1S2.sam ./S1S2/
		cd RBD
			python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NYMixRBD --alpha 1.6 --foldab .6 --mp 4
		cd ..
		cd NTD
			python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NYMixNTD --alpha 1.6 --foldab .6 --mp 4
		cd ..
		cd S1S2
			python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NYMixS1S2 --alpha 1.6 --foldab .6 --mp 4
		cd ..
	cd ..
	cd NTD
		python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NY_NTD --alpha 1.6 --foldab .6 --mp 4
	cd ..
	cd S1S2
		python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NY_S1S2 --alpha 1.6 --foldab .6 --mp 4
	cd ..
	cd NulOmi
		python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NY_RBD_NullOmi --alpha 1.6 --foldab .6 --mp 4
	cd ..
	cd RBD
		python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NY_RBD --alpha 1.6 --foldab .6 --mp 4
	cd ..
	cd preRBD
		python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NY_preRBD --alpha 1.6 --foldab .6 --mp 4
	cd ..
	cd 828
		python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NY_R828 --alpha 1.6 --foldab .6 --mp 4
	cd ..

cd ..

cd Mix
	python /mnt/g/MU_WW/Programs/MixedSAMSplit.py
	mkdir RBD
	mkdir NTD
	mkdir S1S2
	mv *RBD.sam ./RBD/
	mv *NTD.sam ./NTD/
	mv *S1S2.sam ./S1S2/
	cd RBD
		python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_MixRBD --alpha 1.6 --foldab .6 --mp 4
	cd ..
	cd NTD
		python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_MixNTD --alpha 1.6 --foldab .6 --mp 4
	cd ..
	cd S1S2
		python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_MixS1S2 --alpha 1.6 --foldab .6 --mp 4
	cd ..
cd ..
cd RBD
python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_RBD --alpha 1.6 --foldab .6 --mp 4 --collect 0
cd ..
cd NTD
python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_NTD --alpha 1.6 --foldab .6 --mp 4
cd ..
cd S1S2
python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_S1S2 --alpha 1.6 --foldab .6 --mp 4
cd ..
cd NulOmi
python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_RBD_NulOmi --alpha 1.6 --foldab .6 --mp 4 --collect 0
cd ..
cd preRBD
python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_preRBD --alpha 1.6 --foldab .6 --mp 4 --collect 0
cd ..
cd 828
python /mnt/g/MU_WW/SAM_Refiner/SAM_Refiner.py -r /mnt/g/MU_WW/SARS2/GP.fasta --colID=${calid}_R828 --alpha 1.6 --foldab .6 --mp 4 --collect 0
cd ..
echo 'SAM processing done'

# cd Merged
# gzip *.fastq
