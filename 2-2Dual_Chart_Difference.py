import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import neurokit2 as nk

# Load ECG data
data = pd.read_excel("data.xlsx", index_col=0, header=0, usecols='A:B', skiprows=1)
ecg_array = data["ECG"].to_numpy()
sampling_rate = 200  # Each data point represents 0.005 seconds

# Find peaks using scipy's find_peaks
find_peaks_results, _ = scipy.signal.find_peaks(ecg_array, height=(4.55, 4.95), distance=130)

# Find peaks using neurokit2
neurokit_peaks_results = nk.ecg_findpeaks(ecg_array, sampling_rate=sampling_rate)['ECG_R_Peaks']

# Heart rate calculation for each method
def calculate_hr(peaks):
    intervals = np.diff(peaks) * 0.005  # interval in seconds
    heart_rate = 60 / intervals  # bpm calculation
    return heart_rate, np.mean(heart_rate)

hr_find_peaks, avg_hr_find_peaks = calculate_hr(find_peaks_results)
hr_neurokit, avg_hr_neurokit = calculate_hr(neurokit_peaks_results)

# Plotting comparison
plt.figure(figsize=(15, 6))
plt.plot(hr_find_peaks, label=f'find_peaks HR (avg: {avg_hr_find_peaks:.2f} BPM)', marker='x')
plt.plot(hr_neurokit, label=f'Neurokit2 HR (avg: {avg_hr_neurokit:.2f} BPM)', marker='o')
plt.xlabel('Beat number')
plt.ylabel('Heart Rate (BPM)')
plt.title('Heart Rate Comparison Between find_peaks and Neurokit2')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
