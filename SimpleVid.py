from GenerateTimeStamps import *
from moviepy.editor import *

import random, math, os, sys

'''
Simple, randomized, tempo synced video generation 
'''

PERCENTS = (0,10,20,30,40,50,60,70,80,90,100)

def invert_green_blue(image):
    '''
    Inverts green and blue pixels of a clip (VideoFileClip)
    '''
    return image[:,:,[0,2,1]]

def get_closest_percent(percent):
    '''
    returns lowest passed threshold
    '''
    for p in PERCENTS:
        if percent - p < 10:
            return p

def preload():
    '''
    preloads all video files once
    '''
    
    videosList = []

    print("Preloading Videos")

    for vid in os.listdir("videos/"):
        randomiser = random.random() # seed to randomise individual videos orientation / colour to give illusion of change between videos
        if randomiser < 0.3:
            videosList.append(VideoFileClip("videos/" + vid, target_resolution=(720,1280)))
        elif randomiser < 0.6:
            videosList.append(VideoFileClip("videos/" + vid, target_resolution=(720,1280)).fl_image( invert_green_blue ))
        elif randomiser < 0.9:
            videosList.append(VideoFileClip("videos/" + vid, target_resolution=(720,1280)).fx( vfx.mirror_x ))
        else:
            videosList.append(VideoFileClip("videos/" + vid, target_resolution=(720,1280)).fl_image( invert_green_blue ).fx( vfx.mirror_y ))

    
    for vid in videosList:
        if vid.size[0] > 1280 or vid.size[1] > 720:
            print(vid.filename)
            videosList.remove(vid)
    
    return videosList


def make_subMovie(filename, bpm, videosList, output, start, finish, duration):
    '''
    Saves a simple movie synced to the provided audio file

    filename (str): filname of song (.wav)
    bpm (int / float): beats per minute tempo of the song
    videos([VideoFile, VideoFile, ..]): videos to use
    output (str) desired filename output

    start: first downbeat
    finish: last downbeat
    duration: total duration
    '''

    # time between beats
    lengthOfABeat = 1 / (bpm / 60)

    videos = []

    # black screen on start
    if start > 0 and start < 4:
        videos.append(VideoFileClip("titles/"+random.choice([x for x in os.listdir("titles/")])).subclip(0,start).fx(vfx.colorx, 0.0))
    
    # ambient intro on start
    elif start > 0:
        clip = VideoFileClip("titles/"+random.choice([x for x in os.listdir("titles/")])).subclip(0,start)
        videos.append(clip.fx( vfx.fadein, duration=clip.duration/2))

    new4BarBlock = True # outlines every 4 bars to switch up speeds
    beats = 0 # current beats rendered
    currentRenderPercent = 0 # used to print progress to console

    print("Generating video " + str(output+1))
    
    while start < finish:

        # switch up video rate every 4 bars
        if beats % 16 == 0:
            new4BarBlock = True

        if new4BarBlock:
            i = random.choice([1,4,4,4,8,8,16,16,16]) # random rate of change of the videos
            
        while True:
            try: # try / catch block to account for videos that are not long enough 
                video = random.choice(videosList)
                videostart = random.randint(0, math.floor(video.duration - lengthOfABeat * i)) # random video portion
                break
            except ValueError:
                continue
        
        videos.append(video.subclip(videostart,videostart + lengthOfABeat * i))
    
        start += (lengthOfABeat * i)
        beats += i

        # print progress to screen
        percentRendered = get_closest_percent(start / finish * 100)
        if percentRendered != currentRenderPercent:
            currentRenderPercent = percentRendered
            print(str(currentRenderPercent)+ "%/ rendered")

        new4BarBlock = False
    
    # Ambient outro
    if start < duration:
        clip = VideoFileClip("titles/"+random.choice([x for x in os.listdir("titles/")])).subclip(0,duration-start)
        videos.append(clip.fx( vfx.fadeout, duration=clip.duration/2))

    final_clip = concatenate_videoclips(videos,method="compose")
    
    if final_clip.size == (1280,720):
        # write video
        final_clip.write_videofile(filename="temp/small"+str(filename)+str(output)+".mp4",preset="ultrafast",threads=6,audio=False)
    else:
        # name output differently to denote not yet 720p
        final_clip.write_videofile(filename="temp/"+str(filename)+str(output)+".mp4",preset="ultrafast",threads=6,audio=False)

    # memory save
    for v in videos:
        v.close()
    final_clip.close()

def main(argv):

    videosList = preload()
    
    print("Analysing waveform")
    start, finish = guess_first_and_last_DownBeat("music/"+argv[0])
    duration = get_duration("music/"+argv[0])

    bpm = argv[1]

    for i in range(int(argv[2])):
        make_subMovie( argv[0], int(bpm), videosList, i, start, finish, duration)

if __name__ == "__main__":
    main(sys.argv[1:])
