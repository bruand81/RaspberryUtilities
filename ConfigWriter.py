import configparser

config = configparser.ConfigParser()
max_resolution = 20000
max_width = 1920
max_height = 1080
max_framerate = 60
numSecs = 10
fourcc_format = 'FFV1'

config['DEFAULT']['MaxResolution'] = str(max_resolution)
config['DEFAULT']['MaxWidth'] = str(max_width)
config['DEFAULT']['MaxHeight'] = str(max_height)
config['DEFAULT']['MaxFramerate'] = str(max_framerate)
config['DEFAULT']['NumSecs'] = str(numSecs)
config['DEFAULT']['DestDir'] = 'frames'
config['DEFAULT']['VideoFormat'] = fourcc_format
config['DEFAULT']['OutputFormat'] = 'image'
config['DEFAULT']['OutputVideoFilename'] = 'video.avi'
config['DEFAULT']['OutputImageFilename'] = 'frame{0}.tiff'

with open('VideoGrab.ini', 'w') as configfile:
    config.write(configfile)