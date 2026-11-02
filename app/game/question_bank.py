import json
import re
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
    def __init__(self, questions: list[Question], filepath: Path | None = None):
        if not questions:
            raise ValueError("Bank soal tidak boleh kosong.")

        ids = [question.id for question in questions]
        if len(ids) != len(set(ids)):
            raise ValueError("ID soal harus unik.")

        self._questions = {question.id: question for question in questions}
        self._filepath = filepath

    @classmethod
    def from_file(cls, path: Path) -> "QuestionBank":
        if not path.exists():
            raise FileNotFoundError(f"File bank soal tidak ditemukan: {path}")

        with path.open("r", encoding="utf-8") as file:
            raw_questions = json.load(file)

        if not isinstance(raw_questions, list):
            raise ValueError("Isi file bank soal harus berupa JSON array.")

        return cls([Question.from_dict(item) for item in raw_questions], filepath=path)

    def get(self, question_id: str) -> Question:
        question = self._questions.get(question_id)
        if question is None:
            raise ValueError(f"Soal dengan ID '{question_id}' tidak ditemukan.")
        return question

    def all(self) -> list[Question]:
        return list(self._questions.values())

    def admin_list(self) -> list[dict[str, Any]]:
        return [question.to_admin_dict() for question in self.all()]

    def categories(self) -> list[str]:
        return sorted(list({q.category for q in self.all()}))

    def generate_next_id(self) -> str:
        max_num = 0
        for q_id in self._questions.keys():
            m = re.search(r"\d+", q_id)
            if m:
                val = int(m.group())
                if val > max_num:
                    max_num = val
        next_val = max_num + 1
        candidate = f"q{next_val:04d}" if next_val < 10000 else f"q{next_val}"
        while candidate in self._questions:
            next_val += 1
            candidate = f"q{next_val:04d}" if next_val < 10000 else f"q{next_val}"
        return candidate

    def add_question(self, raw: dict[str, Any], save: bool = True) -> Question:
        data = dict(raw)
        q_id = str(data.get("id") or "").strip()
        if not q_id:
            q_id = self.generate_next_id()
        if q_id in self._questions:
            raise ValueError(f"Soal dengan ID '{q_id}' sudah ada.")
        data["id"] = q_id
        question = Question.from_dict(data)
        self._questions[question.id] = question
        if save and self._filepath:
            self.save_to_file()
        return question

    def update_question(self, question_id: str, raw: dict[str, Any], save: bool = True) -> Question:
        if question_id not in self._questions:
            raise ValueError(f"Soal dengan ID '{question_id}' tidak ditemukan.")
        data = dict(raw)
        data["id"] = question_id
        question = Question.from_dict(data)
        self._questions[question_id] = question
        if save and self._filepath:
            self.save_to_file()
        return question

    def delete_question(self, question_id: str, save: bool = True) -> None:
        if question_id not in self._questions:
            raise ValueError(f"Soal dengan ID '{question_id}' tidak ditemukan.")
        if len(self._questions) <= 1:
            raise ValueError("Bank soal minimal harus menyisakan 1 soal.")
        del self._questions[question_id]
        if save and self._filepath:
            self.save_to_file()

    def save_to_file(self, path: Path | None = None) -> None:
        target = path or self._filepath
        if not target:
            return
        target.parent.mkdir(parents=True, exist_ok=True)
        temp_path = target.with_suffix(".tmp")
        data = [q.to_admin_dict() for q in self.all()]
        with temp_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp_path.replace(target)
