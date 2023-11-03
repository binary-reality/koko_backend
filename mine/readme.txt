脚本以及库以及全部完成，音高分析工作完成；
运行环境:Ubuntu 20.04 python3
可能需要的库：（因为我自己之前下载过，如果按照以下部分下载了没有用的话看报错信息找库下载）
import seaborn
sudo apt update
sudo apt install ffmpeg
pip3 install pydub
运行方法：python3 final.py  your-media-path  your-json-path
后两个分别是录音文件地址和包含“accents”项的json文件地址，如果在相同文件夹下直接输入文件名即可；
脚本运行完成后会生成以下文件：
yourname.wav（如果源文件不是wav格式）
yourname.json（初次分析和平滑后的语音图）
accept.json（接收到的json包）
accept1.json（返回的包）
如果不想跑脚本，调用final.py中的main也可，参数仍然是 your-media-path ，your-json-path
返回结果为accept1.json，格式为：“accents":[0,1,2,1]类似。
