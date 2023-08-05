from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    roc_auc_score,
)
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def show_classification(y_test, y_pred):
    r"""
    Confusion matrix

    - Binary:
      - y_test: [1, 0, 1, 0, 1]
      - y_pred: [0.1, 0.2, 0.9, 0, 0.8]
    - Multi:
      - y_test: [1, 2, 1, 0, 1]
      - y_pred: [[0.1, 0.8, 0.1], [0.1, 0.2, 0.7], [0.1, 0.6, 0.3], [0.5, 0.3. 0.2], [0.1, 0.6, 0.4]]
    """
    cm = confusion_matrix(y_test, y_pred)
    TN = cm[0, 0]
    TP = cm[1, 1]
    FP = cm[0, 1]
    FN = cm[1, 0]
    print(sum(y_test), sum(y_pred))
    print("Confusion matrix\n\n", cm)
    print("\nTrue Negatives(TN) = ", TN)
    print("\nTrue Positives(TP) = ", TP)
    print("\nFalse Positives(FP) = ", FP)
    print("\nFalse Negatives(FN) = ", FN)

    classification_accuracy = (TP + TN) / float(TP + TN + FP + FN)
    print("Classification accuracy : {0:0.4f}".format(classification_accuracy))
    classification_error = (FP + FN) / float(TP + TN + FP + FN)
    print("Classification error : {0:0.4f}".format(classification_error))
    precision = TP / float(TP + FP)
    print("Precision : {0:0.4f}".format(precision))
    recall = TP / float(TP + FN)
    print("Recall or Sensitivity : {0:0.4f}".format(recall))
    true_positive_rate = TP / float(TP + FN)
    print("True Positive Rate : {0:0.4f}".format(true_positive_rate))
    false_positive_rate = FP / float(FP + TN)
    print("False Positive Rate : {0:0.4f}".format(false_positive_rate))
    specificity = TN / (TN + FP)
    print("Specificity : {0:0.4f}".format(specificity))

    cm_matrix = pd.DataFrame(
        data=cm.T,
        columns=["Actual Negative:0", "Actual Positive:1"],
        index=["Predict Negative:0", "Predict Positive:1"],
    )
    sns.heatmap(cm_matrix, annot=True, fmt="d", cmap="YlGnBu")

    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    plt.plot(fpr, tpr, linewidth=2)
    plt.plot([0, 1], [0, 1], "k--")
    plt.rcParams["font.size"] = 12
    plt.title("ROC curve for Predicting a Pulsar Star classifier")
    plt.xlabel("False Positive Rate (1 - Specificity)")
    plt.ylabel("True Positive Rate (Sensitivity)")
    plt.show()

    ROC_AUC = roc_auc_score(y_test, y_pred)
    print("ROC AUC : {:.4f}".format(ROC_AUC))
