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
			samp=$(echo $file | cut -d "_" -f 1 )
			if [[ $xfile == *.bam ]]
			then
				echo $xfile
				echo $samp
				samtools view $xfile > $samp.sam
			fi

		done

		cd ..
	fi


done