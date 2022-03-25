#! /bin/bash


for file in *
do
	if [[ $file == *.fastq ]]
		then
		echo $file
		diff /mnt/g/MU_WW/SARS2/MiSeq/2021-12-10.2/Merged/$file /mnt/g/MU_WW/SARS2/MiSeq/2021-12-10.3/Merged/$file
	
	
	fi
done