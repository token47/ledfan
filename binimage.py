#!/bin/true

import numpy as np
import polarTransform
import time

import line_profiler

# BIN Images in general:
# image file has no header, just lines in sequence
# colors are interleaved like this to match physical wiring
# color shading is done by alternating on/off on sequential
# lines (that is why the line resolution so higher than cols)
# central lines (low radius on polar image) should be
# artificially darkened to avoid center being too bright
# col brightness r: 1=2/25, 2=5/25, 3=9/25, 4=12/25, 5=22/25 

# FD42 Model:
# 112 pixels, 3 bits per pixel packed into 42 bytes (336 bits)
# double sided with more 112 in opposite direction but that
# second part is just showing a different line simultaneously
# hardware is 21 shift register ICs of 16 outputs to each side
# one frame is 129024 bytes, 3072 lines * 42 bytes per line

DECODE_BITS = ( # 0,1,2 == R,G,B
    "2102102102102102" # Pattern 1
    "1002211002211002" # Pattern 2
    "2110022110022110" # Pattern 3 r:16
    "2110022110022110" # Pattern 3
    "0221100221100221" # Pattern 4
    "0221100221100221" # Pattern 4 r:32
    "1002211002211002" # Pattern 2
    "1002211002211002" # Pattern 2
    "2110022110022110" # Pattern 3 r:48
    "2110022110022110" # Pattern 3
    "0221100221100221" # Pattern 4
    "0221100221100221" # Pattern 4 r:64
    "1002211002211002" # Pattern 2
    "1002211002211002" # Pattern 2
    "2110022110022110" # Pattern 3 r:80
    "2110022110022110" # Pattern 3
    "0221100221100221" # Pattern 4
    "0221100221100221" # Pattern 4 r:96
    "1002211002211002" # Pattern 2
    "1002211002211002" # Pattern 2
    "2110022110022110" # Pattern 3 r:112 (not tested after this point)
    "2110022110022110" # Pattern 3
    "0221100221100221" # Pattern 4
    "0221100221100221" # Pattern 4 r:128
    )

INFO = {
    "G224-42": {
        "radius": 112, # 2 blades make 224 total, 112 each side
        "theta": 3072,
        "center_attenuation": {
            # how many pixels to turn off, each 25 pixels
            0: 23, # 2/25 on
            1: 20, # 5/25 on
            2: 16, # 9/25 on
            3: 13, # 12/25 on
            4:  3, # 22/25 on
            }
        },
    }


class LedFanBinImage():

    # From user
    model = None
    # From info array
    size_radius = None
    size_theta = None
    center_att = None
    # Calculated
    size_radius_packed = None
    frame_size = None
    total_frames = 0
    # Data storage
    bin_movie = None # whole BIN file
    numpy_movie = None # array of npimages for whole movie


    def __init__(self, model):
        self.model = model
        self.size_radius = INFO[model]["radius"]
        self.size_theta = INFO[model]["theta"]
        self.center_att = INFO[model]["center_attenuation"]
        self.size_radius_packed = int(self.size_radius * 3 / 8)
        self.frame_size = self.size_theta * self.size_radius_packed


    # import and export the raw BIN image

    def import_bin_movie(self, data):
        # it can be a string (will open as a file) or a big bytestream (raw image bytes)
        if type(data) is str:
            data = open(data, "rb").read()
        self.bin_movie = data
        self.total_frames = int(len(self.bin_movie) / self.frame_size)


    def export_bin_movie(self, filename=None):
        # it can be a string (will save as a file) or it will be returned by function
        if filename:
            open(filename, "wb").write(self.bin_movie)
        else:
            return self.bin_movie

    # encode (numpu -> BIN) or decode (BIN -> numpy) between ram BIN image and numpy image

    def decode_movie(self):
        print(f"decoding frames:", end="", flush=True)
        self.numpy_movie = []
        for frame_num in range(self.total_frames):
            print(f" {frame_num}", end="", flush=True)
            pos = frame_num * self.frame_size
            frame = self._decode_frame(self.bin_movie[pos:pos+self.frame_size])
            self.numpy_movie.append(np.array(frame))
        print()


    # this algorithm is performance intensive and very slow, but so far I have tested
    # a lot of different approaches and none is faster than this, including bitstream
    # and other modules written in C.
    @line_profiler.profile
    def _decode_frame(self, bin_frame):
        numpy_frame_temp = np.empty((self.size_theta, self.size_radius, 3), dtype=np.uint8)
        for line_count in range(self.size_theta): # each line
            column_count = [ 0, 0, 0 ] # accumulators for RGB bit pos
            for i in range(self.size_radius_packed):
                byte = bin_frame[line_count * self.size_radius_packed + i]
                for j in range(8):
                    dest_color = int(DECODE_BITS[i*8+j])
                    x = self.size_radius - column_count[dest_color] - 1
                    v = 255 if byte & (128>>j) else 0
                    numpy_frame_temp[line_count][x][dest_color] = v
                    column_count[dest_color] += 1
        return numpy_frame_temp


    def encode_movie(self):
        print(f"encoding frames:", end="", flush=True)
        self.bin_movie = b""
        for frame_num in range(self.total_frames):
            print(f" {frame_num}", end="", flush=True)
            self.attenuate_center_radiuses(self.numpy_movie[frame_num]) # in place
            frame = self._encode_frame(self.numpy_movie[frame_num])
            self.bin_movie += frame
        print()


    def _encode_frame(self, numpy_frame):
        # this is broken, find the issue and fix
        bin_frame_temp = bytearray()
        for line_count in range(self.size_theta):
            column_count = [ 0, 0, 0 ] # accumulators for RGB bit pos
            for i in range(0, self.size_radius * 3, 8):
                byte = 0
                for j in range(8):
                    dest_color = int(DECODE_BITS[i+j])
                    o = numpy_frame[line_count][column_count[dest_color]][dest_color]
                    v = 1 if o >= 128 else 0
                    byte += v << (7-j)
                    column_count[dest_color] += 1
                bin_frame_temp.extend(byte.to_bytes(1, byteorder="little"))
        return bin_frame_temp


    # import and export the numpy (array of) images

    def import_numpy_movie(self, numpy_movie):
        self.numpy_movie = numpy_movie
        self.total_frames, shape_t, shape_r, shape_c = numpy_movie.shape
        print(f"importing numpy movie with {self.total_frames} frames, "
            f"{shape_t}:{shape_r}:{shape_c} resolution")


    def export_numpy_movie(self):
        return self.numpy_movie


    def attenuate_center_radiuses(self, numpy_frame):
        # implement a better interleaving
        return
        for r in range(len(self.center_att)):
            for t1 in range(0, self.size_theta, 25):
                for t2 in range(0, self.center_att[r]):
                    t = t1 + t2
                    if t < self.size_theta:
                        numpy_frame[t][self.size_radius-r-1][0] = 0
                        numpy_frame[t][self.size_radius-r-1][1] = 0
                        numpy_frame[t][self.size_radius-r-1][2] = 0


    # more specialized ways of getting images

    def get_numpy_frame(self, frame_num, rotated=0):
        if frame_num > self.total_frames:
            raise Exception(f"Frames must be <= {self.total_frames}")
        # no rotation by default
        return np.rot90(self.numpy_movie[frame_num], k=rotated, axes=(0,1))


    def get_numpy_frame_cartesian(self, frame_num):
        image_cart, _ = polarTransform.convertToCartesianImage(
            self.get_numpy_frame(frame_num),
            initialAngle=np.pi*0.5,
            finalAngle=np.pi*2.5,
            hasColor=True)
        return image_cart
