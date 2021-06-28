Sync Mic recorded audio with video
===================================

Automatically sync mic recorded audio with a video files. Useful for when you need to replace low quality audio of a video recording with a higher quality simultaneously recorded audio. This project generally follows [this guide](http://www.dsg-bielefeld.de/dsg_wp/wp-content/uploads/2014/10/video_syncing_fun.pdf) but instead trims audio and video to an initial clap event, then replaces the video audio with the recorded mic audio file. 


## Step-by-step guide
-------------------

Getting set up
--------------

All of the software used to generate stimuli are open-source and free: 

1. Install [ffmpeg](https://ffmpeg.org/download.html), I found [this guide useful for windows](https://www.wikihow.com/Install-FFmpeg-on-Windows) although note that with the 2021 release of Praat you use slightly different code to execute Praat from the command line in windows (no need for praatcon.exe). 
2. Install [Praat](https://www.fon.hum.uva.nl/praat/download_win.html) once you have downloaded and extracted the Praat.exe file add it to your Program Files directory.
3. To automate the recording process we presented to-be-read sentences to the human speaker via [psychopy](https://psychopy.org/), this was not necissary but it meant we could present the clap event and cue to speak with systematic timing, if you want to use that part of the protocol you will need to download psychopy.

Recording stimuli
-----------------------

The files we used for recording stimuli can be found in "recording_materials":

*	clap.wav - a wav file to generate the same clap on each recording
*   recording_guide.psyexp - a psychopy experiment file to guide the timing of recordings, cues the researcher to start audio recoring then video recording then shows the sentence to be read. A countdown is presented in advance of th 200ms clap event, 1 second following onset of the clap the speaker is cued to "speak". There is then a period where the researcher can check the recordings and choose whether to re-record or move on to the next sentence. 
*   Sentence_keyword_check.xlsx - a list of sentences to be spoken

Note that these files are intended only to guide timing, video and audio were (by us) recorded independantly of psychopy. Audio was recorded via [audacity](https://www.audacityteam.org/) and video was recorded using a phone (A Huawei P30 lite). 

Processing stimuli
-------------------
To allign our high quility audio recording with our video, we detect an onset event in the audio of the video and allign that with an audio event in our high quality recording. First, extract the audio from videos using **audio_from_vid.py**, make sure you have a subfolder called "audio_only" where the wav files will be stored. 


Extracting audio onset times
-----------------------
The next step is to extract the audio-onset times for both the video audio and mic recordings. For this we use [Praat](https://praat.en.softonic.com/).

1. Launch the Praat app either from program files [or from command line](https://www.fon.hum.uva.nl/praat/manual/Scripting_6_9__Calling_from_the_command_line.html) 

```
> "C:\Program Files\Praat.exe"
```

2. Select to open a script within praat and open `getOnsetBatch.praat`

<img src="/screenshots/praat-openscript.png" width="50%"/>

3. Select *Run > Run*

<img src="/screenshots/Praatrun.png" width="50%"/>

4. Add path to files to be processed as well as the desired output.txt name. Select OK. You should now find that output file in your working directory. 

<img src="/screenshots/Praat_info_gui.png" width="50%"/>

This will have written a list of dictionaries that we can read in python. You will want to run this script twice, once for video audio and once for mic recorded audio - producing 2 .txt files (i.e. "video_onsets.txt" and "mic_onsets.txt")

Trim audio and video files to start at sound onset
-----------------------
Once we know the onset of the sound event in each file, we can trim the audio and video files to start at that event, this can be run using **trim_files.py** currently this script expects two .txt files to exist in your current working directory "video_onsets.txt" and "mic_onsets.txt". It will then output the trimmed mic recordings and video recordings. 

Replace video audio with high quality recording
-----------------------
This is also completed in **trim_files.py**:

```
video_files = glob('videos\\trimmed\\*mp4')
audio_files = glob('audio\\trimmed\\*wav')
video_outpath = "videos\\audio_replaced\\"

for i, video in enumerate(video_files):
    # replace the audio of the video with the high quality mic recording
    out_name = video_outpath + video.split("\\")[2].split(".")[0] + "_micaudio.mp4"
    command = " ffmpeg -i {0} -i {1} -c:v copy -map 0:v:0 -map 1:a:0 {2}".format(video, audio_files[i], out_name)
    print(command)
    os.system(command)
```
The corresponding final files are stored to `videos\\audio_replaced` and there you have it! video recordings with high quality mic audio!



