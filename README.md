# Photography Statistics

Python library to extract statistics in an easy to read format.

### Installation

Requirements

* python 2.7
* exifread

	```pip install exifread```


### Usage

```photostats.py <EXIF Attr>... [--dir=<dir>] ```

### Results

```
$ python stats.py FocalLength WhiteBalance ISOSpeedRatings --dir ./images/


EXIF ISOSpeedRatings
    100     +
    200     ++++++
    250     ++++++++
    400     +
    500     +
    1600    +
EXIF FocalLength
    18      +
    21      ++++++
    96      +
    109     +
    135     ++++++++
    163     +
EXIF WhiteBalance
    Auto    ++++++++++++++++++

```
