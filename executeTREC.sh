#!/bin/bash

allfilesF1=$(ls -r inputF1)
allfilesF2=$(ls -r inputF2)
allfilesF3=$(ls -r inputF3)

amountF1=$(ls -r inputF1 | wc -l)
amountF2=$(ls -r inputF2 | wc -l)
amountF3=$(ls -r inputF3 | wc -l)

echo "There are ${amountF1} files in inputF1!";
echo "There are ${amountF2} files in inputF2!";
echo "There are ${amountF3} files in inputF3!";


for filenametmp in ${allfilesF1}
do
    filename="${filenametmp::-5}";
  
    result=$(./trec_eval qrels.test inputF1/${filenametmp});
    outputfilename=$"outputF1/output_${filename}.test";

    echo "${result}" > ${outputfilename}
done

for filenametmp in ${allfilesF2}
do
    filename="${filenametmp::-5}";
  
    result=$(./trec_eval qrels.test inputF2/${filenametmp});
    outputfilename=$"outputF2/output_${filename}.test";

    echo "${result}" > ${outputfilename}
done

for filenametmp in ${allfilesF3}
do
    filename="${filenametmp::-5}";
  
    result=$(./trec_eval qrels.test inputF3/${filenametmp});
    outputfilename=$"outputF3/output_${filename}.test";

    echo "${result}" > ${outputfilename}
done


#chmod u+x executeTREC.sh
#./executeTREC.sh