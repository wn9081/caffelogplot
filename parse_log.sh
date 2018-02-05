#!/bin/bash
# Usage parse_log.sh caffe.log
# It creates the following two text files, each containing a table:
#     caffe.log.train (columns: '#Iters Seconds TrainingLoss LearningRate loss_bbox loss_cls rpn_cls_loss rpn_loss_bbox')

function pause(){
        read -n 1 -p "$*" INP
        if [ $INP != '' ] ; then
                echo -ne '\b \n'
        fi
}


# get the dirname of the script
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

if [ "$#" -lt 1 ]
then
echo "Usage parse_log.sh /path/to/your.log"
exit
fi
LOG=`basename $1`

sed -n '/Solving.../,/done solving/p' $1 > aux.txt
sed -i '/speed: .* iter/d' aux.txt
sed -i '/Wrote snapshot to:/d' aux.txt
sed -i '/Solving.../d' aux.txt
sed -i '/done solving/d' aux.txt
sed -i '/Iteration .*/{N;/Iteration.*\n.*Optimization Done/d}' aux.txt

grep 'Iteration .*, loss ' aux.txt | sed  's/.*Iteration \([[:digit:]]*\).*/\1/g' > aux0.txt
grep ', loss = ' aux.txt | awk '{print $NF}' > aux1.txt
grep ', lr = ' aux.txt | awk '{print $NF}' > aux2.txt
grep 'Train net output #0' aux.txt | awk '{print $11}' > aux3.txt
grep 'Train net output #1' aux.txt | awk '{print $11}' > aux4.txt
grep 'Train net output #2' aux.txt | awk '{print $11}' > aux5.txt
grep 'Train net output #3' aux.txt | awk '{print $11}' > aux6.txt

# Extracting elapsed seconds
$DIR/extract_seconds.py aux.txt aux7.txt

# Generating
echo '#Iters Seconds TrainingLoss LearningRate loss_bbox loss_cls rpn_cls_loss rpn_loss_bbox'> $LOG.train
paste aux0.txt aux7.txt aux1.txt aux2.txt aux3.txt aux4.txt aux5.txt aux6.txt| column -t >> $LOG.train
rm aux.txt aux0.txt aux7.txt aux1.txt aux2.txt aux3.txt aux4.txt aux5.txt aux6.txt

