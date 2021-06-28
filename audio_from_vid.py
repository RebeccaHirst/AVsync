import os
from glob import glob
import subprocess


# Export the audio track of each video

# Find all mp4 files in current directory, put all filenames in a list
clip_list = glob('recording_materials\\video\\41-80-mask\\*mp4')
print(clip_list)
# For each file in file list, cross-correlate its audio with ref.wav to find the offset (uses Praat).
for clip in clip_list:
    #clip.split("\\")[1]
    clipfile = 'recording_materials\\video\\41-80-mask\\audio_only\\' + clip.split("\\")[3].split(".")[0]+".wav"
    command = "ffmpeg -i {0} -map 0:1 -acodec pcm_s16le -ac 2 {1}".format(clip,
                                                                          clipfile)
    os.system(command)

    print('Exporting audio from video file: ', clipfile)
