import colour
from colour.utilities import first_item
import numpy as np
from PIL import Image


newsz = 100
COLORSPACE = first_item(colour.plotting.filter_RGB_colourspaces('sRGB').values())
WHITE = COLORSPACE.whitepoint
RGBMT = COLORSPACE.RGB_to_XYZ_matrix

def parseimage(fname):
    image = Image.open(fname)
    image = image.resize((newsz, newsz))
    image = np.array(image)/256
    return image

def reshapergb(mat):
    x, y, _ = mat.shape
    mat = mat.reshape((x*y, 3))
    return mat

def converthsl(mat):
    image_HSL = colour.RGB_to_HSL(mat)
    return image_HSL

def convertxy(mat):
    image_XYZ = colour.models.RGB_to_XYZ(mat, WHITE, WHITE, RGBMT)
    image_XY = colour.models.XYZ_to_xy(image_XYZ, WHITE)
    return image_XY