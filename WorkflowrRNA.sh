#! /bin/bash


echo '===================================================================='


for file in *
do
	if [[ $file == *merge.fq ]]
		then
		echo 0
		Sampid=$(echo $file | cut -d "." -f 1 )
		echo $Sampid
		python ../../derep.py $Sampid.merge.fq $Sampid.derep10.fa 10 &>>  ${Sampid}_derepinfo.txt
		minimap2 -a /mnt/g/MU_WW/refseqs/Mito/Animal_mito_plus.fasta $Sampid.derep10.fa -B 12 -A 1 -s 100 -C 2 --cs --secondary=no -o $Sampid.M.sam
		bowtie2 -x /mnt/g/MU_WW/refseqs/Mito/MitoX -f $Sampid.derep10.fa -S $Sampid.S.sam --no-head --mp 5,5 --score-min L,0,-0.1
		echo '||||||||||||||||||||||||||||||||||||||||'
	fi
done
python /mnt/g/MU_WW/Programs/DecapSams.py
python /mnt/g/MU_WW/Programs/rRNA_collect.py

