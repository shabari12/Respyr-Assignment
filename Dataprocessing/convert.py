import os
import cv2
import numpy as np
import pandas as pd
from pdf2image import convert_from_path

# Define folder paths and output CSV
folders = {
    "Emotional_disorder": "Emotional_disorder",
    "BrainDisorder": "BrainDisorder",
    "Sleep_Apnea": "Sleep_Apnea"
}
output_csv = "EEG_Waveform_Data_Combined_15Ranges.csv"
poppler_path = r"C:\poppler-24.08.0\Library\bin"  # Update this path to your poppler installation

# Function to extract EEG waveform data
def extract_eeg_waveform(pdf_path):
    images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    combined_amplitude = []  # Store amplitude data for all pages

    for i, img in enumerate(images):
        print(f"Processing {pdf_path} - Page {i+1}...")

        # Convert image to grayscale
        img_cv = np.array(img)
        img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)

        # Thresholding to isolate the waveform
        _, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
        edges = cv2.Canny(thresh, 50, 150)  # Detect edges

        # Find contours (waveform points)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        waveform_points = []
        for cnt in contours:
            for point in cnt:
                x, y = point[0]  # Extract x (time) and y (amplitude)
                waveform_points.append((x, y))

        # Sort waveform points by time (x-axis)
        waveform_points = sorted(waveform_points, key=lambda p: p[0])

        # Normalize amplitude data
        if waveform_points:
            waveform_data = np.array(waveform_points)
            time_series = waveform_data[:, 0]  # X-axis (time)
            amplitude_series = waveform_data[:, 1]  # Y-axis (EEG amplitude)

            # Normalize amplitude to [0, 1]
            amplitude_series = (amplitude_series - np.min(amplitude_series)) / (
                np.max(amplitude_series) - np.min(amplitude_series)
            )

            # Bin the data into 15 time ranges
            bins = np.linspace(time_series.min(), time_series.max(), num=16)  # 16 bins for 15 ranges
            binned_data = []

            for j in range(len(bins) - 1):
                bin_mask = (time_series >= bins[j]) & (time_series < bins[j + 1])
                if np.any(bin_mask):
                    avg_amplitude = np.mean(amplitude_series[bin_mask])
                    binned_data.append(avg_amplitude)
                else:
                    binned_data.append(np.nan)  # Handle empty bins

            # Append binned data for this page
            combined_amplitude.append(binned_data)

    # Average amplitude data across all pages
    if combined_amplitude:
        combined_amplitude = np.nanmean(np.array(combined_amplitude), axis=0)  # Averaging across pages
    else:
        combined_amplitude = [np.nan] * 15  # If no data, fill with NaN for 15 ranges

    return combined_amplitude

# Extract data from all folders
all_waveform_data = []
for label, folder_path in folders.items():
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)
            eeg_data = extract_eeg_waveform(pdf_path)
            eeg_data_dict = {
                "PDF_Name": file,
                **{f"TimeRange_{j+1}": eeg_data[j] for j in range(len(eeg_data))},
                "Target": label  # Add target label
            }
            all_waveform_data.append(eeg_data_dict)

# Create a DataFrame and save to CSV
df = pd.DataFrame(all_waveform_data)
df.to_csv(output_csv, index=False)

print(f"EEG waveform extraction completed. Data saved to '{output_csv}'.")