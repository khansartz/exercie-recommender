# app.py
import streamlit as st
import pandas as pd
import joblib
import re
import warnings
from PIL import Image, ImageOps
import requests
from io import BytesIO
import base64
import time
import urllib.parse



# Konfigurasi Halaman

st.set_page_config(
    page_title="Sistem Rekomendasi Fitness", 
    layout="centered"
)

# Muat Model & Aset

try:
    knn = joblib.load("models/knn_model.pkl")
    le_dict = joblib.load("models/label_encoders.pkl")
    le_target = joblib.load("models/target_encoder.pkl")
    scaler = joblib.load("models/scaler.pkl")
    preparation = joblib.load("models/preparation_data.pkl")
    
    from media import get_media_dict
    from media_info import get_media_info
    media_dict = get_media_dict()
    media_info = get_media_info()
    
    print("Semua model berhasil dimuat.") 

except FileNotFoundError as e:
    st.error(f"ERROR: File model tidak ditemukan ({e}). Pastikan semua file .pkl, media.py, media_info.py ada di folder yang sama.")  
    st.stop() # Hentikan app jika model tidak ada
except Exception as e:
    st.error(f"Error saat memuat model/aset: {e}") 
    st.stop()


# Inisialisasi Session

if "recommendation_data" not in st.session_state:
    st.session_state["recommendation_data"] = None
if "recommendation_timestamp" not in st.session_state:
    st.session_state["recommendation_timestamp"] = None


# STYLING (CSS)

st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: white; }
.sidebar-center { text-align: center; margin-bottom: 16px; }
.hero { background: linear-gradient(90deg, #4B2EF8 0%, #7A5AF5 50%, #9B6CFF 100%); color: white; padding: 36px; border-radius: 12px; margin-bottom: 18px; box-shadow: 0 6px 30px rgba(59,24,120,0.25); }
.rec-card { background: white; border-radius: 12px; padding: 14px; box-shadow: 0 6px 18px rgba(12,12,30,0.06); }
</style>
""", unsafe_allow_html=True)

# FUNGSI BANTU 

def calculate_bmi(height_cm, weight_kg):
    """Kalkulasi BMI dari tinggi (cm) dan berat (kg).""" 
    if height_cm == 0: return 0
    height_m = height_cm / 100.0
    return weight_kg / (height_m ** 2)

def get_bmi_level(bmi):
    """Menentukan Level BMI.""" 
    if bmi < 18.5: return "Underweight"
    elif 18.5 <= bmi < 24.9: return "Normal"
    elif 25.0 <= bmi < 29.9: return "Overweight"
    else: return "Obese" # Typo 'Obuse' dibenerin

def get_fitness_goal(level):
    """Menentukan Tujuan Fitness berdasarkan Level (aturan dari data)."""  
    if level in ["Underweight", "Normal"]: return "Weight Gain" # Naik Berat Badan
    elif level in ["Overweight", "Obese"]: return "Weight Loss" # Turun Berat Badan
    return None 

# ------------------------
# FUNGSI INFERENSI (Logika Baru)
# ------------------------
categorical_cols = ['Sex', 'Level', 'Fitness Goal']
numeric_cols = ['Age', 'Height', 'Weight', 'BMI']

def knn_predict_fitness(user_input_dict, le_dict, scaler, knn_model, le_target):
    """Prediksi Tipe Fitness dari data user yang sudah lengkap.""" 
    ordered_cols = ['Sex', 'Age', 'Height', 'Weight', 'BMI', 'Level', 'Fitness Goal']
    new_user = pd.DataFrame([user_input_dict])
    try:
        for col in categorical_cols:
            new_user.loc[:, col] = le_dict[col].transform(new_user[col])
    except Exception as e: return f"Error saat encoding: {e}." 
    new_user.loc[:, numeric_cols] = scaler.transform(new_user[numeric_cols])
    new_user = new_user[ordered_cols]
    pred_class = knn_model.predict(new_user)[0]
    return le_target.inverse_transform([pred_class])[0]

def cbf_recommendations(fitness_type, hypertension, diabetes, top_n=5):
    """Fungsi CBF (Content-Based Filtering) """
    hypertension_clean = str(hypertension).strip().title()
    diabetes_clean = str(diabetes).strip().title()
    # Filter dataset berdasarkan tipe fitness dan kondisi penyakit
    filtered_df = preparation[(preparation['Fitness Type'] == fitness_type) & (preparation['Hypertension'].str.strip().str.title() == hypertension_clean) & (preparation['Diabetes'].str.strip().str.title() == diabetes_clean)]
    
    if filtered_df.empty:
        # Fallback: Coba cari hanya berdasarkan tipe fitness jika tidak ada yg cocok persis
        st.warning(f"Tidak ada data cocok DENGAN (Tipe: {fitness_type}, Hipertensi: {hypertension_clean}, Diabetes: {diabetes_clean}). Mencari rekomendasi TANPA filter penyakit.")  
        filtered_df = preparation[preparation['Fitness Type'] == fitness_type]
        if filtered_df.empty: return {"Error": f"Tidak ada data untuk Tipe Fitness: {fitness_type}."}  
    
    # Ambil N baris teratas
    topN = filtered_df.head(top_n)
    
    try:
        # Voting (ambil modus/mayoritas) dari N baris teratas
        final_exercise = topN['Exercises'].mode()[0]
        final_equipment = topN['Equipment'].mode()[0]
        final_diet = topN['Diet'].mode()[0]
    except Exception as e: return {"Error": f"Gagal melakukan voting (mode()) rekomendasi: {e}"}  
    
    return {'Exercises': final_exercise, 'Equipment': final_equipment, 'Diet': final_diet}


# Sidebar (Input User)

with st.sidebar:
    st.markdown("<div class='sidebar-center'>", unsafe_allow_html=True)
    try: st.image("logo.jpg", width=170)
    except: st.info("logo.jpg tidak ditemukan") 
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 🧾 Masukkan Data Anda") 
    age = st.number_input("Usia", 10, 100, 25, 1) 
    height_cm = st.number_input("Tinggi Badan (cm)", 100, 250, 170, 1) 
    weight = st.number_input("Berat Badan (kg)", 30, 200, 70, 1) 

    # Opsi Tampilan Bahasa Indonesia
    sex_options = ["Laki-laki", "Perempuan"]
    yes_no_options = ["Tidak", "Ada"]

    # Pake label dan opsi Bahasa Indonesia
    sex_display = st.selectbox("Jenis Kelamin", sex_options) 
    hypertension_display = st.selectbox("Riwayat Hipertensi", yes_no_options) 
    diabetes_display = st.selectbox("Riwayat Diabetes", yes_no_options)

    # sex = st.selectbox("Jenis Kelamin", ["Male", "Female"]) 
    # hypertension = st.selectbox("Riwayat Hipertensi", ["No", "Yes"]) 
    # diabetes = st.selectbox("Riwayat Diabetes", ["No", "Yes"]) 
    
    submit = st.button("Dapatkan Rekomendasi") 
    if st.session_state["recommendation_data"] is not None and st.button("🧼 Reset Data"): 
        st.session_state.clear()
        st.rerun()


# Tools (Fungsi untuk Tampilan)

def img_to_base64(path_or_url, size=(250,180)):
    """Konversi gambar ke base64 untuk ditampilkan di HTML.""" 
    try:
        if path_or_url.startswith("http"): img = Image.open(BytesIO(requests.get(path_or_url).content))
        else: img = Image.open(path_or_url)
        img = img.convert("RGB").resize(size)
        img = ImageOps.expand(img, border=2, fill="#e6e6e6")
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        print(f"Error img_to_base64 ({path_or_url}): {e}") # Pesan error
        return None

def clean_items(text):
    """Mengubah string (misal: "a, b, and c") menjadi list item.""" 
    if not isinstance(text, str): return []
    text = text.replace("(", "").replace(")", "").replace(";", "|")
    text = text.replace(" and ", "|").replace(" or ", "|").replace(",", "|")
    cleaned_list = [item.strip().title() for item in text.split('|') if item.strip() and item.strip().lower() not in ["and", "or"]]
    return list(dict.fromkeys(cleaned_list)) # Hapus duplikat

def extract_diet_items(category, diet_string):
    """Mengekstrak item diet dari string per kategori pakai regex."""
    if not isinstance(diet_string, str): return []
    match = re.search(fr'{category}:\s*\(([^)]*)\)', diet_string, re.IGNORECASE)
    if match:
        item_string = match.group(1) # isinya "item1, item2, ..."
        return clean_items(item_string) # Kirim ke clean_items untuk di-split
    return []

def render_recommendation_section(title, items_list):
    """Fungsi bantu untuk menampilkan grid 2 kolom pakai clickable_card.""" 
    st.subheader(title)

    if items_list and isinstance(items_list, list):
        for i in range(0, len(items_list), 2):
            cols = st.columns(2)
            items_in_row = items_list[i:i+2]
            for idx, item in enumerate(items_in_row):
                if isinstance(item, str) and item: # Tambah cek string kosong
                    with cols[idx]:
                        clickable_card(item)
            
            #   JARAK ANTAR BARIS 
            st.write("") 
            #  BATAS TAMBAHAN 
            
    else:
        st.info(f"Tidak ada rekomendasi spesifik untuk {title.split(':')[0]}.") 

def clickable_card(label):
    """Membuat kartu rekomendasi yang bisa diklik."""
    if not label or not isinstance(label, str): # Cek keamanan
        print(f"DEBUG clickable_card: Label tidak valid: {label}") # Debugging
        return

    key = label.lower().replace(" ", "_")
    print(f"DEBUG clickable_card: Received label='{label}', Generated key='{key}'") # Debugging
    
    if key in media_dict:
        img64 = img_to_base64(media_dict[key])
        if img64: # Cek jika konversi gambar berhasil
            url = f"/?detail={urllib.parse.quote(key)}" # Buat URL dengan query parameter 'detail'
  
            st.markdown(
                f"""
                <a href="{url}" target="_blank" style="text-decoration:none;"> 
                    <div class="rec-card">
                    <img src="data:image/png;base64,{img64}" style="width:240px; height:170px; border-radius:8px; display:block; margin:auto;">
                    <p style="text-align:center; font-weight:bold; margin-top:6px; color:black;">{label}</p>
                    </div>
                </a>
                """, unsafe_allow_html=True
            )
        else:
             st.markdown(f"**- {label}** (Error Gambar)") # Tampilkan error gambar
    else:
        # Jika tidak ada gambar/key di media_dict, tampilkan sebagai teks biasa
        st.markdown(f"**- {label}** (Media key tidak ditemukan: '{key}')")  


# Tampilan Utama (Hero Section)

st.markdown('<div class="hero"><h1>💪 Pelatih Kebugaran Pribadi Anda</h1><p>Rekomendasi cerdas untuk latihan, alat, dan nutrisi harian Anda.</p></div>', unsafe_allow_html=True)  


# Halaman Detail

# Cek apakah parameter 'detail' ada di URL
if "detail" in st.query_params:
    
    # Ambil list semua value untuk parameter 'detail'
    detail_list = st.query_params.get_all("detail")
    
    # Ambil value PERTAMA dari list itu (jika listnya tidak kosong)
    item_key = detail_list[0] if detail_list else ""
    
    item_title = item_key.replace("_", " ").title() # Buat judul halaman
    
    st.title(item_title)
    print(f"DEBUG HALAMAN DETAIL: item_key dari URL = '{item_key}'") # Debug URL param

    info = media_info.get(item_key, {}) # Ambil info dari media_info.py
    image_path = media_dict.get(item_key) # Ambil path gambar dari media.py
    print(f"DEBUG HALAMAN DETAIL: Info ditemukan={bool(info)}, Gambar ditemukan={bool(image_path)}") # Debug dict lookup

    # Tampilkan Gambar
    if image_path:
        try: st.image(image_path, width=500)
        except Exception as e: st.error(f"Gagal memuat gambar: {e}") 
    
    # Tampilkan Deskripsi
    if "description" in info:
        st.subheader("📝 Penjelasan Singkat") 
        st.write(info["description"])
    
    # Tampilkan Tips (untuk Latihan/Alat)
    if "tips" in info:
        st.subheader("💡 Tips & Cara Pemakaian") 
        for tip in info["tips"]: st.write(f"- {tip}")

    # Tampilkan Kandungan (untuk Diet)
    if "kandungan" in info:
        st.subheader("🔬 Kandungan Baik") 
        for k in info["kandungan"]: st.write(f"- {k}")

    # Tampilkan Video
    if "youtube" in info:
        st.subheader("📺 Video Panduan") 
        st.video(info["youtube"])
    
    # Tampilkan Video untuk Diet
    if "youtube_d" in info:
        st.subheader("📺 Contoh Menu") 
        st.video(info["youtube_d"])
        
    # Jika tidak ada info sama sekali
    if not info:
        st.info("Belum ada info detail untuk item ini.") 

    # Tombol Kembali
    if st.button("⬅ Kembali ke Rekomendasi"): 
        st.query_params.clear() # Hapus parameter 'detail' dari URL
        st.rerun() # Muat ulang halaman utama

    st.stop() # Hentikan eksekusi script agar tidak lanjut ke bagian bawah


# Logika Saat Tombol "Dapatkan Rekomendasi" Ditekan

if submit:
    # Terjemahkan Jenis Kelamin
    sex = "Male" if sex_display == "Laki-laki" else "Female"
    # Terjemahkan Riwayat Penyakit
    hypertension = "Yes" if hypertension_display == "Ada" else "No"
    diabetes = "Yes" if diabetes_display == "Ada" else "No"

    with st.spinner("Mencari rekomendasi terbaik..."): 
        # Kalkulasi Turunan (BMI, Level, Goal) 
        bmi = calculate_bmi(height_cm, weight)
        level = get_bmi_level(bmi)
        goal = get_fitness_goal(level)

        # Siapkan input LENGKAP untuk model KNN 
        knn_input = {"Sex": sex, "Age": age, "Height": height_cm, "Weight": weight, "BMI": bmi, "Level": level, "Fitness Goal": goal}

        # Prediksi Tipe Fitness (KNN)
        pred_label = "Error"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            warnings.simplefilter("ignore", category=FutureWarning)
            pred_label = knn_predict_fitness(knn_input, le_dict, scaler, knn, le_target)

        if "Error" in pred_label: st.error(f"Prediksi KNN Gagal: {pred_label}") 
        else:
            # Dapatkan Rekomendasi Detail (CBF) 
            cbf_result = cbf_recommendations(fitness_type=pred_label, hypertension=hypertension, diabetes=diabetes, top_n=5)

            if "Error" in cbf_result: st.error(f"Rekomendasi CBF Gagal: {cbf_result['Error']}") 
            else:
                # Simpan hasil rekomendasi ke session state
                st.session_state["recommendation_data"] = {"pred_label": pred_label, "level": level, "goal": goal, "bmi": bmi, "best_row": cbf_result}
                st.session_state["recommendation_timestamp"] = time.time()
                st.rerun() # Muat ulang halaman untuk menampilkan hasil


# Tampilan Hasil Rekomendasi atau Info Awal 

# Cek apakah ada rekomendasi di session state
if st.session_state["recommendation_data"] is not None:

    # Jika ada rekomendasi, tampilkan hasilnya
    data = st.session_state["recommendation_data"]
    best_row = data["best_row"] # Ini dict {'Exercises': ..., 'Equipment': ..., 'Diet': ...}
    
    # Tampilkan info header hasil
    st.success(f"Rekomendasi tipe latihan: **{data['pred_label']}**", icon="✅") 
    st.markdown(f"Status Anda: **{data['level']}** (BMI: `{data['bmi']:.2f}`), tujuan yang direkomendasikan adalah **{data['goal']}**.")  
    st.header("Rekomendasi Untuk Anda 👇") 

    # Latihan (Exercises) 
    raw_exercises = best_row.get("Exercises", "")
    exercise_list = clean_items(raw_exercises)
    render_recommendation_section("🏋️ Latihan", exercise_list)  

    # Alat (Equipment) 
    raw_equipment = best_row.get("Equipment", "")
    equipment_list = clean_items(raw_equipment)
    render_recommendation_section("🧰 Alat", equipment_list)  

    # Diet 
    st.subheader("🥗 Diet")  
    raw_diet_string = best_row.get("Diet", "")
    
    if raw_diet_string and raw_diet_string.lower() != 'diet':
        # Ekstrak tiap kategori diet
        vegetables = extract_diet_items("Vegetables", raw_diet_string)
        proteins = extract_diet_items("Protein Intake", raw_diet_string)
        juices = extract_diet_items("Juice", raw_diet_string)
        
        # Tampilkan per kategori jika ada
        if vegetables: render_recommendation_section("Sayuran yang Direkomendasikan:", vegetables)  
        if proteins: render_recommendation_section("Sumber Protein yang Direkomendasikan:", proteins)  
        if juices: render_recommendation_section("Jus yang Direkomendasikan:", juices)  
        
        # Fallback jika format diet tidak dikenali
        if not vegetables and not proteins and not juices:
             st.info("Format diet tidak dikenali, tapi ini rekomendasinya:")  
             st.markdown(f"_{raw_diet_string}_")
    else:
        # Jika tidak ada rekomendasi diet
        st.info("Tidak ada rekomendasi diet spesifik.")  
        
# ELSE UNTUK MENAMPILKAN INFO AWAL ---
else:
    # Jika tidak ada rekomendasi dan tidak di halaman detail (karena halaman detail udah di-stop() di atas)
    # Tampilkan info box awal
    st.info(
        "Silakan isi data Anda di sidebar kiri, lalu klik tombol **'Dapatkan Rekomendasi'** untuk melihat saran latihan, alat, dan diet yang cocok untuk Anda!",
        icon="ℹ️"
    )