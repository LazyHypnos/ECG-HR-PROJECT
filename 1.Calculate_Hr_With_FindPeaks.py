import pandas as pd
import matplotlib.pyplot as plt
import scipy
n = 1080 #specify from which index the graph should start
m = 50000 #specify to which index the graph should be drawn
#next line: specifies the file path, sets the first column as the index, considers the first row as column names, skips the first row
data = pd.read_excel("D:\Files\daneshgah\mabani\data.xlsx", index_col=0, header=0, usecols='A:B', skiprows=1)
data["ECG"][n:m].plot()
array = data["ECG"][n:m].to_numpy() #converts a range of the ECG column into a NumPy array
#next line: detects the R-wave peaks between 4.55 and 4.95 and sets a minimum distance of 130 data points
r_wave, metadata = scipy.signal.find_peaks(array, height = (4.55, 4.95), distance = 130)
r_wave2 = r_wave #storing the x values before changing them since we don't want y values to change
r_wave = list(map(int, r_wave))
for i in range(len(r_wave)):
    r_wave[i] += n #modifies the element in place we want
hb = [0] * (len(r_wave)-1)
for i in range(len(r_wave)-1):
    #next line: calculates the heart rate for each pair of peaks(bpm), the time between each data point is 0.005 s
    hb[i] = (60/((r_wave[i+1]-r_wave[i])*0.005)) 
Heart_beat = 60/((r_wave[(len(r_wave)-1)] - r_wave[0]) / (len(r_wave)-1) * 0.005) #calculate the average heart rate over the entire r_wave list
plt.title("ECG")
plt.plot(r_wave, array[r_wave2], "X") #specifies peaks with the marker 'X'
plt.show()
plt.title("Heart beat: %3.2f bpm" %(Heart_beat))
plt.plot(hb)
plt.show()