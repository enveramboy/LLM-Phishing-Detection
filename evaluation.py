import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import pathlib

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
            evaluation: Dictionary containing True Positives, False Positives, True Negatives, False Negatives, Precision, Recall, Accuracy, and F1 Score of the model's predictions.
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
        accuracy = (TP + TN)/(TP + TN + FP + FN)

        # Store results in results dictionary
        evaluation = {
            "TP": TP,
            "FP": FP,
            "TN": TN,
            "FN": FN,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1_score,
            "Accuracy": accuracy
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

def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate precision, recall, and f1-score.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV")
    args = parser.parse_args()

    df = pd.read_csv(pathlib.Path(args.input))
    model_results = []
    for i in range(len(df)):
        model_results.append([df.iloc[i, 2], df.iloc[i, 1] == 'Phishing'])
        print([df.iloc[i, 2], df.iloc[i, 1] == 'Phishing'])
    evaluator = Evaluator()
    evaluation = evaluator.Evaluate(model_results)
    print(f"TP: {evaluation['TP']}")
    print(f"TN: {evaluation['TN']}")
    print(f"FP: {evaluation['FP']}")
    print(f"FN: {evaluation['FN']}")
    print(f"Precision: {evaluation['Precision']}")
    print(f"Recall: {evaluation['Recall']}")
    print(f"F1-Score: {evaluation['F1 Score']}")
    print(f"Accuracy: {evaluation['Accuracy']}")

# Example usage:
# read from cleaned_phishing_dataset.csv and evaluate it, printing results
# python evaluation.py --input cleaned_phishing_dataset.csv

if __name__ == "__main__":
    main()