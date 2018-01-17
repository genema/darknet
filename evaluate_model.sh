#!/bin/bash
rm results/*.txt
echo " >> Evaluating the model\n"
# ----------------------------------------------------
net_cfg="mgh19_18_6_416_route.cfg"
net_weight="mgh19_18_6_416_route.backup"
thresh=.21
test_pic_num=28
# ----------------------------------------------------
s1="./darknet detect cfg/"
s2=" backup/"
s3=" test_set/JPEGImages/"
s4=".jpg -thresh="
i=0
while (($i < $test_pic_num))
do
	temp="$i"
	th="$thresh"
	cmd=$s1$net_cfg$s2$net_weight$s3$temp$s4$th
	if [ $i -eq 0 ]
	then
		$cmd > log/eval_log.txt
	else
		$cmd >> log/eval_log.txt
	fi
	let "i+=1"
done

echo " >> $m"
rm test_set/results/*.txt
cp results/*.txt test_set/results/
cd ./test_set
python eval_model.py

echo " >> Evaluation done"


