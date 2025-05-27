import pandas as pd
import matplotlib.pyplot as plt
import neurokit2 as nk
# next line: specifies the file path, sets the first column as the index, considers the first row as column names, skips the first row
data = pd.read_excel("D:\Files\daneshgah\mabani\data.xlsx", index_col=0, header=0, usecols='A:B', skiprows=1)
data["ECG"].plot()
plt.show()
data["ECG"].plot()
array = data["ECG"].to_numpy() # converts a range of the ECG column into a NumPy array
sampling_rate = 200 # Since each data point is 5ms apart, the sampling rate is 200 Hz (1 / 0.005s), meaning 200 samples are recorded per second.
# next line: This line detects R-peaks in the ECG signal using NeuroKit2, based on the given sampling rate.
peaks = nk.ecg_findpeaks(array, sampling_rate = sampling_rate) 
r_wave = peaks['ECG_R_Peaks']
r_wave = list(map(int, r_wave))
hb = [0] * (len(r_wave)-1)
for i in range(len(r_wave)-1):
    # next line: calculates the heart rate for each pair of peaks(bpm), the time between each data point is 0.005 s
    hb[i] = (60/((r_wave[i+1]-r_wave[i])*0.005)) 
Heart_beat = 60/((r_wave[(len(r_wave)-1)] - r_wave[0]) / (len(r_wave)-1) * 0.005) # calculate the average heart rate over the entire r_wave list
plt.title("ECG")
plt.plot(r_wave, array[r_wave], "X") # specifies peaks with the marker 'X'
plt.show()
plt.title("Heart beat: %3.2f bpm" %(Heart_beat))
plt.plot(hb)
plt.show()