import numpy as np
from tinytag import TinyTag
from scipy.io.wavfile import read, write
import os, sys, csv

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
    Returns a list [float,float,..] of the timestamps of all the 4 bar regions in the song

    Parameters:
    - bpm (the tempo (beats per minute) of the song)
    '''

    # estimated guess of first and last beat in song
    start, finish = guess_first_and_last_DownBeat(filename)
    
    timeStamps = []
    timeStamps.append(start)

    lengthOfABeat = 1 / (bpm / 60)

    while start < finish:
        timeStamps.append(start + lengthOfABeat * 16) 
        start += lengthOfABeat * 16 

    return timeStamps

def get_counts_in_4_bars(filename, bpm):
    '''
    returns the number of data points in 4 bars of a file for downstream works
    '''
    lengthOfABeat = 1 / (bpm / 60)
    lengthof16beats = lengthOfABeat * 16 # 4 bars

    Fs, data = read(filename)

    # one stereo channel for ease
    data = data[:,0]

    length = len(data)
    duration = get_duration(filename)

    # find how many counts in 16 beats
    for count, point in enumerate(data):
        if count / length >= lengthof16beats / duration:
            return count

def get_intensities(filename, bpm):
    '''
    Returns {4barCount(int):intensity(str)} for each 4 bar segment in the given .wav file

    Intensities = "Low","Medium","High
    '''
    
    duration = get_duration(filename)
    start, finish = guess_first_and_last_DownBeat(filename)
    countsIn4Bars = get_counts_in_4_bars(filename,bpm)

    intensities = {}

    # analyse waveform
    Fs, data = read(filename)

    # one stereo channel for ease
    data = data[:,0]

    length = len(data)
    
    count_ = 0
    sum_ = float(0)
    barBlock = 0 # current index of 4 bar block

    for count, point in enumerate(data):
        if count / length >= start / duration and count / length <= finish / duration: # only calculate between first and last downbeat
            
            count_ += 1
            sum_ += float(abs(point)) # absolute value because deviation from 0 (no volume) is what is important
            
            if sum_ < 0:
                sys.exit()
            
            # calculate and save average every 4 bars
            if count_ >= countsIn4Bars:
                intensities[barBlock] = sum_ / count_
    
                count_ = 0
                sum_ = float(0)
                barBlock += 1
    
    
    maxAverageValue = max(intensities.values())

    # all instensities are relative to one another
    for key in intensities.keys():
        if intensities[key] > 0.96 * maxAverageValue:
            intensities[key] = "High"
        elif intensities[key] > 0.65 * maxAverageValue:
            intensities[key] = "Medium"
        else:
            intensities[key] = "Low"

    return intensities

def save_intensities(intensities, filename):
    '''
    Saves intensities from get_intensities(filename, bpm) as .csv
    '''
    ordered = []    
    for key in intensities.keys():
        ordered.append((key,intensities[key]))
    
    ordered = sorted(ordered)

    with open("analysis/"+str(filename)+".csv", "w", newline='') as file:
        fieldnames = ["Section","Intensity"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        
        writer.writeheader()
      
        for t in ordered:
            writer.writerow({'Section': t[0], 'Intensity': t[1]})
        
        file.close()


def guess_bpm(filename):
    '''
    Reads a .wav file and returns an estimate of the bpm, If bpm is known it should be entered manually for best results
    '''
    pass

def main(argv):
    '''
    stores intensities to file
    '''
    save_intensities(get_intensities("music/"+str(argv[0]),int(argv[1])),argv[0])

if __name__ == "__main__":
    main(sys.argv[1:])    
