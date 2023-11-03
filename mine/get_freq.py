import parselmouth
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import math

sns.set() # Use seaborn's default style to make attractive graphs

# Plot nice figures using Python's "standard" matplotlib library
# snd = parselmouth.Sound("~/test/1オレンジジュースください.wav")
snd = parselmouth.Sound(sys.argv[1]) # 文件读入

dic = {
    "time":[],
    "freq":[],
}

def draw_pitch(pitch):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan

    dic["time"] = pitch.xs().tolist()
    dic["freq"] = pitch_values.tolist()

    for i in range(len(dic["freq"])):
        if math.isnan(dic["freq"][i]):
            dic["freq"][i] = -1
        dic["freq"][i] = "{:.2f}".format(dic["freq"][i])
    
    for i in range(len(dic["time"])):
        dic["time"][i] = "{:.2f}".format(dic["time"][i])

    for i in range(len(dic["freq"])):
        if float(dic["freq"][i]) >= 0:
            dic["startTime"] = dic["time"][i]
            break
    for i in range(len(dic["freq"]) - 1, -1, -1):
        if float(dic["freq"][i]) >= 0:
            dic["endTime"] = dic["time"][i]
            break
    # print(pitch_values)
    # print(pitch.xs())
    # plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    # plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    # plt.grid(False)
    # plt.ylim(0, pitch.ceiling)
    # plt.ylabel("fundamental frequency [Hz]")

pitch = snd.to_pitch()
# If desired, pre-emphasize the sound fragment before calculating the spectrogram
pre_emphasized_snd = snd.copy()
pre_emphasized_snd.pre_emphasize()
spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
# plt.figure()
# draw_spectrogram(spectrogram)
# plt.twinx()
draw_pitch(pitch)
# plt.xlim([snd.xmin, snd.xmax])
# plt.show() # or plt.savefig("spectrogram_0.03.pdf")

file_path = sys.argv[1]
file_path = file_path[:-4]

with open(file_path + ".json","w") as f:
# with open("test" + ".json","w") as f:
    json.dump(dic, f)
# print(dic)