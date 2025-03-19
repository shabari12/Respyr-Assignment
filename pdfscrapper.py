import os
import pdfplumber
import pandas as pd

def extract_waveform_data(pdf_path):
    waveform_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    # Assuming waveform data starts with a timestamp (e.g., "00:02:01")
                    if line.strip() and line.strip()[0].isdigit():
                        waveform_data.append(line.strip())
    return waveform_data

def process_folder(folder_path, label):
    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            waveform_data = extract_waveform_data(pdf_path)
            for data in waveform_data:
                all_data.append([data, label])
    return all_data

# Define paths to your folders
brain_disorder_folder = "BrainDisorder"
emotional_disorder_folder = "Emotional_disorder"
sleep_apnea_folder = "Sleep_Apnea"

# Extract data from each folder
brain_data = process_folder(brain_disorder_folder, "BrainDisorder")
emotional_data = process_folder(emotional_disorder_folder, "EmotionalDisorder")
sleep_apnea_data = process_folder(sleep_apnea_folder, "SleepApnea")

# Combine all data
all_data = brain_data + emotional_data + sleep_apnea_data

# Convert to DataFrame
df = pd.DataFrame(all_data, columns=["Waveform", "Label"])

# Save to CSV
df.to_csv("eeg_waveform_data.csv", index=False)
print("Data saved to eeg_waveform_data.csv")