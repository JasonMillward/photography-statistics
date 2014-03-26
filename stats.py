"""
Auto Ripper

Ripping
    Uses MakeMKV to watch for movies inserted into DVD/BD Drives

    Automaticly checks for existing directory/movie and will NOT overwrite existing
    files or folders

    Checks minimum length of video to ensure movie is ripped not previews or other
    junk that happens to be on the DVD

    DVD goes in > MakeMKV gets a proper DVD name > MakeMKV Rips
    DVD does not get ejected, maybe it will get added to later versions

Compressing
    An optional additional used to rename and compress movies to an acceptable standard
    which still delivers quallity audio and video but reduces the file size
    dramatly.

    Using a nice value of 15 by default, it runs HandBrake as a background task
    that allows other critical tasks to complete first.


Released under the MIT license
Copyright (c) 2014, Jason Millward

@category   misc
@version    $Id: 1.6, 2014-03-11 16:52:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT

Usage:
    stats.py <EXIF Attr>... [--dir=<dir>]

Options:
    -h --help     Show this screen.
    --version     Show version.
    --debug       Output debug.
    --rip         Rip disc using makeMKV.
    --compress    Compress using handbrake.
    --test        Testing?

"""

import exifread
import docopt
import unicodedata
from os import listdir
from os.path import isfile, join

__version__ = "0.1"

def findimages(directory):
    try:
        result = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
    except OSError:
        print "Directory not found"
        result = []
    finally:
        return result

def returnattribute(image, attribute):
    try:
        f = open(image, 'rb')
        tags = exifread.process_file(f)
        result = str(tags[attribute])
    except KeyError:
        #print "Attribute: " + attribute
        result = None
    finally:
        return result

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def parseresults(imageresults):
    for r in imageresults:
        print r
        b = imageresults[r].keys()
        b.sort()
        for v in b:
            count = "+" * imageresults[r][v]
            print "\t{0}\t {1}".format(v, count)

        print ""

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version=__version__)

    directory = arguments["--dir"]

    if directory is None:
        directory = "."

    imageresults = {}

    for f in findimages(directory):
        if f.endswith(".jpg"):
            for e in arguments["<EXIF Attr>"]:
                attribute = "EXIF %s" % e

                val = returnattribute( join(directory, f), attribute)
                if val is not None:
                    if is_number(val):
                        val = int(val)

                    if e in imageresults:
                        if val in imageresults[e]:
                            imageresults[e][val] += 1
                        else:
                            imageresults[e][val] = 1
                    else:
                        imageresults[e] = {}
                        imageresults[e][val] = 1

    parseresults(imageresults)
