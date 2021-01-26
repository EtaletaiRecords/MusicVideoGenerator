from GenerateTimeStamps import *
from moviepy.editor import *
from SimpleVid import preload
import random, math, os, sys

'''
Dynamic video generation - Intense sections of music will have faster visuals
'''

HIGH_INTENSITY = [1,1,1,1,4,4]
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

    beats = 0 # current beats rendered
    
    print("Generating video")

    while beats < (len(intensities) * 16):

        # switch up video rate every 4 bars
        if beats % 16 == 0:
            new4BarBlock = True

        if new4BarBlock:
            print(intensities[current4BarBlock])

            # DYNAMIC video selection
            if intensities[current4BarBlock] == "High":
                if current4BarBlock > 0 and intensities[current4BarBlock - 1] == "Low": # If the previous section was low and this one is high, make it speedy by defualt
                    i = 1
                else:
                    i = random.choice(HIGH_INTENSITY) 
            elif intensities[current4BarBlock] == "Medium":
                i = random.choice(MEDIUM_INTENSITY)
            else:
                i = random.choice(LOW_INTENSITY)
            
            current4BarBlock += 1


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
        
        print(str((beats / (len(intensities)*16) * 100)) + "%/ rendered")

        new4BarBlock = False
    
    # Ambient outro
    if start < duration:
        clip = VideoFileClip("titles/"+random.choice([x for x in os.listdir("titles/")])).subclip(0,duration-start)
        videos.append(clip.fx( vfx.fadeout, duration=clip.duration/2))

    final_clip = concatenate_videoclips(videos,method="compose")
    
    # write video
    final_clip.write_videofile(filename="temp/"+str(filename)+str(output)+".mp4",preset="ultrafast",threads=4,audio=False)

    # memory save
    for v in videos:
        v.close()

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