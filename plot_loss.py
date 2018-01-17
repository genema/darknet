# -*- encoding:utf-8 -*-
import numpy as np
import re
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import time

# >>>>>>>>>>>>>>>>>>>>>>> Plz be sure that u have train_log.txt in the path<<<<<<<<<<<<<<<<<<<<<<<<<<
log_file_path = "log/train_log.txt"
save_name = "plot_0713.png"

def get_batch_num(filename, b_n):
    log = open(filename)
    lines = log.readlines()
    for line in lines:
        temp = re.findall("batch No.(\d+)", line)
        if temp:
            batch_num = map(eval, temp)
            b_n.append(batch_num)
            # print batch_num


def get_loss(filename, loss):
    log = open(filename)
    lines = log.readlines()
    for line in lines:
        temp = re.findall("Loss (\d+\.?\d*)", line)
        if temp:
            temp_loss = map(eval, temp)
            loss.append(temp_loss)


def get_avg_loss(filename, avg_loss):
    log = open(filename)
    lines = log.readlines()
    for line in lines:
        temp = re.findall("avg_loss (\d+\.?\d*)", line)
        if temp:
            temp_avg_loss = map(eval, temp)
            avg_loss.append(temp_avg_loss)

if __name__ == '__main__':
    b_n = []
    loss = []
    avg_loss = []
    get_batch_num(log_file_path, b_n)
    get_loss(log_file_path, loss)
    get_avg_loss(log_file_path, avg_loss)
    b_n = np.array(b_n)
    b_n.resize([b_n.shape[1], b_n.shape[0]])
    loss = np.array(loss)
    loss.resize([loss.shape[1], loss.shape[0]])
    avg_loss = np.array(avg_loss)
    avg_loss.resize([avg_loss.shape[1], avg_loss.shape[0]])
    fig = plt.figure(figsize=(12 * (1 + b_n.shape[1]/10000), 12), dpi=100)
    print " >> Plotting...\n >> may take few minutes.\n"
    time1 = time.time()
    # print loss
    # print avg_loss
    # print b_n
    plt.plot(b_n, loss, color='r', marker='o', markersize=2)
    plt.plot(b_n, avg_loss, color='b', marker='x', markersize=4)
    plt.xlim(b_n.min() - 1000, b_n.max() + 1000)
    plt.ylim(loss.min() * 0.5, loss.max() * 1.1)
    plt.xticks(np.arange(b_n.min(), b_n.max(), 1000))
    plt.xlabel("Batch Number")
    plt.ylabel("Loss/Avg_loss")
    plt.title(' Loss & Avg_loss ')
    plt.grid()
    # plt.legend()
    # plt.show()
    plt.savefig(save_name, format='png')
    time2 = time.time()
    print " >> graph saved in current path, use %.2f secs\n" % (time2 - time1)
