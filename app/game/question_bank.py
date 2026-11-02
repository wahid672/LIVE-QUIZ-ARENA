import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Question:
    id: str
    category: str
    question: str
    options: dict[str, str]
    correct_answer: str
    explanation: str
    hint: str

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Question":
        required = {
            "id", "category", "question", "options",
            "correct_answer", "explanation", "hint"
        }
        missing = required - raw.keys()
        if missing:
            raise ValueError(f"Field soal belum lengkap: {', '.join(sorted(missing))}")

        options = {str(key).upper(): str(value) for key, value in raw["options"].items()}
        if set(options) != {"A", "B", "C", "D"}:
            raise ValueError(f"Soal {raw['id']} harus memiliki pilihan A, B, C, dan D.")

        correct_answer = str(raw["correct_answer"]).upper()
        if correct_answer not in options:
            raise ValueError(f"Kunci jawaban soal {raw['id']} harus A, B, C, atau D.")

        return cls(
            id=str(raw["id"]),
            category=str(raw["category"]),
            question=str(raw["question"]),
            options={key: options[key] for key in ("A", "B", "C", "D")},
            correct_answer=correct_answer,
            explanation=str(raw["explanation"]),
            hint=str(raw["hint"]),
        )

    def to_admin_dict(self) -> dict[str, Any]:
        """Data lengkap untuk dashboard lokal, termasuk kunci jawaban."""
        return {
            "id": self.id,
            "category": self.category,
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "hint": self.hint,
        }


class QuestionBank:
    def __init__(self, questions: list[Question]):
        if not questions:
            raise ValueError("Bank soal tidak boleh kosong.")

        ids = [question.id for question in questions]
        if len(ids) != len(set(ids)):
            raise ValueError("ID soal harus unik.")

        self._questions = {question.id: question for question in questions}

    @classmethod
    def from_file(cls, path: Path) -> "QuestionBank":
        if not path.exists():
            raise FileNotFoundError(f"File bank soal tidak ditemukan: {path}")

        with path.open("r", encoding="utf-8") as file:
            raw_questions = json.load(file)

        if not isinstance(raw_questions, list):
            raise ValueError("Isi file bank soal harus berupa JSON array.")

        return cls([Question.from_dict(item) for item in raw_questions])

    def get(self, question_id: str) -> Question:
        question = self._questions.get(question_id)
        if question is None:
            raise ValueError(f"Soal dengan ID '{question_id}' tidak ditemukan.")
        return question

    def all(self) -> list[Question]:
        return list(self._questions.values())

    def admin_list(self) -> list[dict[str, Any]]:
        return [question.to_admin_dict() for question in self.all()]
