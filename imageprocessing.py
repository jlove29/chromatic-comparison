import pandas as pd
import numpy as np
import imageutils

BATCHSZ = 100

# Calculate dominant wavelength and saturation of images in WGA data
# Performed in batches due to computational intensity
def domsat():
    imagedata = pd.read_csv('./../images/freeart/data.csv').set_index('id')
    batches = [subset[i:i+BATCHSZ] for i in range(0, len(imagedata), BATCHSZ)]
    i = 0
    for batch in batches:
        i += 1
        images = []
        for pidx in batch:
            if pidx in SKIPLIST: continue
            imagefile = './../images/freeart/images/' + pidx + '.jpg'
            image = imageutils.parseimage(imagefile)
            images.append(image)
        images = np.concatenate(images)
        xy = imageutils.convertxy(images)
        d, s = imageutils.stats(xy)
        writefile(d, 'dominant')
        writefile(s, 'saturation')
        print(i)

# General utility to save csv files with all works in xy, hsl, rgb
def convertspaces():
    imagedata = pd.read_csv('./../images/freeart/data.csv').set_index('id')
    for era in ['Rococo', 'Neoclassicism']:
        subset = list(imagedata[imagedata['era'] == era].index)
        images = []
        for pidx in subset:
            imagefile = './../images/freeart/images/' + pidx + '.jpg'
            image = imageutils.parseimage(imagefile)
            images.append(image)
        images = np.concatenate(images)
        rgb = imageutils.reshapergb(images)
        xy = imageutils.convertxy(rgb)
        hsl = imageutils.converthsl(rgb)
        np.savetxt('./values/xy/' + era + '-xy.csv', xy, delimiter=',')
        np.savetxt('./values/hsl/' + era + '-hsl.csv', hsl, delimiter=',')
        np.savetxt('./values/rgb/' + era + '-rgb.csv', rgb, delimiter=',')