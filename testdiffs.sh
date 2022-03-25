#!/bin/bash

for file in *
do
	if [[ $file == *s.tsv ]]
		then
		echo $file
		diff <(sort $file) <(sort ./backup/$file) -s
	fi
done