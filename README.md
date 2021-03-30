# Examples:

Forthcoming 03/21 on HATE LAB: https://www.youtube.com/channel/UCLXM6lFu1s7MjInzUk5bfNA

# 💡 SET UP

## Required Folder structure:

#### music/ (folder for all song files, .wav only, no spaces in the name) 
#### temp/ (required for intermediate video generation)
#### out/ (output folder)
#### titles/ (input videos that are LONG - only for long intro /outro songs, .mp4 only)
#### videos/ (all other input videos, .mp4 only)
#### MusicVideoGenerator.py
#### *.py

## ⚫ INSTALL DEPENDENCIES FROM A CONDA ENVIRONMENT (strongly reccommended)

### make and activate new conda environment

conda create -n [myEnv]
conda activate [myEnv]

### navigate to the MusicVideoGenerator folder then run

conda install --file requirements1.txt
pip install -r requirements2.txt

# 🟢 USEAGE:
 
> python MusicVideoGenerator.py -songName [song.wav] -bpm [int] --output [outputPrefix] --dynamic [True/False]

# 🛑 FAQS:

## What does it do?

- This program cleverly assembles your previously downloaded scaffold videos into a tempo synced music video based on a provided input song and bpm

## How does it do it?

1. Analyses a .wav file (located in music/)
2. Generates 3 seperate tempo and dynamically synced music videos out of random .mp4 videos located in videos/
3. Combines them through the use of overlay FX into one video located in output/ 
4. Applies chroma shifting to the final product to make the videos bleed into eachother for contrast.  

## What does "dyamically synced" mean?

- Louder sections of your input song have a higher chance of faster / more intense visuals and vice versa.

## What does it not do?

- Generate music videos from thin air.

## Where can I find sample videos to use?

Royalty Free:
- https://www.pexels.com/
- https://pixabay.com/

There are also a small selection of videos in this repo to allow you to test the program. These are from pexels.  

## What is the ouput format?

- Video is 720p, audio is 256kps AAC

## How fast is my song? What is my songs BPM?

- https://www.beatsperminuteonline.com/

## Richard, this thing is so slow it's making my head spin. I could do it way faster in Generic X movie editing software!

- Look, fair. My counter to that is you can leave and eat a sandwhich, call a loved one etc rather than have to sit through the the video editing process.
- You may have luck speeding it up by using smaller pool of scaffold videos, or using the --dynamic False flag if you only need tempo synced visuals. 
- My runtimes are generally ~60 - 70 minutes per super loud song (16gb RAM). More RAM allows more videos to be loaded into memory and speeds up the process significantly. I acknowlege that this is nowhere near optimal performance, this is my first proper project. I am more than happy to collaborate with this project going forward.   

## I've used this to make videos that now have billions of hits, how can I credit you?

- A public link to this repo in the description would be appreciated :) 

## I run a company looking for a programmer like you, would you be interested in a position?

- Please get in contact: richardpienaar1@gmail.com
