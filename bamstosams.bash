#! /bin/bash

samp=''
for file in *
do
	# if [ -d $file ]
	# then
		# echo $file
		# cd $file
		# for xfile in *
		# do

	if [[ $file == *.bam ]]
	then
		echo $file
		samp=$(echo $file | cut -d "." -f 1 )
		echo $samp
		samtools view $file > $samp.sam
	fi

		# done

		# cd ..
	# fi


done