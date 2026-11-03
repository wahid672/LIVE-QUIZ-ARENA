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

    # 1. Konsep Dasar Ekonomi & Kelangkaan (50 soal)
    scarcity_and_fundamentals = [
        ("Istilah ekonomi berasal dari bahasa Yunani yaitu 'oikonomia' yang terbentuk dari kata 'oikos' dan 'nomos' yang memiliki arti ...", "Aturan rumah tangga", ["Hukum pasar", "Perdagangan barang", "Keuangan negara"]),
        ("Tokoh filsuf dan ekonom asal Skotlandia yang dijuluki sebagai 'Bapak Ilmu Ekonomi' modern adalah ...", "Adam Smith", ["David Ricardo", "John Maynard Keynes", "Karl Marx"]),
        ("Buku mahakarya Adam Smith yang terbit pada tahun 1776 dan menjadi tonggak ilmu ekonomi berjudul ...", "The Wealth of Nations", ["Das Kapital", "General Theory", "Principles of Economics"]),
        ("Inti masalah ekonomi yang paling mendasar dihadapi oleh setiap manusia adalah adanya ...", "Kelangkaan (Kebutuhan tak terbatas sedangkan alat pemuas terbatas)", ["Kekurangan uang tunai", "Banyaknya lapangan kerja", "Tingginya harga sembako"]),
        ("Kondisi di mana sumber daya yang tersedia tidak cukup untuk memenuhi semua kebutuhan manusia dinamakan ...", "Kelangkaan (Scarcity)", ["Kemiskinan", "Krisis moneter", "Inflasi"]),
        ("Biaya yang dikorbankan karena memilih suatu alternatif pilihan terbaik lainnya dinamakan biaya ...", "Peluang (Opportunity Cost)", ["Produksi", "Variabel", "Tetap"]),
        ("Seseorang memilih kuliah di perguruan tinggi dan melepas tawaran kerja bergaji Rp 4 juta per bulan. Gaji yang dilepas tersebut dinamakan biaya ...", "Peluang (Opportunity Cost)", ["Tetap", "Marginal", "Operasional"]),
        ("Daftar susunan kebutuhan manusia yang diurutkan berdasarkan tingkat kepentingan yang paling mendesak disebut ...", "Skala prioritas", ["Skala kebutuhan", "Anggaran belanja", "Daftar belanjaan"]),
        ("Barang yang untuk mendapatkannya memerlukan pengorbanan berupa uang atau tenaga dinamakan barang ...", "Ekonomi", ["Bebas", "Illith", "Konsumsi"]),
        ("Contoh barang ekonomi yang harus dibeli dengan uang adalah ...", "Beras, pakaian, dan buku tulis", ["Sinar matahari di pantai", "Udara pernapasan di taman", "Air laut di samudra"]),
        ("Barang yang ketersediaannya melimpah di alam dan dapat diperoleh tanpa pengorbanan dinamakan barang ...", "Bebas", ["Ekonomi", "Illith", "Substitusi"]),
        ("Contoh barang bebas yang tersedia melimpah di alam adalah ...", "Udara pernapasan dan sinar matahari", ["Beras dan sayuran", "Air mineral kemasan", "Bensin pertalite"]),
        ("Barang yang jika jumlahnya berlebihan justru dapat merugikan atau membahayakan manusia dinamakan barang ...", "Illith", ["Bebas", "Ekonomi", "Komplementer"]),
        ("Contoh barang illith adalah air dan api yang jika jumlahnya terlalu berlebihan dapat menimbulkan ...", "Banjir bandang dan kebakaran hebat", ["Kekeringan", "Pencemaran udara", "Krisis pangan"]),
        ("Barang yang dapat langsung digunakan oleh manusia untuk memenuhi kebutuhannya dinamakan barang ...", "Konsumsi", ["Produksi", "Modal", "Setengah jadi"]),
        ("Barang yang digunakan sebagai alat bantu untuk menghasilkan barang lain dinamakan barang ...", "Produksi (Barang modal)", ["Konsumsi", "Bebas", "Akhir"]),
        ("Contoh barang modal (barang produksi) di pabrik konveksi pakaian adalah ...", "Mesin jahit dan kain bahan", ["Baju jadi di etalase", "Makanan siang karyawan", "Sepatu pembeli"]),
        ("Bahan alami yang belum mengalami proses pengolahan sama sekali seperti kayu gelondongan dan kapas dinamakan ...", "Bahan mentah (Baku)", ["Barang setengah jadi", "Barang jadi", "Barang modal"]),
        ("Barang yang sudah mengalami proses pengolahan tetapi masih perlu diproses lagi menjadi barang jadi dinamakan barang ...", "Setengah jadi", ["Mentah", "Jadi", "Bebas"]),
        ("Contoh barang setengah jadi adalah ...", "Benang pintal dan tepung terigu", ["Kapas di pohon", "Baju kemeja siap pakai", "Roti matang"]),
        ("Barang yang sudah siap untuk langsung dipakai atau dikonsumsi oleh konsumen dinamakan barang ...", "Jadi", ["Setengah jadi", "Mentah", "Modal"]),
        ("Dua barang yang memiliki fungsi saling menggantikan satu sama lain dinamakan barang ...", "Substitusi", ["Komplementer", "Modal", "Bebas"]),
        ("Contoh pasangan barang substitusi (saling menggantikan) adalah ...", "Beras dengan jagung atau kopi dengan teh", ["Sepatu dengan kaos kaki", "Mobil dengan bensin", "Kompor gas dengan tabung gas"]),
        ("Dua barang yang harus digunakan secara bersama-sama agar dapat berfungsi dinamakan barang ...", "Komplementer (Pelengkap)", ["Substitusi", "Bebas", "Ekonomi"]),
        ("Contoh pasangan barang komplementer (saling melengkapi) adalah ...", "Sepeda motor dengan bensin", ["Beras dengan ubi", "Kopi dengan teh", "Pulpen dengan pensil"]),
        ("Tiga masalah pokok dalam ekonomi klasik yang dikemukakan oleh para ahli adalah masalah ...", "Produksi, Distribusi, dan Konsumsi", ["What, How, dan For Whom", "Uang, Pasar, dan Modal", "Pajak, Utang, dan Bunga"]),
        ("Tiga masalah pokok dalam ekonomi modern adalah apa yang diproduksi, bagaimana cara memproduksi, dan ...", "Untuk siapa barang diproduksi (For whom)", ["Di mana barang diproduksi", "Kapan barang dijual", "Berapa banyak uang dipinjam"]),
        ("Pertanyaan 'Barang apa yang akan diproduksi dan berapa banyak jumlahnya' dalam ekonomi modern disebut masalah ...", "What", ["How", "For Whom", "When"]),
        ("Pertanyaan mengenai teknologi atau metode apa yang digunakan dalam proses produksi adalah masalah ...", "How", ["What", "For Whom", "Where"]),
        ("Pertanyaan mengenai siapa sasaran konsumen yang akan menikmati hasil produksi adalah masalah ...", "For Whom", ["What", "How", "Why"]),
        ("Sistem ekonomi di mana seluruh kegiatan ekonomi diatur secara adat istiadat turun-temurun dinamakan sistem ekonomi ...", "Tradisional", ["Komando (Terpusat)", "Pasar (Liberal)", "Campuran"]),
        ("Sistem ekonomi di mana seluruh keputusan produksi, distribusi, dan harga ditentukan secara mutlak oleh pemerintah pusat adalah ...", "Sistem ekonomi komando (Terpusat / Sosialis)", ["Sistem ekonomi pasar", "Sistem ekonomi tradisional", "Sistem ekonomi campuran"]),
        ("Sistem ekonomi di mana seluruh kegiatan ekonomi diserahkan sepenuhnya kepada mekanisme pasar bebas dan swasta adalah sistem ...", "Pasar (Kapitalis / Liberal)", ["Komando", "Tradisional", "Campuran"]),
        ("Ciri utama sistem ekonomi pasar bebas (kapitalis) adalah adanya ...", "Kebebasan individu memiliki modal dan persaingan bebas", ["Pemerintah memonopoli seluruh usaha", "Tidak ada uang yang beredar", "Harga ditetapkan presiden"]),
        ("Sistem ekonomi yang memadukan kebaikan sistem ekonomi komando dan sistem ekonomi pasar bebas dinamakan ...", "Sistem ekonomi campuran", ["Tradisional", "Feodal", "Merkantilis"]),
        ("Sistem ekonomi yang dianut oleh negara Indonesia berdasarkan Pasal 33 UUD 1945 adalah sistem ekonomi ...", "Demokrasi Ekonomi (Pancasila)", ["Kapitalis liberal", "Komunis terpusat", "Tradisional murni"]),
        ("Pasal 33 ayat 1 UUD 1945 menegaskan bahwa perekonomian disusun sebagai usaha bersama berdasar atas asas ...", "Kekeluargaan", ["Persaingan bebas", "Monopoli negara", "Bunga pinjaman"]),
        ("Pasal 33 ayat 2 UUD 1945 menyatakan bahwa cabang-cabang produksi yang penting bagi negara dan menguasai hajat hidup orang banyak dikuasai oleh ...", "Negara", ["Swasta asing", "Individu kaya", "Bank swasta"]),
        ("Pasal 33 ayat 3 UUD 1945 menegaskan bahwa bumi, air, dan kekayaan alam yang terkandung di dalamnya dikuasai oleh negara dan dipergunakan untuk ...", "Sebesar-besar kemakmuran rakyat", ["Keuntungan pejabat", "Membayar utang", "Pengusaha besar"]),
        ("Prinsip ekonomi bagi produsen adalah menghasilkan barang berkualitas baik dengan ...", "Biaya produksi seefisien mungkin untuk meraih laba maksimal", ["Biaya setinggi mungkin", "Merugikan pembeli", "Menimbun stok"]),
        ("Prinsip ekonomi bagi konsumen adalah mengalokasikan pendapatan yang dimilikinya untuk memperoleh ...", "Kepuasan maksimal (Utilitas tertinggi)", ["Hutang sebanyak-banyaknya", "Barang termahal", "Gengsi sosial"]),
        ("Analisis ekonomi yang mempelajari perilaku pelaku ekonomi secara individual seperti rumah tangga dan perusahaan dinamakan ...", "Ekonomi mikro", ["Ekonomi makro", "Ekonomi moneter", "Ekonomi internasional"]),
        ("Analisis ekonomi yang mempelajari mekanisme perekonomian secara keseluruhan (agregat) seperti inflasi dan pengangguran dinamakan ...", "Ekonomi makro", ["Ekonomi mikro", "Ekonomi manajerial", "Ekonomi perusahaan"]),
        ("Bagian ilmu ekonomi yang mendeskripsikan fakta-fakta peristiwa ekonomi di lapangan apa adanya dinamakan ekonomi ...", "Deskriptif", ["Teori", "Terapan", "Normatif"]),
        ("Pernyataan ekonomi yang mengandung penilaian nilai moral atau saran tentang apa yang seharusnya dilakukan disebut ekonomi ...", "Normatif", ["Positif", "Deskriptif", "Eksak"]),
        ("Pernyataan ekonomi yang menjelaskan hubungan sebab akibat sesuai kenyataan tanpa penilaian subjektif dinamakan ekonomi ...", "Positif", ["Normatif", "Agamis", "Filosofis"]),
    ]
    for q_text, corr, dists in scarcity_and_fundamentals:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami konsep kelangkaan, biaya peluang, sistem ekonomi, dan prinsip ekonomi."))

    # 2. Pelaku Ekonomi & Faktor Produksi (50 soal)
    economic_agents_factors = [
        ("Empat pelaku utama dalam kegiatan perekonomian suatu negara adalah ...", "RTK, RTP, RTN (Pemerintah), dan MLN (Luar Negeri)", ["Petani, Nelayan, Buruh, dan Bos", "Bank, Koperasi, Pasar, dan Toko", "DPR, Presiden, Menteri, dan Hakim"]),
        ("Rumah Tangga Konsumen (RTK) memiliki dua peran utama yaitu sebagai konsumen pemakai barang dan sebagai penyedia ...", "Faktor-faktor produksi", ["Uang kertas", "Undang-undang", "Kredit"]),
        ("Empat faktor produksi utama yang disediakan oleh Rumah Tangga Konsumen adalah ...", "Alam (Tanah), Tenaga Kerja, Modal, dan Kewirausahaan", ["Uang, Emas, Saham, dan Obligasi", "Gedung, Mesin, Kendaraan, dan Listrik", "Padi, Minyak, Gas, dan Baja"]),
        ("Balas jasa yang diterima pemilik faktor produksi tanah atau alam atas pemakaian lahannya dinamakan ...", "Sewa (Rent)", ["Upah", "Bunga", "Laba"]),
        ("Balas jasa yang diterima oleh tenaga kerja atas jasa dan tenaga yang disumbangkannya adalah ...", "Upah / Gaji (Wage)", ["Sewa", "Laba", "Bunga modal"]),
        ("Balas jasa yang diterima oleh pemilik faktor produksi modal atas peminjaman modalnya dinamakan ...", "Bunga modal (Interest)", ["Laba", "Upah", "Sewa"]),
        ("Balas jasa yang diterima oleh seorang wirausahawan atas keahlian dan risiko mengelola usaha dinamakan ...", "Laba / Keuntungan (Profit)", ["Bunga", "Upah", "Sewa"]),
        ("Peran utama Rumah Tangga Produsen (RTP) dalam perekonomian adalah mengombinasikan faktor produksi untuk menghasilkan ...", "Barang dan jasa bagi masyarakat", ["Mencetak uang kertas", "Memungut pajak", "Membuat hukum"]),
        ("Peran utama pemerintah (RTN) sebagai pelaku ekonomi di antaranya bertindak sebagai regulator, produsen fasilitas umum, dan ...", "Konsumen barang operasional serta pemungut pajak", ["Pesaing monopoli swasta", "Pencetak valas asing", "Pedagang eceran"]),
        ("Masyarakat Luar Negeri (MLN) berperan penting dalam perekonomian suatu negara melalui kegiatan ...", "Ekspor, impor barang, dan penanaman investasi asing", ["Membuat mata uang rupiah", "Menyusun APBN", "Mengatur suku bunga"]),
        ("Diagram yang menggambarkan arus perputaran barang, jasa, dan uang antar pelaku ekonomi disebut ...", "Circular Flow Diagram", ["Diagram Venn", "Kurva Lorenz", "Kurva Phillips"]),
        ("Arus lingkaran kegiatan ekonomi sederhana yang hanya melibatkan RTK dan RTP dinamakan model ekonomi ...", "Dua sektor", ["Tiga sektor", "Empat sektor", "Satu sektor"]),
        ("Model arus lingkaran perekonomian tertutup yang melibatkan RTK, RTP, dan Pemerintah (RTN) dinamakan perekonomian ...", "Tiga sektor", ["Dua sektor", "Empat sektor", "Internasional"]),
        ("Model arus perekonomian terbuka yang melibatkan RTK, RTP, RTN, dan Masyarakat Luar Negeri dinamakan perekonomian ...", "Empat sektor", ["Dua sektor", "Tiga sektor", "Tertutup"]),
        ("Tenaga kerja yang memerlukan pendidikan formal tingkat tinggi seperti dokter, arsitek, dan guru dinamakan tenaga kerja ...", "Terdidik", ["Terlatih", "Tidak terdidik", "Lepas"]),
        ("Tenaga kerja yang memperoleh keahliannya melalui latihan dan pengalaman kerja seperti montir dan sopir dinamakan tenaga kerja ...", "Terlatih", ["Terdidik", "Tidak terlatih", "Intelektual"]),
        ("Tenaga kerja yang hanya mengandalkan kekuatan fisik tanpa pendidikan khusus seperti kuli panggul dinamakan tenaga kerja ...", "Tidak terdidik dan tidak terlatih", ["Terdidik", "Terlatih", "Spesialis"]),
        ("Tingkat kepuasan atau kenikmatan yang diperoleh konsumen dari mengonsumsi suatu barang atau jasa disebut ...", "Utilitas (Nilai guna)", ["Margin", "Elastisitas", "Omzet"]),
        ("Hukum Gossen I tentang nilai guna menyatakan bahwa jika konsumsi suatu barang dilakukan terus-menerus, maka tambahan kepuasannya ...", "Lama-kelamaan akan semakin menurun (The Law of Diminishing Marginal Utility)", ["Akan meningkat tak terbatas", "Tetap konstan", "Menjadi dua kali lipat"]),
        ("Hukum Gossen II menyatakan bahwa konsumen akan mengalokasikan pendapatannya untuk memenuhi berbagai macam kebutuhan hingga ...", "Tingkat kepuasan marginal masing-masing kebutuhan bernilai sama", ["Uangnya habis total", "Kebutuhan primer terpenuhi", "Hanya satu barang terbeli"]),
        ("Hukum Tambahan Hasil yang Semakin Menurun (The Law of Diminishing Returns) dalam teori produksi dikemukakan oleh ...", "David Ricardo", ["Adam Smith", "Thomas Malthus", "Alfred Marshall"]),
        ("Hukum The Law of Diminishing Returns menyatakan bahwa penambahan satu faktor produksi variabel pada faktor produksi tetap awalnya menaikkan hasil, tetapi ...", "Akhirnya penambahan hasil marginalnya akan semakin menurun", ["Hasil selalu bertambah terus", "Output menjadi nol", "Biaya menjadi nol"]),
        ("Biaya yang jumlahnya tetap sama tidak terpengaruh oleh banyak sedikitnya jumlah barang yang diproduksi dinamakan ...", "Biaya tetap (Fixed Cost / FC)", ["Biaya variabel", "Biaya total", "Biaya rata-rata"]),
        ("Contoh biaya tetap pada sebuah pabrik garmen adalah ...", "Sewa gedung pabrik dan biaya penyusutan mesin", ["Bahan baku kain", "Upah lembur harian buruh", "Biaya benang"]),
        ("Biaya yang jumlahnya berubah-ubah sebanding dengan volume jumlah barang yang diproduksi dinamakan ...", "Biaya variabel (Variable Cost / VC)", ["Biaya tetap", "Biaya overhead", "Biaya marjinal"]),
        ("Contoh biaya variabel pada usaha pembuatan roti adalah ...", "Biaya tepung terigu, telur, dan mentega", ["Sewa ruko tahunan", "Gaji manajer tetap", "Pajak bumi tahunan"]),
        ("Hasil penjumlahan antara total biaya tetap (FC) dan total biaya variabel (VC) dinamakan ...", "Biaya total (Total Cost / TC)", ["Biaya rata-rata", "Biaya marginal", "Laba kotor"]),
        ("Tambahan biaya yang harus dikeluarkan perusahaan untuk menghasilkan satu unit tambahan output produksi disebut ...", "Biaya marginal (Marginal Cost / MC)", ["Biaya total", "Biaya rata-rata", "Biaya oportunitas"]),
        ("Hasil kali antara jumlah unit barang yang terjual (Q) dengan harga per unit barang (P) dinamakan ...", "Penerimaan total (Total Revenue / TR)", ["Laba bersih", "Margin usaha", "Biaya produksi"]),
        ("Suatu perusahaan berada dalam kondisi titik impas di mana total pendapatan tepat sama dengan total biaya (TR = TC) dinamakan ...", "Break Even Point (BEP)", ["Laba maksimum", "Rugi bersih", "Pailit"]),
        ("Perusahaan akan memperoleh laba maksimal pada saat besarnya penerimaan marginal sama dengan biaya marginal yaitu ...", "MR = MC", ["TR = TC", "AR = AC", "P = FC"]),
    ]
    for q_text, corr, dists in economic_agents_factors:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami peran pelaku ekonomi, faktor produksi, biaya produksi, dan penerimaan usaha."))

    # 3. Permintaan, Penawaran & Struktur Pasar (50 soal)
    demand_supply_markets = [
        ("Hukum permintaan menyatakan bahwa jika harga suatu barang mengalami kenaikan, maka jumlah barang yang diminta akan ...", "Turun / Berkurang (ceteris paribus)", ["Naik / Bertambah", "Tetap sama", "Menjadi tak terhingga"]),
        ("Bunyi hukum permintaan berlaku jika faktor-faktor lain di luar harga dianggap konstan atau tidak berubah yang disebut asumsi ...", "Ceteris paribus", ["Laissez faire", "Invisible hand", "Mutatis mutandis"]),
        ("Bentuk kurva permintaan yang menghubungkan tingkat harga dengan jumlah barang yang diminta bergerak miring dari ...", "Kiri atas turun ke kanan bawah (kemiringan negatif)", ["Kiri bawah naik ke kanan atas", "Garis mendatar horizontal", "Tegak lurus"]),
        ("Hukum penawaran menyatakan bahwa jika tingkat harga suatu barang naik, maka jumlah barang yang ditawarkan penjual akan ...", "Naik / Bertambah", ["Turun / Berkurang", "Tetap sama", "Nol"]),
        ("Bentuk kurva penawaran yang menggambarkan hubungan harga dan kuantitas barang yang ditawarkan penjual miring dari ...", "Kiri bawah naik ke kanan atas (kemiringan positif)", ["Kiri atas turun ke kanan bawah", "Horizontal", "Vertikal"]),
        ("Titik potong antara kurva permintaan dan kurva penawaran menghasilkan titik kesepakatan yang dinamakan ...", "Titik ekuilibrium (Keseimbangan pasar)", ["Titik impas", "Titik puncak", "Titik belok"]),
        ("Tingkat kepekaan perubahan jumlah barang yang diminta akibat adanya perubahan harga dinamakan ...", "Elastisitas harga permintaan", ["Utilitas marginal", "Biaya marginal", "Inflasi harga"]),
        ("Jika persentase perubahan jumlah barang yang diminta lebih besar daripada persentase perubahan harga (Ed > 1), maka sifat permintaannya adalah ...", "Elastis", ["Inelastis", "Uniter", "Inelastis sempurna"]),
        ("Barang-barang mewah dan elektronik pada umumnya memiliki sifat elastisitas permintaan yang ...", "Elastis (Ed > 1)", ["Inelastis", "Inelastis sempurna", "Nol"]),
        ("Jika persentase perubahan jumlah barang yang diminta lebih kecil daripada persentase perubahan harga (Ed < 1), maka sifat permintaannya adalah ...", "Inelastis", ["Elastis", "Uniter", "Elastis sempurna"]),
        ("Barang kebutuhan pokok makanan seperti beras dan garam dapur memiliki sifat permintaan yang ...", "Inelastis (Ed < 1)", ["Elastis", "Elastis sempurna", "Uniter"]),
        ("Pasar di mana terdapat sangat banyak penjual dan pembeli serta barang yang diperdagangkan bersifat homogen (seragam) dinamakan ...", "Pasar persaingan sempurna", ["Pasar monopoli", "Pasar oligopoli", "Pasar monopsoni"]),
        ("Pada pasar persaingan sempurna, penjual dan pembeli tidak dapat menentukan harga secara sepihak sehingga mereka bertindak sebagai ...", "Price taker (Penerima harga)", ["Price maker (Penentu harga)", "Monopolis", "Kolektor"]),
        ("Bentuk pasar di mana hanya terdapat satu orang penjual tunggal yang menguasai seluruh pasokan barang tanpa ada pengganti dekat dinamakan ...", "Pasar monopoli", ["Pasar persaingan sempurna", "Pasar oligopoli", "Pasar duopoli"]),
        ("Penjual tunggal pada pasar monopoli memiliki kekuatan mutlak untuk menentukan harga pasar sehingga dijuluki ...", "Price maker (Penentu harga)", ["Price taker", "Konsumen", "Distributor"]),
        ("Contoh perusahaan yang menjalankan monopoli penyediaan tenaga listrik di Indonesia yang dilindungi undang-undang adalah ...", "PT PLN (Persero)", ["PT Telkom", "PT Pertamina", "PT Astra"]),
        ("Bentuk pasar di mana penawaran barang dikuasai oleh beberapa produsen besar (biasanya 2 hingga 10 perusahaan) dinamakan ...", "Pasar oligopoli", ["Pasar monopoli", "Pasar monopolistik", "Pasar persaingan sempurna"]),
        ("Contoh industri yang tergolong ke dalam struktur pasar oligopoli di Indonesia adalah ...", "Industri semen, operator seluler, dan sepeda motor", ["Pasar beras tradisional", "Penyedia air minum PDAM", "Warung makan tegal"]),
        ("Bentuk pasar oligopoli yang hanya dikuasai oleh dua produsen saja dinamakan pasar ...", "Duopoli", ["Monopoli", "Monopsoni", "Oligopsoni"]),
        ("Struktur pasar di mana terdapat banyak penjual yang menjual produk sejenis namun memiliki corak perbedaan (diferensiasi produk) dinamakan ...", "Pasar persaingan monopolistik", ["Pasar monopoli", "Pasar persaingan sempurna", "Pasar monopsoni"]),
        ("Contoh barang yang diperdagangkan pada pasar persaingan monopolistik dengan persaingan iklan merk ketat adalah ...", "Sabun mandi, sampo, dan pasta gigi", ["Tenaga listrik", "Beras curah", "Bahan bakar minyak"]),
        ("Struktur pasar di mana hanya terdapat satu pihak pembeli tunggal yang menghadapi banyak penjual dinamakan pasar ...", "Monopsoni", ["Monopoli", "Oligopoli", "Oligopsoni"]),
        ("Contoh pasar monopsoni adalah ...", "Para petani teh di suatu desa yang hanya bisa menjual pucuk daun teh ke satu pabrik teh setempat", ["Masyarakat membeli bensin di SPBU", "Konsumen membeli sabun di toko", "Pembeli tiket kereta"]),
        ("Struktur pasar di mana terdapat beberapa pembeli besar yang menghadapi banyak produsen penjual dinamakan pasar ...", "Oligopsoni", ["Monopsoni", "Monopoli", "Duopoli"]),
        ("Kebijakan harga batas tertinggi (Ceiling Price) yang ditetapkan oleh pemerintah untuk melindungi konsumen dari lonjakan harga dinamakan ...", "Harga Eceran Tertinggi (HET)", ["Harga dasar", "Harga pokok", "Harga pasar"]),
        ("Kebijakan harga batas terendah (Floor Price) yang ditetapkan pemerintah untuk melindungi petani dari anjloknya harga gabah panen adalah ...", "Harga Pokok Penjualan (HPP) / Harga dasar", ["Harga eceran tertinggi", "Harga lelang", "Pajak"]),
    ]
    for q_text, corr, dists in demand_supply_markets:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami kurva permintaan, penawaran, elastisitas, dan bentuk struktur pasar."))

    # 4. Bank Sentral, Uang & Kebijakan Moneter (60 soal)
    money_banking_monetary = [
        ("Tujuan tunggal dari Bank Indonesia (BI) selaku bank sentral Republik Indonesia adalah ...", "Mencapai dan memelihara kestabilan nilai rupiah", ["Mencetak uang sebanyak-banyaknya", "Memberikan pinjaman kepada warga", "Mencari laba bisnis"]),
        ("Kestabilan nilai rupiah yang dijaga oleh Bank Indonesia mencakup kestabilan terhadap harga barang (inflasi) dan kestabilan terhadap ...", "Mata uang negara lain (Nilai tukar / Kurs)", ["Pendapatan per kapita", "Jumlah penduduk", "Jumlah cadangan emas"]),
        ("Kebijakan bank sentral dalam mengatur jumlah uang yang beredar di masyarakat dinamakan kebijakan ...", "Moneter", ["Fiskal", "Perdagangan", "Industri"]),
        ("Jika jumlah uang yang beredar di masyarakat terlalu banyak sehingga memicu laju inflasi tinggi, bank sentral menerapkan kebijakan moneter ...", "Kontraktif (Uang ketat / Tight Money Policy)", ["Ekspansif (Easy Money Policy)", "Subsidi harga", "Devaluasi"]),
        ("Jika perekonomian sedang lesu atau terjadi resesi, bank sentral menambah jumlah uang yang beredar melalui kebijakan moneter ...", "Ekspansif (Easy Money Policy)", ["Kontraktif", "Uang ketat", "Sanering"]),
        ("Instrumen kebijakan moneter dengan cara menjual atau membeli surat berharga negara (seperti Sertifikat Bank Indonesia / SBI) disebut ...", "Operasi Pasar Terbuka (Open Market Operation)", ["Politik diskonto", "Giro wajib minimum", "Kredit selektif"]),
        ("Untuk mengurangi jumlah uang beredar di masyarakat melalui operasi pasar terbuka, bank sentral akan ...", "Menjual surat berharga (SBI) kepada perbankan", ["Membeli kembali SBI", "Mencetak uang baru", "Menurunkan pajak"]),
        ("Instrumen kebijakan moneter dengan cara menaikkan atau menurunkan tingkat suku bunga acuan bank sentral dinamakan ...", "Politik Diskonto (Discount Rate Policy)", ["Operasi pasar terbuka", "Cash ratio", "Moral suasion"]),
        ("Jika bank sentral menaikkan suku bunga acuan (BI Rate), maka minat masyarakat menabung di bank akan naik sehingga uang beredar akan ...", "Berkurang", ["Bertambah banyak", "Tetap sama", "Menjadi dua kali lipat"]),
        ("Kewajiban bank umum untuk menyisihkan sebagian dana simpanan nasabahnya sebagai cadangan wajib di bank sentral dinamakan ...", "Giro Wajib Minimum (Cash Ratio / Reserve Requirement)", ["Suku bunga kredit", "Kliring nasional", "Bilyet giro"]),
        ("Untuk mengurangi jumlah uang yang beredar di masyarakat, bank sentral dapat menaikkan persentase ...", "Cadangan kas minimum (Giro Wajib Minimum)", ["Pajak penghasilan", "Bantuan sosial", "Pencetakan uang"]),
        ("Himbauan moral yang dilakukan oleh pimpinan bank sentral kepada para direksi bank umum untuk mengendalikan kredit disebut ...", "Moral suasion (Himbauan moral)", ["Sanering", "Politik diskonto", "Devaluasi"]),
        ("Pemotongan nilai nominal uang kertas tanpa mengurangi nilai harga barang dinamakan ...", "Sanering", ["Redenominasi", "Devaluasi", "Revaluasi"]),
        ("Penyederhanaan penulisan digit angka nol pada pecahan uang rupiah tanpa mengurangi daya beli uang dinamakan ...", "Redenominasi", ["Sanering", "Devaluasi", "Inflasi"]),
        ("Kebijakan pemerintah menurunkan nilai mata uang dalam negeri terhadap mata uang asing secara sengaja dinamakan ...", "Devaluasi", ["Revaluasi", "Depresiasi", "Apresiasi"]),
        ("Kenaikan nilai mata uang dalam negeri terhadap mata uang asing yang ditetapkan secara resmi oleh pemerintah dinamakan ...", "Revaluasi", ["Devaluasi", "Inflasi", "Deflasi"]),
        ("Turunnya nilai tukar rupiah terhadap dolar AS yang terjadi secara alami akibat mekanisme pasar valuta dinamakan ...", "Depresiasi", ["Apresiasi", "Devaluasi", "Revaluasi"]),
        ("Menguatnya nilai tukar mata uang rupiah terhadap dolar AS karena mekanisme pasar bebas dinamakan ...", "Apresiasi", ["Depresiasi", "Deflasi", "Sanering"]),
        ("Teori kuantitas uang yang dirumuskan oleh Irving Fisher menyatakan hubungan kuantitatif peredaran uang yaitu ...", "M x V = P x T", ["M / V = P / T", "M x P = V x T", "M + V = P + T"]),
        ("Pada rumus Irving Fisher M x V = P x T, huruf 'V' melambangkan besaran ...", "Kecepatan perputaran uang (Velocity of money)", ["Volume barang dagang", "Nilai uang kartal", "Tingkat inflasi"]),
        ("Huruf 'M' pada rumus kuantitas uang Fisher melambangkan besaran ...", "Jumlah uang yang beredar (Money supply)", ["Pendapatan nasional", "Tingkat harga", "Kecepatan transaksi"]),
        ("Huruf 'P' pada persamaan pertukaran uang Fisher melambangkan besaran ...", "Tingkat harga rata-rata barang (Price)", ["Kecepatan uang", "Jumlah transaksi", "Pajak"]),
        ("Huruf 'T' pada rumus Fisher melambangkan besaran ...", "Jumlah transaksi barang dan jasa (Transactions)", ["Waktu transaksi", "Pajak total", "Nilai modal"]),
        ("Imbalan atau kompensasi finansial yang diberikan bank kepada nasabah atas uang yang disimpannya di rekening tabungan adalah ...", "Bunga tabungan", ["Biaya administrasi", "Pajak kendaraan", "Harga pokok barang"]),
        ("Biaya yang dibayarkan oleh nasabah peminjam kepada bank atas fasilitas pinjaman kredit yang diterimanya dinamakan ...", "Bunga pinjaman (Kredit)", ["Bunga tabungan", "Dividen", "Premi"]),
    ]
    for q_text, corr, dists in money_banking_monetary:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami peran Bank Indonesia, kebijakan moneter, teori kuantitas uang Fisher, dan bunga bank."))

    # 5. Inflasi, Kebijakan Fiskal & APBN (50 soal)
    inflation_and_fiscal = [
        ("Kenaikan tingkat harga barang dan jasa secara umum dan terus-menerus dalam periode waktu tertentu dinamakan ...", "Inflasi", ["Deflasi", "Resesi", "Stagflasi"]),
        ("Kondisi ekonomi di mana terjadi penurunan tingkat harga barang secara umum dan berkelanjutan dinamakan ...", "Deflasi", ["Inflasi", "Devaluasi", "Depresiasi"]),
        ("Inflasi yang disebabkan oleh tarikan permintaan masyarakat yang melonjak tinggi melebihi kapasitas produksi dinamakan ...", "Demand Pull Inflation", ["Cost Push Inflation", "Imported Inflation", "Hyperinflation"]),
        ("Inflasi yang disebabkan oleh kenaikan biaya produksi (seperti naiknya harga BBM dan bahan baku) dinamakan ...", "Cost Push Inflation", ["Demand Pull Inflation", "Domestic Inflation", "Deflasi"]),
        ("Inflasi yang terjadi karena naiknya harga barang impor dari luar negeri dinamakan ...", "Imported Inflation", ["Domestic Inflation", "Demand Pull Inflation", "Cost Push"]),
        ("Laju inflasi yang berada pada kisaran di bawah 10% per tahun tergolong ke dalam kategori inflasi ...", "Ringan", ["Sedang", "Berat", "Hiperinflasi"]),
        ("Laju inflasi yang berkisar antara 10% sampai 30% per tahun tergolong ke dalam kategori inflasi ...", "Sedang", ["Ringan", "Berat", "Sangat berat"]),
        ("Laju inflasi yang berkisar antara 30% sampai 100% per tahun dikategorikan sebagai inflasi ...", "Berat", ["Sedang", "Ringan", "Hiperinflasi"]),
        ("Laju inflasi ekstrem yang tidak terkendali dengan angka di atas 100% per tahun dinamakan ...", "Hiperinflasi (Hyperinflation)", ["Inflasi ringan", "Stagflasi", "Deflasi"]),
        ("Indeks yang digunakan oleh Badan Pusat Statistik (BPS) untuk mengukur laju inflasi bulanan di Indonesia adalah ...", "IHK (Indeks Harga Konsumen)", ["IHPB (Indeks Harga Perdagangan Besar)", "PDB Deflator", "IHSG"]),
        ("Kebijakan ekonomi yang dijalankan oleh pemerintah melalui pengaturan pendapatan dan belanja negara (APBN) dinamakan kebijakan ...", "Fiskal", ["Moneter", "Perbankan", "Investasi"]),
        ("Dua instrumen utama dalam pelaksanaan kebijakan fiskal pemerintah adalah ...", "Pajak dan Pengeluaran Pemerintah (Belanja negara)", ["Suku bunga dan SBI", "Cadangan kas dan kredit", "Kurs valas dan emas"]),
        ("Rencana keuangan tahunan pemerintah negara Indonesia yang disetujui oleh DPR dinamakan ...", "APBN (Anggaran Pendapatan dan Belanja Negara)", ["APBD", "Nota Keuangan", "DIPA"]),
        ("Rencana anggaran pendapatan dan belanja daerah di tingkat provinsi dan kabupaten/kota dinamakan ...", "APBD (Anggaran Pendapatan dan Belanja Daerah)", ["APBN", "PAD", "DAU"]),
        ("Satu periode tahun anggaran pelaksanaan APBN di Indonesia berlangsung mulai tanggal ...", "1 Januari sampai 31 Desember", ["1 Juli sampai 30 Juni", "1 April sampai 31 Maret", "17 Agustus sampai 16 Agustus"]),
        ("Sumber pendapatan terbesar dalam kas negara Republik Indonesia pada APBN berasal dari penerimaan ...", "Pajak", ["Bantuan luar negeri", "Hasil tambang minyak saja", "Percetakan uang"]),
        ("Pendapatan negara yang berasal dari dividen BUMN, royalti tambang, dan biaya perizinan tergolong ke dalam ...", "PNBP (Penerimaan Negara Bukan Pajak)", ["Penerimaan Pajak", "Hibah murni", "Pinjaman luar negeri"]),
        ("Kondisi anggaran di mana jumlah penerimaan negara lebih besar daripada jumlah pengeluaran belanja negara dinamakan anggaran ...", "Surplus", ["Defisit", "Berimbang", "Nol"]),
        ("Kondisi anggaran di mana jumlah pengeluaran belanja negara lebih besar daripada jumlah penerimaan pendapatan dinamakan anggaran ...", "Defisit", ["Surplus", "Berimbang", "Statis"]),
        ("Kondisi anggaran belanja di mana total penerimaan negara dirancang sama persis dengan total pengeluaran dinamakan anggaran ...", "Berimbang", ["Defisit", "Surplus", "Ganda"]),
        ("Untuk menutup defisit anggaran belanja APBN, salah satu langkah resmi yang diambil pemerintah adalah ...", "Menerbitkan Surat Berharga Negara (SBN / SUN) dan pinjaman", ["Menutup pasar saham", "Meminta sumbangan paksa", "Menghapus mata uang"]),
        ("Dana yang dialokasikan dari APBN kepada daerah untuk mendanai kebutuhan daerah dalam rangka desentralisasi adalah ...", "Dana Transfer ke Daerah (TKD / DAU / DAK)", ["Pajak Daerah", "Pendapatan Asli Daerah", "Retribusi Daerah"]),
        ("Dana dari APBN yang dialokasikan dengan tujuan pemerataan kemampuan keuangan antardaerah adalah ...", "DAU (Dana Alokasi Umum)", ["DAK (Dana Alokasi Khusus)", "Dana Bagi Hasil", "PAD"]),
        ("Dana dari APBN yang dialokasikan untuk mendanai kegiatan khusus yang menjadi prioritas nasional di daerah adalah ...", "DAK (Dana Alokasi Khusus)", ["DAU", "Dana Desa", "Dana Darurat"]),
        ("Dana dari APBN yang disalurkan langsung ke kas pemerintah desa untuk pembangunan infrastruktur desa dinamakan ...", "Dana Desa", ["DAU", "DAK", "Dana Bagi Hasil"]),
    ]
    for q_text, corr, dists in inflation_and_fiscal:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami inflasi, kebijakan fiskal, struktur APBN, dan instrumen penerimaan negara."))

    # 6. Manajemen, Badan Usaha & Kewirausahaan (50 soal)
    management_and_business = [
        ("Empat fungsi dasar manajemen yang sangat terkenal dirumuskan oleh George R. Terry dengan akronim POAC yaitu ...", "Planning, Organizing, Actuating, dan Controlling", ["Production, Operation, Accounting, Cost", "Promotion, Ordering, Advertising, Commerce", "Planning, Owning, Acting, Checking"]),
        ("Fungsi manajemen yang berkaitan dengan penentuan tujuan yang ingin dicapai dan langkah-langkah strategisnya adalah ...", "Planning (Perencanaan)", ["Organizing", "Actuating", "Controlling"]),
        ("Fungsi manajemen berupa pembagian tugas, wewenang, dan tanggung jawab kepada karyawan dinamakan ...", "Organizing (Pengorganisasian)", ["Planning", "Actuating", "Controlling"]),
        ("Fungsi manajemen untuk menggerakkan, memotivasi, dan membimbing karyawan agar bekerja giat mencapai tujuan dinamakan ...", "Actuating (Pelaksanaan / Penggerakan)", ["Planning", "Organizing", "Controlling"]),
        ("Fungsi manajemen untuk mengawasi, menilai, dan mengoreksi kinerja pekerjaan agar sesuai dengan rencana dinamakan ...", "Controlling (Pengawasan / Pengendalian)", ["Planning", "Organizing", "Actuating"]),
        ("Tiga tingkatan manajemen dalam suatu perusahaan adalah top management, middle management, dan ...", "Low management (Manajemen tingkat bawah / lini pertama)", ["Staff management", "Super management", "Board of director"]),
        ("Pimpinan puncak seperti Direktur Utama (CEO) dan jajaran direksi tergolong ke dalam tingkatan ...", "Top Management (Manajemen Puncak)", ["Middle Management", "First Line Management", "Staff Operasional"]),
        ("Kepala bagian, manajer divisi cabang, dan kepala seksi di perusahaan tergolong ke dalam tingkatan ...", "Middle Management (Manajemen Menengah)", ["Top Management", "First Line", "Direktur"]),
        ("Mandor, penyelia (supervisor), dan kepala regu kerja di pabrik tergolong ke dalam tingkatan ...", "Lower Management (Manajemen Lini Pertama)", ["Top Management", "Middle Management", "Komisaris"]),
        ("Kekuasaan tertinggi dalam tata kelola koperasi di Indonesia berada di tangan ...", "Rapat Anggota Tahunan (RAT)", ["Ketua Koperasi", "Pengawas Koperasi", "Dinas Koperasi"]),
        ("Prinsip pembagian Sisa Hasil Usaha (SHU) dalam koperasi diberikan kepada anggota sebanding dengan ...", "Besarnya jasa usaha dan kontribusi transaksi anggota pada koperasi", ["Besarnya jabatan keluarga", "Banyaknya tabungan emas", "Kehadiran semata"]),
        ("Bentuk badan usaha berbadan hukum yang modalnya terbagi atas lembar-lembar saham kepemilikan adalah ...", "Perseroan Terbatas (PT)", ["CV", "Firma", "Perseorangan"]),
        ("Tanda bukti kepemilikan bagian modal pada suatu Perseroan Terbatas (PT) dinamakan ...", "Saham", ["Obligasi", "Kuitansi", "Faktur"]),
        ("Pemilik saham di sebuah Perseroan Terbatas berhak menerima bagian keuntungan laba perusahaan yang disebut ...", "Dividen", ["Bunga bank", "Royalti", "Gaji pokok"]),
        ("Kekuasaan tertinggi dalam sebuah perseroan terbatas (PT) berada dalam forum resmi yaitu ...", "RUPS (Rapat Umum Pemegang Saham)", ["Rapat Direksi", "Rapat Komisaris", "Sidang Pleno Karyawan"]),
        ("Tanggung jawab pemilik modal saham pada sebuah Perseroan Terbatas bersifat terbatas, artinya terbatas pada ...", "Jumlah modal saham yang disetorkannya saja", ["Seluruh harta kekayaan pribadinya", "Rumah tinggal pribadinya", "Gaji seumur hidup"]),
        ("Perusahaan Terbuka (PT Tbk) adalah perseroan terbatas yang sahamnya telah diperjualbelikan kepada masyarakat luas di ...", "Bursa Efek (Pasar Modal)", ["Pasar barang tradisional", "Bank sentral", "Kantor dinas"]),
        ("BUMN perseroan yang modalnya terbagi atas saham dengan tujuan mengejar keuntungan dinamakan ...", "Persero (Perusahaan Perseroan)", ["Perum (Perusahaan Umum)", "Koperasi", "Yayasan"]),
        ("BUMN yang seluruh modalnya dimiliki negara dan bertujuan melayani kemanfaatan umum bagi masyarakat dinamakan ...", "Perum (Perusahaan Umum)", ["Persero", "Firma", "PT Terbuka"]),
        ("Contoh BUMN yang berstatus Perusahaan Umum (Perum) di Indonesia antara lain ...", "Perum Damri dan Perum Bulog", ["PT Kereta Api Indonesia", "PT Telkom Indonesia", "PT Garuda Indonesia"]),
        ("Usaha Mikro, Kecil, dan Menengah yang menjadi tulang punggung penggerak ekonomi kerakyatan di Indonesia disingkat ...", "UMKM", ["BUMN", "BUMD", "BUMS"]),
        ("Kewirausahaan (Entrepreneurship) mencakup kemampuan seseorang untuk melihat peluang bisnis, berani mengambil risiko, dan menciptakan ...", "Inovasi produk baru bernilai tambah", ["Kekacauan pasar", "Utang macet", "Ketergantungan"]),
    ]
    for q_text, corr, dists in management_and_business:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami fungsi manajemen POAC, badan usaha PT, BUMN, koperasi, dan UMKM."))

    # 7. Perdagangan Internasional & Neraca Pembayaran (50 soal)
    international_trade = [
        ("Teori Keunggulan Mutlak (Absolute Advantage) dalam perdagangan internasional dikemukakan oleh tokoh ekonomi ...", "Adam Smith", ["David Ricardo", "John Stuart Mill", "Heckscher-Ohlin"]),
        ("Teori Keunggulan Komparatif (Comparative Advantage) yang menyatakan negara berfokus memproduksi barang dengan biaya peluang terendah dikemukakan oleh ...", "David Ricardo", ["Adam Smith", "Thomas Malthus", "Karl Marx"]),
        ("Kebijakan pemerintah menetapkan pajak bea masuk atas barang impor untuk melindungi produk lokal dinamakan kebijakan ...", "Tarif (Bea Cukai)", ["Kuota impor", "Subsidi", "Dumping"]),
        ("Kebijakan pemerintah membatasi kuantitas jumlah fisik barang impor yang boleh masuk ke dalam negeri dinamakan ...", "Kuota impor", ["Tarif impor", "Dumping", "Devaluasi"]),
        ("Kebijakan menjual barang di pasar luar negeri dengan harga lebih murah daripada harga jual di dalam negeri dinamakan ...", "Politik Dumping", ["Proteksi", "Subsidi", "Diskriminasi tarif"]),
        ("Bantuan finansial dari pemerintah kepada produsen dalam negeri agar biaya produksinya murah dan mampu bersaing dinamakan ...", "Subsidi", ["Pajak", "Tarif", "Cukai"]),
        ("Larangan mutlak terhadap masuknya barang impor tertentu dari luar negeri dinamakan ...", "Embargo / Larangan impor", ["Kuota", "Tarif", "Dumping"]),
        ("Catatan sistematis mengenai seluruh transaksi ekonomi antara penduduk suatu negara dengan negara lain dalam kurun waktu tertentu dinamakan ...", "Neraca Pembayaran Internasional (Balance of Payments)", ["Neraca Perdagangan", "APBN", "Laporan Arus Kas"]),
        ("Catatan perbandingan antara nilai total ekspor dan nilai total impor barang dan jasa suatu negara dinamakan ...", "Neraca Perdagangan (Balance of Trade)", ["Neraca Modal", "Neraca Pembayaran", "Cadangan Devisa"]),
        ("Kondisi di mana nilai total ekspor suatu negara lebih besar daripada nilai total impornya dinamakan neraca perdagangan ...", "Surplus (Aktif)", ["Defisit", "Berimbang", "Nol"]),
        ("Kondisi di mana nilai total impor lebih besar daripada nilai total ekspor suatu negara dinamakan neraca perdagangan ...", "Defisit (Pasif)", ["Surplus", "Berimbang", "Positif"]),
        ("Alat pembayaran luar negeri yang diterima dan diakui secara internasional yang dimiliki oleh bank sentral dinamakan cadangan ...", "Devisa", ["Saham", "Obligasi", "Uang kartal"]),
        ("Contoh devisa suatu negara dapat berwujud ...", "Mata uang kuat (seperti US Dollar), emas moneter, dan SDR", ["Mata uang rupiah kartal", "Tanah perkebunan", "Gedung perkantoran"]),
        ("Sistem penetapan kurs mata uang yang diserahkan sepenuhnya pada kekuatan tarik-menarik permintaan dan penawaran di pasar valuta dinamakan ...", "Sistem kurs mengambang bebas (Floating Exchange Rate)", ["Sistem kurs tetap", "Sistem standar emas", "Sistem patokan resmi"]),
        ("Sistem penentuan kurs di mana bank sentral menetapkan nilai tukar mata uang dalam negeri pada angka tetap tertentu terhadap valas dinamakan ...", "Sistem kurs tetap (Fixed Exchange Rate)", ["Sistem mengambang bebas", "Sistem kurs fleksibel", "Pasar valuta"]),
        ("Pasar tempat bertemunya pihak penjual dan pembeli mata uang asing dinamakan pasar ...", "Valuta Asing (Valas / Forex)", ["Pasar modal", "Pasar uang", "Pasar komoditas"]),
        ("Organisasi Dana Moneter Internasional yang bertugas memelihara stabilitas sistem keuangan dunia dan memberi bantuan pinjaman adalah ...", "IMF (International Monetary Fund)", ["Bank Dunia", "WTO", "OECD"]),
        ("Lembaga keuangan internasional yang bertugas memberikan pinjaman modal jangka panjang untuk proyek pembangunan infrastruktur negara berkembang adalah ...", "Bank Dunia (World Bank)", ["IMF", "WTO", "ADB"]),
    ]
    for q_text, corr, dists in international_trade:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami teori perdagangan internasional, neraca perdagangan, valuta asing, dan devisa."))

    # 8. Pasar Modal, Lembaga Keuangan & Investasi (65 soal)
    capital_markets_and_finance = [
        ("Pasar tempat bertemunya pihak yang membutuhkan dana jangka panjang dengan pihak penanam modal (investor) dinamakan ...", "Pasar Modal (Bursa Efek)", ["Pasar Uang", "Pasar Valas", "Pasar Komoditas"]),
        ("Lembaga bursa efek resmi yang memfasilitasi perdagangan saham dan obligasi di Indonesia adalah ...", "PT Bursa Efek Indonesia (BEI / IDX)", ["Bank Indonesia", "OJK", "Kliring Penjaminan"]),
        ("Surat berharga bukti pengakuan utang dari pihak penerbit obligasi kepada pihak investor yang disertai bunga dinamakan ...", "Obligasi", ["Saham", "Kuitansi", "Cek"]),
        ("Keuntungan berkala yang diterima oleh pemegang obligasi berupa bunga tetap dinamakan ...", "Kupon obligasi", ["Dividen", "Capital gain", "Royalti"]),
        ("Keuntungan yang diperoleh investor dari selisih harga jual saham yang lebih tinggi daripada harga beli saham dinamakan ...", "Capital Gain", ["Capital Loss", "Dividen", "Kupon"]),
        ("Kerugian yang dialami investor ketika menjual saham pada harga yang lebih rendah daripada harga belinya dinamakan ...", "Capital Loss", ["Capital Gain", "Dividen", "Bunga"]),
        ("Kegiatan penawaran saham perdana sebuah perusahaan kepada masyarakat umum untuk pertama kalinya dinamakan ...", "IPO (Initial Public Offering)", ["Right issue", "Stock split", "Buyback"]),
        ("Wadah yang digunakan untuk menghimpun dana dari masyarakat pemodal untuk diinvestasikan dalam portofolio efek oleh manajer investasi dinamakan ...", "Reksa Dana", ["Saham gorengan", "Koperasi harian", "Deposito mandiri"]),
        ("Profesional pengelola investasi yang bertugas mengelola dana portofolio reksa dana dinamakan ...", "Manajer Investasi (MI)", ["Pialang saham", "Broker", "Underwriter"]),
        ("Lembaga perantara yang mempertemukan pesanan beli dan jual saham di bursa efek dinamakan ...", "Broker / Pialang (Perusahaan Sekuritas)", ["Bank kustodian", "Notaris", "Kliring"]),
        ("Bank yang bertugas menyimpan dan mengamankan sertifikat surat berharga dan aset portofolio reksa dana dinamakan ...", "Bank Kustodian", ["Bank Perkreditan", "Bank Syariah", "Bank Sentral"]),
        ("Indeks yang mengukur rata-rata pergerakan seluruh saham yang tercatat di Bursa Efek Indonesia dinamakan ...", "IHSG (Indeks Harga Saham Gabungan)", ["Dow Jones", "Nikkei", "Hang Seng"]),
        ("Indeks di BEI yang berisi 45 emiten saham dengan tingkat likuiditas transaksi sangat tinggi dan kapitalisasi pasar besar dinamakan ...", "Indeks LQ45", ["IHSG", "Kompas 100", "JII"]),
        ("Lembaga yang menjamin simpanan nasabah di bank hingga batas maksimal Rp 2 miliar per nasabah per bank adalah ...", "LPS (Lembaga Penjamin Simpanan)", ["OJK", "Bank Indonesia", "Kemenkeu"]),
        ("Lembaga pengawas independen yang mengawasi seluruh aktivitas bank, asuransi, pasar modal, dan pinjaman online di Indonesia adalah ...", "OJK (Otoritas Jasa Keuangan)", ["BI", "LPS", "BPK"]),
        ("Iuran premi berkala yang dibayarkan oleh nasabah kepada perusahaan asuransi bertujuan untuk ...", "Mendapatkan proteksi perlindungan finansial jika terjadi risiko kerugian", ["Menabung bunga tinggi", "Membeli saham", "Menghindari pajak"]),
        ("Tuntutan ganti rugi resmi yang diajukan oleh pemegang polis kepada perusahaan asuransi saat terjadi musibah kerugian dinamakan ...", "Klaim asuransi", ["Premi", "Polis", "Kupon"]),
        ("Surat kontrak perjanjian resmi tertulis antara pihak pemegang asuransi dengan perusahaan asuransi dinamakan ...", "Polis asuransi", ["Premi", "Klaim", "Akta"]),
        ("Lembaga pembiayaan yang menyediakan barang modal (seperti kendaraan atau mesin pabrik) dengan sistem sewa guna usaha dinamakan ...", "Leasing (Sewa Guna Usaha)", ["Pegadaian", "Asuransi", "Anjak Piutang"]),
        ("Lembaga keuangan yang membeli piutang dagang suatu perusahaan yang belum jatuh tempo dinamakan lembaga ...", "Anjak Piutang (Factoring)", ["Modal Ventura", "Pegadaian", "Leasing"]),
        ("Lembaga investasi yang memberikan pembiayaan modal awal kepada perusahaan rintisan (startup) yang berisiko tinggi dinamakan ...", "Modal Ventura (Venture Capital)", ["Koperasi", "Pegadaian", "Bank Konvensional"]),
        ("Sistem perbankan yang beroperasi tanpa menggunakan sistem bunga melainkan menggunakan prinsip bagi hasil syariah adalah ...", "Perbankan Syariah", ["Perbankan Konvensional", "Bank Gelap", "Renternir"]),
        ("Akad perjanjian bagi hasil antara pemilik modal (shahibul mal) dengan pengelola usaha (mudharib) dalam bank syariah dinamakan akad ...", "Mudharabah", ["Musyarakah", "Murabahah", "Ijarah"]),
        ("Akad jual beli barang dengan menyatakan harga perolehan dan margin keuntungan yang disepakati pembeli dinamakan akad ...", "Murabahah", ["Mudharabah", "Ijarah", "Wadiah"]),
        ("Titipan murni dana simpanan nasabah di bank syariah yang dapat diambil sewaktu-waktu dinamakan akad ...", "Wadiah", ["Mudharabah", "Murabahah", "Salam"]),
        ("Prinsip pembiayaan sewa-menyewa manfaat suatu barang atau jasa tanpa pemindahan kepemilikan dalam bank syariah dinamakan akad ...", "Ijarah", ["Murabahah", "Istishna", "Rahn"]),
    ]
    for q_text, corr, dists in capital_markets_and_finance:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami pasar modal, saham, obligasi, OJK, LPS, asuransi, dan perbankan syariah."))

    # 9. Pendapatan Nasional & Pertumbuhan Ekonomi (45 soal)
    national_income = [
        ("Nilai total seluruh barang dan jasa akhir yang dihasilkan oleh masyarakat di dalam wilayah suatu negara dalam satu tahun dinamakan ...", "PDB (Produk Domestik Bruto / GDP)", ["PNB (Produk Nasional Bruto)", "Pendapatan per kapita", "NNP"]),
        ("Nilai total barang dan jasa akhir yang dihasilkan murni oleh seluruh warga negara suatu negara (baik di dalam maupun luar negeri) disebut ...", "PNB (Produk Nasional Bruto / GNP)", ["PDB (GDP)", "NNP", "Pendapatan per kapita"]),
        ("Rumus hubungan antara PNB (GNP) dan PDB (GDP) adalah ...", "PNB = PDB + Pendapatan Neto Luar Negeri", ["PNB = PDB - Pajak", "PNB = PDB x Kurs", "PNB = PDB / Populasi"]),
        ("Produk Nasional Neto (NNP) diperoleh dari Produk Nasional Bruto (PNB) dikurangi dengan ...", "Penyusutan barang modal (Depresiasi)", ["Pajak tidak langsung", "Subsidi pemerintah", "Laba ditahan"]),
        ("Pendapatan Nasional Neto (NNI) dihitung dari NNP dikurangi dengan ...", "Pajak tidak langsung ditambah subsidi", ["Penyusutan", "Pajak langsung", "Iuran asuransi"]),
        ("Pendapatan perseorangan yang benar-benar siap untuk dibelanjakan atau ditabung oleh individu dinamakan ...", "Pendapatan Disposabel (Disposable Income / DI)", ["Pendapatan Personal (PI)", "Pendapatan Neto", "GNP"]),
        ("Rumus untuk menghitung Pendapatan Disposabel (DI) adalah Pendapatan Perseorangan (PI) dikurangi ...", "Pajak langsung (seperti PPh)", ["Pajak pertambahan nilai", "Penyusutan", "Subsidi"]),
        ("Tiga pendekatan yang digunakan untuk menghitung besarnya pendapatan nasional adalah pendekatan produksi, pendekatan pendapatan, dan ...", "Pendekatan pengeluaran", ["Pendekatan konsumsi", "Pendekatan tabungan", "Pendekatan pajak"]),
        ("Rumus perhitungan pendapatan nasional menurut pendekatan pengeluaran adalah ...", "Y = C + I + G + (X - M)", ["Y = R + W + I + P", "Y = P x Q", "Y = C + S"]),
        ("Pada rumus pengeluaran Y = C + I + G + (X - M), huruf 'C' melambangkan pengeluaran ...", "Konsumsi Rumah Tangga (Consumption)", ["Kredit perbankan", "Modal perusahaan", "Pajak"]),
        ("Pada rumus pengeluaran pendapatan nasional, huruf 'I' melambangkan ...", "Investasi domestik perusahaan (Investment)", ["Impor barang", "Inflasi harga", "Pendapatan"]),
        ("Huruf 'G' pada rumus pendapatan nasional melambangkan ...", "Pengeluaran pemerintah untuk barang dan jasa (Government expenditure)", ["Gaji buruh", "Giro bank", "Gross profit"]),
        ("Komponen '(X - M)' pada rumus pendapatan nasional melambangkan nilai ...", "Ekspor neto (Ekspor dikurangi Impor)", ["Ekspor total", "Impor bruto", "Kurs valas"]),
        ("Rumus perhitungan pendapatan nasional menurut pendekatan pendapatan adalah penjumlahan dari sewa, upah, bunga, dan laba yaitu ...", "Y = r + w + i + p", ["Y = C + I + G", "Y = M x V", "Y = P x Q"]),
        ("Pendapatan rata-rata setiap penduduk di suatu negara dalam satu tahun yang diperoleh dari membagi PNB dengan jumlah penduduk disebut ...", "Pendapatan per kapita", ["Pendapatan nasional bruto", "Upah minimum", "Gaji rata-rata"]),
        ("Pendapatan per kapita sering dijadikan indikator oleh Bank Dunia untuk mengukur tingkat ...", "Kemakmuran dan standar hidup masyarakat suatu negara", ["Kekuatan militer", "Luas wilayah negara", "Jumlah cadangan minyak"]),
        ("Kurva yang digunakan untuk menggambarkan tingkat ketimpangan distribusi pendapatan masyarakat dinamakan kurva ...", "Kurva Lorenz", ["Kurva Phillips", "Kurva Indiferen", "Kurva Permintaan"]),
        ("Ukuran statistik ketimpangan distribusi pendapatan yang nilainya berkisar antara 0 (merata sempurna) hingga 1 (timpang mutlak) dinamakan ...", "Koefisien Gini (Gini Ratio)", ["Indeks Pembangunan Manusia", "Indeks Harga", "Rasio Lancar"]),
        ("Kondisi di mana Produk Domestik Bruto (PDB) suatu negara mengalami penurunan negatif selama dua kuartal berturut-turut dinamakan ...", "Resesi ekonomi", ["Depresi ekonomi", "Stagflasi", "Booming"]),
        ("Kondisi krisis ekonomi yang sangat parah di mana resesi berlangsung bertahun-tahun disertai pengangguran massal dinamakan ...", "Depresi ekonomi (seperti Great Depression 1930)", ["Resesi ringan", "Stagflasi", "Deflasi"]),
        ("Fenomena ekonomi yang sangat sulit diatasi di mana terjadi stagnasi ekonomi (pengangguran tinggi) disertai laju inflasi tinggi dinamakan ...", "Stagflasi", ["Reflasi", "Deflasi", "Resesi biasa"]),
    ]
    for q_text, corr, dists in national_income:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami PDB, PNB, pendapatan per kapita, rumus pendapatan nasional, dan koefisien Gini."))

    # 10. Ketenagakerjaan & Pengangguran (40 soal)
    employment_facts = [
        ("Penduduk yang berada dalam batas usia kerja menurut undang-undang ketenagakerjaan di Indonesia adalah penduduk berusia ...", "15 tahun ke atas (hingga 64 tahun)", ["17 tahun ke atas", "21 tahun ke atas", "12 tahun ke atas"]),
        ("Penduduk usia kerja yang bekerja atau sedang aktif mencari pekerjaan dinamakan ...", "Angkatan kerja (Labor Force)", ["Bukan angkatan kerja", "Penganggur terselubung", "Pekerja paruh waktu"]),
        ("Penduduk usia kerja yang memilih bersekolah, mengurus rumah tangga, atau pensiunan tergolong ke dalam kelompok ...", "Bukan angkatan kerja", ["Angkatan kerja aktif", "Pengangguran terbuka", "Pekerja kontrak"]),
        ("Pengangguran yang terjadi karena seseorang sedang berpindah pekerjaan atau mencari pekerjaan yang lebih sesuai dengan keinginannya disebut ...", "Pengangguran friksional (Peralihan)", ["Pengangguran struktural", "Pengangguran siklis", "Pengangguran musiman"]),
        ("Pengangguran yang timbul akibat perubahan struktur perekonomian (misal dari agraris ke industri mesin) dinamakan pengangguran ...", "Struktural", ["Friksional", "Musiman", "Volunter"]),
        ("Pengangguran yang timbul akibat penurunan kegiatan ekonomi secara umum (masa krisis atau resesi) dinamakan pengangguran ...", "Siklis (Konjungtural)", ["Struktural", "Friksional", "Musiman"]),
        ("Petani sawah yang menganggur selama menunggu masa panen padi tiba tergolong ke dalam jenis pengangguran ...", "Musiman", ["Struktural", "Friksional", "Terbuka"]),
        ("Tenaga kerja yang bekerja tetapi produktivitasnya sangat rendah karena kelebihan jumlah pekerja dinamakan pengangguran ...", "Terselubung (Disguised Unemployment)", ["Terbuka", "Musiman", "Teknologi"]),
        ("Tenaga kerja yang bekerja di bawah jam kerja normal (kurang dari 35 jam per minggu) dan masih mencari pekerjaan tambahan disebut ...", "Setengah menganggur (Underemployment)", ["Pengangguran terbuka", "Pengangguran sukarela", "Pekerja lepas"]),
        ("Orang yang sama sekali tidak bekerja dan sedang berusaha keras mencari pekerjaan dinamakan pengangguran ...", "Terbuka", ["Terselubung", "Musiman", "Friksional"]),
        ("Upah minimum terendah yang ditetapkan oleh gubernur sebagai standar jaring pengaman bagi buruh di tingkat provinsi adalah ...", "UMP (Upah Minimum Provinsi)", ["UMK", "UMR", "Gaji Pokok"]),
        ("Lembaga badan hukum publik yang memberikan perlindungan jaminan kecelakaan kerja, hari tua, dan pensiun bagi pekerja adalah ...", "BPJS Ketenagakerjaan", ["BPJS Kesehatan", "Jasa Raharja", "Taspen"]),
    ]
    for q_text, corr, dists in employment_facts:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami konsep angkatan kerja, jenis-jenis pengangguran, dan upah minimum UMP."))

    # 11. Perpajakan di Indonesia (50 soal)
    taxation_facts = [
        ("Pajak yang bebannya harus ditanggung sendiri oleh wajib pajak dan tidak dapat dilimpahkan kepada pihak lain dinamakan ...", "Pajak langsung", ["Pajak tidak langsung", "Pajak pertambahan nilai", "Cukai"]),
        ("Contoh pajak langsung di Indonesia yang dipungut langsung dari penghasilan seseorang adalah ...", "Pph (Pajak Penghasilan) dan PBB", ["PPN", "Pajak Penjualan Barang Mewah", "Cukai"]),
        ("Pajak yang pembebanannya dapat dialihkan atau digeserkan kepada pihak konsumen pembeli dinamakan pajak ...", "Tidak langsung", ["Langsung", "Pribadi", "Pajak mutlak"]),
        ("Contoh pajak tidak langsung yang dibayar pembeli saat berbelanja di minimarket atau restoran adalah ...", "PPN (Pajak Pertambahan Nilai)", ["PPh 21", "PBB", "Pajak Warisan"]),
        ("Nomor identitas resmi yang diberikan oleh Direktorat Jenderal Pajak kepada wajib pajak untuk administrasi perpajakan adalah ...", "NPWP (Nomor Pokok Wajib Pajak)", ["NIK", "NIP", "SIUP"]),
        ("Batas jumlah penghasilan wajib pajak orang pribadi yang tidak dikenai pemungutan pajak penghasilan dinamakan ...", "PTKP (Penghasilan Tidak Kena Pajak)", ["PKP (Penghasilan Kena Pajak)", "Pajak Final", "Restitusi"]),
        ("Surat formulir yang digunakan oleh wajib pajak untuk melaporkan perhitungan dan pembayaran pajaknya setiap tahun dinamakan ...", "SPT (Surat Pemberitahuan Tahunan)", ["SKP", "STP", "Faktur Pajak"]),
        ("Tarif pajak di mana persentase tarifnya semakin tinggi seiring dengan bertambah besarnya jumlah penghasilan kena pajak dinamakan ...", "Tarif progresif", ["Tarif degresif", "Tarif proporsional", "Tarif tetap"]),
        ("Penerapan tarif pajak progresif di Indonesia digunakan pada pemungutan ...", "PPh Orang Pribadi", ["Bea meterai", "PBB", "Pajak Kendaraan"]),
        ("Tarif pajak yang persentasenya selalu tetap sama untuk berapapun besarnya jumlah dasar pengenaan pajak dinamakan ...", "Tarif proporsional (Sebanding)", ["Tarif progresif", "Tarif degresif", "Tarif tetap"]),
        ("Pungutan negara yang dikenakan khusus atas barang-barang tertentu yang konsumsinya perlu dikendalikan seperti rokok dan alkohol dinamakan ...", "Cukai", ["Pajak", "Retribusi", "Tarif bea masuk"]),
        ("Pajak yang dipungut atas dokumen perjanjian, kuitansi bernilai besar, atau akta notaris dengan menempelkan meterai dinamakan ...", "Bea Meterai", ["Cukai", "Pajak Dokumen", "Pajak Pertambahan Nilai"]),
        ("Asas pemungutan pajak menurut Adam Smith yang menyatakan bahwa pemungutan pajak harus adil dan sesuai kemampuan dinamakan asas ...", "Equality (Keadilan)", ["Certainty", "Convenience of payment", "Economy of collection"]),
        ("Asas yang menyatakan bahwa pemungutan pajak harus jelas, pasti, dan tidak sewenang-wenang berdasarkan undang-undang adalah asas ...", "Certainty (Kepastian hukum)", ["Equality", "Convenience", "Economy"]),
        ("Asas yang menyatakan bahwa pajak hendaknya dipungut pada saat yang paling menyenangkan bagi wajib pajak (seperti saat gajian) dinamakan asas ...", "Convenience of payment (Kenyamanan membayar)", ["Certainty", "Equality", "Efficiency"]),
        ("Asas yang menyatakan bahwa biaya pemungutan pajak tidak boleh lebih besar daripada hasil penerimaan pajak yang dipungut dinamakan asas ...", "Economy of collection (Efisiensi)", ["Equality", "Certainty", "Convenience"]),
        ("Pengembalian kelebihan pembayaran pajak dari kas negara kepada wajib pajak dinamakan ...", "Restitusi pajak", ["Kompensasi", "Amnesti pajak", "Penalti pajak"]),
        ("Penghapusan sanksi administrasi perpajakan dengan membayar uang tebusan secara sukarela dinamakan program ...", "Tax Amnesty (Pengampunan Pajak)", ["Restitusi", "Banding pajak", "Audit forensik"]),
    ]
    for q_text, corr, dists in taxation_facts:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami sistem perpajakan, tarif progresif, PPN, PPh, cukai, dan asas Adam Smith."))

    # 12. Akuntansi Dasar & Keuangan Bisnis (55 soal)
    accounting_basics = [
        ("Proses mencatat, menggolongkan, meringkas, dan menyajikan data transaksi keuangan untuk pengambilan keputusan dinamakan ...", "Akuntansi", ["Manajemen", "Auditing", "Pemasaran"]),
        ("Persamaan dasar akuntansi yang menjadi fondasi sistem pembukuan berpasangan adalah ...", "Aset = Liabilitas + Ekuitas (Harta = Utang + Modal)", ["Aset = Utang - Modal", "Modal = Aset + Utang", "Kas = Penjualan - Biaya"]),
        ("Segala kekayaan atau sumber daya ekonomis yang dimiliki oleh perusahaan dinamakan ...", "Aset (Harta / Aktiva)", ["Liabilitas", "Ekuitas", "Beban"]),
        ("Kewajiban finansial perusahaan kepada pihak luar yang harus dilunasi pada masa mendatang dinamakan ...", "Liabilitas (Utang / Kewajiban)", ["Aset", "Ekuitas", "Pendapatan"]),
        ("Hak sisa kepemilikan pemilik perusahaan atas total aset setelah dikurangi seluruh kewajiban utang dinamakan ...", "Ekuitas (Modal)", ["Liabilitas", "Aset lancar", "Laba kotor"]),
        ("Aset yang berupa uang tunai atau aset yang sangat mudah dicairkan menjadi uang tunai dalam waktu kurang dari satu tahun dinamakan ...", "Aset lancar (Current Assets)", ["Aset tetap", "Aset tak berwujud", "Investasi jangka panjang"]),
        ("Contoh aset lancar pada sebuah toko ritel adalah ...", "Uang kas di kasir, piutang usaha, dan persediaan barang dagang", ["Gedung toko dan tanah", "Mesin pabrik", "Hak paten merk"]),
        ("Aset berwujud yang memiliki masa manfaat ekonomis lebih dari satu tahun dan digunakan dalam operasi usaha dinamakan ...", "Aset tetap (Fixed Assets)", ["Aset lancar", "Aset moneter", "Beban operasional"]),
        ("Contoh aset tetap suatu perusahaan adalah ...", "Tanah, bangunan gedung, mesin, dan kendaraan operasional", ["Uang kas kecil", "Persediaan barang", "Perlengkapan tulis"]),
        ("Aset non-fisik bernilai tinggi seperti merk dagang, hak cipta, lisensi, dan nama baik perusahaan dinamakan ...", "Aset tidak berwujud (Intangible Assets)", ["Aset tetap", "Aset lancar", "Aset fiktif"]),
        ("Nilai lebih yang dimiliki perusahaan karena reputasi baik, pelanggan setia, dan manajemen unggul dinamakan ...", "Goodwill", ["Hak paten", "Hak cipta", "Royalti"]),
        ("Buku catatan pertama tempat seluruh transaksi keuangan dicatat secara kronologis urutan tanggal dinamakan ...", "Jurnal umum", ["Buku besar", "Neraca saldo", "Laporan laba rugi"]),
        ("Kumpulan akun-akun sejenis yang digunakan untuk mengelompokkan saldo aset, utang, modal, pendapatan, dan beban dinamakan ...", "Buku besar (General Ledger)", ["Jurnal umum", "Kertas kerja", "Neraca"]),
        ("Laporan keuangan yang menyajikan rincian pendapatan dan beban usaha untuk mengetahui apakah perusahaan laba atau rugi dinamakan ...", "Laporan Laba Rugi (Income Statement)", ["Laporan Posisi Keuangan (Neraca)", "Laporan Arus Kas", "Laporan Ekuitas"]),
        ("Laporan keuangan yang menyajikan posisi aset, kewajiban utang, dan ekuitas modal perusahaan pada tanggal tertentu dinamakan ...", "Neraca (Laporan Posisi Keuangan / Balance Sheet)", ["Laporan Laba Rugi", "Jurnal Penyesuaian", "Buku Kas"]),
        ("Laporan keuangan yang menyajikan perincian penerimaan dan pengeluaran uang kas selama periode tertentu dinamakan ...", "Laporan Arus Kas (Cash Flow Statement)", ["Neraca saldo", "Laporan laba rugi", "Buku besar"]),
        ("Pengambilan uang kas atau aset perusahaan oleh pemilik untuk keperluan pribadi dinamakan transaksi ...", "Prive (Withdrawal)", ["Dividen", "Beban gaji", "Investasi tambahan"]),
        ("Sistem pembukuan modern di mana setiap transaksi dicatat pada sisi debit dan sisi kredit secara seimbang diciptakan oleh ...", "Luca Pacioli", ["Adam Smith", "David Ricardo", "John Locke"]),
        ("Luca Pacioli yang dijuluki sebagai 'Bapak Akuntansi Dunia' berasal dari negara ...", "Italia", ["Inggris", "Prancis", "Belanda"]),
        ("Kondisi keuangan perusahaan di mana nilai aset lancarnya tidak mampu membayar kewajiban utang jangka pendeknya disebut tidak ...", "Likuid (Ilikuid)", ["Solvabel", "Rentabel", "Audit"]),
        ("Kemampuan perusahaan dalam memenuhi seluruh kewajiban finansialnya baik jangka pendek maupun jangka panjang dinamakan ...", "Solvabilitas", ["Likuiditas", "Rentabilitas", "Aktivitas"]),
        ("Kemampuan perusahaan dalam menghasilkan laba dari seluruh modal dan aset yang dikelolanya dinamakan ...", "Rentabilitas (Profitabilitas)", ["Likuiditas", "Solvabilitas", "Validitas"]),
    ]
    for q_text, corr, dists in accounting_basics:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami persamaan dasar akuntansi, aset, liabilitas, laporan laba rugi, dan neraca."))

    # 13. Tokoh Pemikiran Ekonomi & Literasi Keuangan Praktis (50 soal)
    economic_thinkers_financial_literacy = [
        ("Semboyan ekonomi klasik 'Laissez-faire, laissez-passer' memiliki arti filosofis yaitu ...", "Biarkan bebas berjalan tanpa campur tangan pemerintah", ["Atur semua perdagangan", "Pajak harus tinggi", "Emas adalah segalanya"]),
        ("Konsep 'Tangan Tak Terlihat' (The Invisible Hand) yang mengatur keseimbangan pasar bebas secara alami dikemukakan oleh ...", "Adam Smith", ["Karl Marx", "John Maynard Keynes", "Milton Friedman"]),
        ("Tokoh ekonom Inggris yang menulis buku 'The General Theory of Employment, Interest, and Money' dan menganjurkan intervensi pemerintah saat krisis adalah ...", "John Maynard Keynes", ["Adam Smith", "David Ricardo", "Friedrich Hayek"]),
        ("Tokoh filsuf asal Jerman yang menulis buku 'Das Kapital' dan mengkritik sistem kapitalisme serta mencetuskan komunisme adalah ...", "Karl Marx", ["Adam Smith", "Max Weber", "Jean-Baptiste Say"]),
        ("Teori Malthus yang dikemukakan Thomas Robert Malthus mengkhawatirkan terjadinya kelaparan dunia karena pertumbuhan penduduk mengikuti deret ukur sedangkan pertumbuhan pangan mengikuti ...", "Deret hitung", ["Deret ukur", "Deret kuadrat", "Deret logaritma"]),
        ("Tokoh ekonom Indonesia yang pernah menjabat Menteri Keuangan dan dijuluki sebagai Begawan Ekonomi Indonesia adalah ...", "Prof. Dr. Sumitro Djojohadikusumo", ["Mohammad Hatta", "Ali Wardhana", "Radius Prawiro"]),
        ("Menteri Keuangan Republik Indonesia yang berkali-kali dinobatkan sebagai Menteri Keuangan Terbaik di Asia dan Dunia adalah ...", "Sri Mulyani Indrawati", ["Chatib Basri", "Bambang Brodjonegoro", "Agus Martowardojo"]),
        ("Sistem Informasi Layanan Keuangan (SLIK) di bawah OJK yang mencatat riwayat kelancaran pembayaran kredit nasabah sebelumnya dinamakan ...", "BI Checking (SLIK OJK)", ["Kredit pintar", "Skor Pajak", "Nomor Induk Berusaha"]),
        ("Trik investasi aman yang berbunyi 'Don't put all your eggs in one basket' mengajarkan prinsip penting tentang ...", "Diversifikasi portofolio investasi untuk meminimalkan risiko", ["Membeli satu saham terbaik saja", "Menyimpan seluruh uang di rumah", "Meminjam modal maksimal"]),
        ("Dana yang disisihkan khusus untuk mengantisipasi kejadian mendesak seperti sakit atau kehilangan pekerjaan dinamakan ...", "Dana darurat (Emergency Fund)", ["Dana pensiun", "Modal usaha", "Tabungan haji"]),
        ("Besaran ideal dana darurat bagi seseorang yang masih lajang belum berkeluarga adalah minimal sebesar ...", "3 hingga 6 kali pengeluaran bulanan", ["1 kali pengeluaran", "12 tahun pengeluaran", "Cukup Rp 100 ribu"]),
        ("Bunga berbunga di mana bunga yang diperoleh di periode sebelumnya ikut menghasilkan bunga lagi di periode berikutnya dinamakan ...", "Bunga majemuk (Compound Interest)", ["Bunga tunggal", "Bunga flat", "Bunga diskonto"]),
        ("Albert Einstein pernah menyebut bunga majemuk sebagai keajaiban dunia ke- ...", "Delapan (The 8th Wonder of the World)", ["Tujuh", "Sembilan", "Sepuluh"]),
        ("Layanan pinjaman uang cepat berbasis online yang diawasi resmi oleh OJK dinamakan ...", "Fintech Lending (P2P Lending)", ["Pinjol ilegal", "Bank gelap", "Rentenir"]),
        ("Ciri utama pinjaman online (pinjol) ilegal yang berbahaya dan wajib dihindari masyarakat adalah ...", "Tidak terdaftar di OJK, bunga mencekik, dan menyalin kontak ponsel nasabah", ["Terdaftar di OJK", "Memiliki kantor resmi", "Bunga wajar transparan"]),
        ("Fasilitas pembiayaan belanja online dengan konsep 'beli sekarang, bayar nanti' dinamakan layanan ...", "Paylater", ["Cash on Delivery", "Debit otomatis", "Giro"]),
        ("Tindakan membeli barang secara spontan tanpa rencana matang saat melihat diskon dinamakan perilaku ...", "Impulsive buying (Belanja impulsif)", ["Konsumsi rasional", "Investasi cerdas", "Skala prioritas"]),
        ("Pola hidup hemat sederhana yang memprioritaskan fungsi barang dibanding gengsi merk dinamakan gaya hidup ...", "Frugal living (Minimalis hemat)", ["Hedonisme", "Konsumtif", "Boros"]),
        ("Penipuan investasi bodong yang membayar keuntungan kepada investor lama dari uang setoran investor baru dinamakan skema ...", "Skema Ponzi (Piramida)", ["Skema Saham", "Reksa Dana", "Bursa Berjangka"]),
        ("Pemberitahuan kepada masyarakat mengenai penipuan investasi ilegal dan pinjaman online bodong dikoordinasikan oleh satgas OJK yaitu ...", "Satgas PASTI (Satgas Pemberantasan Aktivitas Keuangan Ilegal)", ["Satpol PP", "Bareskrim", "KPK"]),
    ]
    for q_text, corr, dists in economic_thinkers_financial_literacy:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami tokoh pemikiran ekonomi, literasi finansial, dana darurat, dan diversifikasi investasi."))

    # 14. Istilah Bisnis, Korporasi & Akuntansi Tambahan (45 soal)
    business_corporate_terms = [
        ("Pengurangan nilai buku suatu aset tetap berwujud secara bertahap sepanjang masa manfaat ekonomisnya dinamakan ...", "Penyusutan (Depresiasi)", ["Amortisasi", "Apresiasi", "Likuidasi"]),
        ("Pengurangan nilai aset tidak berwujud seperti hak paten atau merk dagang secara bertahap dinamakan ...", "Amortisasi", ["Depresiasi", "Devaluasi", "Akresi"]),
        ("Pembubaran suatu perusahaan dan penjualan seluruh asetnya untuk melunasi utang-utang dinamakan ...", "Likuidasi", ["Merger", "Akuisisi", "Konsolidasi"]),
        ("Penggabungan dua atau lebih perusahaan menjadi satu perusahaan baru yang berdiri bersama dinamakan ...", "Konsolidasi", ["Merger", "Akuisisi", "Holding"]),
        ("Penggabungan di mana satu perusahaan menyerap perusahaan lain sehingga perusahaan yang diserap lenyap dinamakan ...", "Merger", ["Akuisisi", "Konsolidasi", "Kartel"]),
        ("Pengambilalihan kepemilikan saham pengendali suatu perusahaan oleh perusahaan lain dinamakan ...", "Akuisisi (Takeover)", ["Merger", "Likuidasi", "Konsolidasi"]),
        ("Bentuk kerja sama bisnis di mana pemilik merk memberi hak kepada pihak lain untuk menjual produknya dengan sistem bagi hasil dinamakan ...", "Waralaba (Franchise)", ["Kartel", "Monopoli", "Holding"]),
        ("Pemberi hak waralaba dalam bisnis dinamakan franchisor, sedangkan penerima hak waralaba dinamakan ...", "Franchisee", ["Investor", "Distributor", "Kreditor"]),
        ("Imbalan berkala yang dibayarkan oleh penerima waralaba atau lisensi kepada pemilik hak cipta merk dinamakan ...", "Royalti", ["Dividen", "Bunga", "Kupon"]),
        ("Perusahaan induk yang memiliki saham mayoritas pada beberapa anak perusahaan untuk mengendalikan manajemennya dinamakan ...", "Holding Company (Perusahaan Induk)", ["Kartel", "Trust", "Joint Venture"]),
        ("Bentuk kerja sama beberapa perusahaan sejenis untuk mengendalikan harga atau kuota produksi demi membatasi persaingan dinamakan ...", "Kartel", ["Merger", "Holding", "Konsorsium"]),
        ("Metode penilaian persediaan barang dagang di mana barang yang pertama kali masuk dianggap yang pertama kali dijual dinamakan metode ...", "FIFO (First In First Out)", ["LIFO", "Average", "Spesifik"]),
        ("Metode penilaian persediaan barang di mana barang yang terakhir masuk dianggap yang pertama keluar dinamakan ...", "LIFO (Last In First Out)", ["FIFO", "Average", "Moving"]),
        ("Pemeriksaan independen atas laporan keuangan perusahaan oleh pihak akuntan publik bersertifikat dinamakan ...", "Audit keuangan", ["Akuntansi biaya", "Konsultasi pajak", "Likuidasi"]),
        ("Akuntan profesional independen yang memberikan opini audit atas kewajaran laporan keuangan adalah ...", "Akuntan Publik (CPA)", ["Akuntan Internal", "Akuntan Pemerintah", "Fiskus"]),
        ("Opini audit tertinggi yang menyatakan laporan keuangan disajikan secara wajar dalam semua hal material adalah opini ...", "WTP (Wajar Tanpa Pengecualian / Unqualified Opinion)", ["WDP (Wajar Dengan Pengecualian)", "Tidak Wajar", "Menolak Memberikan Pendapat"]),
        ("Seluruh uang hasil penjualan kotor yang diterima bisnis sebelum dikurangi biaya operasional dinamakan ...", "Omzet (Pendapatan kotor)", ["Laba bersih", "Margin", "Dividen"]),
        ("Sisa keuntungan yang diperoleh bisnis setelah seluruh pendapatan dikurangi seluruh biaya dan beban pajak dinamakan ...", "Laba bersih (Net Profit)", ["Omzet", "Laba kotor", "EBITDA"]),
        ("Hak klaim perusahaan kepada pihak pembeli atas penjualan barang yang pembayarannya belum dilunasi dinamakan ...", "Piutang usaha (Accounts Receivable)", ["Utang usaha", "Beban dibayar di muka", "Modal saham"]),
        ("Kewajiban perusahaan untuk membayar kepada pihak pemasok atas pembelian bahan baku secara kredit dinamakan ...", "Utang usaha (Accounts Payable)", ["Piutang usaha", "Aset lancar", "Prive"]),
        ("Dokumen bukti tertulis resmi atas terjadinya transaksi penerimaan uang kas yang ditandatangani penerima adalah ...", "Kuitansi", ["Faktur", "Nota debet", "Cek"]),
        ("Dokumen rincian tagihan penjualan barang dagangan secara kredit dari penjual kepada pembeli dinamakan ...", "Faktur (Invoice)", ["Kuitansi", "Nota kredit", "Kupon"]),
    ]
    for q_text, corr, dists in business_corporate_terms:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami istilah bisnis, merger, akuisisi, waralaba, audit, dan omzet."))

    # 15. Mata Uang Dunia & Valas (35 soal)
    world_currencies = [
        ("Mata uang resmi bursa keuangan di negara Jepang yang bersimbol JPY adalah ...", "Yen", ["Yuan", "Won", "Ringgit"]),
        ("Mata uang resmi yang diterbitkan oleh People's Bank of China adalah ...", "Yuan (Renminbi)", ["Yen", "Won", "Dollar"]),
        ("Mata uang resmi bursa Korea Selatan yang bersimbol KRW adalah ...", "Won", ["Yen", "Yuan", "Peso"]),
        ("Mata uang resmi Reserve Bank of India yang bersimbol INR adalah ...", "Rupee", ["Rupiah", "Taka", "Kyat"]),
        ("Mata uang resmi bank sentral Rusia yang bersimbol RUB adalah ...", "Rubel", ["Euro", "Krona", "Zloty"]),
        ("Mata uang resmi Bank of England di Britania Raya bersimbol GBP adalah ...", "Poundsterling (GBP)", ["Euro", "Franc", "Dollar"]),
        ("Mata uang bersama yang digunakan oleh sebagian besar negara anggota Uni Eropa adalah ...", "Euro (EUR)", ["Poundsterling", "Krona", "Franc"]),
        ("Mata uang resmi Kerajaan Arab Saudi yang bersimbol SAR adalah ...", "Riyal Arab Saudi", ["Dirham", "Dinar", "Pound"]),
        ("Mata uang resmi yang digunakan di negara Uni Emirat Arab (Dubai & Abu Dhabi) adalah ...", "Dirham UEA", ["Riyal", "Dinar", "Rupiah"]),
        ("Mata uang yang memiliki nilai nominal tukar tertinggi di dunia terhadap Dolar AS berasal dari negara ...", "Dinar Kuwait (KWD)", ["Poundsterling", "Euro", "Riyal"]),
        ("Mata uang resmi yang digunakan di negara Swiss yang terkenal aman dan stabil adalah ...", "Franc Swiss (CHF)", ["Euro", "Pound", "Mark"]),
        ("Mata uang resmi Republik Turki yang bersimbol TRY adalah ...", "Lira Turki", ["Dirham", "Dinar", "Euro"]),
        ("Mata uang resmi Afrika Selatan yang bersimbol ZAR di pasar valas adalah ...", "Rand", ["Pound", "Dollar", "Shilling"]),
        ("Mata uang resmi yang digunakan di negara Brasil di Amerika Selatan adalah ...", "Real Brasil", ["Peso", "Bolivar", "Sol"]),
        ("Mata uang resmi yang digunakan di negara Meksiko adalah ...", "Peso Meksiko", ["Dollar", "Real", "Bolivar"]),
        ("Mata uang cadangan devisa internasional yang paling dominan digunakan dalam perdagangan global adalah ...", "Dolar Amerika Serikat (USD)", ["Euro", "Yen", "Pound"]),
    ]
    for q_text, corr, dists in world_currencies:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami nama mata uang resmi berbagai negara di dunia."))

    # 16. Pasar Modal & Investasi Saham Lanjutan (40 soal)
    stock_market_advanced = [
        ("Satuan standar minimal pembelian saham di Bursa Efek Indonesia (BEI) adalah satu lot yang berisi ...", "100 lembar saham", ["10 lembar saham", "50 lembar saham", "1.000 lembar saham"]),
        ("Kelompok saham dari perusahaan besar terpercaya yang berkinerja stabil dan rutin membagikan dividen dijuluki saham ...", "Blue Chip (Lapis Satu)", ["Second Liner", "Junk Bond", "Saham Gorengan"]),
        ("Saham perusahaan dengan kapitalisasi pasar kecil yang harganya sangat fluktuatif dan mudah dimanipulasi sering dijuluki saham ...", "Gorengan (Third Liner)", ["Blue chip", "LQ45", "Indeks utama"]),
        ("Harga penawaran beli saham yang diajukan oleh calon investor pembeli di aplikasi sekuritas dinamakan harga ...", "Bid", ["Ask (Offer)", "Strike price", "Closing price"]),
        ("Harga penawaran jual saham yang dipasang oleh pemilik saham yang ingin menjual sahamnya dinamakan harga ...", "Ask / Offer", ["Bid", "Open price", "NAV"]),
        ("Tanggal terakhir bagi investor untuk membeli saham agar berhak mendapatkan dividen perusahaan dinamakan tanggal ...", "Cum Date (Cumulative Date)", ["Ex Date", "Recording Date", "Payment Date"]),
        ("Hari bursa pertama di mana pembelian saham sudah tidak lagi mendapatkan hak pembagian dividen dinamakan ...", "Ex Date (Expired Date)", ["Cum Date", "Payment Date", "Recording Date"]),
        ("Tanggal pencatatan nama pemegang saham yang berhak atas dividen dalam daftar pemegang saham dinamakan ...", "Recording Date", ["Cum Date", "Ex Date", "Payment Date"]),
        ("Tanggal pencairan dan pengiriman dana dividen tunai langsung ke rekening saldo investor dinamakan ...", "Payment Date", ["Cum Date", "Ex Date", "Recording Date"]),
        ("Aksi korporasi memecah nilai nominal saham menjadi pecahan lebih kecil agar harga saham lebih terjangkau dinamakan ...", "Stock Split (Pemecahan Saham)", ["Reverse Stock Split", "Right Issue", "Buyback"]),
        ("Aksi korporasi menggabungkan beberapa lembar saham menjadi satu lembar saham baru dengan harga lebih tinggi dinamakan ...", "Reverse Stock Split", ["Stock Split", "Right Issue", "IPO"]),
        ("Penerbitan saham baru oleh perusahaan terbuka dengan memberikan hak memesan efek terlebih dahulu kepada pemegang saham lama dinamakan ...", "Right Issue (HMETD)", ["Stock Split", "Bonus Share", "Obligasi"]),
        ("Tindakan perusahaan membeli kembali saham-sahamnya yang beredar di pasar bursa dinamakan ...", "Buyback Saham", ["IPO", "Right Issue", "Delisting"]),
        ("Penghapusan pencatatan saham suatu emiten dari papan perdagangan Bursa Efek Indonesia dinamakan ...", "Delisting", ["Relisting", "Suspend", "IPO"]),
        ("Penghentian sementara perdagangan suatu saham oleh pihak bursa efek akibat pergerakan harga tidak wajar dinamakan ...", "Suspensi saham (Suspend)", ["Delisting", "Auto reject", "Right issue"]),
        ("Batas maksimal persentase kenaikan harga saham dalam satu hari bursa di BEI yang memicu penghentian otomatis disebut batas ...", "Auto Rejection Atas (ARA)", ["Auto Rejection Bawah (ARB)", "Circuit Breaker", "Margin Call"]),
        ("Batas maksimal persentase penurunan harga saham terendah dalam satu hari bursa di BEI dinamakan ...", "Auto Rejection Bawah (ARB)", ["Auto Rejection Atas (ARA)", "Stop Loss", "Cut Loss"]),
        ("Obligasi atau surat berharga syariah yang diterbitkan dengan akad tanpa riba dinamakan ...", "Sukuk", ["Kupon konvensional", "Saham preferen", "Waran"]),
        ("Nilai Aktiva Bersih per Unit Penyertaan (NAB/UP) pada reksa dana mencerminkan ...", "Harga wajar per unit reksa dana yang dikelola manajer investasi", ["Besar dividen", "Jumlah investor", "Biaya admin"]),
        ("Reksa dana yang seluruh portofolio investasinya dialokasikan pada instrumen pasar uang berjangka pendek dan paling rendah risiko adalah ...", "Reksa Dana Pasar Uang (RDPU)", ["Reksa Dana Saham", "Reksa Dana Campuran", "Reksa Dana Terproteksi"]),
    ]
    for q_text, corr, dists in stock_market_advanced:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami mekanisme pasar modal, lot saham, ARA/ARB, dividen, dan reksa dana."))

    # 17. Lembaga Kerja Sama Ekonomi Dunia & Teori Tambahan (50 soal)
    global_economic_organizations = [
        ("Organisasi Perdagangan Dunia yang mengawasi aturan perjanjian perdagangan multilateral antarnegara berpusat di Jenewa adalah ...", "WTO (World Trade Organization)", ["ILO", "WHO", "UNESCO"]),
        ("Kelompok 20 negara dengan perekonomian terbesar dunia yang mencakup 85% PDB global di mana Indonesia menjadi anggotanya adalah forum ...", "G20", ["G7", "BRICS", "OECD"]),
        ("Kelompok 7 negara industri maju yang terdiri dari AS, Inggris, Prancis, Jerman, Italia, Jepang, dan Kanada dinamakan kelompok ...", "G7", ["G20", "BRICS", "OECD"]),
        ("Organisasi Kerja Sama dan Pembangunan Ekonomi negara-negara berpendapatan tinggi yang berpusat di Paris dinamakan ...", "OECD", ["OPEC", "APEC", "NAFTA"]),
        ("Bank Pembangunan Asia yang berpusat di Kota Manila Filipina dinamakan ...", "ADB (Asian Development Bank)", ["AIIB", "IDB", "Bank Dunia"]),
        ("Bank Pembangunan Islam yang berpusat di Kota Jeddah Arab Saudi dinamakan ...", "IDB (Islamic Development Bank)", ["ADB", "AIIB", "IMF"]),
        ("Bank Investasi Infrastruktur Asia yang diinisiasi oleh Tiongkok dan berpusat di Beijing dinamakan ...", "AIIB (Asian Infrastructure Investment Bank)", ["ADB", "IDB", "Bank Dunia"]),
        ("Kelompok negara berkembang raksasa ekonomi baru yang awalnya terdiri dari Brasil, Rusia, India, Tiongkok, dan Afrika Selatan dinamakan ...", "BRICS", ["G7", "OECD", "ASEAN"]),
        ("Organisasi buruh internasional di bawah naungan PBB yang memperjuangkan hak-hak pekerja sedunia dinamakan ...", "ILO (International Labour Organization)", ["WHO", "FAO", "UNICEF"]),
        ("Perjanjian perdagangan bebas antara Amerika Serikat, Kanada, dan Meksiko dinamakan ...", "USMCA (sebelumnya NAFTA)", ["AFTA", "Uni Eropa", "Mercosur"]),
        ("Blok perdagangan regional negara-negara di Amerika Selatan bagian selatan dinamakan ...", "Mercosur", ["NAFTA", "AFTA", "APEC"]),
        ("Kawasan ekonomi khusus yang dibentuk oleh pemerintah dengan memberikan insentif pajak untuk menarik investor manufaktur ekspor dinamakan ...", "KEK (Kawasan Ekonomi Khusus)", ["Kawasan Lindung", "Kawasan Cagar", "Zona Hijau"]),
        ("Sistem pembayaran transaksi lintas negara antar bank di seluruh dunia menggunakan jaringan kode pesan aman dinamakan jaringan ...", "SWIFT", ["RTGS", "Kliring", "QRIS"]),
        ("Sistem transfer dana elektronik bernilai besar antar bank di Indonesia yang diselesaikan secara seketika (real time) oleh BI adalah ...", "BI-RTGS (Real Time Gross Settlement)", ["Kliring SKNBI", "BI-FAST", "ATM"]),
        ("Layanan transfer antar bank ritel nasional yang beroperasi 24 jam nonstop dengan biaya terjangkau Rp 2.500 per transaksi adalah ...", "BI-FAST", ["RTGS", "Kliring warkat", "Western Union"]),
        ("Uang elektronik yang nilainya tersimpan langsung pada chip kartu fisik (seperti e-Money dan Flazz) tergolong uang elektronik berbasis ...", "Chip (Chip-based)", ["Server (Server-based)", "Giral", "Kertas"]),
        ("Uang elektronik yang nilainya tersimpan pada server aplikasi (seperti GoPay, OVO, DANA, ShopeePay) tergolong berbasis ...", "Server (Server-based)", ["Chip-based", "Uang kartal", "Komoditas"]),
        ("Pajak yang dikenakan oleh pemerintah daerah atas makanan dan minuman yang dibeli pengunjung di restoran dinamakan ...", "PB1 (Pajak Restoran)", ["PPN", "PPh", "PBB"]),
        ("Pajak yang dikenakan atas transaksi jual beli rumah atau tanah yang dibayarkan oleh pembeli dinamakan ...", "BPHTB (Bea Perolehan Hak atas Tanah dan Bangunan)", ["PBB", "PPh Final", "PPN"]),
        ("Pajak penghasilan yang dikenakan kepada penjual tanah atau bangunan atas pengalihan hak dinamakan ...", "PPh Final Pengalihan Tanah dan Bangunan", ["BPHTB", "PBB", "Cukai"]),
    ]
    for q_text, corr, dists in global_economic_organizations:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami organisasi ekonomi dunia, G20, sistem pembayaran SWIFT, BI-FAST, dan perpajakan properti."))

    # 18. Teori Pertumbuhan Ekonomi & Pembangunan (35 soal)
    growth_theories = [
        ("Teori tahap-tahap pertumbuhan ekonomi yang membagi pembangunan menjadi 5 tahapan dari tradisional hingga konsumsi tinggi dikemukakan oleh ...", "W.W. Rostow", ["Joseph Schumpeter", "Robert Solow", "David Ricardo"]),
        ("Tahap ketiga dalam teori pertumbuhan Rostow di mana terjadi revolusi industri dan kemajuan investasi pesat dinamakan tahap ...", "Tinggal landas (Take-off)", ["Masyarakat tradisional", "Prasyarat tinggal landas", "Konsumsi massal tinggi"]),
        ("Tahap puncak tertinggi dalam teori pertumbuhan ekonomi Rostow di mana masyarakat menikmati kemakmuran dan kesejahteraan konsumsi adalah ...", "Konsumsi massal tinggi (Age of High Mass Consumption)", ["Tinggal landas", "Menuju kedewasaan", "Tradisional"]),
        ("Tokoh ekonom yang menekankan bahwa motor penggerak utama pertumbuhan ekonomi adalah inovasi wirausahawan (entrepreneur) adalah ...", "Joseph Schumpeter", ["Robert Solow", "Adam Smith", "Thomas Malthus"]),
        ("Konsep Schumpeter di mana inovasi teknologi baru meruntuhkan industri lama yang usang dinamakan konsep ...", "Creative Destruction (Penghancuran Kreatif)", ["Invisible hand", "Laissez-faire", "Diminishing return"]),
        ("Teori pertumbuhan ekonomi Neoklasik yang menekankan peran kemajuan teknologi, tenaga kerja, dan modal dirumuskan oleh ...", "Robert Solow", ["W.W. Rostow", "Karl Marx", "David Ricardo"]),
        ("Indeks Pembangunan Manusia (IPM / HDI) yang dirilis oleh UNDP mengukur kemajuan pembangunan suatu negara dari tiga dimensi utama yaitu ...", "Kesehatan, Pendidikan, dan Standar Hidup Layak (Pengeluaran)", ["Kekayaan alam, tentara, dan luas wilayah", "Jumlah jalan tol, mobil, dan pesawat", "Pajak, utang, dan bunga"]),
        ("Dimensi kesehatan pada Indeks Pembangunan Manusia (IPM) diukur melalui indikator ...", "Angka Harapan Hidup saat lahir (Life Expectancy)", ["Jumlah rumah sakit", "Banyaknya dokter", "Angka kelahiran"]),
        ("Dimensi pendidikan pada Indeks Pembangunan Manusia (IPM) diukur menggunakan dua indikator yaitu ...", "Harapan Lama Sekolah dan Rata-rata Lama Sekolah", ["Jumlah universitas", "Nilai ujian akhir", "Gaji guru"]),
        ("Dimensi standar hidup layak pada IPM diukur berdasarkan besarnya ...", "Pengeluaran riil per kapita yang disesuaikan (daya beli)", ["Gaji presiden", "Nilai tukar rupiah", "Total APBN"]),
        ("Bank Perkreditan Rakyat (BPR) adalah lembaga perbankan yang melayani masyarakat mikro yang menurut undang-undang dilarang untuk ...", "Menerima simpanan giro dan melakukan transaksi valuta asing", ["Menerima tabungan", "Memberikan kredit pinjaman", "Menerima deposito"]),
        ("Perbedaan utama kartu debit dan kartu kredit adalah kartu debit memotong saldo rekening sendiri, sedangkan kartu kredit ...", "Meminjam dana talangan batas limit dari bank yang wajib dilunasi kemudian", ["Memberikan uang gratis", "Hanya bisa dipakai di luar negeri", "Tidak bisa tarik tunai"]),
        ("Prinsip dasar dalam asuransi syariah (takaful) yang membedakannya dari asuransi konvensional adalah prinsip ...", "Tolong-menolong (Ta'awun) dan saling berbagi risiko (Sharing of risk)", ["Pemindahan risiko (Transfer of risk)", "Mencari keuntungan bunga", "Spekulasi untung-rugi"]),
        ("Dana kebajikan yang dihibahkan secara ikhlas oleh para peserta asuransi syariah untuk membantu peserta lain yang terkena musibah dinamakan dana ...", "Tabarru'", ["Tijarah", "Mudharabah", "Ijarah"]),
    ]
    for q_text, corr, dists in growth_theories:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami teori Rostow, Schumpeter, IPM, BPR, dan asuransi syariah."))

    # 19. Bisnis Digital, E-Commerce & Startup (40 soal)
    digital_economy = [
        ("Gelar sebutan bagi perusahaan rintisan (startup) teknologi yang berhasil mencapai nilai valuasi di atas 1 miliar Dolar AS adalah ...", "Unicorn", ["Decacorn", "Hectocorn", "Centaur"]),
        ("Gelar sebutan bagi perusahaan teknologi rintisan yang berhasil menembus nilai valuasi di atas 10 miliar Dolar AS adalah ...", "Decacorn", ["Unicorn", "Hectocorn", "Soonicorn"]),
        ("Gelar bagi perusahaan teknologi raksasa global yang valuasinya menembus angka di atas 100 miliar Dolar AS adalah ...", "Hectocorn", ["Decacorn", "Unicorn", "Mega-startup"]),
        ("Contoh startup asal Indonesia yang berhasil meraih status Decacorn adalah ...", "GoTo (Gojek)", ["Kopi Kenangan", "Ajaib", "Ruangguru"]),
        ("Model bisnis perdagangan elektronik di mana transaksi jual beli terjadi antar sesama konsumen pengguna di marketplace dinamakan model ...", "C2C (Consumer to Consumer)", ["B2B", "B2C", "B2G"]),
        ("Model bisnis di mana perusahaan produsen menjual produknya langsung kepada konsumen akhir secara online dinamakan ...", "B2C (Business to Consumer)", ["B2B", "C2C", "C2B"]),
        ("Model bisnis perdagangan online di mana transaksi terjadi antara satu perusahaan bisnis dengan perusahaan bisnis lain dinamakan ...", "B2B (Business to Business)", ["B2C", "C2C", "B2G"]),
        ("Sistem transaksi belanja online di mana pembeli membayar uang tunai langsung kepada kurir saat barang tiba di rumah adalah ...", "COD (Cash on Delivery)", ["Paylater", "Transfer bank", "Giro"]),
        ("Model bisnis penjualan online di mana penjual tidak perlu menyetok barang secara fisik dan barang dikirimkan langsung oleh produsen ke pembeli atas nama penjual dinamakan bisnis ...", "Dropshipping (Dropship)", ["Reseller grosir", "Waralaba", "Konsinyasi"]),
        ("Pelaku usaha yang membeli stok barang dagangan dalam jumlah tertentu dari supplier untuk disimpan dan dijual kembali dengan harga eceran disebut ...", "Reseller", ["Dropshipper", "Konsumen", "Afiliator"]),
        ("Program pemasaran digital di mana seseorang membagikan tautan link produk dan mendapatkan persentase komisi setiap kali ada pembelian dari link tersebut dinamakan ...", "Affiliate Marketing (Afiliasi)", ["Endorsement", "Dropship", "Sponsorship"]),
        ("Aktivitas promosi produk di media sosial oleh selebritas atau influencer berbayar untuk mengenalkan merk kepada pengikutnya dinamakan ...", "Endorsement", ["Dropshipping", "Afiliasi", "Crowdfunding"]),
        ("Metode penggalangan dana modal secara massal dari masyarakat luas melalui platform online untuk mendanai proyek atau bisnis dinamakan ...", "Crowdfunding (Urun Dana)", ["Venture Capital", "IPO", "Pinjol"]),
    ]
    for q_text, corr, dists in digital_economy:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami istilah bisnis digital, unicorn, decacorn, e-commerce, dan dropshipping."))

    # 20. Manajemen Pemasaran & Strategi Bisnis (45 soal)
    marketing_and_strategy = [
        ("Empat elemen bauran pemasaran (Marketing Mix 4P) klasik untuk produk barang yang dikemukakan E. Jerome McCarthy adalah ...", "Product, Price, Place, dan Promotion", ["People, Process, Profit, Packaging", "Production, Planning, Payroll, Policy", "Plant, Purchase, Profit, Price"]),
        ("Tiga elemen tambahan dalam bauran pemasaran jasa (Marketing Mix 7P) melengkapi 4P adalah ...", "People, Process, dan Physical Evidence", ["Price, Profit, Power", "Planning, Publicity, Public", "Policy, Payroll, Plant"]),
        ("Tiga tahapan strategi pemasaran modern yang disingkat STP adalah ...", "Segmenting, Targeting, dan Positioning", ["Selling, Trading, Purchasing", "Saving, Transferring, Paying", "Supplying, Tracking, Pricing"]),
        ("Proses membagi-bagi pasar yang heterogen ke dalam kelompok-kelompok pembeli yang memiliki kebutuhan atau karakteristik serupa dinamakan ...", "Segmentasi Pasar (Segmenting)", ["Targeting", "Positioning", "Branding"]),
        ("Proses mengevaluasi dan memilih satu atau beberapa segmen pasar yang paling potensial untuk dimasuki dinamakan ...", "Targeting (Penentuan Pasar Sasaran)", ["Segmenting", "Positioning", "Advertising"]),
        ("Upaya menanamkan citra, persepsi unik, dan keunggulan produk di benak pikiran konsumen dibanding pesaing dinamakan ...", "Positioning (Penempatan Posisi)", ["Segmenting", "Targeting", "Budgeting"]),
        ("Metode analisis perencanaan strategis bisnis yang mengevaluasi faktor internal dan eksternal dinamakan analisis ...", "SWOT (Strengths, Weaknesses, Opportunities, Threats)", ["POAC", "BCG Matrix", "PESTEL"]),
        ("Pada analisis SWOT, huruf 'S' (Strengths) dan 'W' (Weaknesses) mengevaluasi kondisi faktor ...", "Internal perusahaan", ["Eksternal lingkungan", "Internasional", "Kompetitor"]),
        ("Pada analisis SWOT, huruf 'O' (Opportunities) dan 'T' (Threats) mengevaluasi kondisi faktor ...", "Eksternal lingkungan pasar", ["Internal perusahaan", "Keuangan internal", "Karyawan"]),
        ("Tanda pengenal berupa nama, istilah, simbol, atau logo yang membedakan produk suatu produsen dari produk pesaing dinamakan ...", "Merek (Brand)", ["Paten", "Faktur", "Katalog"]),
        ("Bentuk promosi penjualan non-personal melalui media massa berbayar untuk memikat minat calon pembeli dinamakan ...", "Periklanan (Advertising)", ["Penjualan pribadi", "Humas", "Publisitas gratis"]),
        ("Aktivitas promosi penjualan langsung tatap muka antara wiraniaga penjual dengan calon pembeli dinamakan ...", "Personal Selling (Penjualan Tatap Muka)", ["Advertising", "Sales Promotion", "Direct Mail"]),
        ("Pemberian insentif jangka pendek seperti kupon diskon, beli satu gratis satu, atau sampel gratis untuk merangsang pembelian cepat dinamakan ...", "Promosi Penjualan (Sales Promotion)", ["Periklanan", "Humas", "Personal Selling"]),
        ("Strategi penetapan harga awal yang tinggi untuk produk teknologi baru yang inovatif lalu diturunkan perlahan dinamakan strategi ...", "Price Skimming", ["Penetration Pricing", "Bundle Pricing", "Predatory Pricing"]),
        ("Strategi menetapkan harga awal yang sangat murah untuk merebut pangsa pasar secara cepat dinamakan strategi ...", "Penetration Pricing (Harga Penetrasi)", ["Price Skimming", "Premium Pricing", "Loss Leader"]),
        ("Strategi menjual barang dengan harga di bawah biaya produksi untuk menyingkirkan pesaing dari pasar dinamakan praktik ...", "Predatory Pricing (Jual Rugi Predator)", ["Penetration Pricing", "Price Skimming", "Dumping"]),
    ]
    for q_text, corr, dists in marketing_and_strategy:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami bauran pemasaran 4P, 7P, analisis SWOT, dan strategi harga bisnis."))

    # 21. Analisis Keuangan, Hilirisasi & Konsep Ekonomi Terapan (70 soal)
    applied_finance_and_modern_economy = [
        ("Tingkat kemudahan suatu aset atau kekayaan untuk diubah menjadi uang tunai tanpa mengalami penurunan nilai dinamakan ...", "Likuiditas", ["Solvabilitas", "Rentabilitas", "Volatilitas"]),
        ("Aset keuangan yang memiliki tingkat likuiditas paling tinggi dan sempurna di dunia adalah ...", "Uang tunai (Kas)", ["Tanah bangunan", "Saham preferen", "Emas batangan"]),
        ("Aset kekayaan yang memiliki tingkat likuiditas paling rendah karena butuh waktu berbulan-bulan untuk menjualnya adalah ...", "Properti tanah dan gedung", ["Uang tunai", "Reksa dana pasar uang", "Saham LQ45"]),
        ("Rasio keuangan yang mengukur laba bersih yang dihasilkan dari setiap rupiah uang yang diinvestasikan dinamakan ...", "ROI (Return on Investment)", ["ROE", "EPS", "PER"]),
        ("Rasio yang mengukur kemampuan perusahaan menghasilkan laba bersih dari modal ekuitas pemilik saham dinamakan ...", "ROE (Return on Equity)", ["ROI", "ROA", "DER"]),
        ("Rasio valuasi saham yang membandingkan harga pasar per lembar saham dengan laba bersih per lembar sahamnya adalah rasio ...", "PER (Price to Earnings Ratio)", ["PBV", "DER", "ROE"]),
        ("Rasio valuasi saham yang membandingkan harga pasar saham dengan nilai buku ekuitas per lembar sahamnya adalah ...", "PBV (Price to Book Value)", ["PER", "EPS", "DER"]),
        ("Laba bersih perusahaan yang dibagikan untuk setiap satu lembar saham yang beredar dinamakan ...", "EPS (Earning Per Share)", ["PER", "PBV", "Dividen Yield"]),
        ("Nomor identitas tunggal bagi setiap investor di pasar modal Indonesia yang diterbitkan oleh KSEI dinamakan ...", "SID (Single Investor Identification)", ["NPWP", "NIK", "NIB"]),
        ("Rekening khusus atas nama investor di bank yang digunakan untuk menampung dana transaksi jual beli saham dinamakan ...", "RDN (Rekening Dana Nasabah)", ["Rekening Giro", "Rekening Koran", "Deposito"]),
        ("Lembaga di pasar modal Indonesia yang bertugas mengamankan penyimpanan sertifikat efek dan penyelesaian transaksi adalah ...", "PT KSEI (Kustodian Sentral Efek Indonesia)", ["PT BEI", "PT KPEI", "OJK"]),
        ("Lembaga yang bertugas menjamin dan menyelesaikan transaksi kliring bursa efek di Indonesia adalah ...", "PT KPEI (Kliring Penjaminan Efek Indonesia)", ["PT KSEI", "PT BEI", "Bank Indonesia"]),
        ("Pasar tempat saham perusahaan pertama kali dijual kepada masyarakat umum saat IPO sebelum dicatatkan di bursa efek dinamakan ...", "Pasar Perdana (Primary Market)", ["Pasar Sekunder", "Pasar Negosiasi", "Pasar Tunai"]),
        ("Pasar tempat jual beli saham antar sesama investor yang berlangsung setiap hari bursa di BEI dinamakan ...", "Pasar Sekunder (Secondary Market)", ["Pasar Perdana", "Pasar Gelap", "Pasar Komoditas"]),
        ("Surat simpanan berjangka di bank yang bukti kepemilikannya dapat diperjualbelikan atau dipindahtangankan kepada orang lain adalah ...", "Sertifikat Deposito", ["Deposito Berjangka biasa", "Buku Tabungan", "Giro"]),
        ("Perusahaan asuransi yang memberikan pertanggungan asuransi kepada perusahaan asuransi lain dinamakan perusahaan ...", "Reasuransi", ["Multifinance", "Leasing", "Pialang"]),
        ("Tiga syarat (3T) simpanan nasabah agar dijamin penuh oleh Lembaga Penjamin Simpanan (LPS) adalah tercatat dalam pembukuan, tingkat bunga di bawah batas LPS, dan ...", "Tidak melakukan tindakan yang merugikan bank (tidak kredit macet)", ["Harus memiliki deposito", "Menabung di atas Rp 2 miliar", "Memiliki NPWP"]),
        ("Kebijakan fiskal kontraktif (menaikkan tarif pajak dan memangkas belanja negara) diterapkan oleh pemerintah saat kondisi perekonomian ...", "Mengalami laju inflasi yang terlalu tinggi (Perekonomian memanas)", ["Mengalami resesi lesu", "Tingkat pengangguran melonjak", "Deflasi berkepanjangan"]),
        ("Kebijakan fiskal ekspansif (menurunkan pajak dan memperbesar belanja bantuan) diterapkan pemerintah saat ekonomi ...", "Mengalami resesi lesu dan tingkat pengangguran tinggi", ["Mengalami inflasi 100%", "Ekonomi terlalu panas", "Devisa melimpah"]),
        ("Hukum ekonomi klasik yang dikemukakan oleh Jean-Baptiste Say berbunyi bahwa 'Penawaran akan menciptakan permintaannya sendiri' dikenal sebagai ...", "Hukum Say (Say's Law)", ["Hukum Gossen", "Hukum Engel", "Hukum Gresham"]),
        ("Hukum Gresham dalam sejarah peredaran mata uang berbunyi bahwa 'Uang yang buruk akan menyingkirkan uang yang baik dari peredaran' dinamakan ...", "Hukum Gresham (Bad money drives out good money)", ["Hukum Say", "Hukum Fisher", "Hukum Malthus"]),
        ("Kurva yang menggambarkan adanya hubungan terbalik jangka pendek antara tingkat pengangguran dan laju inflasi dinamakan ...", "Kurva Phillips", ["Kurva Lorenz", "Kurva Engel", "Kurva Laffer"]),
        ("Kurva yang menggambarkan hubungan antara persentase tarif pajak dengan total penerimaan pajak negara dinamakan ...", "Kurva Laffer", ["Kurva Phillips", "Kurva Lorenz", "Kurva Indiferen"]),
        ("Tarif pajak impor yang dihitung berdasarkan persentase tertentu dari nilai harga barang impor dinamakan tarif ...", "Ad valorem", ["Spesifik", "Campuran", "Progresif"]),
        ("Tarif bea masuk impor yang dihitung berdasarkan jumlah fisik barang (misal per kilogram atau per liter) dinamakan tarif ...", "Spesifik", ["Ad valorem", "Proporsional", "Degresif"]),
        ("Kebijakan pemerintah Indonesia melarang ekspor bijih nikel dan bauksit mentah demi memprosesnya di dalam negeri dinamakan kebijakan ...", "Hilirisasi industri mineral", ["Privatisasi", "Nasionalisasi", "Liberalisasi"]),
        ("Tujuan utama dari program hilirisasi mineral tambang di Indonesia adalah ...", "Meningkatkan nilai tambah ekonomi, menyerap tenaga kerja, dan membangun pabrik smelter", ["Menurunkan harga logam", "Menghentikan produksi tambang", "Mengurangi cadangan devisa"]),
        ("Fasilitas pabrik pengolahan dan pemurnian hasil tambang mineral mentah menjadi produk logam setengah jadi dinamakan ...", "Smelter", ["Kilang minyak", "Pembangkit nuklir", "Silo"]),
        ("Model perekonomian ramah lingkungan yang meminimalkan limbah dan polusi dengan memperpanjang siklus hidup material melalui daur ulang dinamakan ...", "Ekonomi Sirkular (Circular Economy)", ["Ekonomi Linear", "Ekonomi Fosil", "Ekonomi Tradisional"]),
        ("Perekonomian yang berfokus pada pembangunan rendah karbon, efisiensi sumber daya alam, dan pencegahan kerusakan alam dinamakan ...", "Ekonomi Hijau (Green Economy)", ["Ekonomi Biru", "Ekonomi Abu-abu", "Ekonomi Merah"]),
        ("Perekonomian yang berfokus pada pemanfaatan berkelanjutan potensi sumber daya kelautan dan maritim dinamakan ...", "Ekonomi Biru (Blue Economy)", ["Ekonomi Hijau", "Ekonomi Sirkular", "Ekonomi Terbuka"]),
        ("Pajak yang dikenakan kepada entitas bisnis atas jumlah emisi gas rumah kaca yang dihasilkannya dinamakan ...", "Pajak Karbon (Carbon Tax)", ["Pajak Pertambahan Nilai", "Pajak Bumi", "Bea Cukai"]),
        ("Tempat resmi perdagangan unit sertifikat pengurangan emisi karbon di Indonesia yang diawasi oleh OJK adalah ...", "Bursa Karbon Indonesia (IDX Carbon)", ["Pasar Uang", "Bursa Berjangka Komoditi", "Bank Sentral"]),
    ]
    for q_text, corr, dists in applied_finance_and_modern_economy:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami likuiditas aset, rasio keuangan saham, hilirisasi industri, dan ekonomi hijau."))

    # 22. Keamanan Finansial Digital & Produk Perbankan Riil (40 soal)
    financial_security_and_products = [
        ("Kode angka rahasia 6 digit yang digunakan untuk mengamankan transaksi kartu debit di mesin ATM atau EDC adalah ...", "PIN (Personal Identification Number)", ["CVV", "OTP", "Password wifi"]),
        ("Tiga digit angka rahasia di bagian belakang kartu debit atau kredit yang tidak boleh diberitahukan kepada siapa pun adalah ...", "CVV / CVC (Card Verification Value)", ["PIN", "Nomor rekening", "Kode pos"]),
        ("Kode sandi rahasia sekali pakai yang dikirimkan melalui SMS atau WhatsApp untuk memverifikasi transaksi online dinamakan ...", "OTP (One Time Password)", ["PIN", "CVV", "Username"]),
        ("Kejahatan siber berupa pengiriman link atau situs palsu untuk memancing korban memberikan data pribadi kartu bank dinamakan ...", "Phishing", ["Skimming", "Carding", "Hacking"]),
        ("Modus pencurian data kartu ATM dengan menempelkan alat perekam ilegal pada slot mulut mesin ATM dinamakan ...", "Skimming", ["Phishing", "Spamming", "Phreaking"]),
        ("Manipulasi psikologis yang dilakukan oleh pelaku penipuan online untuk memperdaya korban agar mentransfer uang dinamakan ...", "Social Engineering (Rekayasa Sosial)", ["Skimming", "Malware", "DDoS"]),
        ("Laporan ringkasan bulanan dari bank yang memuat seluruh riwayat transaksi mutasi uang masuk dan keluar pada rekening nasabah dinamakan ...", "Rekening koran", ["Buku cek", "Bilyet giro", "Slip setoran"]),
        ("Suku bunga kebijakan acuan resmi yang ditetapkan oleh Bank Indonesia dalam rapat dewan gubernur bulanan dinamakan ...", "BI-Rate", ["Fed Rate", "Suku bunga pasar", "LPS Rate"]),
        ("Nilai rata-rata dari penjumlahan kurs jual dan kurs beli di bank dinamakan kurs ...", "Kurs tengah", ["Kurs pokok", "Kurs flat", "Kurs riil"]),
        ("Strategi keuangan untuk melindungi nilai aset atau transaksi perdagangan internasional dari risiko fluktuasi kurs mata uang asing dinamakan ...", "Lindung Nilai (Hedging)", ["Spekulasi", "Arbitrase", "Short selling"]),
        ("Surat jaminan resmi dari bank yang menjamin pembayaran pembeli kepada eksportir dalam transaksi perdagangan internasional dinamakan ...", "Letter of Credit (L/C)", ["Bill of Lading", "Invoice", "Packing list"]),
        ("Surat tanda terima resmi muatan barang di atas kapal laut dari perusahaan pelayaran kepada pihak pengirim dinamakan ...", "Bill of Lading (B/L)", ["Letter of Credit", "Faktur", "Asuransi"]),
        ("Jenis asuransi kendaraan bermotor yang hanya memberikan ganti rugi jika kendaraan hilang total atau rusak parah di atas 75% adalah ...", "Asuransi TLO (Total Loss Only)", ["Asuransi All Risk", "Asuransi Jiwa", "Asuransi Unit Link"]),
        ("Jenis asuransi kendaraan bermotor komprehensif yang menanggung seluruh risiko kerusakan mulai dari lecet baret hingga tabrakan berat adalah ...", "Asuransi All Risk (Comprehensive)", ["Asuransi TLO", "Asuransi Tanggung Jawab", "Asuransi Kebakaran"]),
        ("Surat berharga obligasi negara ritel yang diterbitkan oleh pemerintah Indonesia khusus untuk warga negara Indonesia investor perorangan adalah ...", "ORI (Obligasi Negara Ritel)", ["SBI", "IHSG", "SPN"]),
        ("Surat berharga syariah negara ritel yang berbasis akad syariah tanpa bunga yang diterbitkan pemerintah untuk masyarakat adalah ...", "Sukuk Ritel (SR)", ["ORI", "Saham LQ45", "Bilyet Giro"]),
        ("Metode pembiayaan patungan modal saham dari masyarakat untuk mendanai usaha UMKM melalui platform digital berizin OJK dinamakan ...", "Securities Crowdfunding (Urun Dana Efek)", ["Pinjaman online ilegal", "Arisan berantai", "Kredit bank"]),
        ("Penyedia jasa pembayaran yang memfasilitasi transaksi pembayaran digital di situs e-commerce dan aplikasi dinamakan ...", "Payment Gateway", ["Search Engine", "Web Browser", "Cloud Server"]),
        ("Uang panjar muka yang disetorkan pembeli sebagai bukti keseriusan untuk memesan atau membeli suatu aset dinamakan ...", "Uang muka (Down Payment / DP)", ["Cicilan", "Bunga anuitas", "Kupon"]),
    ]
    for q_text, corr, dists in financial_security_and_products:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami keamanan perbankan digital PIN/OTP, asuransi TLO/All Risk, ORI, dan sukuk ritel."))

    # 23. Perbankan Ritel, Sensus & Bappebti (20 soal)
    banking_census_and_crypto = [
        ("Komponen inflasi yang dipengaruhi oleh faktor musiman hasil panen pertanian dan cuaca dinamakan inflasi harga ...", "Bergejolak (Volatile Foods)", ["Inti (Core Inflation)", "Diatur pemerintah", "Impor"]),
        ("Komponen inflasi yang pergerakan harganya diatur dan dipengaruhi langsung oleh kebijakan tarif pemerintah (seperti BBM dan tarif listrik) dinamakan inflasi harga ...", "Diatur pemerintah (Administered Prices)", ["Inti", "Bergejolak", "Domestik"]),
        ("Lembaga pemerintah non-kementerian yang bertugas menyelenggarakan sensus penduduk dan menghitung angka inflasi bulanan di Indonesia adalah ...", "BPS (Badan Pusat Statistik)", ["Bappenas", "Bank Indonesia", "Kemenkeu"]),
        ("Sensus Penduduk di Indonesia diselenggarakan secara nasional oleh BPS secara berkala setiap ...", "10 tahun sekali (pada tahun berakhiran 0)", ["5 tahun sekali", "1 tahun sekali", "25 tahun sekali"]),
        ("Sensus Pertanian diselenggarakan oleh BPS di seluruh Indonesia setiap 10 tahun sekali pada tahun yang berakhiran ...", "Angka 3 (seperti 2013, 2023)", ["Angka 0", "Angka 5", "Angka 8"]),
        ("Sensus Ekonomi diselenggarakan oleh BPS setiap 10 tahun sekali pada tahun yang berakhiran ...", "Angka 6 (seperti 2006, 2016, 2026)", ["Angka 1", "Angka 4", "Angka 9"]),
        ("Program kredit perbankan bersubsidi bunga dari pemerintah untuk memperluas akses permodalan bagi pelaku UMKM adalah ...", "KUR (Kredit Usaha Rakyat)", ["KPR", "KTA", "Leasing"]),
        ("Fasilitas kredit pinjaman dari bank untuk pembelian rumah tinggal dengan jaminan sertifikat rumah dinamakan ...", "KPR (Kredit Pemilikan Rumah)", ["KTA", "KUR", "Leasing"]),
        ("Pinjaman dana dari bank tanpa mewajibkan nasabah menyerahkan jaminan agunan fisik dinamakan fasilitas ...", "KTA (Kredit Tanpa Agunan)", ["KPR", "Pegadaian", "Rahn"]),
        ("Status rekening tabungan di bank yang dibekukan sementara karena tidak pernah ada aktivitas transaksi selama 6 bulan berturut-turut dinamakan rekening ...", "Dormant (Pasif)", ["Aktif", "Giro", "Valas"]),
        ("Surat jaminan tertulis dari bank yang menjamin pembayaran jika nasabah kontraktor gagal menyelesaikan proyek dinamakan ...", "Bank Garansi", ["Letter of Credit", "Bilyet Giro", "Faktur"]),
        ("Badan pemerintah di bawah Kementerian Perdagangan yang bertugas mengawasi perdagangan berjangka komoditi dan aset digital kripto adalah ...", "Bappebti", ["OJK", "Bank Indonesia", "KPK"]),
        ("Nilai total kapitalisasi pasar (Market Cap) sebuah perusahaan di bursa efek diperoleh dari hasil kali antara ...", "Harga pasar per lembar saham dengan total jumlah lembar saham yang beredar", ["Laba bersih dengan dividen", "Total aset dengan utang", "Omzet dengan modal"]),
        ("Sistem bagi hasil pertanian tradisional di Jawa di mana petani penggarap dan pemilik sawah membagi hasil panen sama rata 50:50 dinamakan sistem ...", "Maro", ["Mertelu", "Ijon", "Rente"]),
        ("Sistem bagi hasil panen pertanian di mana penggarap mendapatkan sepertiga bagian hasil panen dinamakan sistem ...", "Mertelu", ["Maro", "Bawon", "Grosir"]),
    ]
    for q_text, corr, dists in banking_census_and_crypto:
        add_q(build_mcq("Ekonomi", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami inflasi inti/bergejolak, BPS, KUR, KPR, dan Bappebti."))

    return questions[:500]
