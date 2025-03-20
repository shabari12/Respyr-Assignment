import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""
    custom_css = """
    <style>
    /* Background */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Arial', sans-serif;
    }

    /* Main heading */
    h1 {
        font-size: 32px;
        text-align: center;
        color: rgba(48, 139, 249, 0.85);
    }

    /* Subheading */
    h2, h3 {
        font-size: 24px;
        color: rgba(48, 139, 249, 0.85);
    }

    /* File uploader */
    .stFileUploader>div>div {
        border: 2px dashed rgba(48, 139, 249, 0.85);
        border-radius: 8px;
        background-color: #e9f5ff;
        padding: 20px;
        text-align: center;
    }

    /* Buttons */
    .stButton>button {
        background-color: rgba(48, 139, 249, 0.85);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: rgba(38, 119, 229, 0.85);
    }

    /* Success message */
    .stAlert {
        background-color: #dff0d8;
        color: #3c763d;
        border-radius: 8px;
        padding: 15px;
    }

    /* Prediction result box */
    .prediction-box {
        font-size: 18px;
        color: #333;
        padding: 10px;
        border-radius: 8px;
        background-color: #f9f9f9;
        margin-top: 20px;
    }

    /* Footer */
    div[data-testid="stMarkdownContainer"] > p {
        text-align: center;
        font-size: 14px;
        color: #666;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
