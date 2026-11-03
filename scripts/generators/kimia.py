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

    # 1. Lambang Unsur Kimia & Tabel Periodik (70 soal)
    elements_facts = [
        ("Zat tunggal yang paling sederhana dan tidak dapat diuraikan lagi menjadi zat lain melalui reaksi kimia biasa disebut ...", "Unsur", ["Senyawa", "Campuran", "Larutan"]),
        ("Unsur kimia paling ringan dan paling melimpah di jagat raya yang memiliki lambang huruf 'H' adalah ...", "Hidrogen", ["Helium", "Oksigen", "Nitrogen"]),
        ("Gas mulia ringan yang tidak mudah terbakar dengan lambang unsur 'He' yang digunakan mengisi balon udara adalah ...", "Helium", ["Hidrogen", "Neon", "Argon"]),
        ("Unsur non-logam yang menjadi penyusun utama seluruh makhluk hidup dan senyawa organik dengan lambang 'C' adalah ...", "Karbon", ["Kalsium", "Klorin", "Kobalt"]),
        ("Unsur gas yang menyusun sekitar 78% volume atmosfer bumi dengan lambang unsur 'N' adalah ...", "Nitrogen", ["Natrium", "Nikel", "Neon"]),
        ("Unsur gas di atmosfer yang sangat penting untuk pernapasan dan pembakaran dengan lambang 'O' adalah ...", "Oksigen", ["Ozon", "Osmium", "Oksalat"]),
        ("Logam alkali yang sangat reaktif dengan air dan memiliki lambang kimia 'Na' adalah ...", "Natrium (Sodium)", ["Nitrogen", "Nikel", "Neon"]),
        ("Logam alkali tanah yang banyak terkandung dalam susu dan bermanfaat memperkuat tulang dan gigi dengan lambang 'Ca' adalah ...", "Kalsium", ["Karbon", "Kalium", "Kadmium"]),
        ("Unsur logam alkali yang penting untuk fungsi otot dan saraf tubuh dengan lambang kimia 'K' adalah ...", "Kalium (Potassium)", ["Kalsium", "Kromium", "Klorin"]),
        ("Logam ringan yang tahan karat dan banyak digunakan sebagai perabot dapur dengan lambang 'Al' adalah ...", "Aluminium", ["Perak", "Besi", "Emas"]),
        ("Unsur logam keras yang memiliki lambang kimia 'Fe' (Ferrum) adalah ...", "Besi", ["Tembaga", "Emas", "Timah"]),
        ("Unsur logam berwarna kemerahan pengantar listrik kabel terbaik dengan lambang 'Cu' (Cuprum) adalah ...", "Tembaga", ["Kuningan", "Perunggu", "Besi"]),
        ("Logam mulia berharga mahal berwarna kuning mengilap dengan lambang 'Au' (Aurum) adalah ...", "Emas", ["Perak", "Platina", "Tembaga"]),
        ("Logam mulia berkilau putih yang memiliki lambang kimia 'Ag' (Argentum) adalah ...", "Perak", ["Aluminium", "Seng", "Baja"]),
        ("Logam berat cair berwarna perak pada suhu ruang yang ada di dalam termometer dengan lambang 'Hg' (Hydrargyrum) adalah ...", "Air Raksa (Merkuri)", ["Timbel", "Timah", "Perak"]),
        ("Unsur logam pelindung karat dengan lambang kimia 'Zn' (Zincum) adalah ...", "Seng (Zinc)", ["Timah", "Nikel", "Tembaga"]),
        ("Logam lunak yang digunakan sebagai bahan pelapis kaleng makanan dengan lambang 'Sn' (Stannum) adalah ...", "Timah", ["Besi", "Aluminium", "Tembaga"]),
        ("Logam berat beracun berwarna abu-abu kebiruan dengan lambang kimia 'Pb' (Plumbum) adalah ...", "Timbal (Timbel / Timah hitam)", ["Timah putih", "Seng", "Nikel"]),
        ("Logam keras tahan karat yang digunakan untuk koin dan baterai dengan lambang kimia 'Ni' adalah ...", "Nikel", ["Natrium", "Nitrogen", "Neon"]),
        ("Unsur non-logam berwarna kuning menyengat dari kawah gunung berapi dengan lambang 'S' (Sulfur) adalah ...", "Belerang", ["Silikon", "Selenium", "Fosfor"]),
        ("Unsur halogen berwujud gas kehijauan yang digunakan sebagai desinfektan kaporit air dengan lambang 'Cl' adalah ...", "Klorin (Klor)", ["Kalsium", "Karbon", "Kromium"]),
        ("Unsur halogen yang penting untuk mencegah penyakit gondok dengan lambang kimia 'I' adalah ...", "Iodin (Yodium)", ["Besi", "Seng", "Kalsium"]),
        ("Unsur halogen berwujud cairan cokelat kemerahan dengan lambang kimia 'Br' adalah ...", "Bromin (Brom)", ["Barium", "Boron", "Berilium"]),
        ("Unsur gas mulia yang memancarkan pendar cahaya merah oranye terang pada lampu reklame dengan lambang 'Ne' adalah ...", "Neon", ["Argon", "Helium", "Kripton"]),
        ("Unsur gas mulia yang banyak digunakan untuk mengisi ruang dalam lampu bohlam dengan lambang 'Ar' adalah ...", "Argon", ["Neon", "Helium", "Kripton"]),
        ("Unsur metaloid yang banyak digunakan sebagai bahan utama pembuatan komponen mikrochip komputer dengan lambang 'Si' adalah ...", "Silikon", ["Belerang", "Karbon", "Bauksit"]),
        ("Unsur non-logam yang dapat bersinar dalam gelap dan terdapat pada korek api dengan lambang 'P' adalah ...", "Fosfor", ["Fluor", "Belerang", "Kalium"]),
        ("Unsur halogen paling elektronegatif yang sering ditambahkan pada pasta gigi untuk menguatkan email gigi dengan lambang 'F' adalah ...", "Fluorin (Fluor)", ["Fosfor", "Besi", "Klorin"]),
        ("Logam alkali tanah yang ringan dan terbakar menghasilkan nyala putih sangat menyilaukan dengan lambang 'Mg' adalah ...", "Magnesium", ["Mangan", "Kalsium", "Natrium"]),
        ("Unsur logam keras pembuat baja tahan karat (stainless steel) dengan lambang kimia 'Cr' adalah ...", "Kromium (Krom)", ["Kobalt", "Tembaga", "Kalsium"]),
        ("Tabel susunan seluruh unsur kimia berdasarkan kenaikan nomor atom dan kemiripan sifatnya dinamakan ...", "Tabel Periodik Unsur", ["Tabel Logam", "Tabel Valensi", "Diagram Alir"]),
        ("Ilmuwan asal Rusia yang dikenal sebagai penemu dan perancang sistem tabel periodik unsur modern adalah ...", "Dmitri Mendeleev", ["Antoine Lavoisier", "John Dalton", "Ernest Rutherford"]),
        ("Baris-baris mendatar (horizontal) pada tabel periodik unsur dinamakan ...", "Periode", ["Golongan", "Blok", "Deret"]),
        ("Kolom-kolom tegak (vertikal) pada tabel periodik unsur yang memiliki kemiripan sifat kimia dinamakan ...", "Golongan", ["Periode", "Keluarga", "Siklus"]),
        ("Kelompok unsur pada Golongan VIII-A (Golongan 18) yang sangat stabil dan sukar bereaksi disebut unsur ...", "Gas Mulia", ["Logam Alkali", "Halogen", "Alkali Tanah"]),
        ("Kelompok unsur pada Golongan I-A (kecuali hidrogen) yang sangat reaktif dan mudah melepaskan 1 elektron dinamakan ...", "Logam Alkali", ["Logam Alkali Tanah", "Halogen", "Gas Mulia"]),
        ("Kelompok unsur pada Golongan II-A seperti Mg dan Ca dinamakan golongan ...", "Logam Alkali Tanah", ["Logam Alkali", "Halogen", "Gas Mulia"]),
        ("Kelompok unsur pada Golongan VII-A seperti F, Cl, Br, dan I dinamakan golongan ...", "Halogen (Pembentuk garam)", ["Gas Mulia", "Alkali", "Aktinida"]),
        ("Unsur-unsur logam yang berada di bagian tengah tabel periodik (Golongan B) dinamakan logam ...", "Transisi", ["Alkali", "Aktinida", "Lantanida"]),
        ("Nomor atom pada suatu unsur kimia menunjukkan jumlah ...", "Proton di dalam inti atom", ["Neutron", "Massa total", "Kulit atom"]),
        ("Pada atom netral yang tidak bermuatan, jumlah proton selalu sama dengan jumlah ...", "Elektron", ["Neutron", "Kulit atom", "Valensi"]),
        ("Nomor massa suatu atom diperoleh dari hasil penjumlahan antara jumlah ...", "Proton dan Neutron di dalam inti atom", ["Proton dan Elektron", "Elektron dan Neutron", "Kulit atom dan proton"]),
        ("Atom-atom dari unsur yang sama yang memiliki nomor atom sama tetapi memiliki nomor massa berbeda dinamakan ...", "Isotop", ["Isobar", "Isoton", "Isomer"]),
        ("Atom-atom yang memiliki nomor massa sama tetapi memiliki nomor atom berbeda dinamakan ...", "Isobar", ["Isotop", "Isoton", "Alotrop"]),
        ("Atom-atom dari unsur berbeda yang memiliki jumlah neutron yang sama di dalam intinya disebut ...", "Isoton", ["Isotop", "Isobar", "Isomer"]),
        ("Bentuk-bentuk struktur kristal yang berbeda dari unsur yang sama seperti intan dan grafit dinamakan ...", "Alotrop karbon", ["Isotop", "Isomer", "Polimer"]),
        ("Zat alami paling keras di muka bumi yang tersusun murni dari atom karbon adalah ...", "Intan (Berlian)", ["Grafit", "Baja", "Batu giok"]),
        ("Mineral lunak berwarna hitam kelabu penyusun mata pensil yang juga tersusun dari atom karbon murni adalah ...", "Grafit", ["Intan", "Batu bara", "Belerang"]),
    ]
    for q_text, corr, dists in elements_facts:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami lambang unsur kimia, sistem periodik, dan nomor atom."))

    # 2. Rumus Kimia Zat & Senyawa Sehari-hari (60 soal)
    formulas_facts = [
        ("Zat tunggal yang terbentuk dari gabungan dua atau lebih unsur kimia berbeda melalui ikatan kimia dinamakan ...", "Senyawa", ["Unsur", "Campuran", "Larutan"]),
        ("Rumus kimia untuk molekul air murni adalah ...", "H2O", ["H2O2", "HO", "O2H"]),
        ("Molekul air murni (H2O) tersusun dari dua atom hidrogen dan satu atom ...", "Oksigen", ["Nitrogen", "Karbon", "Helium"]),
        ("Rumus kimia untuk garam dapur yang biasa digunakan sebagai bumbu masak adalah ...", "NaCl (Natrium Klorida)", ["NaOH", "KCl", "NaHCO3"]),
        ("Garam dapur (NaCl) tersusun atas gabungan ion natrium dan ion ...", "Klorida (Klorin)", ["Kalium", "Kalsium", "Sulfat"]),
        ("Rumus kimia dari gas karbon dioksida yang dikeluarkan saat manusia menghembuskan napas adalah ...", "CO2", ["CO", "C2O", "CH4"]),
        ("Gas beracun tak berwarna dan tak berbau hasil pembakaran mesin kendaraan yang tidak sempurna adalah ...", "CO (Karbon Monoksida)", ["CO2", "SO2", "NO2"]),
        ("Rumus kimia untuk gas oksigen bebas yang kita hirup sehari-hari adalah ...", "O2", ["O", "O3", "O4"]),
        ("Molekul gas yang tersusun atas tiga atom oksigen dan berfungsi menyaring radiasi UV matahari adalah ...", "O3 (Ozon)", ["O2", "CO2", "H2O2"]),
        ("Rumus kimia untuk senyawa glukosa atau gula darah adalah ...", "C6H12O6", ["C12H22O11", "CH4", "C2H5OH"]),
        ("Rumus kimia untuk senyawa sukrosa yang merupakan gula pasir putih dari tebu adalah ...", "C12H22O11", ["C6H12O6", "CH3COOH", "NaCl"]),
        ("Rumus kimia untuk asam asetat yang terkandung dalam cuka makan di dapur adalah ...", "CH3COOH", ["HCl", "H2SO4", "HNO3"]),
        ("Rumus kimia dari soda kue (baking soda) yang membuat adonan roti mengembang adalah ...", "NaHCO3 (Natrium Bikarbonat)", ["Na2CO3", "NaOH", "NaCl"]),
        ("Rumus kimia untuk soda abu yang sering digunakan dalam deterjen pembersih adalah ...", "Na2CO3 (Natrium Karbonat)", ["NaHCO3", "NaOH", "NaCl"]),
        ("Rumus kimia untuk soda api (kaustik) yang digunakan untuk melancarkan saluran pipa wastafel mampet adalah ...", "NaOH (Natrium Hidroksida)", ["KOH", "Ca(OH)2", "NaHCO3"]),
        ("Rumus kimia dari asam klorida yang menjadi asam lambung pencerna makanan adalah ...", "HCl", ["H2SO4", "HNO3", "HF"]),
        ("Rumus kimia dari asam sulfat pekat yang digunakan sebagai cairan pengisi aki (akumulator) motor adalah ...", "H2SO4", ["HCl", "H2CO3", "HNO3"]),
        ("Rumus kimia dari kalsium karbonat yang merupakan penyusun utama batu kapur, marmer, dan cangkang kerang adalah ...", "CaCO3", ["CaO", "Ca(OH)2", "CaCl2"]),
        ("Batu gamping mentah yang dipanggang menghasilkan kapur tohor dengan rumus kimia ...", "CaO (Kalsium Oksida)", ["CaCO3", "Ca(OH)2", "CaSO4"]),
        ("Kapur tohor yang disiram air menghasilkan kapur sirih (air kapur padam) dengan rumus kimia ...", "Ca(OH)2 (Kalsium Hidroksida)", ["CaO", "CaCO3", "CaCl2"]),
        ("Senyawa gips yang digunakan untuk membalut tulang yang patah adalah kalsium sulfat dengan rumus ...", "CaSO4", ["CaCO3", "CaCl2", "CaO"]),
        ("Rumus kimia untuk gas metana yang menjadi komponen utama gas alam dan biogas adalah ...", "CH4", ["C2H6", "C3H8", "C4H10"]),
        ("Rumus kimia untuk gas propana yang menjadi komponen utama gas elpiji (LPG) tabung melon adalah ...", "C3H8", ["CH4", "C4H10", "C2H6"]),
        ("Rumus kimia untuk gas butana yang juga terkandung dalam tabung gas elpiji adalah ...", "C4H10", ["C3H8", "CH4", "C5H12"]),
        ("Rumus kimia untuk senyawa alkohol jenis etanol yang terdapat pada antiseptik pembersih tangan adalah ...", "C2H5OH", ["CH3OH", "C3H7OH", "C6H12O6"]),
        ("Alkohol jenis metanol (spiritus) sangat beracun dan tidak boleh dikonsumsi karena dapat menyebabkan kebutaan memiliki rumus ...", "CH3OH", ["C2H5OH", "CH4", "H2O2"]),
        ("Cairan antiseptik pembersih luka yang menghasilkan busa gelembung oksigen saat terkena darah adalah hidrogen peroksida dengan rumus ...", "H2O2", ["H2O", "HO", "H2SO4"]),
        ("Gas berbau menyengat yang menjadi bahan baku utama pembuatan pupuk urea adalah amonia dengan rumus ...", "NH3", ["NO2", "N2O", "NH4Cl"]),
        ("Rumus kimia untuk pupuk urea yang banyak digunakan petani menyuburkan tanaman padi adalah ...", "CO(NH2)2", ["NH3", "NH4NO3", "(NH4)2SO4"]),
        ("Gas yang sering dijuluki 'gas gelak' atau obat bius kedokteran gigi adalah dinitrogen monoksida dengan rumus ...", "N2O", ["NO", "NO2", "NH3"]),
        ("Asam nitrat yang banyak digunakan dalam industri pembuatan bahan peledak dan pupuk memiliki rumus ...", "HNO3", ["HCl", "H2SO4", "H3PO4"]),
        ("Asam fosfat yang sering ditambahkan sebagai pengatur keasaman pada minuman bersoda (cola) memiliki rumus ...", "H3PO4", ["H2SO4", "HNO3", "HCl"]),
        ("Zat pemutih pakaian cair (klorin pemutih) mengandung senyawa aktif natrium hipoklorit dengan rumus ...", "NaOCl", ["NaCl", "NaClO3", "NaOH"]),
        ("Karbit yang digunakan oleh tukang las untuk menghasilkan gas asetilena memiliki nama kimia kalsium karbida dengan rumus ...", "CaC2", ["CaCO3", "CaO", "CaCl2"]),
        ("Gas asetilena (etuna) yang dihasilkan saat karbit disiram air dan terbakar dengan nyala api sangat panas memiliki rumus ...", "C2H2", ["CH4", "C2H4", "C2H6"]),
        ("Kapur barus yang biasa digunakan sebagai pengharum lemari pakaian memiliki nama kimia naftalena dengan rumus ...", "C10H8", ["C6H6", "CH4", "C8H18"]),
    ]
    for q_text, corr, dists in formulas_facts:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami rumus kimia senyawa penting dalam kehidupan sehari-hari."))

    # 3. Asam, Basa, Garam & Skala pH (60 soal)
    acids_and_bases = [
        ("Larutan yang memiliki derajat keasaman dengan nilai pH lebih kecil dari 7 (pH < 7) tergolong larutan ...", "Asam", ["Basa", "Netral", "Garam"]),
        ("Larutan yang memiliki nilai pH tepat sama dengan 7 (pH = 7) seperti air murni tergolong larutan ...", "Netral", ["Asam", "Basa", "Keras"]),
        ("Larutan yang memiliki nilai pH lebih besar dari 7 (pH > 7) tergolong larutan ...", "Basa (Alkali)", ["Asam", "Netral", "Organik"]),
        ("Ciri khas dari larutan yang bersifat asam jika dicicipi memiliki rasa ...", "Masam", ["Pahit", "Manis", "Asin"]),
        ("Ciri khas dari larutan yang bersifat basa jika dicicipi berasa pahit dan jika terkena kulit terasa ...", "Licin seperti sabun", ["Perih terbakar", "Lengket", "Kasar"]),
        ("Kertas lakmus biru jika dicelupkan ke dalam larutan asam akan berubah warna menjadi ...", "Merah", ["Tetap biru", "Kuning", "Hijau"]),
        ("Kertas lakmus merah jika dicelupkan ke dalam larutan basa akan berubah warna menjadi ...", "Biru", ["Tetap merah", "Kuning", "Ungu"]),
        ("Kertas lakmus merah dan lakmus biru tidak akan berubah warna jika dicelupkan ke dalam larutan yang bersifat ...", "Netral", ["Asam kuat", "Basa kuat", "Asam lemah"]),
        ("Asam alami yang banyak terkandung di dalam buah jeruk, lemon, dan jeruk nipis adalah ...", "Asam sitrat", ["Asam asetat", "Asam format", "Asam laktat"]),
        ("Asam yang terkandung di dalam buah apel yang belum matang adalah ...", "Asam malat", ["Asam sitrat", "Asam format", "Asam askorbat"]),
        ("Asam yang terkandung di dalam buah anggur adalah ...", "Asam tartrat", ["Asam sitrat", "Asam asetat", "Asam format"]),
        ("Asam yang terkandung di dalam susu yang telah basi atau produk keju dan yogurt adalah ...", "Asam laktat", ["Asam sitrat", "Asam butirat", "Asam asetat"]),
        ("Asam yang disuntikkan oleh gigitan semut merah atau sengatan lebah madu yang menimbulkan rasa gatal perih adalah ...", "Asam format (Asam semut)", ["Asam sitrat", "Asam cuka", "Asam klorida"]),
        ("Vitamin C yang penting untuk menjaga daya tahan tubuh memiliki nama kimia asam ...", "Asam askorbat", ["Asam folat", "Asam sitrat", "Asam amino"]),
        ("Vitamin B9 yang sangat penting bagi ibu hamil untuk perkembangan janin adalah asam ...", "Asam folat", ["Asam askorbat", "Asam retinoat", "Asam laktat"]),
        ("Asam lemak omega-3 yang banyak terkandung di dalam minyak ikan salmon dan tuna baik untuk kecerdasan otak dinamakan ...", "DHA dan EPA", ["Asam sitrat", "Asam format", "Asam asetat"]),
        ("Obat sakit maag (antasida) bekerja menetralkan kelebihan asam lambung karena mengandung zat yang bersifat basa yaitu ...", "Magnesium hidroksida dan Aluminium hidroksida", ["Asam sulfat pekat", "Natrium klorida", "Asam asetat"]),
        ("Reaksi kimia antara senyawa asam dengan senyawa basa yang menghasilkan garam dan air dinamakan reaksi ...", "Netralisasi (Penetralan)", ["Oksidasi", "Reduksi", "Fermentasi"]),
        ("Contoh indikator asam-basa alami yang terbuat dari tumbuhan dan berubah warna merah pekat di asam dan kuning di basa adalah ...", "Kunyit", ["Bawang putih", "Minyak goreng", "Garam"]),
        ("Indikator alami dari sayuran yang berubah menjadi merah terang di asam dan hijau/kuning di basa adalah ...", "Ekstrak kol ungu (kubis ungu)", ["Wortel", "Kentang", "Tauge"]),
        ("Larutan pembersih lantai dan sabun mandi di rumah tangga pada umumnya bersifat ...", "Basa", ["Asam", "Netral", "Garam murni"]),
        ("Air aki (accu zuur) yang digunakan pada baterai basah sepeda motor bersifat ...", "Asam kuat (pH sangat rendah sekitar 1)", ["Basa kuat", "Netral", "Asam lemah"]),
        ("Minuman teh manis, kopi hitam, dan jus jeruk pada umumnya memiliki sifat larutan ...", "Asam lemah", ["Basa kuat", "Netral sempurna", "Basa lemah"]),
        ("Darah manusia yang sehat memiliki nilai pH sedikit basa yang berkisar antara ...", "7,35 hingga 7,45", ["5,0 hingga 6,0", "8,5 hingga 9,5", "4,0 hingga 5,0"]),
        ("Air laut di samudra pada umumnya memiliki pH sedikit basa dengan nilai berkisar sekitar ...", "8,0 hingga 8,2", ["5,5", "6,0", "12,0"]),
        ("Fenomena hujan asam di daerah industri terjadi jika air hujan memiliki nilai pH di bawah ...", "5,6", ["7,0", "8,0", "9,0"]),
        ("Penyebab utama terjadinya hujan asam adalah pencemaran udara oleh gas buang pabrik berupa gas ...", "Sulfur dioksida (SO2) dan Nitrogen oksida (NOx)", ["Karbon monoksida dan uap air", "Gas helium dan argon", "Gas oksigen murni"]),
        ("Petani menaburkan bubuk kapur pertanian (dolomit / kalsium karbonat) pada lahan sawah bertujuan untuk ...", "Mengurangi tingkat keasaman tanah sawah agar netral kembali", ["Membunuh semua tanaman", "Membuat tanah jadi asin", "Menyerap air hujan"]),
        ("Asam kuat yang terionisasi sempurna di dalam air contohnya adalah ...", "HCl, H2SO4, dan HNO3", ["CH3COOH dan H2CO3", "H2O dan NaCl", "NaOH dan KOH"]),
        ("Basa kuat yang terionisasi sempurna di dalam air contohnya adalah ...", "NaOH dan KOH", ["NH4OH dan Mg(OH)2", "HCl dan H2SO4", "CH3COOH"]),
        ("Zat yang dapat mempertahankan nilai pH larutan agar tidak mudah berubah drastis saat ditambah sedikit asam atau basa disebut larutan ...", "Penyangga (Buffer)", ["Jenuh", "Koloid", "Elektrolit kuat"]),
    ]
    for q_text, corr, dists in acids_and_bases:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami konsep asam, basa, nilai pH, lakmus, dan reaksi netralisasi."))

    # 4. Struktur Atom & Ikatan Kimia (50 soal)
    atomic_structure = [
        ("Partikel subatom penyusun inti atom yang memiliki muatan listrik positif adalah ...", "Proton", ["Elektron", "Neutron", "Foton"]),
        ("Partikel subatom yang bermuatan listrik negatif dan bergerak mengelilingi inti atom pada kulit atom adalah ...", "Elektron", ["Proton", "Neutron", "Positron"]),
        ("Partikel di dalam inti atom yang tidak memiliki muatan listrik (netral) adalah ...", "Neutron", ["Proton", "Elektron", "Kation"]),
        ("Tokoh ilmuwan yang pertama kali mengemukakan teori atom modern berbentuk bola pejal padat adalah ...", "John Dalton", ["J.J. Thomson", "Ernest Rutherford", "Niels Bohr"]),
        ("Tokoh penemu partikel elektron melalui percobaan tabung sinar katode adalah ...", "J.J. Thomson", ["Ernest Rutherford", "James Chadwick", "John Dalton"]),
        ("Model atom yang mengibaratkan elektron tersebar di dalam bola bermuatan positif seperti kismis di dalam roti adalah model atom ...", "Roti Kismis (J.J. Thomson)", ["Tata Surya (Niels Bohr)", "Bola Pejal (Dalton)", "Mekanika Kuantum"]),
        ("Tokoh ilmuwan yang membuktikan bahwa sebagian besar ruang atom adalah ruang hampa dan memiliki inti atom sangat kecil dan padat adalah ...", "Ernest Rutherford", ["J.J. Thomson", "Niels Bohr", "John Dalton"]),
        ("Percobaan terkenal yang dilakukan oleh Ernest Rutherford untuk menemukan inti atom adalah ...", "Penembakan lempeng emas tipis dengan partikel alfa", ["Percobaan tetes minyak", "Tabung sinar katode", "Eksperimen difraksi"]),
        ("Tokoh penemu partikel neutron di dalam inti atom pada tahun 1932 adalah ...", "James Chadwick", ["Ernest Rutherford", "Niels Bohr", "J.J. Thomson"]),
        ("Model atom yang menyatakan bahwa elektron beredar mengelilingi inti atom pada lintasan atau tingkat energi tertentu (kulit atom) dirumuskan oleh ...", "Niels Bohr", ["John Dalton", "J.J. Thomson", "Max Planck"]),
        ("Kulit atom yang letaknya paling dekat dengan inti atom dinamakan kulit ...", "Kulit K (n = 1)", ["Kulit L", "Kulit M", "Kulit N"]),
        ("Jumlah elektron maksimum yang dapat ditampung pada kulit atom pertama (kulit K) adalah ...", "2 elektron (rumus 2n^2)", ["8 elektron", "18 elektron", "32 elektron"]),
        ("Jumlah elektron maksimum yang dapat ditampung pada kulit kedua (kulit L) adalah ...", "8 elektron", ["2 elektron", "18 elektron", "32 elektron"]),
        ("Jumlah elektron maksimum yang dapat ditampung pada kulit ketiga (kulit M) adalah ...", "18 elektron", ["8 elektron", "2 elektron", "32 elektron"]),
        ("Elektron-elektron yang berada pada kulit terluar dari suatu atom dinamakan elektron ...", "Valensi", ["Inti", "Bebas", "Eksitasi"]),
        ("Elektron valensi suatu atom sangat menentukan ...", "Sifat kimia dan kecenderungan pembentukan ikatan kimia", ["Massa atom total", "Warna zat", "Titik didih"]),
        ("Kaidah oktet menyatakan bahwa atom-atom cenderung berikatan untuk mencapai konfigurasi elektron stabil sebanyak ...", "8 elektron pada kulit terluar (seperti gas mulia)", ["2 elektron", "10 elektron", "18 elektron"]),
        ("Kaidah duplet kestabilan 2 elektron kulit terluar dicapai oleh unsur hidrogen dan ...", "Helium (He)", ["Neon", "Argon", "Kripton"]),
        ("Atom yang kehilangan atau melepaskan elektron sehingga bermuatan listrik positif dinamakan ...", "Kation (Ion positif)", ["Anion", "Molekul", "Isotop"]),
        ("Atom yang menangkap atau menerima elektron tambahan sehingga bermuatan listrik negatif dinamakan ...", "Anion (Ion negatif)", ["Kation", "Radikal", "Netron"]),
        ("Ikatan kimia yang terbentuk akibat adanya serah terima elektron antara atom logam (melepas) dan non-logam (menerima) disebut ...", "Ikatan ionik (Elektrovalen)", ["Ikatan kovalen", "Ikatan logam", "Ikatan hidrogen"]),
        ("Contoh senyawa yang terbentuk melalui ikatan ionik adalah ...", "NaCl (Garam dapur) dan CaO", ["H2O (Air)", "CH4 (Metana)", "CO2"]),
        ("Ciri khas dari senyawa berikatan ionik antara lain titik leleh dan titik didihnya sangat tinggi serta lelehannya dapat ...", "Menghantarkan arus listrik (Elektrolit)", ["Tidak larut di air", "Mudah menguap", "Berwujud gas"]),
        ("Ikatan kimia yang terbentuk melalui pemakaian bersama pasangan elektron oleh dua atom non-logam disebut ikatan ...", "Kovalen", ["Ionik", "Logam", "Van der Waals"]),
        ("Contoh molekul yang terbentuk melalui ikatan kovalen adalah ...", "H2O, CH4, CO2, dan NH3", ["NaCl dan KCl", "MgO dan CaF2", "LiCl dan KBr"]),
        ("Ikatan kovalen tunggal terjadi jika dua atom saling berbagi ...", "1 pasang elektron (2 elektron)", ["2 pasang elektron", "3 pasang elektron", "4 elektron"]),
        ("Molekul gas oksigen (O2) diikat oleh jenis ikatan kovalen ...", "Kovalen rangkap dua (2 pasang elektron)", ["Kovalen tunggal", "Kovalen rangkap tiga", "Ikatan ionik"]),
        ("Molekul gas nitrogen (N2) yang sangat kuat dan stabil diikat oleh jenis ikatan ...", "Kovalen rangkap tiga (3 pasang elektron)", ["Kovalen tunggal", "Kovalen rangkap dua", "Ikatan hidrogen"]),
        ("Ikatan kovalen di mana pasangan elektron ikatan yang digunakan bersama hanya disumbangkan oleh salah satu atom disebut ikatan ...", "Kovalen koordinasi (Datif)", ["Kovalen murni", "Ikatan ion", "Ikatan logam"]),
        ("Gaya tarik elektrostatik antara awan elektron bebas yang bergerak bebas mengelilingi kation-kation logam dinamakan ...", "Ikatan logam", ["Ikatan ion", "Ikatan kovalen", "Ikatan hidrogen"]),
        ("Adanya lautan elektron bebas pada ikatan logam menjelaskan mengapa logam bersifat ...", "Penghantar panas dan listrik yang sangat baik serta mudah ditempa", ["Sangat rapuh mudah hancur", "Tidak dapat menghantar listrik", "Selalu berwujud gas"]),
        ("Ikatan antarmolekul yang terbentuk antara atom hidrogen dengan atom yang sangat elektronegatif (F, O, N) dinamakan ...", "Ikatan hidrogen", ["Ikatan kovalen", "Ikatan Van der Waals", "Gaya London"]),
        ("Adanya ikatan hidrogen yang kuat antarmolekul air menyebabkan air memiliki titik didih yang relatif ...", "Tinggi (100 derajat C) dibanding senyawa hidrida segolongannya", ["Sangat rendah di bawah nol", "Nol derajat", "Sama dengan metana"]),
    ]
    for q_text, corr, dists in atomic_structure:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami partikel atom, konfigurasi elektron, ikatan ionik, dan kovalen."))

    # 5. Campuran, Larutan & Metode Pemisahan (60 soal)
    mixtures_and_separation = [
        ("Materi yang terbentuk dari gabungan dua zat atau lebih tanpa melalui reaksi kimia dan perbandingan komponennya sembarang disebut ...", "Campuran", ["Senyawa", "Unsur", "Molekul murni"]),
        ("Campuran yang serba sama di setiap bagian sehingga zat-zat penyusunnya tidak dapat dibedakan lagi dinamakan ...", "Campuran homogen (Larutan)", ["Campuran heterogen", "Suspensi", "Koloid kasar"]),
        ("Contoh campuran homogen yang menyatu sempurna adalah ...", "Larutan gula dalam air dan larutan garam", ["Air bercampur minyak goreng", "Air bercampur pasir pantai", "Kopi tubruk berampas"]),
        ("Campuran yang tidak serba sama di mana batas antara zat-zat penyusunnya masih dapat dilihat dengan jelas dinamakan ...", "Campuran heterogen", ["Campuran homogen", "Larutan murni", "Paduan logam"]),
        ("Contoh campuran heterogen yang akan mengendap jika didiamkan adalah ...", "Air bercampur pasir dan air bercampur tepung terigu", ["Larutan sirup manis", "Air garam jernih", "Udara bersih"]),
        ("Sistem campuran yang keadaannya terletak di antara larutan sejati dan suspensi (seperti susu dan santan) dinamakan ...", "Koloid", ["Larutan murni", "Senyawa", "Endapan"]),
        ("Contoh koloid yang sering dijumpai dalam kehidupan sehari-hari adalah ...", "Susu, santan, mayones, dan kabut awan", ["Air garam bening", "Air gula murni", "Batu kerikil"]),
        ("Efek penghamburan berkas cahaya oleh partikel-partikel koloid dinamakan efek ...", "Efek Tyndall", ["Efek Doppler", "Efek Rumah Kaca", "Efek Fotolistrik"]),
        ("Sorot lampu mobil yang tampak jelas membentuk berkas cahaya terang di tengah kabut malam membuktikan adanya efek ...", "Efek Tyndall koloid", ["Pemantulan cermin", "Pembiasan pelangi", "Resonansi"]),
        ("Gerak acak zig-zag partikel koloid di bawah mikroskop ultra akibat tumbukan molekul medium disebut gerak ...", "Gerak Brown", ["Gerak lurus", "Gerak melingkar", "Gerak osilasi"]),
        ("Metode pemisahan campuran yang didasarkan pada perbedaan ukuran partikel zat menggunakan kertas saring atau membran disebut ...", "Filtrasi (Penyaringan)", ["Distilasi", "Evaporasi", "Sublimasi"]),
        ("Zat cair bening yang berhasil lolos melewati kertas saring dinamakan ...", "Filtrat", ["Residu (Ampas)", "Endapan", "Destilat"]),
        ("Zat padat atau ampas yang tertinggal dan tertahan pada kertas saring dinamakan ...", "Residu (Ampas)", ["Filtrat", "Supernatan", "Destilat"]),
        ("Menyaring air teh dari ampas daun teh menggunakan saringan teh merupakan contoh sederhana dari proses ...", "Filtrasi", ["Distilasi", "Kromatografi", "Kristalisasi"]),
        ("Metode pemisahan zat padat terlarut dari larutannya dengan cara menguapkan pelarutnya menggunakan panas dinamakan ...", "Evaporasi (Penguapan)", ["Filtrasi", "Sublimasi", "Kromatografi"]),
        ("Petani garam tradisional di tepi pantai memproduksi garam dari air laut memanfaatkan metode ...", "Evaporasi dengan bantuan sinar matahari dan angin", ["Distilasi bertingkat", "Sublimasi uap", "Penyaringan kertas"]),
        ("Metode pemisahan campuran zat cair yang didasarkan pada perbedaan titik didih komponen-komponennya dinamakan ...", "Distilasi (Penyulingan)", ["Filtrasi", "Kristalisasi", "Kromatografi"]),
        ("Uap zat cair yang terkumpul dari pendinginan kondensor pada proses distilasi dinamakan ...", "Destilat", ["Residu", "Filtrat", "Endapan"]),
        ("Pemisahan minyak bumi mentah menjadi fraksi bensin, minyak tanah, dan solar dilakukan menggunakan teknik ...", "Distilasi bertingkat (Fraksinasi)", ["Filtrasi vakum", "Sentrifugasi", "Kristalisasi"]),
        ("Metode pemisahan campuran zat padat di mana satu zat dapat menyublim menjadi gas dan zat lain tidak disebut ...", "Sublimasi", ["Distilasi", "Evaporasi", "Ekstraksi"]),
        ("Pemisahan kapur barus kotor dari campuran pasir dan debu dilakukan menggunakan metode ...", "Sublimasi", ["Filtrasi biasa", "Distilasi air", "Sentrifugasi"]),
        ("Metode pemisahan campuran zat yang didasarkan pada perbedaan kecepatan perambatan zat warna pada fase diam dinamakan ...", "Kromatografi", ["Distilasi", "Sublimasi", "Filtrasi"]),
        ("Pemisahan zat warna pigmen tinta spidol hitam atau klorofil daun menjadi warna-warna penyusunnya menggunakan teknik ...", "Kromatografi kertas", ["Distilasi uap", "Sentrifugasi", "Kristalisasi"]),
        ("Metode pemisahan campuran dengan cara memutar tabung sampel dengan kecepatan sangat tinggi menggunakan gaya sentrifugal dinamakan ...", "Sentrifugasi", ["Filtrasi", "Dekantasi", "Evaporasi"]),
        ("Pemisahan sel-sel darah merah dari plasma darah di laboratorium medis dilakukan menggunakan alat ...", "Sentrifus (Centrifuge)", ["Kertas saring", "Kondensor Liebig", "Corong pisah"]),
        ("Metode penuangan cairan secara perlahan-lahan untuk memisahkan cairan dari endapan padat kasar di dasar wadah disebut ...", "Dekantasi", ["Distilasi", "Kromatografi", "Sentrifugasi"]),
        ("Alat khusus berbentuk corong berkeran yang digunakan untuk memisahkan dua cairan yang tidak saling bercampur (seperti air dan minyak) adalah ...", "Corong pisah", ["Kondensor", "Gelas ukur", "Buret"]),
        ("Zat yang jumlahnya lebih banyak dan bertindak melarutkan zat lain di dalam larutan dinamakan zat ...", "Pelarut (Solvent)", ["Terlarut (Solute)", "Katalis", "Endapan"]),
        ("Pelarut universal alami yang paling banyak digunakan di bumi karena kepolarannya adalah ...", "Air (H2O)", ["Minyak goreng", "Alkohol", "Aseton"]),
        ("Zat yang dilarutkan ke dalam pelarut seperti butiran gula pasir dinamakan zat ...", "Terlarut (Solute)", ["Pelarut", "Katalisator", "Koloid"]),
        ("Larutan yang sudah tidak dapat lagi melarutkan zat terlarut tambahan pada suhu tertentu dinamakan larutan ...", "Jenuh", ["Tak jenuh", "Lewat jenuh", "Encer"]),
    ]
    for q_text, corr, dists in mixtures_and_separation:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami campuran homogen heterogen, koloid, dan teknik pemisahan materi."))

    # 6. Reaksi Kimia, Korosi & Kimia Terapan (60 soal)
    chemical_reactions = [
        ("Perubahan zat yang hanya mengubah bentuk atau wujud fisiknya saja tanpa menghasilkan zat baru dinamakan perubahan ...", "Fisika", ["Kimia", "Biologis", "Nuklir"]),
        ("Perubahan materi yang menghasilkan satu atau lebih jenis zat baru dengan sifat yang berbeda sama sekali dinamakan perubahan ...", "Kimia", ["Fisika", "Mekanik", "Termal murni"]),
        ("Beras ditumbuk menjadi tepung beras atau es batu mencair menjadi air merupakan contoh perubahan ...", "Fisika", ["Kimia", "Reaksi redoks", "Fermentasi"]),
        ("Kayu yang dibakar menjadi arang hitam dan abu merupakan contoh perubahan ...", "Kimia", ["Fisika", "Fase", "Bentuk"]),
        ("Kembang api yang meledak menghasilkan kilatan cahaya warna-warni dan suara keras merupakan contoh perubahan ...", "Kimia", ["Fisika", "Mekanik", "Alami"]),
        ("Susu segar yang difermentasi menjadi keju atau yogurt merupakan contoh perubahan ...", "Kimia", ["Fisika", "Mencair", "Menyublim"]),
        ("Singkong yang diberi ragi dan difermentasi menjadi tape manis yang beraroma alkohol merupakan contoh perubahan ...", "Kimia", ["Fisika", "Penyusutan", "Penguapan"]),
        ("Kawat besi yang dibiarkan di udara lembap berubah menjadi berkarat kemerahan merupakan contoh perubahan ...", "Kimia", ["Fisika", "Pengendapan fisis", "Membeku"]),
        ("Garam dilarutkan ke dalam segelas air hangat merupakan contoh perubahan ...", "Fisika", ["Kimia", "Pembusukan", "Oksidasi"]),
        ("Empat tanda atau gejala utama yang menunjukkan terjadinya suatu reaksi kimia adalah perubahan warna, perubahan suhu, terbentuknya endapan, dan ...", "Timbulnya gas (gelembung)", ["Perubahan wujud sementara", "Benda mengecil", "Perubahan massa"]),
        ("Reaksi kimia yang melepaskan energi panas ke lingkungan sehingga wadah terasa hangat atau panas dinamakan reaksi ...", "Eksoterm", ["Endoterm", "Isoterm", "Reversibel"]),
        ("Contoh nyata dari reaksi eksoterm yang melepaskan kalor adalah ...", "Reaksi pembakaran kayu api dan batu kapur disiram air", ["Es batu mencair", "Garam dilarutkan dalam air", "Fotosintesis tumbuhan"]),
        ("Reaksi kimia yang menyerap energi panas dari lingkungan sehingga wadah terasa dingin dinamakan reaksi ...", "Endoterm", ["Eksoterm", "Pembakaran", "Oksidasi"]),
        ("Contoh reaksi endoterm di alam yang membutuhkan dan menyerap energi cahaya matahari adalah ...", "Proses fotosintesis pada tumbuhan hijau", ["Pembakaran gas kompor", "Ledakan bom dinamit", "Besi berkarat"]),
        ("Zat yang dapat mempercepat laju terjadinya reaksi kimia tanpa ikut habis bereaksi di akhir reaksi dinamakan ...", "Katalis (Katalisator)", ["Reaktan", "Produk", "Inhibitor"]),
        ("Katalis biologis alami yang bekerja mempercepat reaksi kimia di dalam tubuh makhluk hidup adalah ...", "Enzim", ["Hormon", "Vitamin", "Glukosa"]),
        ("Hukum Kekekalan Massa yang menyatakan bahwa massa zat sebelum dan sesudah reaksi selalu sama dikemukakan oleh ...", "Antoine Lavoisier", ["John Dalton", "Joseph Proust", "Avogadro"]),
        ("Hukum Perbandingan Tetap yang menyatakan bahwa massa unsur-unsur dalam suatu senyawa selalu memiliki perbandingan tetap dikemukakan oleh ...", "Joseph Proust", ["Antoine Lavoisier", "John Dalton", "Gay-Lussac"]),
        ("Proses perkaratan pada besi terjadi akibat reaksi antara logam besi dengan dua zat di udara yaitu ...", "Oksigen dan uap air (kelembapan)", ["Karbon dioksida dan nitrogen", "Gas helium dan hidrogen", "Minyak pelumas"]),
        ("Rumus kimia dari karat besi berwarna cokelat kemerahan adalah ...", "Fe2O3 . xH2O (Besi(III) Oksida terhidrasi)", ["FeO", "FeCl3", "FeSO4"]),
        ("Cara pencegahan karat pada badan mobil dengan melapisi logam menggunakan lapisan tipis seng (Zn) dinamakan ...", "Galvanisasi", ["Elektroforesis", "Vulkanisasi", "Sublimasi"]),
        ("Cara sederhana mencegah karat pada rantai sepeda dan engsel pintu adalah dengan mengoleskan ...", "Minyak pelumas (Oli atau gemuk)", ["Air garam", "Cuka makan", "Cat air"]),
        ("Pengecatan pada pagar besi rumah bertujuan untuk melindungi besi dari kontak langsung dengan ...", "Oksigen dan air di udara", ["Sinar matahari", "Bakteri tanah", "Debu"]),
        ("Molekul sabun memiliki dua bagian yaitu bagian kepala yang suka air dan bagian ekor yang suka minyak. Bagian suka air disebut ...", "Hidrofilik", ["Hidrofobik", "Lipofilik", "Nonpolar"]),
        ("Bagian ekor pada molekul sabun yang tidak suka air dan mengikat kotoran minyak/lemak disebut bagian ...", "Hidrofobik", ["Hidrofilik", "Polar", "Ionik"]),
        ("Air yang mengandung ion kalsium (Ca2+) dan magnesium (Mg2+) tinggi sehingga sukar menghasilkan busa sabun disebut ...", "Air sadah", ["Air murni", "Air lunak", "Air aki"]),
        ("Endapan kerak putih yang sering muncul di dasar teko pemanas air berasal dari senyawa sadah yaitu ...", "Kalsium karbonat (CaCO3)", ["Natrium klorida", "Asam sitrat", "Besi sulfat"]),
        ("Zat kimia pengawet sintetis yang sering digunakan pada minuman kemasan sari buah dan saus adalah natrium ...", "Natrium Benzoat", ["Natrium Klorida", "Natrium Bikarbonat", "Natrium Hidroksida"]),
        ("Pewarna makanan sintetis warna kuning yang banyak digunakan pada sirup dan kerupuk adalah ...", "Tartrazin", ["Karmoisin", "Klorofil", "Kurkumin"]),
        ("Penyedap rasa sintetis monosodium glutamat (MSG) mengandung ion dari asam amino yaitu asam ...", "Glutamat", ["Askorbat", "Asetat", "Sitrat"]),
    ]
    for q_text, corr, dists in chemical_reactions:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami perubahan kimia fisika, reaksi eksoterm endoterm, dan korosi."))

    # 7. Bahan Kimia Lingkungan & Polutan (50 soal)
    environmental_chemistry = [
        ("Bahan bakar minyak bumi tersusun atas campuran senyawa organik yang mengandung unsur utama ...", "Karbon dan Hidrogen (Hidrokarbon)", ["Nitrogen dan Oksigen", "Kalsium dan Besi", "Silikon dan Belerang"]),
        ("Ukuran kemampuan bahan bakar bensin untuk menahan ketukan mesin (knocking) dinamakan angka ...", "Oktan (Research Octane Number / RON)", ["Setana", "Kalori", "Viskositas"]),
        ("Bahan bakar bensin Pertalite memiliki nilai angka oktan sebesar ...", "RON 90", ["RON 92", "RON 95", "RON 98"]),
        ("Bahan bakar bensin Pertamax memiliki nilai angka oktan sebesar ...", "RON 92", ["RON 90", "RON 88", "RON 98"]),
        ("Ukuran kualitas penyalaan bahan bakar solar mesin diesel diukur menggunakan angka ...", "Setana (Cetane Number)", ["Oktan", "Flash point", "Viskositas"]),
        ("Zat aditif berbahaya tetraethyl lead (TEL) yang dahulu ditambahkan ke bensin untuk menaikkan oktan mengandung logam berat ...", "Timbal (Pb)", ["Merkuri", "Kadmium", "Arsenik"]),
        ("Penggunaan timbal pada bensin dihapuskan di seluruh dunia karena asap knalpotnya dapat menyebabkan ...", "Penurunan kecerdasan anak dan kerusakan saraf otak", ["Karat pada knalpot", "Mobil mogok", "Asap berwarna hitam"]),
        ("Gas buang beracun dari rokok dan knalpot yang mengikat hemoglobin darah 200 kali lebih kuat dibanding oksigen adalah ...", "Karbon Monoksida (CO)", ["Karbon Dioksida (CO2)", "Gas Nitrogen (N2)", "Gas Metana"]),
        ("Gejala keracunan gas karbon monoksida (CO) di dalam mobil tertutup yang AC-nya menyala saat mesin hidup adalah ...", "Pusing, mengantuk lemas, hilang kesadaran hingga kematian", ["Mata merah berair", "Bersin terus-menerus", "Batuk berdarah"]),
        ("Gas polutan yang memiliki bau seperti telur busuk yang sangat beracun di tempat pembuangan sampah adalah ...", "Hidrogen Sulfida (H2S)", ["Karbon Dioksida", "Amonia", "Gas Metana"]),
        ("Zat kimia beracun yang digunakan dalam racun tikus dan kasus pembunuhan terkenal zaman dahulu adalah ...", "Arsenik (As)", ["Besi", "Kalsium", "Seng"]),
        ("Penyakit Minamata di Jepang disebabkan oleh pencemaran limbah industri teluk yang mengandung logam berat ...", "Merkuri (Air Raksa)", ["Timbal", "Tembaga", "Besi"]),
        ("Penyakit Itai-itai di Jepang yang menyebabkan tulang menjadi sangat rapuh dan nyeri disebabkan keracunan logam ...", "Kadmium (Cd)", ["Kalsium", "Merkuri", "Timah"]),
        ("Senyawa plastik yang paling banyak digunakan untuk membuat botol air mineral bening sekali pakai adalah plastik ...", "PET / PETE (Polietilena Tereftalat)", ["PVC", "HDPE", "Styrofoam"]),
        ("Plastik polimer yang banyak digunakan untuk pipa paralon saluran air rumah adalah ...", "PVC (Polivinil Klorida)", ["PET", "Nilon", "Teflon"]),
        ("Bahan pelapis antilengket pada wajan penggorengan modern adalah polimer politetrafluoroetilena yang dikenal dengan nama ...", "Teflon (PTFE)", ["PVC", "Nilon", "Styrofoam"]),
        ("Zat kimia berbahaya pada wadah plastik yang dapat mengganggu sistem hormon manusia jika terpapar panas adalah ...", "BPA (Bisphenol-A)", ["Teflon", "Kalsium", "Silika"]),
        ("Kantong kemasan makanan yang aman dari bahan kimia berbahaya sering diberi label ...", "BPA Free", ["BPA Plus", "PVC Only", "Non-Organic"]),
        ("Gel silika (silica gel) putih di dalam kotak sepatu dan tas baru berfungsi sebagai zat penyerap ...", "Uap air dan kelembapan agar barang tidak berjamur", ["Bau wangi", "Debu halus", "Panas api"]),
        ("Larutan pembasmi kuman kuman penyakit pada lantai atau kandang hewan dinamakan ...", "Desinfektan", ["Antiseptik", "Insektisida", "Herbisida"]),
        ("Cairan pembersih kuman yang aman digunakan langsung pada jaringan kulit manusia yang terluka dinamakan ...", "Antiseptik", ["Desinfektan", "Pestisida", "Fungisida"]),
        ("Obat kimia yang digunakan petani khusus untuk membasmi hama serangga perusak tanaman dinamakan ...", "Insektisida", ["Herbisida", "Fungisida", "Rodentisida"]),
        ("Obat kimia yang digunakan khusus untuk membasmi gulma dan rumput liar pengganggu tanaman dinamakan ...", "Herbisida", ["Insektisida", "Fungisida", "Bakterisida"]),
        ("Obat kimia yang digunakan untuk memberantas hama jamur pada tanaman pertanian dinamakan ...", "Fungisida", ["Insektisida", "Herbisida", "Rodentisida"]),
        ("Obat kimia yang digunakan khusus untuk membasmi hama tikus di persawahan dinamakan ...", "Rodentisida", ["Insektisida", "Herbisida", "Fungisida"]),
    ]
    for q_text, corr, dists in environmental_chemistry:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami kimia lingkungan, polusi, polimer plastik, dan bahan kimia rumah tangga."))

    # 8. Biomolekul & Kimia Organik (45 soal)
    biomolecules = [
        ("Zat gizi makro yang menjadi sumber energi utama dan tercepat bagi tubuh manusia adalah ...", "Karbohidrat", ["Protein", "Lemak", "Vitamin", "Mineral"]),
        ("Karbohidrat paling sederhana yang terdiri dari satu unit molekul gula dinamakan ...", "Monosakarida", ["Disakarida", "Polisakarida", "Oligosakarida"]),
        ("Gula alami yang paling manis yang banyak terkandung di dalam madu dan buah-buahan matang adalah ...", "Fruktosa", ["Glukosa", "Galaktosa", "Sukrosa"]),
        ("Gula darah utama yang diedarkan ke seluruh sel tubuh untuk diubah menjadi energi adalah ...", "Glukosa", ["Fruktosa", "Laktosa", "Maltosa"]),
        ("Gula yang terdapat di dalam air susu ibu (ASI) dan susu sapi adalah ...", "Laktosa", ["Sukrosa", "Fruktosa", "Maltosa"]),
        ("Ketidakmampuan tubuh mencerna gula susu akibat kekurangan enzim laktase dinamakan ...", "Intoleransi Laktosa", ["Diabetes melitus", "Alergi gluten", "Anemia"]),
        ("Karbohidrat kompleks yang tersusun dari ribuan rantai unit glukosa seperti pada nasi dan kentang dinamakan ...", "Polisakarida (Pati / Amilum)", ["Monosakarida", "Disakarida", "Lipid"]),
        ("Zat tepung cadangan makanan pada biji padi, jagung, dan gandum dinamakan ...", "Amilum (Pati)", ["Glikogen", "Selulosa", "Kitin"]),
        ("Cadangan karbohidrat yang disimpan di dalam hati dan otot hewan/manusia dinamakan ...", "Glikogen (Gula otot)", ["Amilum", "Selulosa", "Pektin"]),
        ("Serat tumbuhan yang menyusun dinding sel tumbuhan dan tidak dapat dicerna oleh usus manusia adalah ...", "Selulosa", ["Amilum", "Glikogen", "Fruktosa"]),
        ("Polisakarida keras yang menyusun cangkang kepiting, udang, dan dinding sel jamur adalah ...", "Kitin", ["Selulosa", "Pektin", "Lignin"]),
        ("Uji amilum di laboratorium menggunakan larutan lugol (iodin) akan menghasilkan warna khas yaitu ...", "Biru tua kehitaman", ["Merah bata", "Ungu pekat", "Kuning terang"]),
        ("Uji glukosa pada makanan menggunakan larutan Fehling atau Benedict yang dipanaskan menghasilkan endapan berwarna ...", "Merah bata", ["Biru bening", "Ungu", "Hitam"]),
        ("Zat pembangun tubuh yang berfungsi memperbaiki sel-sel tubuh yang rusak dan pertumbuhan adalah ...", "Protein", ["Karbohidrat", "Lemak", "Serat"]),
        ("Unit molekul tunggal penyusun rantai protein dinamakan ...", "Asam amino", ["Asam lemak", "Glukosa", "Gliserol"]),
        ("Jumlah jenis asam amino standar yang menyusun protein di dalam tubuh makhluk hidup berjumlah ...", "20 jenis", ["10 jenis", "50 jenis", "100 jenis"]),
        ("Asam amino yang tidak dapat diproduksi sendiri oleh tubuh manusia dan wajib diperoleh dari makanan disebut asam amino ...", "Esensial", ["Non-esensial", "Kondisional", "Sintetis"]),
        ("Uji protein di laboratorium menggunakan pereaksi Biuret akan menghasilkan perubahan warna khas yaitu ...", "Ungu (Violet)", ["Merah bata", "Biru tua", "Kuning"]),
        ("Kerusakan struktur lipatan protein akibat pemanasan suhu tinggi atau asam kuat (seperti telur digoreng) dinamakan ...", "Denaturasi protein", ["Koagulasi", "Fermentasi", "Kristalisasi"]),
        ("Zat nutrisi penghasil energi terbesar per gramnya (9 kkal per gram) adalah ...", "Lemak (Lipid)", ["Karbohidrat", "Protein", "Vitamin"]),
        ("Molekul lemak tersusun atas gabungan satu molekul gliserol dengan tiga molekul ...", "Asam lemak", ["Asam amino", "Glukosa", "Monosakarida"]),
        ("Lemak yang pada suhu kamar berwujud padat dan banyak terdapat pada daging sapi atau mentega adalah lemak ...", "Jenuh", ["Tak jenuh", "Trans", "Omega"]),
        ("Minyak nabati dari kelapa sawit, zaitun, dan jagung pada suhu ruang berwujud cair karena kaya akan asam lemak ...", "Tak jenuh", ["Jenuh", "Padat", "Trigliserida"]),
        ("Asam nukleat pembawa informasi genetik keturunan di dalam inti sel tubuh adalah ...", "DNA (Asam Deoksiribonukleat)", ["RNA", "ATP", "Enzim"]),
        ("Asam nukleat yang bertugas membaca kode genetik dan melakukan sintesis protein adalah ...", "RNA (Asam Ribonukleat)", ["DNA", "ADP", "Glukosa"]),
        ("Basa nitrogen adenin (A) pada untai rantai DNA selalu berpasangan dengan basa ...", "Timin (T)", ["Guanin", "Sitosin", "Urasil"]),
        ("Basa nitrogen guanin (G) pada rantai DNA selalu berpasangan dengan basa ...", "Sitosin (C)", ["Timin", "Adenin", "Urasil"]),
        ("Basa nitrogen khusus yang hanya ditemukan pada molekul RNA menggantikan timin adalah ...", "Urasil (U)", ["Timin", "Guanin", "Adenin"]),
    ]
    for q_text, corr, dists in biomolecules:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami senyawa organik karbohidrat, protein, lemak, dan asam nukleat DNA."))

    # 9. Paduan Logam & Uji Nyala (45 soal)
    alloys_and_flames = [
        ("Campuran homogen antara dua atau lebih unsur logam atau logam dengan non-logam dinamakan ...", "Paduan logam (Aloi / Alloy)", ["Biji logam", "Mineral murni", "Senyawa kovalen"]),
        ("Paduan logam kuningan (brass) yang banyak digunakan untuk alat musik tiup dan gembok terbuat dari campuran ...", "Tembaga (Cu) dan Seng (Zn)", ["Tembaga dan Timah", "Besi dan Karbon", "Aluminium dan Emas"]),
        ("Paduan logam perunggu (bronze) yang digunakan untuk medali dan patung terbuat dari campuran ...", "Tembaga (Cu) dan Timah (Sn)", ["Tembaga dan Seng", "Besi dan Nikel", "Aluminium dan Timbal"]),
        ("Baja (steel) yang kokoh untuk konstruksi jembatan dan rel kereta api dibuat dari campuran ...", "Besi (Fe) dan sedikit Karbon (C)", ["Tembaga dan Seng", "Aluminium murni", "Emas dan Perak"]),
        ("Baja tahan karat (stainless steel) yang tidak mudah berkarat dibuat dengan menambahkan logam ...", "Kromium (Cr) dan Nikel (Ni)", ["Tembaga", "Emas murni", "Air raksa"]),
        ("Paduan logam duralumin yang sangat ringan dan kuat untuk badan pesawat terbang tersusun dari ...", "Aluminium, tembaga, dan magnesium", ["Besi dan timbal", "Seng dan emas", "Nikel dan perak"]),
        ("Kawat timah solder yang digunakan untuk menyambung komponen elektronika terbuat dari paduan ...", "Timah (Sn) dan Timbal (Pb)", ["Besi dan baja", "Tembaga murni", "Emas dan perak"]),
        ("Campuran antara air raksa (merkuri) dengan logam perak yang dahulu digunakan untuk menambal gigi berlubang dinamakan ...", "Amalgam", ["Perunggu", "Kuningan", "Duralumin"]),
        ("Emas murni 24 karat bersifat sangat lunak, sehingga untuk membuat perhiasan emas dicampur dengan perak atau tembaga menghasilkan emas ...", "Emas 18 karat atau 22 karat", ["Emas 30 karat", "Emas baja", "Emas putih 100 karat"]),
        ("Kembang api memancarkan kilatan warna kuning terang karena mengandung senyawa garam dari unsur ...", "Natrium (Sodium)", ["Tembaga", "Barium", "Stronsium"]),
        ("Kembang api memancarkan kilatan warna hijau kebiruan yang indah karena mengandung senyawa garam dari unsur ...", "Tembaga (Cu)", ["Natrium", "Kalsium", "Kalium"]),
        ("Kembang api memancarkan kilatan warna merah terang kirmizi karena mengandung garam dari logam ...", "Stronsium (Sr) atau Litium", ["Natrium", "Barium", "Tembaga"]),
        ("Kembang api memancarkan kilatan warna hijau apel karena mengandung garam dari logam ...", "Barium (Ba)", ["Kalsium", "Natrium", "Kalium"]),
        ("Uji nyala senyawa garam kalium pada nyala api pembakar Bunsen menghasilkan warna khas yaitu ...", "Ungu (Lila)", ["Kuning terang", "Hijau apel", "Merah bata"]),
        ("Uji nyala senyawa garam kalsium menghasilkan pendaran nyala berwarna ...", "Merah bata (Oranye kemerahan)", ["Hijau", "Biru", "Kuning"]),
        ("Serbuk logam yang ditambahkan pada kembang api untuk menghasilkan kilatan percikan putih menyilaukan (sparkler) adalah ...", "Magnesium atau Aluminium", ["Tembaga", "Belerang", "Karbon"]),
        ("Bubuk mesiu hitam (black powder) kuno yang ditemukan bangsa Tiongkok tersusun dari belerang, arang, dan ...", "Kalium nitrat (Sendawa / KNO3)", ["Natrium klorida", "Kalsium karbonat", "Asam sulfat"]),
    ]
    for q_text, corr, dists in alloys_and_flames:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami jenis paduan logam (alloy), uji nyala kation, dan bahan kembang api."))

    # 10. Larutan Elektrolit & Reaksi Redoks (50 soal)
    electrolytes_and_redox = [
        ("Larutan yang dapat menghantarkan arus listrik karena zat terlarutnya terurai menjadi ion-ion bebas dinamakan larutan ...", "Elektrolit", ["Nonelektrolit", "Jenuh", "Koloid"]),
        ("Larutan yang tidak dapat menghantarkan arus listrik sama sekali karena zat terlarutnya tidak membentuk ion dinamakan larutan ...", "Nonelektrolit", ["Elektrolit kuat", "Elektrolit lemah", "Buffer"]),
        ("Ciri pengujian larutan elektrolit kuat dengan alat uji elektrolit adalah ...", "Lampu menyala terang dan banyak gelembung gas di elektrode", ["Lampu mati total", "Tidak ada gelembung", "Kabel terbakar"]),
        ("Contoh larutan yang tergolong elektrolit kuat penghantar listrik yang baik adalah ...", "Larutan garam dapur (NaCl) dan air aki (H2SO4)", ["Larutan gula pasir murni", "Larutan alkohol 70%", "Minyak kelapa"]),
        ("Ciri pengujian larutan elektrolit lemah adalah ...", "Lampu menyala redup atau padam tetapi timbul sedikit gelembung gas", ["Lampu menyala sangat terang", "Banyak sekali gelembung", "Elektrode meleleh"]),
        ("Contoh larutan yang tergolong elektrolit lemah adalah ...", "Larutan asam cuka dapur (CH3COOH) dan air kapur", ["Larutan asam klorida pekat", "Larutan garam dapur jenuh", "Larutan soda api"]),
        ("Contoh larutan yang tergolong nonelektrolit (tidak menghantarkan listrik sama sekali) adalah ...", "Larutan gula pasir dan larutan alkohol", ["Air garam dapur", "Air aki asam sulfat", "Larutan pupuk urea"]),
        ("Air murni murni hasil distilasi (aquades) pada dasarnya tergolong penghantar listrik yang ...", "Sangat buruk / non-konduktor (nonelektrolit)", ["Sangat kuat seperti kabel", "Berbahaya tegangan tinggi", "Mudah meledak"]),
        ("Alasan air banjir atau air ledeng dapat menyetrum manusia jika terkena kabel listrik PLN adalah karena ...", "Mengandung banyak garam mineral terlarut yang bertindak sebagai elektrolit", ["Air ledeng terbuat dari tembaga", "Air banjir menghasilkan listrik sendiri", "Air bereaksi dengan udara"]),
        ("Minuman isotonik yang diminum setelah berolahraga berfungsi untuk menggantikan ...", "Cairan tubuh dan elektrolit ion mineral yang hilang melalui keringat", ["Kekurangan oksigen", "Menambah lemak tubuh", "Mencegah lapar"]),
        ("Reaksi kimia di mana suatu zat mengikat gas oksigen dinamakan reaksi ...", "Oksidasi", ["Reduksi", "Hidrolisis", "Kondensasi"]),
        ("Reaksi kimia di mana suatu zat melepaskan gas oksigen dinamakan reaksi ...", "Reduksi", ["Oksidasi", "Netralisasi", "Polimerisasi"]),
        ("Dalam konsep transfer elektron, oksidasi didefinisikan sebagai peristiwa ...", "Pelepasan elektron oleh suatu atom atau ion", ["Penangkapan elektron", "Penambahan neutron", "Pelepasan proton"]),
        ("Dalam konsep transfer elektron, reduksi didefinisikan sebagai peristiwa ...", "Penangkapan atau penerimaan elektron oleh suatu spesi", ["Pelepasan elektron", "Pelepasan muatan", "Penyusutan massa"]),
        ("Zat yang menyebabkan zat lain mengalami oksidasi sementara dirinya sendiri mengalami reduksi dinamakan ...", "Oksidator (Pengoksidasi)", ["Reduktor", "Katalis", "Inhibitor"]),
        ("Zat yang menyebabkan zat lain mengalami reduksi sementara dirinya sendiri mengalami oksidasi dinamakan ...", "Reduktor (Pereduksi)", ["Oksidator", "Katalisator", "Pelarut"]),
        ("Reaksi kimia di mana peristiwa reduksi dan oksidasi selalu berlangsung secara bersamaan dinamakan reaksi ...", "Redoks (Reduksi-Oksidasi)", ["Asam basa", "Netralisasi", "Pengendapan"]),
        ("Bilangan oksidasi (biloks) untuk atom unsur bebas murni seperti O2, Fe, H2, dan Cu bernilai ...", "Nol (0)", ["+1", "-1", "+2"]),
        ("Bilangan oksidasi atom hidrogen (H) dalam sebagian besar senyawanya (seperti H2O, HCl) bernilai ...", "+1", ["-1", "0", "+2"]),
        ("Bilangan oksidasi atom oksigen (O) dalam sebagian besar senyawanya bernilai ...", "-2", ["-1", "+2", "0"]),
        ("Penyepuhan logam perhiasan menggunakan arus listrik searah untuk melapisi permukaan logam dengan logam mulia dinamakan ...", "Elektroplating (Penyepuhan listrik)", ["Elektroforesis", "Galvanisasi murni", "Distilasi"]),
        ("Pada proses penyepuhan sendok besi dengan lapisan perak, sendok besi dipasang pada kutub ...", "Katode (Kutub negatif)", ["Anode (Kutub positif)", "Sumber AC", "Arde tanah"]),
        ("Kutub tempat terjadinya reaksi reduksi pada sel elektrokimia dinamakan ...", "Katode", ["Anode", "Jembatan garam", "Dioda"]),
        ("Kutub elektrode tempat terjadinya reaksi oksidasi pada sel elektrokimia dinamakan ...", "Anode", ["Katode", "Kondensor", "Resistor"]),
    ]
    for q_text, corr, dists in electrolytes_and_redox:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami larutan elektrolit, nonelektrolit, konsep redoks, dan elektrokimia."))

    # 11. Kimia Bahan Makanan, Obat & Rumah Tangga (50 soal)
    food_and_drugs = [
        ("Zat pemanis alami rendah kalori yang diekstrak dari daun tanaman Stevia rebaudiana adalah ...", "Stevia (Steviol glikosida)", ["Sakarin", "Siklamat", "Aspartam"]),
        ("Zat pengemulsi alami pada kuning telur dan kacang kedelai yang menyatukan campuran air dan minyak adalah ...", "Lesitin", ["Gelatin", "Agar-agar", "Pektin"]),
        ("Bahan alami pembuat jeli dan pengental makanan yang diekstrak dari rumput laut merah adalah ...", "Agar-agar (Karagenan)", ["Gelatin", "Tepung maizena", "Sagu"]),
        ("Bahan protein pengental yang diperoleh dari ekstraksi kolagen tulang dan kulit sapi atau ikan adalah ...", "Gelatin", ["Agar-agar", "Pektin", "Amilum"]),
        ("Pengental alami yang banyak terdapat pada kulit buah apel dan jeruk yang digunakan membuat selai buah adalah ...", "Pektin", ["Gelatin", "Karagenan", "Gliserin"]),
        ("Jamur ragi mikroskopis yang digunakan dalam pembuatan roti untuk menghasilkan gelembung gas CO2 pengembang adalah ...", "Saccharomyces cerevisiae", ["Aspergillus oryzae", "Lactobacillus bulgaricus", "Rhizopus oryzae"]),
        ("Bakteri baik yang digunakan dalam fermentasi susu sapi menjadi yogurt yang asam segar adalah ...", "Lactobacillus bulgaricus dan Streptococcus thermophilus", ["Escherichia coli", "Salmonella", "Clostridium botulinum"]),
        ("Jamur kapang yang digunakan dalam proses fermentasi kedelai menjadi tempe tradisional adalah ...", "Rhizopus oryzae", ["Saccharomyces", "Neurospora sitophila", "Penicillium"]),
        ("Jamur kapang berwarna oranye yang digunakan dalam fermentasi ampas tahu menjadi oncom merah adalah ...", "Neurospora sitophila", ["Rhizopus oryzae", "Aspergillus", "Saccharomyces"]),
        ("Zat antiseptik pembersih luka luar yang mengandung iodin kompleks berwarna cokelat adalah ...", "Povidone Iodine (Betadine)", ["Alkohol 96%", "Rivanol", "Klorin"]),
        ("Obat yang paling umum digunakan untuk meredakan sakit kepala, nyeri, dan menurunkan demam tanpa resep dokter adalah ...", "Parasetamol (Asetaminofen)", ["Amoksisilin", "Antasida", "Omeprazol"]),
        ("Obat pereda nyeri dan pengencer darah yang memiliki nama kimia asam asetilsalisilat adalah ...", "Aspirin", ["Parasetamol", "Ibuprofen", "Asam mefenamat"]),
        ("Kelompok obat keras yang khusus digunakan untuk membunuh atau menghambat pertumbuhan bakteri infeksi adalah ...", "Antibiotik", ["Antivirus", "Antijamur", "Analgesik"]),
        ("Antibiotik pertama yang ditemukan di dunia oleh Alexander Fleming berasal dari jamur ...", "Penicillium notatum (Penisilin)", ["Aspergillus niger", "Saccharomyces", "Rhizopus"]),
        ("Obat antibiotik wajib diminum sampai habis sesuai petunjuk dokter bertujuan untuk ...", "Mencegah bakteri kuman menjadi kebal (resisten)", ["Agar obat tidak mubazir", "Membuat tubuh gemuk", "Membersihkan darah"]),
        ("Gas kimia beracun yang digunakan oleh pelaku teror atau perang kimia yang melumpuhkan saraf manusia dinamakan ...", "Gas Sarin", ["Gas Oksigen", "Gas Karbon Dioksida", "Gas Helium"]),
        ("Kandungan senyawa kimia di dalam cairan pengering kutek kuku (remover) adalah pelarut organik ...", "Aseton (Propanon)", ["Alkohol", "Bensin", "Cuka"]),
        ("Zat kimia asam yang digunakan pada produk kosmetik perawatan wajah untuk eksfoliasi kulit mati adalah ...", "AHA dan BHA (Asam Salisilat)", ["Asam Sulfat", "Asam Klorida", "Asam Nitrat"]),
        ("Kandungan senyawa kimia di dalam sabun cuci piring yang menghasilkan banyak busa pembersih lemak adalah ...", "Surfaktan (seperti SLS / Sodium Lauryl Sulfate)", ["Asam sitrat", "Garam", "Pewarna"]),
        ("Kapur ajaib atau kapur antiserangga mengandung insektisida kimia yang efektif membasmi kecoak dan semut yaitu ...", "Deltametrin / Cypermethrin", ["DDT", "Boraks", "Formalin"]),
    ]
    for q_text, corr, dists in food_and_drugs:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami kimia makanan, fermentasi ragi, obat-obatan, dan produk rumah tangga."))

    # 12. Proses Industri Kimia & Gas Khusus (50 soal)
    industrial_chemistry = [
        ("Proses kimia industri untuk memproduksi gas amonia secara massal dari gas nitrogen dan hidrogen dinamakan ...", "Proses Haber-Bosch", ["Proses Kontak", "Proses Solvay", "Proses Bessemer"]),
        ("Proses kimia industri yang digunakan untuk memproduksi asam sulfat (H2SO4) pekat menggunakan katalis V2O5 dinamakan ...", "Proses Kontak", ["Proses Haber-Bosch", "Proses Down", "Proses Ostwald"]),
        ("Proses kimia industri untuk memproduksi asam nitrat (HNO3) melalui oksidasi amonia dinamakan ...", "Proses Ostwald", ["Proses Kontak", "Proses Haber", "Proses Hall-Heroult"]),
        ("Metode elektrolisis industri yang digunakan untuk memurnikan aluminium dari bijih bauksit dinamakan ...", "Proses Hall-Heroult", ["Proses Kontak", "Proses Bessemer", "Proses Solvay"]),
        ("Baterai isi ulang yang paling banyak digunakan pada smartphone dan laptop modern adalah baterai ...", "Litium-Ion (Li-ion)", ["Nikel-Kadmium", "Seng-Karbon", "Aki Basah"]),
        ("Logam paling ringan di tabel periodik yang menjadi komponen utama baterai ponsel dan mobil listrik adalah ...", "Litium (Li)", ["Natrium", "Aluminium", "Besi"]),
        ("Elektrode positif (katode) pada batu baterai kering biasa (baterai seng-karbon) terbuat dari batang ...", "Karbon (Grafit)", ["Seng", "Tembaga", "Besi"]),
        ("Wadah pembungkus bagian luar pada batu baterai kering biasa sekaligus bertindak sebagai anode terbuat dari ...", "Logam Seng (Zn)", ["Aluminium", "Tembaga", "Plastik"]),
        ("Pasta elektrolit yang terdapat di dalam batu baterai seng-karbon biasa adalah campuran ...", "Amonium klorida (NH4Cl) dan Mangan dioksida (MnO2)", ["Asam sulfat pekat", "Garam dapur murni", "Air raksa"]),
        ("Cairan elektrolit yang digunakan di dalam aki motor basah adalah ...", "Asam sulfat (H2SO4) encer", ["Asam klorida", "Air murni", "Minyak rem"]),
        ("Pelat timbel pada aki motor saat terisi penuh (disetrum) terdiri atas pelat Pb dan pelat ...", "Timbel dioksida (PbO2)", ["Besi oksida", "Aluminium", "Tembaga sulfat"]),
        ("Sel elektrokimia yang mengubah energi kimia dari bahan bakar hidrogen dan oksigen langsung menjadi listrik dinamakan ...", "Sel Bahan Bakar (Fuel Cell)", ["Sel Kering", "Aki Basah", "Sel Surya"]),
        ("Kelebihan utama mobil bermesin sel bahan bakar hidrogen (fuel cell) bagi kelestarian lingkungan adalah ...", "Hanya menghasilkan emisi berupa air murni (H2O) tanpa polusi", ["Tidak membutuhkan bahan bakar", "Harganya sangat murah", "Bisa terbang"]),
        ("Gas kimia berbau khas menusuk hidung yang digunakan untuk mengisi tabung pemadam api busa adalah ...", "Karbon dioksida (CO2)", ["Gas oksigen murni", "Gas hidrogen", "Gas metana"]),
        ("Alat pemadam api ringan (APAR) tipe serbuk kimia kering (dry chemical powder) umumnya berisi bahan ...", "Natrium bikarbonat (Soda kue) atau monoamonium fosfat", ["Garam dapur", "Batu kapur", "Pasir laut"]),
        ("Gas kimia beracun yang digunakan dalam pemutihan bubur kertas (pulp) dan desinfektan kolam renang adalah ...", "Gas Klorin (Cl2)", ["Gas Helium", "Gas Oksigen", "Gas Karbon Monoksida"]),
        ("Senyawa gas fluor yang digunakan dalam industri pemisahan isotop pengayaan uranium adalah gas ...", "Uranium heksafluorida (UF6)", ["Uranium dioksida", "Uranium klorida", "Uranium nitrat"]),
        ("Pancaran cahaya biru terang di dalam kolam pendingin air reaktor nuklir yang berasal dari partikel bermuatan yang melaju melebihi kecepatan cahaya di air dinamakan radiasi ...", "Radiasi Cherenkov", ["Radiasi Benda Hitam", "Sinar Rontgen", "Sinar Alfa"]),
        ("Kadar kemurnian alkohol teknis yang paling efektif untuk mematikan kuman bakteri pada antiseptik tangan adalah ...", "70%", ["100% murni", "20%", "40%"]),
        ("Alkohol berkadar 70% lebih efektif membunuh bakteri dibanding alkohol 96% murni karena ...", "Kandungan airnya membantu membuka pori-pori dinding sel bakteri sehingga alkohol meresap masuk", ["Alkohol murni tidak beracun", "Alkohol 70% lebih wangi", "Alkohol murni cepat membeku"]),
    ]
    for q_text, corr, dists in industrial_chemistry:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami proses kimia industri, baterai, sel bahan bakar, dan aplikasi kimia terapan."))

    # 13. Nomor Atom Unsur 1-20 & Unsur Spesifik (40 soal)
    elements_numbers_extra = [
        ("Nomor atom dari unsur Hidrogen (H) yang merupakan unsur pertama di tabel periodik adalah ...", "1", ["2", "3", "0"]),
        ("Nomor atom dari unsur gas mulia Helium (He) adalah ...", "2", ["1", "4", "3"]),
        ("Nomor atom dari unsur logam alkali teringan Litium (Li) adalah ...", "3", ["2", "4", "5"]),
        ("Nomor atom dari unsur logam Berilium (Be) adalah ...", "4", ["3", "5", "6"]),
        ("Nomor atom dari unsur metaloid Boron (B) adalah ...", "5", ["4", "6", "7"]),
        ("Nomor atom dari unsur Karbon (C) yang menjadi dasar senyawa organik adalah ...", "6", ["5", "7", "8"]),
        ("Nomor atom dari unsur gas Nitrogen (N) penyusun udara terbanyak adalah ...", "7", ["6", "8", "9"]),
        ("Nomor atom dari unsur gas Oksigen (O) di dalam tabel periodik adalah ...", "8", ["7", "9", "10"]),
        ("Nomor atom dari unsur halogen Fluorin (F) adalah ...", "9", ["8", "10", "11"]),
        ("Nomor atom dari unsur gas mulia Neon (Ne) adalah ...", "10", ["9", "11", "12"]),
        ("Nomor atom dari unsur logam alkali Natrium (Na) adalah ...", "11", ["10", "12", "13"]),
        ("Nomor atom dari unsur logam alkali tanah Magnesium (Mg) adalah ...", "12", ["11", "13", "14"]),
        ("Nomor atom dari unsur logam Aluminium (Al) adalah ...", "13", ["12", "14", "15"]),
        ("Nomor atom dari unsur semikonduktor Silikon (Si) adalah ...", "14", ["13", "15", "16"]),
        ("Nomor atom dari unsur non-logam Fosfor (P) adalah ...", "15", ["14", "16", "17"]),
        ("Nomor atom dari unsur Belerang (S) yang berwarna kuning adalah ...", "16", ["15", "17", "18"]),
        ("Nomor atom dari unsur halogen Klorin (Cl) adalah ...", "17", ["16", "18", "19"]),
        ("Nomor atom dari unsur gas mulia Argon (Ar) adalah ...", "18", ["17", "19", "20"]),
        ("Nomor atom dari unsur logam alkali Kalium (K) adalah ...", "19", ["18", "20", "21"]),
        ("Nomor atom dari unsur logam Kalsium (Ca) adalah ...", "20", ["19", "21", "22"]),
        ("Unsur logam yang sangat kuat, ringan, dan tahan korosi yang sering digunakan pada implan tulang dan bodi pesawat adalah Titanium dengan lambang ...", "Ti", ["Ta", "Tl", "Te"]),
        ("Unsur logam transisi berwarna keperakan yang banyak digunakan sebagai katalis dan elektrode sel bahan bakar adalah Platina dengan lambang ...", "Pt", ["Pl", "Pa", "Pb"]),
        ("Unsur gas mulia terberat yang bersifat radioaktif dan keluar dari rekahan batuan tanah adalah gas Radon dengan lambang ...", "Rn", ["Ra", "Rd", "Ro"]),
        ("Unsur radioaktif alami yang dahulu ditemukan oleh Marie Curie di dalam bijih uranium adalah Radium dengan lambang ...", "Ra", ["Rn", "Rd", "Ru"]),
        ("Unsur logam langka yang dinamai sesuai nama benua Eropa adalah Europium dengan lambang ...", "Eu", ["Er", "Es", "Ep"]),
        ("Unsur kimia buatan yang dinamai untuk menghormati ilmuwan Albert Einstein adalah Einsteinium dengan lambang ...", "Es", ["Ei", "Et", "En"]),
        ("Unsur kimia yang dinamai untuk menghormati penemu sistem periodik Dmitri Mendeleev adalah Mendelevium dengan lambang ...", "Md", ["Mv", "Me", "Ml"]),
    ]
    for q_text, corr, dists in elements_numbers_extra:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami nomor atom unsur dasar dan lambang kimia unsur periodik."))

    # 14. Konsep Mol, Stoikiometri & Sifat Koligatif (40 soal)
    mole_and_colligative = [
        ("Bilangan Avogadro yang menyatakan jumlah partikel (atom atau molekul) di dalam 1 mol zat bernilai ...", "6,02 x 10^23 partikel", ["3 x 10^8", "9,8 x 10^2", "1,6 x 10^-19"]),
        ("Massa satu mol zat yang dinyatakan dalam satuan gram per mol dinamakan ...", "Massa molar (Mr)", ["Massa jenis", "Massa relatif", "Berat jenis"]),
        ("Massa molekul relatif (Mr) dari molekul air murni (H2O) dengan Ar H = 1 dan O = 16 adalah ...", "18 gram/mol (2 + 16)", ["17 gram/mol", "20 gram/mol", "16 gram/mol"]),
        ("Massa molekul relatif (Mr) dari gas karbon dioksida (CO2) dengan Ar C = 12 dan O = 16 adalah ...", "44 gram/mol (12 + 32)", ["28 gram/mol", "32 gram/mol", "56 gram/mol"]),
        ("Volume 1 mol gas ideal apa pun pada kondisi standar (STP: 0 derajat C dan 1 atmosfer) bernilai tepat ...", "22,4 liter", ["24,0 liter", "11,2 liter", "44,8 liter"]),
        ("Banyaknya mol zat terlarut di dalam setiap 1 liter larutan dinamakan ...", "Molaritas (M)", ["Molalitas", "Fraksi mol", "Persen massa"]),
        ("Sifat larutan yang hanya bergantung pada jumlah partikel zat terlarut dan tidak bergantung pada jenis zat terlarutnya disebut ...", "Sifat Koligatif Larutan", ["Sifat intensif", "Sifat kualitatif", "Sifat termal"]),
        ("Empat sifat koligatif larutan adalah penurunan tekanan uap, kenaikan titik didih, penurunan titik beku, dan ...", "Tekanan osmosis", ["Kekentalan cairan", "Daya hantar listrik", "Tegangan permukaan"]),
        ("Air murni mendidih pada suhu 100 derajat C. Jika ke dalam air ditambahkan garam dapur, maka titik didih larutan garam akan ...", "Naik menjadi di atas 100 derajat Celcius", ["Turun di bawah 100 C", "Tetap 100 C", "Membeku"]),
        ("Fenomena kenaikan titik didih larutan saat ditambahi zat terlarut dinamakan ...", "Kenaikan titik didih (delta Tb)", ["Penurunan titik beku", "Tekanan uap", "Osmosis"]),
        ("Alasan petugas kebersihan di negara bermusim dingin menaburkan garam dapur atau kalsium klorida di jalan bersalju adalah untuk ...", "Menurunkan titik beku air sehingga salju mencair lebih cepat", ["Menghangatkan aspal jalan", "Mencegah debu jalanan", "Menambah gesekan ban saja"]),
        ("Peristiwa mengalirnya molekul pelarut dari larutan encer ke larutan yang lebih pekat melewati membran semipermeabel disebut ...", "Osmosis", ["Difusi", "Filtrasi", "Dialisis"]),
        ("Tekanan minimum yang diperlukan untuk menghentikan proses aliran osmosis dinamakan ...", "Tekanan osmosis", ["Tekanan hidrostatis", "Tekanan parsial", "Tekanan uap"]),
        ("Teknologi desalinasi air laut untuk mengubah air laut menjadi air minum tawar menggunakan membran bertekanan dinamakan ...", "Osmosis balik (Reverse Osmosis / RO)", ["Elektrodialisis", "Distilasi bertingkat", "Filtrasi kertas"]),
        ("Proses cuci darah bagi penderita gagal ginjal menggunakan mesin untuk menyaring racun darah bekerja berdasarkan prinsip pemisahan koloid yaitu ...", "Dialisis", ["Koagulasi", "Elektroforesis", "Kondensasi"]),
        ("Penggumpalan partikel-partikel koloid membentuk endapan besar (seperti penambahan tawas pada air keruh) dinamakan ...", "Koagulasi koloid", ["Peptisasi", "Emulsi", "Dialisis"]),
        ("Bahan kimia tawas (aluminium sulfat) yang sering ditambahkan ke dalam bak penampungan air sumur berfungsi untuk ...", "Menggumpalkan kotoran lumpur halus agar cepat mengendap ke dasar", ["Membunuh semua virus", "Membuat air berbau harum", "Menambah rasa manis"]),
    ]
    for q_text, corr, dists in mole_and_colligative:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami konsep mol, sifat koligatif larutan, osmosis, dan koagulasi koloid."))

    # 15. Radioisotop Medis & Gugus Fungsi Organik (40 soal)
    radioisotopes_and_organics = [
        ("Isotop radioaktif karbon-14 (C-14) banyak dimanfaatkan oleh arkeolog untuk ...", "Menentukan perkiraan umur fosil dan peninggalan purbakala", ["Mengobati kanker", "Pembangkit listrik", "Membasmi rayap"]),
        ("Isotop radioaktif Iodin-131 (I-131) banyak dimanfaatkan dalam dunia kedokteran untuk mendeteksi dan mengobati kelainan pada kelenjar ...", "Tiroid (Kelenjar gondok)", ["Pankreas", "Hati", "Jantung"]),
        ("Isotop radioaktif Kobalt-60 (Co-60) memancarkan sinar gamma yang digunakan untuk ...", "Radioterapi penghancur sel kanker dan sterilisasi alat medis", ["Penanggalan umur fosil", "Bahan bakar kapal selam", "Pewarna makanan"]),
        ("Isotop radioaktif Teknesium-99m (Tc-99m) paling banyak digunakan di rumah sakit modern untuk ...", "Pencitraan pemindaian medis organ jantung, otak, dan tulang", ["Pembedahan laser", "Sterilisasi air", "Pemberantas hama"]),
        ("Isotop Natrium-24 (Na-24) digunakan dalam bidang teknik sipil dan industri untuk ...", "Mendeteksi kebocoran pada pipa air atau minyak di bawah tanah", ["Mengawetkan ikan", "Bahan baterai", "Membuat semen"]),
        ("Isotop Fosfor-32 (P-32) digunakan dalam bidang pertanian untuk ...", "Mempelajari penyerapan pupuk fosfat oleh tanaman", ["Membasmi rumput liar", "Membuat buah manis", "Mencegah banjir"]),
        ("Senyawa hidrokarbon alifatik yang seluruh ikatan antar atom karbonnya berupa ikatan tunggal jenuh dinamakan ...", "Alkana (CnH2n+2)", ["Alkena", "Alkuna", "Benzena"]),
        ("Senyawa hidrokarbon yang memiliki setidaknya satu ikatan rangkap dua antar atom karbonnya dinamakan ...", "Alkena (CnH2n)", ["Alkana", "Alkuna", "Sikloalkana"]),
        ("Senyawa hidrokarbon yang memiliki setidaknya satu ikatan rangkap tiga antar atom karbonnya dinamakan ...", "Alkuna (CnH2n-2)", ["Alkana", "Alkena", "Alkohol"]),
        ("Senyawa organik yang memiliki gugus fungsi hidroksil (-OH) terikat pada rantai karbon dinamakan ...", "Alkohol (Alkanol)", ["Eter", "Aldehid", "Ester"]),
        ("Senyawa organik dengan gugus fungsi alkoksi (-O-) yang dahulu pernah digunakan sebagai obat bius umum adalah ...", "Eter (Alkoksi alkana)", ["Alkohol", "Keton", "Asam karboksilat"]),
        ("Senyawa organik beraroma wangi harum khas buah-buahan yang dihasilkan dari reaksi esterifikasi dinamakan ...", "Ester (Alkil alkanoat)", ["Eter", "Aldehid", "Keton"]),
        ("Ester isoamil asetat memiliki aroma wangi yang sangat khas menyerupai aroma ...", "Buah pisang", ["Buah nanas", "Buah apel", "Bunga mawar"]),
        ("Ester etil butirat memiliki aroma wangi yang menyerupai aroma buah ...", "Nanas", ["Pisang", "Jeruk", "Melon"]),
        ("Ester oktil asetat menghasilkan aroma wangi khas buah ...", "Jeruk", ["Pisang", "Apel", "Nanas"]),
        ("Senyawa organik dengan gugus karbonil di tengah rantai (-CO-) seperti aseton pembersih cat kuku tergolong golongan ...", "Keton (Alkanon)", ["Aldehid", "Eter", "Ester"]),
        ("Senyawa formalin yang digunakan untuk mengawetkan preparat biologi merupakan larutan dari gas ...", "Formaldehida (Metanal / Aldehid)", ["Aseton", "Asam asetat", "Etanol"]),
        ("Senyawa organik yang memiliki gugus karboksil (-COOH) dan berasa masam tergolong golongan ...", "Asam karboksilat (Asam alkanoat)", ["Alkohol", "Ester", "Keton"]),
        ("Senyawa hidrokarbon aromatik berbentuk cincin segi enam dengan rumus kimia C6H6 adalah ...", "Benzena", ["Sikloheksana", "Heksana", "Naftalena"]),
    ]
    for q_text, corr, dists in radioisotopes_and_organics:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami pemanfaatan radioisotop medis dan gugus fungsi senyawa organik."))

    # 16. Kimia Terapan & Reaksi Sehari-hari (50 soal)
    applied_daily_chemistry = [
        ("Kandungan senyawa kimia di dalam cairan pembersih porselen kamar mandi yang berbau tajam adalah ...", "Asam klorida (HCl)", ["Asam asetat", "Natrium klorida", "Air kapur"]),
        ("Bahan kimia yang terkandung di dalam kapur barus toilet yang dapat mengusir serangga kecoak adalah ...", "Paradichlorobenzene (PDCB) atau Naftalena", ["Kalsium karbonat", "Silika gel", "Baking soda"]),
        ("Reaksi pembentukan sabun dari reaksi antara minyak/lemak nabati dengan basa kuat (seperti NaOH) dinamakan reaksi ...", "Saponifikasi (Penyabunan)", ["Esterifikasi", "Netralisasi", "Hidrogenasi"]),
        ("Hasil sampingan yang bernilai ekonomi tinggi dari reaksi pembuatan sabun (saponifikasi) adalah ...", "Gliserol (Gliserin)", ["Alkohol murni", "Asam cuka", "Minyak goreng"]),
        ("Bahan aktif pada pasta gigi sensitif yang berfungsi menutup pori-pori dentin gigi adalah ...", "Kalium nitrat atau Stronsium klorida", ["Kalsium karbonat", "Natrium fluorida", "Mentol"]),
        ("Kandungan gas di dalam kaleng whipped cream atau aerosol yang bertindak sebagai gas pendorong makanan adalah ...", "Dinitrogen oksida (N2O)", ["Karbon monoksida", "Klorin", "Hidrogen"]),
        ("Batu baterai kancing pipih yang digunakan pada jam tangan dan kalkulator umumnya adalah baterai jenis ...", "Baterai perak oksida atau baterai lithium koin", ["Baterai aki timbal", "Baterai seng basah", "Baterai nuklir"]),
        ("Penyebab utama timbulnya karat hijau pada patung tembaga atau perunggu kuno di luar ruangan adalah pembentukan senyawa ...", "Patina (Tembaga karbonat basa / CuCO3 . Cu(OH)2)", ["Karat besi merah", "Belerang murni", "Emas pudar"]),
        ("Warna hijau toska yang melapisi permukaan Patung Liberty di Amerika Serikat berasal dari lapisan pelindung alami yaitu ...", "Patina tembaga", ["Cat hijau", "Lumut dan jamur", "Kotoran debu"]),
        ("Reaksi perubahan minyak cair menjadi margarin padat dilakukan dengan menambahkan gas hidrogen pada ikatan rangkap yang disebut reaksi ...", "Hidrogenasi lemak", ["Saponifikasi", "Fermentasi", "Oksidasi"]),
        ("Minyak kelapa sawit yang digunakan berkali-kali untuk menggoreng hingga berwarna hitam kecokelatan dinamakan ...", "Minyak jelantah", ["Minyak murni", "Minyak zaitun", "Minyak jarak"]),
        ("Minyak jelantah berbahaya bagi kesehatan jantung jika terus dikonsumsi karena kaya akan kandungan ...", "Asam lemak trans dan radikal bebas karsinogenik", ["Vitamin A dan E", "Protein tinggi", "Omega 3"]),
        ("Zat kimia di dalam cabai yang menimbulkan sensasi rasa pedas membakar di lidah adalah ...", "Kapsaisin (Capsaicin)", ["Kafein", "Piperin", "Alisin"]),
        ("Cara paling efektif untuk meredakan rasa pedas di lidah adalah meminum ...", "Susu hangat (mengandung protein kasein yang melarutkan kapsaisin)", ["Air es dingin berulang kali", "Minuman bersoda", "Air garam"]),
        ("Zat kimia khas di dalam rempah lada atau merica yang menimbulkan rasa hangat pedas adalah ...", "Piperin", ["Kapsaisin", "Alisin", "Kurkumin"]),
        ("Zat kimia antibakteri khas yang terkandung di dalam bawang putih yang telah dimemarkan adalah ...", "Alisin", ["Kapsaisin", "Kafein", "Kurkumin"]),
        ("Zat aktif antioksidan alami yang memberikan warna kuning khas pada rimpang kunyit adalah ...", "Kurkumin", ["Klorofil", "Karoten", "Antosianin"]),
        ("Pigmen alami yang memberikan warna ungu kemerahan pada buah naga, ubi ungu, dan bunga telang adalah ...", "Antosianin", ["Klorofil", "Kurkumin", "Karotenoid"]),
        ("Pigmen alami berwarna oranye pada wortel dan labu kuning yang merupakan provitamin A adalah ...", "Beta-karoten", ["Klorofil", "Antosianin", "Lutein"]),
        ("Pigmen merah alami yang banyak terdapat pada buah tomat dan semangka yang baik untuk kesehatan prostat adalah ...", "Likopen (Lycopene)", ["Klorofil", "Antosianin", "Kurkumin"]),
    ]
    for q_text, corr, dists in applied_daily_chemistry:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami kimia makanan, bumbu dapur, reaksi saponifikasi, dan pigmen alami."))

    # 17. Laju Reaksi, Kesetimbangan & Kimia Sehari-hari (80 soal)
    reaction_rates_and_applied = [
        ("Energi kinetik minimum yang harus dimiliki oleh partikel-partikel zat yang bertumbukan agar dapat menghasilkan reaksi kimia dinamakan ...", "Energi Aktivasi (Ea)", ["Energi Potensial", "Energi Ikatan", "Entalpi"]),
        ("Peran utama katalisator dalam mempercepat laju terjadinya suatu reaksi kimia adalah dengan cara ...", "Menurunkan nilai energi aktivasi reaksi", ["Menaikkan suhu larutan", "Menambah jumlah zat hasil", "Menaikkan tekanan ruang"]),
        ("Jika suhu suatu reaksi dinaikkan, maka laju reaksi kimia akan berlangsung ...", "Jauh lebih cepat karena partikel bergerak lebih lincah dan sering bertumbukan", ["Jauh lebih lambat", "Tetap konstan", "Berhenti"]),
        ("Aturan praktis kinetika kimia menyatakan bahwa setiap kenaikan suhu sebesar 10 derajat Celcius akan menyebabkan laju reaksi ...", "Menjadi 2 hingga 3 kali lebih cepat", ["Menjadi separuh", "Tetap sama", "Menjadi 10 kali"]),
        ("Gula pasir berbentuk butiran halus lebih cepat larut di dalam air dibandingkan dengan sebongkah gula batu karena ...", "Luas permukaan bidang sentuh gula halus jauh lebih besar", ["Massa gula halus lebih ringan", "Gula batu tidak manis", "Gula batu mengandung garam"]),
        ("Daging sapi yang dipotong kecil-kecil lebih cepat matang saat dimasak dibandingkan sepotong daging utuh besar karena ...", "Luas permukaan sentuh panas lebih besar", ["Daging kecil lebih empuk", "Bumbu lebih asin", "Suhu kompor naik"]),
        ("Bahan makanan yang disimpan di dalam lemari es (kulkas) menjadi lebih awet dan tidak cepat basi karena ...", "Suhu dingin memperlambat laju reaksi pembusukan oleh bakteri", ["Bakteri mati total membeku", "Kulkas hampa udara", "Kulkas menyerap air"]),
        ("Reaksi kimia yang dapat berlangsung bolak-balik di mana produk dapat bereaksi kembali membentuk reaktan dinamakan reaksi ...", "Reversibel (Dapat balik)", ["Irreversibel", "Searah", "Statis"]),
        ("Keadaan di mana laju reaksi maju sama persis dengan laju reaksi balik pada wadah tertutup dinamakan ...", "Kesetimbangan kimia dinamis", ["Kesetimbangan statis", "Reaksi tuntas", "Endapan jenuh"]),
        ("Asas yang menyatakan bahwa jika pada suatu sistem kesetimbangan diberikan aksi gangguan maka sistem akan bergeser mengurangi gangguan tersebut adalah ...", "Asas Le Chatelier", ["Hukum Hess", "Hukum Raoult", "Hukum Faraday"]),
        ("Pada sistem kesetimbangan kimia, jika suhu dinaikkan maka posisi kesetimbangan akan bergeser ke arah reaksi ...", "Endoterm (yang menyerap kalor)", ["Eksoterm", "Kiri saja", "Kanan saja"]),
        ("Pada sistem kesetimbangan gas, jika tekanan diperbesar (volume diperkecil), maka kesetimbangan akan bergeser ke arah ...", "Jumlah koefisien gas yang lebih kecil", ["Jumlah koefisien lebih besar", "Reaksi endoterm", "Tidak bergeser"]),
        ("Air sadah sementara yang mengandung senyawa kalsium bikarbonat Ca(HCO3)2 dapat dihilangkan kesadahannya dengan cara mudah yaitu ...", "Memanaskan atau mendidihkan air sampai matang", ["Menyaring dengan kapas", "Menambahkan garam dapur", "Mendinginkan di freezer"]),
        ("Air sadah tetap yang mengandung kalsium klorida (CaCl2) atau magnesium sulfat (MgSO4) dapat dihilangkan dengan cara menambahkan ...", "Soda abu (Natrium Karbonat / Na2CO3)", ["Cuka makan", "Gula pasir", "Asam sitrat"]),
        ("Garam konsumsi dapur di Indonesia wajib diperkaya dengan senyawa kalium iodat (KIO3) yang bertujuan untuk mencegah penyakit ...", "Gondok dan kretinisme (kekerdilan mental)", ["Diabetes melitus", "Maag kronis", "Kanker paru"]),
        ("Logam natrium (Na) dan kalium (K) murni harus disimpan terendam di dalam minyak tanah atau parafin cair karena ...", "Sangat reaktif dan dapat meledak terbakar jika terkena udara lembap atau air", ["Dapat menguap menjadi gas", "Dapat berkarat hitam", "Mudah meleleh"]),
        ("Logam aluminium tidak mudah keropos dimakan karat seperti besi karena pada permukaannya terbentuk ...", "Lapisan tipis aluminium oksida (Al2O3) yang sangat rapat dan melindungi logam di dalamnya", ["Lapisan cat alami", "Minyak pelindung", "Lapisan lilin"]),
        ("Bahan baku utama yang digunakan dalam industri pembuatan kaca jendela bening adalah pasir silika yang mengandung senyawa ...", "Silikon dioksida (SiO2)", ["Kalsium karbonat", "Natrium hidroksida", "Aluminium oksida"]),
        ("Bahan baku utama tanah liat putih halus yang digunakan dalam industri keramik porselen dan tembikar adalah ...", "Kaolin (Aluminosilikat)", ["Pasir kuarsa", "Batu kapur", "Bauksit"]),
        ("Bahan perekat bangunan semen Portland dibuat dengan memanaskan campuran batu kapur, pasir silika, dan ...", "Tanah liat (Lempung) serta sedikit gips", ["Pasir laut", "Garam dapur", "Batu bara"]),
        ("Zat kimia pengembang adonan kue baking powder mengandung campuran soda kue (baking soda) dengan ...", "Zat asam padat (seperti krim tartar) dan pati jagung", ["Garam dapur", "Cuka cair", "Ragi basah"]),
        ("Serbuk pemutih pakaian klorin padat yang sering digunakan untuk menjernihkan air sumur dan kolam renang adalah ...", "Kaporit (Kalsium hipoklorit / Ca(OCl)2)", ["Garam dapur", "Tawas", "Soda kue"]),
        ("Gas kimia berbau khas yang dikeluarkan oleh buah pisang yang sedang matang dan dapat memicu pematangan buah lain di sekitarnya adalah ...", "Gas Etilena (Etena / C2H4)", ["Gas Metana", "Gas Karbon Dioksida", "Gas Nitrogen"]),
        ("Pedagang buah sering memeram buah mentah agar cepat matang menggunakan batu karbit (CaC2) yang melepaskan gas ...", "Gas Asetilena (Etuna)", ["Gas Oksigen", "Gas Karbon Monoksida", "Gas Butana"]),
        ("Zat aditif makanan yang ditambahkan pada keripik kentang atau minyak goreng untuk mencegah ketengikan akibat oksidasi adalah antioksidan sintetis ...", "BHA dan BHT", ["Formalin dan Boraks", "Sakarin dan Siklamat", "MSG dan Garam"]),
        ("Senyawa gas CFC (klorofluorokarbon) pada masa lalu banyak digunakan sebagai zat pendingin pada kulkas dan AC karena memiliki sifat ...", "Stabil, tidak mudah terbakar, dan tidak beracun secara langsung", ["Sangat wangi", "Harganya mahal", "Berwarna hijau"]),
        ("Alasan senyawa gas CFC dilarang penggunaannya melalui Protokol Montreal adalah karena ...", "Atom klorin dari CFC memecah dan merusak lapisan molekul ozon di stratosfer", ["Menyebabkan banjir bandang", "Membuat udara berbau busuk", "Memicu gempa"]),
        ("Peristiwa perubahan warna apel atau kentang yang dikupas menjadi kecokelatan saat dibiarkan di udara terbuka dinamakan reaksi ...", "Pencokelatan enzimatis (Browning)", ["Fermentasi ragi", "Saponifikasi", "Pembusukan anaerob"]),
        ("Cara sederhana untuk mencegah apel yang telah dipotong agar tidak berubah warna cokelat adalah dengan ...", "Merendamnya sebentar dalam air perasan jeruk lemon (mengandung vitamin C antioksidan)", ["Menaburkan garam banyak", "Memanaskan di oven", "Mencelupkan ke minyak"]),
        ("Bahan kimia yang terkandung di dalam obat tetes mata untuk meredakan mata merah akibat iritasi ringan adalah vasokonstriktor ...", "Tetrahidrozolin hidroklorida", ["Asam sulfat pekat", "Parasetamol", "Amoksisilin"]),
    ]
    for q_text, corr, dists in reaction_rates_and_applied:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami faktor laju reaksi, kesetimbangan kimia, dan kimia praktis sehari-hari."))

    # 18. Polimer, Plastik & Karet Vulkanisasi (50 soal)
    polymers_and_plastics = [
        ("Molekul raksasa rantai panjang yang terbentuk dari gabungan ratusan hingga ribuan unit molekul kecil berulang dinamakan ...", "Polimer (Makromolekul)", ["Monomer", "Isomer", "Isotop"]),
        ("Unit molekul tunggal terkecil yang menjadi bahan penyusun rantai polimer dinamakan ...", "Monomer", ["Polimer", "Dimer", "Oligomer"]),
        ("Reaksi kimia penggabungan molekul-molekul monomer menjadi rantai polimer panjang dinamakan reaksi ...", "Polimerisasi", ["Saponifikasi", "Esterifikasi", "Hidrolisis"]),
        ("Kelompok polimer yang terbentuk secara alami di dalam tubuh makhluk hidup dinamakan polimer alam, contohnya adalah ...", "Karet alam, selulosa, amilum, dan protein", ["Plastik kresek dan pipa paralon", "Nilon dan teflon", "Styrofoam dan dakron"]),
        ("Contoh polimer sintetis buatan manusia yang tidak ada di alam adalah ...", "Plastik polietilena, nilon, teflon, dan PVC", ["Protein dan DNA", "Karet lateks dan wol", "Kapas dan sutra"]),
        ("Monomer penyusun polimer alami karet alam dari getah lateks adalah ...", "Isoprena (2-metil-1,3-butadiena)", ["Etena", "Glukosa", "Stirena"]),
        ("Monomer penyusun polimer karbohidrat pati (amilum) dan selulosa adalah ...", "Glukosa", ["Fruktosa", "Asam amino", "Gliserol"]),
        ("Monomer penyusun polimer alami protein adalah ...", "Asam amino", ["Asam lemak", "Glukosa", "Nukleotida"]),
        ("Monomer penyusun polimer plastik kantong kresek (Polietilena / PE) adalah ...", "Etena (Etilena)", ["Propena", "Vinil klorida", "Stirena"]),
        ("Monomer penyusun plastik pipa paralon saluran air (Polivinil Klorida / PVC) adalah ...", "Vinil klorida (Kloroetena)", ["Etena", "Tetrafluoroetena", "Akrilat"]),
        ("Monomer penyusun plastik gabus putih peredam getaran (Polistirena / Styrofoam) adalah ...", "Stirena", ["Etena", "Propena", "Isoprena"]),
        ("Monomer penyusun bahan pelapis wajan antilengket Teflon (PTFE) adalah ...", "Tetrafluoroetena", ["Vinil klorida", "Etena", "Stirena"]),
        ("Serat sintetis kuat dan lentur yang banyak digunakan untuk tali pancing dan bulu sikat gigi adalah ...", "Nilon", ["Katun", "Sutra", "Wol"]),
        ("Bahan serat sintetis pengisi bantal dan boneka yang lembut dan empuk adalah ...", "Dakron (Poliester)", ["Nilon", "PVC", "Teflon"]),
        ("Jenis plastik yang dapat melunak dan meleleh saat dipanaskan sehingga dapat didaur ulang dibentuk kembali dinamakan ...", "Termoplastik", ["Termoset", "Elastomer", "Serat"]),
        ("Contoh kelompok plastik termoplastik yang dapat didaur ulang adalah ...", "Botol PET, botol sampo HDPE, dan kantong PE", ["Bakelit sakelar listrik", "Piring melamin", "Resin epoksi"]),
        ("Jenis plastik yang tidak melunak saat dipanaskan melainkan akan hangus atau rusak dan tidak dapat didaur ulang dinamakan ...", "Termoset", ["Termoplastik", "Elastomer", "Koloid"]),
        ("Plastik termoset tahan panas dan isolator listrik yang digunakan sebagai bahan wadah sakelar dan steker listrik adalah ...", "Bakelit", ["Polietilena", "PVC", "Styrofoam"]),
        ("Plastik keras tahan benturan yang sering digunakan untuk piring dan mangkok tahan pecah di rumah makan adalah ...", "Melamin", ["PET", "Polietilena", "PVC"]),
        ("Proses pemanasan karet alam mentah bersama belerang (sulfur) agar karet menjadi elastis, kuat, dan tahan gesekan dinamakan ...", "Vulkanisasi karet", ["Saponifikasi", "Polimerisasi adisi", "Galvanisasi"]),
        ("Tokoh penemu proses vulkanisasi karet yang namanya diabadikan menjadi merk ban mobil terkenal adalah ...", "Charles Goodyear", ["John Dunlop", "Edouard Michelin", "Nikola Tesla"]),
        ("Sebelum ditemukan proses vulkanisasi, karet alam mentah memiliki kelemahan utama yaitu ...", "Sangat lengket jika cuaca panas dan menjadi rapuh patah jika cuaca dingin", ["Mudah meledak", "Sangat berat", "Beracun mematikan"]),
        ("Karet vulkanisasi yang dicampur dengan karbon hitam banyak dimanfaatkan oleh industri untuk memproduksi ...", "Ban kendaraan mobil dan sepeda motor", ["Baju kaos katun", "Pipa paralon", "Piring makan"]),
        ("Plastik dengan kode daur ulang nomor 1 berbentuk segitiga adalah jenis plastik ...", "PET / PETE (Polietilena Tereftalat)", ["HDPE", "PVC", "LDPE"]),
        ("Plastik dengan kode daur ulang nomor 2 segitiga untuk botol deterjen dan botol sampo tebal adalah ...", "HDPE (High Density Polyethylene)", ["PET", "PVC", "PP"]),
        ("Plastik dengan kode daur ulang nomor 5 segitiga yang paling aman dan tahan panas untuk kotak bekal makanan adalah ...", "PP (Polipropilena)", ["PVC", "PS", "PET"]),
        ("Plastik dengan kode daur ulang nomor 6 segitiga yang sebaiknya dihindari untuk makanan panas berlemak adalah ...", "PS (Polistirena / Styrofoam)", ["PP", "HDPE", "PET"]),
    ]
    for q_text, corr, dists in polymers_and_plastics:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami polimer alam, polimer sintetis, plastik, dan vulkanisasi karet."))

    # 19. Fakta Kimia Menarik & Sehari-hari (20 soal)
    fun_chemistry_facts = [
        ("Pengisian gas nitrogen murni pada ban kendaraan bermotor disukai karena ...", "Tekanan ban lebih stabil, tidak cepat panas, dan tidak mengandung uap air penyebab karat", ["Membuat ban menjadi sangat ringan melayang", "Ban tidak akan pernah bocor tertusuk paku", "Menghasilkan suara lebih halus"]),
        ("Es kering (dry ice) yang digunakan untuk mendinginkan es krim adalah bentuk padat dari senyawa ...", "Karbon Dioksida (CO2) beku pada suhu -78,5 derajat C", ["Air murni beku", "Gas nitrogen cair", "Oksigen padat"]),
        ("Menghirup gas helium dari balon pesta dapat membuat suara manusia menjadi melengking lucu seperti tokoh kartun karena ...", "Kecepatan rambat suara di gas helium jauh lebih cepat daripada di udara", ["Helium menciutkan pita suara", "Helium mendinginkan tenggorokan", "Helium menaikkan frekuensi paru"]),
        ("Pembersih pemutih pakaian (mengandung NaOCl) dilarang keras dicampur dengan pembersih toilet (mengandung HCl) karena ...", "Akan melepaskan gas klorin (Cl2) yang sangat beracun dan mematikan paru-paru", ["Akan menimbulkan ledakan api besar", "Warna lantai menjadi ungu", "Sabun kehilangan busa"]),
        ("Tablet norit (karbon aktif) diminum saat keracunan makanan atau diare karena bekerja dengan cara ...", "Mengadsorpsi (menyerap) racun dan gas pada permukaan pori-porinya lalu dibuang", ["Membunuh bakteri dengan asam", "Mencerna makanan cepat", "Menetralkan air liur"]),
        ("Alasan es batu dapat terapung di atas permukaan air adalah karena ...", "Massa jenis es (0,92 g/cm3) lebih kecil daripada massa jenis air cair (1 g/cm3)", ["Es mengandung banyak gelembung udara", "Air menolak zat padat", "Suhu es sangat dingin"]),
        ("Senyawa aktif utama yang terkandung di dalam minyak kayu putih yang memberikan rasa hangat adalah ...", "Sineol (Eukaliptol)", ["Kapsaisin", "Alisin", "Eugenol"]),
        ("Senyawa aktif di dalam minyak cengkeh yang berkhasiat antiseptik dan pereda rasa nyeri sakit gigi adalah ...", "Eugenol", ["Sineol", "Mentol", "Piperin"]),
        ("Kristal mentol yang memberikan sensasi dingin semriwing pada pasta gigi dan permen diekstrak dari tanaman ...", "Daun mint (Mentha arvensis)", ["Daun teh", "Daun sirih", "Daun salam"]),
        ("Atom logam yang menjadi pusat pengikat pada molekul zat hijau daun (klorofil) adalah atom ...", "Magnesium (Mg)", ["Besi (Fe)", "Kalsium (Ca)", "Tembaga (Cu)"]),
        ("Atom logam yang menjadi pusat pengikat oksigen pada molekul hemoglobin sel darah merah adalah atom ...", "Besi (Fe)", ["Magnesium (Mg)", "Seng (Zn)", "Timbal (Pb)"]),
        ("Zat racun sianida (CN-) sangat berbahaya dan mematikan karena bekerja dengan cara ...", "Mengikat zat besi pada enzim respirasi seluler sehingga sel tubuh tidak bisa menggunakan oksigen", ["Membekukan darah di jantung", "Melarutkan dinding lambung", "Menghancurkan sel darah merah"]),
        ("Logam mulia emas tidak bereaksi dengan asam tunggal biasa, namun hanya dapat larut dalam campuran asam pekat khusus yaitu ...", "Air raja (Aqua Regia / campuran asam klorida dan asam nitrat)", ["Air aki pekat", "Cuka makan murni", "Air kapur mendidih"]),
        ("Perbandingan campuran asam pada larutan air raja (Aqua Regia) pelarut emas adalah ...", "3 bagian HCl pekat dan 1 bagian HNO3 pekat", ["1 bagian HCl dan 3 bagian HNO3", "1 bagian H2SO4 dan 1 bagian HCl", "Semua asam sama"]),
        ("Bahan bakar alternatif ramah lingkungan yang diproduksi dari fermentasi karbohidrat tetes tebu adalah ...", "Bioetanol", ["Biodiesel", "Biogas", "Bensin pertamax"]),
        ("Senyawa ester amil asetat yang dihasilkan secara sintetis memiliki aroma wangi yang sering digunakan sebagai ...", "Perisa aroma pisang pada sirup dan kue", ["Pembersih kaca", "Bahan pengawet ikan", "Pelarut cat kuku"]),
        ("Zat kimia pemanis buatan sakarin memiliki tingkat kemanisan sekitar ...", "300 hingga 500 kali lebih manis dibanding gula pasir", ["2 kali lebih manis", "10 kali lebih manis", "Sama dengan gula"]),
        ("Pemanis buatan aspartam tidak boleh dikonsumsi oleh penderita kelainan genetik langka yaitu penyakit ...", "Fenilketonuria (PKU)", ["Diabetes melitus", "Hipertensi", "Anemia"]),
        ("Proses penyulingan minyak atsiri wangi dari bunga mawar atau melati di industri parfum menggunakan metode ...", "Distilasi uap", ["Filtrasi", "Sublimasi", "Kristalisasi"]),
        ("Batu gamping kalsium karbonat jika ditetesi dengan larutan asam klorida encer akan bereaksi melepaskan gelembung gas ...", "Karbon Dioksida (CO2)", ["Gas Hidrogen", "Gas Oksigen", "Gas Belerang"]),
    ]
    for q_text, corr, dists in fun_chemistry_facts:
        add_q(build_mcq("Kimia", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami kimia sehari-hari, sifat es kering, norit karbon aktif, dan aqua regia."))

    return questions[:500]
