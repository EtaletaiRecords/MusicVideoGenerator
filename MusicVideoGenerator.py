import os, sys, argparse, time

# TODO:
# Only make 720p if already not **
#
# Add automatic bpm detection
# Choose videos to use based on tags
# 720p vs 1080p option
# different time signature support


def main(args):
    '''
    Generates a Music Video based on a specfic song by calling a few python files and movie ediitng command line tools

    Arguments:
    1. Song name (should be located in music/)
    2. Song BPM
    3. Complexity (2 OR 3), 2 for quicker and 3 for more intense visuals (3 by default)

    '''
    
    start = time.time()

    # Generates n(compelxity) number of randomized videos   
    if args.dynamic == True:
        os.system("python SmartVid.py " + args.songName + " " + args.bpm + " " + args.complexity)
    else:
        os.system("python SimpleVid.py " + args.songName + " " + args.bpm + " " + args.complexity)
    
    # makes all videos 720p
    print("making Subvideos 720p")
    for i in range(int(args.complexity)):
        if not os.path.exists("temp/small"+ args.songName +str(i)+".mp4"):
            print("Smallerizing video"+str(i))
            os.system("ffmpeg -i temp/"+ args.songName +str(i)+".mp4 -vf scale=1280:720 -crf 18 -preset medium temp/small"+ args.songName +str(i)+".mp4 -hide_banner -loglevel warning")
        else:
            print("Video" +str(i) +" is already 720p")

    # get output name
    if args.output:
        outputName = args.output
    else:
        outputName = args.songName # song name by default

    # Blends all videos
    if int(args.complexity) == 3:
        for i in range(int(args.complexity)-1):
            print("Blending videos together "+str(i+1))

            os.system("ffmpeg -i temp/small"+ args.songName +str(i)+".mp4 -i temp/small"+ args.songName +str(i+1)+".mp4 -filter_complex blend='difference' temp/output"+args.songName+str(i)+".mp4 -hide_banner -loglevel warning")
        
        print("Mashing those blended videos together")
        os.system("ffmpeg -i temp/output"+args.songName+"0.mp4 -i temp/output"+args.songName+"1.mp4 -filter_complex blend='difference temp/"+args.songName+"GeneratedMusicVideo.mp4 -hide_banner -loglevel warning")

    elif int(args.complexity) == 2:
        print("Blending")
        for i in range(int(args.complexity)-1):
            os.system("ffmpeg -i temp/small" + args.songName + str(i) + ".mp4 -i temp/small" + args.songName + str(i + 1) +".mp4 -filter_complex blend='difference' temp/" + args.songName + "GeneratedMusicVideo.mp4 -hide_banner -loglevel warning")

    else:
        print("Invalid compleity: please choose 2 (fast) or 3 (slow, more complicated output)")
    
    # make temporary .aac file to add to the mp4 video (.wav not supported directly)
    os.system("ffmpeg -i music/" + args.songName +" -ab 256k -hide_banner -loglevel warning temp/tempAudio.aac")

    # chromashift to add pizazz\
    print("Gliching final result")
    os.system("ffmpeg -i temp/" + args.songName  + "GeneratedMusicVideo.mp4 -vf chromashift=crv=-200:cbv=100:crh=100 temp/" + args.songName  + "GeneratedMusicVideoFinal.mp4 -hide_banner -loglevel warning")

    # add audio
    os.system("ffmpeg -i temp/" + args.songName  + "GeneratedMusicVideoFinal.mp4 -i temp/tempAudio.aac -c copy -map 0:v:0 -map 1:a:0 out/" + outputName + ".mp4 -hide_banner -loglevel warning")

    # file clean up
    print("deleting temporaary files")
    for vid in os.listdir("temp/"):
        os.remove("temp/"+vid)
    
    end = time.time()
    print(end - start)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a music video - talent free!')
    parser.add_argument("-songName", help="Song name (should be located in music/) i.e Music1.wav")
    parser.add_argument("-bpm", help="Song BPM")
    parser.add_argument("--complexity", help="Complexity (2 OR 3), 2 for quicker and 3 for more intense visuals (3 by default)", default="3")
    parser.add_argument("--dynamic",help="True for dynamic visals which respond to song intensity, False for random visuals", default=True)
    parser.add_argument("--output",help="Output file prefix eg MyVideo")
    args = parser.parse_args()
    
    main(args)