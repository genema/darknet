# -*- encoding:utf-8 -*-
import numpy as np
import re
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
import time
import scipy.interpolate as interpolate

log_file_path = "test_set/mAP_recall.txt"
save_name = "model_0717.png"


def get_mAP_recall(filename, mAP, Recall):
    log = open(filename)
    lines = log.readlines()
    for line in lines:
        if re.findall("Recall: (\d+\.?\d*)", line):
            Recall.append(map(eval, re.findall("Recall: (\d+\.?\d*)", line))[0])
            mAP.append(map(eval, re.findall("mAP: (\d+\.?\d*)", line))[0])
        else:
            continue


if __name__ == '__main__':
    mAP = []
    Recall = []
    get_mAP_recall(log_file_path, mAP, Recall)
    print mAP
    print Recall
    fig = plt.figure(figsize=(12, 12))
    print " >> Plotting...\n >> may take few seconds.\n"
    time1 = time.time()
    f = interpolate.interp1d(Recall, mAP, kind='nearest')
    f2 = interpolate.interp1d(np.linspace(np.array(Recall).min(), np.array(Recall).max(), 10),
                              f(np.linspace(np.array(Recall).min(), np.array(Recall).max(), 10)), kind='cubic')
    f3 = interpolate.interp1d(np.linspace(np.array(Recall).min(), np.array(Recall).max(), 20),
                              f(np.linspace(np.array(Recall).min(), np.array(Recall).max(), 20)), kind='cubic')
    newx = np.linspace(np.array(Recall).min(), np.array(Recall).max(), 50)
    plt.plot(Recall, mAP, "bx")
    plt.plot(newx, f3(newx), color='purple')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.ylabel("mAP")
    plt.xlabel("Recall")
    plt.title('Performance')
    plt.grid()
    plt.savefig(save_name, format='png')
    time2 = time.time()
    print " >> graph saved in current path, use %.2f secs\n" % (time2 - time1)
