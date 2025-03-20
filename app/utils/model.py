import joblib
import pandas as pd

def load_model(model_path, label_encoder_path):
    """Load the trained model and label encoder."""
    model = joblib.load(model_path)
    label_encoder = joblib.load(label_encoder_path)
    return model, label_encoder

def predict_target(model, label_encoder, eeg_data):
    """Predict the target using the extracted time range data."""
    
    time_ranges = [eeg_data[f"TimeRange_{i}"] for i in range(1, 10)]

    
    input_data = pd.DataFrame([time_ranges], columns=[f"TimeRange_{i}" for i in range(1, 10)])

    
    prediction = model.predict(input_data)

    
    predicted_class = label_encoder.inverse_transform(prediction)[0]
    return predicted_class