
Settup

Required Folder structure:

music/ (folder for all song files, .wav only) 
temp/ (required for intermediate video generation)
out/ (output folder)
titles/ (input videos that are LONG - only for long intro /outro songs, .mp4 only)
videos/ (all other input videos, .mp4 only)
MusicVideoGenerator.py
*.py

INSTALL DEPENDENCIES FROM A CONDA ENVIRONMENT (strongly reccomended)

# make and  activate new conda environment

conda create -n [myEnv]
conda activate [myEnv]

# navigate to the MusicVideoGenerator folder then run

conda install --file requirements1.txt
pip install -r requirements2.txt

USEAGE:

MusicVideoGenerator.py -songName [song.wav] -bpm [int] --output [outputPrefix] --dynamic [True/False]


FAQS:

What does it do?

- This program cleverly assembles your previously downloaded scaffold videos into a tempo synced music video based on a provided input song and bpm

How does is do it?

1. Analyses a .wav file (located in music/)
2. Generates 3 seperate tempo and dynamically synced music videos out of random .mp4 videos located in videos/
3. Combines them into one video located in output/ 

What does "dyamically synced" mean?

- Louder sections of your input song have a higher chance of faster / more intense visuals and vice versa

What does it not do?

- Generate music videos from thin air

Where can I find sample videos to use?

- https://www.pexels.com/



