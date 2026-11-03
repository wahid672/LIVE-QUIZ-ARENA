from __future__ import annotations

import random
from .common import build_mcq


def generate() -> list[dict]:
    questions: list[dict] = []
    seen_prompts: set[str] = set()

    def add_q(q_dict: dict) -> bool:
        if q_dict["question"] in seen_prompts:
            return False
        seen_prompts.add(q_dict["question"])
        questions.append(q_dict)
        return True

    # 1. Penjumlahan sederhana (120 soal)
    add_pairs = []
    for a in range(3, 35):
        for b in range(3, 30):
            add_pairs.append((a, b))
    random.seed(101)
    random.shuffle(add_pairs)

    for a, b in add_pairs:
        if len([q for q in questions if "+" in q["question"]]) >= 120:
            break
        ans = a + b
        wrongs = [str(ans + 1), str(ans - 1 if ans > 1 else ans + 3), str(ans + 2)]
        prompt = f"Berapa hasil dari {a} + {b}?"
        add_q(build_mcq(
            "Matematika",
            prompt,
            str(ans),
            wrongs,
            f"{a} ditambah {b} sama dengan {ans}.",
            "Hitung operasi penjumlahan dasar ini.",
        ))

    # 2. Pengurangan sederhana (120 soal)
    sub_pairs = []
    for a in range(15, 100):
        for b in range(3, 30):
            if a > b:
                sub_pairs.append((a, b))
    random.seed(102)
    random.shuffle(sub_pairs)

    for a, b in sub_pairs:
        if len([q for q in questions if "-" in q["question"]]) >= 120:
            break
        ans = a - b
        wrongs = [str(ans + 1), str(max(1, ans - 1)), str(ans + 2)]
        prompt = f"Berapa hasil dari {a} - {b}?"
        add_q(build_mcq(
            "Matematika",
            prompt,
            str(ans),
            wrongs,
            f"{a} dikurangi {b} sama dengan {ans}.",
            "Hitung operasi pengurangan dasar ini.",
        ))

    # 3. Perkalian dasar (120 soal)
    mul_pairs = []
    for a in range(2, 13):
        for b in range(2, 13):
            mul_pairs.append((a, b))
    for a in [14, 15, 20, 25]:
        for b in [2, 3, 4, 5]:
            mul_pairs.append((a, b))
    random.seed(103)
    random.shuffle(mul_pairs)

    for a, b in mul_pairs:
        if len([q for q in questions if "×" in q["question"]]) >= 120:
            break
        ans = a * b
        wrongs = [str(ans + a), str(max(1, ans - b)), str(ans + 2)]
        prompt = f"Berapa hasil dari {a} × {b}?"
        add_q(build_mcq(
            "Matematika",
            prompt,
            str(ans),
            wrongs,
            f"{a} dikali {b} hasilnya {ans}.",
            "Gunakan tabel perkalian dasar.",
        ))

    # 4. Pembagian bulat (80 soal)
    div_pairs = []
    for b in range(2, 13):
        for c in range(2, 16):
            div_pairs.append((b * c, b, c))
    random.seed(104)
    random.shuffle(div_pairs)

    for a, b, c in div_pairs:
        if len([q for q in questions if "÷" in q["question"]]) >= 80:
            break
        wrongs = [str(c + 1), str(max(1, c - 1)), str(c + 2)]
        prompt = f"Berapa hasil dari {a} ÷ {b}?"
        add_q(build_mcq(
            "Matematika",
            prompt,
            str(c),
            wrongs,
            f"{a} dibagi {b} hasilnya {c}.",
            "Operasi ini merupakan kebalikan dari perkalian.",
        ))

    # 5. Geometri, Bangun Datar, Satuan & Angka Romawi (60 soal)
    concept_facts = [
        ("Bangun datar yang memiliki 3 sisi dan 3 sudut adalah ...", "Segitiga", ["Persegi", "Lingkaran", "Trapesium"]),
        ("Bangun datar yang memiliki 4 sisi sama panjang dan 4 sudut siku-siku adalah ...", "Persegi", ["Segitiga", "Jajar genjang", "Trapesium"]),
        ("Bangun datar segiempat dengan sisi berhadapan sama panjang dan 4 sudut siku-siku adalah ...", "Persegi panjang", ["Segitiga", "Trapesium", "Lingkaran"]),
        ("Bangun datar segilima memiliki berapa sisi?", "5", ["4", "6", "8"]),
        ("Bangun datar segienam memiliki berapa sisi?", "6", ["5", "7", "8"]),
        ("Bangun datar segidelapan (oktagon) memiliki berapa sisi?", "8", ["6", "7", "10"]),
        ("Bangun datar yang tidak memiliki titik sudut adalah ...", "Lingkaran", ["Persegi", "Segitiga", "Trapesium"]),
        ("Besar sudut siku-siku adalah ...", "90 derajat", ["45 derajat", "60 derajat", "180 derajat"]),
        ("Besar sudut lurus adalah ...", "180 derajat", ["90 derajat", "270 derajat", "360 derajat"]),
        ("Besar satu putaran sudut penuh adalah ...", "360 derajat", ["180 derajat", "90 derajat", "270 derajat"]),
        ("Jumlah besar seluruh sudut dalam sebuah segitiga adalah ...", "180 derajat", ["90 derajat", "360 derajat", "270 derajat"]),
        ("Jumlah besar seluruh sudut dalam sebuah segiempat adalah ...", "360 derajat", ["180 derajat", "90 derajat", "270 derajat"]),
        ("Sudut yang besarnya kurang dari 90 derajat disebut sudut ...", "Lancip", ["Tumpul", "Siku-siku", "Refleks"]),
        ("Sudut yang besarnya antara 90 derajat sampai 180 derajat disebut sudut ...", "Tumpul", ["Lancip", "Siku-siku", "Nol"]),
        ("Garis yang membagi lingkaran menjadi dua bagian sama besar melewati titik pusat disebut ...", "Diameter", ["Jari-jari", "Tali busur", "Apotema"]),
        ("Panjang garis dari titik pusat ke tepi lingkaran disebut ...", "Jari-jari", ["Diameter", "Keliling", "Tali busur"]),
        ("Jika diameter lingkaran 14 cm, berapakah panjang jari-jarinya?", "7 cm", ["14 cm", "28 cm", "21 cm"]),
        ("Jika jari-jari lingkaran 10 cm, berapakah panjang diameternya?", "20 cm", ["10 cm", "5 cm", "30 cm"]),
        ("Keliling persegi dengan panjang sisi 5 cm adalah ...", "20 cm", ["15 cm", "25 cm", "10 cm"]),
        ("Keliling persegi dengan panjang sisi 8 cm adalah ...", "32 cm", ["24 cm", "64 cm", "16 cm"]),
        ("Luas persegi dengan panjang sisi 6 cm adalah ...", "36 cm²", ["24 cm²", "30 cm²", "12 cm²"]),
        ("Luas persegi dengan panjang sisi 7 cm adalah ...", "49 cm²", ["28 cm²", "42 cm²", "14 cm²"]),
        ("Luas persegi panjang dengan panjang 8 cm dan lebar 5 cm adalah ...", "40 cm²", ["26 cm²", "13 cm²", "35 cm²"]),
        ("Luas persegi panjang dengan panjang 10 cm dan lebar 4 cm adalah ...", "40 cm²", ["28 cm²", "14 cm²", "50 cm²"]),
        ("Keliling persegi panjang dengan panjang 6 cm dan lebar 4 cm adalah ...", "20 cm", ["24 cm", "10 cm", "16 cm"]),
        ("Keliling segitiga sama sisi dengan sisi 9 cm adalah ...", "27 cm", ["18 cm", "36 cm", "81 cm"]),
        ("1 jam sama dengan berapa menit?", "60 menit", ["30 menit", "100 menit", "120 menit"]),
        ("setengah jam sama dengan berapa menit?", "30 menit", ["15 menit", "45 menit", "60 menit"]),
        ("1 menit sama dengan berapa detik?", "60 detik", ["30 detik", "100 detik", "120 detik"]),
        ("1 hari sama dengan berapa jam?", "24 jam", ["12 jam", "48 jam", "60 jam"]),
        ("1 minggu sama dengan berapa hari?", "7 hari", ["5 hari", "6 hari", "10 hari"]),
        ("1 tahun ada berapa bulan?", "12 bulan", ["10 bulan", "14 bulan", "6 bulan"]),
        ("1 tahun masehi (bukan kabisat) memiliki berapa hari?", "365 hari", ["366 hari", "360 hari", "300 hari"]),
        ("Tahun kabisat masehi memiliki jumlah total hari dalam setahun sebanyak ...", "366 hari", ["365 hari", "360 hari", "364 hari"]),
        ("Bulan Februari pada tahun kabisat memiliki berapa hari?", "29 hari", ["28 hari", "30 hari", "31 hari"]),
        ("1 kilogram (kg) sama dengan berapa gram (g)?", "1.000 gram", ["100 gram", "10 gram", "10.000 gram"]),
        ("1 meter (m) sama dengan berapa sentimeter (cm)?", "100 cm", ["10 cm", "1.000 cm", "50 cm"]),
        ("1 kilometer (km) sama dengan berapa meter (m)?", "1.000 meter", ["100 meter", "10.000 meter", "500 meter"]),
        ("1 liter (L) sama dengan berapa mililiter (mL)?", "1.000 mL", ["100 mL", "500 mL", "10.000 mL"]),
        ("1 ton sama dengan berapa kilogram?", "1.000 kg", ["100 kg", "500 kg", "10.000 kg"]),
        ("1 kuintal sama dengan berapa kilogram?", "100 kg", ["1.000 kg", "50 kg", "10 kg"]),
        ("1 lusin sama dengan berapa buah?", "12 buah", ["10 buah", "20 buah", "24 buah"]),
        ("setengah lusin sama dengan berapa buah?", "6 buah", ["12 buah", "5 buah", "8 buah"]),
        ("2 lusin sama dengan berapa buah?", "24 buah", ["12 buah", "20 buah", "36 buah"]),
        ("1 kodi sama dengan berapa lembar/potong?", "20 buah", ["12 buah", "24 buah", "100 buah"]),
        ("1 rim kertas sama dengan berapa lembar?", "500 lembar", ["100 lembar", "1.000 lembar", "144 lembar"]),
        ("1 gross sama dengan berapa buah?", "144 buah", ["100 buah", "120 buah", "500 buah"]),
        ("Lambang angka Romawi untuk bilangan 5 adalah ...", "V", ["I", "X", "L"]),
        ("Lambang angka Romawi untuk bilangan 10 adalah ...", "X", ["V", "L", "C"]),
        ("Lambang angka Romawi untuk bilangan 50 adalah ...", "L", ["X", "C", "D"]),
        ("Lambang angka Romawi untuk bilangan 100 adalah ...", "C", ["L", "D", "M"]),
        ("Lambang angka Romawi untuk bilangan 500 adalah ...", "D", ["C", "M", "L"]),
        ("Lambang angka Romawi untuk bilangan 1.000 adalah ...", "M", ["D", "C", "K"]),
        ("Bilangan 4 dalam angka Romawi ditulis sebagai ...", "IV", ["VI", "IIII", "V"]),
        ("Bilangan 9 dalam angka Romawi ditulis sebagai ...", "IX", ["XI", "VIIII", "X"]),
        ("Bilangan 15 dalam angka Romawi ditulis sebagai ...", "XV", ["VX", "XIIIII", "XX"]),
        ("Bilangan 20 dalam angka Romawi ditulis sebagai ...", "XX", ["VV", "X", "XL"]),
        ("Bilangan yang hanya memiliki dua faktor, yaitu 1 dan dirinya sendiri disebut ...", "Bilangan prima", ["Bilangan genap", "Bilangan ganjil", "Bilangan komposit"]),
        ("Bilangan prima terkecil adalah ...", "2", ["1", "3", "0"]),
        ("Satu-satunya bilangan prima yang genap adalah ...", "2", ["4", "6", "0"]),
    ]

    for question_text, correct, wrongs in concept_facts:
        if len(questions) >= 500:
            break
        add_q(build_mcq(
            "Matematika",
            question_text,
            correct,
            wrongs,
            f"{question_text} Jawabannya adalah {correct}.",
            "Pikirkan konsep dasar matematika dan satuan pengukuran.",
        ))

    # Pad to exactly 500 if needed with more additions/multiplications
    extra_a = 50
    while len(questions) < 500:
        extra_a += 1
        prompt = f"Berapa hasil penjumlahan {extra_a} + 10?"
        ans = str(extra_a + 10)
        wrongs = [str(extra_a + 9), str(extra_a + 11), str(extra_a + 20)]
        add_q(build_mcq("Matematika", prompt, ans, wrongs, f"{extra_a} + 10 = {ans}.", "Hitung operasi penjumlahan."))

    return questions[:500]
