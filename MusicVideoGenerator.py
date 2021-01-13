import os, sys

def main(argv):
    '''
    Generates a Music Video based on a specfic song by calling a few python files and movie ediitng command line tools

    Arguments:
    1. Song name (should be located in music/)
    2. Song BPM
    3. Complexity (2 OR 3), 2 for quicker and 3 for more intense visuals

    '''

    os.system("python SimpleVid.py " + argv[0] + " " + argv[1] + " " + argv[2])
    
    print("Smallerizing")
    
    # makes all files 720p
    for i in range(int(argv[2])):
        os.system("ffmpeg -i temp/"+str(argv[0])+str(i)+".mp4 -vf scale=1280:780 temp/small"+str(argv[0])+str(i)+".mp4")
    
    if int(argv[2]) == 3:

        print("Blending")
        for i in range(int(argv[2])-1):
            os.system("ffmpeg -i temp/small"+str(argv[0])+str(i)+".mp4 -i temp/small"+str(argv[0])+str(i+1)+".mp4 -filter_complex blend='difference' temp/output"+str(argv[0])+str(i)+".mp4")
        
        print("Mashing")
        os.system("ffmpeg -i temp/output"+str(argv[0])+"0.mp4 -i temp/output"+str(argv[0])+"1.mp4 -filter_complex blend='difference temp/"+str(argv[0])+"GeneratedMusicVideo.mp4")

    elif int(argv[2]) == 2:
        print("Blending")
        for i in range(int(argv[2])-1):
            os.system("ffmpeg -i temp/small" + str(argv[0]) + str(i) + ".mp4 -i temp/small" + str(argv[0]) + str(i + 1) +".mp4 -filter_complex blend='difference' temp/" + str(argv[0]) + "GeneratedMusicVideo.mp4")

    else:
        print("Invalid compleity: please choose 2 (fast) or 3 (slow, more complicated output)")
    
    # add audio
    os.system("ffmpeg -i temp/" + str(argv[0])  + "GeneratedMusicVideo.mp4 -i music/" + str(argv[0]) + " -map 0:v -map 1:a -c:v copy out/output" + str(argv[0]) + "GeneratedMusicVideo.mp4")

    print("deleting temporaary files")
    os.system("del temp\* ")


if __name__ == "__main__":
    main(sys.argv[1:])