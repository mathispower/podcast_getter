#!/usr/bin/env python
"""
    TODO:
        - Check if ad present at start of file; remove 15-30s if so
"""
import glob, math, os, subprocess as sp, sys

DIR_OUT = "output"
program = "ffmpeg.exe"

def crop_ad(file_name, crop_time=32):
    """
        crop_time = time in seconds at the start to crop out
    """

    prefix = file_name[:-4]
    suffix = file_name[-4:]
    new_file_name = os.path.join(DIR_OUT, "%s_c%s" % (prefix, suffix))

    if os.path.isfile(new_file_name):
        print "\033[1;33m%s already exists,"%(new_file_name),
        print "skipping %s\033[0m"%(file_name)
        sys.stdout.flush()
        return new_file_name

    args = [ program,
             "-i", file_name,
             "-ss", "%i"%crop_time,
             "-acodec", "copy", new_file_name ]

    p = sp.Popen(args, stdout=sp.PIPE, stderr=sp.STDOUT)

    output = []
    while True:
        line = p.stdout.readline().rstrip()
        if not line: break

        output.append(line)

    if not os.path.isfile(new_file_name):
        print "\033[1;31mERROR processing %s" % file_name
        for line in output:
            print line
        print "\033[0m"
        sys.stdout.flush()
        return ''

    else:
        print "Cropped %s" % file_name
        sys.stdout.flush()

        return new_file_name

def split(file_name, seg_length=900):
    """ """
    if not os.path.isfile(file_name): return

    prefix = file_name[:-4]
    suffix = file_name[-4:]
    new_file_name = "%s_%%2d%s" % (prefix,suffix)

    # Get duration
    args = [program, "-i", file_name]
    out = sp.Popen(args, stdout=sp.PIPE, stderr=sp.STDOUT).communicate()[0]

    token = "Duration:"
    start = out.find(token) + len(token)
    h,m,s = out[start:].split(':')[0:3]; s = s.split(',')[0]
    dur = int(h) * 3600 + int(m) * 60 + float(s)

    if dur < (2 * seg_length): return # No Splitting necessary

    inc = dur // int(seg_length)
    seg_length = "%i" % math.ceil(dur / float(inc))

    args = [ program,
             "-i", file_name,
             "-f", "segment", "-segment_time", seg_length,
             "-acodec", "copy", new_file_name ]

    out = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE).communicate()

    # Need some better error checking here
    os.remove(file_name)

if __name__ == "__main__":
    file_list = glob.glob("*.m4a")
    file_list.extend(glob.glob("*.mp3"))

    for f_l in file_list:
        split( crop_ad(f_l) )
