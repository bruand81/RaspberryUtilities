import os
import math
import time
import configparser
import shutil
import picamera


class YUVCameraGrabber:

    w = 0
    h = 0
    fps = 0
    numFrames = 0
    numDigits = 0

    def grab(self, opts):
        # Grab as a sequence of frames
        print("Camera = %s" % opts["CameraIndex"])
        print("Use threads = %s" % opts["UseThread"])
        dest_dir = self.__manage_path__(opts)
        print("Frames will be stored in %s" % os.path.abspath(dest_dir))
        self.w = opts["MaxWidth"]
        self.h = opts["MaxHeight"]

        if opts["OutputFormat"] == 'video':
            return self.grab_as_video(dest_dir=dest_dir, opts=opts, numvideos=opts['NumVideos'])
        else:
            raise ValueError("Value \"%s\" not recognized for OutputFormat\n\t Admitted value are: video")

    def grab_as_video(self, dest_dir, opts, numvideos = 1):
        video_format = opts["VideoFormat"]
        # video_output = os.path.join(dest_dir, opts["OutputVideoFilename"])
        image_output_template = os.path.join(dest_dir, opts["OutputVideoFilename"])
        self.fps = opts["MaxFramerate"]
        self.numFrames = self.fps * opts["NumSecs"]
        self.numDigits = math.ceil(math.log10(self.numFrames))
        # frame_num_expansion = "%s"
        frame_num_expansion = "%d"

        with picamera.PiCamera(camera_num=opts["CameraIndex"]) as camera:
            for i in range(0, numvideos):
                idx = i
                print("\n********************************")
                print("***** Registering video %d *****" % (idx + 1))
                print("********************************\n")
                print("Width: %d, height: %d" % (self.w, self.h))
                print("FrameRate: %d fps" % self.fps)
                fname = image_output_template.format(frame_num_expansion % (idx + 1))

                camera.resolution = (self.w, self.h)
                camera.framerate = self.fps
                camera.zoom = (0.0, 0.0, 1.0, 1.0)
                start_time = time.time()
                camera.start_preview()
                camera.start_recording(output=fname, format=video_format)
                camera.wait_recording(timeout=opts["NumSecs"])
                camera.stop_recording()
                end_time = time.time()
                time_taken = end_time - start_time
                print("Video stored in %d seconds" % time_taken)
                print("Video stored in %s" % fname)

        return

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
    config.read('YUVCameraGrabber.ini')
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
    options["NumVideos"] = int(config['DEFAULT']['NumVideos'])
    grabber = YUVCameraGrabber()
    grabber.grab(options)
