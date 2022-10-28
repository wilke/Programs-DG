#! /bin/bash


fastqs=()
if [ ! -d Merged ]
	then
		mkdir Merged
fi

echo $folder
Sampid=""

for file in *
do
	if [[ $file == *Entero*_R1_001.fastq.gz ]]
		then
		echo 0
		Sampid=$(echo $file | rev | cut -d "_" -f 3- | rev )
		echo $Sampid
		bash /mnt/c/BBTools/BBMap/bbmerge.sh in1=$file in2=${Sampid}_R2_001.fastq.gz  out=$Sampid.merge.fq &>> $Sampid.mergestats.txt
		mv $file ./Merged/$file
		mv ${Sampid}_R2_001.fastq.gz ./Merged/${Sampid}_R2_001.fastq.gz
		echo $Sampid
		python ../derep.py $Sampid.merge.fq $Sampid.derep.fa 100 &>>  ${Sampid}_derepinfo.txt
		echo $file
		echo $Sampid
		/mnt/c/bowtie2..bowtie2 -x /mnt/c/Enterovirus/Entero -f ${Sampid}.derep.fa -S $Sampid.BT.sam --no-head &>> $Sampid.BTinfo.txt
	fi
done

python /mnt/g/MU_WW/Programs/EnteroAggreg.py