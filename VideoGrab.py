import numpy as np
import cv2
import os
import math
from time import time
import configparser
# import threading

# rec = True


# def stoprec():
#   global rec
#   rec = False
config = configparser.ConfigParser()
config.read('VideoGrab.ini')
max_resolution = int(config['DEFAULT']['MaxResolution'])
max_width = int(config['DEFAULT']['MaxWidth'])
max_height = int(config['DEFAULT']['MaxHeight'])
max_framerate = int(config['DEFAULT']['MaxFramerate'])
numSecs = int(config['DEFAULT']['NumSecs'])
destDir = config['DEFAULT']['DestDir']
fourcc_format = config['DEFAULT']['VideoFormat']
output_format = config['DEFAULT']['OutputFormat']
video_output = config['DEFAULT']['OutputVideoFilename']
image_output_template = config['DEFAULT']['OutputImageFilename']
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, max_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, max_height)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
print("Width: %d, height: %d" % (w,h))
cap.set(cv2.CAP_PROP_FPS, max_framerate)
prop =int(cap.get(cv2.CAP_PROP_FPS))
print("FrameRate: %d fps" % prop)
numFrames = prop * numSecs
print("Total number of frames to be captured: %d" % numFrames)
numDigits = math.ceil(math.log10(numFrames))

# print(prop)

if not os.path.exists(destDir):
    os.makedirs(destDir)
print("Frames will be stored in %s" % os.path.abspath(destDir))

i = 0

# t = threading.Timer(30, stoprec)
# t.start()
print("Capturing frames...")
frames = list()
start_time = time()
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # baseName = "frame_%0"+str(numDigits)+"d.tiff"
        # fname = baseName % i
        # dest = os.path.join(destDir, fname)
        # print("Saving frame %d on %s"%(i,dest))
        # cv2.imshow("Current frame", frame)

        # print(ret);
        # cv2.imwrite(dest, frame)
        frames.append(frame)
        i += 1

    if i >= numFrames:
       break
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

end_time=time()
time_taken = end_time - start_time
stats = "%d,%d, %d,%d, %d" % (w, h, prop, numFrames, time_taken)
print("Captured %d frames in %d seconds" % (numFrames, time_taken))
cap.release()

i=1

print('Saving captured frames to disk')
start_time = end_time
if output_format == 'video':
    out = cv2.VideoWriter(os.path.join(destDir, video_output), cv2.VideoWriter_fourcc(fourcc_format[0], fourcc_format[1], fourcc_format[2], fourcc_format[3]), prop, (w, h))

for frame in frames:
    if output_format == 'video':
        out.write(frame)
    else:
        fname = image_output_template.format('%05d' % i)
        dest = os.path.join(destDir, fname)
        # print("Saving frame %d on %s" % (i, dest))
        cv2.imwrite(dest, frame)

    i += 1
end_time=time()
time_taken = end_time - start_time
print("Saved %d frames in %d seconds" % (numFrames, time_taken))

if output_format == 'video':
    out.release()
cv2.destroyAllWindows()
