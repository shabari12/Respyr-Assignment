import streamlit as st
import time
from utils.preprocessing import extract_eeg_waveform
from utils.model import load_model, predict_target
from utils.styling import apply_custom_styles


st.set_page_config(
    page_title="Respyr EEG Prediction",
    page_icon="🧠",
    layout="centered",
)


apply_custom_styles()


st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: rgba(48, 139, 249, 0.85);">🧠 Respyr EEG Prediction</h1>
        <p style="font-size: 18px; color: #555;">
            Upload a PDF containing EEG data, and our AI will analyze the data to provide a medical insight.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown("<h3 style='color: rgba(48, 139, 249, 0.85);'>📄 Upload EEG Data (PDF)</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")


MODEL_PATH = "../model/random_forest_model.pkl"
LABEL_ENCODER_PATH = "../model/label_encoder.pkl"
rf_model, label_encoder = load_model(MODEL_PATH, LABEL_ENCODER_PATH)


if uploaded_file is not None:
 
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())


    st.markdown(
        """
        <div style="text-align: center; font-size: 24px; margin-top: 20px;">
            🧠🤖Our AI is Processing your EEG Report...
        </div>
        """,
        unsafe_allow_html=True,
    )


    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_complete + 1)


    eeg_data = extract_eeg_waveform("temp.pdf")
    predicted_class = predict_target(rf_model, label_encoder, eeg_data)


    st.success("✅ Analysis Complete!")
    st.markdown(
        f"""
        <div style="font-size: 18px; color: #333; padding: 10px; border-radius: 8px; background-color: #f9f9f9;">
            The analysis indicates that the patient is likely experiencing symptoms associated with 
            <b style="color: rgba(48, 139, 249, 0.85);">{predicted_class}</b>. 
            This condition may require further medical assessment. Please consult a neurologist for a 
            comprehensive evaluation.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; color: #666;">
        <p>Powered by AI | © 2025 Respyr EEG Analysis</p>
    </div>
    """,
    unsafe_allow_html=True,
)
