#! /bin/bash

samp=''
for file in *
do
	if [ -d $file ]
	then
		echo $file
		cd $file
		for xfile in *
		do
			#samp=$(echo $file| rev | cut -d "_" -f 3- | rev)
			if [[ $xfile == *.bam ]]
			then
				echo $xfile
				# echo $samp
				samtools fasta $xfile > $file.fasta
			fi

		done

		cd ..
	fi


done