import json
from collections import Counter
from pathlib import Path


def test_question_bank_has_500_questions_for_each_subject():
    root = Path(__file__).resolve().parents[1]
    questions = json.loads((root / "data" / "questions.json").read_text(encoding="utf-8"))
    counts = Counter(item["category"] for item in questions)

    expected_subjects = {
        "Matematika", "Geografi", "Biologi", "Bahasa Indonesia",
        "Pengetahuan Umum", "Bahasa Inggris", "Sejarah", "IPA",
        "IPS", "Fisika", "Kimia", "Ekonomi",
    }
    assert len(questions) == 6000
    assert set(counts) == expected_subjects
    assert all(counts[subject] == 500 for subject in expected_subjects)


def test_each_question_has_four_distinct_options_and_a_valid_answer():
    root = Path(__file__).resolve().parents[1]
    questions = json.loads((root / "data" / "questions.json").read_text(encoding="utf-8"))
    for item in questions:
        options = item["options"]
        assert set(options) == {"A", "B", "C", "D"}
        assert len(set(options.values())) == 4
        assert item["correct_answer"] in options
        assert item["question"].strip()


def test_question_bank_items_have_required_fields():
    root = Path(__file__).resolve().parents[1]
    questions = json.loads((root / "data" / "questions.json").read_text(encoding="utf-8"))
    sample = questions[0]
    assert sample["id"].startswith("q")
    assert isinstance(sample["question"], str) and sample["question"]
    assert isinstance(sample["options"], dict) and set(sample["options"]) == {"A", "B", "C", "D"}
    assert sample["correct_answer"] in {"A", "B", "C", "D"}
    assert isinstance(sample["explanation"], str) and sample["explanation"]
    assert isinstance(sample["hint"], str) and sample["hint"]
