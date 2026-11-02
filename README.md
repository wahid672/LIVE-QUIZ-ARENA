# LIVE QUIZ ARENA — Tahap 1

Fondasi game kuis interaktif berbasis Python dan FastAPI. Tahap ini berjalan secara lokal di Windows dan Linux. Belum ada koneksi TikTok LIVE, dashboard visual, WebSocket overlay, atau integrasi OBS.

## Persyaratan

- Windows 10/11 atau distribusi Linux modern
- Python 3.11 atau lebih baru
- Koneksi internet saat instalasi dependency

## Windows

1. Ekstrak folder `LIVE-QUIZ-ARENA`.
2. Buka folder tersebut.
3. Klik dua kali `run.bat`.
4. Tunggu instalasi dependency selesai.
5. Buka `http://127.0.0.1:8000/docs`.

Launcher `run.bat` membuat virtual environment `.venv`, memasang dependency, lalu menjalankan FastAPI.

### Instalasi manual Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Jika aktivasi ditolak oleh PowerShell, jalankan:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Kemudian ulangi aktivasi.

## Linux

Pastikan Python 3.11+, `venv`, dan `pip` tersedia. Pada Debian/Ubuntu, jika modul venv belum tersedia:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

Dari direktori proyek:

```bash
chmod +x run.sh
./run.sh
```

Script akan membuat `.venv`, memasang dependency, lalu menjalankan FastAPI.

### Instalasi manual Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Membuka aplikasi

- API Documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

Hentikan server dengan `Ctrl+C` pada terminal.

## Menguji melalui Swagger

Buka `http://127.0.0.1:8000/docs`.

### Mulai permainan acak

`POST /api/game/start`

```json
{
  "mode": "random",
  "question_count": 10,
  "answer_duration": 15
}
```

### Mulai permainan manual

Gunakan ID dari `GET /api/questions`:

```json
{
  "mode": "manual",
  "question_id": "q001",
  "question_count": 10,
  "answer_duration": 15
}
```

### Kirim jawaban pemain

`POST /api/game/answer`

```json
{
  "username": "PemainContoh",
  "user_id": "user-001",
  "answer": "B"
}
```

Format jawaban: `A`, `B`, `C`, `D`, atau `JAWAB A`. Satu pemain hanya mendapat satu kesempatan per pertanyaan. Identitas memakai `user_id` jika tersedia, atau username sebagai cadangan.

### Status dan kontrol

- `GET /api/game/state` — status dan leaderboard.
- `POST /api/game/pause` — jeda.
- `POST /api/game/resume` — lanjutkan.
- `POST /api/game/next` — pertanyaan berikutnya.
- `POST /api/game/end` — akhiri permainan.

Kunci jawaban tidak dikirim saat fase `question`; jawaban dan penjelasan muncul setelah fase `reveal`. Endpoint `GET /api/questions` memuat kunci jawaban untuk dashboard lokal, jadi jangan publikasikan endpoint tersebut ke internet.

## Menambah soal

Edit `data/questions.json`. Setiap soal memerlukan `id` unik, `category`, `question`, `options` A-D, `correct_answer`, `explanation`, dan `hint`. Restart server setelah mengubah bank soal.

## Menjalankan pengujian

Aktifkan virtual environment, kemudian:

```bash
python -m pytest -q
```

## Aturan skor

- Jawaban benar: 100 poin dasar.
- Bonus kecepatan: maksimal 50 poin.
- Bonus streak: 10 poin per jawaban benar beruntun sebelumnya, maksimal 30 poin.
- Jawaban salah: 0 poin dan streak kembali ke 0.
- Jawaban pertama per pemain per pertanyaan yang dihitung.

## Batasan Tahap 1

Belum termasuk koneksi TikTok LIVE, pembaca event komentar/like/gift/follow, dashboard visual, WebSocket overlay, database permanen, dan OBS. Skor serta sesi masih disimpan di memori dan hilang ketika server dimatikan.

## Kompatibilitas

Kode aplikasi menggunakan Python dan dependency lintas platform. Launcher tersedia terpisah:
- `run.bat` untuk Windows.
- `run.sh` untuk Linux.


## Tahap 2 — Dashboard dan Overlay

Setelah memperbarui project dengan paket Tahap 2:

- Dashboard streamer: `http://127.0.0.1:8000/dashboard`
- OBS game overlay: `http://127.0.0.1:8000/overlay`
- WebSocket realtime: `/ws`
- API docs tetap tersedia di `/docs`

Dashboard menyediakan:
- Start, pause, resume, next question, dan end game.
- Mode random atau pemilihan soal manual.
- Pengaturan jumlah soal dan durasi.
- Leaderboard realtime.
- Player Simulator untuk menguji komentar tanpa TikTok LIVE.

Overlay menyediakan:
- Tampilan kuis vertikal.
- Empat pilihan jawaban.
- Countdown.
- Jawaban benar setelah ronde selesai.
- Leaderboard lima pemain teratas.

### Menguji Tahap 2

1. Jalankan server dengan `run.bat` (Windows) atau `./run.sh` (Linux).
2. Buka `/dashboard`.
3. Pilih Random atau Manual.
4. Tekan Start Quiz.
5. Buka `/overlay` pada tab lain.
6. Gunakan Player Simulator di dashboard untuk mengirim jawaban.
7. Amati perubahan timer, jumlah jawaban, skor, dan leaderboard pada dashboard serta overlay.

Untuk OBS, tambahkan Browser Source dengan URL `http://127.0.0.1:8000/overlay`. Atur lebar 1080 dan tinggi 1920. Background halaman overlay transparan; font eksternal memerlukan internet. Untuk penggunaan LIVE publik, jalankan server hanya pada perangkat sendiri dan jangan membuka port/API admin ke internet tanpa autentikasi.

WebSocket mengirim snapshot state setiap 0,4 detik. Pada tahap berikutnya, mekanisme polling-snapshot ini dapat dioptimalkan menjadi event-driven bila dibutuhkan.


## Tahap 3 — UI Refresh dan Auto Play

### Admin dashboard: Tabler

Dashboard menggunakan Tabler Core melalui CDN resmi:
- CSS: `https://cdn.jsdelivr.net/npm/@tabler/core@latest/dist/css/tabler.min.css`
- JavaScript: `https://cdn.jsdelivr.net/npm/@tabler/core@latest/dist/js/tabler.min.js`
- Icons: `https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css`

Tabler adalah UI kit admin open-source berbasis Bootstrap 5 dengan lisensi MIT. Karena asset template dimuat dari CDN, browser memerlukan koneksi internet untuk memuat stylesheet, script, dan ikon Tabler. Game Engine dan API lokal tetap berjalan di komputer.

### Overlay vertikal

- Rasio kanvas: 9:16.
- Browser preview otomatis menampilkan kanvas portrait di tengah halaman.
- Untuk OBS Browser Source: Width `1080`, Height `1920`.
- Konten menampilkan brand, nomor ronde, kategori, kartu pertanyaan, jawaban 2x2, countdown, jumlah jawaban, dan leaderboard.
- Latar kanvas gelap mengikuti contoh visual yang diberikan; elemen di luar kanvas transparan.

### Auto Play

Pengaturan Auto Play berada di Game Control:
- Default: OFF.
- Saat ON, timer pertanyaan selesai -> jawaban benar ditampilkan -> sistem menunggu sesuai Reveal time -> soal berikutnya dimulai otomatis.
- Reveal time dapat dipilih 2, 3, 4, 5, 8, 10, atau 15 detik.
- Pada Random mode, sistem memilih soal acak yang belum digunakan terlebih dahulu.
- Pada Manual mode, streamer memilih soal awal; auto advance berikutnya mengikuti urutan bank soal.
- Jika ronde terakhir selesai, sesi otomatis masuk ke status `finished`.
- Tombol Next Question tetap bisa digunakan untuk melewati waktu reveal. Aksi manual membatalkan auto advance yang sedang menunggu.

Pengaturan Auto Play disimpan pada sesi saat tombol Start Quiz ditekan.

### Pengujian tambahan

Pengujian Game Engine mencakup:
- Auto advance ke pertanyaan berikutnya.
- Auto finish setelah pertanyaan terakhir.
- Tombol Next manual membatalkan auto advance terjadwal.


### Third-party UI attribution

The dashboard shell and component styling are based on Tabler Core, an open-source Bootstrap 5 UI kit distributed under the MIT License. Tabler's official repository and license are available at:
- https://github.com/tabler/tabler
- https://github.com/tabler/tabler/blob/dev/LICENSE

Tabler assets are loaded from jsDelivr CDN in this version. The dashboard needs an internet connection to load those visual assets. The Python backend, quiz engine, and overlay remain local.


## Tahap 4 — TikTok LIVE Integration

### Install / update

Stage 4 adds `TikTokLive>=7.0.1,<8.0` to `requirements.txt`.
Start the project with `run.bat` on Windows or `./run.sh` on Linux; both launchers install any newly added dependencies automatically. For manual installation inside the activated virtual environment:

```bash
python -m pip install -r requirements.txt
```

### Connect to a public TikTok LIVE

1. Open `http://127.0.0.1:8000/dashboard`.
2. In **TikTok LIVE connection**, enter the creator username, for example `@yourusername`.
3. Click **Connect LIVE**.
4. The connection badge should change from `CONNECTING` to `CONNECTED` after TikTok accepts the connection.
5. Start a quiz session and check the activity feed.

Only the public creator username is needed. Do not enter a TikTok password, session cookie, or other account credentials. The adapter is read-only: it receives LIVE events and does not send messages, gifts, or account actions.

TikTokLive is an unofficial reverse-engineering project, not a TikTok-supported API. It may stop working when TikTok changes its Webcast protocol. It is intended for personal prototyping; there is no uptime guarantee. The connection must be to a publicly accessible LIVE room. Age-restricted rooms, offline creators, rate limits, regional restrictions, or protocol changes can prevent a connection. If it disconnects, use **Connect LIVE** again; automatic reconnection is not enabled in this MVP.

### Interaction rules

| TikTok event | LIVE QUIZ ARENA behavior |
|---|---|
| Comment `A`, `B`, `C`, `D`, or `JAWAB B` | Submits one answer per player per question using the existing quiz scoring |
| Like | Every 100 likes adds 5 seconds to the current question; maximum 30 bonus seconds per question |
| Follow | Awards 25 bonus points once per viewer per game session |
| Gift | Triggers a gift alert and adds diamond totals to a separate Top Gifters board; does not add quiz answer points |

Likes received outside an active question are queued and applied when the next question opens. A viewer's follow before a game session starts is not awarded retroactively. Gift streak intermediate events are ignored; the final streak event is counted once. TikTok may batch like updates, so the like meter uses the event's per-update `count` rather than treating each event as exactly one like.

### Local event simulator

The **Live event simulator** card lets you test each event without a TikTok connection:
- Comment: use `A`, `B`, `C`, or `D` while a question is open.
- Like: send `100` to test a +5 second reward.
- Follow: send the same viewer twice to confirm the bonus is awarded only once.
- Gift: send a gift and confirm the alert and Top Gifters leaderboard.

The simulator calls the same interaction processor as the real TikTok event handlers.

### New API endpoints

- `GET /api/tiktok/status` — connection and interaction status.
- `POST /api/tiktok/connect` — connect to a creator's public LIVE.
- `POST /api/tiktok/disconnect` — disconnect.
- `POST /api/tiktok/test-event` — local event simulation.
- `GET /api/game/state` — existing game state.

### Privacy and local safety

Run the app on `127.0.0.1` for personal use. Do not expose the local API to the public internet without authentication, rate limiting, and a security review. The event feed stores only a short in-memory list of recent public LIVE events and resets at the start of a new game session. The game and interaction data remain in memory and are lost when the server stops.

### Third-party attribution

TikTokLive is an independent, unofficial Python library. Its license is a modified AGPL license; review the upstream license before redistributing or offering this application as a hosted service:
https://github.com/isaackogan/TikTokLive/blob/master/LICENSE


## Tahap 5 — YouTube Music, Countdown Sound, dan Mobile Polish

### Perbaikan tampilan overlay

- Latar halaman di luar kanvas 9:16 sekarang berwarna gelap, bukan transparan ke latar putih browser.
- Spacing dan ukuran beberapa kartu overlay dipadatkan agar leaderboard dan supporter panel lebih muat pada layar portrait.
- Tombol countdown sound tersedia di header overlay.
- Animasi timer menjadi merah dan berdenyut saat lima detik terakhir.

### Countdown sound

1. Buka `/overlay`.
2. Ketuk tombol **SOUND OFF** di header untuk mengaktifkan suara.
3. Beep dibuat langsung oleh Web Audio API (tidak memerlukan file audio).
4. Beep berbunyi pada 5, 4, 3, 2, dan 1 detik terakhir setiap pertanyaan.
5. Ketuk tombol yang sama untuk mematikan suara.

Browser dapat memblokir audio otomatis sebelum ada interaksi pengguna. Untuk OBS Browser Source, klik kanan source `/overlay` → **Interact**, lalu klik tombol SOUND OFF satu kali. Pengaturan audio browser source dapat berbeda di tiap perangkat.

### YouTube Music Playlist

Dashboard menyediakan YouTube Music Playlist:
- Paste beberapa link, satu link per baris.
- Mendukung video `youtube.com/watch`, `youtu.be`, Shorts, dan link playlist `youtube.com/playlist?list=...`.
- Link duplikat diabaikan.
- Play, Pause, Previous, Next, Loop, Volume, dan hapus track.
- Daftar link disimpan di `data/music_playlist.json` dan tetap tersedia setelah server restart.

### Menambahkan music player ke OBS

YouTube player disediakan sebagai Browser Source terpisah agar pemutar YouTube tetap terlihat dan tidak disembunyikan di dalam overlay kuis.

1. Tambahkan Browser Source baru di OBS.
2. URL: `http://127.0.0.1:8000/music` (atau URL hosting aplikasi yang sama dengan dashboard).
3. Ukuran yang disarankan: Width `360`, Height `260`.
4. Klik **Enable Music** pada halaman player satu kali jika autoplay diblokir.
5. Aktifkan **Control audio via OBS** pada Browser Source untuk mengatur audio melalui mixer OBS.
6. Kelola queue dan volume dari kartu YouTube Music Playlist di dashboard.

YouTube harus dapat diakses oleh browser source. Sebagian video/playlist tidak mengizinkan embedding, dibatasi wilayah/usia, atau tidak dapat diputar di browser source. Jika demikian, pilih video lain. Gunakan hanya musik yang memang boleh Anda gunakan dalam siaran; kebijakan hak cipta YouTube dan platform LIVE tetap berlaku.

### Google Translate

Halaman overlay dan dashboard menggunakan `translate="no"`, class `notranslate`, dan meta `google=notranslate` untuk meminta Google Translate tidak menerjemahkan UI. Pengaturan ini mencegah terjemahan otomatis pada implementasi Google Translate yang menghormati atribut tersebut; fitur terjemahan browser pihak ketiga yang mengabaikannya tidak dapat dikendalikan oleh halaman.

### API musik

- `GET /api/music/state` — membaca queue dan status player.
- `POST /api/music/playlist/add` — menambah satu atau beberapa URL.
- `POST /api/music/playlist/remove` — menghapus track.
- `POST /api/music/control` — play, pause, previous, next, ended, select, volume, dan loop.
- `/music` — halaman Browser Source untuk YouTube IFrame Player.


## Tahap 6 — Overlay Redesign, Fix YouTube Playlist, dan Large Question Bank

### Overlay redesign untuk LIVE production

Overlay vertikal didesain ulang agar:
- lebih ringan dilihat,
- tidak terlalu menumpuk,
- header lebih sederhana,
- countdown memakai lingkaran mengambang,
- leaderboard di bagian bawah memuat lebih banyak penonton.

Perubahan utama:
- Header menjadi satu baris informasi yang lebih ringkas.
- Tombol **SOUND OFF** dihapus dari tampilan produksi.
- Countdown diganti menjadi floating circular timer.
- Kartu leaderboard menampilkan sampai 8 pemain.
- Kartu top gifters dipisahkan agar overlay tetap rapi.
- Audio countdown beep tetap tersedia dan otomatis aktif setelah interaksi pertama dengan halaman (misalnya klik pada browser source melalui mode Interact di OBS).

### Perbaikan YouTube Playlist

Playlist YouTube diperbaiki agar lebih toleran terhadap input pengguna:
- Mendukung URL biasa `youtube.com/watch?v=...`
- Mendukung `youtu.be/...`
- Mendukung URL dengan parameter tambahan seperti `&t=`, `&si=`, dan lain-lain
- Mendukung Shorts / live / embed URL
- Mendukung **paste langsung video ID** 11 karakter
- Mendukung **paste langsung playlist ID**
- Pesan status di dashboard sekarang lebih jelas saat link berhasil ditambahkan atau gagal divalidasi

Jika video tetap gagal diputar, kemungkinan besar video tersebut memang tidak mengizinkan embed di browser source YouTube. Dalam kasus itu, coba video lain.

### Large question bank

Ditambahkan bank soal ringan dan fun:
- Matematika: 500 soal
- Geografi: 500 soal
- Biologi: 500 soal
- Bahasa Indonesia: 500 soal
- Pengetahuan Umum: 500 soal

Total bawaan saat ini: **2.500 soal**.

Semua soal dirancang ringan, cepat dijawab, dan cocok untuk format LIVE interaktif.

### Regenerasi bank soal

Jika ingin membangun ulang bank soal:
```bash
python scripts/generate_question_bank.py
```

Script ini akan membuat ulang `data/questions.json`.


## Tahap 7 — Bank Soal 6.000, Fastest Answer Popup, dan Round Result

### Bank soal diperluas

Bank soal sekarang memiliki 12 kategori, masing-masing 500 soal ringan:
- Matematika
- Geografi
- Biologi
- Bahasa Indonesia
- Pengetahuan Umum
- Bahasa Inggris
- Sejarah
- IPA
- IPS
- Fisika
- Kimia
- Ekonomi

Total: **6.000 soal**.

Soal tambahan menggunakan format pilihan ganda A/B/C/D, dilengkapi kunci, penjelasan singkat, dan hint. Generator tersedia di `scripts/generate_question_bank.py`.

### Filter mata pelajaran di dashboard

Saat menggunakan Manual Selection, pilih mata pelajaran terlebih dahulu. Daftar pertanyaan kemudian difilter agar tidak perlu mencari di antara ribuan soal sekaligus. Random mode tetap dapat memilih dari seluruh bank soal.

### Fastest Answer popup

- Penonton pertama yang mengirim jawaban benar dalam satu ronde mendapat bonus tambahan **+50 poin**.
- Bonus kecepatan dan streak yang sudah ada tetap dihitung.
- Popup animasi muncul di tengah overlay dan menampilkan nama penonton serta bonus poin.
- Hanya satu penonton yang mendapat bonus tercepat per ronde. Jawaban salah tidak mengunci bonus ini.

### Round result popup

Saat ronde berakhir, overlay menampilkan:
- jumlah jawaban benar,
- jumlah jawaban salah,
- total penonton yang mengirim jawaban.

Popup hasil tampil di tengah layar dengan animasi, lalu menghilang otomatis sebelum ronde berikutnya.

### Catatan scoring

Jawaban benar tetap mendapat 100 poin dasar, bonus kecepatan hingga 50 poin, bonus streak hingga 30 poin, dan bonus penjawab benar pertama sebesar 50 poin. Jadi penjawab tercepat bisa memperoleh hingga 230 poin pada ronde tersebut jika bonus lain mencapai nilai maksimal.
