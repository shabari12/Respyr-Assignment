import cv2
import numpy as np
from pdf2image import convert_from_path

def extract_eeg_waveform(pdf_path):
    images = convert_from_path(pdf_path, dpi=300)
    combined_amplitude = []  

    for i, img in enumerate(images):
  
        img_cv = np.array(img)
        img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)

        
        _, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
        edges = cv2.Canny(thresh, 50, 150)  

      
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        waveform_points = []
        for cnt in contours:
            for point in cnt:
                x, y = point[0]  
                waveform_points.append((x, y))

       
        waveform_points = sorted(waveform_points, key=lambda p: p[0])

      
        if waveform_points:
            waveform_data = np.array(waveform_points)
            time_series = waveform_data[:, 0]  
            amplitude_series = waveform_data[:, 1]  

           
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
        combined_amplitude = np.nanmean(np.array(combined_amplitude), axis=0)  
    else:
        combined_amplitude = [np.nan] * 9  

    return {
        "PDF_Name": pdf_path,
        **{f"TimeRange_{j+1}": combined_amplitude[j] for j in range(len(combined_amplitude))}
    }