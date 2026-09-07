import json

MODEL = "claude-haiku-4-5-20251001"


def build_prompt(study_material, weak_concepts, num_questions):
    concept_list = ", ".join(c["concept"] for c in weak_concepts) or "general review"

    return f"""You are a study tutor. Using ONLY the study material below, write {num_questions} multiple-choice questions that focus on these weak concepts the student needs more practice on: {concept_list}.

Study material:
---
{study_material}
---

Respond with ONLY a JSON array (no markdown fences, no extra text). Each element must have exactly these keys:
- "question": string
- "choices": array of 4 strings
- "correct_answer": string (must exactly match one of the choices)
- "concept": string (which weak concept this targets)
- "explanation": string (why the correct answer is right, referencing the study material)
"""


def generate_quiz(study_material, weak_concepts, num_questions, client):
    prompt = build_prompt(study_material, weak_concepts, num_questions)

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    quiz = json.loads(raw_text)
    return quiz
