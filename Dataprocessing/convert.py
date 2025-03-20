import os
import cv2
import numpy as np
import pandas as pd
from pdf2image import convert_from_path


folder_path = "Emotional_disorder"
output_csv = "Final_Data.csv"
poppler_path = r"C:\poppler-24.08.0\Library\bin"  


def extract_eeg_waveform(pdf_path):
    images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    combined_amplitude = []  

    for i, img in enumerate(images):
        print(f"Processing {pdf_path} - Page {i+1}...")


        img_cv = np.array(img)
        img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)

        
        _, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
        edges = cv2.Canny(thresh, 50, 150)  

        # Find Contours (Extract EEG Waveforms)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        waveform_points = []
        for cnt in contours:
            for point in cnt:
                x, y = point[0]  
                waveform_points.append((x, y))


        waveform_points = sorted(waveform_points, key=lambda p: p[0])

   
        if waveform_points:
            waveform_data = np.array(waveform_points)
            time_series = waveform_data[:, 0]  # X-axis (time)
            amplitude_series = waveform_data[:, 1]  # Y-axis (EEG amplitude)

           
            amplitude_series = (amplitude_series - np.min(amplitude_series)) / (np.max(amplitude_series) - np.min(amplitude_series))

     
            bins = np.linspace(time_series.min(), time_series.max(), num=10)
            binned_data = []

            for j in range(len(bins) - 1):
                bin_mask = (time_series >= bins[j]) & (time_series < bins[j + 1])
                if np.any(bin_mask):
                    avg_amplitude = np.mean(amplitude_series[bin_mask])
                    binned_data.append(avg_amplitude)
                else:
                    binned_data.append(np.nan)  

  
            combined_amplitude.append(binned_data)


    if combined_amplitude:
        combined_amplitude = np.nanmean(np.array(combined_amplitude), axis=0)  # Averaging across pages
    else:
        combined_amplitude = [np.nan] * 9  
    return {
        "PDF_Name": os.path.basename(pdf_path),
        **{f"TimeRange_{j+1}": combined_amplitude[j] for j in range(len(combined_amplitude))}
    }


all_waveform_data = []
for file in os.listdir(folder_path):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, file)
        eeg_data = extract_eeg_waveform(pdf_path)
        all_waveform_data.append(eeg_data)


df = pd.DataFrame(all_waveform_data)
df.to_csv(output_csv, index=False)

print(f"EEG waveform extraction completed. Data saved to '{output_csv}'.")
