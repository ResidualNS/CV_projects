# -*- coding: utf-8 -*-
# __author__:YZY
import numpy as np
from my_utils.my_util import *
import time
import random
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

'''
画混淆矩阵 ROC曲线
'''
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    import itertools
    plt.imshow(cm, interpolation = 'nearest', cmap = cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation = 0)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis = 1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment = "center",
                 color = "white" if cm[i, j] > thresh else "black")

    # 去掉该语句，否则保存的混淆矩阵图左侧文字显示不全
    # plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def show_matrix(y_pred, y_true, classes_count, out_put_dir, fig_size=4, dpi=110):
    #cnf_matrix = confusion_matrix(y_true, y_pred)
    cnf_matrix = np.array([[2, 0, 0, 0], [2, 28, 1, 0], [1, 1, 20, 3], [1, 0, 1, 6]])
    # Plot non-normalized confusion matrix

    plt.figure(figsize = (fig_size, fig_size), dpi = dpi)
    classes = [str(x) for x in range(classes_count)]
    plot_confusion_matrix(cnf_matrix, classes = classes,
                               title = 'Confusion matrix')

    rand = random.randint(1, 1000)
    file_name = time.strftime("%Y-%m-%d-%H-%M_", time.localtime()) + str(rand) + ".png"
    file_path = os.path.abspath(out_put_dir + '/' + file_name)
    plt.savefig(file_path)

    # err = 0
    # for i in range(0, len(y_pred)):
    #     if y_pred[i] != y_true[i]:
    #         err += 1
    #
    # overall_acc = 1 - err * 1.0 / len(y_pred)
    # print(cnf_matrix)
    # acc_list = []
    # for i in range(cnf_matrix.shape[0]):
    #     acc = 100 * cnf_matrix[i, i] / np.sum(cnf_matrix[i, :])
    #     print('%02d acc: %.2f%%' % (i, acc))
    #     acc_list.append(acc)
    # print('overall acc: %.2f%%, avg acc: %.2f%%' % (100 * overall_acc, np.mean(acc_list)))
    #
    # return file_path

if __name__ == '__main__':
    to_check_path_result = r'E:\朱益洁dataset\数据准备'
    # y_true = np.array([[2, 0, 0, 0], [0, 31, 0, 0], [0, 0, 25, 0], [0, 0, 0, 8]])
    # y_pred = np.array([[2, 0, 0, 0], [2, 28, 1, 0], [1, 1, 20, 3], [1, 0, 1, 6]])
    y_true = [0, 0, 1, 2, 2, 3]
    y_pred = [1, 0, 1, 1, 2, 3]
    show_matrix(y_pred, y_true, 4, to_check_path_result)
    plt.show()