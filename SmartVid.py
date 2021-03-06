from GenerateTimeStamps import *
from moviepy.editor import *
from SimpleVid import preload, get_closest_percent
import random, math, os, sys

'''
Dynamic video generation - Intense sections of music will have faster visuals
'''

HIGH_INTENSITY = [1,1,1,4,4,4]
MEDIUM_INTENSITY = [4,4,4,4,8,8,8,16]
LOW_INTENSITY = [8,8,8,16,16,16,16]

def make_subMovie(filename, bpm, videosList, output, start, finish, duration, intensities):
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
    current4BarBlock = 0 # current 4 bar block to pull intensities from
    fadeOut = False # used to fade out before a drop
    beats = 0 # current beats rendered

    currentRenderPercent = 0 # used to print progress to console
    
    print("Generating video " + str(output+1))

    while beats < (len(intensities) * 16):

        # switch up video rate every 4 bars
        if beats % 16 == 0:
            new4BarBlock = True

        if new4BarBlock:
            # DYNAMIC video selection
            if intensities[current4BarBlock] == "High":
                if current4BarBlock > 0 and intensities[current4BarBlock - 1] == "Low": # If the previous section was low and this one is high, make it speedy by defualt
                    i = 1
                else:
                    i = random.choice(HIGH_INTENSITY) 

            elif intensities[current4BarBlock] == "Medium":
                i = random.choice(MEDIUM_INTENSITY)
            else: 
                try:
                    if intensities[current4BarBlock + 1] == "High": # check next section is a "drop"
                        i = 16
                        fadeOut = True
                    else:
                        i = random.choice(LOW_INTENSITY)
                except KeyError:
                    i = random.choice(LOW_INTENSITY)
                
            current4BarBlock += 1


        while True:
            try: # try / catch block to account for videos that are not long enough 
                video = random.choice(videosList)
                videostart = random.randint(0, math.floor(video.duration - lengthOfABeat * i)) # random video portion
                break
            except ValueError:
                continue
        
        if not fadeOut:
            videos.append(video.subclip(videostart,videostart + lengthOfABeat * i))
        else: # fadeout before a drop
            videoFadeOut = video.subclip(videostart,videostart + lengthOfABeat * i)
            videos.append(videoFadeOut.fx(vfx.fadeout, duration=videoFadeOut.duration / 4))
            fadeOut = False
        
        start += (lengthOfABeat * i)
        beats += i
        
        # print progress to screen
        percentRendered = get_closest_percent((beats / (len(intensities)*16) * 100))
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

    intensities = get_intensities("music/"+argv[0],int(bpm))

    for i in range(int(argv[2])):
        make_subMovie( argv[0], int(bpm), videosList, i, start, finish, duration, intensities)

if __name__ == "__main__":
    main(sys.argv[1:])