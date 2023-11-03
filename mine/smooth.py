import os
import sys
import json

def getSmooth(window):
    tmpSum = 0
    tmpNum = 0
    for i in range(len(window)):
        if window[i] != -1:
            tmpSum += window[i]
            tmpNum += 1
    if tmpNum == 0:
        return -1
    else:
        return tmpSum / tmpNum

def smooth_data(data, window_size):
    smoothed_data = []
    for i in range(len(data)):
        if data[i] == -1:
            smoothed_data.append(-1)
            continue
        if i < window_size:
            window = data[:i+1]
        else:
            window = data[i-window_size+1:i+1]
        smoothed_value = getSmooth(window)
        smoothed_data.append(smoothed_value)
    return smoothed_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        return

    input_file = sys.argv[1]
    output_file = input_file  # Save result in the same file

    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    freq_data = json_data.get("freq", [])
    # Convert string values to integers
    freq_data = [float(value) for value in freq_data]

    window_size = 10

    smoothed_freq = smooth_data(freq_data, window_size)
    json_data["freq"] = smoothed_freq


    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)

    print("Smoothed 'freq' data written to", output_file)

if __name__ == "__main__":
    main()
