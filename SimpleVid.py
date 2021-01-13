from GenerateTimeStamps import *
from moviepy.editor import *
import random, math, os, sys

# TODO: 
# - Only Works in 4/4
# - just not fast
# - load music after for increased quality

def preload():
    '''
    preloads all video files once
    '''
    
    videosList = []

    print("Preloading")
    for vid in os.listdir("videos/"):
        videosList.append(VideoFileClip("videos/" + vid, target_resolution=(720,1280)))
    
    return videosList


def make_subMovie(filename, bpm, videosList, output):
    '''
    Saves a simple movie synced to the provided audio file

    filename: filname of song (.wav)
    bpm: beats per minute tempo of the song
    videos: videos to use
    output desired filename output
    '''

    print("Analysing waveform")
    start, finish = guess_first_and_last_DownBeat("music/"+str(filename))
    duration = get_duration("music/"+str(filename))

    # time between beats
    lengthOfABeat = 1 / (bpm / 60)

    videos = []

    # black screen on start
    if start > 0 and start < 4:
        videos.append(VideoFileClip("titles/"+random.choice([x for x in os.listdir("titles/")])).subclip(0,start).fx(vfx.colorx, 0.0))
    
    # ambient intro on start
    elif start > 0:
        videos.append(VideoFileClip("titles/"+random.choice([x for x in os.listdir("titles/")])).subclip(0,start))

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
        videos.append(VideoFileClip("titles/"+random.choice([x for x in os.listdir("titles/")])).subclip(0,duration-start))

    final_clip = concatenate_videoclips(videos,method="compose")
    
    # write video
    final_clip.write_videofile(filename="temp/"+str(filename)+str(output)+".mp4",preset="ultrafast",threads=4,audio=False)


def main(argv):

    videosList = preload()

    for i in range(int(argv[2])):
        make_subMovie(argv[0],int(argv[1]),videosList,i)

if __name__ == "__main__":
    main(sys.argv[1:])
