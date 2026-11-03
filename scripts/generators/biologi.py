from __future__ import annotations

from .common import build_mcq


def generate() -> list[dict]:
    questions: list[dict] = []
    seen: set[str] = set()

    def add_q(q_dict: dict) -> bool:
        if q_dict["question"] in seen:
            return False
        seen.add(q_dict["question"])
        questions.append(q_dict)
        return True

    # 1. Organ Tubuh Manusia & Fungsinya
    human_organs = [
        ("Organ tubuh manusia yang berfungsi utama memompa darah ke seluruh tubuh adalah ...", "Jantung", ["Paru-paru", "Ginjal", "Hati"]),
        ("Organ tubuh yang berfungsi sebagai tempat pertukaran oksigen dan karbon dioksida adalah ...", "Paru-paru", ["Jantung", "Lambung", "Ginjal"]),
        ("Organ tubuh yang berfungsi menyaring darah dan menghasilkan urine (air seni) adalah ...", "Ginjal", ["Hati", "Lambung", "Pankreas"]),
        ("Organ pencernaan yang memproduksi asam klorida (HCl) untuk mencerna makanan adalah ...", "Lambung", ["Mulut", "Usus besar", "Tenggorokan"]),
        ("Organ tubuh terbesar di dalam tubuh manusia yang berfungsi menetralkan racun adalah ...", "Hati", ["Ginjal", "Jantung", "Paru-paru"]),
        ("Tempat penyerapan sari-sari makanan utama dalam sistem pencernaan manusia terjadi di ...", "Usus halus", ["Lambung", "Usus besar", "Kerongkongan"]),
        ("Tempat penyerapan kembali air dan pembusukan sisa makanan oleh bakteri E. coli adalah ...", "Usus besar", ["Usus halus", "Lambung", "Anus"]),
        ("Pusat kendali seluruh aktivitas dan sistem koordinasi tubuh manusia berada pada ...", "Otak", ["Jantung", "Sumsum tulang", "Mata"]),
        ("Saluran penghubung antara rongga mulut dengan lambung disebut ...", "Kerongkongan (Esofagus)", ["Tenggorokan (Trakea)", "Bronkus", "Laring"]),
        ("Saluran pernapasan yang menghubungkan laring dengan bronkus pada paru-paru disebut ...", "Tenggorokan (Trakea)", ["Kerongkongan", "Esofagus", "Faring"]),
        ("Gerakan meremas dan mendorong makanan di sepanjang kerongkongan menuju lambung disebut ...", "Gerak peristaltik", ["Gerak refleks", "Gerak amuboid", "Gerak brown"]),
        ("Organ panca indra manusia yang peka terhadap rangsang cahaya adalah ...", "Mata", ["Telinga", "Hidung", "Kulit"]),
        ("Organ panca indra yang berfungsi menangkap rangsang gelombang bunyi/suara adalah ...", "Telinga", ["Mata", "Lidah", "Kulit"]),
        ("Organ panca indra manusia yang peka terhadap rangsang bau atau aroma adalah ...", "Hidung", ["Lidah", "Mata", "Telinga"]),
        ("Organ panca indra yang berfungsi mengecap rasa manis, asin, asam, dan pahit adalah ...", "Lidah", ["Hidung", "Bibir", "Gigi"]),
        ("Organ panca indra terluas pada tubuh manusia yang peka terhadap sentuhan dan suhu adalah ...", "Kulit", ["Mata", "Telinga", "Lidah"]),
        ("Bagian mata yang mengatur banyaknya cahaya yang masuk ke dalam bola mata adalah ...", "Pupil", ["Kornea", "Retina", "Lensa mata"]),
        ("Bagian mata yang memberi warna hitam, cokelat, atau biru pada bola mata adalah ...", "Iris", ["Pupil", "Sklera", "Retina"]),
        ("Lapisan mata yang paling peka menerima bayangan benda seperti film kamera adalah ...", "Retina (selaput jala)", ["Kornea", "Iris", "Lensa"]),
        ("Lapisan terluar mata yang bening dan berfungsi meneruskan cahaya ke lensa adalah ...", "Kornea", ["Retina", "Sklera", "Pupil"]),
        ("Bagian telinga luar yang berfungsi menangkap dan mengarahkan gelombang suara adalah ...", "Daun telinga", ["Gendang telinga", "Saluran eustachius", "Rumah siput"]),
        ("Selaput tipis di dalam telinga yang bergetar saat menerima gelombang bunyi disebut ...", "Gendang telinga", ["Daun telinga", "Koklea", "Tulang martil"]),
        ("Bagian telinga dalam yang menyerupai cangkang siput dan berisi cairan pendengaran disebut ...", "Koklea (Rumah siput)", ["Saluran eustachius", "Daun telinga", "Gendang telinga"]),
        ("Saluran yang menghubungkan rongga telinga tengah dengan rongga mulut/faring adalah ...", "Saluran Eustachius", ["Koklea", "Bronkus", "Kerongkongan"]),
        ("Tiga tulang pendengaran pada telinga tengah manusia adalah tulang martil, landasan, dan ...", "Tulang sanggurdi", ["Tulang kering", "Tulang selangka", "Tulang hasta"]),
        ("Bintil-bintil kecil pada permukaan lidah tempat berkumpulnya saraf pengecap rasa disebut ...", "Papila", ["Stomata", "Kelenjar ludah", "Enzim ptialin"]),
        ("Rasa manis umumnya paling peka dirasakan pada bagian lidah sebelah ...", "Ujung depan", ["Pangkal belakang", "Tepi kiri", "Tepi kanan"]),
        ("Rasa pahit umumnya paling kuat dideteksi pada permukaan lidah bagian ...", "Pangkal belakang", ["Ujung depan", "Tepi depan", "Samping"]),
        ("Lapisan kulit terluar yang mati dan dapat mengelupas disebut lapisan ...", "Epidermis (kulit ari)", ["Dermis (kulit jangat)", "Hipodermis", "Jaringan lemak"]),
        ("Pigmen alami di dalam kulit yang menentukan warna kulit seseorang adalah ...", "Melanin", ["Hemoglobin", "Klorofil", "Karoten"]),
        ("Organ tubuh yang memproduksi cairan empedu untuk mencerna lemak adalah ...", "Hati", ["Ginjal", "Pankreas", "Lambung"]),
        ("Organ berbentuk kantong kecil tempat menyimpan cairan empedu sebelum dialirkan ke usus adalah ...", "Kantong empedu", ["Lambung", "Limpa", "Pankreas"]),
        ("Kelenjar yang memproduksi hormon insulin untuk mengatur kadar gula darah adalah ...", "Pankreas", ["Tiroid", "Adrenal", "Hipofisis"]),
        ("Penyakit kekurangan hormon insulin yang menyebabkan tingginya kadar gula darah disebut ...", "Diabetes melitus (Kencing manis)", ["Hipertensi", "Anemia", "Hipotensi"]),
        ("Kantung udara kecil di paru-paru tempat terjadinya pertukaran gas O2 dan CO2 disebut ...", "Alveolus", ["Bronkiolus", "Trakea", "Pleura"]),
        ("Selaput pembungkus paru-paru yang melindunginya dari gesekan saat bernapas disebut ...", "Pleura", ["Perikardium", "Meninges", "Periosteum"]),
        ("Selaput pembungkus jantung manusia disebut ...", "Perikardium", ["Pleura", "Meninges", "Peritoneum"]),
        ("Otot berbentuk kubah yang membatasi rongga dada dan rongga perut saat bernapas disebut ...", "Diafragma", ["Otot bisep", "Otot trisep", "Otot jantung"]),
        ("Jumlah ruang pada jantung manusia dewasa adalah ...", "4 ruang", ["2 ruang", "3 ruang", "5 ruang"]),
        ("Empat ruang pada jantung manusia terdiri dari serambi kanan, serambi kiri, bilik kanan, dan ...", "Bilik kiri", ["Bilik atas", "Serambi atas", "Katup bawah"]),
        ("Ruang jantung yang berfungsi memompa darah bersih kaya oksigen ke seluruh tubuh adalah ...", "Bilik kiri (Ventrikel kiri)", ["Bilik kanan", "Serambi kiri", "Serambi kanan"]),
        ("Ruang jantung yang berfungsi menerima darah kotor kaya CO2 dari seluruh tubuh adalah ...", "Serambi kanan (Atrium kanan)", ["Serambi kiri", "Bilik kiri", "Bilik kanan"]),
        ("Pembuluh darah yang mengalirkan darah keluar meninggalkan jantung disebut pembuluh ...", "Arteri (Nadi)", ["Vena (Balik)", "Kapiler", "Limfa"]),
        ("Pembuluh darah yang mengalirkan darah kembali menuju ke jantung disebut pembuluh ...", "Vena (Balik)", ["Arteri (Nadi)", "Aorta", "Kapiler"]),
        ("Pembuluh nadi terbesar yang keluar langsung dari bilik kiri jantung disebut ...", "Aorta", ["Vena kava", "Arteri pulmonalis", "Kapiler"]),
    ]
    for q_text, corr, dists in human_organs:
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami fungsi sistem organ tubuh manusia."))

    # 2. Darah, Rangka Tulang & Gigi
    blood_and_bones = [
        ("Sel darah yang berfungsi utama mengangkut oksigen ke seluruh tubuh adalah ...", "Sel darah merah (Eritrosit)", ["Sel darah putih (Leukosit)", "Keping darah (Trombosit)", "Plasma darah"]),
        ("Zat warna merah pada sel darah merah yang mengikat gas oksigen disebut ...", "Hemoglobin", ["Melanin", "Klorofil", "Bilirubin"]),
        ("Sel darah yang berfungsi melawan kuman penyakit dan menjaga kekebalan tubuh adalah ...", "Sel darah putih (Leukosit)", ["Sel darah merah (Eritrosit)", "Keping darah (Trombosit)", "Serum darah"]),
        ("Komponen darah yang berperan sangat penting dalam proses pembekuan darah saat luka adalah ...", "Keping darah (Trombosit)", ["Sel darah merah", "Sel darah putih", "Hemoglobin"]),
        ("Bagian cair dari darah yang mengangkut sari-sari makanan dan hormon disebut ...", "Plasma darah", ["Eritrosit", "Leukosit", "Trombosit"]),
        ("Penyakit kekurangan sel darah merah atau hemoglobin dalam tubuh disebut ...", "Anemia", ["Leukemia", "Hipertensi", "Hemofilia"]),
        ("Penyakit kelainan darah sukar membeku bila terjadi luka disebut ...", "Hemofilia", ["Anemia", "Thalasemia", "Leukemia"]),
        ("Kanker darah akibat produksi sel darah putih berlebih yang tidak terkendali disebut ...", "Leukemia", ["Anemia", "Hemofilia", "Hipotensi"]),
        ("Golongan darah manusia dalam sistem ABO terbagi menjadi empat jenis, yaitu A, B, AB, dan ...", "O", ["C", "D", "E"]),
        ("Golongan darah yang disebut sebagai resipien universal karena dapat menerima transfusi darah dari semua golongan adalah ...", "Golongan darah AB", ["Golongan darah O", "Golongan darah A", "Golongan darah B"]),
        ("Golongan darah yang sering disebut pendonor universal karena bisa diberikan ke semua golongan darah adalah ...", "Golongan darah O", ["Golongan darah AB", "Golongan darah A", "Golongan darah B"]),
        ("Tekanan darah tinggi di atas batas normal sering disebut istilah medis ...", "Hipertensi", ["Hipotensi", "Anemia", "Varises"]),
        ("Tekanan darah rendah di bawah batas normal disebut ...", "Hipotensi", ["Hipertensi", "Leukemia", "Stroke"]),
        ("Pelebaran pembuluh darah vena pada betis kaki disebut ...", "Varises", ["Ambeien", "Arteriosklerosis", "Emboli"]),
        ("Tulang terpanjang dan terkuat pada rangka tubuh manusia adalah ...", "Tulang paha (Femur)", ["Tulang kering", "Tulang lengan atas", "Tulang betis"]),
        ("Tulang yang berfungsi melindungi organ otak manusia dari benturan adalah ...", "Tulang tengkorak", ["Tulang rusuk", "Tulang belakang", "Tulang panggul"]),
        ("Tulang yang melindungi organ penting jantung dan paru-paru adalah ...", "Tulang rusuk dan dada", ["Tulang panggul", "Tulang tengkorak", "Tulang belikat"]),
        ("Jumlah tulang rusuk sejati pada manusia dewasa adalah ...", "7 pasang", ["3 pasang", "2 pasang", "12 pasang"]),
        ("Jumlah tulang rusuk palsu pada manusia adalah ...", "3 pasang", ["7 pasang", "2 pasang", "5 pasang"]),
        ("Jumlah tulang rusuk melayang pada manusia adalah ...", "2 pasang", ["3 pasang", "7 pasang", "1 pasang"]),
        ("Sendi yang memungkinkan gerakan ke segala arah seperti pada hubungan antara lengan atas dan gelang bahu adalah ...", "Sendi peluru", ["Sendi engsel", "Sendi putar", "Sendi pelana"]),
        ("Sendi yang hanya memungkinkan gerakan ke satu arah seperti pada siku dan lutut adalah ...", "Sendi engsel", ["Sendi peluru", "Sendi putar", "Sendi geser"]),
        ("Sendi yang memungkinkan gerakan berputar seperti antara tulang tengkorak dan tulang leher pertama (atlas) adalah ...", "Sendi putar", ["Sendi engsel", "Sendi pelana", "Sendi peluru"]),
        ("Sendi yang memungkinkan gerakan ke dua arah seperti pada pangkal ibu jari tangan adalah ...", "Sendi pelana", ["Sendi putar", "Sendi engsel", "Sendi geser"]),
        ("Kelainan tulang belakang yang membengkok ke samping kiri atau kanan disebut ...", "Skoliosis", ["Lordosis", "Kifosis", "Osteoporosis"]),
        ("Kelainan tulang belakang yang membengkok ke depan pada bagian pinggang disebut ...", "Lordosis", ["Kifosis", "Skoliosis", "Rakitis"]),
        ("Kelainan tulang belakang yang membengkok ke belakang sehingga tubuh tampak bungkuk disebut ...", "Kifosis", ["Lordosis", "Skoliosis", "Polio"]),
        ("Penyakit pengeroposan massa tulang akibat kekurangan kalsium pada usia lanjut disebut ...", "Osteoporosis", ["Rakitis", "Rematik", "Kifosis"]),
        ("Penyakit pelunakan dan pembengkokan tulang pada anak-anak (kaki bentuk X atau O) akibat defisiensi vitamin D disebut ...", "Rakitis", ["Osteoporosis", "Skoliosis", "Polio"]),
        ("Gigi manusia yang berfungsi untuk memotong makanan adalah ...", "Gigi seri", ["Gigi taring", "Gigi geraham", "Gigi susu"]),
        ("Gigi manusia yang berujung runcing dan berfungsi untuk merobek makanan adalah ...", "Gigi taring", ["Gigi seri", "Gigi geraham", "Gigi bungsu"]),
        ("Gigi manusia yang permukaannya lebar dan berfungsi melumatkan atau mengunyah makanan adalah ...", "Gigi geraham", ["Gigi taring", "Gigi seri", "Gigi depan"]),
        ("Lapisan terluar gigi yang paling keras dan berwarna putih mengilap disebut ...", "Email gigi", ["Dentin (tulang gigi)", "Pulpa", "Gusi"]),
        ("Bagian dalam gigi yang berisi pembuluh darah dan saraf adalah ...", "Pulpa", ["Email", "Dentin", "Semen gigi"]),
        ("Jumlah gigi susu lengkap pada anak-anak adalah ...", "20 buah", ["32 buah", "28 buah", "24 buah"]),
        ("Jumlah gigi permanen lengkap pada orang dewasa adalah ...", "32 buah", ["20 buah", "28 buah", "36 buah"]),
        ("Enzim pencernaan di dalam rongga mulut yang mengubah amilum/karbohidrat menjadi glukosa/maltosa adalah ...", "Enzim ptialin (Amilase mulut)", ["Enzim pepsin", "Enzim renin", "Enzim lipase"]),
        ("Enzim di dalam lambung yang berfungsi memecah protein menjadi pepton adalah ...", "Enzim pepsin", ["Enzim ptialin", "Enzim lipase", "Enzim maltase"]),
        ("Enzim di dalam lambung yang berfungsi mengendapkan protein kasein susu adalah ...", "Enzim renin", ["Enzim pepsin", "Enzim amilase", "Enzim tripsin"]),
        ("Enzim pencernaan yang mencerna lemak menjadi asam lemak dan gliserol adalah ...", "Enzim lipase", ["Enzim amilase", "Enzim pepsin", "Enzim ptialin"]),
    ]
    for q_text, corr, dists in blood_and_bones:
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan tentang darah, tulang, sendi, dan gigi manusia."))

    # 3. Klasifikasi Hewan Berdasarkan Makanan & Reproduksi
    animal_classes = [
        ("Hewan pemakan tumbuhan seperti rumput dan daun-daunan disebut kelompok ...", "Herbivora", ["Karnivora", "Omnivora", "Insektivora"]),
        ("Hewan pemakan daging hewan lain disebut kelompok ...", "Karnivora", ["Herbivora", "Omnivora", "Insektivora"]),
        ("Hewan pemakan segala, baik tumbuhan maupun daging, disebut kelompok ...", "Omnivora", ["Herbivora", "Karnivora", "Insektivora"]),
        ("Hewan pemakan khusus serangga seperti bunglon dan cecak disebut ...", "Insektivora", ["Herbivora", "Karnivora", "Frugivora"]),
        ("Sapi, kambing, kelinci, dan kuda berdasarkan jenis makanannya termasuk kelompok ...", "Herbivora", ["Karnivora", "Omnivora", "Insektivora"]),
        ("Gajah, jerapah, panda, dan rusa termasuk golongan hewan pemakan tumbuhan atau ...", "Herbivora", ["Karnivora", "Omnivora", "Insektivora"]),
        ("Harimau, singa, serigala, dan elang berdasarkan jenis makanannya termasuk kelompok ...", "Karnivora", ["Herbivora", "Omnivora", "Insektivora"]),
        ("Ikan hiu, buaya, komodo, dan citah termasuk golongan hewan pemakan daging atau ...", "Karnivora", ["Herbivora", "Omnivora", "Insektivora"]),
        ("Ayam, bebek, tikus, dan monyet berdasarkan jenis makanannya termasuk kelompok ...", "Omnivora", ["Herbivora", "Karnivora", "Insektivora"]),
        ("Beruang, babi, dan simpanse memakan buah dan daging sehingga digolongkan sebagai ...", "Omnivora", ["Herbivora", "Karnivora", "Insektivora"]),
        ("Katak, cecak, bunglon, dan trenggiling memakan semut/nyamuk sehingga tergolong ...", "Insektivora", ["Herbivora", "Karnivora", "Omnivora"]),
        ("Hewan yang berkembang biak dengan cara melahirkan (beranak) disebut hewan ...", "Vivipar", ["Ovipar", "Ovovivipar", "Fragmentasi"]),
        ("Hewan yang berkembang biak dengan cara bertelur disebut hewan ...", "Ovipar", ["Vivipar", "Ovovivipar", "Tunas"]),
        ("Hewan yang berkembang biak dengan cara bertelur dan menetas di dalam tubuh induknya baru dilahirkan disebut ...", "Ovovivipar", ["Vivipar", "Ovipar", "Membelah diri"]),
        ("Kucing, sapi, kambing, dan kelinci berkembang biak dengan cara ...", "Melahirkan (Vivipar)", ["Bertelur (Ovipar)", "Bertelur-melahirkan (Ovovivipar)", "Tunas"]),
        ("Paus dan lumba-lumba meskipun hidup di laut bernapas dengan paru-paru dan berkembang biak secara ...", "Melahirkan (Vivipar)", ["Bertelur (Ovipar)", "Bertelur-melahirkan (Ovovivipar)", "Membelah diri"]),
        ("Kelelawar mamalia yang bisa terbang berkembang biak dengan cara ...", "Melahirkan (Vivipar)", ["Bertelur (Ovipar)", "Bertelur-melahirkan", "Fragmentasi"]),
        ("Ayam, bebek, burung dara, dan angsa berkembang biak dengan cara ...", "Bertelur (Ovipar)", ["Melahirkan (Vivipar)", "Ovovivipar", "Membelah diri"]),
        ("Katak, ikan mas, penyu, dan buaya berkembang biak dengan cara ...", "Bertelur (Ovipar)", ["Melahirkan (Vivipar)", "Ovovivipar", "Tunas"]),
        ("Ikan pari, ikan hiu tertentu, dan ular boa berkembang biak secara ...", "Bertelur-melahirkan (Ovovivipar)", ["Melahirkan saja (Vivipar)", "Bertelur saja (Ovipar)", "Fragmentasi"]),
        ("Platipus mamalia berkaki selaput dan berparuh bebek dari Australia berkembang biak dengan cara ...", "Bertelur (Ovipar)", ["Melahirkan (Vivipar)", "Ovovivipar", "Tunas"]),
        ("Ciri khas hewan mamalia yang melahirkan adalah memiliki kelenjar ...", "Susu (Mammae)", ["Bisa", "Minyak sayap", "Lendir"]),
        ("Ciri khas hewan mamalia darat pada bagian luar tubuhnya adalah memiliki daun ...", "Telinga", ["Sayap", "Sirip", "Insang"]),
        ("Hewan yang memiliki tulang belakang disebut kelompok hewan ...", "Vertebrata", ["Avertebrata (Invertebrata)", "Mikroskopis", "Uniseluler"]),
        ("Hewan yang tidak memiliki tulang belakang disebut kelompok hewan ...", "Avertebrata (Invertebrata)", ["Vertebrata", "Mamalia", "Reptil"]),
        ("Cacing, serangga, ubur-ubur, dan gurita termasuk kelompok hewan ...", "Avertebrata (Tidak bertulang belakang)", ["Vertebrata", "Mamalia", "Amfibi"]),
        ("Ikan, amfibi, reptil, burung, dan mamalia termasuk kelompok hewan ...", "Vertebrata (Bertulang belakang)", ["Avertebrata", "Insekta", "Moluska"]),
        ("Hewan berdarah panas yang suhu tubuhnya konstan/tetap terhadap lingkungan disebut ...", "Poikiloterm", ["Poikiloterm", "Heterotrof", "Autotrof"]),
        ("Hewan berdarah dingin yang suhu tubuhnya menyesuaikan dengan suhu lingkungan disebut ...", "Poikiloterm", ["Homoioterm", "Karnivora", "Mamalia"]),
        ("Kelompok hewan yang termasuk berdarah panas (homoioterm) adalah ...", "Burung dan Mamalia", ["Ikan dan Reptil", "Amfibi dan Serangga", "Cacing dan Moluska"]),
        ("Kelompok hewan yang termasuk berdarah dingin (poikiloterm) adalah ...", "Ikan, Amfibi, dan Reptil", ["Burung dan Mamalia", "Kucing dan Sapi", "Ayam dan Bebek"]),
    ]
    for q_text, corr, dists in animal_classes:
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami penggolongan jenis hewan dan reproduksinya."))

    # 4. Pernapasan & Adaptasi Hewan
    animal_respiration = [
        ("Organ pernapasan utama pada ikan untuk menyaring oksigen dari air adalah ...", "Insang", ["Paru-paru", "Trakea", "Kulit"]),
        ("Alat bantu pernapasan tambahan pada ikan lele untuk hidup di lumpur minim oksigen adalah ...", "Labirin", ["Kantung udara", "Paru-paru", "Trakea"]),
        ("Katak dewasa dapat bernapas dengan dua organ, yaitu paru-paru dan ...", "Kulit yang lembap", ["Insang luar", "Trakea", "Sayap"]),
        ("Kecebong atau berudu katak yang masih hidup di air bernapas dengan ...", "Insang", ["Paru-paru", "Kulit kering", "Trakea"]),
        ("Hewan reptil seperti buaya, kadal, dan ular bernapas menggunakan ...", "Paru-paru", ["Insang", "Kulit", "Trakea"]),
        ("Burung bernapas dengan paru-paru yang dibantu oleh kantung penyimpan udara bernama ...", "Pundi-pundi udara (Kantung udara)", ["Labirin", "Insang", "Kloaka"]),
        ("Pundi-pundi udara pada burung terutama berfungsi membantu pernapasan saat burung sedang ...", "Terbang", ["Tidur", "Makan", "Mengerami telur"]),
        ("Serangga seperti belalang, semut, kupu-kupu, dan nyamuk bernapas menggunakan sistem ...", "Trakea", ["Insang", "Paru-paru", "Kulit lembap"]),
        ("Lubang-lubang pernapasan di sepanjang sisi tubuh serangga penghubung saluran trakea disebut ...", "Spirakel (Stigma)", ["Stomata", "Pori kulit", "Insang"]),
        ("Cacing tanah menyerap gas oksigen dari udara melalui seluruh permukaan ...", "Kulitnya yang basah dan berlendir", ["Mulut", "Insang", "Paru-paru"]),
        ("Hewan mamalia air seperti paus dan lumba-lumba muncul ke permukaan air untuk bernapas menghirup ...", "Oksigen menggunakan paru-paru", ["Air menggunakan insang", "Makanan", "Garam"]),
        ("Hewan yang mengalami metamorfosis sempurna melalui tahapan telur -> larva (ulat) -> pupa (kepompong) -> dewasa adalah ...", "Kupu-kupu", ["Belalang", "Kecoa", "Capung"]),
        ("Tahapan metamorfosis sempurna pada nyamuk dimulai dari telur -> jentik-jentik -> pupa -> nyamuk ...", "Dewasa", ["Nimfa", "Kepompong daun", "Ulat"]),
        ("Tahapan metamorfosis pada lalat dimulai dari telur -> belatung (larva) -> pupa -> lalat ...", "Dewasa", ["Nimfa", "Ulat", "Jentik"]),
        ("Metamorfosis pada belalang dan kecoa disebut metamorfosis tidak sempurna karena tidak melalui tahap ...", "Pupa (Kepompong)", ["Telur", "Dewasa", "Nimfa"]),
        ("Anak belalang atau kecoa muda yang bentuk fisiknya menyerupai dewasa tetapi belum bersayap disebut ...", "Nimfa", ["Larva", "Pupa", "Kepompong"]),
        ("Kemampuan bunglon mengubah warna kulit tubuhnya sesuai dengan warna lingkungan sekitarnya disebut ...", "Mimikri", ["Autotomi", "Ekolokasi", "Kamuflase"]),
        ("Kemampuan cecak atau kadal memutuskan ekornya untuk mengelabui mangsa disebut ...", "Autotomi", ["Mimikri", "Ekolokasi", "Hibernasi"]),
        ("Kemampuan kelelawar dan lumba-lumba memancarkan dan mendeteksi pantulan bunyi frekuensi tinggi disebut ...", "Ekolokasi", ["Autotomi", "Mimikri", "Estivasi"]),
        ("Hewan trenggiling dan kaki seribu melindungi diri dari serangan musuh dengan cara ...", "Menggulungkan tubuhnya", ["Memutuskan ekor", "Mengubah warna kulit", "Menyemprotkan bisa"]),
        ("Cumi-cumi dan gurita melindungi diri dari pemangsa dengan cara menyemprotkan cairan ...", "Tinta hitam pekat", ["Racun bisa", "Bau busuk", "Minyak"]),
        ("Walang sangit melindungi dirinya dari ancaman predator dengan cara mengeluarkan ...", "Bau yang sangat menyengat", ["Tinta hitam", "Cahaya kilat", "Sengatan listrik"]),
        ("Unta mampu bertahan berhari-hari di padang pasir tanpa makan karena menyimpan cadangan lemak pada ...", "Punuknya", ["Lehernya", "Kakinya", "Lambungnya"]),
        ("Bebek memiliki selaput pada jari-jari kakinya yang berfungsi memudahkan saat ...", "Berenang di air", ["Mencengkeram pohon", "Memanjat tebing", "Menangkap mangsa"]),
        ("Burung kolibri memiliki paruh kecil yang panjang dan runcing untuk menghisap ...", "Nektar (madu bunga)", ["Daging", "Biji-bijian", "Ikan"]),
        ("Burung elang memiliki paruh kokoh melengkung tajam dan cakar kuat yang berfungsi untuk ...", "Mencabik daging mangsa", ["Memecah biji", "Menyaring lumpur", "Menghisap madu"]),
        ("Tidur panjang tanpa aktivitas yang dilakukan hewan tertentu saat musim dingin bersalju disebut ...", "Hibernasi", ["Estivasi", "Migrasi", "Adaptasi"]),
    ]
    for q_text, corr, dists in animal_respiration:
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan cara adaptasi dan sistem pernapasan makhluk hidup."))

    # 5. Tumbuhan, Fotosintesis, Perkembangbiakan Tumbuhan
    plant_biology = [
        ("Bagian tumbuhan yang berfungsi menyerap air dan mineral dari dalam tanah adalah ...", "Akar", ["Batang", "Daun", "Bunga"]),
        ("Bagian tumbuhan yang berfungsi menopang tubuh tumbuhan dan mengalirkan sari makanan adalah ...", "Batang", ["Akar", "Bunga", "Biji"]),
        ("Bagian utama tumbuhan yang menjadi tempat berlangsungnya proses fotosintesis adalah ...", "Daun", ["Akar", "Batang", "Bunga"]),
        ("Zat hijau daun yang berfungsi menangkap energi cahaya matahari untuk fotosintesis adalah ...", "Klorofil", ["Karoten", "Hemoglobin", "Melanin"]),
        ("Gas dari udara yang diserap oleh daun tumbuhan hijau untuk proses fotosintesis adalah ...", "Karbon dioksida (CO2)", ["Oksigen", "Nitrogen", "Helium"]),
        ("Gas yang dihasilkan oleh tumbuhan hijau pada akhir reaksi fotosintesis yang kita hirup adalah ...", "Oksigen (O2)", ["Karbon dioksida", "Karbon monoksida", "Metana"]),
        ("Zat makanan hasil fotosintesis yang tersimpan dalam bentuk cadangan energi tumbuhan adalah ...", "Glukosa / Karbohidrat (Amilum)", ["Protein", "Lemak hewani", "Garam mineral"]),
        ("Mulut daun yang berfungsi sebagai tempat pertukaran udara dan penguapan air disebut ...", "Stomata", ["Lentisel", "Klorofil", "Kutikula"]),
        ("Lubang-lubang kecil pada kulit batang pohon tempat pertukaran udara disebut ...", "Lentisel", ["Stomata", "Floem", "Xilem"]),
        ("Jaringan pembuluh pada tumbuhan yang bertugas mengangkut air dan mineral dari akar ke daun adalah ...", "Xilem (Pembuluh kayu)", ["Floem (Pembuluh tapis)", "Kambium", "Korteks"]),
        ("Jaringan pembuluh yang mengangkut hasil fotosintesis dari daun ke seluruh bagian tumbuhan adalah ...", "Floem (Pembuluh tapis)", ["Xilem (Pembuluh kayu)", "Kambium", "Epidermis"]),
        ("Jaringan pada tumbuhan dikotil yang aktif membelah dan menyebabkan batang membesar adalah ...", "Kambium", ["Xilem", "Floem", "Epidermis"]),
        ("Akar utama yang berukuran besar dan memiliki percabangan akar kecil disebut jenis akar ...", "Akar tunggang", ["Akar serabut", "Akar gantung", "Akar napas"]),
        ("Pohon mangga, jambu, durian, dan jeruk memiliki sistem perakaran ...", "Akar tunggang", ["Akar serabut", "Akar napas", "Akar lekat"]),
        ("Tumbuhan padi, jagung, kelapa, dan rumput memiliki sistem perakaran ...", "Akar serabut", ["Akar tunggang", "Akar tunjang", "Akar gantung"]),
        ("Pohon beringin memiliki akar khusus yang menjulur dari batang ke bawah disebut ...", "Akar gantung", ["Akar napas", "Akar serabut", "Akar tunggang"]),
        ("Pohon bakau (mangrove) yang tumbuh di pantai berlumpur memiliki akar khusus bernama ...", "Akar napas / tunjang", ["Akar gantung", "Akar serabut", "Akar semu"]),
        ("Tumbuhan sirih merayap pada batang pohon inang dengan bantuan akar ...", "Akar lekat", ["Akar gantung", "Akar tunggang", "Akar serabut"]),
        ("Bentuk susunan tulang daun pada tanaman pepaya dan singkong adalah ...", "Menjari", ["Menyirip", "Sejajar", "Melengkung"]),
        ("Bentuk susunan tulang daun pada pohon mangga dan jambu adalah ...", "Menyirip", ["Menjari", "Sejajar", "Melengkung"]),
        ("Bentuk susunan tulang daun pada tanaman padi, jagung, dan tebu adalah ...", "Sejajar", ["Menyirip", "Menjari", "Melengkung"]),
        ("Bentuk susunan tulang daun pada tanaman sirih dan genjer adalah ...", "Melengkung", ["Sejajar", "Menjari", "Menyirip"]),
        ("Tumbuhan yang bijinya berkeping satu disebut tumbuhan ...", "Monokotil", ["Dikotil", "Gymnospermae", "Paku"]),
        ("Tumbuhan yang bijinya berkeping dua disebut tumbuhan ...", "Dikotil", ["Monokotil", "Lumut", "Alga"]),
        ("Padi, jagung, kelapa, dan pisang merupakan contoh kelompok tumbuhan ...", "Monokotil", ["Dikotil", "Paku-pakuan", "Kaktus"]),
        ("Mangga, kacang tanah, rambutan, dan cabai merupakan contoh tumbuhan ...", "Dikotil", ["Monokotil", "Alga", "Lumut"]),
        ("Alat perkembangbiakan jantan pada bunga yang menghasilkan serbuk sari adalah ...", "Benang sari", ["Putik", "Mahkota bunga", "Kelopak bunga"]),
        ("Alat perkembangbiakan betina pada bunga yang menerima serbuk sari adalah ...", "Putik", ["Benang sari", "Mahkota bunga", "Tangkai bunga"]),
        ("Bagian bunga yang berwarna-warni mencolok untuk menarik perhatian serangga penyerbuk adalah ...", "Mahkota bunga", ["Kelopak bunga", "Tangkai bunga", "Dasar bunga"]),
        ("Bagian bunga terluar yang berwarna hijau dan melindungi kuncup bunga sebelum mekar adalah ...", "Kelopak bunga", ["Mahkota bunga", "Dasar bunga", "Putik"]),
        ("Peristiwa jatuhnya serbuk sari ke atas kepala putik disebut proses ...", "Penyerbukan (Polinasi)", ["Pembuahan (Fertilisasi)", "Fotosintesis", "Germinasi"]),
        ("Tumbuhan pisang dan bambu berkembang biak secara vegetatif alami menggunakan ...", "Tunas", ["Umbi batang", "Spora", "Rizoma"]),
        ("Tumbuhan cocor bebek berkembang biak secara vegetatif alami melalui tunas ...", "Tunas adventif pada daun", ["Umbi lapis", "Geragih", "Biji"]),
        ("Tanaman stroberi dan rumput teki berkembang biak secara vegetatif dengan batang merayap di tanah bernama ...", "Geragih (Stolon)", ["Rizoma", "Umbi akar", "Tunas"]),
        ("Jahe, kunyit, kencur, dan lengkuas berkembang biak secara vegetatif menggunakan batang bawah tanah bernama ...", "Rizoma (Akar tinggal)", ["Geragih", "Umbi batang", "Tunas adventif"]),
        ("Bawang merah dan bawang putih berkembang biak secara vegetatif menggunakan ...", "Umbi lapis", ["Umbi batang", "Rizoma", "Spora"]),
        ("Kentang dan ubi jalar menyimpan cadangan makanannya pada batang bawah tanah yang disebut ...", "Umbi batang", ["Umbi akar", "Umbi lapis", "Rizoma"]),
        ("Wortel dan lobak menyimpan cadangan makanannya pada bagian akar yang membesar disebut ...", "Umbi akar", ["Umbi batang", "Umbi lapis", "Geragih"]),
        ("Tumbuhan paku dan lumut yang tidak berbunga berkembang biak menggunakan ...", "Spora", ["Biji", "Bunga", "Tunas"]),
        ("Tumbuhan pemakan serangga seperti kantong semar dan venus flytrap memakan serangga untuk mendapatkan zat ...", "Nitrogen", ["Karbohidrat", "Kalsium", "Air"]),
        ("Tumbuhan kaktus yang hidup di gurun kering mengubah bentuk daunnya menjadi ...", "Duri tajam", ["Bunga besar", "Akar gantung", "Kulit kayu tebal"]),
        ("Kaktus menyimpan cadangan air dalam jumlah besar pada bagian ...", "Batangnya yang tebal dan berdaging", ["Akarnya", "Durinya", "Bunganya"]),
    ]
    for q_text, corr, dists in plant_biology:
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami bagian tumbuhan, fotosintesis, dan perkembangbiakannya."))

    # 6. Ekologi, Simbiosis & Rantai Makanan
    ecology_facts = [
        ("Organisme yang mampu membuat makanannya sendiri melalui fotosintesis dalam ekosistem disebut ...", "Produsen (Autotrof)", ["Konsumen primer", "Dekomposer", "Pengurai"]),
        ("Hewan herbivora yang langsung memakan tumbuhan produsen menempati tingkatan ...", "Konsumen tingkat I (Primer)", ["Konsumen sekunder", "Konsumen tersier", "Pengurai"]),
        ("Organisme pengurai seperti bakteri dan jamur yang menguraikan sisa makhluk hidup mati disebut ...", "Dekomposer", ["Produsen", "Konsumen primer", "Predator"]),
        ("Hubungan ketergantungan makan dan dimakan antara makhluk hidup dalam urutan tertentu disebut ...", "Rantai makanan", ["Piramida makanan", "Jaring-jaring kehidupan", "Simbiosis"]),
        ("Kumpulan dari beberapa rantai makanan yang saling berhubungan dan bercabang disebut ...", "Jaring-jaring makanan", ["Simbiosis", "Habitat", "Populasi"]),
        ("Tempat hidup alami tempat suatu makhluk hidup tumbuh dan berkembang biak disebut ...", "Habitat", ["Komunitas", "Ekosistem", "Bioma"]),
        ("Hubungan hidup bersama antara dua jenis makhluk hidup yang berbeda disebut ...", "Simbiosis", ["Predasi", "Kompetisi", "Adaptasi"]),
        ("Hubungan simbiosis di mana kedua belah pihak saling mendapatkan keuntungan disebut ...", "Simbiosis mutualisme", ["Simbiosis komensalisme", "Simbiosis parasitisme", "Predasi"]),
        ("Hubungan simbiosis di mana satu pihak untung sementara pihak lain tidak dirugikan dan tidak diuntungkan disebut ...", "Simbiosis komensalisme", ["Simbiosis mutualisme", "Simbiosis parasitisme", "Kompetisi"]),
        ("Hubungan simbiosis di mana satu pihak mendapat untung sedangkan pihak lainnya menderita kerugian disebut ...", "Simbiosis parasitisme", ["Simbiosis mutualisme", "Simbiosis komensalisme", "Netral"]),
        ("Hubungan antara kupu-kupu atau lebah dengan bunga tanaman berbunga merupakan contoh ...", "Simbiosis mutualisme", ["Simbiosis parasitisme", "Simbiosis komensalisme", "Predasi"]),
        ("Hubungan antara burung jalak yang memakan kutu di punggung kerbau merupakan contoh ...", "Simbiosis mutualisme", ["Simbiosis parasitisme", "Simbiosis komensalisme", "Predasi"]),
        ("Hubungan antara ikan badut yang berlindung di antara tentakel anemon laut merupakan contoh ...", "Simbiosis mutualisme", ["Simbiosis komensalisme", "Simbiosis parasitisme", "Kompetisi"]),
        ("Hubungan antara tanaman anggrek yang menempel pada batang pohon mangga merupakan contoh ...", "Simbiosis komensalisme", ["Simbiosis mutualisme", "Simbiosis parasitisme", "Kompetisi"]),
        ("Hubungan antara ikan remora yang menempel pada tubuh ikan hiu untuk mencari sisa makanan merupakan contoh ...", "Simbiosis komensalisme", ["Simbiosis mutualisme", "Simbiosis parasitisme", "Predasi"]),
        ("Hubungan antara tanaman paku tanduk rusa yang menempel pada pohon inang tanpa merugikan inang adalah ...", "Simbiosis komensalisme", ["Simbiosis mutualisme", "Simbiosis parasitisme", "Predasi"]),
        ("Kutu rambut yang hidup di kepala manusia dan menghisap darah merupakan contoh ...", "Simbiosis parasitisme", ["Simbiosis mutualisme", "Simbiosis komensalisme", "Netral"]),
        ("Tanaman benalu yang menyerap air dan mineral dari pohon inang hingga inangnya kurus/mati merupakan contoh ...", "Simbiosis parasitisme", ["Simbiosis mutualisme", "Simbiosis komensalisme", "Kompetisi"]),
        ("Tanaman tali putri yang tumbuh menutupi tanaman pagar dan menghisap nutrisinya merupakan contoh ...", "Simbiosis parasitisme", ["Simbiosis mutualisme", "Simbiosis komensalisme", "Predasi"]),
        ("Cacing pita yang hidup di dalam usus manusia dan mengambil sari makanan adalah contoh ...", "Simbiosis parasitisme", ["Simbiosis komensalisme", "Simbiosis mutualisme", "Netral"]),
        ("Peristiwa di mana satu hewan memangsa hewan lain untuk dimakan disebut ...", "Predasi", ["Simbiosis", "Kompetisi", "Parasitisme"]),
        ("Singa yang memburu dan memangsa zebra di padang rumput bertindak sebagai ...", "Predator (Pemangsa)", ["Mangsa", "Parasit", "Produsen"]),
        ("Hewan yang diburu dan dimakan oleh predator disebut ...", "Mangsa (Prey)", ["Predator", "Parasit", "Dekomposer"]),
    ]
    for q_text, corr, dists in ecology_facts:
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami rantai makanan dan hubungan antar makhluk hidup."))

    # 7. Vitamin, Gizi, Kesehatan & Makanan Sehat
    health_and_vitamins = [
        ("Vitamin yang sangat penting untuk menjaga kesehatan mata dan mencegah rabun senja adalah ...", "Vitamin A", ["Vitamin B", "Vitamin C", "Vitamin D"]),
        ("Sayuran berwarna oranye yang kaya akan kandungan provitamin A (beta karoten) adalah ...", "Wortel", ["Bayam", "Mentimun", "Kembang kol"]),
        ("Kekurangan vitamin A dalam jangka panjang dapat menyebabkan penyakit mata bernama ...", "Xeroftalmia (Rabun senja)", ["Beri-beri", "Sariawan", "Rakitis"]),
        ("Penyakit beri-beri disebabkan oleh tubuh yang kekurangan asupan ...", "Vitamin B1", ["Vitamin C", "Vitamin A", "Vitamin D"]),
        ("Vitamin yang membantu pembentukan sel darah merah dan mencegah anemia adalah ...", "Vitamin B12", ["Vitamin C", "Vitamin D", "Vitamin K"]),
        ("Vitamin yang berfungsi meningkatkan daya tahan tubuh dan mencegah sariawan adalah ...", "Vitamin C", ["Vitamin A", "Vitamin D", "Vitamin E"]),
        ("Buah-buahan segar yang kaya akan kandungan vitamin C adalah ...", "Jeruk dan jambu biji", ["Alpukat dan kelapa", "Pisang dan salak", "Semangka dan melon"]),
        ("Penyakit gusi berdarah dan sariawan parah akibat kekurangan vitamin C disebut ...", "Skorbut", ["Rakhitis", "Beri-beri", "Polio"]),
        ("Vitamin yang berperan penting dalam membantu penyerapan kalsium untuk pertumbuhan tulang dan gigi adalah ...", "Vitamin D", ["Vitamin C", "Vitamin B", "Vitamin E"]),
        ("Sumber alami yang membantu tubuh manusia memproduksi vitamin D sendiri di bawah kulit adalah ...", "Sinar matahari pagi", ["Air hujan", "Udara dingin", "Minyak goreng"]),
        ("Kekurangan vitamin D dan kalsium pada masa pertumbuhan anak dapat memicu penyakit ...", "Rakitis", ["Skorbut", "Beri-beri", "Anemia"]),
        ("Vitamin yang berfungsi sebagai antioksidan alami dan menjaga kesehatan kulit adalah ...", "Vitamin E", ["Vitamin K", "Vitamin B", "Vitamin C"]),
        ("Bahan makanan kecambah (toge) dan minyak nabati banyak mengandung ...", "Vitamin E", ["Vitamin D", "Vitamin B12", "Kalsium murni"]),
        ("Vitamin yang berperan penting dalam proses pembekuan darah saat tubuh mengalami luka adalah ...", "Vitamin K", ["Vitamin A", "Vitamin C", "Vitamin D"]),
        ("Mineral yang dibutuhkan tubuh untuk membentuk hemoglobin dalam sel darah merah adalah ...", "Zat besi (Fe)", ["Kalsium", "Iodium", "Fluor"]),
        ("Sayuran hijau gelap seperti daun bayam dan hati ayam merupakan sumber makanan kaya akan ...", "Zat besi", ["Vitamin D", "Glukosa", "Iodium"]),
        ("Mineral utama pembentuk kepadatan tulang dan kekuatan email gigi manusia adalah ...", "Kalsium (Ca)", ["Zat besi", "Iodium", "Natrium"]),
        ("Susu, keju, dan yoghurt merupakan sumber makanan yang sangat kaya akan ...", "Kalsium", ["Vitamin C", "Zat besi", "Zat asam sitrat"]),
        ("Mineral yang dibutuhkan oleh kelenjar tiroid untuk mencegah penyakit gondok adalah ...", "Iodium", ["Zat besi", "Kalsium", "Fosfor"]),
        ("Garam dapur yang sehat untuk mencegah pembengkakan kelenjar gondok diperkaya dengan mineral ...", "Iodium", ["Kalsium", "Tembaga", "Besi"]),
        ("Mineral yang sering ditambahkan pada pasta gigi untuk menguatkan lapisan gigi dari kuman adalah ...", "Fluorida (Fluor)", ["Kalsium", "Belerang", "Besi"]),
        ("Zat gizi yang berfungsi sebagai sumber energi utama bagi tubuh untuk beraktivitas adalah ...", "Karbohidrat", ["Protein", "Vitamin", "Mineral"]),
        ("Makanan pokok seperti beras, jagung, kentang, dan singkong kaya akan kandungan ...", "Karbohidrat", ["Protein hewani", "Vitamin C", "Kalsium"]),
        ("Zat gizi yang berfungsi sebagai zat pembangun tubuh, membentuk sel baru, dan mengganti sel rusak adalah ...", "Protein", ["Karbohidrat", "Lemak", "Mineral"]),
        ("Contoh sumber makanan yang kaya akan protein nabati (tumbuhan) adalah ...", "Tempe dan tahu", ["Daging sapi", "Telur ayam", "Ikan tongkol"]),
        ("Contoh sumber makanan yang kaya akan protein hewani adalah ...", "Ikan, telur, dan daging", ["Tempe dan kedelai", "Bayam dan wortel", "Nasi dan jagung"]),
        ("Zat gizi yang berfungsi sebagai cadangan energi dan pelindung organ tubuh dari benturan adalah ...", "Lemak", ["Karbohidrat", "Vitamin", "Air"]),
        ("Kondisi tubuh kekurangan cairan karena kurang minum air putih atau diare disebut ...", "Dehidrasi", ["Anemia", "Hipertensi", "Malnutrisi"]),
        ("Berapa liter jumlah air putih minimal yang dianjurkan diminum setiap hari untuk menjaga kesehatan?", "Sekitar 2 liter (8 gelas)", ["10 liter", "500 mL", "1 gelas saja"]),
        ("Vaksinasi atau imunisasi diberikan ke dalam tubuh dengan tujuan untuk ...", "Membentuk kekebalan tubuh terhadap penyakit tertentu", ["Mengobati patah tulang", "Mengurangi berat badan", "Menambah tinggi badan"]),
        ("Nyamuk Aedes aegypti dikenal sebagai perantara (vektor) penularan penyakit ...", "Demam Berdarah Dengue (DBD)", ["Malaria", "Tifus", "Kolera"]),
        ("Nyamuk Anopheles betina dikenal sebagai vektor perantara penularan penyakit ...", "Malaria", ["Demam Berdarah", "Flu burung", "Rabies"]),
        ("Bakteri Salmonella typhi dapat menular melalui makanan tercemar dan menyebabkan penyakit ...", "Tifus (Tipes)", ["Demam berdarah", "TBC", "Cacar"]),
        ("Penyakit batuk menular pada saluran pernapasan yang disebabkan oleh bakteri Mycobacterium tuberculosis adalah ...", "TBC (Tuberkulosis)", ["Asma", "Bronkitis", "Pneumonia"]),
        ("Penyakit rabies yang menyerang sistem saraf ditularkan melalui gigitan hewan berdarah panas seperti ...", "Anjing atau kera", ["Nyamuk", "Ikan lele", "Kecoa"]),
        ("Upacara 3M Plus untuk mencegah perkembangbiakan jentik nyamuk DBD adalah menguras, menutup, dan ...", "Mendaur ulang / mengubur barang bekas", ["Membakar rumah", "Mencuci piring", "Menyiram tanaman"]),
    ]
    for q_text, corr, dists in health_and_vitamins:
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan tentang vitamin, mineral, makanan bergizi, dan kesehatan."))

    # Additional biology questions to reach exactly 500
    more_bio = [
        ("Organel sel tumbuhan tempat berlangsungnya fotosintesis adalah ...", "Kloroplas", ["Mitokondria", "Ribosom", "Vakuola"]),
        ("Organel sel yang berfungsi sebagai pusat pembangkit energi sel (respirasi seluler) adalah ...", "Mitokondria", ["Kloroplas", "Ribosom", "Lisosom"]),
        ("Dinding sel yang kaku dan tebal hanya dimiliki oleh ...", "Sel tumbuhan", ["Sel hewan", "Sel darah merah", "Sel saraf manusia"]),
        ("Bagian sel yang mengatur seluruh kegiatan sel adalah ...", "Inti sel (Nukleus)", ["Sitoplasma", "Membran sel", "Vakuola"]),
        ("Cairan kental pengisi di dalam rongga sel disebut ...", "Sitoplasma", ["Plasma darah", "Hemoglobin", "Getah bening"]),
        ("Bagian sel hewan terluar yang lentur dan mengatur keluar masuknya zat adalah ...", "Membran sel", ["Dinding sel", "Korteks", "Epidermis"]),
        ("Organel sel tempat berlangsungnya sintesis protein adalah ...", "Ribosom", ["Sentriol", "Lisosom", "Kloroplas"]),
        ("Organel sel yang berfungsi mencerna bagian sel yang rusak atau zat asing adalah ...", "Lisosom", ["Mitokondria", "Ribosom", "Plastida"]),
        ("Kumpulan dari beberapa sel yang memiliki bentuk dan fungsi yang sama disebut ...", "Jaringan", ["Organ", "Sistem organ", "Individu"]),
        ("Kumpulan dari beberapa jaringan yang bekerja sama menjalankan fungsi tertentu membentuk ...", "Organ", ["Sel", "Sistem organ", "Populasi"]),
        ("Kumpulan dari beberapa organ yang bekerja sama menjalankan fungsi besar dalam tubuh membentuk ...", "Sistem organ", ["Jaringan", "Sel tunggal", "Komunitas"]),
        ("Contoh jaringan pada hewan dan manusia yang berfungsi menerima dan menghantarkan rangsang adalah ...", "Jaringan saraf", ["Jaringan otot", "Jaringan epitel", "Jaringan ikat"]),
        ("Contoh jaringan yang berfungsi sebagai alat gerak aktif karena mampu berkontraksi adalah ...", "Jaringan otot", ["Jaringan saraf", "Jaringan tulang", "Jaringan lemak"]),
        ("Tiga jenis otot pada tubuh manusia adalah otot lurik (rangka), otot jantung, dan ...", "Otot polos", ["Otot bisep", "Otot diafragma", "Otot sendi"]),
        ("Otot yang bekerja secara sadar di bawah kendali perintah otak menempel pada rangka adalah ...", "Otot lurik (rangka)", ["Otot polos", "Otot jantung", "Otot pembuluh"]),
        ("Otot yang bekerja secara tidak sadar (otomatis) menyusun dinding lambung dan usus adalah ...", "Otot polos", ["Otot lurik", "Otot rangka", "Otot sendi"]),
        ("Otot istimewa yang hanya ditemukan pada dinding jantung dan bekerja terus-menerus tanpa lelah adalah ...", "Otot jantung", ["Otot lurik", "Otot polos", "Otot seran lintang"]),
        ("Kemampuan makhluk hidup untuk melestarikan jenisnya agar tidak punah disebut ...", "Berkembang biak (Reproduksi)", ["Adaptasi", "Iritabilitas", "Evolusi"]),
        ("Ciri makhluk hidup yang peka dan merespons terhadap rangsangan luar disebut ...", "Iritabilitas", ["Respirasi", "Ekskresi", "Regenerasi"]),
        ("Proses pengeluaran zat-zat sisa metabolisme yang sudah tidak terpakai oleh tubuh disebut ...", "Ekskresi", ["Sekresi", "Defekasi", "Respirasi"]),
        ("Organ ekskresi pada manusia yang mengeluarkan zat sisa berupa keringat adalah ...", "Kulit", ["Paru-paru", "Hati", "Lambung"]),
        ("Organ ekskresi pada manusia yang mengeluarkan zat sisa berupa gas karbon dioksida dan uap air adalah ...", "Paru-paru", ["Kulit", "Ginjal", "Hati"]),
        ("Organ ekskresi yang mengeluarkan zat sisa berupa urine adalah ...", "Ginjal", ["Kulit", "Paru-paru", "Jantung"]),
        ("Organ ekskresi yang mengeluarkan zat sisa berupa zat warna empedu (bilirubin) adalah ...", "Hati", ["Ginjal", "Lambung", "Pankreas"]),
        ("Hewan amfibi adalah hewan yang dapat hidup di dua alam, yaitu di darat dan di ...", "Air", ["Puncak pohon", "Udara hampa", "Gurun pasir"]),
        ("Contoh hewan amfibi yang sangat terkenal di sekitar kita adalah ...", "Katak dan kodok", ["Kadal dan ular", "Buaya dan kura-kura", "Ikan mas dan lele"]),
        ("Hewan mamalia terbesar di muka bumi yang hidup di laut adalah ...", "Paus biru", ["Hiu megalodon", "Gajah afrika", "Ikan pari"]),
        ("Hewan darat terbesar yang masih hidup di bumi saat ini adalah ...", "Gajah afrika", ["Jerapah", "Kuda nil", "Badak putih"]),
        ("Hewan mamalia darat tertinggi di dunia yang memiliki leher sangat panjang adalah ...", "Jerapah", ["Unta", "Gajah", "Kuda"]),
        ("Hewan darat tercepat di dunia saat berlari mengejar mangsa adalah ...", "Citah (Cheetah)", ["Singa", "Kuda", "Kancil"]),
        ("Burung terbesar di dunia yang tidak bisa terbang dan bertelur sangat besar adalah ...", "Burung unta", ["Burung kasuari", "Burung merak", "Burung elang"]),
        ("Burung perenang handal berbulu tebal tahan dingin yang hidup di kutub selatan adalah ...", "Penguin", ["Flamingo", "Burung hantu", "Pelikan"]),
        ("Burung yang aktif berburu mangsa pada malam hari dan kepalanya bisa memutar 270 derajat adalah ...", "Burung hantu", ["Burung elang", "Burung gagak", "Burung bangau"]),
        ("Tumbuhan pemanjat yang batangnya berduri dan menghasilkan buah salak adalah ...", "Pohon salak", ["Pohon kelapa", "Pohon durian", "Pohon nangka"]),
        ("Tanaman yang menggugurkan daunnya pada musim kemarau untuk mengurangi penguapan contohnya adalah ...", "Pohon jati", ["Pohon pisang", "Pohon cemara", "Pohon bambu"]),
        ("Tumbuhan hidrofit yang seluruh atau sebagian tubuhnya terapung dan beradaptasi hidup di air adalah ...", "Teratai dan eceng gondok", ["Kaktus dan kurma", "Kunyit dan jahe", "Lidah buaya"]),
        ("Batang berongga udara pada tanaman eceng gondok berfungsi untuk membantu tanaman ...", "Mengapung di permukaan air", ["Menyerap oksigen tanah", "Menghasilkan getah", "Menyimpan racun"]),
        ("Daun lebar dan tipis pada tumbuhan teratai berfungsi untuk mempercepat proses ...", "Penguapan air", ["Fotosintesis di dalam lumpur", "Pertumbuhan bunga", "Pematangan biji"]),
        ("Tumbuhan higrofit yang beradaptasi di lingkungan lembap dan teduh contohnya adalah ...", "Tumbuhan paku dan lumut", ["Kaktus", "Eceng gondok", "Pohon kurma"]),
        ("Tumbuhan xerofit yang beradaptasi di lingkungan sangat kering atau tandus contohnya adalah ...", "Kaktus dan lidah buaya", ["Teratai", "Paku tanduk rusa", "Lumut hati"]),
        ("Tanaman putri malu akan mengatupkan daunnya bila terkena rangsangan sentuhan karena gerak ...", "Seismonasti (Tigmonasti)", ["Fototropisme", "Geotropisme", "Hidrotropisme"]),
        ("Gerak pertumbuhan ujung batang tanaman yang membelok ke arah datangnya cahaya matahari disebut ...", "Fototropisme positif", ["Geotropisme", "Hidrotropisme", "Tigmotropisme"]),
        ("Gerak pertumbuhan akar tumbuhan yang selalu menuju ke pusat gravitasi bumi disebut ...", "Geotropisme positif", ["Fototropisme", "Seismonasti", "Niktinasti"]),
        ("Gerak menutupnya daun tanaman lamtoro atau petai cina saat malam hari tiba disebut gerak ...", "Niktinasti (Gerak tidur)", ["Fototropisme", "Seismonasti", "Kemotropisme"]),
        ("Bakteri baik yang digunakan dalam proses fermentasi pembuatan yoghurt dari susu adalah ...", "Lactobacillus bulgaricus", ["Escherichia coli", "Salmonella typhi", "Amoeba"]),
        ("Jamur mikroskopis (ragi) yang digunakan dalam proses pembuatan tempe adalah ...", "Rhizopus oryzae", ["Saccharomyces cerevisiae", "Aspergillus", "Penicillium"]),
        ("Ragi yang digunakan dalam proses pembuatan roti agar adonan mengembang adalah ...", "Saccharomyces cerevisiae", ["Rhizopus", "Lactobacillus", "Spirulina"]),
        ("Antibiotik pertama di dunia yang ditemukan oleh Alexander Fleming dari jamur bernama ...", "Penisilin (Penicillium notatum)", ["Amoksisilin", "Tetrasiklin", "Streptomisin"]),
        ("Organisme uniseluler yang bergerak menggunakan kaki semu (pseudopodia) adalah ...", "Amoeba", ["Paramecium", "Euglena", "Plasmodium"]),
        ("Organisme uniseluler yang bergerak menggunakan rambut getar (silia) adalah ...", "Paramecium", ["Amoeba", "Euglena", "Bakteri"]),
        ("Organisme uniseluler yang bergerak menggunakan bulu cambuk (flagela) adalah ...", "Euglena", ["Amoeba", "Paramecium", "Jamur"]),
    ]
    for q_text, corr, dists in more_bio:
        if len(questions) >= 500:
            break
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan fakta dan konsep dasar ilmu biologi."))

    # Additional 210+ unique biology questions
    # A. Diet Classification for specific animals (60 distinct animals)
    herbivores = [
        "Sapi", "Kambing", "Domba", "Kuda", "Kelinci", "Gajah", "Jerapah", "Rusa", "Kancil", "Kerbau",
        "Unta", "Zebra", "Panda", "Koala", "Kangguru", "Badak", "Kuda nil", "Hamster", "Marmut", "Tapir"
    ]
    for animal in herbivores:
        add_q(build_mcq(
            "Biologi",
            f"Berdasarkan jenis makanannya, hewan {animal} tergolong dalam kelompok apa?",
            "Herbivora (pemakan tumbuhan)",
            ["Karnivora (pemakan daging)", "Omnivora (pemakan segala)", "Insektivora (pemakan serangga)"],
            f"{animal} memakan rumput atau bagian tumbuhan sehingga termasuk herbivora.",
            "Hewan ini memakan dedaunan, rumput, atau buah-buahan.",
        ))

    carnivores = [
        "Singa", "Harimau", "Serigala", "Burung elang", "Burung hantu", "Buaya", "Ikan hiu", "Komodo", "Citah", "Macan tutul",
        "Berang-berang laut", "Ikan piranha", "Ular piton", "Ular kobra", "Burung rajawali", "Burung bangau", "Anjing laut", "Paus orca", "Singa laut", "Kucing hutan"
    ]
    for animal in carnivores:
        add_q(build_mcq(
            "Biologi",
            f"Berdasarkan jenis makanannya, hewan {animal} tergolong dalam kelompok apa?",
            "Karnivora (pemakan daging)",
            ["Herbivora (pemakan tumbuhan)", "Omnivora (pemakan segala)", "Insektivora (pemakan serangga)"],
            f"{animal} memangsa hewan lain dan memakan daging sehingga tergolong karnivora.",
            "Hewan ini berburu mangsa dan memakan daging.",
        ))

    omnivores = [
        "Ayam", "Bebek", "Angsa", "Tikus", "Beruang hitam", "Babi hutan", "Monyet", "Simpanse", "Orangutan", "Musang",
        "Landak", "Kura-kura air tawar", "Burung gagak", "Burung jalak", "Ikan lele", "Ikan mujair", "Ikan nila", "Luwak", "Tupai", "Burung kutilang"
    ]
    for animal in omnivores:
        add_q(build_mcq(
            "Biologi",
            f"Berdasarkan jenis makanannya, hewan {animal} tergolong dalam kelompok apa?",
            "Omnivora (pemakan segala)",
            ["Herbivora (pemakan tumbuhan)", "Karnivora (pemakan daging)", "Insektivora (pemakan serangga)"],
            f"{animal} memakan tumbuhan sekaligus hewan kecil sehingga tergolong omnivora.",
            "Hewan ini memakan tumbuhan dan daging.",
        ))

    # B. Reproduction method for specific animals (50 distinct animals)
    viviparous = [
        "Kucing rumah", "Anjing peliharaan", "Kuda pacu", "Kelinci hias", "Lumba-lumba samudra",
        "Paus biru", "Kelelawar buah", "Kambing etawa", "Gajah sumatra", "Harimau jawa",
        "Singa afrika", "Monyet ekor panjang", "Rusa bawean", "Unta padang pasir", "Zebra afrika",
        "Jerapah sabana", "Beruang madu", "Serigala abu-abu", "Kera gibbon", "Sapi perah"
    ]
    for animal in viviparous:
        add_q(build_mcq(
            "Biologi",
            f"Hewan {animal} berkembang biak dengan cara apa?",
            "Melahirkan (Vivipar)",
            ["Bertelur (Ovipar)", "Bertelur-melahirkan (Ovovivipar)", "Membelah diri"],
            f"{animal} adalah mamalia yang berkembang biak dengan cara melahirkan (vivipar).",
            "Hewan ini mengandung anaknya dan menyusui.",
        ))

    oviparous = [
        "Ayam kampung", "Bebek petelur", "Burung merpati", "Burung merak", "Katak pohon",
        "Kodok buduk", "Ikan cupang", "Ikan mas koki", "Ikan gurame", "Penyu hijau",
        "Kura-kura darat", "Buaya muara", "Tokek rumah", "Cicak dinding", "Kadal kebun",
        "Nyamuk malaria", "Kupu-kupu raja", "Belalang sembah", "Capung jarum", "Semut rangrang"
    ]
    for animal in oviparous:
        add_q(build_mcq(
            "Biologi",
            f"Hewan {animal} berkembang biak dengan cara apa?",
            "Bertelur (Ovipar)",
            ["Melahirkan (Vivipar)", "Bertelur-melahirkan (Ovovivipar)", "Tunas vegetatif"],
            f"{animal} berkembang biak dengan mengeluarkan telur (ovipar).",
            "Induk hewan ini mengeluarkan telur yang kemudian menetas.",
        ))

    # C. Natural Habitats (40 distinct organisms)
    habitats = [
        ("Ikan hiu martil", "Laut lepas dan samudra"),
        ("Beruang kutub", "Hamparan es Kutub Utara"),
        ("Unta berpunuk satu", "Gurun pasir yang gersang"),
        ("Orangutan sumatra", "Hutan hujan tropis di pepohonan"),
        ("Katak sawah hijau", "Sawah dan rawa berlumpur"),
        ("Cacing tanah merah", "Tanah subur yang gembur dan lembap"),
        ("Burung maleo", "Pasir pantai vulkanik bersuhu hangat"),
        ("Bunga Rafflesia arnoldii", "Dasar hutan tropis menempel pada inang"),
        ("Pohon bakau (mangrove)", "Garis pantai berlumpur dan muara pasang surut"),
        ("Kaktus centong berduri", "Padang pasir tandus dan kering"),
        ("Bunga edelweiss jawa", "Lereng puncak pegunungan tinggi"),
        ("Bunga teratai putih", "Permukaan air danau atau kolam tenang"),
        ("Lumut kerak", "Bebatuan dan batang pohon yang lembap"),
        ("Ikan mas koki", "Kolam dan perairan air tawar tenang"),
        ("Burung cenderawasih", "Hutan belantara Pulau Papua"),
        ("Komodo", "Padang sabana Pulau Komodo dan Rinca"),
        ("Badak bercula satu", "Hutan dataran rendah Taman Nasional Ujung Kulon"),
        ("Singa afrika", "Padang rumput terbuka (sabana)"),
        ("Penguin kaisar", "Benua Antartika di kutub selatan"),
        ("Burung hantu serak jawa", "Gudang beras, pepohonan, dan atap rumah pada malam hari"),
        ("Ikan arwana", "Sungai berarus tenang di Kalimantan dan Papua"),
        ("Pohon cemara gunung", "Dataran tinggi dan lereng gunung yang sejuk"),
        ("Tanaman eceng gondok", "Rawa-rawa dan perairan tawar yang tenang"),
        ("Burung jalak bali", "Kawasan hutan kering Taman Nasional Bali Barat"),
        ("Lumba-lumba hidung botol", "Perairan laut pantai yang hangat"),
    ]
    for name, habitat in habitats:
        wrongs = [h[1] for h in habitats if h[1] != habitat][:3]
        add_q(build_mcq(
            "Biologi",
            f"Di manakah habitat alami tempat hidup dari {name}?",
            habitat,
            wrongs,
            f"{name} secara alami berhabitat di {habitat}.",
            "Pikirkan lingkungan asli tempat makhluk hidup ini ditemukan.",
        ))

    # D. More Genetics, Cells & General Biology Facts
    extra_concepts = [
        ("Berapa jumlah total kromosom pada sel tubuh manusia normal?", "46 buah (23 pasang)", ["44 buah", "48 buah", "23 buah"]),
        ("Berapa pasang kromosom seks (gonosom) yang menentukan jenis kelamin pada manusia?", "1 pasang (XX atau XY)", ["2 pasang", "22 pasang", "23 pasang"]),
        ("Pasangan kromosom seks yang dimiliki oleh seorang perempuan normal adalah ...", "XX", ["XY", "YY", "XO"]),
        ("Pasangan kromosom seks yang dimiliki oleh seorang laki-laki normal adalah ...", "XY", ["XX", "YY", "XO"]),
        ("Molekul pembawa informasi genetik yang diwariskan dari orang tua ke anak adalah ...", "DNA (Asam Deoksiribonukleat)", ["ATP", "Glukosa", "Klorofil"]),
        ("Bapak Genetika Dunia yang pertama kali meneliti hukum pewarisan sifat pada tanaman kacang kapri adalah ...", "Gregor Mendel", ["Charles Darwin", "Louis Pasteur", "Alexander Fleming"]),
        ("Tokoh yang mencetuskan teori evolusi melalui seleksi alam dalam bukunya The Origin of Species adalah ...", "Charles Darwin", ["Gregor Mendel", "Antonie van Leeuwenhoek", "Robert Hooke"]),
        ("Ilmuwan yang pertama kali melihat sel pada sayatan gabus menggunakan mikroskop sederhana adalah ...", "Robert Hooke", ["Charles Darwin", "Gregor Mendel", "Louis Pasteur"]),
        ("Ilmu biologi yang khusus mempelajari tentang hewan disebut ...", "Zoologi", ["Botani", "Mikologi", "Virologi"]),
        ("Ilmu biologi yang khusus mempelajari tentang tumbuhan disebut ...", "Botani", ["Zoologi", "Entomologi", "Mikrobiologi"]),
        ("Ilmu biologi yang khusus mempelajari tentang jamur disebut ...", "Mikologi", ["Zoologi", "Botani", "Bakteriologi"]),
        ("Ilmu biologi yang khusus mempelajari tentang serangga disebut ...", "Entomologi", ["Ornitologi", "Iktiologi", "Herpetologi"]),
        ("Ilmu biologi yang khusus mempelajari tentang burung disebut ...", "Ornitologi", ["Entomologi", "Mamalogi", "Mikologi"]),
        ("Ilmu biologi yang khusus mempelajari tentang ikan disebut ...", "Iktiologi", ["Ornitologi", "Entomologi", "Zoologi"]),
        ("Ilmu biologi yang khusus mempelajari tentang virus disebut ...", "Virologi", ["Bakteriologi", "Parasitologi", "Mikologi"]),
        ("Ilmu biologi yang khusus mempelajari tentang fungsi kerja organ dan sistem tubuh disebut ...", "Fisiologi", ["Anatomi", "Morfologi", "Histologi"]),
        ("Ilmu biologi yang mempelajari struktur letak organ-organ dalam tubuh makhluk hidup disebut ...", "Anatomi", ["Fisiologi", "Ekologi", "Genetika"]),
        ("Ilmu biologi yang mempelajari bentuk luar dan susunan fisik tubuh makhluk hidup disebut ...", "Morfologi", ["Anatomi", "Fisiologi", "Sitologi"]),
        ("Ilmu biologi yang khusus mempelajari tentang jaringan tubuh di bawah mikroskop adalah ...", "Histologi", ["Sitologi", "Morfologi", "Embriologi"]),
        ("Ilmu biologi yang mempelajari struktur dan fungsi sel disebut ...", "Sitologi", ["Histologi", "Ekologi", "Taksonomi"]),
    ]
    for q_text, corr, dists in extra_concepts:
        if len(questions) >= 500:
            break
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan cabang ilmu dan fakta biologi modern."))

    # E. More specific plant & animal facts to reach exactly 500
    respiration_specific = [
        ("Belalang sembah", "Sistem trakea"),
        ("Lumba-lumba hidung botol", "Paru-paru"),
        ("Ikan hiu martil", "Insang"),
        ("Cacing tanah merah", "Permukaan kulit lembap"),
        ("Burung elang", "Paru-paru dan pundi-pundi udara"),
        ("Ikan mas koki", "Insang"),
        ("Kecebong katak", "Insang luar"),
        ("Paus sperma", "Paru-paru"),
        ("Capung sawah", "Sistem trakea"),
        ("Buaya muara", "Paru-paru"),
        ("Nyamuk demam berdarah", "Sistem trakea"),
    ]
    for an_name, resp_org in respiration_specific:
        wrongs = [r[1] for r in respiration_specific if r[1] != resp_org][:3]
        add_q(build_mcq(
            "Biologi",
            f"Organ pernapasan utama pada hewan {an_name} adalah ...",
            resp_org,
            wrongs,
            f"{an_name} bernapas menggunakan {resp_org}.",
            "Pikirkan sistem pernapasan kelompok hewan tersebut.",
        ))

    plant_veggie = [
        ("Cocor bebek", "Tunas adventif pada daun"),
        ("Jahe merah", "Akar tinggal (Rizoma)"),
        ("Kunyit", "Akar tinggal (Rizoma)"),
        ("Bawang merah", "Umbi lapis"),
        ("Bawang putih", "Umbi lapis"),
        ("Kentang", "Umbi batang"),
        ("Ubi jalar", "Umbi batang"),
        ("Wortel", "Umbi akar"),
        ("Rumput teki", "Geragih (Stolon)"),
        ("Stroberi", "Geragih (Stolon)"),
        ("Tanaman pisang", "Tunas anakan"),
        ("Bambu kuning", "Tunas rebung"),
        ("Tumbuhan paku", "Spora"),
        ("Lumut daun", "Spora"),
    ]
    for pl_name, pl_veg in plant_veggie:
        wrongs = [v[1] for v in plant_veggie if v[1] != pl_veg][:3]
        add_q(build_mcq(
            "Biologi",
            f"Tanaman {pl_name} berkembang biak secara vegetatif alami menggunakan ...",
            pl_veg,
            wrongs,
            f"{pl_name} berkembang biak dengan {pl_veg}.",
            "Pikirkan organ perkembangbiakan vegetatif tumbuhan ini.",
        ))

    health_and_illness = [
        ("Kebiasaan membaca buku terlalu dekat dalam kondisi gelap dapat memicu gangguan penglihatan ...", "Miopi (Rabun jauh)", ["Hipermetropi (Rabun dekat)", "Katarak", "Presbiopi"]),
        ("Kacamata dengan lensa cekung (minus) digunakan untuk membantu penderita rabun ...", "Rabun jauh (Miopi)", ["Rabun dekat (Hipermetropi)", "Mata tua (Presbiopi)", "Katarak"]),
        ("Kacamata dengan lensa cembung (plus) digunakan untuk membantu penderita rabun ...", "Rabun dekat (Hipermetropi)", ["Rabun jauh (Miopi)", "Buta warna", "Astigmatisma"]),
        ("Gangguan penglihatan akibat lensa mata yang keruh karena proses penuaan disebut ...", "Katarak", ["Glaukoma", "Miopi", "Juling"]),
        ("Penyakit sesak napas akibat penyempitan saluran pernapasan yang dipicu alergi atau dingin adalah ...", "Asma", ["TBC", "Pneumonia", "Bronkitis"]),
        ("Penyakit peradangan pada umbai cacing (usus buntu) di perut kanan bawah disebut ...", "Apendisitis (Usus buntu)", ["Maag", "Diare", "Tifus"]),
        ("Penyakit peradangan pada lambung akibat tingginya produksi asam lambung berlebih disebut ...", "Gastritis (Maag)", ["Hepatitis", "Kolera", "Apendisitis"]),
        ("Gangguan buang air besar sulit dan keras akibat usus besar menyerap terlalu banyak air disebut ...", "Konstipasi (Sembelit)", ["Diare", "Maag", "Disentri"]),
        ("Buang air besar encer berkali-kali akibat infeksi kuman pada saluran cerna disebut ...", "Diare", ["Konstipasi", "Ambeien", "Radang tenggorokan"]),
        ("Hewan mamalia berkantung yang merawat anaknya di dalam kantung perut disebut golongan ...", "Marsupialia", ["Karnivora", "Rodentia", "Primata"]),
        ("Rambut kaku di sekitar moncong kucing yang sangat peka mendeteksi getaran dan navigasi gelap disebut ...", "Vibrisae (Kumis kucing)", ["Bulu pelindung", "Duri", "Antena"]),
        ("Bulu bebek tidak basah dan tetap mengapung di air karena dilapisi oleh zat ...", "Minyak alami dari kelenjar ekor", ["Lilin tebal", "Kapur", "Garam"]),
        ("Dalam ekosistem sawah, padi bertindak sebagai ...", "Produsen (penghasil makanan)", ["Konsumen tingkat 1", "Konsumen puncak", "Pengurai"]),
        ("Dalam ekosistem sawah, katak yang memangsa serangga belalang bertindak sebagai ...", "Konsumen tingkat II", ["Produsen", "Konsumen primer", "Pengurai"]),
        ("Organisme jamur dan bakteri pembusuk yang menguraikan bangkai makhluk hidup bertindak sebagai ...", "Dekomposer (Pengurai)", ["Produsen", "Konsumen sekunder", "Herbivora"]),
        ("Hewan avertebrata bertubuh lunak dan sering bercangkang seperti bekicot dan kerang termasuk filum ...", "Moluska", ["Arthropoda", "Porifera", "Echinodermata"]),
        ("Hewan dengan tubuh berpori-pori halus yang hidup menetap di dasar laut adalah ...", "Porifera (Spons laut)", ["Moluska", "Cnidaria", "Protozoa"]),
        ("Hewan berbuku-buku dengan 6 kaki (3 pasang) seperti semut dan lebah termasuk kelas ...", "Insekta (Serangga)", ["Arachnida", "Crustacea", "Myriapoda"]),
        ("Hewan berkaki 8 (4 pasang) seperti laba-laba dan kalajengking termasuk kelas ...", "Arachnida", ["Insekta", "Crustacea", "Myriapoda"]),
        ("Hewan berkaki sepuluh seperti udang dan kepiting termasuk kelas ...", "Crustacea (Udang-udangan)", ["Insekta", "Arachnida", "Moluska"]),
        ("Berapa pasang kaki yang dimiliki oleh seekor laba-laba?", "4 pasang (8 kaki)", ["3 pasang", "5 pasang", "6 pasang"]),
        ("Berapa pasang kaki yang dimiliki oleh seekor serangga seperti semut atau lalat?", "3 pasang (6 kaki)", ["4 pasang", "2 pasang", "5 pasang"]),
        ("Berapa pasang sayap yang dimiliki oleh seekor kupu-kupu?", "2 pasang (4 sayap)", ["1 pasang", "3 pasang", "Tanpa sayap"]),
        ("Pohon jati menggugurkan daunnya pada musim kemarau bertujuan untuk ...", "Mengurangi penguapan air (Meranggas)", ["Mempercepat fotosintesis", "Membunuh hama daun", "Menyerap air tanah"]),
        ("Tumbuhan kantong semar menjebak serangga bertujuan untuk memenuhi kebutuhan zat ...", "Nitrogen", ["Glukosa", "Kalsium", "Air"]),
        ("Lapisan lilin pada permukaan daun talas dan teratai berfungsi untuk ...", "Mencegah daun membusuk akibat air", ["Menarik serangga", "Mempercepat penguapan", "Menyerap sinar matahari"]),
        ("Hewan yang aktif mencari makan pada malam hari dan beristirahat di siang hari disebut hewan ...", "Nokturnal", ["Diurnal", "Karnivora", "Herbivora"]),
        ("Hewan yang aktif beraktivitas pada siang hari disebut kelompok hewan ...", "Diurnal", ["Nokturnal", "Amfibi", "Reptil"]),
        ("Contoh hewan nokturnal yang aktif mencari makan di kegelapan malam adalah ...", "Burung hantu dan kelelawar", ["Ayam dan bebek", "Kuda dan sapi", "Kupu-kupu dan burung pipit"]),
        ("Lumba-lumba dan paus menghirup udara di permukaan laut melalui lubang pernapasan di atas kepala bernama ...", "Blowhole (Lubang sembur)", ["Insang", "Kloaka", "Trakea"]),
        ("Organ pencernaan pada burung yang berfungsi menyimpan makanan sementara sebelum dicerna adalah ...", "Tembolok", ["Empedal", "Usus besar", "Hati"]),
        ("Bagian lambung burung yang tebal berotot dan sering berisi kerikil kecil untuk melumatkan biji adalah ...", "Empedal (Ampela)", ["Tembolok", "Kerongkongan", "Pankreas"]),
        ("Hewan pemamah biak (ruminansia) seperti sapi memiliki lambung yang terbagi menjadi ...", "4 ruangan (Rumen, Retikulum, Omasum, Abomasum)", ["2 ruangan", "3 ruangan", "5 ruangan"]),
        ("Proses mengunyah kembali makanan dari lambung ke mulut pada waktu istirahat pada sapi disebut ...", "Memamah biak", ["Menggiling", "Mencerna kimiawi", "Menelan"]),
        ("Penyakit gondok disebabkan oleh pembengkakan pada kelenjar ...", "Tiroid di bagian leher", ["Pankreas di perut", "Adrenal di ginjal", "Hipofisis di otak"]),
        ("Hormon yang memicu detak jantung berdegup kencang saat seseorang kaget atau takut adalah ...", "Hormon Adrenalin", ["Hormon Insulin", "Hormon Tiroksin", "Hormon Melatonin"]),
    ]
    for q_text, corr, dists in health_and_illness:
        if len(questions) >= 500:
            break
        add_q(build_mcq("Biologi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami konsep kesehatan organ dan rantai makanan."))

    return questions[:500]
