import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import colour
import imageutils

# Load filenames and painting information from FreeArt catalogue
def loaddata():
    data = pd.read_csv('./../images/freeart/data.csv')
    data = data.set_index('id')
    data = data[data['year'] > 0]
    artists = pd.read_csv('./../images/freeart/meta.csv')
    artists = artists.set_index('artist')
    data = data.join(artists, on='artist')
    data['decade'] = data['year'].apply(lambda x: x-(x%10))
    return data

# Load and parse image data from list of filenames
def loadimages(imagelist):
    allimages = []
    for f in imagelist:
        fname = './../images/freeart/images/' + f + '.jpg'
        imgdata = imageutils.parseimage(fname)
        imgdata = imageutils.reshapergb(imgdata)
        allimages.append(imgdata)
    allimages = np.concatenate(allimages)
    return allimages

# Generic file reader
def readfile(fname):
    data = []
    with open(fname, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader: data.append(row)
    data = np.stack(data).astype(float)
    return data

def plot2D(f, title):
    plt.matshow(f)
    plt.title(title)
    plt.show()

def plotCIE(colors, title):
    colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False)
    xs = colors[:,0]
    ys = colors[:,1]
    plt.plot(xs, ys, c='gray')
    plt.scatter(xs, ys, s=8, c=range(colors.shape[0]), cmap='RdYlBu')
    colour.plotting.render()

def label3D(ax, title):
    if 'rgb' in title:
        ax.set_xlabel('red')
        ax.set_ylabel('green')
        ax.set_zlabel('blue')
    if 'hsl' in title:
        ax.set_xlabel('hue')
        ax.set_ylabel('saturation')
        ax.set_zlabel('lightness')
    return ax

def plot3D(colors, title):
    xs = colors[:,0]
    ys = colors[:,1]
    zs = colors[:,2]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs, ys, zs, c=range(colors.shape[0]), cmap='RdYlBu')
    plt.plot(xs, ys, zs, c='gray')
    ax = label3D(ax, title)
    fig.suptitle(title)
    plt.show()



