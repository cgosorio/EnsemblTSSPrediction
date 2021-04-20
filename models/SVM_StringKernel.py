import sys
sys.path.append("../utils")
from ReadData import seqfile_to_instances
from WDKernel import wdkernel, get_K_value
import time

from strkernel.mismatch_kernel import MismatchKernel
from strkernel.mismatch_kernel import preprocess

from Bio import SeqIO
from Bio.Seq import Seq
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
from sklearn.metrics import classification_report  # classfication summary
import matplotlib.pyplot as plt
import numpy as np
from numpy import random

import pickle 

X_train_seqs_pos = seqfile_to_instances('../data/TIS/seqs/X_train_TISseqs_pos.txt')[::10]
print('xtrp', len(X_train_seqs_pos))
X_train_seqs_neg = seqfile_to_instances('../data/TIS/seqs/X_train_TISseqs_neg.txt')[::100]
print('xtrn', len(X_train_seqs_neg))
#X_val_seqs_pos = seqfile_to_instances('../data/TIS/seqs/X_val_TISseqs_pos.txt')
#X_val_seqs_neg = seqfile_to_instances('../data/TIS/seqs/X_val_TISseqs_neg.txt')
X_test_seqs_pos = seqfile_to_instances('../data/TIS/seqs/X_test_TISseqs_pos.txt')
X_test_seqs_neg = seqfile_to_instances('../data/TIS/seqs/X_test_TISseqs_neg.txt')




# train
X_train = np.concatenate([X_train_seqs_pos, X_train_seqs_neg])
y_train = np.concatenate([np.ones(len(X_train_seqs_pos), dtype=int), np.zeros(len(X_train_seqs_neg), dtype=int)])

X_train = wdkernel(X_train, d=3)

print('X_train shape:', X_train.shape)


# test

X_test = np.concatenate([X_test_seqs_pos, X_test_seqs_neg])
y_test = np.concatenate([np.ones(len(X_test_seqs_pos), dtype=int), np.zeros(len(X_test_seqs_neg), dtype=int)])

X_test = wdkernel(X_test, d=3)

print('X_test shape:', X_test.shape)





clf = SVC()
clf.fit(X_train, y_train)


y_true, y_pred = y_test, clf.predict(X_test)
print(classification_report(y_true, y_pred))

y_score = clf.decision_function(X_test)

# compute true positive rate and false positive rate
fpr, tpr, thresholds = roc_curve(y_test, y_score)
roc_auc = auc(fpr, tpr)  # compute auc

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating curve')
plt.legend(loc="lower right")
plt.show()