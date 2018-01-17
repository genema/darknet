#!/bin/bash
rm results/*.txt
echo " >> Evaluating the model"
# ----------------------------------------------------
net_cfg="mgh19_18_6_416_route.cfg"
net_weight="mgh19_18_6_416_route.backup"
test_pic_num=28
# ----------------------------------------------------
s1="./darknet detect cfg/"
s2=" backup/"
s3=" test_set/JPEGImages/"
s4=".jpg -thresh "
cmd2="python eval_model.py"
rm test_set/results/*.txt
rm results/*.txt
for((th=3;th<100;th+=5))
do
if [ $th -eq 100 ]
then
	thresh="1"
else
	thresh="0.$th"
fi
for((i=0;i<test_pic_num;i++))
do
temp="$i"
cmd=$s1$net_cfg$s2$net_weight$s3$temp$s4$thresh
$cmd
done
rm test_set/results/*.txt
mv results/*.txt test_set/results/
cd test_set
if [ $th -eq 0 ]
then
	$cmd2 > mAP_recall.txt
else
	$cmd2 >> mAP_recall.txt
fi
cd ..
done
python plot_performance.py
echo " >> Evaluation done"


