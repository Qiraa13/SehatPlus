import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

def main():
    print("Memulai proses training model...")
    
    # Define path to dataset
    dataset_path = 'ObesityDataSet_raw_and_data_sinthetic.csv'
    
    # Cek apakah file ada
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset {dataset_path} tidak ditemukan!")
        return

    # Load dataset
    df = pd.read_csv(dataset_path)
    print("Dataset berhasil dimuat.")
    
    # Preprocessing spesifik sesuai permintaan: Ubah Height dari meter ke centimeter
    print("Mengonversi kolom 'Height' dari meter ke centimeter...")
    df['Height'] = df['Height'] * 100
    
    # Pisahkan fitur (X) dan target (y)
    X = df.drop('NObeyesdad', axis=1)
    y = df['NObeyesdad']
    
    # Encode target variable
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Simpan mapping kelas target
    target_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
    print("Target Classes Mapping:", target_mapping)

    # Identifikasi kolom numerik dan kategorikal
    numeric_features = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
    categorical_features = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']
    
    # Buat transformer untuk preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ])
    
    # Buat pipeline model menggunakan Random Forest
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Split data untuk evaluasi (opsional, tapi baik untuk mengecek performa)
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    
    # Train pipeline
    print("Sedang melatih model Random Forest...")
    model_pipeline.fit(X_train, y_train)
    
    # Evaluasi model
    y_pred = model_pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Akurasi Model pada Test Set: {acc:.4f}")
    
    # Simpan pipeline model dan label encoder
    print("Menyimpan model ke dalam file 'model.pkl' dan encoder ke 'label_encoder.pkl'...")
    joblib.dump(model_pipeline, 'model.pkl')
    joblib.dump(label_encoder, 'label_encoder.pkl')
    
    print("Selesai! Model berhasil dilatih dan disimpan.")

if __name__ == "__main__":
    main()
