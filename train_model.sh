#!/bin/bash
# --------------------------------
data_cfg="voc.data"
net_cfg="mgh19_10_6_416_route.cfg"
backup_file=""
# --------------------------------

echo " >> Start trainning !"
read -p "Press enter to continue ..."
echo " >> continue"
s1="./darknet detector train cfg/"
s2=" cfg/"
s3=" > log/train_log.txt"
if [ "$backup_file"x = ""x ]
then
	cmd=$s1$data_cfg$s2$net_cfg
	$cmd > log/train_log.txt
else
	cmd=$s1$data_cfg$s2$net_cfg$backupfile
	$cmd > log/train_log.txt
fi
echo " >> trainning done\n"
read -p "Press enter to plot the loss-batch_number curve"
python plot_loss.py
echo " >> Done, the graph was saved in current path.\n"




