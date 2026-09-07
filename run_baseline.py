import argparse
import json
import os
import sys

from anthropic import Anthropic

from study_agent.mastery import compute_weak_concepts
from study_agent.quiz_generator import generate_quiz


def main():
    parser = argparse.ArgumentParser(description="Generate a personalized quiz targeting weak concepts.")
    parser.add_argument("--material", required=True, help="Path to study material text file")
    parser.add_argument("--performance-log", required=True, help="Path to past performance JSON log")
    parser.add_argument("--num-questions", type=int, default=5, help="Number of quiz questions to generate")
    parser.add_argument("--threshold", type=float, default=0.7, help="Accuracy threshold below which a concept is 'weak'")
    parser.add_argument("--output", default="outputs/quiz_output.json", help="Where to save the generated quiz")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    with open(args.material, "r") as f:
        study_material = f.read()

    with open(args.performance_log, "r") as f:
        performance_log = json.load(f)

    weak_concepts = compute_weak_concepts(performance_log, threshold=args.threshold)

    print("=== Weak Concepts Detected ===")
    if not weak_concepts:
        print("(none below threshold - generating a general review quiz)")
    for wc in weak_concepts:
        print(f"  - {wc['concept']}: {wc['accuracy']:.0%} accuracy over {wc['attempts']} attempts")
    print()

    client = Anthropic(api_key=api_key)
    quiz = generate_quiz(study_material, weak_concepts, args.num_questions, client)

    print("=== Generated Quiz ===")
    for i, q in enumerate(quiz, 1):
        print(f"\nQ{i} [{q.get('concept', 'unknown')}]: {q['question']}")
        for choice in q["choices"]:
            print(f"   - {choice}")
        print(f"   Correct answer: {q['correct_answer']}")
        print(f"   Explanation: {q['explanation']}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(quiz, f, indent=2)
    print(f"\nSaved quiz to {args.output}")


if __name__ == "__main__":
    main()
