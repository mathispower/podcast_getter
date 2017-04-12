#!/usr/bin/env python
""" Requires pydub and libav_bin """
## TODO:
import argparse
import os
import sys
import urllib

update_only = False

###
PODCASTS = ( "http://www.kfiam640.com/podcast/BillHandel.xml",
             "http://www.kfiam640.com/podcast/HOTL.xml",
             "http://www.kfiam640.com/podcast/darksecretplace.xml",
             "http://www.kfiam640.com/podcast/RicEdelman.xml",)
             # "http://kfiam640.iheart.com/podcast/garyandshannon.xml" )

ARCHIVES = ( "BillHandel.txt",
             "HOTL.txt",
             "darksecretplace.txt",
             "RicEdelman.txt",)
             # "garyandshannon.txt" )

EXT = ( "hotn",
        "hotl",
        "dsp",
        "re",)
        # "gas" )
         
def Progress(count, blockSize, totalSize):
    if totalSize != 0: percent = int(count*blockSize*100/totalSize)
    else: percent = 100
    a = "\rDownloading: %s...%d%%" % (fileP, percent)
    sys.stdout.write("%80s" % a)
    sys.stdout.flush()

def DownloadFiles(number):
    url_xml = PODCASTS[number]
    archive = ARCHIVES[number]
    show = EXT[number]

    links = []; fileNames = []; archives = []; i = 0
    
    # Extract the file names from the xml file
    file = urllib.urlopen(url_xml)

    for lines in file:
        t0 = lines.split("<guid>")
        if len(t0) > 1:
            links.append( t0[1].split("</guid>")[0] )
            fileNames.append( links[i].split('/')[-1] )
            i += 1

    file.close()

    # Read the names of files already downloaded
    file = open(archive, 'rb')
    for lines in file: archives.append(lines[:-1])
    file.close()

    # Compare the file names from the xml to the archives
    newFiles = []; newURLs = []; exists = 0;
    for index, i in enumerate(fileNames):
        for j in archives:
            if i == j:
                exists = 1
                break;
        if exists == 0:
            newFiles.append(i)
            newURLs.append(links[index])
            index += 1
        else: exists = 0

    if not update_only:
        # Download the new files
        for index, i in enumerate(newURLs):
            global fileP
            fileP = newFiles[index]
            newName = fileP.split("_")[-1]
            if newName[-4:] == ".mp3" or newName[-4:] == ".wav":
                newName = newName[:-4] + "_" + show + newName[-4:]
                urllib.urlretrieve(i, newName, reporthook=Progress)
                print "\n"

                err = SplitFile(newName,34)

                if err == 0: os.remove(newName)

            print "\n"

    # Update the archive file (with only files from this run to
    # prevent the archive file from getting too big
    file = open(archive, 'wb')
    for lines in fileNames:
        file.write(lines+"\n")
    file.close()

def SplitFile(file_name,break_len=10):
    """ file_name is Something.mp3
        break_len is in minutes """

    from pydub import AudioSegment

    name = file_name.split(".mp3")

    if len(name) > 1: name = name[0]
    else:
        name = file_name.split(".wav")
        if len(name) > 1: name = name[0]
        else: return 1

    sound = AudioSegment.from_mp3(file_name)

    # break_len *= 60000
    break_len = len(sound) // 4
    # len() and slicing are in milliseconds
    seg_len = len(sound) / break_len

    for i in range(seg_len):
        seg = sound[i*break_len:(i+1)*break_len]
        print "Exporting segment %i..."%(i+1); sys.stdout.flush()

        seg.export("%s_%s.mp3"%(name,("%s"%(i+1)).zfill(2)), format="mp3")

    # Last one (Usually very short and non-essential
    # seg = sound[(i+1)*break_len:]
    # print "Exporting segment %i..."%(i+2); sys.stdout.flush()

    # seg.export("%s_%s.mp3"%(name,("%s"%(i+2)).zfill(2)), format="mp3")

    return 0

if __name__ == '__main__':
    for i, z in enumerate(PODCASTS):
        DownloadFiles(i)

    # raw_input('Press enter to exit ...')