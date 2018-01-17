import pickle
import os
import numpy as np

# >>>>>>>>>>>>>>>>>> Change the following value <<<<<<<<<<<<<<<<<<<
image_num = 5.  # How many pic u have in the test set
cls_num = 18  # the class number of your network model
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
iou_thresh = 0.5
count_per_class = np.zeros(cls_num)


def parse_ground_truth(image_id):
    return np.loadtxt("labels/" + str(image_id) + ".txt")


def parse_result(image_id):
    return np.loadtxt("results/" + str(image_id) + ".txt")


def dataset_info_get(ground_truth):
    if len(list(ground_truth.shape)) == 1:
        count_per_class[int(ground_truth[0])] += 1
    else:
        for i in range(0, ground_truth.shape[0]):
            count_per_class[int(ground_truth[i][0])] += 1


def overlap(l, r, r_l, r_r):
    left = bool(l > r_l) and l or r_l
    right = bool(r < r_r) and r or r_r
    return right - left


def calc_intersection(left, right, r_left, r_right, top, bot, r_top, r_bot):
    w = overlap(left, right, r_left, r_right)
    h = overlap(top, bot, r_top, r_bot)
    if (w < 0) or (h < 0):
        return 0
    else:
        return w * h


def calc_union(inter, wid, hei, r_wid, r_hei):
    temp = wid * hei + r_wid * r_hei - inter
    if temp <= 0:
        print " Err : U <= 0 ,use .001 instead\n"
        return 0.001
    else:
        return temp


def calc(ground_truth, result):
    true_pos = np.zeros(cls_num)
    false_pos = np.zeros(cls_num)
    i = 0
    if len(list(result.shape)) == 1:
        if len(list(ground_truth.shape)) == 1:
            g_t_class = ground_truth[0]
            wid = ground_truth[3]
            hei = ground_truth[4]
            left = ground_truth[1] - wid/2
            top = ground_truth[2] - hei/2
            right = left + wid
            bot = top + hei
            r_class = result[0]
            r_left = result[1]
            r_top = result[2]
            r_wid = result[3]
            r_hei = result[4]
            r_right = r_left + r_wid
            r_bot = r_top + r_hei
            inter = calc_intersection(left, right, r_left, r_right, top, bot, r_top, r_bot)
            uni = calc_union(inter, wid, hei, r_wid, r_hei)
            iou = inter / uni
            if iou >= iou_thresh:
                if (g_t_class - r_class) < 1:
                    true_pos[int(r_class)] += 1
                else:
                    false_pos[int(r_class)] += 1

        else:
            while i < ground_truth.shape[0]:
                g_t_class = ground_truth[i][0]
                wid = ground_truth[i][3]
                hei = ground_truth[i][4]
                left = ground_truth[i][1] - wid/2
                top = ground_truth[i][2] - hei/2
                right = left + wid
                bot = top + hei
                r_class = result[0]
                r_left = result[1]
                r_top = result[2]
                r_wid = result[3]
                r_hei = result[4]
                r_right = r_left + r_wid
                r_bot = r_top + r_hei
                inter = calc_intersection(left, right, r_left, r_right, top, bot, r_top, r_bot)
                uni = calc_union(inter, wid, hei, r_wid, r_hei)
                iou = inter / uni
                if iou >= iou_thresh:
                    if (g_t_class - r_class) < 1:
                        true_pos[int(r_class)] += 1
                    else:
                        false_pos[int(r_class)] += 1
                i += 1
    else:
        while i < ground_truth.shape[0]:
            g_t_class = ground_truth[i][0]
            wid = ground_truth[i][3]
            hei = ground_truth[i][4]
            left = ground_truth[i][1] - wid/2
            top = ground_truth[i][2] - hei/2
            right = left + wid
            bot = top + hei
            j = 0
            while j < result.shape[0]:
                r_class = result[j][0]
                r_left = result[j][1]
                r_top = result[j][2]
                r_wid = result[j][3]
                r_hei = result[j][4]
                r_right = r_left + r_wid
                r_bot = r_top + r_hei
                inter = calc_intersection(left, right, r_left, r_right, top, bot, r_top, r_bot)
                uni = calc_union(inter, wid, hei, r_wid, r_hei)
                iou = inter / uni
                if iou >= iou_thresh:
                    if (g_t_class - r_class) < 1:
                        true_pos[int(r_class)] += 1
                    else:
                        false_pos[int(r_class)] += 1
                j += 1
            i += 1
    return true_pos, false_pos

if __name__ == "__main__":
    sum_tp = np.zeros(cls_num)
    sum_fp = np.zeros(cls_num)
    for i in range(0, int(image_num)):
        g_t = parse_ground_truth(i)
        dataset_info_get(g_t)

    for image_id in range(0, int(image_num)):
        g_t = parse_ground_truth(image_id)
        if os.path.getsize("results/" + str(image_id) + ".txt"):
            r = parse_result(image_id)
            true_pos, false_pos = calc(g_t, r)
            for x in range(0, cls_num):
                sum_tp[x] += true_pos[x]
                sum_fp[x] += false_pos[x]

    print " >> Test set info:\n"
    g_t_not_empty_cls = 0.
    result_not_empty_cls = 0.
    sum_recall = 0
    sum_map = 0
    # print count_per_class
    # print sum_tp
    for i in range(0, cls_num):
        if count_per_class[i]:
            g_t_not_empty_cls += 1
            if sum_tp[i]:
                result_not_empty_cls += 1
                print "class:%d  --> sample number: %d \n" % (i, count_per_class[i])
                print "          --> mean_average_precision: %.2f  re-call: %.2f\n"\
                      % (sum_tp[i]/(sum_tp[i]+sum_fp[i]), sum_tp[i]/count_per_class[i])
                sum_recall += sum_tp[i]/count_per_class[i]
                sum_map += sum_tp[i]/(sum_tp[i]+sum_fp[i])
            else:
                print "class:%d  --> sample number: %d \n" % (i, count_per_class[i])
                print "          --> mean_average_precision: none  re-call: 0\n"

    if g_t_not_empty_cls:
        print " >> Recall: %.2f  mAP: %.2f \n" % (sum_recall/g_t_not_empty_cls, sum_map/result_not_empty_cls)

