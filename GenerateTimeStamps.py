import numpy as np
from tinytag import TinyTag
from scipy.io.wavfile import read, write

def get_duration(filename):
    '''
    reads song metadata ard returns duration
    '''
    return TinyTag.get(filename).duration

def guess_first_and_last_DownBeat(filename):
    '''
    Reads a .wav audio file (str) and guesses the timestamp of first and last downbeats (float,float) in seconds
    '''

    Fs, data = read(filename)

    # one stereo channel for ease
    data = data[:,0]

    highestDB = max(data)
    
    # find first downbeat
    for count, point in enumerate(data):
        if point >= (highestDB / 1.5): # > 0 to avoid noise / ambience
            break
    
    # find last downbeat
    for count2, point in enumerate(data[::-1]):
        if point >= (highestDB / 1.5): # > 0 to avoid noise / ambience
            break
    
    duration = get_duration(filename)
    
    return ((count / len(data)) * duration, ((len(data)- count2) / len(data)) * duration)
     

def get_timestamps(filename, bpm):
    '''
    Returns a list [float,float,..] of the timestamps of all the downbeats in the song

    Parameters:
    - bpm (the tempo (beats per minute) of the song)
    '''

    # estimated guess of first and last beat in song
    start, finish = guess_first_and_last_DownBeat(filename)
    
    timeStamps = []
    timeStamps.append(start)

    lengthOfABeat = 1 / (bpm / 60)

    while start < finish:
        timeStamps.append(start + lengthOfABeat) 
        start += lengthOfABeat

    return timeStamps
