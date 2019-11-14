#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(
    prog="PalCycleGen",
    epilog="""Dependencies: numpy, matplotlib, tqdm"""
)
parser.add_argument(
    "filenames",
    help="Input filenames (in order).",
    nargs='+'
)
parser.add_argument(
    "-o",
    "--imageOut",
    default="out.png",
    dest="imageOut",
    help="Filename for the generated base image."
)
parser.add_argument(
    "-c",
    "--cycleOut",
    default="cycle.png",
    dest="cycleOut",
    help="Filename for the generate palette cycle."
)

args = parser.parse_args()

import numpy as np
import matplotlib
matplotlib.use('agg')
from matplotlib.image import imread
import matplotlib.pyplot as plt
from tqdm.autonotebook import tqdm,trange

images = []
for filename in args.filenames:
    images.append(imread(filename))

npImages = np.array(images)

cycle = []
newimage = images[0].copy()

def isColorInUse(color):
    colorInUse = False
    
    for cycleEntryOther in cycle:
        if np.allclose(cycleEntryOther[0], color):
            colorInUse = True
            break

    if colorInUse:
        return True

    for x in range(images[0].shape[0]):
        for y in range(images[0].shape[1]):
            for image in images:
                if np.allclose(image[x][y], color):
                    colorInUse = True
                    break

    return colorInUse
    

def addPixel(x, y):
    cycleEntry = np.zeros((len(images) + 1, 4))
    for i in range(len(images)):
        image = images[i]
        cycleEntry[i + 1] = image[x][y]
        
    color = None
    alreadyExists = False
    
    for cycleEntryOther in cycle:
        isMatch = True
        for i in range(1, len(cycleEntryOther)):
            if not np.allclose(cycleEntryOther[i], cycleEntry[i]):
                isMatch = False
                break
        if isMatch:
            color = cycleEntryOther[0]
            alreadyExists = True
            break

    if not alreadyExists:
        while True:
            color = np.random.rand(4)
            color[3] = 1
            if isColorInUse(color):
                continue
            break
                    
        cycleEntry[0] = color
        cycle.append(cycleEntry)
 
    newimage[x][y] = color

for x in trange(images[0].shape[0]):
    for y in range(images[0].shape[1]):
        pixelcolorPrev = None
        for image in (images):
            pixelcolor = image[x][y]
            if pixelcolorPrev is None:
                pixelcolorPrev = pixelcolor
                continue
            if not np.allclose(pixelcolorPrev, pixelcolor):
                addPixel(x, y)
            pixelcolorPrev = pixelcolor
            
cycle = np.array(cycle)

plt.imsave(args.cycleOut, np.rot90(cycle, 3))
plt.imsave(args.imageOut, newimage)