import numpy as np
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
import time

# Load ECG data from Excel file
sampling_rate = 200  # Sampling rate in Hz (200 samples/sec)
window_size = 2 * sampling_rate  # 2-second window for memory efficiency
step_size = 10  # Number of new samples processed in each iteration

data = pd.read_excel("data.xlsx", index_col=0, header=0, usecols='A:B', skiprows=1)
ecg_data = data["ECG"].to_numpy()

# Initialize buffers and lists to store real-time data
ecg_buffer = np.zeros(window_size)
hr_values = []
time_stamps = []

# Prepare dynamic plots
plt.ion()
fig, (ax_ecg, ax_hr) = plt.subplots(2, 1, figsize=(12, 8))

# Function to calculate heart rate with outlier filtering
def calculate_hr(ecg_segment, sampling_rate):
    peaks_dict = nk.ecg_findpeaks(ecg_segment, sampling_rate=sampling_rate)
    peaks = peaks_dict['ECG_R_Peaks']
    if len(peaks) > 1:
        rr_intervals = np.diff(peaks) / sampling_rate
        if len(rr_intervals) > 0:
            mean_rr = np.mean(rr_intervals)
            if mean_rr > 0:
                hr_current = 60 / mean_rr
                if 40 < hr_current < 180:
                    return hr_current, peaks
    return None, []

# Real-time simulation loop
for i in range(0, len(ecg_data) - step_size, step_size):
    # Update ECG buffer with new incoming data
    new_data = ecg_data[i:i+step_size]
    ecg_buffer = np.roll(ecg_buffer, -len(new_data))
    ecg_buffer[-len(new_data):] = new_data

    # Calculate HR from ECG segment
    hr_current, peaks = calculate_hr(ecg_buffer, sampling_rate)
    current_time = i / sampling_rate

    if hr_current is not None:
        hr_values.append(hr_current)
        time_stamps.append(current_time)

    # Smooth HR values using moving average
    if len(hr_values) > 5:
        hr_smoothed = np.convolve(hr_values, np.ones(5)/5, mode='valid')
        time_smoothed = time_stamps[4:]
    else:
        hr_smoothed = hr_values
        time_smoothed = time_stamps

    # Update ECG plot dynamically
    ax_ecg.clear()
    ax_ecg.plot(ecg_buffer, label="ECG Signal")
    if len(peaks) > 0:
        ax_ecg.plot(peaks, ecg_buffer[peaks], 'rx', label="Detected Peaks")
    ax_ecg.set_title(f"Real-Time ECG Signal - HR: {hr_current:.2f} BPM" if hr_current else "Real-Time ECG Signal")
    ax_ecg.set_xlabel("Samples (Last 2 seconds)")
    ax_ecg.set_ylabel("Amplitude")
    ax_ecg.legend()
    ax_ecg.grid(True)

    # Update HR plot dynamically with smoothed data
    ax_hr.clear()
    ax_hr.plot(time_smoothed, hr_smoothed, linestyle='-', color='blue')
    ax_hr.set_title("Real-Time Heart Rate")
    ax_hr.set_xlabel("Time (seconds)")
    ax_hr.set_ylabel("Heart Rate (BPM)")
    ax_hr.grid(True)

    plt.tight_layout()
    plt.pause(0.01)

    # Simulate real-time delay
    time.sleep(0.05)

plt.ioff()
plt.show()
