#! /bin/bash

# Writen by Devon Gregory
# bash to execute pipeline to download and process
# MiSeq reads of Spike amplicons
# required: custom scripts; Pullfastqgz, derep, MixedSAMSplit
# bbmap/bbmerge
# cutadapt
# minimap2
# SAM Refiner
# Last edited on 8-11-22

# get folder name for sequencing run
echo "Please enter the name of the sequencing run (to make a folder for it)"
read -r folder
mkdir $folder
cd $folder

# get url for download
echo "Please paste the url to download the samples"
read -r url
curl -L -o download.zip $url

python3 ../Pullfastqgz.py

echo '===================================================================='

fastqs=()
if [ ! -d Merged ]
	then
		mkdir Merged
fi

echo $folder
Sampid=""

for file in *
do
	if [[ $file == *_R1_001.fastq.gz ]]
	then
		echo 0
		Sampid=$(echo $file | rev | cut -d "_" -f 3- | rev )
		echo $Sampid
		echo $file
		bash ../bbmap/bbmerge.sh in1=$file in2=${Sampid}_R2_001.fastq.gz  out=$Sampid.merge.fq &>> $Sampid.mergestats.txt
		mv $file ./Merged/$file
		mv ${Sampid}_R2_001.fastq.gz ./Merged/${Sampid}_R2_001.fastq.gz
		echo $Sampid
		python ../derep.py $Sampid.merge.fq $Sampid.derep.fa 100 &>>  ${Sampid}_derepinfo.txt
		if [[ $Sampid == *RBD* || $Sampid == *Mix* ]]
		then
			cutadapt -g ^GTGATGAAGTCAGACAAATCGC -e .3 -o $Sampid.derep.cut1.fa $Sampid.derep.fa &>> $Sampid.CutInfo.txt
			cutadapt -a CAGACACTTGAGATTCTTGACAT'$' -e .3 -o $Sampid.derep.cut.fa $Sampid.derep.cut1.fa &>> $Sampid.CutInfo.txt
			minimap2 -a ../GP.fasta $Sampid.derep.cut.fa -o $Sampid.sam &>> $Sampid.MMinfo.txt
		else
			minimap2 -a ../GP.fasta $Sampid.derep.fa -o $Sampid.sam &>> $Sampid.MMinfo.txt
		fi

		echo '||||||||||||||||||||||||||||||||||||||||'

	fi
done

mkdir RBD
mkdir preRBD
mkdir NTD
mkdir S1S2
mkdir rRNA
mkdir Mix
mkdir NulOmi
mkdir 828

mv *12s* ./rRNA/
mv *16s* ./rRNA/
mv *12S* ./rRNA/
mv *16S* ./rRNA/

mv *alt* ./NulOmi/
mv *Alt* ./NulOmi/
mv *ALT* ./NulOmi/

mv *RBD*NTD* ./Mix/
mv *NTD*S1S2* ./Mix/
mv *preRBD*.* ./preRBD/
mv *PreRBD*.* ./preRBD/
mv *RBD*.* ./RBD/
mv *NTD*.* ./NTD/
mv *S1S2*.* ./S1S2/
mv *S1S1*.* ./S1S2/
mv *828_*.* ./828/

cd Mix
	python ../MixedSAMSplit.py
	mkdir RBD
	mkdir NTD
	mkdir S1S2
	mv *RBD.sam ./RBD/
	mv *NTD.sam ./NTD/
	mv *S1S2.sam ./S1S2/
	cd RBD
		python ../../../SAM_Refiner.py -r ../../../GP.fasta --colID=${folder}_MixRBD --alpha 1.6 --foldab .6 --mp 4
	cd ..
	cd NTD
		python ../../../SAM_Refiner.py -r ../../../GP.fasta --colID=${folder}_MixNTD --alpha 1.6 --foldab .6 --mp 4
	cd ..
	cd S1S2
		python ../../../SAM_Refiner.py -r ../../../GP.fasta --colID=${folder}_MixS1S2 --alpha 1.6 --foldab .6 --mp 4
	cd ..
cd ..
cd RBD
python ../../SAM_Refiner.py -r ../../GP.fasta --colID=${folder}_RBD --alpha 1.6 --foldab .6 --mp 4
cd ..
cd NTD
python ../../SAM_Refiner.py -r ../../GP.fasta --colID=${folder}_NTD --alpha 1.6 --foldab .6 --mp 4
cd ..
cd S1S2
python ../../SAM_Refiner.py -r ../../GP.fasta --colID=${folder}_S1S2 --alpha 1.6 --foldab .6 --mp 4
cd ..
cd NulOmi
python ../../SAM_Refiner.py -r ../../GP.fasta --colID=${folder}_RBD_NulOmi --alpha 1.6 --foldab .6 --mp 4
cd ..
cd preRBD
python ../../SAM_Refiner.py -r ../../GP.fasta --colID=${folder}_preRBD --alpha 1.6 --foldab .6 --mp 4
cd ..
cd 828
python ../../SAM_Refiner.py -r ../../GP.fasta --colID=${folder}_R828 --alpha 1.6 --foldab .6 --mp 4
cd ..
cd ..
echo 'SAM processing done'

