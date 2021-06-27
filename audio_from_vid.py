import os
from glob import glob
import subprocess


# Export the audio track of each video

# Find all mp4 files in current directory, put all filenames in a list
clip_list = glob('videos\*mp4')

# For each file in file list, cross-correlate its audio with ref.wav to find the offset (uses Praat).
for clip in clip_list:
    #clip.split("\\")[1]
    clipfile = 'videos\\audio_only\\' + clip.split("\\")[1].split(".")[0]+".wav"
    command = "ffmpeg -i {0} -map 0:1 -acodec pcm_s16le -ac 2 {1}".format(clip,
                                                                          clipfile)
    os.system(command)

    print('Exporting audio from video file: ', clipfile)
