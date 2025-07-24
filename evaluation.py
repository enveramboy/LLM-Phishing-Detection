import random

def Evaluate(model_results):
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

    return evaluation

mock_model_results = []
for i in range(100):
    mock_model_results.append([random.randint(0, 1), random.randint(0, 1)])

print(Evaluate(mock_model_results))