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

    # 1. Rumah Adat Tradisional Nusantara (30 soal)
    rumah_adat = [
        ("Rumah Gadang dengan atap melengkung runcing seperti tanduk kerbau (gonjong) berasal dari provinsi ...", "Sumatera Barat", ["Riau", "Jambi", "Sumatera Utara"]),
        ("Rumah adat Tongkonan dengan atap melengkung menyerupai perahu berasal dari suku Toraja di provinsi ...", "Sulawesi Selatan", ["Sulawesi Tengah", "Sulawesi Tenggara", "Sulawesi Utara"]),
        ("Rumah adat Honai berbentuk bulat beratap jerami tanpa jendela merupakan rumah khas suku Dani di pulau ...", "Papua", ["Maluku", "Sulawesi", "Nusa Tenggara"]),
        ("Rumah adat Joglo yang memiliki tiang utama soko guru merupakan rumah tradisional suku Jawa di provinsi ...", "Jawa Tengah, DI Yogyakarta, dan Jawa Timur", ["Jawa Barat dan Banten", "Bali dan NTB", "Lampung dan Bengkulu"]),
        ("Rumah adat Gapura Candi Bentar yang menyerupai pintu gerbang candi khas berasal dari provinsi ...", "Bali", ["Lombok", "Jawa Timur", "Banten"]),
        ("Rumah adat Bolon berbentuk panggung besar yang dihuni bersama merupakan rumah tradisional suku Batak di ...", "Sumatera Utara", ["Sumatera Barat", "Aceh", "Jambi"]),
        ("Rumah adat Krong Bade berbentuk panggung kayu berukir tangga di depan berasal dari provinsi ...", "Aceh", ["Sumatera Utara", "Riau", "Sumatera Barat"]),
        ("Rumah adat Sasak beratap jerami dan lantai campuran tanah liat berasal dari pulau ...", "Lombok (NTB)", ["Bali", "Flores", "Sumbawa"]),
        ("Rumah adat Musalaki beratap tinggi khas tempat tinggal kepala suku berasal dari suku Ende di pulau ...", "Flores (NTT)", ["Sumba", "Timor", "Rote"]),
        ("Rumah adat Panjang (Lamin / Radakng) panggung yang sangat panjang dihuni puluhan keluarga Dayak di ...", "Kalimantan", ["Sumatra", "Sulawesi", "Papua"]),
        ("Rumah adat Baileo yang berfungsi sebagai tempat musyawarah adat dan upacara berasal dari provinsi ...", "Maluku", ["Papua", "Sulawesi Utara", "NTT"]),
        ("Rumah adat Souw Raja (Banua Oge) merupakan rumah peninggalan raja di Kota Palu provinsi ...", "Sulawesi Tengah", ["Sulawesi Selatan", "Sulawesi Barat", "Gorontalo"]),
        ("Rumah adat Dulohupa berbentuk panggung dengan atap pelana khas berasal dari provinsi ...", "Gorontalo", ["Sulawesi Utara", "Sulawesi Tengah", "Maluku Utara"]),
        ("Rumah adat Walewangko beratap tinggi dengan dua tangga di serambi berasal dari suku Minahasa di ...", "Sulawesi Utara", ["Gorontalo", "Sulawesi Tengah", "Maluku"]),
        ("Rumah adat Boyang berbentuk panggung dengan ornamen ukiran khas Mandar berasal dari provinsi ...", "Sulawesi Barat", ["Sulawesi Selatan", "Sulawesi Tenggara", "Sulawesi Tengah"]),
        ("Rumah adat Banua Tada bertingkat tanpa menggunakan paku besi berasal dari Kesultanan Buton di provinsi ...", "Sulawesi Tenggara", ["Sulawesi Selatan", "Sulawesi Tengah", "Maluku"]),
        ("Rumah adat Bumbungan Lima dengan ornamen ukiran flora khas Melayu berasal dari provinsi ...", "Bengkulu", ["Sumatera Selatan", "Jambi", "Lampung"]),
        ("Rumah adat Nuwo Sesat panggung besar tempat musyawarah adat tetua marga berasal dari provinsi ...", "Lampung", ["Sumatera Selatan", "Bengkulu", "Banten"]),
        ("Rumah adat Limas dengan lantai bertingkat-tingkat (kekijing) berasal dari kota Palembang di provinsi ...", "Sumatera Selatan", ["Jambi", "Bengkulu", "Lampung"]),
        ("Rumah adat Kajang Lako berbentuk panggung persegi panjang khas Melayu berasal dari provinsi ...", "Jambi", ["Riau", "Sumatera Selatan", "Bengkulu"]),
        ("Rumah adat Selaso Jatuh Kembar dengan balai pertemuan adat khas Melayu berasal dari provinsi ...", "Riau", ["Kepulauan Riau", "Sumatera Barat", "Jambi"]),
        ("Rumah adat Belah Bubung atau Rabung merupakan rumah panggung Melayu pesisir di provinsi ...", "Kepulauan Riau", ["Bangka Belitung", "Riau", "Sumatera Barat"]),
        ("Rumah adat Rakit berbentuk rumah panggung terapung di atas permukaan sungai berasal dari ...", "Bangka Belitung dan Sumsel", ["Kalimantan Barat", "Jambi", "Riau"]),
        ("Rumah adat Badui (Sulah Nyanda) berdinding anyaman bambu tanpa paku besi berasal dari provinsi ...", "Banten", ["Jawa Barat", "Jawa Tengah", "DKI Jakarta"]),
        ("Rumah adat Kebaya dengan teras depan sangat luas dan beratap lipat kebaya berasal dari suku Betawi di ...", "DKI Jakarta", ["Banten", "Jawa Barat", "Jawa Tengah"]),
        ("Rumah adat Kasepuhan peninggalan keraton bersejarah berada di kota Cirebon provinsi ...", "Jawa Barat", ["Jawa Tengah", "Banten", "DKI Jakarta"]),
        ("Rumah adat Tambi berbentuk kerucut prisma yang lantainya berfungsi sekaligus atap dari suku Lore di ...", "Sulawesi Tengah", ["Sulawesi Selatan", "Sulawesi Tenggara", "Gorontalo"]),
        ("Rumah adat Bubungan Tinggi yang megah merupakan istana kesultanan suku Banjar di provinsi ...", "Kalimantan Selatan", ["Kalimantan Timur", "Kalimantan Tengah", "Kalimantan Barat"]),
        ("Rumah adat Betang merupakan rumah panggung kayu ulin raksasa dihuni puluhan keluarga di ...", "Kalimantan Tengah", ["Kalimantan Selatan", "Kalimantan Timur", "Kalimantan Utara"]),
        ("Rumah adat Baloy dengan empat ruang utama adat suku Tidung berasal dari provinsi ...", "Kalimantan Utara", ["Kalimantan Timur", "Kalimantan Selatan", "Kalimantan Barat"]),
    ]
    for q_text, corr, dists in rumah_adat:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan kekayaan rumah adat tradisional Indonesia."))

    # 2. Senjata Tradisional & Alat Musik Nusantara (50 soal)
    weapons_and_instruments = [
        ("Senjata pusaka berbilah keluk (luk) khas masyarakat Jawa yang diakui UNESCO adalah ...", "Keris", ["Rencong", "Kujang", "Mandau"]),
        ("Senjata tradisional berbentuk belati melengkung dengan gagang menyerupai huruf L khas Aceh adalah ...", "Rencong", ["Keris", "Badik", "Kujang"]),
        ("Senjata tradisional sejenis pedang berukir bulu burung khas suku Dayak di Kalimantan adalah ...", "Mandau", ["Rencong", "Keris", "Clurit"]),
        ("Senjata tradisional berbentuk sabit melengkung tajam khas masyarakat Madura adalah ...", "Celurit (Clurit)", ["Golok", "Kujang", "Rencong"]),
        ("Senjata tradisional khas suku Sunda Jawa Barat yang berbentuk melengkung dengan lubang kecil adalah ...", "Kujang", ["Keris", "Rencong", "Badik"]),
        ("Senjata tikam berbilah tunggal khas masyarakat suku Bugis dan Makassar di Sulawesi Selatan adalah ...", "Badik", ["Mandau", "Kujang", "Rencong"]),
        ("Senjata tradisional suku Betawi Jakarta yang sering diselipkan di pinggang pendekar adalah ...", "Golok Betawi", ["Keris", "Rencong", "Mandau"]),
        ("Senjata tradisional khas masyarakat Papua yang digunakan untuk berburu adalah ...", "Busur dan panah", ["Kujang", "Keris", "Celurit"]),
        ("Senjata tradisional khas suku Banjar di Kalimantan Selatan yang menyerupai belati ramping adalah ...", "Sungga / Beladau", ["Kujang", "Keris", "Celurit"]),
        ("Senjata tombak kayu bermata besi khas suku Batak Sumatera Utara disebut ...", "Hujur Siringis", ["Rencong", "Mandau", "Kujang"]),
        ("Alat musik tradisional berbahan bambu yang dimainkan dengan cara digoyangkan berasal dari Jawa Barat adalah ...", "Angklung", ["Saluang", "Sasando", "Kolintang"]),
        ("Alat musik petik tradisional yang wadah resonansinya terbuat dari anyaman daun lontar berasal dari Pulau Rote (NTT) adalah ...", "Sasando", ["Kecapi", "Gitar", "Sape"]),
        ("Alat musik pukul bilah kayu berjejer khas suku Minahasa di Sulawesi Utara adalah ...", "Kolintang", ["Gamelan", "Calung", "Talempong"]),
        ("Alat musik tabung kulit khas masyarakat Maluku dan Papua yang dimainkan dengan cara dipukul adalah ...", "Tifa", ["Kendang", "Rebana", "Gong"]),
        ("Ansambel musik tradisional yang terdiri dari gong, kendang, saron, dan bonang di Jawa dan Bali disebut ...", "Gamelan", ["Tanjidor", "Kolintang", "Gambus"]),
        ("Alat musik tiup tradisional sejenis seruling bambu dengan empat lubang nada khas Minangkabau adalah ...", "Saluang", ["Angklung", "Sasando", "Tifa"]),
        ("Alat musik pukul mirip gong kecil berbahan kuningan yang dimainkan berirama khas Minangkabau adalah ...", "Talempong", ["Kolintang", "Angklung", "Calung"]),
        ("Alat musik petik khas suku Dayak di Kalimantan yang berbentuk perahu dan berukir indah adalah ...", "Sape (Sampe)", ["Sasando", "Kecapi", "Gitar"]),
        ("Alat musik petik berdawai banyak yang biasa mengiringi tembang Sunda dan suling di Jawa Barat adalah ...", "Kecapi", ["Sape", "Gitar", "Rebab"]),
        ("Alat musik gesek berdawai dua yang sering hadir dalam pergelaran gamelan Jawa adalah ...", "Rebab", ["Biola", "Kecapi", "Siter"]),
        ("Alat musik tiup terompet kuningan berukuran besar pengiring orkes kesenian khas Betawi adalah ...", "Tanjidor", ["Gamelan", "Angklung", "Sasando"]),
        ("Alat musik pukul membran kulit satu sisi pengiring kasidah dan musik Melayu/Islam adalah ...", "Rebana", ["Tifa", "Kendang", "Drum"]),
        ("Alat musik bambu di Jawa Barat yang mirip angklung namun dimainkan dengan cara dipukul bilahnya adalah ...", "Calung", ["Angklung", "Kolintang", "Talempong"]),
        ("Alat musik tiup bambu dengan lubang jari pengatur nada yang ditiup dari ujung atas adalah ...", "Suling bambu", ["Terompet", "Sasando", "Tifa"]),
        ("Alat musik petik khas masyarakat Riau yang bernuansa Timur Tengah adalah ...", "Gambus", ["Kecapi", "Sape", "Sasando"]),
    ]
    for q_text, corr, dists in weapons_and_instruments:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami ragam senjata dan alat musik tradisional Indonesia."))

    # 3. Tarian Tradisional & Kuliner Khas Nusantara (60 soal)
    dance_and_culinary = [
        ("Tarian tradisional dari Aceh yang ditarikan berkelompok duduk berjajar dengan tepukan dada ritmis adalah ...", "Tari Saman", ["Tari Piring", "Tari Kecak", "Tari Jaipong"]),
        ("Tarian khas Bali yang dibawakan puluhan pria duduk melingkar sambil menyerukan suara 'cak-cak-cak' adalah ...", "Tari Kecak", ["Tari Pendet", "Tari Barong", "Tari Saman"]),
        ("Tarian khas Minangkabau di mana penarinya mengayunkan piring kaca di telapak tangan tanpa terjatuh adalah ...", "Tari Piring", ["Tari Payung", "Tari Saman", "Tari Jaipong"]),
        ("Tarian selamat datang yang khas di Pulau Bali di mana penarinya menaburkan bunga adalah ...", "Tari Pendet", ["Tari Kecak", "Tari Legong", "Tari Barong"]),
        ("Tarian dinamis dan lincah dengan iringan kendang khas masyarakat Sunda Jawa Barat adalah ...", "Tari Jaipong", ["Tari Saman", "Tari Piring", "Tari Gambyong"]),
        ("Tarian penyambutan tamu terhormat suku Batak Sumatera Utara dengan iringan gondang adalah ...", "Tari Tor-tor", ["Tari Saman", "Tari Piring", "Tari Kecak"]),
        ("Kesenian tari topeng singa raksasa berhias bulu merak yang diangkat dengan gigi berasal dari kota Ponorogo adalah ...", "Reog Ponorogo", ["Kuda Lumping", "Barongsai", "Ondel-ondel"]),
        ("Tarian pergaulan tradisional Jawa Tengah yang dibawakan penari wanita lemah gemulai menyambut tamu adalah ...", "Tari Gambyong", ["Tari Jaipong", "Tari Saman", "Tari Piring"]),
        ("Tarian perang tradisional suku Dayak di Kalimantan yang membawa perisai dan mandau adalah ...", "Tari Kancet Papatai (Tari Perang)", ["Tari Saman", "Tari Piring", "Tari Kecak"]),
        ("Boneka raksasa khas Betawi yang sering diarak berpasangan laki-laki dan perempuan saat perayaan adalah ...", "Ondel-ondel", ["Wayang Golek", "Reog", "Barong"]),
        ("Tarian pergaulan riang gembira khas Papua di mana penari saling bergandengan tangan adalah ...", "Tari Yospan (Yosim Pancar)", ["Tari Saman", "Tari Kecak", "Tari Piring"]),
        ("Tarian selamat datang yang membawa kotak tepak sirih khas kepulauan Riau dan Melayu adalah ...", "Tari Sekapur Sirih (Tari Persembahan)", ["Tari Saman", "Tari Jaipong", "Tari Kecak"]),
        ("Tarian khas Jawa Timur yang dibawakan oleh penari dengan selendang menyampir di leher dan riasan khas adalah ...", "Tari Remo", ["Tari Jaipong", "Tari Piring", "Tari Pendet"]),
        ("Masakan olahan daging sapi berempah khas Minangkabau yang pernah dinobatkan sebagai makanan terlezat di dunia adalah ...", "Rendang", ["Gudeg", "Rawon", "Soto"]),
        ("Makanan khas Kota Palembang yang terbuat dari olahan daging ikan dan sagu disajikan dengan kuah cuko asam manis adalah ...", "Pempek", ["Siomay", "Batagor", "Tekwan"]),
        ("Makanan khas Yogyakarta yang terbuat dari nangka muda dimasak manis gurih dengan santan dan gula kelapa adalah ...", "Gudeg", ["Rendang", "Rawon", "Soto Kudus"]),
        ("Sup daging sapi berkuah hitam pekat khas Jawa Timur yang dimasak menggunakan buah kluwek adalah ...", "Rawon", ["Soto Betawi", "Coto Makassar", "Gulai"]),
        ("Kue bika berpori harum berwarna kuning keemasan yang menjadi oleh-oleh khas Kota Medan adalah ...", "Bika Ambon", ["Lapis Legit", "Bolu Kukus", "Kue Lumpur"]),
        ("Sup daging dan jeroan berkuah gurih kental berempah khas Kota Makassar yang disajikan bersama ketupat adalah ...", "Coto Makassar", ["Rawon", "Gudeg", "Pempek"]),
        ("Makanan pokok khas masyarakat Maluku dan Papua yang terbuat dari tepung sagu bertekstur kenyal adalah ...", "Papeda", ["Nasi Liwet", "Ketupat", "Ti ti"]),
        ("Soto ayam khas Kalimantan Selatan yang disajikan dengan kuah rempah susu telur dan perkedel singkong adalah ...", "Soto Banjar", ["Soto Lamongan", "Soto Betawi", "Soto Madura"]),
        ("Makanan tradisional khas Betawi berbahan beras ketan, telur bebek, dan serundeng kelapa sangrai adalah ...", "Kerak Telor", ["Nasi Uduk", "Ketoprak", "Karedok"]),
        ("Olahan ayam utuh panggang berbumbu rempah pedas base genep khas Pulau Bali adalah ...", "Ayam Betutu", ["Ayam Taliwang", "Ayam Pop", "Ayam Geprek"]),
        ("Olahan ayam bakar pedas manis khas Pulau Lombok yang terkenal gurih adalah ...", "Ayam Taliwang", ["Ayam Betutu", "Ayam Kalasan", "Ayam Penyet"]),
        ("Kudapan lumpia basah atau goreng berisi rebung dan daging ayam/udang merupakan kuliner khas kota ...", "Semarang", ["Solo", "Yogyakarta", "Bandung"]),
        ("Kudapan tempe tipis berbalut tepung setengah matang yang disajikan dengan cabai rawit khas Banyumas adalah ...", "Tempe Mendoan", ["Tempe Orek", "Tempe Bacem", "Keripik Tempe"]),
        ("Kudapan tahu gurih tanpa isi yang bagian luarnya garing renyah khas Jawa Barat berasal dari kabupaten ...", "Sumedang", ["Garut", "Cianjur", "Ciamis"]),
        ("Dodol legit manis kenyal yang sangat populer sebagai oleh-oleh khas Jawa Barat berasal dari kabupaten ...", "Garut", ["Cianjur", "Tasikmalaya", "Kuningan"]),
        ("Rujak khas Surabaya Jawa Timur yang menggunakan saus petis udang dan sayuran serta cingur (moncong sapi) adalah ...", "Rujak Cingur", ["Rujak Buah", "Rujak Manis", "Rujak Uleg"]),
        ("Nasi khas Solo Jawa Tengah yang disajikan dengan suwiran ayam, telur pindang, dan kuah santan areh adalah ...", "Nasi Liwet Solo", ["Nasi Uduk", "Nasi Kuning", "Nasi Padang"]),
    ]
    for q_text, corr, dists in dance_and_culinary:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Kenali kekayaan tarian tradisional dan kuliner daerah di nusantara."))

    # 4. Hari Besar Nasional & Lambang Negara (50 soal)
    national_symbols_and_days = [
        ("Lambang resmi negara Republik Indonesia adalah ...", "Burung Garuda Pancasila", ["Burung Rajawali", "Harimau Sumatra", "Banteng Jawa"]),
        ("Semboyan resmi negara Indonesia yang dicengkeram oleh kaki burung Garuda adalah ...", "Bhinneka Tunggal Ika", ["Tut Wuri Handayani", "Ing Ngarsa Sung Tuladha", "Sumpah Palapa"]),
        ("Arti dari semboyan nasional 'Bhinneka Tunggal Ika' adalah ...", "Berbeda-beda tetapi tetap satu jua", ["Bersatu kita teguh bercerai kita runtuh", "Maju terus pantang mundur", "Bekerja bersama demi negeri"]),
        ("Semboyan Bhinneka Tunggal Ika pertama kali tertulis dalam kitab kuno Sutasoma karya ...", "Mpu Tantular", ["Mpu Prapanca", "Mpu Gandring", "Mpu Sedah"]),
        ("Lambang simbol dari sila pertama Pancasila (Ketuhanan Yang Maha Esa) adalah ...", "Bintang emas bersudut lima", ["Rantai emas", "Pohon beringin", "Kepala banteng"]),
        ("Lambang simbol dari sila kedua Pancasila (Kemanusiaan yang Adil dan Beradab) adalah ...", "Rantai emas bulat dan persegi", ["Bintang", "Pohon beringin", "Padi dan kapas"]),
        ("Lambang simbol dari sila ketiga Pancasila (Persatuan Indonesia) adalah ...", "Pohon beringin", ["Kepala banteng", "Bintang", "Rantai"]),
        ("Lambang simbol dari sila keempat Pancasila (Kerakyatan yang Dipimpin oleh Hikmat Kebijaksanaan...) adalah ...", "Kepala banteng", ["Pohon beringin", "Padi dan kapas", "Rantai"]),
        ("Lambang simbol dari sila kelima Pancasila (Keadilan Sosial bagi Seluruh Rakyat Indonesia) adalah ...", "Padi dan kapas", ["Kepala banteng", "Bintang emas", "Pohon beringin"]),
        ("Bunga melati putih (Jasminum sambac) ditetapkan sebagai puspa nasional bergelar Puspa ...", "Puspa Bangsa", ["Puspa Pesona", "Puspa Langka", "Puspa Indah"]),
        ("Bunga anggrek bulan (Phalaenopsis amabilis) bergelar sebagai Puspa ...", "Puspa Pesona", ["Puspa Bangsa", "Puspa Langka", "Puspa Rimba"]),
        ("Bunga Padma Raksasa (Rafflesia arnoldii) bergelar sebagai Puspa ...", "Puspa Langka", ["Puspa Bangsa", "Puspa Pesona", "Puspa Alam"]),
        ("Lagu kebangsaan resmi negara Republik Indonesia adalah ...", "Indonesia Raya", ["Bagimu Negeri", "Garuda Pancasila", "Hari Merdeka"]),
        ("Lagu kebangsaan Indonesia Raya diciptakan oleh komponis nasional bernama ...", "Wage Rudolf Supratman (W.R. Supratman)", ["Ismail Marzuki", "Ibu Sud", "Kusbini"]),
        ("Bendera kebangsaan Indonesia dinamakan Sang Merah Putih di mana warna merah melambangkan keberanian dan putih melambangkan ...", "Kesucian", ["Kemakmuran", "Kesuburan", "Ketenteraman"]),
        ("Hari Kemerdekaan Republik Indonesia diperingati setiap tanggal ...", "17 Agustus", ["10 November", "28 Oktober", "1 Juni"]),
        ("Hari Pahlawan Nasional diperingati setiap tahun pada tanggal ...", "10 November", ["17 Agustus", "20 Mei", "21 April"]),
        ("Hari Sumpah Pemuda diperingati setiap tahun pada tanggal ...", "28 Oktober", ["20 Mei", "1 Juni", "10 November"]),
        ("Hari Kebangkitan Nasional diperingati setiap tahun pada tanggal ...", "20 Mei", ["21 April", "2 Mei", "17 Agustus"]),
        ("Hari Pendidikan Nasional diperingati setiap tahun pada tanggal ...", "2 Mei", ["21 April", "20 Mei", "25 November"]),
        ("Hari Lahir Pancasila diperingati setiap tahun pada tanggal ...", "1 Juni", ["1 Oktober", "17 Agustus", "28 Oktober"]),
        ("Hari Kesaktian Pancasila diperingati setiap tahun pada tanggal ...", "1 Oktober", ["1 Juni", "10 November", "20 Mei"]),
        ("Hari Kartini diperingati setiap tahun pada tanggal ...", "21 April", ["2 Mei", "22 Desember", "1 Juni"]),
        ("Hari Ibu Nasional di Indonesia diperingati setiap tahun pada tanggal ...", "22 Desember", ["21 April", "25 November", "10 November"]),
        ("Hari Guru Nasional diperingati setiap tahun pada tanggal ...", "25 November", ["2 Mei", "20 Mei", "17 Agustus"]),
        ("Hari Pramuka di Indonesia diperingati setiap tahun pada tanggal ...", "14 Agustus", ["17 Agustus", "28 Oktober", "20 Mei"]),
        ("Hari Batik Nasional diperingati setiap tahun pada tanggal ...", "2 Oktober", ["1 Oktober", "17 Agustus", "10 November"]),
        ("Hari Tentara Nasional Indonesia (TNI) diperingati setiap tahun pada tanggal ...", "5 Oktober", ["10 November", "17 Agustus", "1 Juli"]),
        ("Hari Bhayangkara (Kepolisian Republik Indonesia / POLRI) diperingati pada tanggal ...", "1 Juli", ["5 Oktober", "10 November", "17 Agustus"]),
        ("Hari Anak Nasional di Indonesia diperingati setiap tanggal ...", "23 Juli", ["2 Mei", "1 Juni", "21 April"]),
    ]
    for q_text, corr, dists in national_symbols_and_days:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami hari besar nasional dan lambang negara Indonesia."))

    # 5. Olahraga & Permainan Dunia (60 soal)
    sports_facts = [
        ("Berapa jumlah pemain dalam satu regu tim sepak bola di lapangan?", "11 pemain", ["9 pemain", "10 pemain", "12 pemain"]),
        ("Lama waktu normal pertandingan sepak bola standar adalah 2 babak dengan durasi masing-masing ...", "45 menit", ["40 menit", "50 menit", "30 menit"]),
        ("Organisasi induk olahraga sepak bola tertinggi di dunia adalah ...", "FIFA", ["FIBA", "BWF", "FIVB"]),
        ("Induk organisasi resmi sepak bola di seluruh wilayah Indonesia adalah ...", "PSSI", ["PBSI", "PERBASI", "PBVSI"]),
        ("Berapa jumlah pemain dalam satu tim bola basket di dalam lapangan?", "5 pemain", ["6 pemain", "7 pemain", "4 pemain"]),
        ("Induk organisasi bola basket tertinggi di dunia adalah ...", "FIBA", ["FIFA", "BWF", "FIVB"]),
        ("Induk organisasi olahraga bola basket di Indonesia adalah ...", "PERBASI", ["PSSI", "PBVSI", "PBSI"]),
        ("Berapa jumlah pemain dalam satu tim bola voli di lapangan?", "6 pemain", ["5 pemain", "7 pemain", "11 pemain"]),
        ("Induk organisasi olahraga bola voli di Indonesia adalah ...", "PBVSI", ["PERBASI", "PSSI", "PBSI"]),
        ("Induk organisasi olahraga bulu tangkis di Indonesia adalah ...", "PBSI", ["PSSI", "PERBASI", "PBVSI"]),
        ("Induk organisasi olahraga bulu tangkis tertinggi di dunia adalah ...", "BWF", ["FIFA", "FIBA", "FIVB"]),
        ("Bola khusus yang digunakan dalam pertandingan bulu tangkis terbuat dari bulu unggas disebut ...", "Shuttlecock (Kok)", ["Bola kasti", "Bola bekel", "Puck"]),
        ("Kejuaraan beregu bulu tangkis bergengsi dunia khusus untuk pemain putra adalah ...", "Thomas Cup (Piala Thomas)", ["Uber Cup", "Sudirman Cup", "Davis Cup"]),
        ("Kejuaraan beregu bulu tangkis bergengsi dunia khusus untuk pemain putri adalah ...", "Uber Cup (Piala Uber)", ["Thomas Cup", "Sudirman Cup", "Fed Cup"]),
        ("Kejuaraan bulu tangkis beregu campuran dunia yang dinamai dari tokoh bulu tangkis Indonesia adalah ...", "Sudirman Cup (Piala Sudirman)", ["Thomas Cup", "Uber Cup", "All England"]),
        ("Turnamen bulu tangkis tertua dan paling prestisius di dunia yang diselenggarakan di Inggris adalah ...", "All England", ["Indonesia Open", "Malaysia Open", "Olimpiade"]),
        ("Berapa jumlah cincin berwarna-warni yang menjadi lambang resmi Olimpiade dunia?", "5 cincin melambangkan 5 benua", ["3 cincin", "4 cincin", "6 cincin"]),
        ("Pesta olahraga multicabang terbesar di dunia (Olimpiade Musim Panas) diadakan sekali setiap ...", "4 tahun sekali", ["2 tahun sekali", "3 tahun sekali", "5 tahun sekali"]),
        ("Pesta olahraga multicabang antarnegara-negara di kawasan Asia Tenggara adalah ...", "SEA Games", ["Asian Games", "Olimpiade", "Commonwealth Games"]),
        ("Pesta olahraga multicabang terbesar antarseluruh negara di Benua Asia adalah ...", "Asian Games", ["SEA Games", "Olimpiade", "Piala Asia"]),
        ("Pekan Olahraga Nasional (PON) antarprovinsi di Indonesia diselenggarakan setiap ...", "4 tahun sekali", ["2 tahun sekali", "1 tahun sekali", "5 tahun sekali"]),
        ("Seni bela diri tradisional warisan leluhur bangsa Indonesia yang diakui dunia adalah ...", "Pencak Silat", ["Karate", "Taekwondo", "Judo"]),
        ("Induk organisasi olahraga pencak silat di seluruh Indonesia adalah ...", "IPSI", ["PSSI", "KONI", "FORKI"]),
        ("Seni bela diri tradisional yang berasal dari negara Jepang yang mengandalkan pukulan dan tendangan adalah ...", "Karate", ["Taekwondo", "Silat", "Kungfu"]),
        ("Seni bela diri tradisional dari Korea yang terkenal dengan jurus tendangan kakinya yang tinggi adalah ...", "Taekwondo", ["Karate", "Judo", "Muay Thai"]),
        ("Seni bela diri tinju tradisional bertarung menggunakan tangan, siku, dan lutut dari Thailand adalah ...", "Muay Thai", ["Taekwondo", "Karate", "Wushu"]),
        ("Seni bela diri pedang bambu tradisional dari Jepang disebut ...", "Kendo", ["Karate", "Judo", "Aikido"]),
        ("Seni bela diri asal Jepang yang berfokus pada teknik bantingan dan kuncian di lantai tanpa pukulan adalah ...", "Judo", ["Karate", "Taekwondo", "Muay Thai"]),
        ("Gaya renang yang gerakannya meniru gerakan kaki dan tangan katak saat berenang disebut ...", "Gaya dada (Katak)", ["Gaya bebas (Crawl)", "Gaya punggung", "Gaya kupu-kupu"]),
        ("Gaya renang tercepat dengan kayuhan tangan bergantian ke depan dan kibasan kaki adalah ...", "Gaya bebas (Crawl)", ["Gaya dada", "Gaya punggung", "Gaya kupu-kupu"]),
        ("Satu-satunya gaya renang di mana perenang menghadap ke atas langit dan tidak melihat dinding finis adalah ...", "Gaya punggung", ["Gaya bebas", "Gaya dada", "Gaya kupu-kupu"]),
        ("Gaya renang yang membutuhkan kekuatan otot bahu terbesar dengan kedua tangan mengayuh serempak menyerupai sayap adalah ...", "Gaya kupu-kupu", ["Gaya dada", "Gaya bebas", "Gaya punggung"]),
        ("Kondisi dalam permainan catur saat raja lawan diserang dan tidak memiliki langkah legal untuk kabur disebut ...", "Skakmat (Checkmate)", ["Remis", "Pion promosi", "Rokade"]),
        ("Langkah khusus dalam catur di mana raja dan benteng bertukar posisi pelindung secara bersamaan disebut ...", "Rokade (Castling)", ["En passant", "Skakmat", "Promosi"]),
        ("Bidang papan permainan catur standar terdiri dari berapa kotak hitam dan putih?", "64 kotak (8 × 8)", ["100 kotak", "32 kotak", "81 kotak"]),
        ("Olahraga balap mobil paling bergengsi di dunia dengan mobil roda terbuka (open-wheel) berkecepatan tinggi adalah ...", "Formula 1 (F1)", ["MotoGP", "NASCAR", "Rally"]),
        ("Ajang balap motor prototipe tercepat dan paling bergengsi di dunia adalah ...", "MotoGP", ["Formula 1", "Superbike", "Motocross"]),
        ("Jarak lari maraton penuh resmi standar internasional adalah ...", "42,195 kilometer", ["21 kilometer", "10 kilometer", "50 kilometer"]),
        ("Perlombaan lari cepat jarak pendek di lintasan atletik sering disebut lari ...", "Sprint", ["Maraton", "Estafet", "Jalan cepat"]),
        ("Lomba lari beregu di mana para pelari menyerahkan tongkat estafet kepada pelari berikutnya disebut lari ...", "Estafet (Sambung)", ["Sprint", "Maraton", "Gawang"]),
    ]
    for q_text, corr, dists in sports_facts:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan fakta dan istilah dalam dunia olahraga."))

    # 6. Tokoh Penemu Terkenal Dunia (40 soal)
    inventors = [
        ("Siapakah ilmuwan penemu bola lampu pijar praktis dan fonograf rekaman suara?", "Thomas Alva Edison", ["Alexander Graham Bell", "Nikola Tesla", "Albert Einstein"]),
        ("Siapakah tokoh yang dikenal sebagai penemu alat komunikasi pesawat telepon?", "Alexander Graham Bell", ["Thomas Edison", "Guglielmo Marconi", "Samuel Morse"]),
        ("Dua bersaudara yang berhasil menciptakan dan menerbangkan pesawat terbang bermesin pertama kali adalah ...", "Wright bersaudara (Orville & Wilbur Wright)", ["Montgolfier bersaudara", "Lumiere bersaudara", "Grimm bersaudara"]),
        ("Siapakah penemu konsep gaya gravitasi bumi saat melihat buah apel jatuh dari pohon?", "Isaac Newton", ["Galileo Galilei", "Albert Einstein", "Johannes Kepler"]),
        ("Siapakah fisikawan jenius penemu rumus teori relativitas E = mc²?", "Albert Einstein", ["Isaac Newton", "Niels Bohr", "Stephen Hawking"]),
        ("Siapakah penemu teknologi radio nirkabel gelombang elektromagnetik?", "Guglielmo Marconi", ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla"]),
        ("Siapakah tokoh insinyur Skotlandia yang berhasil mendemonstrasikan televisi elektronik pertama kali?", "John Logie Baird", ["Thomas Edison", "Nikola Tesla", "Steve Jobs"]),
        ("Siapakah tokoh yang dijuluki Bapak Komputer Dunia penemu mesin analitis mekanik?", "Charles Babbage", ["Alan Turing", "Bill Gates", "Steve Wozniak"]),
        ("Siapakah ilmuwan Inggris yang menemukan jaring komunikasi internet World Wide Web (WWW)?", "Tim Berners-Lee", ["Bill Gates", "Steve Jobs", "Mark Zuckerberg"]),
        ("Siapakah ilmuwan penemu kode sandi titik dan garis (kode telegraf) yang dinamai sesuai namanya?", "Samuel Morse", ["Thomas Edison", "Alexander Graham Bell", "Marconi"]),
        ("Siapakah ilmuwan penemu obat antibiotik pertama (penisilin) yang menyelamatkan jutaan nyawa?", "Alexander Fleming", ["Louis Pasteur", "Edward Jenner", "Robert Koch"]),
        ("Siapakah ilmuwan Prancis yang menemukan proses pembasmian kuman pada susu (pasteurisasi) dan vaksin rabies?", "Louis Pasteur", ["Alexander Fleming", "Edward Jenner", "Marie Curie"]),
        ("Siapakah dokter penemu vaksin cacar pertama di dunia yang mempelopori konsep imunisasi?", "Edward Jenner", ["Louis Pasteur", "Alexander Fleming", "Jonas Salk"]),
        ("Siapakah penemu sistem pengelompokan golongan darah manusia (sistem ABO)?", "Karl Landsteiner", ["Gregor Mendel", "Louis Pasteur", "Robert Hooke"]),
        ("Siapakah ilmuwan wanita peraih dua Nobel penemu unsur radioaktif polonium dan radium?", "Marie Curie", ["Rosalind Franklin", "Ada Lovelace", "Jane Goodall"]),
        ("Siapakah astronom Italia yang menyempurnakan teropong teleskop dan menemukan empat bulan planet Jupiter?", "Galileo Galilei", ["Nicolaus Copernicus", "Johannes Kepler", "Edwin Hubble"]),
        ("Siapakah tokoh penemu mesin cetak huruf bergerak pertama yang merevolusi penyebaran buku di Eropa?", "Johannes Gutenberg", ["Leonardo da Vinci", "Isaac Newton", "Galileo"]),
        ("Siapakah tokoh seniman jenius dari Italia pelukis mahakarya Mona Lisa dan Perjamuan Terakhir?", "Leonardo da Vinci", ["Michelangelo", "Vincent van Gogh", "Pablo Picasso"]),
        ("Siapakah presiden ke-3 Republik Indonesia yang dikenal sebagai teknokrat jenius perancang pesawat N-250 Gatotkaca?", "B.J. Habibie", ["Soekarno", "Soeharto", "Abdurrahman Wahid"]),
        ("Siapakah tokoh pencetus arus listrik bolak-balik (AC) dan motor induksi modern?", "Nikola Tesla", ["Thomas Edison", "Michael Faraday", "James Watt"]),
        ("Siapakah ilmuwan penemu dinamo dan hukum induksi elektromagnetik yang dijuluki Bapak Kelistrikan?", "Michael Faraday", ["James Watt", "Nikola Tesla", "Thomas Edison"]),
        ("Siapakah tokoh penyempurna mesin uap yang mengawali era Revolusi Industri dan namanya diabadikan sebagai satuan daya listrik?", "James Watt", ["James Prescott Joule", "Michael Faraday", "Isaac Newton"]),
        ("Siapakah tokoh pendiri perusahaan perangkat lunak Microsoft?", "Bill Gates", ["Steve Jobs", "Jeff Bezos", "Elon Musk"]),
        ("Siapakah tokoh pendiri perusahaan teknologi Apple yang mempopulerkan iPhone dan iPad?", "Steve Jobs", ["Bill Gates", "Larry Page", "Mark Zuckerberg"]),
        ("Siapakah tokoh pendiri media sosial Facebook (Meta)?", "Mark Zuckerberg", ["Steve Jobs", "Bill Gates", "Jack Dorsey"]),
    ]
    for q_text, corr, dists in inventors:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan tokoh-tokoh penemu dan ilmuwan besar dunia."))

    # 7. Mata Uang Negara di Dunia (35 soal)
    currencies = [
        ("Mata uang resmi yang digunakan di negara Malaysia adalah ...", "Ringgit", ["Rupiah", "Dolar", "Baht"]),
        ("Mata uang resmi yang digunakan di negara Singapura adalah ...", "Dolar Singapura", ["Ringgit", "Baht", "Rupiah"]),
        ("Mata uang resmi yang digunakan di negara Thailand adalah ...", "Baht", ["Ringgit", "Dong", "Peso"]),
        ("Mata uang resmi yang digunakan di negara Filipina adalah ...", "Peso", ["Ringgit", "Baht", "Dolar"]),
        ("Mata uang resmi yang digunakan di negara Vietnam adalah ...", "Dong", ["Kip", "Riel", "Baht"]),
        ("Mata uang resmi yang digunakan di negara Kamboja adalah ...", "Riel", ["Dong", "Kip", "Baht"]),
        ("Mata uang resmi yang digunakan di negara Laos adalah ...", "Kip", ["Riel", "Dong", "Baht"]),
        ("Mata uang resmi yang digunakan di negara Myanmar adalah ...", "Kyat", ["Baht", "Rupee", "Riel"]),
        ("Mata uang resmi yang digunakan di negara Brunei Darussalam adalah ...", "Dolar Brunei", ["Ringgit", "Rupiah", "Dinar"]),
        ("Mata uang resmi yang digunakan di negara Jepang adalah ...", "Yen", ["Won", "Yuan", "Dolar"]),
        ("Mata uang resmi yang digunakan di negara Korea Selatan adalah ...", "Won", ["Yen", "Yuan", "Ringgit"]),
        ("Mata uang resmi yang digunakan di negara Tiongkok (China) adalah ...", "Yuan (Renminbi)", ["Yen", "Won", "Hong Kong Dolar"]),
        ("Mata uang resmi yang digunakan di negara India adalah ...", "Rupee", ["Rupiah", "Taka", "Kyat"]),
        ("Mata uang resmi yang digunakan di negara Arab Saudi adalah ...", "Riyal", ["Dinar", "Dirham", "Rupiah"]),
        ("Mata uang resmi yang digunakan di negara Uni Emirat Arab (Dubai) adalah ...", "Dirham", ["Riyal", "Dinar", "Dolar"]),
        ("Mata uang resmi yang digunakan di negara Kuwait adalah ...", "Dinar Kuwait", ["Riyal", "Dirham", "Dolar"]),
        ("Mata uang resmi yang digunakan di negara Turki adalah ...", "Lira", ["Euro", "Riyal", "Dinar"]),
        ("Mata uang resmi yang digunakan di negara Amerika Serikat adalah ...", "Dolar AS (US Dollar)", ["Poundsterling", "Euro", "Yen"]),
        ("Mata uang resmi yang digunakan di negara Inggris (Britania Raya) adalah ...", "Poundsterling", ["Euro", "Dolar", "Franc"]),
        ("Mata uang tunggal yang digunakan bersama oleh sebagian besar negara Uni Eropa adalah ...", "Euro", ["Poundsterling", "Franc", "Krona"]),
        ("Mata uang resmi yang digunakan di negara Rusia adalah ...", "Rubel", ["Euro", "Lira", "Dinar"]),
        ("Mata uang resmi yang digunakan di negara Swiss adalah ...", "Franc Swiss", ["Euro", "Mark", "Krona"]),
        ("Mata uang resmi yang digunakan di negara Australia adalah ...", "Dolar Australia", ["Dolar AS", "Pound", "Euro"]),
        ("Mata uang resmi yang digunakan di negara Brasil adalah ...", "Real Brasil", ["Peso", "Dolar", "Bolivar"]),
        ("Mata uang resmi yang digunakan di negara Afrika Selatan adalah ...", "Rand", ["Dinar", "Pound", "Shilling"]),
    ]
    for q_text, corr, dists in currencies:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan mata uang negara di dunia."))

    # 8. Kalender, Waktu & Satuan Waktu (25 soal)
    time_and_calendar = [
        ("Satu dasawarsa (dekade) sama dengan berapa tahun?", "10 tahun", ["5 tahun", "8 tahun", "100 tahun"]),
        ("Satu windu sama dengan berapa tahun?", "8 tahun", ["5 tahun", "10 tahun", "12 tahun"]),
        ("Satu lustrum sama dengan berapa tahun?", "5 tahun", ["8 tahun", "10 tahun", "25 tahun"]),
        ("Satu abad sama dengan berapa tahun?", "100 tahun", ["50 tahun", "500 tahun", "1.000 tahun"]),
        ("Satu milenium sama dengan berapa tahun?", "1.000 tahun", ["100 tahun", "500 tahun", "10.000 tahun"]),
        ("Berapa jumlah hari dalam bulan Januari?", "31 hari", ["30 hari", "28 hari", "29 hari"]),
        ("Berapa jumlah hari dalam bulan April?", "30 hari", ["31 hari", "29 hari", "28 hari"]),
        ("Berapa jumlah hari dalam bulan Juni?", "30 hari", ["31 hari", "28 hari", "29 hari"]),
        ("Berapa jumlah hari dalam bulan Agustus?", "31 hari", ["30 hari", "29 hari", "28 hari"]),
        ("Berapa jumlah hari dalam bulan Desember?", "31 hari", ["30 hari", "28 hari", "29 hari"]),
        ("Tahun kabisat terjadi setiap berapa tahun sekali?", "4 tahun sekali", ["2 tahun sekali", "5 tahun sekali", "10 tahun sekali"]),
        ("Pada tahun kabisat, bulan Februari memiliki berapa hari?", "29 hari", ["28 hari", "30 hari", "31 hari"]),
        ("Tahun kabisat adalah tahun yang habis dibagi dengan angka ...", "4", ["3", "5", "7"]),
        ("Satu caturwulan sama dengan berapa bulan?", "4 bulan", ["3 bulan", "6 bulan", "2 bulan"]),
        ("Satu semester sama dengan berapa bulan?", "6 bulan", ["3 bulan", "4 bulan", "12 bulan"]),
        ("Satu triwulan sama dengan berapa bulan?", "3 bulan", ["4 bulan", "6 bulan", "2 bulan"]),
    ]
    for q_text, corr, dists in time_and_calendar:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Hitung konversi waktu kalender."))

    # 9. Pengetahuan Umum Populer Sehari-hari (untuk mencapai 500 soal)
    daily_facts = [
        ("Cairan antiseptik yang biasa digunakan untuk membersihkan luka lecet dari kuman adalah ...", "Betadine (Povidon Iodin)", ["Minyak goreng", "Cuka makan", "Kecap manis"]),
        ("Alat untuk memeriksa detak jantung dan suara napas dada yang dikalungkan dokter di leher adalah ...", "Stetoskop", ["Termometer", "Tensimeter", "Mikroskop"]),
        ("Alat untuk mengukur tekanan darah seseorang disebut ...", "Tensimeter (Sfigmomanometer)", ["Stetoskop", "Termometer", "Timbangan"]),
        ("Kendaraan darurat yang dilengkapi sirine khusus untuk membawa pasien gawat ke rumah sakit adalah ...", "Mobil Ambulans", ["Mobil Pemadam", "Mobil Derek", "Mobil Patroli"]),
        ("Kendaraan darurat berwarna merah bersirine yang bertugas memadamkan kebakaran adalah ...", "Mobil Pemadam Kebakaran (Damkar)", ["Ambulans", "Truk Tangki", "Mobil Polisi"]),
        ("Nomor panggilan darurat kepolisian di Indonesia yang dapat dihubungi bebas pulsa adalah ...", "110", ["112", "113", "118"]),
        ("Nomor panggilan darurat pemadam kebakaran di Indonesia adalah ...", "113", ["110", "118", "119"]),
        ("Nomor panggilan darurat ambulans medis gawat darurat di Indonesia adalah ...", "118 atau 119", ["110", "113", "112"]),
        ("Warna lampu lalu lintas yang menandakan kendaraan wajib berhenti di belakang garis marka adalah ...", "Warna Merah", ["Warna Kuning", "Warna Hijau", "Warna Biru"]),
        ("Warna lampu lalu lintas yang menandakan kendaraan bersiap-siap dan berhati-hati adalah ...", "Warna Kuning", ["Warna Merah", "Warna Hijau", "Warna Putih"]),
        ("Warna lampu lalu lintas yang menandakan kendaraan diperbolehkan berjalan melaju adalah ...", "Warna Hijau", ["Warna Merah", "Warna Kuning", "Warna Ungu"]),
        ("Zebra cross di jalan raya berfungsi khusus sebagai tempat penyeberangan bagi ...", "Pejalan kaki", ["Sepeda motor", "Mobil sedan", "Truk muatan"]),
        ("Jalur khusus di pinggir jalan raya yang diperuntukkan bagi pejalan kaki disebut ...", "Trotoar", ["Bahu jalan", "Zebra cross", "Marka jalan"]),
        ("Helm pengaman pengendara sepeda motor berstandar resmi di Indonesia wajib memiliki label ...", "SNI (Standar Nasional Indonesia)", ["MUI", "BPOM", "ISO"]),
        ("Lembaga pemerintah yang bertugas mengawasi keamanan peredaran obat dan makanan di Indonesia adalah ...", "BPOM", ["KPK", "KPU", "BPS"]),
        ("Sertifikat resmi yang menyatakan suatu produk makanan halal dikonsumsi di Indonesia dikeluarkan oleh ...", "BPJPH / MUI", ["BPOM", "BPS", "Kemenkes"]),
        ("Bahan bakar minyak (BBM) bersubsidi untuk kendaraan bermotor beroktan 90 di SPBU Pertamina adalah ...", "Pertalite", ["Pertamax", "Solar", "Dexlite"]),
        ("Bahan bakar minyak non-subsidi Pertamina beroktan 92 dengan warna cairan biru adalah ...", "Pertamax", ["Pertalite", "Solar", "Bio Solar"]),
        ("Bahan bakar khusus untuk mesin kendaraan bermesin diesel adalah ...", "Solar / Dexlite", ["Pertalite", "Pertamax", "Bensin murni"]),
        ("Bahan bakar cair khusus untuk mesin pesawat terbang turbin jet adalah ...", "Avtur (Aviation Turbine)", ["Bensin", "Solar", "Oli mesin"]),
        ("Bahan bakar cair khusus untuk pesawat bermesin piston baling-baling adalah ...", "Avgas (Aviation Gasoline)", ["Avtur", "Kerosin", "Minyak tanah"]),
        ("Kereta api rel listrik komuter yang menghubungkan Jakarta, Bogor, Depok, Tangerang, dan Bekasi adalah ...", "KRL Commuter Line", ["MRT", "LRT", "Kereta Cepat"]),
        ("Kereta cepat pertama di Asia Tenggara yang menghubungkan Jakarta dan Bandung bernama ...", "Whoosh", ["Shinkansen", "KRL", "LRT"]),
        ("Singkatan dari transportasi massal bawah tanah dan layang modern di Jakarta MRT adalah ...", "Mass Rapid Transit (Moda Raya Terpadu)", ["Mobil Cepat", "Kereta Cepat", "Jalur Monorel"]),
        ("Tempat parkir dan lepas landas helikopter di atas gedung tinggi disebut ...", "Helipad", ["Landasan pacu", "Hangar", "Apron"]),
        ("Bangunan tinggi di tepi pantai yang memancarkan lampu sorot penuntun kapal laut di malam hari adalah ...", "Mercusuar", ["Menara radar", "Menara ATC", "Dermaga"]),
        ("Jembatan penyeberangan orang di atas jalan raya padat kendaraan disingkat ...", "JPO", ["Jalan Tol", "Flyover", "Underpass"]),
        ("Jalan layang yang dibangun melintasi jalan raya lain di bawahnya disebut ...", "Flyover (Jalan Layang)", ["Underpass", "Terowongan", "JPO"]),
        ("Jalan terowongan yang dibangun di bawah tanah melintasi persimpangan disebut ...", "Underpass", ["Flyover", "JPO", "Jembatan"]),
    ]
    for q_text, corr, dists in daily_facts:
        if len(questions) >= 500:
            break
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan fakta umum dan aturan sehari-hari."))

    # Pad if needed with unique animal trivia to reach 500
    extra_animal_trivia = [
        ("Mamalia yang merupakan satu-satunya mamalia sejati yang bisa terbang di udara adalah ...", "Kelelawar", ["Tupai terbang", "Burung hantu", "Elang"]),
        ("Hewan laut cerdas yang terkenal suka menolong manusia dan menggunakan sonar suara adalah ...", "Lumba-lumba", ["Hiu", "Pari", "Ubur-ubur"]),
        ("Burung yang menjadi lambang kebijaksanaan dan sering digambarkan memakai toga wisuda adalah ...", "Burung Hantu", ["Burung Elang", "Burung Merpati", "Burung Gagak"]),
        ("Burung pembawa pesan surat di zaman kuno yang memiliki navigasi ingatan arah sangat baik adalah ...", "Burung Merpati", ["Burung Pipit", "Burung Rajawali", "Burung Beo"]),
        ("Burung yang pintar menirukan suara ucapan manusia bila dilatih adalah ...", "Burung Beo / Kakatua", ["Burung Elang", "Burung Gereja", "Burung Hantu"]),
        ("Serangga penghasil cairan manis madu yang kaya manfaat kesehatan adalah ...", "Lebah madu", ["Semut", "Lalat", "Kumbang"]),
        ("Serangga yang memproduksi benang kepompong halus bahan kain sutra mewah adalah ...", "Ulat Sutra (Bombyx mori)", ["Ulat daun", "Laba-laba", "Capung"]),
        ("Hewan yang dijuluki sebagai 'Kapal Padang Pasir' karena ketahanannya menjelajah gurun adalah ...", "Unta", ["Kuda", "Keledai", "Gajah"]),
        ("Hewan mamalia berkantung asal Tiongkok yang makanannya hampir 99% berupa bambu adalah ...", "Panda raksasa", ["Koala", "Beruang kutub", "Kukang"]),
        ("Hewan marsupial asal Australia yang suka memeluk pohon kayu putih dan makan daun eukaliptus adalah ...", "Koala", ["Panda", "Kangguru", "Wombat"]),
        ("Hewan yang memiliki kemampuan merayap di dinding kaca dan langit-langit tanpa jatuh adalah ...", "Cecak dan Tokek", ["Katak", "Kadal", "Ular"]),
        ("Hewan amfibi yang kulitnya sering beracun dan dapat melompat jauh adalah ...", "Katak pohon", ["Buaya", "Ikan", "Kura-kura"]),
        ("Reptil purba bertubuh keras yang dapat menarik kepala dan kakinya masuk ke dalam tempurung adalah ...", "Kura-kura / Penyu", ["Buaya", "Komodo", "Bunglon"]),
        ("Hewan karnivora yang dijuluki 'Raja Hutan' dengan rambut lebat di leher singa jantan adalah ...", "Singa", ["Harimau", "Serigala", "Macan tutul"]),
        ("Kucing besar terkuat dan berbadan paling loreng garis hitam oranye di Asia adalah ...", "Harimau", ["Singa", "Citah", "Puma"]),
        ("Hewan mamalia tercepat berlari di daratan mengejar buruannya dengan bintik totol hitam adalah ...", "Citah (Cheetah)", ["Harimau", "Singa", "Kuda"]),
        ("Ikan air laut yang memiliki tentakel dengan racun menyengat dan tubuh transparan kenyal adalah ...", "Ubur-ubur", ["Cumi-cumi", "Gurita", "Bintang laut"]),
        ("Hewan laut berkulit duri berbentuk bintang berujung lima adalah ...", "Bintang laut", ["Bulu babi", "Teripang", "Ubur-ubur"]),
        ("Hewan laut berkulit duri tajam beracun yang menyerupai landak laut bulat hitam adalah ...", "Bulu babi", ["Bintang laut", "Teripang", "Kepiting"]),
        ("Hewan laut bercangkang yang terkenal menghasilkan butiran mutiara perhiasan berharga adalah ...", "Kerang Mutiara", ["Siput laut", "Teritip", "Kepiting"]),
    ]
    for q_text, corr, dists in extra_animal_trivia:
        if len(questions) >= 500:
            break
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pikirkan fakta fauna dan keajaiban dunia fauna."))

    # 10. Tradisi & Upacara Adat Nusantara (30 soal)
    rituals = [
        ("Upacara pembakaran jenazah tradisional umat Hindu di Pulau Bali disebut ...", "Ngaben", ["Rambu Solo", "Tiwah", "Kasada"]),
        ("Upacara adat pemakaman di mana peti jenazah diletakkan di celah tebing batu khas suku Toraja adalah ...", "Rambu Solo", ["Ngaben", "Tiwah", "Pasola"]),
        ("Perlombaan pacuan perahu dayung panjang khas di Sungai Kuantan Riau adalah ...", "Pacu Jalur", ["Karapan Sapi", "Makepung", "Fahombo"]),
        ("Tradisi melompati susunan batu setinggi dua meter khas pemuda di Pulau Nias adalah ...", "Fahombo (Lompat Batu)", ["Pacu Jalur", "Peresean", "Seba"]),
        ("Upacara melempar sesaji hasil bumi ke dalam kawah Gunung Bromo oleh suku Tengger disebut ...", "Yadnya Kasada", ["Rambu Solo", "Sekaten", "Tiwah"]),
        ("Perayaan pasar malam dan gamelan memperingati Maulid Nabi Muhammad SAW di Yogyakarta dan Solo adalah ...", "Sekaten", ["Grebeg Syawal", "Kasada", "Ngaben"]),
        ("Perang tanding menunggang kuda saling melempar tombak kayu tumpul di Sumba NTT adalah ...", "Pasola", ["Peresean", "Makepung", "Fahombo"]),
        ("Pertarungan ketangkasan dua pria saling memukul dengan rotan dan tameng kulit di Lombok disebut ...", "Peresean", ["Pasola", "Silat", "Tarung Derajat"]),
        ("Tradisi lomba balap kerbau yang dihias megah di Kabupaten Jembrana Bali disebut ...", "Makepung", ["Karapan Sapi", "Pacu Jalur", "Pasola"]),
        ("Tradisi pesta memasak daging dan ubi bersama beralaskan batu membara khas suku Papua adalah ...", "Bakar Batu (Barapen)", ["Tiwah", "Seba", "Kasada"]),
        ("Upacara adat syukuran panen padi masyarakat Sunda dengan mengarak rengkong disebut ...", "Seren Taun", ["Dugderan", "Sekaten", "Tabuik"]),
        ("Karnaval arak-arakan hewan imajiner Warak Ngendog menyambut bulan puasa di Semarang adalah ...", "Dugderan", ["Sekaten", "Seren Taun", "Grebeg"]),
        ("Tradisi mengarak keranda berbentuk buroq bermahkota lalu dilarung ke laut di Pariaman Sumbar adalah ...", "Tabuik", ["Sekaten", "Ngaben", "Kasada"]),
        ("Tradisi suku Baduy berjalan kaki ratusan kilometer menyerahkan hasil bumi kepada bupati/gubernur adalah ...", "Seba Baduy", ["Seren Taun", "Pasola", "Fahombo"]),
        ("Tradisi berburu dan menangkap cacing laut warna-warni di pantai selatan Lombok disebut ...", "Bau Nyale", ["Pasola", "Peresean", "Karapan"]),
        ("Pesta laut tradisi syukuran nelayan melarung sesaji kepala kerbau ke tengah laut disebut ...", "Petik Laut / Larung Sesaji", ["Ngaben", "Kasada", "Sekaten"]),
    ]
    for q_text, corr, dists in rituals:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami upacara adat dan tradisi di Indonesia."))

    # 11. Ciri Bendera Negara-Negara Dunia (25 soal)
    flags = [
        ("Bendera negara Jepang terdiri dari latar belakang putih dengan gambar di tengahnya berupa ...", "Lingkaran merah matahari", ["Bintang merah", "Bulan sabit", "Naga"]),
        ("Bendera kebangsaan Prancis tersusun dari tiga garis vertikal dengan urutan warna ...", "Biru, putih, dan merah", ["Merah, putih, dan biru", "Hitam, merah, dan kuning", "Hijau, putih, dan merah"]),
        ("Bendera kebangsaan Italia tersusun dari tiga garis vertikal dengan urutan warna ...", "Hijau, putih, dan merah", ["Biru, putih, dan merah", "Merah, putih, dan hijau", "Kuning, biru, dan merah"]),
        ("Bendera kebangsaan Jerman tersusun dari tiga garis horizontal berwarna ...", "Hitam, merah, dan emas (kuning)", ["Merah, putih, dan biru", "Biru, putih, dan merah", "Hijau, putih, dan merah"]),
        ("Bendera kebangsaan Belanda tersusun dari tiga garis horizontal berwarna ...", "Merah, putih, dan biru", ["Biru, putih, dan merah", "Hitam, merah, dan emas", "Putih, biru, dan merah"]),
        ("Bendera negara Arab Saudi berwarna dasar hijau dengan tulisan kaligrafi syahadat dan gambar ...", "Pedang lurus", ["Bulan sabit", "Bintang emas", "Pohon kurma"]),
        ("Bendera negara Kanada dihiasi simbol daun khas di bagian tengahnya, yaitu daun ...", "Daun Maple merah", ["Daun Eukaliptus", "Daun Zaitun", "Daun Semanggi"]),
        ("Bendera negara Amerika Serikat (The Stars and Stripes) memiliki berapa bintang putih pada bidang biru?", "50 bintang mewakili 50 negara bagian", ["48 bintang", "52 bintang", "45 bintang"]),
        ("Bendera kebangsaan Inggris (Union Jack) merupakan gabungan dari salib Santo George, Santo Andreas, dan ...", "Santo Patrick", ["Santo Petrus", "Santo Paulus", "Santo Thomas"]),
        ("Satu-satunya bendera nasional di dunia yang berbentuk bujur sangkar (persegi sama sisi) adalah bendera ...", "Swiss dan Vatikan", ["Jerman dan Prancis", "Jepang dan Korea", "Belgia dan Belanda"]),
        ("Bendera negara Turki berwarna merah menyala dengan gambar simbol berwarna putih berupa ...", "Bulan sabit dan satu bintang", ["Matahari terbit", "Pedang bersilang", "Singa"]),
        ("Bendera negara Korea Selatan (Taegukgi) memiliki simbol lingkaran merah-biru di tengah yang disebut ...", "Taegeuk (Yin dan Yang)", ["Matahari", "Bunga mawar", "Naga"]),
        ("Bendera kebangsaan Vietnam berwarna merah polos dengan lambang di tengahnya berupa ...", "Bintang kuning bersudut lima", ["Bulan sabit", "Palu arit", "Matahari"]),
        ("Bendera kebangsaan Brasil memiliki tulisan semboyan pada lingkaran bola dunia biru yang berbunyi ...", "Ordem e Progresso (Keteraturan dan Kemajuan)", ["Bhinneka Tunggal Ika", "In God We Trust", "E Pluribus Unum"]),
        ("Bendera kebangsaan Australia menampilkan gambar bendera Union Jack dan rasi bintang ...", "Salib Selatan (Southern Cross)", ["Orion", "Ursa Mayor", "Scorpio"]),
        ("Bendera negara Singapura terdiri dari warna merah dan putih yang dilengkapi lambang ...", "Bulan sabit dan 5 bintang putih", ["Matahari dan elang", "Bintang kuning besar", "Singa laut"]),
        ("Bendera negara Malaysia (Jalur Gemilang) memiliki lambang bulan sabit dan bintang bersudut ...", "14 sudut", ["5 sudut", "8 sudut", "12 sudut"]),
        ("Satu-satunya bendera negara di dunia yang tidak berbentuk segi empat melainkan dua segitiga bertumpuk adalah bendera ...", "Nepal", ["Bhutan", "Maladewa", "Sri Lanka"]),
        ("Bendera negara Tiongkok (China) berwarna merah dengan hiasan lima buah bintang berwarna ...", "Kuning emas", ["Putih perak", "Merah muda", "Biru"]),
        ("Bendera negara Yunani memiliki warna khas laut kepulauan Aegea, yaitu kombinasi warna ...", "Biru dan putih", ["Merah dan putih", "Hijau dan putih", "Kuning dan biru"]),
    ]
    for q_text, corr, dists in flags:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami bentuk dan warna bendera negara-negara di dunia."))

    # 12. Fakta Luar Angkasa, Penerbangan & Sains Populer (60 soal)
    space_and_flight = [
        ("Manusia pertama di dunia yang berhasil mendarat dan berjalan di permukaan Bulan pada 1969 adalah ...", "Neil Armstrong", ["Buzz Aldrin", "Yuri Gagarin", "Michael Collins"]),
        ("Manusia pertama di dunia yang berhasil meluncur ke luar angkasa mengorbit bumi pada 1961 adalah ...", "Yuri Gagarin", ["Neil Armstrong", "John Glenn", "Valentina Tereshkova"]),
        ("Wanita pertama di dunia yang berhasil terbang ke luar angkasa adalah ...", "Valentina Tereshkova", ["Sally Ride", "Kalpana Chawla", "Sunita Williams"]),
        ("Satelit buatan pertama buatan manusia yang berhasil diluncurkan ke orbit bumi oleh Uni Soviet adalah ...", "Sputnik 1", ["Explorer 1", "Vostok 1", "Apollo 11"]),
        ("Pesawat antariksa berawak Amerika Serikat yang pertama kali berhasil mendaratkan astronot di Bulan adalah ...", "Apollo 11", ["Apollo 13", "Challenger", "Columbia"]),
        ("Stasiun luar angkasa internasional terbesar yang dihuni para astronot mengorbit bumi adalah ...", "ISS (International Space Station)", ["Mir", "Skylab", "Tiangong"]),
        ("Teleskop cermin luar angkasa legendaris yang diluncurkan NASA tahun 1990 adalah ...", "Teleskop Luar Angkasa Hubble", ["Teleskop James Webb", "Teleskop Kepler", "Teleskop Spitzer"]),
        ("Teleskop inframerah tercanggih pelanjut Hubble yang diluncurkan NASA tahun 2021 adalah ...", "Teleskop Luar Angkasa James Webb", ["Teleskop Hubble", "Teleskop Galileo", "Teleskop Chandra"]),
        ("Planet dalam tata surya yang memiliki sistem cincin paling indah dan megah dari bongkahan es adalah ...", "Saturnus", ["Jupiter", "Uranus", "Neptunus"]),
        ("Bintang terdekat dari planet Bumi kita setelah Matahari adalah ...", "Proxima Centauri", ["Sirius", "Betelgeuse", "Polaris"]),
        ("Planet terdekat jaraknya dari Matahari adalah ...", "Merkurius", ["Venus", "Bumi", "Mars"]),
        ("Planet terpanas dalam tata surya karena efek rumah kaca gas karbon dioksida tebal adalah ...", "Venus", ["Merkurius", "Mars", "Jupiter"]),
        ("Bintang terdekat dari planet Bumi kita adalah ...", "Matahari", ["Proxima Centauri", "Sirius", "Polaris"]),
        ("Bintang paling terang di langit malam dilihat dari bumi adalah ...", "Sirius (Bintang Anjing)", ["Polaris", "Betelgeuse", "Rigel"]),
        ("Bintang kutub utara yang sejak zaman kuno digunakan pelaut sebagai pedoman arah utara adalah ...", "Polaris (Bintang Kutub)", ["Sirius", "Canopus", "Vega"]),
        ("Galaksi tempat tata surya dan planet Bumi kita berada dinamakan Galaksi ...", "Bima Sakti (Milky Way)", ["Andromeda", "Sombrero", "Triangulum"]),
        ("Galaksi spiral besar terdekat dari Galaksi Bima Sakti kita adalah Galaksi ...", "Andromeda", ["Bima Sakti", "Magellan", "Whirlpool"]),
        ("Lapisan atmosfer bumi tempat terjadinya fenomena cuaca, hujan, awan, dan petir adalah ...", "Troposfer", ["Stratosfer", "Mesosfer", "Termosfer"]),
        ("Lapisan atmosfer tempat pesawat jet komersial terbang tenang dan terdapat lapisan ozon pelindung UV adalah ...", "Stratosfer", ["Troposfer", "Mesosfer", "Eksosfer"]),
        ("Lapisan atmosfer paling dingin yang berfungsi membakar dan menghancurkan meteor jatuh adalah ...", "Mesosfer", ["Troposfer", "Stratosfer", "Termosfer"]),
        ("Lapisan atmosfer yang memantulkan gelombang radio sehingga radio AM bisa memancar jauh adalah ...", "Termosfer (Ionosfer)", ["Troposfer", "Stratosfer", "Mesosfer"]),
        ("Lapisan atmosfer terluar yang berbatasan langsung dengan ruang hampa hampa udara luar angkasa adalah ...", "Eksosfer", ["Mesosfer", "Stratosfer", "Troposfer"]),
        ("Cahaya warna-warni yang berkilau di langit malam kutub utara dan selatan akibat partikel matahari adalah ...", "Aurora (Borealis dan Australis)", ["Pelangi", "Komet", "Meteor"]),
        ("Batu luar angkasa yang terbakar menyala saat memasuki atmosfer bumi sering disebut bintang jatuh atau ...", "Meteor", ["Meteorit", "Meteoroid", "Asteroid"]),
        ("Sisa batu meteor dari luar angkasa yang berhasil jatuh sampai ke permukaan tanah bumi disebut ...", "Meteorit", ["Meteor", "Meteoroid", "Asteroid"]),
        ("Benda antariksa dari es dan debu yang mengorbit matahari dan mengeluarkan ekor gas bercahaya adalah ...", "Komet (Bintang berekor)", ["Asteroid", "Meteorit", "Planet"]),
        ("Komet paling terkenal yang melintas dekat bumi sekali setiap sekitar 76 tahun adalah ...", "Komet Halley", ["Komet Hale-Bopp", "Komet Neowise", "Komet Encke"]),
    ]
    for q_text, corr, dists in space_and_flight:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami fakta astronomi, atmosfer, dan antariksa."))

    # 13. Makanan & Minuman Populer Nusantara Lanjutan (40 soal)
    indo_culinary_more = [
        ("Minuman hangat rempah jahe, gula merah, kayu manis khas suku Sunda Jawa Barat adalah ...", "Bandrek", ["Bajigur", "Wedang Ronde", "Sekoteng"]),
        ("Minuman tradisional Sunda berbahan santan kelapa gurih, gula aren, dan irisan kelapa muda adalah ...", "Bajigur", ["Bandrek", "Es Cendol", "Bir Pletok"]),
        ("Minuman hangat berempah khas Betawi Jakarta yang sebenarnya tidak mengandung alkohol sama sekali adalah ...", "Bir Pletok", ["Bandrek", "Bajigur", "Wedang Jahe"]),
        ("Kudapan ketan fermentasi yang dibungkus daun pisang atau daun jambu air khas Jawa Barat adalah ...", "Peuyeum / Tape Ketan", ["Dodol", "Wajik", "Getuk"]),
        ("Kudapan manis dari olahan singkong rebus yang ditumbuk halus bersama gula dan kelapa parut adalah ...", "Getuk lindri", ["Tape singkong", "Combro", "Misro"]),
        ("Gorengan singkong parut berisi oncom pedas khas Sunda Jawa Barat adalah ...", "Combro (Oncom di jero)", ["Misro", "Gehu", "Cireng"]),
        ("Gorengan singkong parut berisi lelehan gula merah manis khas Sunda adalah ...", "Misro (Amis di jero)", ["Combro", "Bala-bala", "Cireng"]),
        ("Camilan kenyal goreng khas Bandung yang terbuat dari aci (tepung kanji) digoreng adalah ...", "Cireng (Aci digoreng)", ["Cilok", "Cimol", "Batagor"]),
        ("Camilan aci kenyal berbentuk bola kecil yang dimasak dengan cara direbus dan disiram bumbu kacang adalah ...", "Cilok (Aci dicolok)", ["Cireng", "Cimol", "Batagor"]),
        ("Camilan aci berbentuk bulatan kecil yang digoreng mengembang renyah gurih adalah ...", "Cimol (Aci digemol)", ["Cilok", "Cireng", "Batagor"]),
        ("Kudapan bakso tahu goreng renyah disiram bumbu kacang khas Bandung disingkat ...", "Batagor", ["Siomay", "Cireng", "Cilok"]),
        ("Minuman es segar berisi bulir hijau tepung beras, santan gurih, dan sirup gula merah khas Sunda adalah ...", "Es Cendol / Es Dawet", ["Es Teler", "Es Campur", "Es Goyobod"]),
        ("Minuman penutup segar khas Makassar yang memadukan pisang raja berbalut adonan hijau pandan dan bubur sumsum adalah ...", "Es Pisang Ijo", ["Es Pallubutung", "Es Cendol", "Es Doger"]),
        ("Bubur Manado khas Sulawesi Utara yang dimasak dengan labu kuning, jagung manis, dan aneka sayuran hijau adalah ...", "Tinutuan", ["Bubur Ayam", "Bubur Sumsum", "Coto Manado"]),
        ("Olahan sate khas Bali yang terbuat dari cincangan daging ikan atau ayam berbumbu lalu dililitkan pada batang serai adalah ...", "Sate Lilit", ["Sate Madura", "Sate Padang", "Sate Maranggi"]),
        ("Olahan sate daging sapi manis gurih empuk tanpa bumbu kacang khas Purwakarta Jawa Barat adalah ...", "Sate Maranggi", ["Sate Madura", "Sate Padang", "Sate Lilit"]),
        ("Sate kambing khas Bantul Yogyakarta yang ditusuk menggunakan jeruji besi sepeda adalah ...", "Sate Klathak", ["Sate Maranggi", "Sate Madura", "Sate Ponorogo"]),
        ("Olahan daging sapi kuah berempah kental khas Minangkabau dengan kuah tepung beras kuning gurih adalah ...", "Sate Padang", ["Sate Madura", "Sate Maranggi", "Sate Lilit"]),
        ("Sup ikan khas Batak Danau Toba yang dibumbui asam pedas menggunakan buah andaliman dan kecombrang adalah ...", "Arsik Ikan Mas", ["Gulai Ikan", "Pindang Patin", "Ikan Kuah Kuning"]),
        ("Sup ikan patin berkuah asam manis pedas beraroma nanas khas Palembang adalah ...", "Pindang Patin", ["Arsik", "Rawon", "Coto"]),
    ]
    for q_text, corr, dists in indo_culinary_more:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami ragam makanan, minuman, dan camilan khas daerah Indonesia."))

    # 14. Lambang Daerah, Kota & Fauna Endemik (hingga genap 500 soal)
    extra_geo_and_fauna = [
        ("Pulau di Indonesia yang mendapat julukan 'Pulau Seribu Pura' dan 'Pulau Dewata' adalah ...", "Pulau Bali", ["Pulau Lombok", "Pulau Flores", "Pulau Sumbawa"]),
        ("Pulau di Nusa Tenggara Barat yang mendapat julukan 'Pulau Seribu Masjid' adalah ...", "Pulau Lombok", ["Pulau Bali", "Pulau Flores", "Pulau Sumba"]),
        ("Daerah Istimewa di Indonesia yang mendapat julukan 'Kota Pelajar' dan 'Kota Gudeg' adalah ...", "DI Yogyakarta", ["Kota Bandung", "Kota Solo", "Kota Malang"]),
        ("Provinsi di Indonesia yang memiliki otonomi khusus syariat Islam dan dijuluki 'Serambi Mekkah' adalah ...", "Aceh", ["Sumatera Barat", "Riau", "Banten"]),
        ("Satu-satunya daerah di Indonesia setingkat provinsi yang dipimpin oleh seorang Sultan turun-temurun adalah ...", "DI Yogyakarta (Sultan Hamengkubuwono)", ["Surakarta", "Cirebon", "Ternate"]),
        ("Pulau Komodo secara administratif berada di dalam wilayah provinsi ...", "Nusa Tenggara Timur (NTT)", ["Nusa Tenggara Barat", "Bali", "Maluku"]),
        ("Hewan endemik kadal raksasa purba komodo memiliki nama ilmiah ...", "Varanus komodoensis", ["Panthera tigris", "Pongo pygmaeus", "Elephas maximus"]),
        ("Hewan primata orangutan yang terkenal cerdas hidup di pulau ...", "Sumatra dan Kalimantan", ["Jawa dan Bali", "Sulawesi dan Papua", "Maluku dan Timor"]),
        ("Badak bercula satu yang terancam punah hanya tersisa hidup di habitat alaminya di ...", "Taman Nasional Ujung Kulon Banten", ["Way Kambas Lampung", "Gunung Leuser", "Taman Safari"]),
        ("Pusat pelatihan dan konservasi gajah sumatra yang sangat terkenal berada di Taman Nasional ...", "Way Kambas di Lampung", ["Ujung Kulon", "Baluran", "Kerinci Seblat"]),
        ("Satwa endemik sejenis kerbau kerdil bertanduk runcing khas Pulau Sulawesi adalah ...", "Anoa", ["Babi rusa", "Tapir", "Tarsius"]),
        ("Satwa endemik unik yang memiliki taring mencuat menembus moncongnya di Pulau Sulawesi adalah ...", "Babi Rusa", ["Anoa", "Tapir", "Komodo"]),
        ("Primata terkecil di dunia dengan mata bulat besar yang hidup di Pulau Sulawesi adalah ...", "Tarsius (Tarsius spectrum)", ["Orangutan", "Owa jawa", "Bekantan"]),
        ("Monyet berhidung panjang dan besar yang menjadi maskot fauna Provinsi Kalimantan Selatan adalah ...", "Bekantan (Nasalis larvatus)", ["Tarsius", "Lutung kelabu", "Orangutan"]),
        ("Satwa bertubuh belang hitam-putih mirip babi berbelalai pendek yang hidup di hutan Sumatra adalah ...", "Tapir asia", ["Anoa", "Badak", "Trenggiling"]),
        ("Burung indah kebanggaan masyarakat Bali yang bulunya putih dengan lingkar mata biru adalah ...", "Jalak Bali (Leucopsar rothschildi)", ["Burung Merak", "Cenderawasih", "Kasuari"]),
        ("Burung kasuari yang bertubuh besar bergelambir dan bertanduk helm berasal dari pulau ...", "Papua", ["Sulawesi", "Kalimantan", "Sumatra"]),
        ("Pohon kayu harum bernilai sangat tinggi yang banyak tumbuh di Nusa Tenggara Timur adalah ...", "Pohon Cendana", ["Pohon Jati", "Pohon Ulin", "Pohon Gaharu"]),
        ("Pohon kayu besi yang sangat keras dan tahan air khas hutan Kalimantan adalah ...", "Kayu Ulin (Kayu Besi)", ["Kayu Jati", "Kayu Mahoni", "Kayu Pinus"]),
        ("Pohon penghasil minyak wangi termahal dari gumpalan resin hitam pohonnya di hutan tropis adalah ...", "Pohon Gaharu", ["Pohon Cendana", "Pohon Pinus", "Pohon Karet"]),
    ]
    for q_text, corr, dists in extra_geo_and_fauna:
        if len(questions) >= 500:
            break
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami fauna endemik dan julukan daerah Indonesia."))

    # 15. Lagu Wajib & Daerah Nusantara (35 soal)
    songs = [
        ("Lagu wajib nasional 'Bagimu Negeri' diciptakan oleh komponis ...", "Kusbini", ["Ismail Marzuki", "W.R. Supratman", "Ibu Sud"]),
        ("Lagu wajib nasional 'Halo-Halo Bandung' diciptakan oleh komponis ...", "Ismail Marzuki", ["Kusbini", "C. Simanjuntak", "L. Manik"]),
        ("Lagu wajib nasional 'Rayuan Pulau Kelapa' diciptakan oleh ...", "Ismail Marzuki", ["Kusbini", "W.R. Supratman", "A. Simanjuntak"]),
        ("Lagu wajib nasional 'Gugur Bunga' diciptakan untuk mengenang para pahlawan oleh ...", "Ismail Marzuki", ["Kusbini", "Ibu Sud", "H. Mutahar"]),
        ("Lagu wajib nasional 'Satu Nusa Satu Bangsa' diciptakan oleh ...", "Liberty Manik (L. Manik)", ["Ismail Marzuki", "Kusbini", "W.R. Supratman"]),
        ("Lagu wajib nasional 'Garuda Pancasila' diciptakan oleh ...", "Prohar Sudharnoto", ["Kusbini", "W.R. Supratman", "Ismail Marzuki"]),
        ("Lagu perjuangan 'Hari Merdeka' (Tujuh Belas Agustus Tahun Empat Lima) diciptakan oleh ...", "Husein Mutahar (H. Mutahar)", ["Ismail Marzuki", "Kusbini", "C. Simanjuntak"]),
        ("Lagu wajib nasional 'Syukur' yang bernuansa khidmat diciptakan oleh ...", "Husein Mutahar (H. Mutahar)", ["Ismail Marzuki", "Kusbini", "Ibu Sud"]),
        ("Lagu wajib nasional 'Maju Tak Gentar' diciptakan oleh komponis pejuang ...", "Cornel Simanjuntak (C. Simanjuntak)", ["Ismail Marzuki", "Kusbini", "L. Manik"]),
        ("Lagu perjuangan 'Bangun Pemudi Pemuda' diciptakan oleh ...", "Alfred Simanjuntak (A. Simanjuntak)", ["Cornel Simanjuntak", "Kusbini", "Ismail Marzuki"]),
        ("Lagu wajib nasional 'Dari Sabang Sampai Merauke' diciptakan oleh ...", "R. Soerardjo", ["Ismail Marzuki", "W.R. Supratman", "Kusbini"]),
        ("Lagu wajib 'Berkibarlah Benderaku' dan 'Tanah Airku' diciptakan oleh tokoh pendidik wanita ...", "Ibu Sud (Saridjah Niung)", ["Ibu Kasur", "Fatmawati", "Kartini"]),
        ("Lagu khidmat 'Mengheningkan Cipta' yang biasa dinyanyikan saat upacara bendera diciptakan oleh ...", "T. Prawit", ["Kusbini", "Ismail Marzuki", "W.R. Supratman"]),
        ("Lagu wajib nasional 'Indonesia Pusaka' (Indonesia tanah air beta...) diciptakan oleh ...", "Ismail Marzuki", ["Kusbini", "W.R. Supratman", "H. Mutahar"]),
        ("Lagu daerah 'Ampar-Ampar Pisang' yang menceritakan pisang diolah menjadi rimpi berasal dari ...", "Kalimantan Selatan", ["Kalimantan Barat", "Kalimantan Timur", "Kalimantan Tengah"]),
        ("Lagu daerah 'Yamko Rambe Yamko' dan 'Apuse' berasal dari provinsi ...", "Papua", ["Maluku", "Nusa Tenggara Timur", "Sulawesi Utara"]),
        ("Lagu daerah ceria 'Rasa Sayange' berasal dari kepulauan ...", "Maluku", ["Papua", "Nusa Tenggara", "Sulawesi"]),
        ("Lagu daerah 'Bungong Jeumpa' yang menceritakan keindahan bunga cempaka berasal dari ...", "Aceh", ["Sumatera Utara", "Sumatera Barat", "Riau"]),
        ("Lagu daerah 'Sinanggar Tulo' dan 'Butet' merupakan lagu tradisional suku Batak di ...", "Sumatera Utara", ["Sumatera Barat", "Aceh", "Jambi"]),
        ("Lagu daerah 'Kampuang Nan Jauh Di Mato' dan 'Ayam Den Lapeh' berasal dari suku Minang di ...", "Sumatera Barat", ["Riau", "Jambi", "Sumatera Selatan"]),
        ("Lagu daerah 'Kicir-Kicir' dan 'Jali-Jali' merupakan kesenian musik tradisional khas ...", "DKI Jakarta (Betawi)", ["Jawa Barat", "Banten", "Jawa Tengah"]),
        ("Lagu daerah 'Manuk Dadali', 'Bubuy Bulan', dan 'Tokecang' berasal dari suku Sunda di ...", "Jawa Barat", ["Jawa Tengah", "Jawa Timur", "Banten"]),
        ("Lagu daerah 'Gundul-Gundul Pacul' dan 'Suwe Ora Jamu' berasal dari masyarakat suku Jawa di ...", "Jawa Tengah dan DIY", ["Jawa Barat", "Bali", "Banten"]),
        ("Lagu daerah 'O Ina Ni Keke' berasal dari daerah Minahasa di provinsi ...", "Sulawesi Utara", ["Sulawesi Selatan", "Sulawesi Tengah", "Gorontalo"]),
        ("Lagu daerah 'Anging Mammiri' yang syahdu berasal dari suku Makassar di provinsi ...", "Sulawesi Selatan", ["Sulawesi Utara", "Sulawesi Tenggara", "Sulawesi Barat"]),
        ("Lagu daerah 'Bolelebo' berasal dari daerah kepulauan di provinsi ...", "Nusa Tenggara Timur (NTT)", ["Nusa Tenggara Barat", "Bali", "Maluku"]),
    ]
    for q_text, corr, dists in songs:
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami lagu wajib nasional dan lagu daerah di Indonesia."))

    # 16. Sejarah Tokoh & Monumen Umum (50 soal)
    history_monuments = [
        ("Patih Gajah Mada mengucapkan sumpah bersejarah untuk menyatukan wilayah Nusantara yang dinamakan ...", "Sumpah Palapa", ["Sumpah Pemuda", "Sumpah Setia", "Piagam Jakarta"]),
        ("Kerajaan maritim Buddha terbesar di Indonesia yang menjadi pusat pembelajaran agama Buddha internasional adalah ...", "Kerajaan Sriwijaya", ["Kerajaan Majapahit", "Kerajaan Mataram", "Kerajaan Kutai"]),
        ("Kerajaan Hindu tertua di Indonesia yang meninggalkan prasasti tiang batu bertuliskan huruf Pallawa (Yupa) adalah ...", "Kerajaan Kutai di Kalimantan Timur", ["Tarumanegara", "Sriwijaya", "Singasari"]),
        ("Kerajaan Hindu pertama di Pulau Jawa yang dipimpin oleh Raja Purnawarman adalah ...", "Kerajaan Tarumanegara", ["Kerajaan Kutai", "Kerajaan Kalingga", "Kerajaan Kediri"]),
        ("Kerajaan Islam pertama di Indonesia yang berada di wilayah ujung utara Pulau Sumatra adalah ...", "Kesultanan Samudera Pasai", ["Kesultanan Demak", "Kesultanan Malaka", "Kesultanan Aceh"]),
        ("Pahlawan wanita nasional asal Maluku yang gigih memimpin perlawanan rakyat melawan Belanda di usia muda adalah ...", "Christina Martha Tiahahu", ["Cut Nyak Dien", "R.A. Kartini", "Dewi Sartika"]),
        ("Kerajaan Islam pertama di Pulau Jawa yang didirikan oleh Raden Patah adalah ...", "Kesultanan Demak", ["Kesultanan Mataram", "Kesultanan Banten", "Kesultanan Cirebon"]),
        ("Sembilan ulama besar yang menyebarkan ajaran Islam di Pulau Jawa secara damai dan berbudaya dikenal dengan sebutan ...", "Wali Songo", ["Tiga Serangkai", "Panitia Sembilan", "Tritura"]),
        ("Sultan Mataram Islam yang memimpin penyerangan tentara besar-besaran mengepung Batavia melawan VOC adalah ...", "Sultan Agung Hanyokrokusumo", ["Sultan Hamengkubuwono I", "Raden Patah", "Sultan Hasanuddin"]),
        ("Pahlawan nasional yang dijuluki 'Ayam Jantan dari Timur' karena keberaniannya melawan VOC Belanda adalah ...", "Sultan Hasanuddin dari Makassar", ["Pangeran Antasari", "Kapitan Pattimura", "Tuanku Imam Bonjol"]),
        ("Pahlawan nasional dari Saparua Maluku yang memimpin perebutan Benteng Duurstede Belanda adalah ...", "Kapitan Pattimura (Thomas Matulessy)", ["Sultan Baabullah", "Pangeran Diponegoro", "Tuanku Imam Bonjol"]),
        ("Pahlawan wanita dari Maluku yang gigih mengangkat senjata melawan penjajah sejak usia belia (17 tahun) adalah ...", "Martha Christina Tiahahu", ["Cut Nyak Dien", "Cut Meutia", "R.A. Kartini"]),
        ("Pahlawan nasional yang memimpin rakyat Minangkabau dalam Perang Padri di Sumatera Barat adalah ...", "Tuanku Imam Bonjol", ["Pangeran Diponegoro", "Pattimura", "Teuku Umar"]),
        ("Pahlawan nasional yang memimpin Perang Jawa (1825–1830) melawan penindasan kolonial Belanda adalah ...", "Pangeran Diponegoro", ["Sentot Alibasyah", "Kiai Mojo", "Tuanku Imam Bonjol"]),
        ("Pahlawan wanita dari Aceh yang melanjutkan perjuangan gerilya suaminya Teuku Umar di hutan belantara adalah ...", "Cut Nyak Dien", ["Cut Meutia", "R.A. Kartini", "Dewi Sartika"]),
        ("Pahlawan nasional dari tanah Batak Sumatera Utara yang berjuang mempertahankan tanah air hingga gugur adalah ...", "Sisingamangaraja XII", ["Pattimura", "Diponegoro", "Antasari"]),
        ("Pahlawan nasional dari Kalimantan Selatan yang memimpin perlawanan rakyat dalam Perang Banjar adalah ...", "Pangeran Antasari", ["Pattimura", "Hasanuddin", "Diponegoro"]),
        ("Pahlawan nasional dari Bali yang memimpin perang puputan sampai titik darah penghabisan di Margarana adalah ...", "I Gusti Ngurah Rai", ["Ida Bagus Mantra", "Anak Agung", "Udayana"]),
        ("Organisasi pergerakan nasional modern pertama di Indonesia yang didirikan pada tanggal 20 Mei 1908 adalah ...", "Budi Utomo", ["Sarekat Islam", "Indische Partij", "Perhimpunan Indonesia"]),
        ("Tokoh pelopor emansipasi wanita Indonesia asal Jepara yang terkenal dengan buku 'Habis Gelap Terbitlah Terang' adalah ...", "Raden Ajeng Kartini (R.A. Kartini)", ["Dewi Sartika", "Cut Nyak Dien", "Rohana Kudus"]),
        ("Tokoh pelopor pendidikan wanita dari Tatar Sunda Jawa Barat pendiri Sakola Istri pada tahun 1904 adalah ...", "Raden Dewi Sartika", ["R.A. Kartini", "Nyi Ageng Serang", "Rasuna Said"]),
        ("Tokoh pendiri perguruan nasional Taman Siswa yang dinobatkan sebagai Bapak Pendidikan Nasional Indonesia adalah ...", "Ki Hajar Dewantara", ["Mohammad Hatta", "Soekarno", "K.H. Ahmad Dahlan"]),
        ("Tokoh pemuda yang mengetik naskah Proklamasi Kemerdekaan Indonesia yang bersih dan ditandatangani adalah ...", "Sayuti Melik", ["B.M. Diah", "Sukarni", "Chaerul Saleh"]),
        ("Ibu negara yang menjahit bendera pusaka Sang Saka Merah Putih untuk dikibarkan pada 17 Agustus 1945 adalah ...", "Ibu Fatmawati", ["Ibu Kartini", "Ibu Tien Soeharto", "Ibu Megawati"]),
        ("Dua tokoh pemuda pengibar bendera Merah Putih saat pembacaan naskah Proklamasi di Pegangsaan Timur adalah ...", "Latief Hendraningrat dan Suhud", ["Sayuti Melik dan Sukarni", "Chaerul Saleh dan Wikana", "B.M. Diah dan Yusuf"]),
        ("Panglima Besar TNI pertama yang memimpin perlawanan perang gerilya dari atas tandu melawan Belanda adalah ...", "Jenderal Sudirman", ["Jenderal Ahmad Yani", "Jenderal Nasution", "Jenderal Gatot Subroto"]),
        ("Pertempuran dahsyat di Surabaya mempertahankan kemerdekaan yang kemudian diperingati sebagai Hari Pahlawan terjadi pada ...", "10 November 1945", ["17 Agustus 1945", "28 Oktober 1928", "20 Mei 1908"]),
        ("Tokoh pemuda Surabaya yang pidatonya menggelegar membakar semangat juang arek-arek Suroboyo lewat corong radio adalah ...", "Bung Tomo (Sutomo)", ["Bung Karno", "Bung Hatta", "Gubernur Suryo"]),
        ("Peristiwa pembumihangusan kota oleh pejuang dan rakyat agar kota tidak dikuasai tentara Sekutu pada Maret 1946 adalah ...", "Bandung Lautan Api", ["Pertempuran Surabaya", "Palagan Ambarawa", "Medan Area"]),
        ("Pahlawan muda yang gugur bersama pasukannya meledakkan gudang mesiu Sekutu saat Bandung Lautan Api adalah ...", "Mohammad Toha", ["Bung Tomo", "Halim Perdanakusuma", "Abdul Halim"]),
        ("Gedung peninggalan Belanda di Bandung yang menjadi tempat terselenggaranya Konferensi Asia Afrika tahun 1955 adalah ...", "Gedung Merdeka", ["Gedung Sate", "Gedung Lawang Sewu", "Gedung Kesenian"]),
        ("Perjanjian pengakuan kedaulatan Republik Indonesia oleh kerajaan Belanda pada tahun 1949 disahkan dalam ...", "Konferensi Meja Bundar (KMB)", ["Perjanjian Renville", "Perjanjian Linggarjati", "Perjanjian Roem-Royen"]),
        ("Jembatan penyeberangan megah di atas Selat Madura yang menghubungkan Surabaya dan Pulau Madura adalah ...", "Jembatan Suramadu", ["Jembatan Ampera", "Jembatan Barito", "Jembatan Kutai Kartanegara"]),
        ("Jembatan megah di Kota Palembang yang melintasi Sungai Musi adalah ...", "Jembatan Ampera", ["Jembatan Suramadu", "Jembatan Merah", "Jembatan Barelang"]),
        ("Nama jembatan AMPERA di Palembang merupakan singkatan dari ...", "Amanat Penderitaan Rakyat", ["Angkatan Muda Pejuang Rakyat", "Amanah Persatuan Rakyat", "Aspirasi Masyarakat Perantau"]),
    ]
    for q_text, corr, dists in history_monuments:
        if len(questions) >= 500:
            break
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami peristiwa sejarah perjuangan bangsa dan monumen bersejarah."))

    # 17. Rekor Dunia & Pengetahuan Sehari-hari (30 soal)
    world_records = [
        ("Mamalia tertinggi di dunia yang memiliki leher sangat panjang adalah ...", "Jerapah", ["Unta", "Gajah", "Kuda"]),
        ("Hewan mamalia tercepat di darat saat berlari mengejar mangsa adalah ...", "Citah (Cheetah)", ["Singa", "Kuda", "Harimau"]),
        ("Burung tercepat di dunia saat menukik di udara menyambar mangsa adalah ...", "Alap-alap kawah (Peregrine Falcon)", ["Burung Elang", "Burung Rajawali", "Burung Kolibri"]),
        ("Ikan tercepat berenang di lautan dengan sirip punggung tinggi mirip layar adalah ...", "Ikan Layaran (Sailfish)", ["Ikan Hiu", "Ikan Tuna", "Lumba-lumba"]),
        ("Hewan dengan rentang usia terpanjang di dunia yang bisa hidup ratusan tahun adalah ...", "Kura-kura raksasa Galapagos / Aldabra", ["Paus biru", "Buaya", "Gajah"]),
        ("Tumbuhan berbunga dengan bunga tunggal terbesar dan terberat di dunia adalah ...", "Rafflesia arnoldii", ["Bunga Bangkai", "Teratai raksasa", "Bunga Matahari"]),
        ("Tumbuhan berbunga majemuk dengan struktur perbungaan tertinggi di dunia yang berbau busuk adalah ...", "Bunga Bangkai (Amorphophallus titanum)", ["Rafflesia arnoldii", "Kantong semar", "Kaktus"]),
        ("Pohon tertinggi di dunia yang berada di hutan California Amerika Serikat adalah ...", "Pohon Sequoia raksasa (Redwood)", ["Pohon Baobab", "Pohon Beringin", "Pohon Cemara"]),
        ("Gurun terluas di dunia (termasuk gurun dingin) adalah ...", "Gurun Benua Antartika", ["Gurun Sahara", "Gurun Gobi", "Gurun Kalahari"]),
        ("Negara kepulauan dengan jumlah pulau terbanyak di dunia adalah ...", "Swedia", ["Indonesia", "Filipina", "Norwegia"]),
        ("Terusan kapal buatan manusia yang memotong daratan genting di Mesir adalah ...", "Terusan Suez", ["Terusan Panama", "Terusan Kiel", "Terusan Korintus"]),
        ("Terusan kapal yang menghubungkan Samudra Pasifik dan Samudra Atlantik di Benua Amerika adalah ...", "Terusan Panama", ["Terusan Suez", "Terusan Kiel", "Terusan Volga"]),
        ("Pariwisata dunia yang memiliki Menara Jam Raksasa Big Ben berada di kota ...", "London", ["Paris", "Roma", "Berlin"]),
        ("Ikon pariwisata dunia Gedung Opera Sydney berada di negara ...", "Australia", ["Selandia Baru", "Kanada", "Inggris"]),
        ("Karya arsitektur kuno Tembok Besar yang panjangnya ribuan kilometer berada di negara ...", "Tiongkok", ["Jepang", "Mongolia", "Korea"]),
        ("Candi makam megah dari marmer putih Taj Mahal dibangun oleh Kaisar Shah Jahan di negara ...", "India", ["Pakistan", "Bangladesh", "Iran"]),
        ("Museum seni terkenal Louvre tempat dipamerkannya lukisan Mona Lisa berada di kota ...", "Paris", ["Amsterdam", "Madrid", "Wina"]),
        ("Patung batu Sphinx berkepala manusia dan bertubuh singa menjaga piramida di negara ...", "Mesir", ["Sudan", "Irak", "Yunani"]),
        ("Patung Yesus Kristus Penebus yang berdiri di puncak Gunung Corcovado berada di kota ...", "Rio de Janeiro (Brasil)", ["Sao Paulo", "Buenos Aires", "Bogota"]),
        ("Kanal air kota terapung dengan perahu gondola yang romantis berada di kota ...", "Venesia (Italia)", ["Florence", "Napoli", "Amsterdam"]),
        ("Sistem penulisan huruf timbul yang digunakan oleh para tunanetra untuk membaca adalah ...", "Huruf Braille", ["Huruf Pallawa", "Huruf Morse", "Huruf Kanji"]),
        ("Tokoh pencipta sistem tulisan huruf timbul Braille asal Prancis adalah ...", "Louis Braille", ["Alexander Graham Bell", "Louis Pasteur", "Samuel Morse"]),
        ("Tokoh pendiri gerakan Pramuka (Kepanduan Dunia) adalah ...", "Lord Robert Baden-Powell", ["Henry Dunant", "Alexander Fleming", "Thomas Edison"]),
        ("Warna pakaian seragam resmi anggota Pramuka Indonesia adalah ...", "Cokelat muda dan cokelat tua", ["Putih dan biru", "Merah dan putih", "Hijau lumut"]),
        ("Semboyan dan janji kehormatan bagi anggota Pramuka Penggalang adalah ...", "Tri Satya dan Dasa Darma", ["Pancasila dan UUD", "Sumpah Pemuda", "Bhinneka Tunggal Ika"]),
        ("Satu kodi kain sama dengan berapa lembar?", "20 lembar", ["12 lembar", "24 lembar", "100 lembar"]),
        ("Satu lusin piring sama dengan berapa buah?", "12 buah", ["10 buah", "20 buah", "24 buah"]),
        ("Satu gross kancing baju sama dengan berapa buah?", "144 buah (12 lusin)", ["100 buah", "120 buah", "200 buah"]),
        ("Satu rim kertas HVS cetak sama dengan berapa lembar?", "500 lembar", ["100 lembar", "1.000 lembar", "144 lembar"]),
    ]
    for q_text, corr, dists in world_records:
        if len(questions) >= 500:
            break
        add_q(build_mcq("Pengetahuan Umum", q_text, corr, dists, f"{q_text} Jawabannya adalah {corr}.", "Pahami fakta rekor dunia dan ukuran sehari-hari."))

    # 18. Pusat Pemerintahan Daerah di Indonesia (38 soal)
    prov_centers = [
        ("Jawa Timur", "Surabaya"), ("Jawa Tengah", "Semarang"), ("Jawa Barat", "Bandung"),
        ("Bali", "Denpasar"), ("Sumatera Utara", "Medan"), ("Sumatera Barat", "Padang"),
        ("Sulawesi Selatan", "Makassar"), ("Kalimantan Timur", "Samarinda"), ("Papua", "Jayapura"),
        ("Aceh", "Banda Aceh"), ("Riau", "Pekanbaru"), ("Lampung", "Bandar Lampung"),
        ("Nusa Tenggara Barat", "Mataram"), ("Nusa Tenggara Timur", "Kupang"),
        ("Kalimantan Selatan", "Banjarbaru"), ("Kalimantan Barat", "Pontianak"),
        ("Sulawesi Utara", "Manado"), ("Maluku", "Ambon"), ("Banten", "Serang"),
        ("Daerah Istimewa Yogyakarta", "Yogyakarta"), ("Sumatera Selatan", "Palembang"),
        ("Jambi", "Jambi"), ("Bengkulu", "Bengkulu"), ("Kepulauan Bangka Belitung", "Pangkalpinang"),
        ("Kepulauan Riau", "Tanjungpinang"), ("Kalimantan Tengah", "Palangka Raya"),
        ("Kalimantan Utara", "Tanjung Selor"), ("Gorontalo", "Gorontalo"),
        ("Sulawesi Tengah", "Palu"), ("Sulawesi Barat", "Mamuju"),
        ("Sulawesi Tenggara", "Kendari"), ("Maluku Utara", "Sofifi"),
        ("Papua Barat", "Manokwari"), ("Papua Barat Daya", "Sorong"),
        ("Papua Selatan", "Merauke"), ("Papua Tengah", "Nabire"),
        ("Papua Pegunungan", "Wamena"), ("Republik Indonesia saat ini", "DKI Jakarta"),
    ]
    for pr_name, c_center in prov_centers:
        if len(questions) >= 500:
            break
        dists = [c[1] for c in prov_centers if c[1] != c_center][:3]
        add_q(build_mcq(
            "Pengetahuan Umum",
            f"Pusat pemerintahan dan ibu kota dari Provinsi {pr_name} adalah kota ...",
            c_center,
            dists,
            f"Pusat pemerintahan Provinsi {pr_name} adalah {c_center}.",
            "Pikirkan ibu kota provinsi di Indonesia.",
        ))

    return questions[:500]
