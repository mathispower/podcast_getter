#!/usr/bin/env python

## TODO:

import os
import sys
import urllib

###
PODCASTS = ( "http://www.kfiam640.com/podcast/BillHandel.xml",
			 "http://www.kfiam640.com/podcast/HOTL.xml",
			 "http://www.kfiam640.com/podcast/darksecretplace.xml",
			 "http://www.kfiam640.com/podcast/RicEdelman.xml" )
ARCHIVES = ( "BillHandel.txt",
			 "HOTL.txt",
			 "darksecretplace.txt",
			 "RicEdelman.txt" )
         
def Progress(count, blockSize, totalSize):
	percent = int(count*blockSize*100/totalSize)
	a = "\rDownloading: %s...%d%%" % (fileP, percent)
	sys.stdout.write("%80s" % a)
	sys.stdout.flush()

def DownloadFiles(url_xml, archive):
	links = []; fileNames = []; archives = []; i = 0
	
	# Extract the file names from the xml file
	file = urllib.urlopen(url_xml)

	for lines in file:
		if lines.split('>')[0] == "<guid":
			links.append(lines.split('>')[1].split('<')[0])
			fileNames.append(links[i].split('/')[-1])
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

	# Download the new files
	for index, i in enumerate(newURLs):
		global fileP
		fileP = newFiles[index]
		newName = fileP.split("_")[-1]
		if newName[-4:] == ".mp3" or newName[-4:] == ".wav":
			urllib.urlretrieve(i, newName, reporthook=Progress)
		print "\n"

	# Update the archive file (with only files from this run to
	# prevent the archive file from getting too big
	file = open(archive, 'wb')
	for lines in fileNames:
		file.write(lines+"\n")
	file.close()

if __name__ == '__main__':
	for i, z in enumerate(PODCASTS):
		DownloadFiles(PODCASTS[i],ARCHIVES[i])
