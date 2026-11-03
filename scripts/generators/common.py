from __future__ import annotations

import random
from typing import Any

CATEGORY_FALLBACKS: dict[str, list[str]] = {
    "Matematika": ["0", "1", "10", "15", "20", "25", "50", "100"],
    "Geografi": ["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar", "Tokyo", "London", "Paris"],
    "Biologi": ["Jantung", "Paru-paru", "Hati", "Akar", "Daun", "Batang", "Herbivora", "Karnivora"],
    "Bahasa Indonesia": ["Baku", "Sinonim", "Antonim", "Kiasan", "Subjek", "Predikat"],
    "Pengetahuan Umum": ["Indonesia", "Garuda", "Merah Putih", "Jakarta", "Pancasila"],
    "Bahasa Inggris": ["Book", "Water", "House", "School", "Happy", "Family"],
    "Sejarah": ["1945", "Soekarno", "Mohammad Hatta", "Majapahit", "Diponegoro", "Borobudur"],
    "IPA": ["Oksigen", "Matahari", "Bumi", "Gravitasi", "Padat", "Cair", "Fotosintesis"],
    "IPS": ["Produsen", "Konsumen", "Distributor", "Pasar", "Desa", "Gotong Royong"],
    "Fisika": ["Newton", "Meter", "Joule", "Watt", "Gravitasi", "Gesekan", "Cermin"],
    "Kimia": ["H2O", "O2", "CO2", "NaCl", "Asam", "Basa", "Padat", "Larutan"],
    "Ekonomi": ["Uang", "Pasar", "Bank", "Laba", "Produksi", "Konsumsi", "Ekspor", "Impor"],
}


def build_mcq(
    category: str,
    question: str,
    correct: Any,
    wrongs: list[Any],
    explanation: str = "",
    hint: str = "",
) -> dict[str, Any]:
    correct_str = str(correct).strip()
    clean_wrongs: list[str] = []

    for w in wrongs:
        w_str = str(w).strip()
        if w_str and w_str != correct_str and w_str not in clean_wrongs:
            clean_wrongs.append(w_str)

    # If fewer than 3 distractors, draw from fallbacks
    fallbacks = CATEGORY_FALLBACKS.get(category, ["Pilihan A", "Pilihan B", "Pilihan C", "Pilihan D"])
    for fb in fallbacks:
        if len(clean_wrongs) >= 3:
            break
        fb_str = str(fb).strip()
        if fb_str and fb_str != correct_str and fb_str not in clean_wrongs:
            clean_wrongs.append(fb_str)

    # Extra safety guarantee
    extra_idx = 1
    while len(clean_wrongs) < 3:
        cand = f"Opsi {extra_idx}"
        if cand != correct_str and cand not in clean_wrongs:
            clean_wrongs.append(cand)
        extra_idx += 1

    options = [correct_str, clean_wrongs[0], clean_wrongs[1], clean_wrongs[2]]
    random.shuffle(options)

    option_map = {
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
    }

    correct_label = next(k for k, v in option_map.items() if v == correct_str)

    if not explanation:
        explanation = f"Jawaban yang tepat adalah {correct_str}."
    if not hint:
        hint = f"Fokus pada konsep {category.lower()}."

    return {
        "category": category,
        "question": question.strip(),
        "options": option_map,
        "correct_answer": correct_label,
        "explanation": explanation.strip(),
        "hint": hint.strip(),
    }
