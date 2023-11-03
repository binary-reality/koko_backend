from pydub import AudioSegment
import sys


def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format='wav')

# 指定输入文件和输出文件的路径
input_file = sys.argv[1]
output_file = sys.argv[2]

# 调用函数进行转换
convert_to_wav(input_file, output_file)