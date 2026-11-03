from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.generators import (
    bahasa_indonesia,
    bahasa_inggris,
    biologi,
    ekonomi,
    fisika,
    geografi,
    ipa,
    ips,
    kimia,
    matematika,
    pengetahuan_umum,
    sejarah,
)

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = BASE_DIR / "data" / "questions.json"
USED_QUESTIONS_PATH = BASE_DIR / "data" / "used_questions.json"

GENERATORS = [
    ("Matematika", matematika),
    ("Geografi", geografi),
    ("Biologi", biologi),
    ("Bahasa Indonesia", bahasa_indonesia),
    ("Pengetahuan Umum", pengetahuan_umum),
    ("Bahasa Inggris", bahasa_inggris),
    ("Sejarah", sejarah),
    ("IPA", ipa),
    ("IPS", ips),
    ("Fisika", fisika),
    ("Kimia", kimia),
    ("Ekonomi", ekonomi),
]


def generate_all() -> list[dict]:
    all_raw_questions: list[dict] = []
    seen_prompts: set[str] = set()

    for subject_name, generator_module in GENERATORS:
        subject_qs = generator_module.generate()
        if len(subject_qs) != 500:
            raise ValueError(
                f"Subject '{subject_name}' generated {len(subject_qs)} questions; expected exactly 500."
            )
        for q in subject_qs:
            prompt = q["question"]
            if prompt in seen_prompts:
                raise ValueError(f"Duplicate question detected across bank: {prompt}")
            seen_prompts.add(prompt)
            all_raw_questions.append(q)

    # Assign sequential IDs: q0001 through q6000
    final_questions: list[dict] = []
    for idx, raw_q in enumerate(all_raw_questions, start=1):
        formatted = {
            "id": f"q{idx:04d}",
            "category": raw_q["category"],
            "question": raw_q["question"],
            "options": raw_q["options"],
            "correct_answer": raw_q["correct_answer"],
            "explanation": raw_q.get("explanation", f"Jawaban yang benar adalah {raw_q['options'][raw_q['correct_answer']]}."),
            "hint": raw_q.get("hint", f"Petunjuk: Pikirkan konsep dasar {raw_q['category']}."),
        }
        final_questions.append(formatted)

    return final_questions


def main():
    print("Generating comprehensive, 100% unique question bank...")
    questions = generate_all()
    print(f"Total questions generated: {len(questions)}")
    unique_count = len(set(q["question"] for q in questions))
    print(f"Unique question prompts: {unique_count}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"Saved to: {OUTPUT_PATH}")

    # Reset used_questions.json so gameplay starts completely fresh
    with open(USED_QUESTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    print(f"Reset {USED_QUESTIONS_PATH} to empty list.")


if __name__ == "__main__":
    main()
