import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve, ConfusionMatrixDisplay
from sklearn.metrics import precision_score, recall_score, f1_score

"""

     Prescriptive - Answer the question (What action should we take?)

     Functions that might be useful for classification 
     - Confusion Matrix
     - plot the roc curve

"""


def visualize_confusion_matrix(y_test, y_predicted):
    confusion_matrix_ = confusion_matrix(y_test, y_predicted)
    cm_display = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix_, display_labels=[False, True])
    cm_display.plot()
    print({"Accuracy": accuracy_score(y_test, y_predicted),
           "Precision": precision_score(y_test, y_predicted),
           "Sensitivity_recall": recall_score(y_test, y_predicted),
           "Specificity": recall_score(y_test, y_predicted, pos_label=0),
           "F1_score": f1_score(y_test, y_predicted)
           })
    plt.show()


def plot_roc_curve(true_y, y_prob):
    """
    plots the roc curve based of the probabilities
    :param true_y:
    :param y_prob:
    :return:
    """
    fpr, tpr, thresholds = roc_curve(true_y, y_prob)
    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.show()
    print(f"AUC score: {roc_auc_score(true_y, y_prob)}")