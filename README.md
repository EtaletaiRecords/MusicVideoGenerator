# Music Video Generator
Cleverly assembles audio and video clips into a tempo-synced music video.

# 💡 SET UP

## Make sure you have Python ^3.9 with Conda

## Required Files

#### music/ (folder for all song files, .wav only, no spaces in the name) 
#### titles/ (input videos that are LONG - only for long intro /outro songs, .mp4 only)
#### videos/ (all other input videos, .mp4 only)
#### MusicVideoGenerator.py, etc

## Make and activate new conda environment

```conda create -n mvg```
```conda activate mvg```

## Install Conda and PIP requirements.

```conda install --file Requirements1.txt```
```pip3 install -r Requirements2.txt```

# 🟢 USEAGE:
 
```python3 MusicVideoGenerator.py -songName [song.wav] -bpm [int] --output [outputPrefix] --dynamic [True/False]```

---



based on code by: richardpienaar1@gmail.com
