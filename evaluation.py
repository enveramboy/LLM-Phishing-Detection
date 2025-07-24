import random
import numpy as np
import matplotlib.pyplot as plt

class Evaluator():
    """
    Evaluator object that encapsulates evaluation functionality for model_results.
    """

    def __init__(self):
        self.evaluations = []

    def Evaluate(self, model_results):
        """
        Calculates Precision, Recall, and F1-Score of the model's results.

        Args:
            model_results: List of predictions, along with their corresponding labels. Indexes correspond to original index of the feature.
    
        Returns:
            evaluation: Dictionary containing True Positives, False Positives, True Negatives, False Negatives, Precision, Recall, and F1 Score of the model's predictions.
        """

        TP = 0
        FP = 0
        TN = 0
        FN = 0
    
        # Calculate TP, FP, FN
        for model_result in model_results:
            if model_result[0] != model_result[1]:
                if model_result[0] == 1: FP += 1
                else: FN += 1
            else: 
                if model_result[0] == 1: TP += 1
                else: TN += 1

        # Calculate Precision, Recall, and F1-Score
        precision = TP/(TP + FP)
        recall = TP/(TP + FN)
        f1_score = 2 * (precision * recall)/(precision + recall)

        # Store results in results dictionary
        evaluation = {
            "TP": TP,
            "FP": FP,
            "TN": TN,
            "FN": FN,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1_score
        }

        self.evaluations.append(evaluation)

        return evaluation

    def _Plot(self, target):
        """
        Plots target in all currently stored evaluations.

        Args:
            target (str): Name of dictionary entry to plot.
        """
        x = np.linspace(0, len(self.evaluations)-1, len(self.evaluations))
        y = []
        for evaluation in self.evaluations: y.append(evaluation[target])
        plt.figure(f"{target} Over Iterations")
        plt.plot(x, y, label=target, color='green')
        plt.title(f"{target} Over Iterations")
        plt.xlabel('Iteration')
        plt.ylabel(target)
        plt.legend()
        plt.grid(True)
        plt.show()

    def Plot_Precision(self): 
        """
        Plots Precision Over Iterations of all evaluations ran by evaluator.
        """
        self._Plot('Precision')
    def Plot_Recall(self): 
        """
        Plots Recall Over Iterations of all evaluations ran by evaluator.
        """
        self._Plot('Recall')
    def Plot_F1_Score(self): 
        """
        Plots F1 Score Over Iterations of all evaluations ran by evaluator.
        """
        self._Plot('F1 Score')

# Testing
evaluator = Evaluator()
mock_model_results = []
for i in range(100):
    mock_model_results = []
    for x in range(100):
        mock_model_results.append([random.randint(0, 1), random.randint(0, 1)])
    evaluator.Evaluate(mock_model_results)

evaluator.Plot_Precision()
evaluator.Plot_Recall()
evaluator.Plot_F1_Score()