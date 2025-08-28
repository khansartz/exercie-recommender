import streamlit as st
import pandas as pd
import joblib

# ------------------------
# Load model & data
# ------------------------
knn = joblib.load("knn_model.pkl")
le_dict = joblib.load("label_encoders.pkl")
le_target = joblib.load("target_encoder.pkl")
tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")
preparation = joblib.load("preparation_data.pkl")

# ------------------------
# Streamlit UI
# ------------------------
st.title("Fitness Recommendation System 💪")

st.header("Masukkan Data Diri Kamu")

# Input user
age = st.number_input("Age", min_value=10, max_value=100, value=25)
height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.7)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)

# Hitung BMI otomatis
bmi = weight / (height ** 2)
st.write(f"Your BMI is: {bmi:.2f}")

# Drop-downs
sex = st.selectbox("Sex", ["Male", "Female"])
level = st.selectbox("Level", ["Underweight", "Normal", "Overweight", "Obese"])
fitness_goal = st.selectbox("Fitness Goal", ["Weight Gain", "Weight Loss"])

# ------------------------
# Prediksi Fitness Type
# ------------------------
if st.button("Rekomendasi Fitness Type"):
    # Buat DataFrame user baru
    user_df = pd.DataFrame([{
        'Sex': sex,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'BMI': bmi,
        'Level': level,
        'Fitness Goal': fitness_goal
    }])

    # Encode fitur kategorikal
    for col in ['Sex', 'Level', 'Fitness Goal']:
        le = le_dict[col]
        user_df[col] = le.transform(user_df[col])

    # Prediksi KNN
    pred_class = knn.predict(user_df)[0]
    pred_label = le_target.inverse_transform([pred_class])[0]

    st.success(f"Tipe latihan yang direkomendasikan: {pred_label}")

    # ------------------------
    # CBF Recommendations
    # ------------------------
    # Masukkan user baru ke preparation sebagai row ke-0 sementara
    prep_copy = preparation.copy()
    prep_copy.loc[-1] = {
        'Fitness Type': pred_label,
        'Hypertension': 'No',  # default buat testing
        'Diabetes': 'No',       # default buat testing
        'Exercises': '',
        'Equipment': '',
        'Diet': ''
    }
    prep_copy.index = range(prep_copy.shape[0])  # reset index

    # Cosine similarity
    from sklearn.metrics.pairwise import cosine_similarity
    tfidf_user = tfidf_vectorizer.transform(prep_copy['Exercises'].astype(str) + " " +
                                           prep_copy['Equipment'].astype(str) + " " +
                                           prep_copy['Diet'].astype(str))
    cosine_sim = cosine_similarity(tfidf_user)
    cosine_sim_df = pd.DataFrame(cosine_sim, index=prep_copy.index, columns=prep_copy.index)

    # Filter dataset sesuai Fitness Type
    filtered_idx = prep_copy[prep_copy['Fitness Type'] == pred_label].index
    sim_scores = cosine_sim_df.loc[0, filtered_idx]
    top_indices = sim_scores.sort_values(ascending=False).head(5).index

    st.header("Rekomendasi Exercises, Equipment, Diet")
    st.table(prep_copy.loc[top_indices, ['Fitness Type', 'Exercises', 'Equipment', 'Diet']])
