
# ![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+) SET UP

## Required Folder structure:

#### music/ (folder for all song files, .wav only) 
#### temp/ (required for intermediate video generation)
#### out/ (output folder)
#### titles/ (input videos that are LONG - only for long intro /outro songs, .mp4 only)
#### videos/ (all other input videos, .mp4 only)
#### MusicVideoGenerator.py
#### *.py

## INSTALL DEPENDENCIES FROM A CONDA ENVIRONMENT (strongly reccommended)

### make and activate new conda environment

conda create -n [myEnv]
conda activate [myEnv]

### navigate to the MusicVideoGenerator folder then run

conda install --file requirements1.txt
pip install -r requirements2.txt

# ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) USEAGE:
 
> python MusicVideoGenerator.py -songName [song.wav] -bpm [int] --output [outputPrefix] --dynamic [True/False]

# ![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) FAQS:

## What does it do?

- This program cleverly assembles your previously downloaded scaffold videos into a tempo synced music video based on a provided input song and bpm

## How does it do it?

1. Analyses a .wav file (located in music/)
2. Generates 3 seperate tempo and dynamically synced music videos out of random .mp4 videos located in videos/
3. Combines them into one video located in output/ 

## What does "dyamically synced" mean?

- Louder sections of your input song have a higher chance of faster / more intense visuals and vice versa

## What does it not do?

- Generate music videos from thin air

## Where can I find sample videos to use?

- https://www.pexels.com/
- https://pixabay.com/

## What is the ouput format?

- 720p

## How fast is my song? What is my songs BPM?

- https://www.beatsperminuteonline.com/

## Richard, this thing is so slow it's making my head spin. I could do it way faster in Generic X movie editing software!

- Look, fair. My counter to that is you can leave and eat a sandwhich, call a loved one etc rather than have to sit through the hell hole that is the video editing process
- You may have luck speeding it up by using smaller pool of lesser resolution videos, or using the --dynamic False flag if you only need tempo synced visuals. 

## I've used this to make videos that now have billions of hits, how can I credit you?

- A public link to this repo in the description would be appreciated :) 






