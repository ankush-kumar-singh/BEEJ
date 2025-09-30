import joblib
import os
import numpy as np

# 1️⃣ Load trained model and encoder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CROP_MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_model.pkl")
CROP_ENCODER_PATH = os.path.join(BASE_DIR, "models", "crop_label.pkl")

model = joblib.load(CROP_MODEL_PATH)
label_encoder = joblib.load(CROP_ENCODER_PATH)

# 2️⃣ Function to get top 3 crops with confidence
def recommend_top3_with_confidence(features):
    """
    features: list of [N, P, K, ph, rainfall, humidity, temp]
    returns: list of tuples (crop_name, confidence%)
    """
    # Predict probabilities for all crops
    proba = model.predict_proba([features])[0]
    
    # Get indices of top 3 probabilities
    top3_idx = np.argsort(proba)[-3:][::-1]
    
    # Convert indices to crop names
    top3_crops = label_encoder.inverse_transform(top3_idx)
    
    # Pair crop names with confidence percentages
    result = [(crop, round(proba[label_encoder.transform([crop])[0]]*100, 2)) 
              for crop in top3_crops]
    
    return result

# 3️⃣ Example input
sample_input = [89,45,36,21.3,80.5,6.4,185.5]  # [N, P, K, ph, rainfall, humidity, temp]

# 4️⃣ Get top 3 crops with confidence
top3_with_confidence = recommend_top3_with_confidence(sample_input)

# 5️⃣ Display results
print("Top 3 Recommended Crops with Confidence:")
for crop, confidence in top3_with_confidence:
    print(f"{crop}: {confidence}%")
