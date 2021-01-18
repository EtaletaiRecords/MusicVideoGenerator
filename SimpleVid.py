from GenerateTimeStamps import *
from moviepy.editor import *
import random, math, os, sys

def preload():
    '''
    preloads all video files once
    '''
    
    videosList = []

    print("Preloading")
    for vid in os.listdir("videos/"):
        videosList.append(VideoFileClip("videos/" + vid, target_resolution=(720,1280)))
    
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
    firstDB = start # used to show progress
    
    print("Generating video")
    while start < finish:
        
        # switch up video rate every 4 bars
        if (start - firstDB) % (lengthOfABeat * 16) == 0:
            new4BarBlock = True

        if new4BarBlock:
            i = random.choice([1,4,4,4,8,8,16,16,16]) # random rate of change of the videos
            
        print(str(start / finish * 100) + "%/ rendered")

        video = random.choice(videosList)
        videostart = random.randint(0, math.floor(video.duration - 3)) # random video portion
        videos.append(video.subclip(videostart,videostart + lengthOfABeat * i))
    
        start += (lengthOfABeat * i)
        new4BarBlock = False
    
    # Ambient outro
    if start < duration:
        videos.append(VideoFileClip("titles/"+random.choice([x for x in os.listdir("titles/")])).subclip(0,duration-start).fx( vfx.fadeout, duration=clip.duration/2))

    final_clip = concatenate_videoclips(videos,method="compose")
    
    # write video
    final_clip.write_videofile(filename="temp/"+str(filename)+str(output)+".mp4",preset="ultrafast",threads=4,audio=False)


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
