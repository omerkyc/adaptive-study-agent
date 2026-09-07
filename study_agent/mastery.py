from collections import defaultdict


def compute_weak_concepts(performance_log, threshold=0.7):
    correct_counts = defaultdict(int)
    total_counts = defaultdict(int)

    for attempt in performance_log:
        concept = attempt["concept"]
        total_counts[concept] += 1
        if attempt["correct"]:
            correct_counts[concept] += 1

    accuracies = []
    for concept, total in total_counts.items():
        accuracy = correct_counts[concept] / total
        accuracies.append({"concept": concept, "accuracy": accuracy, "attempts": total})

    weak = [a for a in accuracies if a["accuracy"] < threshold]
    weak.sort(key=lambda a: a["accuracy"])
    return weak
