import os
from glob import glob
import ast

onset_list = glob('*txt')

for fileList in onset_list:
    # read in the txt file as a literal list of dicts
    fileInfoList = []
    with open(fileList, "r") as inFile:
        fileInfoList = ast.literal_eval(inFile.read())

    for file in fileInfoList:
        if not isinstance(file, list):
            if 'video' in fileList:
                in_name = "videos\\" + file['soundFile'].split('.')[0]+'.mp4'
                out_name = 'videos\\trimmed\\' + file['soundFile'].split('.')[0] + '.mp4'
            elif 'mic' in fileList:
                in_name = "audio\\" + file['soundFile'].split('.')[0] + '.wav'
                out_name = 'audio\\trimmed\\' + file['soundFile'].split('.')[0] + '.wav'
            else:
                ValueError('Looking for txt files that correspond to either video or mic recordings - make sure the word "video" or "mic" are in filenames')

            clip_start = file['onset']# onset of clap event
            clip_dur = 6 # assuming 3 second duration for all files

            command = "ffmpeg -i {0} -ss {1} -t {2} {3}".format(in_name,
                                                                str(clip_start),
                                                                str(clip_dur),
                                                                out_name)
            os.system(command)

video_files = glob('videos\\trimmed\\*mp4')
audio_files = glob('audio\\trimmed\\*wav')
video_outpath = "videos\\audio_replaced\\"

for i, video in enumerate(video_files):
    # replace the audio of the video with the high quality mic recording
    out_name = video_outpath + video.split("\\")[2].split(".")[0] + "_micaudio.mp4"
    command = " ffmpeg -i {0} -i {1} -c:v copy -map 0:v:0 -map 1:a:0 {2}".format(video, audio_files[i], out_name)
    print(command)
    os.system(command)



