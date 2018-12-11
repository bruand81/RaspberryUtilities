import cv2
import os
import math
from time import time
import _thread
import configparser
import shutil


class RawVideoGrabber:
    w = 0
    h = 0
    fps = 0
    numFrames = 0
    numDigits = 0

    def grab(self, opts):
        # Grab as a sequence of frames
        cap = self.__open_cap__(opts)
        print("Width: %d, height: %d" % (self.w, self.h))
        print("FrameRate: %d fps" % self.fps)
        print("Total number of frames to be captured: %d" % self.numFrames)

        dest_dir = self.__manage_path__(opts)
        print("Frames will be stored in %s" % os.path.abspath(dest_dir))

        if opts["OutputFormat"] == 'video':
            return self.grab_as_video(cap, dest_dir, opts)
        elif opts["OutputFormat"] == 'image':
            return self.grab_as_image(cap, dest_dir, opts)
        else:
            raise ValueError("Value \"%s\" not recognized for OutputFormat\n\t Admitted value are: video or image")

    def grab_as_video(self, cap, dest_dir, opts):
        # Grab as a sequence of frames from camera as a video file
        fourcc_format = opts["VideoFormat"]
        video_output = os.path.join(dest_dir, opts["OutputVideoFilename"])

        out = cv2.VideoWriter(os.path.join(dest_dir, video_output),
                              cv2.VideoWriter_fourcc(fourcc_format[0], fourcc_format[1], fourcc_format[2],
                                                     fourcc_format[3]), self.fps, (self.w, self.h))

        print("Capturing frames...")
        i = 0
        start_time = time()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                out.write(frame)

            i += 1

            if i >= self.numFrames:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        end_time = time()
        time_taken = end_time - start_time
        print("Saved %d frames in %d seconds" % (self.numFrames, time_taken))
        return

    def grab_as_image(self, cap, dest_dir, opts):
        # Grab as a sequence of frames from camera as a sequence of images

        image_output_template = opts["OutputImageFilename"]
        #frame_num_expansion = "%0"+str(self.numDigits)+"d"
        frame_num_expansion = "%s"
        i = 0

        print("Capturing frames...")
        start_time = time()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                fname = image_output_template.format(frame_num_expansion % int(round(time() * 1000)))
                if(opts["UseThread"]):
                    try:
                        _thread.start_new_thread(RawVideoGrabber.__store_image_file__, (frame, fname, dest_dir, ))
                    except Exception as e:
                        # print('Error in new thred for frame %d": %s' % (i, str(e)))
                        raise RuntimeError('Error in new thred for frame %d": %s' % (i, str(e)))
                else:
                    RawVideoGrabber.__store_image_file__(frame, fname, dest_dir)

            i += 1

            if i >= self.numFrames:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        end_time = time()
        time_taken = end_time - start_time
        print("Saved %d frames in %d seconds" % (self.numFrames, time_taken))
        print("Effective average fps: %d" % (self.numFrames/time_taken))
        return

    @staticmethod
    def __store_image_file__(frame, fname, dest_dir):
        dest = os.path.join(dest_dir, fname)
        cv2.imwrite(dest, frame)

    def __open_cap__(self, opts):
        cap = cv2.VideoCapture(opts["CameraIndex"])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, opts["MaxWidth"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, opts["MaxHeight"])
        self.w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.set(cv2.CAP_PROP_FPS, opts["MaxFramerate"])
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        self.numFrames = self.fps * opts["NumSecs"]
        self.numDigits = math.ceil(math.log10(self.numFrames))
        return cap

    @staticmethod
    def __manage_path__(opts):
        dest_dir = opts["DestDir"]

        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)

        os.makedirs(dest_dir)

        return dest_dir


if __name__ == '__main__':
    # Reading configuration from file
    options = dict()
    config = configparser.ConfigParser()
    config.read('RawVideoGrabber.ini')
    options["CameraIndex"] = int(config['DEFAULT']['CameraIndex'])
    options["MaxWidth"] = int(config['DEFAULT']['MaxWidth'])
    options["MaxHeight"] = int(config['DEFAULT']['MaxHeight'])
    options["MaxFramerate"] = int(config['DEFAULT']['MaxFramerate'])
    options["NumSecs"] = int(config['DEFAULT']['NumSecs'])
    options["DestDir"] = config['DEFAULT']['DestDir']
    options["VideoFormat"] = config['DEFAULT']['VideoFormat']
    options["OutputFormat"] = config['DEFAULT']['OutputFormat']
    options["OutputVideoFilename"] = config['DEFAULT']['OutputVideoFilename']
    options["OutputImageFilename"] = config['DEFAULT']['OutputImageFilename']
    options["UseThread"] = bool(int(config['DEFAULT']['UseThread']))
    grabber = RawVideoGrabber()
    grabber.grab(options)
