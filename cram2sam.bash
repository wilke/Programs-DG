#! /bin/bash

for file in *
do
	if [[ $file == *cram ]]
	then
		Sampid=$(echo $file | rev | cut -d "." -f 2- | rev)
		echo $file
		echo $Sampid
		samtools view -o $Sampid.sam $file
	fi
done
