#! /bin/bash


calid1=$(echo $PWD | rev | cut -d "/" -f 1 | rev)
calid2=$(echo $PWD | rev | cut -d "/" -f 2 | rev)
echo $calid1
echo $calid2
calid=""
/mnt/d/MU_WW/rakudo/bin/raku /mnt/d/MU_WW/SARS2/Program2.rk --colID="${calid2}"_"${calid1}" --foldab=.6