import re, argparse
import sys
import matplotlib.pyplot as plt
import plistlib
import numpy as np

def findCommonTracks(fileNames):
    """
    Find common tracks in given file lists
    and save them into "common.txt"
    """
    trackNameSets = []
    for filename in fileNames:
        trackNames = set()
        plist = plistlib.load(filename)
        tracks = plist['Tracks']
        for trackId, track in tracks.items():
            try:
                trackNames.add(track['Name'])
            except:
                pass

        trackNameSets.append(trackNames)

    commonTracks = set.intersection(*trackNameSets)

    if len(commonTracks) > 0:
        f = open("common.txt", 'w')
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()

def findDuplicates(fileName):
    print("Finding duplicate tracks in %s..." % fileName)
    plist = plistlib.load(fileName)
    tracks = plist['Tracks']
    trackNames = dict()

    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            if name in trackNames:
                if duration // 1000 == trackNames[name][0] // 1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count + 1)
            else:
                trackNames[name] = (duration, 1)
        except:
            pass

    # store duplicates as (name, count) tuples:
    dups = []
    for k, v in trackNames.items():
        if v[1] > 0:
            dups.append((k, v[1]))

    if len(dups) > 0:
        print("Found %d duplicates. Track names saved into dup.txt" % len(dups))
    else:
        print("No duplicate tracks found!")

    f = open("dups.txt", "w")
    for val in dups:
        f.write("[%d] %s\n" % (val[1], val[0]))
    f.close()

def plotStats(filename):
    """
    Plot some statistics by reading track information from playlist
    """
    plist = plistlib.load(filename)
    tracks = plist['Tracks']
    ratings = []
    durations = []

    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass

    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in %s." % filename)
        return

    x = np.array(durations, np.int32)
    # convert to minutes
    x = x / 60000.0
    y = np.array(ratings, np.int32)

    # scatter plot
    plt.subplot(2, 1, 1)
    plt.plot(x, y, 'o')
    plt.axis([0, 1.05 * np.max(x), -1, 110])
    plt.xlabel('Track duration')
    plt.ylabel('Track rating')

    # histogram plot
    plt.subplot(2, 1, 2)
    plt.hist(x, bins=20)
    plt.xlabel('Track duration')
    plt.ylabel('Count')

    plt.show()

def main():
    description = "This program analyzes playlist files (.xml) exported from iTunes"
    parser = argparse.ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', nargs='plFile', required=False)
    group.add_argument('--dup', nargs='plFileD', required=False)

    args = parser.parse_args()

    if args.plFiles:
        findCommonTracks(args.plFiles)
    elif args.plFile:
        plotStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")