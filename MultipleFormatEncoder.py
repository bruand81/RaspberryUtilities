import subprocess
import os


def encode(input_file, output_file, opts: dict, input_opts: list, output_opts: list):
    if not os.path.exists(input_file):
        raise FileNotFoundError("Input video %s not found" % os.path.abspath(input_file))

    if os.path.exists(output_file):
        if not opts['AllowOverrideOutput']:
            raise FileExistsError("Output file %s is already present and option AllowOverrideOutput is set to false" % os.path.abspath(output_file))
        else:
            os.remove(output_file)

    command = "ffmpeg"
    options = ""

    for opt in input_opts:
        options = options + opt + " "

    options = options + "-i " + input_file + " "

    for opt in output_opts:
        options = options + opt + " "

    options = options + output_file

    subprocess.run([command] + input_opts + ["-i"] + [input_file] + output_opts + [output_file])


def get_output_config(fmt, infile):
    options = {'h264': h264,
               'h265': h265,
               'vp9': vp9,
               'av1': av1}
    return options[fmt](infile)


def h264(infile):
    basename = os.path.splitext(infile)[0]
    output_file = basename + "_h264.mp4"
    output_opts = ["-c:v", "libx264", "-crf", "30", "-b:v", "0", "-s:v", "1920x1080"]
    return output_file, output_opts


def h265(infile):
    basename = os.path.splitext(infile)[0]
    output_file = basename + "_h265.mp4"
    output_opts = ["-c:v", "libx265", "-crf", "30", "-b:v", "0", "-s:v", "1920x1080"]
    return output_file, output_opts


def vp9(infile):
    basename = os.path.splitext(infile)[0]
    output_file = basename + "_vp9.webm"
    output_opts = ["-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0", "-s:v", "1920x1080"]
    return output_file, output_opts


def av1(infile):
    basename = os.path.splitext(infile)[0]
    output_file = basename + "_av1.mkv"
    output_opts = ["-c:v", "libaom-av1", "-crf", "30", "-b:v", "0", "-s:v", "1920x1080", "-strict", "experimental"]
    return output_file, output_opts


if __name__ == '__main__':
    # encoding_formats = ["h264", "h265", "vp9", "av1"]
    encoding_formats = ["h264", "h265", "vp9"]
    opts = dict()
    opts["AllowOverrideOutput"] = False
    input_file = "video.yuv"
    input_opts = ["-f", "rawvideo", "-pix_fmt", "yuv420p", "-s:v", "1920x1088", "-r", "60"]
    for fmt in encoding_formats:
        (outfile, outopts) = get_output_config(fmt=fmt, infile=input_file)
        encode(input_file=input_file, output_file=outfile, output_opts=outopts, input_opts=input_opts, opts=opts)
