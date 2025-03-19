import os
import pandas as pd
import numpy as np
import pdfplumber  # Alternative: use PyPDF2
from pdf2image import convert_from_path
import cv2

# Define folders
folders = ["BrainDisorder", "Emotional_disorder", "Sleep_Apnea"]
data_list = []

# Extract text from PDF (choose PyPDF2 or pdfplumber)
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

# Extract EEG waveform data
def extract_waveform_data(pdf_path):
    """Extract waveform graph from EEG report."""
    images = convert_from_path(pdf_path, dpi=300, poppler_path=r"C:\poppler-23.11.0\Library\bin")

    for img in images:
        img.save("temp_page.png", "PNG")
        image = cv2.imread("temp_page.png", cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
        edges = cv2.Canny(thresh, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        waveform_data = [(x, y) for cnt in contours for point in cnt for x, y in point]
        return sorted(waveform_data, key=lambda p: p[0])  # Sort by x-coordinates

# Process all PDFs
for folder in folders:
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder, file)
            patient_text = extract_text_from_pdf(pdf_path)
            eeg_waveform = extract_waveform_data(pdf_path)

            data_list.append({
                "Patient_ID": file.replace(".pdf", ""),
                "Disorder_Type": folder,
                "Report_Text": patient_text,
                "EEG_Data": eeg_waveform
            })

# Save as CSV
df = pd.DataFrame(data_list)
df.to_csv("EEG_Patient_Reports.csv", index=False)
