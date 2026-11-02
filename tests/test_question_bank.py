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


def test_question_bank_crud_operations(tmp_path):
    from app.game.question_bank import QuestionBank

    file_path = tmp_path / "questions.json"
    initial_data = [
        {
            "id": "q0001",
            "category": "Matematika",
            "question": "Berapa 1 + 1?",
            "options": {"A": "1", "B": "2", "C": "3", "D": "4"},
            "correct_answer": "B",
            "explanation": "1 + 1 = 2",
            "hint": "Dasar"
        },
        {
            "id": "q0002",
            "category": "IPA",
            "question": "Rumus air?",
            "options": {"A": "H2O", "B": "CO2", "C": "O2", "D": "NaCl"},
            "correct_answer": "A",
            "explanation": "H2O adalah air.",
            "hint": "Hidrogen dan oksigen"
        }
    ]
    file_path.write_text(json.dumps(initial_data), encoding="utf-8")

    bank = QuestionBank.from_file(file_path)
    assert len(bank.all()) == 2
    assert bank.categories() == ["IPA", "Matematika"]

    # 1. Add Question
    new_q = bank.add_question({
        "category": "Sejarah",
        "question": "Tahun kemerdekaan RI?",
        "options": {"A": "1940", "B": "1945", "C": "1950", "D": "1955"},
        "correct_answer": "B",
        "explanation": "17 Agustus 1945.",
        "hint": "Abad 20"
    })
    assert new_q.id == "q0003"
    assert len(bank.all()) == 3

    # Reload from file to ensure persistence
    reloaded = QuestionBank.from_file(file_path)
    assert len(reloaded.all()) == 3
    assert reloaded.get("q0003").question == "Tahun kemerdekaan RI?"

    # 2. Update Question
    updated = bank.update_question("q0003", {
        "category": "Sejarah",
        "question": "Kapan Indonesia merdeka?",
        "options": {"A": "1940", "B": "1945", "C": "1950", "D": "1955"},
        "correct_answer": "B",
        "explanation": "17 Agustus 1945.",
        "hint": "Abad 20"
    })
    assert updated.question == "Kapan Indonesia merdeka?"
    reloaded2 = QuestionBank.from_file(file_path)
    assert reloaded2.get("q0003").question == "Kapan Indonesia merdeka?"

    # 3. Delete Question
    bank.delete_question("q0003")
    assert len(bank.all()) == 2
    reloaded3 = QuestionBank.from_file(file_path)
    assert len(reloaded3.all()) == 2

    # Cannot delete down to 0
    bank.delete_question("q0002")
    try:
        bank.delete_question("q0001")
        assert False, "Harusnya error saat menyisakan 0 soal"
    except ValueError as e:
        assert "minimal" in str(e)


def test_question_api_crud_endpoints():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        # Search & pagination
        r_list = client.get("/api/questions?page=1&page_size=10&search=Berapa")
        assert r_list.status_code == 200
        data = r_list.json()
        assert "items" in data
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert data["total"] > 0

        # Create
        create_payload = {
            "category": "Uji Coba",
            "question": "Apakah ini soal uji coba?",
            "options": {"A": "Bukan", "B": "Ya", "C": "Mungkin", "D": "Ragu"},
            "correct_answer": "B",
            "explanation": "Ini hanya uji coba.",
            "hint": "Pilih Ya"
        }
        r_create = client.post("/api/questions", json=create_payload)
        assert r_create.status_code == 200
        created = r_create.json()["question"]
        qid = created["id"]
        assert created["question"] == "Apakah ini soal uji coba?"

        # Get Single
        r_single = client.get(f"/api/questions/{qid}")
        assert r_single.status_code == 200
        assert r_single.json()["id"] == qid

        # Update
        update_payload = {
            "category": "Uji Coba",
            "question": "Apakah ini soal uji coba update?",
            "options": {"A": "Bukan", "B": "Ya Betul", "C": "Mungkin", "D": "Ragu"},
            "correct_answer": "B",
            "explanation": "Penjelasan terupdate.",
            "hint": "Pilih Ya Betul"
        }
        r_update = client.put(f"/api/questions/{qid}", json=update_payload)
        assert r_update.status_code == 200
        assert r_update.json()["question"]["question"] == "Apakah ini soal uji coba update?"

        # Delete
        r_del = client.delete(f"/api/questions/{qid}")
        assert r_del.status_code == 200
        assert r_del.json()["status"] == "deleted"

        # 404 after delete
        r_404 = client.get(f"/api/questions/{qid}")
        assert r_404.status_code == 404
