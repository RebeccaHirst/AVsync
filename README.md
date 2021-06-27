Sync Mic recorded audio with video
===================================

Automatically sync mic recorded audio with a video files. Useful for when you need to replace low quality audio of a video recording with a higher quality simultaneously recorded audio. This project generally follows [this guide](http://www.dsg-bielefeld.de/dsg_wp/wp-content/uploads/2014/10/video_syncing_fun.pdf). 


## Step-by-step guide
-------------------

Getting set up
--------------
1. Install [ffmpeg](https://ffmpeg.org/download.html), I found [this guide useful for windows](https://www.wikihow.com/Install-FFmpeg-on-Windows) although note that with the 2021 release of Praat you use slightly different code to execute Praat from the command line in windows (no need for praatcon.exe). 
2. Install [Praat](https://www.fon.hum.uva.nl/praat/download_win.html) once you have downloaded and extracted the Praat.exe file add it to your Program Files directory.

Extracting video audio
-----------------------
To allign our high quility audio recording with out video, we detect an onset event in the audio of the video and allign that with an audio event in our high quality recording. The first step is therefore to extract the audio of our videos and store them. This can be done by running **audio_from_vid.py**. 


Extracting audio onset times
-----------------------
The next step is to extract the audio-onset times for our video audio and mic recordings. For this we use Praat.

1. Launch the Praat app either from program files [or from command line (https://www.fon.hum.uva.nl/praat/manual/Scripting_6_9__Calling_from_the_command_line.html) 

```
> "C:\Program Files\Praat.exe"
```

2. Select to open a script within praat and open `getOnsetBatch.praat`

<img src="/screenshots/praat-openscript.png" width="50%"/>

3. Select *Run > Run*

<img src="/screenshots/Praatrun.png" width="50%"/>

4. Add path to files to be processed as well as the desired output.txt name. Select OK. You should now find that output file in your working directory. 

<img src="/screenshots/Praat_info_gui.png" width="50%"/>

This will have written a list of dictionaries that we can read in python. You will want to run this script twice, once fir video audio and once for mic recorded audio - producing 2 .txt files (i.e. "video_onsets.txt" and "mic_onsets.txt")

Trim audio and video files to start at sound onset
-----------------------
Once we know the onset of the sound event in each file, we can trim the audio and video files to start at that event, this can be run using **trim_files.py** currently this script expects two .txt files to exist in your current working directory "video_onsets.txt" and "mic_onsets.txt". It will then output the trimmed mic recordings and video recordings. 

Replace video audio with high quality recording
-----------------------
This is actually also completed in **trim_files.py**:

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
The corresponding final files are stored to `videos\\audio_replaced`

References:
---------------
