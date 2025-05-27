import pandas as pd
import matplotlib.pyplot as plt
import neurokit2 as nk
import scipy
data = pd.read_excel("D:\Files\daneshgah\mabani\data.xlsx", index_col=0, header=0, usecols='A:B', skiprows=1)
data["ECG"].plot()
array = data["ECG"].to_numpy() 
sampling_rate = 200 
peaks = nk.ecg_findpeaks(array, sampling_rate = sampling_rate) 
r_wave1 = peaks['ECG_R_Peaks']
r_wave1 = list(map(int, r_wave1))
r_wave, metadata = scipy.signal.find_peaks(array, height = (4.55, 4.95), distance = 130)
r_wave = list(map(int, r_wave))
plt.title("ECG")
plt.plot(r_wave1, array[r_wave1], "X") 
plt.plot(r_wave, array[r_wave], "x")
plt.show()
hb = [0] * (len(r_wave)-1)
for i in range(len(r_wave)-1):
    hb[i] = (60/((r_wave[i+1]-r_wave[i])*0.005)) 
Heart_beat = 60/((r_wave[(len(r_wave)-1)] - r_wave[0]) / (len(r_wave)-1) * 0.005) 
plt.plot(hb)
hb1 = [0] * (len(r_wave1)-1)
for i in range(len(r_wave1)-1):
    hb1[i] = (60/((r_wave1[i+1]-r_wave1[i])*0.005)) 
Heart_beat1 = 60/((r_wave1[(len(r_wave1)-1)] - r_wave1[0]) / (len(r_wave1)-1) * 0.005) 
plt.title("Heart beat: %3.2f bpm(%3.2f)" %(Heart_beat, Heart_beat1))
plt.plot(hb1)
plt.show()