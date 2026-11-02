from __future__ import annotations

import json
import random
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = BASE_DIR / "data" / "questions.json"


def build_mcq(category: str, question: str, correct: str, wrongs: list[str], explanation: str, hint: str):
    options = [str(correct)]
    for candidate in wrongs:
        candidate = str(candidate)
        if candidate not in options and len(options) < 4:
            options.append(candidate)

    # Some legacy geography distractor lists contain the correct answer twice.
    # Fill any missing option with a relevant, distinct fallback instead of
    # showing duplicate choices to viewers.
    fallback_by_category = {
        "Geografi": [
            "Malaysia", "Singapura", "Manila", "Canberra", "Paris", "London",
            "Brasilia", "New Delhi", "Kairo", "Riyadh", "Samarinda", "Bandung",
            "Semarang", "Surabaya", "Padang", "Pekanbaru", "Jayapura", "Denpasar",
            "Asia", "Afrika", "Eropa", "Samudra Pasifik",
        ],
    }
    fallback = fallback_by_category.get(category, [
        "Pilihan lainnya", "Tidak diketahui", "Semua pilihan salah", "Tidak ada jawaban",
    ])
    for candidate in fallback:
        if candidate not in options and len(options) < 4:
            options.append(candidate)
    while len(options) < 4:
        candidate = f"Pilihan {len(options) + 1}"
        if candidate not in options:
            options.append(candidate)

    random.shuffle(options)
    labels = ["A", "B", "C", "D"]
    option_map = {label: option for label, option in zip(labels, options)}
    correct_label = next(label for label, option in option_map.items() if option == str(correct))
    return {
        "category": category,
        "question": question,
        "options": option_map,
        "correct_answer": correct_label,
        "explanation": explanation,
        "hint": hint,
    }


def generate_matematika():
    questions = []

    # Penjumlahan
    for a in range(2, 27):
        for b in range(2, 22):
            correct = str(a + b)
            wrongs = [str(a + b + 1), str(a + b - 1), str(a + b + 2)]
            questions.append(build_mcq(
                "Matematika",
                f"Berapa hasil {a} + {b}?",
                correct,
                wrongs,
                f"{a} + {b} = {correct}.",
                "Ini operasi penjumlahan dasar.",
            ))

    # Pengurangan
    for a in range(20, 90, 2):
        for b in range(1, 10):
            if a - b < 0:
                continue
            correct = str(a - b)
            wrongs = [str(a - b + 1), str(max(0, a - b - 1)), str(a - b + 2)]
            questions.append(build_mcq(
                "Matematika",
                f"Berapa hasil {a} - {b}?",
                correct,
                wrongs,
                f"{a} - {b} = {correct}.",
                "Ini operasi pengurangan dasar.",
            ))

    # Perkalian
    for a in range(2, 13):
        for b in range(2, 13):
            correct = str(a * b)
            wrongs = [str(a * b + a), str(a * b - b if a*b-b > 0 else a*b+1), str(a * b + 2)]
            questions.append(build_mcq(
                "Matematika",
                f"Berapa hasil {a} × {b}?",
                correct,
                wrongs,
                f"{a} dikali {b} hasilnya {correct}.",
                "Ingat tabel perkalian.",
            ))

    # Pembagian sederhana
    for b in range(2, 11):
        for c in range(2, 16):
            a = b * c
            correct = str(c)
            wrongs = [str(c + 1), str(max(1, c - 1)), str(c + 2)]
            questions.append(build_mcq(
                "Matematika",
                f"Berapa hasil {a} ÷ {b}?",
                correct,
                wrongs,
                f"{a} dibagi {b} = {c}.",
                "Gunakan kebalikan dari perkalian.",
            ))

    # Bentuk dan satuan
    shape_facts = [
        ("Segitiga", "3"), ("Persegi", "4"), ("Persegi panjang", "4"),
        ("Pentagon", "5"), ("Heksagon", "6"), ("Oktagon", "8"),
    ]
    for shape, sides in shape_facts:
        questions.append(build_mcq(
            "Matematika",
            f"{shape} memiliki berapa sisi?",
            sides,
            [str(int(sides)+1), str(max(1, int(sides)-1)), str(int(sides)+2)],
            f"{shape} memiliki {sides} sisi.",
            "Hitung jumlah sisi pada bangun datar.",
        ))

    # Genap ganjil
    for n in range(10, 110):
        correct = "Genap" if n % 2 == 0 else "Ganjil"
        wrongs = ["Ganjil", "Genap", "Bilangan prima"] if correct == "Genap" else ["Genap", "Ganjil", "Bilangan prima"]
        questions.append(build_mcq(
            "Matematika",
            f"Bilangan {n} termasuk bilangan apa?",
            correct,
            [w for w in wrongs if w != correct][:3],
            f"{n} adalah bilangan {correct.lower()}.",
            "Lihat angka terakhirnya.",
        ))

    dedup = []
    seen = set()
    for q in questions:
        if q["question"] in seen:
            continue
        seen.add(q["question"])
        dedup.append(q)
    return dedup[:500]


def generate_biologi():
    questions = []

    organs = [
        ("jantung", "memompa darah"), ("paru-paru", "membantu pernapasan"),
        ("otak", "mengatur aktivitas tubuh"), ("lambung", "mencerna makanan"),
        ("ginjal", "menyaring darah"), ("mata", "melihat"), ("telinga", "mendengar"),
        ("hidung", "mencium bau"), ("lidah", "mengecap rasa"), ("kulit", "merasakan sentuhan"),
    ]
    for organ, fungsi in organs:
        questions.append(build_mcq(
            "Biologi",
            f"Apa fungsi utama {organ}?",
            fungsi,
            ["memompa udara", "membuat tulang", "menghasilkan rambut"],
            f"Fungsi utama {organ} adalah {fungsi}.",
            "Pikirkan peran organ itu dalam tubuh.",
        ))

    body_parts = [
        ("manusia", "jantung"), ("ikan", "insang"), ("burung", "sayap"),
        ("sapi", "paru-paru"), ("katak", "kulit"), ("unta", "punuk"),
    ]
    for makhluk, bagian in body_parts:
        questions.append(build_mcq(
            "Biologi",
            f"Bagian tubuh penting pada {makhluk} untuk ciri khasnya adalah ...",
            bagian,
            ["roda", "mesin", "baut"],
            f"{makhluk.title()} memiliki ciri khas {bagian}.",
            "Ingat ciri khas makhluk hidup tersebut.",
        ))

    animals = [
        ("herbivora", "pemakan tumbuhan", ["pemakan daging", "pemakan batu", "pemakan logam"]),
        ("karnivora", "pemakan daging", ["pemakan daun", "pemakan buah saja", "pemakan kayu"]),
        ("omnivora", "pemakan segala", ["pemakan udara", "pemakan tanah", "pemakan pasir"]),
    ]
    for istilah, arti, wrongs in animals:
        for prefix in ["Istilah", "Hewan dengan sifat", "Arti kata"]:
            questions.append(build_mcq(
                "Biologi",
                f"{prefix} {istilah} adalah ...",
                arti,
                wrongs,
                f"{istilah.title()} berarti {arti}.",
                "Ini tentang jenis makanan hewan.",
            ))

    senses = [
        ("mata", "cahaya"), ("hidung", "bau"), ("lidah", "rasa"),
        ("telinga", "suara"), ("kulit", "sentuhan"),
    ]
    for indera, rangsang in senses:
        for obj in ["menangkap", "menerima", "mendeteksi", "merespons"]:
            questions.append(build_mcq(
                "Biologi",
                f"{indera.title()} berfungsi untuk {obj} ...",
                rangsang,
                ["warna", "mesin", "angka"],
                f"{indera.title()} membantu tubuh menerima {rangsang}.",
                "Hubungkan alat indera dengan rangsang yang sesuai.",
            ))

    plant_parts = [
        ("akar", "menyerap air"), ("daun", "tempat fotosintesis"),
        ("batang", "menopang tumbuhan"), ("bunga", "alat perkembangbiakan"),
        ("buah", "melindungi biji"), ("biji", "calon tumbuhan baru"),
    ]
    for bagian, fungsi in plant_parts:
        for lead in ["Fungsi", "Tugas utama", "Peran utama", "Kegunaan"]:
            questions.append(build_mcq(
                "Biologi",
                f"{lead} {bagian} pada tumbuhan adalah ...",
                fungsi,
                ["menjadi roda", "memotong kertas", "menghasilkan bensin"],
                f"{bagian.title()} berfungsi untuk {fungsi}.",
                "Ini tentang bagian-bagian tumbuhan.",
            ))

    health = [
        ("makan sayur", "baik untuk kesehatan"),
        ("olahraga teratur", "membantu tubuh tetap bugar"),
        ("cukup tidur", "membantu tubuh beristirahat"),
        ("minum air putih", "mencegah dehidrasi"),
        ("cuci tangan", "mengurangi kuman"),
    ]
    for kebiasaan, hasil in health:
        for stem in ["Mengapa", "Apa manfaat", "Apa hasil", "Kebiasaan"]:
            questions.append(build_mcq(
                "Biologi",
                f"{stem} dari {kebiasaan}?",
                hasil,
                ["membuat lemah", "membuat kotor", "membuat bingung"],
                f"{kebiasaan.title()} {hasil}.",
                "Pikirkan kebiasaan hidup sehat.",
            ))

    # Tambahkan variasi hewan dan habitat
    habitat_pairs = [
        ("ikan", "air"), ("unta", "gurun"), ("beruang kutub", "daerah dingin"),
        ("katak", "dua alam"), ("burung", "udara"), ("harimau", "hutan"),
        ("paus", "laut"), ("ayam", "darat"), ("penguin", "daerah dingin"), ("monyet", "pepohonan"),
    ]
    for hewan, habitat in habitat_pairs:
        for stem in ["Habitat utama", "Tempat hidup", "Lingkungan hidup", "Hewan"]:
            questions.append(build_mcq(
                "Biologi",
                f"{stem} {hewan} adalah ...",
                habitat,
                ["angkasa", "mesin", "lemari"],
                f"{hewan.title()} umumnya hidup di {habitat}.",
                "Pikirkan tempat makhluk hidup itu biasa ditemukan.",
            ))

    seen = set()
    dedup = []
    for q in questions:
        if q["question"] in seen:
            continue
        seen.add(q["question"])
        dedup.append(q)

    # Tambah pertanyaan numerik sederhana sampai 500
    extras = []
    numbers = [
        ("Berapa jumlah kaki laba-laba?", "8", ["6", "4", "10"]),
        ("Berapa jumlah kaki ayam?", "2", ["4", "6", "8"]),
        ("Berapa jumlah sayap kupu-kupu?", "4", ["2", "6", "8"]),
    ]
    while len(dedup) + len(extras) < 500:
        template = numbers[(len(extras)) % len(numbers)]
        base_q = build_mcq("Biologi", template[0], template[1], template[2], f"Jawabannya adalah {template[1]}.", "Hitung anggota tubuh hewan tersebut.")
        base_q["question"] = f"{template[0]} (versi {len(extras)+1})"
        extras.append(base_q)
    return (dedup + extras)[:500]


def generate_geografi():
    questions = []
    countries = [
        ("Indonesia", "Jakarta"), ("Jepang", "Tokyo"), ("Thailand", "Bangkok"),
        ("Malaysia", "Kuala Lumpur"), ("Singapura", "Singapura"),
        ("Filipina", "Manila"), ("Korea Selatan", "Seoul"), ("Tiongkok", "Beijing"),
        ("India", "New Delhi"), ("Australia", "Canberra"), ("Prancis", "Paris"),
        ("Jerman", "Berlin"), ("Italia", "Roma"), ("Belanda", "Amsterdam"),
        ("Mesir", "Kairo"), ("Arab Saudi", "Riyadh"), ("Turki", "Ankara"),
        ("Amerika Serikat", "Washington, D.C."), ("Inggris", "London"), ("Brasil", "Brasilia"),
    ]
    for negara, ibu in countries:
        questions.append(build_mcq(
            "Geografi",
            f"Ibu kota {negara} adalah ...",
            ibu,
            [countries[(i+3) % len(countries)][1] for i, pair in enumerate(countries) if pair[0] == negara][:1] + ["Tokyo", "Bangkok", "Seoul"],
            f"Ibu kota {negara} adalah {ibu}.",
            "Ini materi ibu kota negara.",
        ))
        questions.append(build_mcq(
            "Geografi",
            f"Kota {ibu} merupakan ibu kota negara ...",
            negara,
            ["Thailand", "Indonesia", "Jepang"] if negara != "Thailand" else ["Indonesia", "Jepang", "Malaysia"],
            f"{ibu} adalah ibu kota {negara}.",
            "Balikkan pasangan negara dan ibu kotanya.",
        ))

    provinces = [
        ("Lampung", "Bandar Lampung"), ("Jawa Barat", "Bandung"), ("Jawa Tengah", "Semarang"),
        ("Jawa Timur", "Surabaya"), ("Bali", "Denpasar"), ("Sumatera Utara", "Medan"),
        ("Sumatera Barat", "Padang"), ("Riau", "Pekanbaru"), ("Kalimantan Timur", "Samarinda"),
        ("Sulawesi Selatan", "Makassar"), ("Papua", "Jayapura"), ("Nusa Tenggara Barat", "Mataram"),
    ]
    for provinsi, ibu in provinces:
        questions.append(build_mcq(
            "Geografi",
            f"Ibu kota Provinsi {provinsi} adalah ...",
            ibu,
            ["Bandung", "Semarang", "Surabaya"],
            f"Ibu kota Provinsi {provinsi} adalah {ibu}.",
            "Fokus pada ibu kota provinsi Indonesia.",
        ))

    simple_facts = [
        ("Benua terbesar di dunia", "Asia", ["Afrika", "Eropa", "Australia"]),
        ("Samudra terbesar di dunia", "Samudra Pasifik", ["Samudra Atlantik", "Samudra Hindia", "Samudra Arktik"]),
        ("Garis khayal pembagi bumi utara dan selatan", "Khatulistiwa", ["Garis lintang", "Garis bujur", "Tropic"]),
        ("Alat untuk menunjukkan arah", "Kompas", ["Termometer", "Barometer", "Mikroskop"]),
        ("Matahari terbit dari arah", "Timur", ["Barat", "Utara", "Selatan"]),
        ("Matahari terbenam di arah", "Barat", ["Timur", "Utara", "Selatan"]),
        ("Peta digunakan untuk menunjukkan", "letak suatu tempat", ["suara", "rasa makanan", "cara bernapas"]),
        ("Gunung tertinggi di dunia", "Everest", ["Merapi", "Fuji", "Rinjani"]),
        ("Negara kepulauan terbesar di dunia", "Indonesia", ["Thailand", "Nepal", "Swiss"]),
    ]
    for topik, benar, salah in simple_facts:
        for lead in ["", "", "Dalam geografi, "]:
            questions.append(build_mcq(
                "Geografi",
                f"{lead}{topik} adalah ...".strip(),
                benar,
                salah,
                f"{topik} adalah {benar}.",
                "Ingat fakta geografi umum.",
            ))

    islands = [
        ("Pulau Jawa", "Indonesia"), ("Pulau Sumatra", "Indonesia"), ("Pulau Kalimantan", "Indonesia"),
        ("Pulau Bali", "Indonesia"), ("Pulau Sulawesi", "Indonesia"), ("Pulau Papua", "Indonesia"),
        ("Pulau Madagaskar", "Afrika"), ("Pulau Greenland", "Amerika Utara"),
    ]
    for pulau, wilayah in islands:
        questions.append(build_mcq(
            "Geografi",
            f"{pulau} berada di wilayah ...",
            wilayah,
            ["Eropa", "Antartika", "Timur Tengah"],
            f"{pulau} berada di wilayah {wilayah}.",
            "Hubungkan pulau dengan wilayahnya.",
        ))

    directions = [("utara", "atas"), ("selatan", "bawah"), ("timur", "kanan"), ("barat", "kiri")]
    for arah, posisi in directions:
        for stem in ["Pada peta sederhana", "Dalam ilustrasi arah mata angin", "Arah"]:
            questions.append(build_mcq(
                "Geografi",
                f"{stem}, {arah} biasanya berada di bagian ...",
                posisi,
                ["pojok", "tengah", "belakang"],
                f"Pada peta umum, {arah} berada di bagian {posisi}.",
                "Pikirkan arah mata angin di peta.",
            ))

    # Isi hingga 500
    dedup, seen = [], set()
    for q in questions:
        if q["question"] in seen:
            continue
        seen.add(q["question"])
        dedup.append(q)
    extras = []
    while len(dedup) + len(extras) < 500:
        negara, ibu = countries[len(extras) % len(countries)]
        q = build_mcq(
            "Geografi",
            f"Soal santai geografi #{len(extras)+1}: ibu kota {negara} adalah ...",
            ibu,
            ["Tokyo", "Seoul", "Bangkok"],
            f"Ibu kota {negara} adalah {ibu}.",
            "Gunakan pengetahuan ibu kota negara.",
        )
        extras.append(q)
    return (dedup + extras)[:500]


def generate_bahasa_indonesia():
    questions = []
    sinonim = [
        ("indah", "cantik", ["rusak", "pelan", "kasar"]),
        ("cepat", "lekas", ["lama", "susah", "keras"]),
        ("rajin", "giat", ["malas", "marah", "dingin"]),
        ("cerdas", "pandai", ["bodoh", "haus", "lapar"]),
        ("senang", "gembira", ["sedih", "malam", "kosong"]),
        ("bersih", "rapi", ["kotor", "acak", "berisik"]),
    ]
    for kata, benar, salah in sinonim:
        for stem in ["Sinonim kata", "Kata yang mirip dengan", "Persamaan kata", "Arti dekat kata"]:
            questions.append(build_mcq(
                "Bahasa Indonesia",
                f"{stem} \"{kata}\" adalah ...",
                benar,
                salah,
                f"Sinonim {kata} adalah {benar}.",
                "Cari kata yang artinya paling mirip.",
            ))

    antonim = [
        ("panas", "dingin", ["cerah", "hangat", "besar"]),
        ("besar", "kecil", ["tinggi", "cepat", "keras"]),
        ("tinggi", "rendah", ["lama", "berat", "halus"]),
        ("siang", "malam", ["pagi", "terang", "senja"]),
        ("masuk", "keluar", ["naik", "diam", "cepat"]),
        ("dekat", "jauh", ["tengah", "rapi", "halus"]),
    ]
    for kata, benar, salah in antonim:
        for stem in ["Lawan kata", "Antonim", "Kebalikan dari kata", "Berlawanan dengan"]:
            questions.append(build_mcq(
                "Bahasa Indonesia",
                f"{stem} \"{kata}\" adalah ...",
                benar,
                salah,
                f"Antonim {kata} adalah {benar}.",
                "Cari kata yang paling berlawanan.",
            ))

    ejaan = [
        ("apotik", "apotek"), ("aktifitas", "aktivitas"), ("resiko", "risiko"),
        ("analisa", "analisis"), ("sekedar", "sekadar"), ("nafas", "napas"),
        ("ijin", "izin"), ("praktek", "praktik"),
    ]
    for salah, benar in ejaan:
        options = [benar, salah, benar + "h", salah + "h"]
        questions.append(build_mcq(
            "Bahasa Indonesia",
            f"Penulisan yang benar untuk kata \"{salah}\" adalah ...",
            benar,
            [opt for opt in options if opt != benar][:3],
            f"Bentuk baku yang benar adalah {benar}.",
            "Pilih ejaan baku bahasa Indonesia.",
        ))

    classes = [
        ("mangga", "buah"), ("kucing", "hewan"), ("meja", "benda"),
        ("wortel", "sayuran"), ("dokter", "pekerjaan"), ("sekolah", "tempat"),
        ("pensil", "alat tulis"), ("motor", "kendaraan"),
    ]
    for kata, kategori in classes:
        for stem in ["termasuk", "digolongkan sebagai", "masuk kelompok", "berjenis"]:
            questions.append(build_mcq(
                "Bahasa Indonesia",
                f"Kata \"{kata}\" {stem} ...",
                kategori,
                ["warna", "perasaan", "musik"],
                f"Kata {kata} termasuk kategori {kategori}.",
                "Tentukan kelompok kata yang paling tepat.",
            ))

    kalimat = [
        ("Siapa nama kamu?", "kalimat tanya", ["kalimat berita", "kalimat perintah", "kalimat seru"]),
        ("Tolong tutup pintu!", "kalimat perintah", ["kalimat tanya", "kalimat berita", "kalimat sambung"]),
        ("Wah, pemandangannya indah!", "kalimat seru", ["kalimat tanya", "kalimat berita", "kalimat pasif"]),
        ("Hari ini cuaca cerah.", "kalimat berita", ["kalimat tanya", "kalimat seru", "kalimat perintah"]),
    ]
    for teks, jenis, salah in kalimat:
        questions.append(build_mcq(
            "Bahasa Indonesia",
            f"Kalimat \"{teks}\" termasuk ...",
            jenis,
            salah,
            f'"{teks}" termasuk {jenis}.',
            "Lihat tanda baca dan maksud kalimat.",
        ))

    kata_baku = [
        ("telepon", ["tilpun", "telpon", "telefon"]),
        ("subjek", ["subyek", "subyik", "sobjek"]),
        ("objek", ["obyek", "obek", "objekk"]),
        ("karier", ["karir", "kariir", "karer"]),
        ("jadwal", ["jadual", "jadwall", "jadualh"]),
    ]
    for benar, salah in kata_baku:
        questions.append(build_mcq(
            "Bahasa Indonesia",
            f"Manakah bentuk baku yang benar?",
            benar,
            salah,
            f"Kata baku yang benar adalah {benar}.",
            "Pilih bentuk kata yang resmi digunakan.",
        ))

    dedup, seen = [], set()
    for q in questions:
        if q["question"] in seen:
            continue
        seen.add(q["question"])
        dedup.append(q)
    extras = []
    while len(dedup) + len(extras) < 500:
        kata, benar, salah = sinonim[len(extras) % len(sinonim)]
        q = build_mcq(
            "Bahasa Indonesia",
            f"Soal santai bahasa #{len(extras)+1}: sinonim kata \"{kata}\" adalah ...",
            benar,
            salah,
            f"Sinonim {kata} adalah {benar}.",
            "Cari kata yang maknanya mirip.",
        )
        extras.append(q)
    return (dedup + extras)[:500]


def generate_pengetahuan_umum():
    questions = []
    facts = [
        ("Warna bendera Indonesia", "merah dan putih", ["biru dan putih", "merah dan hijau", "kuning dan putih"]),
        ("Hewan yang menghasilkan susu", "sapi", ["ayam", "ikan", "elang"]),
        ("Alat untuk menulis", "pensil", ["piring", "bantal", "sepatu"]),
        ("Hari setelah Senin", "Selasa", ["Minggu", "Kamis", "Sabtu"]),
        ("Bulan setelah Januari", "Februari", ["Maret", "April", "Desember"]),
        ("Jumlah hari dalam satu minggu", "7", ["5", "6", "8"]),
        ("Jumlah bulan dalam satu tahun", "12", ["10", "11", "13"]),
        ("Planet tempat kita tinggal", "Bumi", ["Mars", "Venus", "Jupiter"]),
        ("Hewan yang dikenal sebagai raja hutan", "singa", ["kucing", "kambing", "kuda"]),
        ("Alat untuk melihat waktu", "jam", ["sendok", "garpu", "ember"]),
        ("Minuman yang paling dibutuhkan tubuh", "air putih", ["sirup", "saus", "cat"]),
        ("Makanan pokok banyak orang Indonesia", "nasi", ["es batu", "kue sabun", "kapur"]),
        ("Alat transportasi di rel", "kereta", ["kapal", "sepeda", "pesawat"]),
        ("Bagian rumah untuk memasak", "dapur", ["garasi", "teras", "loteng"]),
        ("Binatang yang suka mengeong", "kucing", ["sapi", "kambing", "ikan"]),
    ]
    for topik, benar, salah in facts:
        for stem in ["", "Tahukah kamu,", "Soal ringan:", "Dalam pengetahuan umum,"]:
            questions.append(build_mcq(
                "Pengetahuan Umum",
                f"{stem} {topik} adalah ...".strip(),
                benar,
                salah,
                f"{topik} adalah {benar}.",
                "Ini fakta umum sehari-hari.",
            ))

    colors = [
        ("langit cerah", "biru"), ("daun segar", "hijau"), ("pisang matang", "kuning"),
        ("arang", "hitam"), ("kapas", "putih"), ("jeruk", "oranye"),
        ("stroberi", "merah"), ("terong", "ungu"),
    ]
    for benda, warna in colors:
        questions.append(build_mcq(
            "Pengetahuan Umum",
            f"Warna yang paling umum untuk {benda} adalah ...",
            warna,
            ["merah", "biru", "hitam"] if warna != "merah" else ["hijau", "biru", "putih"],
            f"{benda.title()} umumnya berwarna {warna}.",
            "Bayangkan warna benda tersebut.",
        ))

    activities = [
        ("pagi hari", "sarapan"), ("malam hari", "tidur"), ("hujan turun", "membawa payung"),
        ("haus", "minum"), ("lapar", "makan"), ("sekolah dimulai", "belajar"),
    ]
    for situasi, jawaban in activities:
        questions.append(build_mcq(
            "Pengetahuan Umum",
            f"Aktivitas yang cocok saat {situasi} adalah ...",
            jawaban,
            ["bersepeda di kolam", "tidur di jalan", "menyimpan buku di freezer"],
            f"Saat {situasi}, aktivitas yang cocok adalah {jawaban}.",
            "Pikirkan kebiasaan sehari-hari yang wajar.",
        ))

    dedup, seen = [], set()
    for q in questions:
        if q["question"] in seen:
            continue
        seen.add(q["question"])
        dedup.append(q)
    extras = []
    while len(dedup) + len(extras) < 500:
        topik, benar, salah = facts[len(extras) % len(facts)]
        q = build_mcq(
            "Pengetahuan Umum",
            f"Soal fun #{len(extras)+1}: {topik} adalah ...",
            benar,
            salah,
            f"{topik} adalah {benar}.",
            "Ini fakta umum yang ringan.",
        )
        extras.append(q)
    return (dedup + extras)[:500]




def build_subject_pack(category, facts, target=500):
    """Create a full pack from concise, easy facts with varied quiz phrasing."""
    forms = [
        "{question}",
        "Soal cepat: {question}",
        "Yuk tebak: {question}",
        "Pilih jawaban yang tepat: {question}",
        "Pertanyaan kilat: {question}",
        "Coba jawab: {question}",
        "Kuis santai: {question}",
        "Ayo jawab dengan cepat: {question}",
        "Uji ingatanmu: {question}",
        "Mana pilihan yang benar? {question}",
        "Tantangan ringan: {question}",
        "Siap menjawab? {question}",
        "Satu pertanyaan seru: {question}",
    ]
    result = []
    seen = set()
    # Interleave the phrasings so manual auto-play does not show 13
    # near-identical versions of one fact back-to-back.
    for form in forms:
        for question, correct, wrongs, explanation, hint in facts:
            if len(result) >= target:
                break
            prompt = form.format(question=question)
            if prompt in seen:
                continue
            seen.add(prompt)

            clean_options = []
            for option in [correct, *wrongs]:
                option = str(option)
                if option != str(correct) and option not in clean_options:
                    clean_options.append(option)
            fallback = [
                "Tidak ada pilihan yang benar", "Semua jawaban salah",
                "Tidak diketahui", "Pilihan lainnya",
            ]
            for option in fallback:
                if len(clean_options) >= 3:
                    break
                if option != str(correct) and option not in clean_options:
                    clean_options.append(option)

            result.append(build_mcq(
                category, prompt, str(correct), clean_options[:3],
                explanation, hint,
            ))
        if len(result) >= target:
            break

    if len(result) < target:
        raise ValueError(f"{category}: only generated {len(result)} unique questions; need {target}")

    random.shuffle(result)
    return result[:target]


def generate_bahasa_inggris():
    facts = [
        ("Apa arti kata 'apple'?", "apel", ["jeruk", "pisang", "anggur"], "Apple berarti apel.", "Ingat nama buah dalam bahasa Inggris."),
        ("Apa arti kata 'book'?", "buku", ["meja", "kursi", "tas"], "Book berarti buku.", "Benda yang biasa dibaca."),
        ("Apa arti kata 'cat'?", "kucing", ["anjing", "burung", "ikan"], "Cat berarti kucing.", "Hewan yang suka mengeong."),
        ("Apa arti kata 'dog'?", "anjing", ["kucing", "kelinci", "kuda"], "Dog berarti anjing.", "Hewan yang sering menggonggong."),
        ("Apa arti kata 'red'?", "merah", ["biru", "hijau", "kuning"], "Red berarti merah.", "Salah satu warna dasar."),
        ("Apa arti kata 'blue'?", "biru", ["merah", "hitam", "putih"], "Blue berarti biru.", "Warna langit cerah."),
        ("Apa arti kata 'water'?", "air", ["api", "tanah", "angin"], "Water berarti air.", "Minuman yang dibutuhkan tubuh."),
        ("Apa arti kata 'milk'?", "susu", ["kopi", "teh", "jus"], "Milk berarti susu.", "Minuman berwarna putih."),
        ("Apa arti kata 'school'?", "sekolah", ["rumah sakit", "pasar", "stasiun"], "School berarti sekolah.", "Tempat belajar."),
        ("Apa arti kata 'teacher'?", "guru", ["dokter", "petani", "pilot"], "Teacher berarti guru.", "Orang yang mengajar."),
        ("Apa arti kata 'family'?", "keluarga", ["teman", "tetangga", "kelas"], "Family berarti keluarga.", "Orang-orang terdekat di rumah."),
        ("Apa arti kata 'mother'?", "ibu", ["ayah", "kakak", "adik"], "Mother berarti ibu.", "Orang tua perempuan."),
        ("Apa arti kata 'father'?", "ayah", ["ibu", "nenek", "bibi"], "Father berarti ayah.", "Orang tua laki-laki."),
        ("Apa arti kata 'brother'?", "saudara laki-laki", ["saudara perempuan", "ibu", "anak perempuan"], "Brother berarti saudara laki-laki.", "Anggota keluarga laki-laki."),
        ("Apa arti kata 'sister'?", "saudara perempuan", ["saudara laki-laki", "ayah", "paman"], "Sister berarti saudara perempuan.", "Anggota keluarga perempuan."),
        ("Apa arti ungkapan 'thank you'?", "terima kasih", ["selamat pagi", "sampai jumpa", "maaf"], "Thank you berarti terima kasih.", "Ungkapan saat berterima kasih."),
        ("Apa arti ungkapan 'good morning'?", "selamat pagi", ["selamat malam", "selamat tidur", "selamat tinggal"], "Good morning berarti selamat pagi.", "Sapaan pada pagi hari."),
        ("Apa arti ungkapan 'good night'?", "selamat malam", ["selamat pagi", "selamat siang", "terima kasih"], "Good night berarti selamat malam.", "Biasanya diucapkan sebelum tidur."),
        ("Apa arti kata 'goodbye'?", "sampai jumpa", ["selamat datang", "tolong", "silakan"], "Goodbye berarti sampai jumpa.", "Ucapan saat berpisah."),
        ("Apa arti kata 'please'?", "tolong", ["maaf", "terima kasih", "selamat"], "Please berarti tolong atau silakan.", "Kata sopan saat meminta sesuatu."),
        ("Apa arti kata 'sorry'?", "maaf", ["terima kasih", "selamat pagi", "sampai jumpa"], "Sorry berarti maaf.", "Diucapkan saat meminta maaf."),
        ("Apa arti angka 'one'?", "satu", ["dua", "tiga", "empat"], "One berarti satu.", "Angka pertama."),
        ("Apa arti angka 'two'?", "dua", ["satu", "tiga", "lima"], "Two berarti dua.", "Satu ditambah satu."),
        ("Apa arti angka 'three'?", "tiga", ["dua", "empat", "enam"], "Three berarti tiga.", "Dua ditambah satu."),
        ("Apa arti kata 'Monday'?", "Senin", ["Selasa", "Rabu", "Minggu"], "Monday berarti Senin.", "Hari setelah Minggu."),
        ("Apa arti kata 'Sunday'?", "Minggu", ["Senin", "Jumat", "Sabtu"], "Sunday berarti Minggu.", "Hari libur yang umum."),
        ("Apa arti kata 'hot'?", "panas", ["dingin", "basah", "gelap"], "Hot berarti panas.", "Lawan kata cold."),
        ("Apa arti kata 'cold'?", "dingin", ["panas", "tinggi", "cepat"], "Cold berarti dingin.", "Lawan kata hot."),
        ("Apa arti kata 'happy'?", "senang", ["sedih", "marah", "takut"], "Happy berarti senang.", "Perasaan gembira."),
        ("Apa arti kata 'sad'?", "sedih", ["senang", "lucu", "lapar"], "Sad berarti sedih.", "Lawan kata happy."),
        ("Apa arti kata kerja 'run'?", "berlari", ["berjalan", "makan", "tidur"], "Run berarti berlari.", "Gerakan cepat menggunakan kaki."),
        ("Apa arti kata kerja 'eat'?", "makan", ["minum", "membaca", "menulis"], "Eat berarti makan.", "Aktivitas saat lapar."),
        ("Apa arti kata kerja 'drink'?", "minum", ["makan", "berlari", "tidur"], "Drink berarti minum.", "Aktivitas saat haus."),
        ("Apa arti kata kerja 'read'?", "membaca", ["menulis", "menggambar", "menyanyi"], "Read berarti membaca.", "Aktivitas dengan buku."),
        ("Apa arti kata kerja 'write'?", "menulis", ["membaca", "berlari", "berenang"], "Write berarti menulis.", "Aktivitas menggunakan pensil atau pena."),
        ("Apa arti kata 'friend'?", "teman", ["musuh", "guru", "orang asing"], "Friend berarti teman.", "Orang yang kita kenal dan sukai."),
        ("Apa arti kata 'house'?", "rumah", ["sekolah", "kantor", "toko"], "House berarti rumah.", "Tempat tinggal."),
        ("Apa arti kata 'car'?", "mobil", ["sepeda", "kereta", "kapal"], "Car berarti mobil.", "Kendaraan roda empat."),
        ("Apa arti kata 'bird'?", "burung", ["ikan", "kucing", "kupu-kupu"], "Bird berarti burung.", "Hewan yang memiliki sayap dan bulu."),
        ("Apa arti kata 'fish'?", "ikan", ["burung", "ayam", "kambing"], "Fish berarti ikan.", "Hewan yang hidup di air."),
    ]
    return build_subject_pack("Bahasa Inggris", facts)


def generate_sejarah():
    facts = [
        ("Kapan Indonesia memproklamasikan kemerdekaan?", "17 Agustus 1945", ["10 November 1945", "20 Mei 1908", "28 Oktober 1928"], "Indonesia merdeka pada 17 Agustus 1945.", "Ingat tanggal kemerdekaan Indonesia."),
        ("Siapa yang membacakan teks Proklamasi Indonesia?", "Soekarno", ["Mohammad Yamin", "Ki Hajar Dewantara", "Sutan Sjahrir"], "Soekarno membacakan teks Proklamasi.", "Beliau adalah presiden pertama Indonesia."),
        ("Siapa yang mendampingi Soekarno saat Proklamasi?", "Mohammad Hatta", ["Jenderal Sudirman", "Pattimura", "Diponegoro"], "Mohammad Hatta mendampingi Soekarno.", "Beliau adalah wakil presiden pertama."),
        ("Di kota mana Proklamasi Indonesia dibacakan?", "Jakarta", ["Bandung", "Surabaya", "Yogyakarta"], "Proklamasi dibacakan di Jakarta.", "Lokasinya di Jalan Pegangsaan Timur 56."),
        ("Siapa presiden pertama Republik Indonesia?", "Soekarno", ["Soeharto", "B.J. Habibie", "Abdurrahman Wahid"], "Soekarno adalah presiden pertama Indonesia.", "Nama beliau juga dikenal sebagai Bung Karno."),
        ("Siapa wakil presiden pertama Indonesia?", "Mohammad Hatta", ["Adam Malik", "Soeharto", "Megawati"], "Mohammad Hatta adalah wakil presiden pertama.", "Beliau dikenal sebagai Bung Hatta."),
        ("Apa nama peristiwa penculikan Soekarno-Hatta menjelang Proklamasi?", "Peristiwa Rengasdengklok", ["Bandung Lautan Api", "Pertempuran Ambarawa", "Peristiwa 10 November"], "Peristiwa Rengasdengklok terjadi menjelang Proklamasi.", "Peristiwa ini terjadi pada 16 Agustus 1945."),
        ("Apa kepanjangan BPUPKI?", "Badan Penyelidik Usaha-Usaha Persiapan Kemerdekaan Indonesia", ["Badan Persatuan Umum Pemuda Indonesia", "Badan Pembangunan Usaha Pemuda", "Badan Perdagangan Umum"], "BPUPKI mempersiapkan hal-hal terkait kemerdekaan Indonesia.", "Lembaga ini dibentuk pada masa pendudukan Jepang."),
        ("Apa kepanjangan PPKI?", "Panitia Persiapan Kemerdekaan Indonesia", ["Persatuan Pemuda Kemerdekaan Indonesia", "Panitia Perdagangan dan Industri", "Persatuan Pendidikan Indonesia"], "PPKI adalah Panitia Persiapan Kemerdekaan Indonesia.", "PPKI mengesahkan UUD 1945."),
        ("Kapan Hari Pahlawan diperingati di Indonesia?", "10 November", ["17 Agustus", "1 Juni", "21 April"], "Hari Pahlawan diperingati setiap 10 November.", "Tanggal ini terkait pertempuran di Surabaya."),
        ("Peristiwa apa yang diperingati pada Hari Pahlawan?", "Pertempuran Surabaya", ["Sumpah Pemuda", "Proklamasi", "Konferensi Asia Afrika"], "Hari Pahlawan mengenang perjuangan di Surabaya.", "Pertempuran besar terjadi pada November 1945."),
        ("Kapan Sumpah Pemuda diikrarkan?", "28 Oktober 1928", ["20 Mei 1908", "17 Agustus 1945", "10 November 1945"], "Sumpah Pemuda diikrarkan pada 28 Oktober 1928.", "Hari ini diperingati sebagai Hari Sumpah Pemuda."),
        ("Apa organisasi yang berdiri pada 20 Mei 1908?", "Budi Utomo", ["VOC", "PPKI", "PETA"], "Budi Utomo berdiri pada 20 Mei 1908.", "Tanggal itu diperingati sebagai Hari Kebangkitan Nasional."),
        ("Siapa tokoh emansipasi perempuan Indonesia yang diperingati setiap 21 April?", "R.A. Kartini", ["Cut Nyak Dien", "Dewi Sartika", "Martha Christina Tiahahu"], "R.A. Kartini dikenal memperjuangkan pendidikan perempuan.", "Hari Kartini diperingati pada tanggal kelahirannya."),
        ("Siapa pahlawan yang memimpin Perang Diponegoro?", "Pangeran Diponegoro", ["Pattimura", "Tuanku Imam Bonjol", "Sisingamangaraja XII"], "Pangeran Diponegoro memimpin Perang Jawa.", "Perang ini berlangsung pada 1825–1830."),
        ("Siapa mahapatih terkenal dari Kerajaan Majapahit?", "Gajah Mada", ["Hayam Wuruk", "Ken Arok", "Airlangga"], "Gajah Mada adalah mahapatih Majapahit.", "Ia terkenal dengan Sumpah Palapa."),
        ("Kerajaan Majapahit mencapai masa kejayaan pada masa raja siapa?", "Hayam Wuruk", ["Kertanegara", "Purnawarman", "Mulawarman"], "Majapahit berjaya pada masa Hayam Wuruk.", "Ia memerintah bersama Mahapatih Gajah Mada."),
        ("Apa nama sumpah terkenal yang diucapkan Gajah Mada?", "Sumpah Palapa", ["Sumpah Pemuda", "Sumpah Setia", "Sumpah Merdeka"], "Gajah Mada mengucapkan Sumpah Palapa.", "Sumpah ini berkaitan persatuan Nusantara."),
        ("Candi Borobudur merupakan peninggalan agama apa?", "Buddha", ["Hindu", "Islam", "Kristen"], "Borobudur merupakan candi Buddha.", "Candi ini berada di Magelang."),
        ("Candi Prambanan merupakan peninggalan agama apa?", "Hindu", ["Buddha", "Islam", "Konghucu"], "Prambanan merupakan kompleks candi Hindu.", "Candi ini terkenal dengan kisah Roro Jonggrang."),
        ("VOC merupakan kongsi dagang milik negara mana?", "Belanda", ["Portugis", "Inggris", "Spanyol"], "VOC berasal dari Belanda.", "VOC aktif berdagang di Nusantara."),
        ("Siapa tokoh pendidikan yang mendirikan Taman Siswa?", "Ki Hajar Dewantara", ["Soekarno", "Mohammad Hatta", "Jenderal Sudirman"], "Ki Hajar Dewantara dikenal sebagai Bapak Pendidikan Nasional.", "Semboyannya antara lain Tut Wuri Handayani."),
        ("Apa semboyan pendidikan yang terkenal dari Ki Hajar Dewantara?", "Tut Wuri Handayani", ["Bhinneka Tunggal Ika", "Merdeka atau Mati", "Sekali Merdeka"], "Tut Wuri Handayani adalah bagian dari semboyan pendidikan.", "Semboyan ini masih dikenal di sekolah."),
        ("Siapa pencipta lagu Indonesia Raya?", "W.R. Supratman", ["Ismail Marzuki", "Ibu Sud", "C. Simanjuntak"], "Indonesia Raya diciptakan oleh W.R. Supratman.", "Lagu ini pertama kali diperdengarkan pada Kongres Pemuda II."),
        ("Apa warna bendera Indonesia?", "Merah putih", ["Merah biru", "Biru putih", "Kuning hijau"], "Bendera Indonesia berwarna merah dan putih.", "Bendera ini dikenal sebagai Sang Merah Putih."),
        ("Peristiwa Bandung Lautan Api terjadi di kota mana?", "Bandung", ["Surabaya", "Medan", "Semarang"], "Bandung Lautan Api terjadi di Bandung.", "Peristiwa ini terjadi pada Maret 1946."),
        ("Siapa tokoh yang dikenal sebagai Jenderal Sudirman?", "Panglima Besar TNI", ["Presiden pertama", "Pencipta lagu Indonesia Raya", "Mahapatih Majapahit"], "Jenderal Sudirman adalah Panglima Besar TNI.", "Ia memimpin perang gerilya."),
        ("Kapan Hari Kebangkitan Nasional diperingati?", "20 Mei", ["21 April", "1 Juni", "28 Oktober"], "Hari Kebangkitan Nasional diperingati setiap 20 Mei.", "Tanggal ini terkait berdirinya Budi Utomo."),
        ("Apa nama naskah yang dibacakan saat kemerdekaan Indonesia?", "Teks Proklamasi", ["Sumpah Palapa", "Piagam Jakarta", "Sumpah Pemuda"], "Teks Proklamasi dibacakan pada 17 Agustus 1945.", "Naskah ini menyatakan kemerdekaan Indonesia."),
        ("Di kota mana Konferensi Asia Afrika tahun 1955 diselenggarakan?", "Bandung", ["Jakarta", "Yogyakarta", "Surabaya"], "Konferensi Asia Afrika diselenggarakan di Bandung.", "Gedung Merdeka menjadi tempat penting acara ini."),
        ("Tembok Besar merupakan bangunan bersejarah dari negara mana?", "Tiongkok", ["Jepang", "India", "Mesir"], "Tembok Besar berada di Tiongkok.", "Bangunan ini terkenal sangat panjang."),
        ("Piramida Giza berada di negara mana?", "Mesir", ["Yunani", "Italia", "Turki"], "Piramida Giza berada di Mesir.", "Bangunan ini berkaitan dengan peradaban Mesir Kuno."),
        ("Colosseum merupakan bangunan bersejarah di kota mana?", "Roma", ["Paris", "London", "Athena"], "Colosseum berada di Roma, Italia.", "Bangunan ini digunakan untuk pertunjukan pada masa Romawi."),
        ("Peradaban Mesir Kuno berkembang di sepanjang sungai apa?", "Sungai Nil", ["Sungai Amazon", "Sungai Gangga", "Sungai Thames"], "Peradaban Mesir Kuno berkembang di Sungai Nil.", "Sungai ini sangat penting bagi pertanian Mesir."),
        ("Perang Dunia II berakhir pada tahun berapa?", "1945", ["1918", "1939", "1955"], "Perang Dunia II berakhir pada 1945.", "Tahun yang sama dengan kemerdekaan Indonesia."),
        ("Siapa tokoh yang dikenal sebagai Bapak Proklamator Indonesia bersama Soekarno?", "Mohammad Hatta", ["Sutan Sjahrir", "Jenderal Sudirman", "Tan Malaka"], "Mohammad Hatta bersama Soekarno dikenal sebagai Proklamator.", "Beliau juga wakil presiden pertama."),
        ("Siapa pahlawan perempuan dari Aceh yang terkenal melawan Belanda?", "Cut Nyak Dien", ["R.A. Kartini", "Dewi Sartika", "Nyi Ageng Serang"], "Cut Nyak Dien merupakan pahlawan dari Aceh.", "Ia memimpin perlawanan terhadap kolonial Belanda."),
        ("Siapa pahlawan dari Maluku yang dikenal dengan nama Pattimura?", "Thomas Matulessy", ["Pangeran Diponegoro", "Tuanku Imam Bonjol", "Sisingamangaraja"], "Pattimura memiliki nama Thomas Matulessy.", "Ia memimpin perlawanan di Maluku."),
        ("Apa nama semboyan negara Indonesia?", "Bhinneka Tunggal Ika", ["Tut Wuri Handayani", "Ing Ngarsa Sung Tuladha", "Sumpah Palapa"], "Bhinneka Tunggal Ika berarti berbeda-beda tetapi tetap satu.", "Semboyan ini tertulis pada Garuda Pancasila."),
        ("Siapa presiden Indonesia yang dikenal sebagai Bapak Pembangunan?", "Soeharto", ["Soekarno", "B.J. Habibie", "Joko Widodo"], "Soeharto adalah presiden kedua Indonesia.", "Ia memimpin Indonesia selama beberapa dekade."),
    ]
    return build_subject_pack("Sejarah", facts)


def generate_ipa():
    facts = [
        ("Proses tumbuhan membuat makanan dengan bantuan cahaya disebut apa?", "Fotosintesis", ["Respirasi", "Evaporasi", "Fermentasi"], "Fotosintesis menggunakan cahaya untuk membuat makanan.", "Kata ini sering dipelajari pada materi tumbuhan."),
        ("Bagian tumbuhan yang menyerap air dari tanah adalah ...", "Akar", ["Daun", "Bunga", "Buah"], "Akar menyerap air dan mineral dari tanah.", "Bagian ini biasanya berada di dalam tanah."),
        ("Bagian tumbuhan yang umumnya menjadi tempat fotosintesis adalah ...", "Daun", ["Akar", "Biji", "Kulit batang"], "Daun menjadi tempat utama fotosintesis.", "Bagian ini biasanya berwarna hijau."),
        ("Gas yang dibutuhkan manusia untuk bernapas adalah ...", "Oksigen", ["Karbon dioksida", "Helium", "Nitrogen murni"], "Manusia membutuhkan oksigen untuk respirasi.", "Gas ini ada di udara."),
        ("Organ tubuh yang memompa darah adalah ...", "Jantung", ["Paru-paru", "Lambung", "Ginjal"], "Jantung memompa darah ke seluruh tubuh.", "Organ ini berdetak."),
        ("Organ utama untuk bernapas pada manusia adalah ...", "Paru-paru", ["Hati", "Lambung", "Usus"], "Paru-paru membantu pertukaran gas.", "Organ ini ada di rongga dada."),
        ("Tulang berfungsi terutama untuk ...", "Menopang tubuh", ["Mencerna makanan", "Memompa darah", "Mencium bau"], "Tulang menopang dan melindungi tubuh.", "Rangka membuat tubuh berdiri."),
        ("Indra untuk melihat adalah ...", "Mata", ["Telinga", "Hidung", "Lidah"], "Mata digunakan untuk melihat.", "Indra ini menangkap cahaya."),
        ("Indra untuk mendengar adalah ...", "Telinga", ["Mata", "Kulit", "Hidung"], "Telinga digunakan untuk mendengar.", "Indra ini menangkap suara."),
        ("Indra untuk mencium aroma adalah ...", "Hidung", ["Lidah", "Mata", "Telinga"], "Hidung membantu mencium bau.", "Indra ini juga menjadi jalur udara."),
        ("Hewan pemakan tumbuhan disebut ...", "Herbivora", ["Karnivora", "Omnivora", "Insektivora"], "Herbivora adalah pemakan tumbuhan.", "Contohnya sapi dan kambing."),
        ("Hewan pemakan daging disebut ...", "Karnivora", ["Herbivora", "Omnivora", "Frugivora"], "Karnivora adalah pemakan daging.", "Contohnya harimau."),
        ("Hewan pemakan tumbuhan dan hewan disebut ...", "Omnivora", ["Herbivora", "Karnivora", "Autotrof"], "Omnivora memakan berbagai jenis makanan.", "Contohnya ayam dan beruang."),
        ("Ikan bernapas menggunakan ...", "Insang", ["Paru-paru", "Sayap", "Kulit kering"], "Ikan umumnya bernapas dengan insang.", "Organ ini mengambil oksigen dari air."),
        ("Katak dewasa dapat bernapas melalui paru-paru dan ...", "Kulit", ["Bulu", "Sisik", "Sirip"], "Katak dapat bernapas melalui kulit dan paru-paru.", "Kulitnya harus tetap lembap."),
        ("Perubahan air menjadi uap disebut ...", "Penguapan", ["Pembekuan", "Pencairan", "Pengembunan"], "Penguapan mengubah cairan menjadi gas.", "Contohnya air yang dipanaskan."),
        ("Perubahan uap air menjadi titik-titik air disebut ...", "Pengembunan", ["Penguapan", "Pembakaran", "Penyubliman"], "Pengembunan mengubah gas menjadi cairan.", "Contohnya embun di pagi hari."),
        ("Air yang membeku berubah menjadi ...", "Es", ["Uap", "Asap", "Pasir"], "Air membeku menjadi es.", "Perubahan ini terjadi pada suhu rendah."),
        ("Matahari merupakan ...", "Bintang", ["Planet", "Satelit", "Asteroid"], "Matahari adalah bintang yang memancarkan cahaya.", "Benda langit ini menjadi pusat tata surya."),
        ("Bumi merupakan planet keberapa dari Matahari?", "Ketiga", ["Pertama", "Kedua", "Kelima"], "Bumi adalah planet ketiga dari Matahari.", "Planet sebelum Bumi adalah Venus."),
        ("Satelit alami Bumi adalah ...", "Bulan", ["Matahari", "Mars", "Venus"], "Bulan merupakan satelit alami Bumi.", "Benda langit ini tampak berubah bentuk."),
        ("Planet yang dikenal sebagai planet merah adalah ...", "Mars", ["Venus", "Jupiter", "Saturnus"], "Mars dikenal sebagai planet merah.", "Warnanya tampak kemerahan."),
        ("Planet terbesar dalam tata surya adalah ...", "Jupiter", ["Bumi", "Mars", "Merkurius"], "Jupiter merupakan planet terbesar.", "Planet ini memiliki Bintik Merah Besar."),
        ("Hewan yang mengalami metamorfosis dari ulat menjadi kupu-kupu adalah ...", "Kupu-kupu", ["Kucing", "Ayam", "Sapi"], "Kupu-kupu mengalami metamorfosis sempurna.", "Tahap awalnya berupa telur dan ulat."),
        ("Lebah membantu penyerbukan dengan memindahkan ...", "Serbuk sari", ["Akar", "Batu", "Air laut"], "Lebah membantu memindahkan serbuk sari.", "Proses ini membantu tumbuhan berkembang biak."),
        ("Tempat hidup alami makhluk hidup disebut ...", "Habitat", ["Populasi", "Komunitas", "Ekosistem buatan"], "Habitat adalah tempat hidup organisme.", "Contohnya hutan atau sungai."),
        ("Hubungan timbal balik makhluk hidup dengan lingkungannya disebut ...", "Ekosistem", ["Planet", "Cuaca", "Batuan"], "Ekosistem melibatkan makhluk hidup dan lingkungannya.", "Contohnya ekosistem hutan."),
        ("Sumber energi utama bagi kehidupan di Bumi adalah ...", "Matahari", ["Bulan", "Batu", "Awan"], "Matahari memberi cahaya dan panas.", "Energi ini membantu fotosintesis."),
        ("Benda yang dapat ditarik magnet contohnya ...", "Paku besi", ["Kertas", "Kayu", "Plastik"], "Besi dapat ditarik magnet.", "Bahan ini sering dipakai membuat paku."),
        ("Alat untuk mengukur suhu disebut ...", "Termometer", ["Barometer", "Kompas", "Penggaris"], "Termometer digunakan untuk mengukur suhu.", "Alat ini sering dipakai saat demam."),
        ("Air bersih yang aman diminum disebut ...", "Air layak minum", ["Air limbah", "Air asin", "Air berlumpur"], "Air minum harus bersih dan aman.", "Jangan minum air yang tercemar."),
        ("Sampah daun dan sisa makanan termasuk sampah ...", "Organik", ["Anorganik", "Logam", "Kaca"], "Sisa makhluk hidup termasuk sampah organik.", "Sampah ini dapat terurai."),
        ("Plastik termasuk sampah ...", "Anorganik", ["Organik", "Cair alami", "Kompos"], "Plastik termasuk sampah anorganik.", "Bahan ini sulit terurai secara alami."),
        ("Pelangi biasanya muncul setelah ...", "Hujan saat ada sinar matahari", ["Malam tanpa bulan", "Gempa bumi", "Salju di gurun"], "Pelangi terbentuk saat cahaya matahari dibiaskan oleh tetes air.", "Perhatikan langit setelah hujan."),
        ("Awan tersusun dari kumpulan ...", "Tetes air atau kristal es", ["Pasir", "Asap kendaraan saja", "Daun"], "Awan tersusun dari tetes air kecil atau kristal es.", "Awan berada di atmosfer."),
        ("Bagian tumbuhan yang biasanya menghasilkan biji setelah pembuahan adalah ...", "Buah", ["Akar", "Batang", "Duri"], "Buah berkembang dari bakal buah dan melindungi biji.", "Bagian ini sering kita makan."),
        ("Hewan yang aktif pada malam hari disebut ...", "Nokturnal", ["Diurnal", "Herbivora", "Akuatik"], "Nokturnal berarti aktif pada malam hari.", "Contohnya burung hantu."),
        ("Tempat hidup ikan umumnya adalah ...", "Air", ["Gurun", "Puncak gunung", "Padang pasir"], "Ikan hidup di lingkungan perairan.", "Ikan berenang menggunakan sirip."),
        ("Sumber daya alam yang dapat diperbarui contohnya ...", "Tumbuhan", ["Batu bara", "Minyak bumi", "Gas alam"], "Tumbuhan dapat ditanam dan tumbuh kembali.", "Sumber daya ini bisa dipulihkan."),
        ("Bagian telinga yang membantu menangkap gelombang suara dari luar adalah ...", "Daun telinga", ["Gendang lambung", "Lidah", "Retina"], "Daun telinga membantu menangkap suara.", "Bagian ini tampak di sisi kepala."),
    ]
    return build_subject_pack("IPA", facts)


def generate_ips():
    facts = [
        ("Ilmu yang mempelajari kehidupan masyarakat dan hubungan sosial adalah ...", "Ilmu sosial", ["Ilmu hitung", "Ilmu kimia", "Ilmu astronomi"], "Ilmu sosial mempelajari kehidupan masyarakat.", "Kata kuncinya adalah masyarakat."),
        ("Tempat bertemunya penjual dan pembeli disebut ...", "Pasar", ["Perpustakaan", "Rumah sakit", "Terminal"], "Pasar menjadi tempat kegiatan jual beli.", "Di sini orang membeli kebutuhan."),
        ("Orang yang menghasilkan barang atau jasa disebut ...", "Produsen", ["Konsumen", "Pembeli", "Penonton"], "Produsen menghasilkan barang atau jasa.", "Contohnya petani dan pengrajin."),
        ("Orang yang menggunakan barang atau jasa disebut ...", "Konsumen", ["Produsen", "Distributor", "Pemasok"], "Konsumen menggunakan barang atau jasa.", "Kita termasuk kelompok ini saat berbelanja."),
        ("Kegiatan menyalurkan barang dari produsen ke konsumen disebut ...", "Distribusi", ["Produksi", "Konsumsi", "Rekreasi"], "Distribusi menyalurkan barang.", "Contohnya pengiriman barang ke toko."),
        ("Kegiatan menghasilkan barang disebut ...", "Produksi", ["Konsumsi", "Distribusi", "Komunikasi"], "Produksi adalah kegiatan menghasilkan barang atau jasa.", "Contohnya membuat roti."),
        ("Kegiatan memakai barang atau jasa disebut ...", "Konsumsi", ["Produksi", "Distribusi", "Investasi"], "Konsumsi berarti menggunakan barang atau jasa.", "Contohnya makan nasi."),
        ("Alat yang biasa digunakan untuk menunjukkan arah adalah ...", "Kompas", ["Termometer", "Mikroskop", "Kalkulator"], "Kompas menunjukkan arah mata angin.", "Jarumnya menunjuk arah utara."),
        ("Gambar permukaan bumi pada bidang datar disebut ...", "Peta", ["Novel", "Poster iklan", "Kalender"], "Peta menggambarkan suatu wilayah.", "Peta membantu kita mencari lokasi."),
        ("Arah mata angin tempat matahari terbit adalah ...", "Timur", ["Barat", "Utara", "Selatan"], "Matahari tampak terbit dari timur.", "Arah sebaliknya adalah barat."),
        ("Arah yang berlawanan dengan utara adalah ...", "Selatan", ["Timur", "Barat", "Tenggara"], "Selatan berlawanan dengan utara.", "Pada peta biasanya berada di bawah."),
        ("Lingkungan pemerintahan di bawah kecamatan disebut ...", "Desa atau kelurahan", ["Provinsi", "Negara", "Benua"], "Desa atau kelurahan berada di bawah kecamatan.", "Wilayah ini dekat dengan warga."),
        ("Pemimpin pemerintahan desa disebut ...", "Kepala desa", ["Gubernur", "Presiden", "Menteri"], "Kepala desa memimpin pemerintahan desa.", "Jabatannya berada di tingkat desa."),
        ("Pemimpin sebuah provinsi disebut ...", "Gubernur", ["Wali kota", "Camat", "Kepala desa"], "Gubernur memimpin provinsi.", "Contohnya gubernur Lampung."),
        ("Pemimpin pemerintahan kabupaten disebut ...", "Bupati", ["Gubernur", "Presiden", "Camat"], "Bupati memimpin kabupaten.", "Jabatan ini setingkat dengan wali kota."),
        ("Kegiatan bekerja bersama untuk kepentingan bersama disebut ...", "Gotong royong", ["Persaingan", "Pertengkaran", "Perpecahan"], "Gotong royong mencerminkan kerja sama.", "Contohnya membersihkan lingkungan."),
        ("Aturan yang menjadi pedoman perilaku dalam masyarakat disebut ...", "Norma", ["Cuaca", "Harga", "Peta"], "Norma mengatur perilaku dalam masyarakat.", "Contohnya sopan santun."),
        ("Sikap menghargai perbedaan disebut ...", "Toleransi", ["Egois", "Diskriminasi", "Permusuhan"], "Toleransi berarti menghargai perbedaan.", "Sikap ini penting dalam masyarakat beragam."),
        ("Semboyan persatuan Indonesia adalah ...", "Bhinneka Tunggal Ika", ["Tut Wuri Handayani", "Sumpah Palapa", "Merdeka Belajar"], "Bhinneka Tunggal Ika berarti berbeda-beda tetapi tetap satu.", "Semboyan ini ada pada lambang negara."),
        ("Kebutuhan pokok manusia contohnya ...", "Makanan", ["Perhiasan mewah", "Konsol game", "Mobil sport"], "Makanan termasuk kebutuhan pokok.", "Kebutuhan ini penting untuk hidup."),
        ("Contoh kebutuhan sekunder adalah ...", "Televisi", ["Air minum", "Makanan pokok", "Tempat tinggal"], "Televisi dapat menjadi kebutuhan sekunder.", "Bukan kebutuhan paling dasar."),
        ("Kegiatan ekonomi masyarakat pesisir yang umum adalah ...", "Nelayan", ["Penambang salju", "Peternak unta", "Penjaga gunung"], "Nelayan menangkap ikan di perairan.", "Pekerjaan ini dekat dengan laut."),
        ("Orang yang bekerja mengolah sawah disebut ...", "Petani", ["Pilot", "Dokter", "Masinis"], "Petani mengolah lahan pertanian.", "Pekerjaan ini menghasilkan bahan pangan."),
        ("Tempat untuk mendapatkan layanan kesehatan adalah ...", "Puskesmas", ["Stadion", "Pasar malam", "Museum"], "Puskesmas memberikan layanan kesehatan.", "Fasilitas ini ada di banyak kecamatan."),
        ("Tempat untuk meminjam dan membaca buku adalah ...", "Perpustakaan", ["Bengkel", "Pelabuhan", "Bandara"], "Perpustakaan menyediakan buku untuk dibaca atau dipinjam.", "Tempat ini mendukung kegiatan belajar."),
        ("Kegiatan mengirim barang ke negara lain disebut ...", "Ekspor", ["Impor", "Konsumsi", "Produksi"], "Ekspor adalah menjual atau mengirim barang ke luar negeri.", "Kebalikannya adalah impor."),
        ("Kegiatan membeli barang dari negara lain disebut ...", "Impor", ["Ekspor", "Distribusi lokal", "Produksi"], "Impor adalah memasukkan barang dari luar negeri.", "Kebalikannya adalah ekspor."),
        ("Sumber daya alam yang berasal dari hutan contohnya ...", "Kayu", ["Plastik", "Baja buatan", "Kaca"], "Kayu dapat berasal dari pohon di hutan.", "Gunakan sumber daya ini secara bijak."),
        ("Sumber daya alam yang berasal dari laut contohnya ...", "Ikan", ["Batu bata", "Kertas", "Semen"], "Laut menyediakan ikan dan hasil perairan lainnya.", "Banyak nelayan mencari hasil ini."),
        ("Kegiatan menabung sebaiknya dilakukan untuk ...", "Mempersiapkan kebutuhan masa depan", ["Menghabiskan uang", "Membuang uang", "Menghindari belajar"], "Menabung membantu menyiapkan kebutuhan mendatang.", "Sisihkan sebagian uang secara teratur."),
        ("Sikap membeli barang sesuai kebutuhan disebut ...", "Hidup hemat", ["Boros", "Konsumtif berlebihan", "Pamer"], "Hidup hemat berarti menggunakan uang secara bijak.", "Belanja sesuai kebutuhan."),
        ("Kerja sama antarnegara di kawasan Asia Tenggara dilakukan melalui organisasi ...", "ASEAN", ["OPEC", "NATO", "WHO"], "ASEAN adalah organisasi negara-negara Asia Tenggara.", "Indonesia termasuk pendirinya."),
        ("Jumlah negara pendiri ASEAN adalah ...", "Lima", ["Tiga", "Empat", "Sepuluh"], "ASEAN didirikan oleh lima negara.", "Indonesia termasuk salah satunya."),
        ("Indonesia terletak di kawasan ...", "Asia Tenggara", ["Eropa Barat", "Asia Tengah", "Amerika Selatan"], "Indonesia berada di Asia Tenggara.", "Negara tetangganya antara lain Malaysia."),
        ("Kegiatan perjalanan untuk bersenang-senang dan berkunjung disebut ...", "Pariwisata", ["Produksi", "Distribusi", "Pertambangan"], "Pariwisata berkaitan dengan perjalanan dan kunjungan.", "Contohnya berlibur ke pantai."),
        ("Tempat kapal berlabuh dan bongkar muat barang disebut ...", "Pelabuhan", ["Bandara", "Stasiun", "Terminal bus"], "Pelabuhan melayani kapal dan kegiatan bongkar muat.", "Tempat ini berada di tepi perairan."),
        ("Kendaraan umum yang berjalan di atas rel adalah ...", "Kereta api", ["Bus", "Kapal", "Pesawat"], "Kereta api berjalan di atas rel.", "Kendaraan ini sering digunakan antarkota."),
        ("Kegiatan menjual dan membeli barang disebut ...", "Perdagangan", ["Pertanian", "Pendidikan", "Kesehatan"], "Perdagangan adalah kegiatan jual beli.", "Kegiatan ini terjadi di pasar."),
        ("Pekerjaan yang memberikan layanan mengajar adalah ...", "Guru", ["Nelayan", "Petani", "Sopir"], "Guru memberikan layanan pendidikan.", "Pekerjaan ini dilakukan di sekolah."),
        ("Contoh fasilitas umum yang digunakan untuk olahraga adalah ...", "Lapangan", ["Gudang pribadi", "Dapur", "Kamar tidur"], "Lapangan dapat digunakan masyarakat untuk olahraga.", "Tempat ini sering dipakai bermain bola."),
    ]
    return build_subject_pack("IPS", facts)


def generate_fisika():
    facts = [
        ("Satuan SI untuk panjang adalah ...", "Meter", ["Kilogram", "Sekon", "Ampere"], "Meter adalah satuan SI untuk panjang.", "Penggaris biasanya memiliki skala ini."),
        ("Satuan SI untuk massa adalah ...", "Kilogram", ["Meter", "Liter", "Watt"], "Kilogram adalah satuan SI untuk massa.", "Massa sering ditimbang dengan satuan ini."),
        ("Satuan SI untuk waktu adalah ...", "Sekon", ["Meter", "Newton", "Joule"], "Sekon adalah satuan SI untuk waktu.", "Satu menit terdiri dari 60 satuan ini."),
        ("Satuan SI untuk kuat arus listrik adalah ...", "Ampere", ["Volt", "Ohm", "Watt"], "Ampere adalah satuan SI kuat arus.", "Simbol satuannya adalah A."),
        ("Satuan gaya dalam SI adalah ...", "Newton", ["Joule", "Watt", "Pascal"], "Gaya diukur dalam newton.", "Nama satuan ini diambil dari ilmuwan Newton."),
        ("Satuan energi dalam SI adalah ...", "Joule", ["Meter", "Ampere", "Kelvin"], "Energi diukur dalam joule.", "Satuan ini juga dipakai untuk usaha."),
        ("Satuan daya listrik adalah ...", "Watt", ["Volt", "Ohm", "Kilogram"], "Daya diukur dalam watt.", "Lampu sering memiliki label satuan ini."),
        ("Satuan tegangan listrik adalah ...", "Volt", ["Ampere", "Ohm", "Newton"], "Tegangan listrik diukur dalam volt.", "Baterai memiliki nilai tegangan."),
        ("Satuan hambatan listrik adalah ...", "Ohm", ["Watt", "Joule", "Meter"], "Hambatan listrik diukur dalam ohm.", "Simbolnya adalah huruf Yunani omega."),
        ("Alat untuk mengukur suhu adalah ...", "Termometer", ["Speedometer", "Amperemeter", "Barometer"], "Termometer mengukur suhu.", "Alat ini sering digunakan saat demam."),
        ("Alat untuk mengukur kuat arus listrik adalah ...", "Amperemeter", ["Voltmeter", "Termometer", "Penggaris"], "Amperemeter mengukur arus listrik.", "Namanya mirip satuan ampere."),
        ("Alat untuk mengukur tegangan listrik adalah ...", "Voltmeter", ["Amperemeter", "Neraca", "Stopwatch"], "Voltmeter mengukur tegangan.", "Namanya berasal dari satuan volt."),
        ("Gaya yang menarik benda ke arah Bumi disebut ...", "Gravitasi", ["Gesekan", "Magnet", "Pegas"], "Gravitasi menarik benda ke arah Bumi.", "Gaya ini membuat benda jatuh."),
        ("Gaya yang muncul saat dua permukaan saling bergesekan disebut ...", "Gaya gesek", ["Gaya magnet", "Gaya apung", "Gaya listrik"], "Gaya gesek terjadi saat permukaan bersentuhan.", "Gaya ini dapat memperlambat gerak."),
        ("Gaya dapat mengubah ...", "Gerak atau bentuk benda", ["Warna langit", "Jumlah hari", "Rasa makanan"], "Gaya dapat mengubah gerak dan bentuk benda.", "Dorongan dan tarikan adalah gaya."),
        ("Bunyi dapat merambat melalui ...", "Zat padat, cair, dan gas", ["Ruang hampa saja", "Cahaya saja", "Warna"], "Bunyi membutuhkan medium untuk merambat.", "Bunyi tidak merambat di ruang hampa."),
        ("Cahaya dapat merambat di ruang hampa, sedangkan bunyi ...", "Tidak dapat", ["Selalu lebih cepat", "Berubah menjadi air", "Tidak memiliki energi"], "Bunyi membutuhkan medium.", "Di luar angkasa suara tidak terdengar seperti di udara."),
        ("Benda yang dapat memantulkan cahaya dengan baik adalah ...", "Cermin", ["Kain tebal", "Kertas tisu", "Busa"], "Cermin memantulkan cahaya dengan baik.", "Kita dapat melihat bayangan di benda ini."),
        ("Perubahan arah cahaya saat melewati dua medium berbeda disebut ...", "Pembiasan", ["Penguapan", "Pembekuan", "Pengembunan"], "Pembiasan mengubah arah rambat cahaya.", "Sedotan di gelas air tampak bengkok."),
        ("Bayangan terbentuk ketika cahaya ...", "Terhalang benda", ["Menjadi suara", "Menguap", "Membeku"], "Bayangan terbentuk saat cahaya terhalang.", "Coba berdiri di bawah sinar matahari."),
        ("Bahan yang mudah menghantarkan listrik disebut ...", "Konduktor", ["Isolator", "Resistor saja", "Transparan"], "Konduktor menghantarkan listrik.", "Contohnya tembaga."),
        ("Bahan yang sulit menghantarkan listrik disebut ...", "Isolator", ["Konduktor", "Magnet", "Elektrolit saja"], "Isolator menghambat aliran listrik.", "Contohnya karet."),
        ("Logam yang sering digunakan sebagai kabel listrik adalah ...", "Tembaga", ["Kayu", "Kertas", "Karet"], "Tembaga merupakan penghantar listrik yang baik.", "Kabel rumah sering menggunakan logam ini."),
        ("Kutub magnet yang senama jika didekatkan akan ...", "Tolak-menolak", ["Tarik-menarik", "Melebur", "Menghilang"], "Kutub magnet senama saling menolak.", "Utara dengan utara akan saling menjauh."),
        ("Kutub magnet yang berbeda jika didekatkan akan ...", "Tarik-menarik", ["Tolak-menolak", "Menguap", "Membeku"], "Kutub magnet berbeda saling menarik.", "Utara dengan selatan saling mendekat."),
        ("Perpindahan panas tanpa zat perantara disebut ...", "Radiasi", ["Konduksi", "Konveksi", "Evaporasi"], "Radiasi memindahkan panas melalui gelombang.", "Panas Matahari sampai ke Bumi dengan cara ini."),
        ("Perpindahan panas melalui sentuhan langsung disebut ...", "Konduksi", ["Radiasi", "Konveksi", "Refleksi"], "Konduksi terjadi melalui kontak langsung.", "Sendok logam menjadi panas saat dicelupkan ke air panas."),
        ("Perpindahan panas yang disertai aliran zat disebut ...", "Konveksi", ["Konduksi", "Radiasi", "Refraksi"], "Konveksi terjadi bersama aliran fluida.", "Contohnya gerakan air saat dipanaskan."),
        ("Benda yang bergerak lebih cepat menempuh jarak yang sama dalam waktu ...", "Lebih singkat", ["Lebih lama", "Selalu sama", "Tidak terukur"], "Kecepatan lebih tinggi berarti waktu tempuh lebih singkat untuk jarak sama.", "Bandingkan dua pelari."),
        ("Rumus sederhana kecepatan adalah ...", "Jarak dibagi waktu", ["Waktu dibagi massa", "Massa kali suhu", "Gaya dibagi warna"], "Kecepatan = jarak / waktu.", "Gunakan jarak yang ditempuh dan lama perjalanan."),
        ("Alat untuk mengukur waktu adalah ...", "Stopwatch", ["Termometer", "Neraca", "Kompas"], "Stopwatch mengukur selang waktu.", "Alat ini digunakan dalam lomba lari."),
        ("Energi yang dimiliki benda karena gerak disebut ...", "Energi kinetik", ["Energi potensial", "Energi kimia", "Energi bunyi"], "Energi kinetik adalah energi gerak.", "Kata kuncinya adalah bergerak."),
        ("Energi yang tersimpan karena posisi disebut ...", "Energi potensial", ["Energi kinetik", "Energi cahaya", "Energi bunyi"], "Energi potensial berkaitan dengan posisi.", "Contohnya air di bendungan yang tinggi."),
        ("Baterai menyimpan energi dalam bentuk ...", "Energi kimia", ["Energi bunyi", "Energi angin", "Energi cahaya"], "Baterai menyimpan energi kimia.", "Energi ini diubah menjadi listrik saat digunakan."),
        ("Kipas angin mengubah energi listrik menjadi energi ...", "Gerak", ["Makanan", "Kimia saja", "Nuklir"], "Kipas mengubah listrik menjadi gerak putaran.", "Baling-balingnya berputar."),
        ("Lampu mengubah energi listrik menjadi energi ...", "Cahaya", ["Bunyi saja", "Gerak saja", "Massa"], "Lampu menghasilkan cahaya dari energi listrik.", "Kita menyalakannya saat gelap."),
        ("Benda yang dapat ditembus cahaya dengan jelas disebut ...", "Bening atau transparan", ["Gelap", "Kasar", "Magnetis"], "Benda transparan meneruskan cahaya.", "Contohnya kaca jendela bening."),
        ("Benda yang tidak dapat ditembus cahaya disebut ...", "Opaque atau tidak tembus cahaya", ["Transparan", "Cair", "Elastis"], "Benda opak menghalangi cahaya.", "Contohnya papan kayu."),
        ("Alat untuk melihat benda sangat kecil adalah ...", "Mikroskop", ["Teleskop", "Periskop", "Kompas"], "Mikroskop memperbesar benda kecil.", "Alat ini digunakan di laboratorium."),
        ("Alat untuk melihat benda langit yang jauh adalah ...", "Teleskop", ["Mikroskop", "Termometer", "Barometer"], "Teleskop membantu mengamati benda langit.", "Alat ini digunakan oleh astronom."),
        ("Pada tekanan normal, air mulai membeku pada suhu ...", "0°C", ["10°C", "50°C", "100°C"], "Air membeku pada 0°C pada tekanan normal.", "Titik beku air adalah nol derajat Celsius."),
    ]
    return build_subject_pack("Fisika", facts)


def generate_kimia():
    facts = [
        ("Rumus kimia air adalah ...", "H2O", ["CO2", "O2", "NaCl"], "Air memiliki rumus kimia H2O.", "Satu molekul air terdiri dari hidrogen dan oksigen."),
        ("Lambang kimia oksigen adalah ...", "O", ["H", "C", "N"], "Lambang oksigen adalah O.", "Gas ini dibutuhkan manusia untuk bernapas."),
        ("Lambang kimia hidrogen adalah ...", "H", ["O", "He", "Na"], "Lambang hidrogen adalah H.", "Unsur ini paling ringan."),
        ("Lambang kimia karbon adalah ...", "C", ["Ca", "Cl", "K"], "Lambang karbon adalah C.", "Unsur ini ada dalam makhluk hidup."),
        ("Lambang kimia natrium adalah ...", "Na", ["N", "Ne", "Ni"], "Lambang natrium adalah Na.", "Unsur ini terdapat dalam garam dapur."),
        ("Lambang kimia besi adalah ...", "Fe", ["Be", "B", "Br"], "Lambang besi adalah Fe.", "Banyak digunakan untuk membuat benda logam."),
        ("Lambang kimia emas adalah ...", "Au", ["Ag", "Al", "Ar"], "Lambang emas adalah Au.", "Logam mulia ini sering dibuat perhiasan."),
        ("Lambang kimia perak adalah ...", "Ag", ["Au", "Ar", "As"], "Lambang perak adalah Ag.", "Logam ini berwarna putih mengilap."),
        ("Rumus kimia karbon dioksida adalah ...", "CO2", ["H2O", "O2", "NaCl"], "Karbon dioksida memiliki rumus CO2.", "Gas ini dihasilkan saat kita mengembuskan napas."),
        ("Rumus kimia garam dapur adalah ...", "NaCl", ["H2O", "CO2", "O2"], "Garam dapur adalah natrium klorida, NaCl.", "Bahan ini memberi rasa asin."),
        ("Zat dengan pH kurang dari 7 umumnya bersifat ...", "Asam", ["Basa", "Netral", "Logam"], "Larutan asam memiliki pH di bawah 7.", "Contohnya air lemon."),
        ("Zat dengan pH lebih dari 7 umumnya bersifat ...", "Basa", ["Asam", "Netral", "Gas"], "Larutan basa memiliki pH di atas 7.", "Contohnya larutan sabun."),
        ("Larutan netral memiliki pH sekitar ...", "7", ["1", "3", "14"], "pH netral adalah sekitar 7.", "Air murni pada kondisi standar memiliki pH sekitar ini."),
        ("Rasa asam pada lemon berasal dari kandungan ...", "Asam sitrat", ["Garam dapur", "Gula pasir", "Minyak"], "Lemon mengandung asam sitrat.", "Asam ini juga ada pada jeruk."),
        ("Cuka mengandung asam ...", "Asetat", ["Klorida", "Sulfur", "Nitrat"], "Cuka mengandung asam asetat.", "Bahan dapur ini memiliki rasa asam."),
        ("Wujud zat yang memiliki bentuk dan volume tetap adalah ...", "Padat", ["Cair", "Gas", "Plasma saja"], "Zat padat memiliki bentuk dan volume tetap.", "Contohnya batu."),
        ("Wujud zat yang memiliki volume tetap tetapi mengikuti bentuk wadah adalah ...", "Cair", ["Padat", "Gas", "Asap"], "Zat cair memiliki volume tetap dan bentuk mengikuti wadah.", "Contohnya air."),
        ("Wujud zat yang bentuk dan volumenya mengikuti ruang adalah ...", "Gas", ["Padat", "Cair", "Kristal"], "Gas mengisi ruang yang tersedia.", "Contohnya udara."),
        ("Perubahan zat padat menjadi cair disebut ...", "Mencair", ["Membeku", "Menguap", "Mengembun"], "Mencair mengubah padat menjadi cair.", "Es berubah menjadi air."),
        ("Perubahan zat cair menjadi padat disebut ...", "Membeku", ["Mencair", "Menguap", "Menyublim"], "Membeku mengubah cair menjadi padat.", "Air menjadi es."),
        ("Perubahan zat cair menjadi gas disebut ...", "Menguap", ["Mengembun", "Membeku", "Mencair"], "Menguap mengubah cair menjadi gas.", "Air panas dapat menghasilkan uap."),
        ("Perubahan gas menjadi cair disebut ...", "Mengembun", ["Menguap", "Mencair", "Membeku"], "Mengembun mengubah gas menjadi cair.", "Titik air muncul di permukaan gelas dingin."),
        ("Perubahan padat langsung menjadi gas disebut ...", "Menyublim", ["Mencair", "Membeku", "Mengembun"], "Menyublim adalah perubahan padat langsung menjadi gas.", "Contohnya kapur barus."),
        ("Campuran yang komponennya tercampur merata disebut ...", "Homogen", ["Heterogen", "Unsur", "Senyawa tunggal"], "Campuran homogen tampak seragam.", "Contohnya larutan gula."),
        ("Campuran yang komponennya masih dapat dibedakan disebut ...", "Heterogen", ["Homogen", "Unsur", "Atom tunggal"], "Campuran heterogen tidak seragam.", "Contohnya air dan minyak."),
        ("Gula yang larut dalam air membentuk ...", "Larutan", ["Logam", "Gas murni", "Unsur"], "Gula dan air membentuk larutan.", "Campuran ini tampak merata."),
        ("Partikel terkecil dari suatu unsur yang masih memiliki sifat unsur disebut ...", "Atom", ["Sel", "Jaringan", "Organ"], "Atom adalah bagian dasar unsur.", "Semua materi tersusun dari partikel ini."),
        ("Gabungan dua atau lebih atom yang terikat disebut ...", "Molekul", ["Jaringan", "Planet", "Organ"], "Molekul tersusun dari atom-atom yang terikat.", "Contohnya molekul air."),
        ("Tabel yang menyusun unsur-unsur kimia disebut ...", "Tabel periodik", ["Tabel perkalian", "Peta dunia", "Diagram batang"], "Tabel periodik menyusun unsur kimia.", "Tabel ini ada di laboratorium kimia."),
        ("Unsur yang memiliki lambang He adalah ...", "Helium", ["Hidrogen", "Hafnium", "Holmium"], "He adalah lambang helium.", "Gas ini dapat mengisi balon."),
        ("Unsur yang memiliki lambang K adalah ...", "Kalium", ["Kalsium", "Karbon", "Kobalt"], "K adalah lambang kalium.", "Unsur ini juga dikenal sebagai potassium."),
        ("Unsur yang memiliki lambang Ca adalah ...", "Kalsium", ["Karbon", "Kadmium", "Klorin"], "Ca adalah lambang kalsium.", "Mineral ini penting untuk tulang."),
        ("Unsur yang memiliki lambang Cl adalah ...", "Klorin", ["Karbon", "Kalsium", "Kobalt"], "Cl adalah lambang klorin.", "Unsur ini digunakan untuk desinfeksi air."),
        ("Bahan yang mempercepat reaksi kimia tanpa habis bereaksi disebut ...", "Katalis", ["Pelarut", "Produk", "Endapan"], "Katalis mempercepat reaksi kimia.", "Katalis tidak habis dalam reaksi keseluruhan."),
        ("Zat yang melarutkan zat lain disebut ...", "Pelarut", ["Zat terlarut", "Endapan", "Katalis"], "Pelarut adalah zat yang melarutkan.", "Air sering menjadi pelarut."),
        ("Zat yang dilarutkan dalam pelarut disebut ...", "Zat terlarut", ["Pelarut", "Katalis", "Gas buang"], "Zat terlarut adalah zat yang dilarutkan.", "Gula dalam air merupakan contohnya."),
        ("Bahan utama pembuat kaca sehari-hari adalah ...", "Pasir silika", ["Garam", "Gula", "Tepung"], "Kaca umumnya dibuat dari pasir silika.", "Bahan ini kaya akan silikon dioksida."),
        ("Logam yang banyak digunakan untuk membuat kaleng minuman adalah ...", "Aluminium", ["Kayu", "Karet", "Kertas"], "Kaleng minuman sering dibuat dari aluminium.", "Logam ini ringan."),
        ("Proses besi bereaksi dengan oksigen dan air hingga berkarat disebut ...", "Korosi", ["Fotosintesis", "Distilasi", "Sublimasi"], "Karat merupakan hasil korosi besi.", "Proses ini sering terjadi pada benda logam."),
        ("Zat yang memiliki rasa manis dan sering digunakan dalam minuman adalah ...", "Gula", ["Garam", "Cuka", "Pasir"], "Gula memberi rasa manis.", "Zat ini mudah larut dalam air."),
    ]
    return build_subject_pack("Kimia", facts)


def generate_ekonomi():
    facts = [
        ("Kebutuhan yang harus dipenuhi agar manusia dapat bertahan hidup disebut ...", "Kebutuhan primer", ["Kebutuhan tersier", "Keinginan", "Hiburan"], "Kebutuhan primer meliputi makanan, pakaian, dan tempat tinggal.", "Ini kebutuhan paling dasar."),
        ("Contoh kebutuhan primer adalah ...", "Makanan", ["Perhiasan", "Konsol game", "Mobil mewah"], "Makanan adalah kebutuhan primer.", "Setiap orang membutuhkannya."),
        ("Barang yang dibeli karena keinginan, bukan kebutuhan pokok, contohnya ...", "Mainan baru", ["Air minum", "Makanan pokok", "Obat penting"], "Mainan baru dapat menjadi keinginan.", "Kita bisa hidup tanpa membelinya."),
        ("Alat tukar yang umum digunakan dalam kegiatan ekonomi adalah ...", "Uang", ["Daun", "Batu biasa", "Kertas kosong"], "Uang digunakan sebagai alat tukar.", "Kita menggunakannya saat berbelanja."),
        ("Pertukaran barang dengan barang tanpa uang disebut ...", "Barter", ["Kredit", "Investasi", "Tabungan"], "Barter adalah pertukaran barang atau jasa.", "Cara ini digunakan sebelum uang modern."),
        ("Orang atau badan yang menghasilkan barang dan jasa disebut ...", "Produsen", ["Konsumen", "Pembeli", "Pelanggan"], "Produsen menghasilkan barang atau jasa.", "Contohnya perusahaan roti."),
        ("Orang yang memakai barang atau jasa disebut ...", "Konsumen", ["Produsen", "Distributor", "Pemasok"], "Konsumen menggunakan barang dan jasa.", "Pembeli termasuk konsumen."),
        ("Tempat berlangsungnya transaksi jual beli disebut ...", "Pasar", ["Museum", "Sekolah", "Taman"], "Pasar mempertemukan penjual dan pembeli.", "Transaksi dapat berlangsung di tempat ini."),
        ("Uang yang diterima seseorang dari bekerja disebut ...", "Pendapatan", ["Pengeluaran", "Utang", "Denda"], "Pendapatan adalah uang yang diterima.", "Gaji merupakan salah satu contohnya."),
        ("Uang yang dikeluarkan untuk membeli barang disebut ...", "Pengeluaran", ["Pendapatan", "Keuntungan", "Tabungan"], "Pengeluaran adalah uang yang digunakan.", "Catat belanja bulanan sebagai ini."),
        ("Kegiatan menyisihkan uang untuk digunakan nanti disebut ...", "Menabung", ["Boros", "Berutang", "Membuang"], "Menabung membantu menyiapkan kebutuhan masa depan.", "Sisihkan uang secara teratur."),
        ("Lembaga yang umum menerima simpanan uang masyarakat adalah ...", "Bank", ["Pasar", "Museum", "Terminal"], "Bank menerima simpanan dan menyediakan layanan keuangan.", "Kita dapat membuka rekening di sini."),
        ("Keuntungan diperoleh ketika pendapatan lebih besar daripada ...", "Biaya", ["Tabungan", "Aset", "Modal sendiri"], "Laba adalah pendapatan dikurangi biaya.", "Bandingkan pemasukan dan pengeluaran usaha."),
        ("Kerugian terjadi ketika biaya lebih besar daripada ...", "Pendapatan", ["Keuntungan", "Tabungan", "Diskon"], "Kerugian terjadi saat biaya melebihi pendapatan.", "Usaha mengeluarkan uang lebih banyak daripada yang diterima."),
        ("Kegiatan membuat barang atau menyediakan jasa disebut ...", "Produksi", ["Konsumsi", "Distribusi", "Promosi"], "Produksi menghasilkan barang atau jasa.", "Contohnya membuat pakaian."),
        ("Kegiatan menyalurkan barang kepada pembeli disebut ...", "Distribusi", ["Produksi", "Konsumsi", "Tabungan"], "Distribusi menyalurkan barang.", "Contohnya pengiriman ke toko."),
        ("Kegiatan menggunakan barang atau jasa disebut ...", "Konsumsi", ["Produksi", "Distribusi", "Investasi"], "Konsumsi menggunakan barang dan jasa.", "Contohnya memakai sepatu."),
        ("Jumlah barang yang ingin dibeli konsumen pada berbagai harga disebut ...", "Permintaan", ["Penawaran", "Produksi", "Pajak"], "Permintaan berasal dari sisi pembeli.", "Konsumen menginginkan barang."),
        ("Jumlah barang yang ingin dijual produsen disebut ...", "Penawaran", ["Permintaan", "Konsumsi", "Utang"], "Penawaran berasal dari sisi penjual.", "Produsen menyediakan barang."),
        ("Jika barang langka sementara banyak orang ingin membelinya, harga cenderung ...", "Naik", ["Turun terus", "Menjadi nol", "Tidak pernah berubah"], "Permintaan tinggi dan barang terbatas dapat mendorong harga naik.", "Ingat saat barang sedang populer."),
        ("Potongan harga saat berbelanja disebut ...", "Diskon", ["Pajak", "Bunga", "Denda"], "Diskon adalah pengurangan harga.", "Biasanya ditulis dalam persen."),
        ("Uang yang dibayarkan masyarakat kepada negara sesuai aturan disebut ...", "Pajak", ["Hadiah", "Diskon", "Tip"], "Pajak digunakan untuk membiayai kebutuhan negara.", "Contohnya pajak kendaraan."),
        ("Rencana pemasukan dan pengeluaran disebut ...", "Anggaran", ["Promosi", "Produksi", "Distribusi"], "Anggaran membantu mengatur keuangan.", "Buat daftar sebelum berbelanja."),
        ("Modal awal untuk menjalankan usaha disebut ...", "Modal", ["Laba", "Diskon", "Pajak"], "Modal digunakan untuk memulai atau menjalankan usaha.", "Contohnya uang untuk membeli bahan baku."),
        ("Orang yang menjalankan dan mengembangkan usaha disebut ...", "Wirausahawan", ["Konsumen", "Penonton", "Pelanggan"], "Wirausahawan mengelola usaha dan mengambil peluang.", "Istilah lainnya entrepreneur."),
        ("Kegiatan menjual barang ke luar negeri disebut ...", "Ekspor", ["Impor", "Konsumsi", "Barter lokal"], "Ekspor menjual barang ke negara lain.", "Contohnya mengirim kopi ke luar negeri."),
        ("Kegiatan membeli barang dari luar negeri disebut ...", "Impor", ["Ekspor", "Produksi", "Tabungan"], "Impor membeli barang dari negara lain.", "Contohnya memasukkan mesin dari luar negeri."),
        ("Kenaikan harga barang dan jasa secara umum dan terus-menerus disebut ...", "Inflasi", ["Deflasi", "Diskon", "Subsidi"], "Inflasi adalah kenaikan harga secara umum.", "Daya beli uang bisa menurun."),
        ("Penurunan harga barang dan jasa secara umum disebut ...", "Deflasi", ["Inflasi", "Produksi", "Distribusi"], "Deflasi adalah penurunan tingkat harga umum.", "Kebalikan dari inflasi."),
        ("Koperasi dijalankan berdasarkan asas ...", "Kekeluargaan", ["Persaingan bebas saja", "Kekuasaan pribadi", "Monopoli"], "Koperasi berasaskan kekeluargaan.", "Anggota menjadi bagian penting koperasi."),
        ("Orang yang memiliki simpanan di bank disebut ...", "Nasabah", ["Produsen", "Distributor", "Petugas pasar"], "Nasabah menggunakan layanan bank.", "Istilah ini digunakan di dunia perbankan."),
        ("Bunga tabungan adalah ...", "Imbalan atas simpanan", ["Biaya membeli barang", "Harga pokok", "Pajak kendaraan"], "Bunga tabungan merupakan imbalan sesuai ketentuan bank.", "Nilainya biasanya dihitung dalam persen."),
        ("Kegiatan menggunakan uang secara bijak disebut ...", "Mengelola keuangan", ["Boros", "Pamer", "Belanja impulsif"], "Mengelola keuangan berarti merencanakan pemasukan dan pengeluaran.", "Buat anggaran sederhana."),
        ("Barang yang digunakan untuk menghasilkan barang lain disebut ...", "Barang modal", ["Barang konsumsi", "Barang gratis", "Barang pajangan"], "Barang modal membantu proses produksi.", "Contohnya mesin di pabrik."),
        ("Contoh jasa adalah ...", "Layanan potong rambut", ["Beras", "Sepatu", "Buku tulis"], "Jasa adalah layanan yang diberikan kepada orang lain.", "Kita membayar layanan ini di salon."),
        ("Harga yang dibayar pembeli untuk mendapatkan barang disebut ...", "Harga jual", ["Biaya tetap", "Modal awal", "Pajak penghasilan"], "Harga jual adalah harga yang ditawarkan kepada pembeli.", "Lihat label harga di toko."),
        ("Kegiatan mempromosikan produk bertujuan untuk ...", "Mengenalkan produk kepada calon pembeli", ["Menyembunyikan produk", "Mengurangi kualitas", "Menghentikan produksi"], "Promosi membantu calon konsumen mengenal produk.", "Contohnya iklan."),
        ("Kebutuhan manusia tidak terbatas, sedangkan sumber daya ...", "Terbatas", ["Selalu berlimpah", "Tidak diperlukan", "Tidak memiliki nilai"], "Kelangkaan muncul karena sumber daya terbatas.", "Inilah masalah dasar ekonomi."),
        ("Pilihan yang dikorbankan saat memilih sesuatu disebut ...", "Biaya peluang", ["Harga diskon", "Pajak", "Pendapatan"], "Biaya peluang adalah nilai alternatif terbaik yang dilepas.", "Setiap pilihan memiliki konsekuensi."),
        ("Orang yang membeli barang untuk dijual kembali disebut ...", "Pedagang", ["Konsumen akhir", "Penonton", "Pemakai"], "Pedagang membeli dan menjual barang.", "Contohnya pemilik toko."),
    ]
    return build_subject_pack("Ekonomi", facts)



def assign_ids(questions):
    final = []
    for index, item in enumerate(questions, start=1):
        final.append({
            "id": f"q{index:04d}",
            **item,
        })
    return final


def main():
    questions = []
    questions.extend(generate_matematika())
    questions.extend(generate_geografi())
    questions.extend(generate_biologi())
    questions.extend(generate_bahasa_indonesia())
    questions.extend(generate_pengetahuan_umum())
    questions.extend(generate_bahasa_inggris())
    questions.extend(generate_sejarah())
    questions.extend(generate_ipa())
    questions.extend(generate_ips())
    questions.extend(generate_fisika())
    questions.extend(generate_kimia())
    questions.extend(generate_ekonomi())

    questions = assign_ids(questions)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {len(questions)} questions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
