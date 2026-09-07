# Adaptive AI Study Agent (Baseline)

A minimal, runnable baseline for a study agent that adapts to a student's
**quiz/test performance**. Given a study-material file and a log of past
quiz attempts (tagged by concept), it identifies the student's weak
concepts and generates a personalized quiz (with explanations) that
targets those weak spots.

## How it works

1. `study_agent/mastery.py` — a pure rule-based pass (no LLM) that groups
   past quiz attempts by concept and computes accuracy per concept.
   Concepts below a threshold (default 70%) are flagged as "weak."
2. `study_agent/quiz_generator.py` — sends the study material and the list
   of weak concepts to Claude (`claude-haiku-4-5-20251001`), asking it to
   generate multiple-choice questions targeting those concepts, with an
   answer key and an explanation for each.
3. `run_baseline.py` — CLI that wires the two together, prints the quiz,
   and saves it as JSON.

## Setup

```bash
git clone <this-repo-url>
cd adaptive-study-agent
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## API key

You need an Anthropic API key (get one at https://console.anthropic.com/).

```bash
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY=sk-ant-...
export $(cat .env | xargs)     # or use python-dotenv / your shell's method of loading .env
```

The script reads the key from the `ANTHROPIC_API_KEY` environment variable.

## Run it

```bash
python run_baseline.py \
  --material examples/study_material.txt \
  --performance-log examples/performance_log.json \
  --num-questions 4
```

- **Input:** `examples/study_material.txt` (notes on Binary Search Trees) and
  `examples/performance_log.json` (a sample log of 18 past quiz attempts
  across 5 BST concepts).
- **Output:** printed to the terminal, and saved to
  `outputs/quiz_output.json`.

### Optional flags

- `--threshold` — accuracy cutoff below which a concept counts as "weak" (default `0.7`)
- `--output` — where to save the generated quiz JSON (default `outputs/quiz_output.json`)

## Test case

With the provided example files, the performance log gives:

- `insertion`: 75% (not weak)
- `search`: 100% (not weak)
- `deletion`: 25% (weak)
- `tree_balance`: 33% (weak)
- `in_order_traversal`: 100% (not weak)

Running the baseline correctly detects `deletion` and `tree_balance` as the
weak concepts and generates questions only about those two topics, each
with a correct answer and an explanation grounded in `study_material.txt`.
See `proposal/` for a sample run's full output and screenshot.

## Known limitations

- Single LLM call, no retry/repair loop if the model's JSON output is malformed.
- Mastery model is a simple accuracy threshold, not a real spaced-repetition
  or Bayesian knowledge-tracing model.
- No persistence of quiz results back into the performance log (the loop
  is not yet closed — a future version would update the log after each
  quiz attempt).
- Only supports multiple-choice questions currently.
