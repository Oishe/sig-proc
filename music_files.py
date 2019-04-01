#%%
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Imports dictionary with all info
db_files = dict()
with open('db_files.pickle', 'rb') as handle:
    db_files = pickle.load(handle)


# sorting through to select the csv files I want
# music files of choice from Oishe with songID 2
# CHANGE TO PICK MUSIC OR SIMON
user = 'Oishe Farhan'
music_files = dict()
for file_name, file_data in db_files.items():
    if file_data['activity'] == 'Music':
        if file_data['user_name'] == user:
            if file_data['songId'] == 2:
                music_files[file_name] = file_data

eeg_data = []
# [[[tp9], [af7], [af8], [tp10]], ...]

# populating from csv files
for file_name in music_files:
    rawdf = pd.read_csv('recordings/'+file_name)
    eeg_data.append([rawdf['TP9'], rawdf['AF7'], rawdf['AF8'], rawdf['TP10']])

min_size = len(eeg_data[0][0])
# truncating all csv files to smallest size
for recording in eeg_data:
    for electrode in recording:
        electrode_size = len(electrode)
        if electrode_size < min_size:
            min_size = electrode_size


# Creating average across same songs
# Known in the EEG world as an Event Related Potential (ERP)

# WE SHOULD BE CREATING AVERAGE OVER MUSIC vs. AVERAGE OVER SIMON
# MY WORRY IS THAT EACH INDIVIDUAL MUSIC EEG MIGHT HAVE DIFFERENT CHARACTERISTICS
zeros = np.zeros(min_size)
average = np.array([zeros, zeros, zeros, zeros])
recording_size = len(eeg_data)

for r, recording in enumerate(eeg_data):
    for e, electrode in enumerate(recording):
        # linear interpolation for NaN in data
        mask = np.isnan(electrode)
        electrode[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), electrode[~mask])
        # averaging recordings
        average[e] += (1/recording_size) * electrode[0:min_size]


print('done')

#%%
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


#%%
average = butter_bandpass_filter(average, 3, 30, 256, 5)

#%%

# THE FOLLOWING DOESN'T WORK
# HAVEN'T AVERAGED ACROSS ALL 4 electrodes
# NEED TO PLOT FFTS AND COMPARE FFT PLOTS

from scipy.fftpack import fft
# Number of sample points
N = len(average[0])
# sample spacing
fs = 256.0
T = 1.0 / fs

yf = fft(average[0])
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.xlim((1,50))
plt.grid()
plt.show()

#%%
