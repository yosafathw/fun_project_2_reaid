import streamlit as st
import requests
import json

# Konfigurasi halaman dasar
st.set_page_config(
    page_title="Local Guide Chatbot",
    page_icon="🤖",
    layout="centered"
)
st.title("Local Guide Chatbot")

# Init session state
if "active_profile" not in st.session_state:
    st.session_state.active_profile = {}
if "hasilperkenalan" not in st.session_state:
    st.session_state.hasilperkenalan = []
if "perkenalan_prompt" not in st.session_state:
    st.session_state.perkenalan_prompt = {}
if "profiles" not in st.session_state:
    st.session_state.profiles = []
if "choice" not in st.session_state:
    st.session_state.slct_profile = []
if "chatlogs" not in st.session_state:
    st.session_state.chatlogs = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "showhistory" not in st.session_state:
    st.session_state.showhistory = False
if "active_key" not in st.session_state: 
    st.session_state.active_key = []
name = []
location = []

#FUNCTIONS
def run_perkenalan(payload, model_name, api_key):
    if not api_key:
        st.error("API Key tidak diberikan. Masukkan di sidebar.", icon="🚨")
        return None
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            data=json.dumps({
                "model": model_name,
                "messages": payload
            })
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal terhubung ke API: {e}", icon="🔥")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}", icon="👎")
    return None

def get_ai_response(command_payload, model_name, api_key):
    if not api_key:
        st.error("API Key tidak diberikan. Masukkan di sidebar.", icon="🚨")
        return None
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            data=json.dumps({
                "model": model_name,
                "messages": command_payload,
            })
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal terhubung ke API: {e}", icon="🔥")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}", icon="👎")
    return None

#SIDEBARS
with st.sidebar:
    st.title("⚙️ Pengaturan")
    with st.expander("Tambah-Ubah-Pilih Profil", expanded=True):
        name = st.text_input("Masukkan Nama Kamu", placeholder="Budi", key="name")
        location = st.text_input("Masukkan Lokasi Kamu saat ini (komplek perumahan, desa / kelurahan, kecamatan, dan/atau kota)",placeholder="Serpong Utara, Tangerang Selatan", key="location")
        
        if st.button ("Tambah Profil"):
            if name and location:
                profile = {"name": name, "location": location}
                if profile in st.session_state.profiles:
                    st.warning("Profil duplikat")
                    profile_names = [prf["name"] for prf in st.session_state.profiles[-10:]]
                else: 
                    st.session_state.profiles.append(profile)
                    st.success(f"Profil '{name}' berhasil ditambahkan!")
                    profile_names = [prf["name"] for prf in st.session_state.profiles[-10:]]
            else:
                st.warning("Nama dan lokasi tidak boleh kosong!")
        
        profile_names = [prf["name"] for prf in st.session_state.profiles[-10:]]
        choice = st.selectbox("Pilihan Profil (klik Pilih Profil sebelum melanjutkan)", options=profile_names, key="profile_choice")   
        
        if st.button("Pilih Profil"):           
            matching_profile = next((p for p in st.session_state.profiles if p["name"] == choice), None)
            keys = f"{matching_profile['name']}_{matching_profile['location']}"
            if matching_profile:
                if matching_profile in st.session_state.slct_profile:
                    st.warning("Profil sudah dipilih sebelumnya")
                else:
                    st.session_state.slct_profile.append(matching_profile)
                    st.success(f"Profil '{matching_profile['name']}' berhasil dipilih")
                st.session_state.active_profile = matching_profile
                if keys not in st.session_state.chatlogs:
                    st.session_state.chatlogs[keys] = []
                st.session_state.active_profile = matching_profile
                st.session_state.active_key = keys
                if st.session_state.chatlogs[st.session_state.active_key]:
                    st.session_state.showhistory = True                 
            else:
                st.warning("Profil tidak ditemukan")
        
        if st.button ("Hapus Profil Terakhir dan Reset Pilihan Profil"):
            if st.session_state.profiles:
                rmv_profile = st.session_state.profiles.pop()
                st.success(f"Profil '{rmv_profile['name']}' berhasil dihapus")
                st.session_state.active_profile = []
            else:
                st.warning("Belum ada profil yang Ditambahkan")
    
    with st.expander("Pengaturan Model dan History", expanded=True):
        api_key_input = st.text_input(
            "OpenRouter API Key",
            type="password",
            placeholder="sk-or-v1-...",
            help="Dapatkan API key Anda di https://openrouter.ai/keys"
        )
        # Pilihan Model AI
        MODEL_LIST = {
            "Mistral Devstral 24B (Free)": "mistralai/devstral-small-2505:free",
            "Deepseek R1T2 (Free)": "tngtech/deepseek-r1t2-chimera:free",
            "Llama 3.1 Instruct (Free)": "meta-llama/llama-3.1-405b-instruct:free",
            "Google Flash 2.0 (Free)": "google/gemini-2.0-flash-exp:free",
            "Qwen 3 8B (Free)": "qwen/qwen3-8b:free"
        }
        selected_model = st.selectbox("Pilih Model", options=list(MODEL_LIST.keys()))
        model_id = MODEL_LIST[selected_model]

        if st.button("Konfirmasi Model AI"):
            if st.session_state.get("active_profile"):
                st.session_state.perkenalan_prompt = []
                st.session_state.hasilperkenalan = []                 
                prompt = f"Halo {selected_model}, saya {st.session_state.active_profile['name']} dan saya berada di daerah {st.session_state.active_profile['location']}, mohon bantuannya ya."
                payload = [{"role": "user", "content": prompt}]
                st.session_state.perkenalan_prompt = prompt
                st.session_state.perkenalan_payload = payload
                st.session_state.showspinner = True
                st.session_state.showhistory = True       
            else:
                st.session_state.showspinner = False

    if st.button("Hapus Riwayat Chat", use_container_width=True):
        if st.session_state.showhistory  == True:
            st.session_state.chatlogs[st.session_state.active_key] = []
            st.rerun()
            st.session_state.showhistory = False              
        else:
            st.session_state.messages=[]
            st.rerun()
    
# OUT FROM SIDEBAR  
if st.session_state.get("showspinner", False):
    with st.spinner("Mengirim informasi profil ke model AI"):
        hasil = run_perkenalan(
            model_name=model_id,
            payload=st.session_state.perkenalan_payload,
            api_key=api_key_input
        )
    st.session_state.hasilperkenalan = hasil
    st.session_state.showspinner = False

if st.session_state.hasilperkenalan != []:
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(st.session_state.perkenalan_prompt)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(st.session_state.hasilperkenalan)
else:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("Silahkan Atur Profil dan Pilih terlebih dahulu untuk personalisasi hasil dan riwayat chat atau lanjutkan sebagai tamu:")

if st.session_state.showhistory == True:
    if st.session_state.active_key:
        for message in st.session_state.chatlogs.get(st.session_state.active_key,[]):
            avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
    else:
        st.session_state.chatlogs[st.session_state.active_key] = {"info": keys, "messages": []}
        st.session_state.chatlogs.append(st.session_state.active_key)
else:
    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

if command := st.chat_input("Tulis pesan Anda..."):
            if st.session_state.active_profile.get('location', ''):
                loc = st.session_state.active_profile['location']
                loccommand = f"Di Daerah, {loc},, {command}"
                st.session_state.chatlogs[st.session_state.active_key].append({"role": "user", "content": loccommand})
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(command)
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Sedang memproses..."):
                        ai_response = get_ai_response(
                        command_payload = st.session_state.chatlogs.get(st.session_state.active_key,[]),
                        model_name=model_id,
                        api_key=api_key_input
                        )
                if ai_response:
                    st.markdown(ai_response)
                    st.session_state.chatlogs[st.session_state.active_key].append({"role": "assistant", "content": ai_response})
                else:
                    st.error("Gagal mendapatkan respons dari AI.")
            else:
                st.session_state.messages.append({"role": "user", "content": command})
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(command)    
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Sedang memproses..."):
                        ai_response = get_ai_response(
                        command_payload=st.session_state.messages,
                        model_name=model_id,
                        api_key=api_key_input
                    )
                if ai_response:
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.error("Gagal mendapatkan respons dari AI.")
        
        

    



