import exifread
# Open image file for reading (binary mode)
f = open("./image.jpg", 'rb')

# Return Exif tags
tags = exifread.process_file(f)

print tags['EXIF FocalLength']
