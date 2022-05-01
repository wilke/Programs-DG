#! /bin/bash

for file in *
do
	if [[ $file == *.fasta ]]
		then
		Sampid=$(echo $file | cut -d "." -f 1 )
		echo $Sampid
		cutadapt -g file:/mnt/g/MU_WW/SARS2/Wisconsin/QIAseqDIRECTSARSCoV2_for_plus.fasta -e .2 --trim-n --report minimal -o $Sampid.cut1.fa $file
		cutadapt -a file:/mnt/g/MU_WW/SARS2/Wisconsin/QIAseqDIRECTSARSCoV2_rev_plus.fasta -e .2 --report minimal -o $Sampid.cut2.fa $Sampid.cut1.fa
	fi
done
