import os
from glob import glob
import subprocess

# Find all mp4 files in current directory, put all filenames in a list
clip_list = glob('*mp4')

#load in the list of reference sounds (the high quiality audio)
# sound_list

# Paths for finding praat scripts and application
praat_script = "C:\\Users\\44797\\PycharmProjects\\AVsync\\crosscorrelate.praat"
praat_onset_script = "C:\\Users\\44797\\PycharmProjects\\AVsync\\getOnsetBatch.praat"
praat = "C:\\Program Files\\Praat.exe"
ref_sound= "C:\\Users\\44797\\PycharmProjects\\AVsync\\files\\testing_48000.wav"

results = []
results.append((ref_sound, 0))#the reference sound has an offset of 0

# For each file in file list, cross-correlate its audio with ref.wav to find the offset (uses Praat).
for clip in clip_list:
    clipfile = clip.split(".")[0]+".wav"
    command = "ffmpeg -i {0} -map 0:1 -acodec pcm_s16le -ac 2 {1}".format(clip,
                                                                          clipfile)
    os.system(command)

    print('Exporting audio from video file: ', clipfile)

    praat_command = '"{}" --run "{}" "{}" "{}"'.format(
        praat, praat_script, ref_sound, clipfile)

    print(praat_command)

    result = subprocess.check_output(
        praat_command, shell=True).decode("utf-16")

    print('Comparing wav files for onset discrepancies: ', ref_sound, clipfile)

    # Add all results (filename, offset) to a list, which contains one item already: (ref filename, 0)
    results.append((clip, result.split("\n")[0]))

# get the sound onset for all wav files
praat_command = '"{}" --run "{}"'.format(
    praat, praat_onset_script)
print(praat_command)
check = subprocess.check_output(
    praat_command, shell=True).decode("utf-16")
# Delete all WAV files we don't need to keep (extracted from videos)
#command = "rm *wav"
#os.system(command)

# For each item in the results list, trim the video at the given start and duration, taking into
# account the offset. The reference file will be trimmed at exactly the start time (its offset is
# zero), but each other file will be trimmed from a start that is shifted by the respective offset
for result in results:
    clip_start = 4# - this should correspond to time of clap
    clip_dur = 4#  - this should correspond to time of clap to end
    in_name = result[0]
    out_name = "trimmed_videos\\" + in_name.split(".")[0]+"_part2.mp4"
    offset = round(float(result[1]), 3)
    clip_start += offset
    print(result[1])
    print(type(result[1]))
    if result[1] != 0:# the first result has no corresponding video file at the moment - it is audio only
        command = "ffmpeg -i {0} -ss {1} -t {2} {3}".format(in_name,
                                                            str(clip_start),
                                                            str(clip_dur),
                                                            out_name)
        os.system(command)




# path to praat script
# praat_script = "C:\\Users\\44797\\PycharmProjects\\AVsync\\praat_scripts\\crosscorrelate.praat"
# praat = "C:\\Program Files\\Praat.exe"
# sound = "C:\\Users\\44797\\PycharmProjects\\AVsync\\files\\testing_48000.wav"
# sound_studio = "C:\\Users\\44797\\PycharmProjects\\AVsync\\VID_20210627_093024.wav"
# praat_command = '"{}" --run "{}" "{}" "{}"'.format(
#     praat, praat_script, sound, sound_studio)
#
# sound_offset_time = subprocess.check_output(
#     praat_command, shell=True).decode("utf-16")
#
# print(sound_offset_time)
#
# #