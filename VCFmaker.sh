#! /bin/bash

gzip -d *fq.gz
for file in *
do
	if [[ $file == *.merge.fq ]]
		then
		samp=$(echo $file| cut -d "." -f 1 )
		echo $samp
		minimap2 -a /mnt/g/MU_WW/SARS2/GP.fasta $file -o $samp.unrep.sam &>> MMinfo.txt
		samtools view -S -b $samp.unrep.sam > $samp.bam
		samtools sort $samp.bam -o $samp.sorted.bam
		samtools index $samp.sorted.bam
	fi
done

# for file in *
# do
	# if [[ $file == *.sorted.bam ]]
		# then
		# samp=$(echo $file| cut -d "." -f 1 )
		# echo $samp
		# freebayes -f /mnt/g/MU_WW/SARS2/GP.fasta -p 1 --min-coverage 10 -C 10 -G 10 -F .01 $samp.sorted.bam -v $samp.vcf
	# fi
# done
