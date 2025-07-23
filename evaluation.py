
def Evaluate(model_results):
    """
    Calculates Precision, Recall, and F1-Score of the model's results.

    Args:
        model_results: Data structure containing features, labels, and predictions.
    
    Returns:
        results: Dictionary containing Precision, Recall, and F1 Score of the model's predictions.
    """

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    # TODO: update TP, TN, FP, FN based off model results

    # Calculate Precision, Recall, and F1-Score
    precision = TP/(TP + FP)
    recall = TP/(TP + FN)
    f1_score = 2 * (precision * recall)/(precision + recall)

    # Store results in results dictionary
    results = {
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1_score
    }

    return results