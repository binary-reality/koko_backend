import subprocess
import sys
import os
import json
import numpy as np

def call_script(script_name, args):
    try:
        subprocess.run([sys.executable, script_name] + args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")
        sys.exit(1)



def analyze_tones(json_file_path, accents):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    freq_array = np.array(data['freq'],dtype=float)
    time_array = np.array(data['time'],dtype=float)
    start_time = float(data['startTime'])  # 确保时间是浮点数
    end_time = float(data['endTime'])      # 确保时间是浮点数

    # Calculate intervals
    ac_length = len(accents)
    interval = (end_time - start_time) / ac_length
    start_points = np.arange(start_time, end_time, interval)
    end_points = start_points + interval

    mean_freqs = []
    for i in range(ac_length):
        # Mask for the current interval
        mask = (time_array >= start_points[i]) & (time_array < end_points[i])
        # Frequencies for the current interval
        current_freqs = freq_array[mask]
        # Mean frequency excluding negative values (which might be invalid)
        mean_freq = current_freqs[current_freqs >= 0].mean() if any(current_freqs >= 0) else -1
        mean_freqs.append(mean_freq)

    word_res = []
    delta_freq = 5  # 假设的频率变化阈值

    # Determine the accents based on the mean frequencies and given conditions
    for i, accent in enumerate(accents):
        if accent == 0:
            if i == 0 or mean_freqs[i] + delta_freq < min(mean_freqs[:i]):
                word_res.append(0)
            else:
                word_res.append(1)
        elif accent == 1:
            if i == 0 or mean_freqs[i] > mean_freqs[0] + delta_freq:
                word_res.append(1)
            else:
                word_res.append(0)
        elif accent == 2:  # accent == "2"
            word_res.append(2)

    return word_res


# Example usage:






# ...（其它函数不变）...

# def main(audio_input, json_input):
def main(audio_input, accents):
    # 提取文件名（无扩展名）并为wav文件设置新的文件路径
    file_path_without_extension, _ = os.path.splitext(audio_input)
    wav_output = file_path_without_extension + '.wav'

    # 首先调用 audio_trans2wav.py 来转换音频文件到 WAV 格式
    call_script('./mine/audio_trans2wav.py', [audio_input, wav_output])

    # 接下来调用 get_freq.py 来提取频率信息到 JSON 文件
    call_script('./mine/get_freq.py', [wav_output])

    # 最后调用 smooth.py 来平滑数据，并将结果保存在同一 JSON 文件中
    call_script('./mine/smooth.py', [wav_output.replace('.wav', '.json')])

    # # 从 JSON 输入文件读取accents
    # with open(json_input, 'r') as file:
    #     data = json.load(file)
    #     accents = data['accents']

    # 分析音调
    result = analyze_tones(wav_output.replace('.wav', '.json'), accents)

    return result
    # # 输出文件的路径是输入文件路径后加上'1'
    # json_output = json_input.replace('.json', '1.json')

    # # 将结果写入 JSON 输出文件
    # with open(json_output, 'w') as file:
    #     json.dump({'results': result}, file, indent=4)

    # print(f"Analysis results written to {json_output}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python final.py audio_input json_input")
        sys.exit(1)

    audio_input = sys.argv[1]
    json_input = sys.argv[2]

    main(audio_input, json_input)

