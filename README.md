#🧭 Local Guide Chatbot

Chatbot personal berbasis Streamlit dan OpenRouter AI, memungkinkan pengguna untuk berinteraksi dengan AI berdasarkan profil nama dan lokasi yang dipilih. Dirancang untuk menyesuaikan respons AI dengan konteks geografis pengguna, seolah-olah AI adalah pemandu lokal pribadi Anda.

##🚀 Fitur Unggulan

👤 Manajemen Profil: Tambah, pilih, dan hapus profil pengguna (nama & lokasi).

🤖 Interaksi AI Kontekstual: AI memberikan respons berdasarkan profil aktif.

🧠 Riwayat Chat per Profil: Setiap profil memiliki riwayat chat tersendiri.

🔄 Pemilihan Model AI: Bebas memilih dari beberapa model AI gratis (via OpenRouter).

🗑️ Reset Riwayat Chat: Hapus riwayat percakapan sesuai profil dengan mudah.


##🛠️ Teknologi yang Digunakan

Streamlit untuk antarmuka pengguna

OpenRouter API sebagai penyedia model AI

Python 3.11+

requests, json untuk komunikasi API


##🔧 Cara Menjalankan di Lokal

Clone repositori

git clone https://github.com/namakamu/fun_project_2_reaid

cd local-guide-chatbot

(Opsional) Buat dan aktifkan virtual environment


##Instalasi dependensi

pip install streamlit requests


##Jalankan aplikasi

streamlit run app.py


##🔑 Cara Menggunakan

Tambahkan Nama dan Lokasi kamu dan user2 lain (misal teman atau keluarga di daerah lain) di bagian samping (sidebar).

Klik Tambah Profil

Pilih User sesuai pilihan di dropdown bawah, lalu klik Pilih Profil

Pilih Model AI, lalu klik Konfirmasi Model.

Mulai percakapan seperti biasa!

Ganti profil untuk melihat riwayat percakapan berbeda atau Hapus History jika diperlukan.

Dapat juga gunakan sebagai tamu namun nama, lokasi, dan riwayat tidak terpersonalisasi.
