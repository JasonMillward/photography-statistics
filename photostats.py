"""


Released under the MIT license
Copyright (c) 2014, Jason Millward

@category   misc
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT

Usage:
    stats.py <EXIF Attr>... [--dir=<dir>]

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

def statistics(arguments):
    imageresults = {}

    directory = arguments["--dir"]

    if directory is None:
        directory = "."

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
if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version=__version__)
    statistics(arguments)

