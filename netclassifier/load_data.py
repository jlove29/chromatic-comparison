import torch
from torch.utils.data import Dataset, DataLoader
import random
import os

# Reads filenames from different folders
def read_from_folders(dpath):
    folders = os.listdir(dpath)
    fnames = []
    for fol in folders:
        if fol[0] == '.':
            continue
        fpath = dpath + fol
        fnames += [fpath + x for x in os.listdir(fpath)]
    return fnames

def load_paths(dpath, n=None):
    fnames = os.listdir(dpath)
    fpaths = []
    for x in fnames:
        if x[-3:] != 'jpg':
            continue
        fpaths.append(dpath + x)
    if n == None:
        n = len(fpaths)
    sample = random.sample(fpaths, n)
    return sample, n

class ImageData(Dataset):
    def __init__(self, image_list, labels):
        self.image_list = torch.stack(image_list)
        self.labels = labels
        self.nimgs = len(image_list)
    def __len__(self):
        return self.nimgs
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        xs = self.image_list[idx]
        xs = xs[0,:,:,:]
        ys = self.labels[idx]
        sample = xs, ys
        return sample

def split_data(X, Y):
    splits = { 'train': 0.8, 'val': 0.2}
    nimgs = len(Y)
    tX = X[int(nimgs*splits['train']):]
    tY = Y[int(nimgs*splits['train']):]
    vX = X[int(nimgs*splits['val']):]
    vY = Y[int(nimgs*splits['val']):]
    return tX, tY, vX, vY

def load_data(paths, img_loader, labels=None, device='cpu'):
    if labels is None: labels = [x for x in range(len(paths))]
    batch_size = 10
    imgs, labels = img_loader.load_images(paths)
    toshuffle = list(zip(imgs, labels))
    random.shuffle(toshuffle)
    imgs, labels = zip(*toshuffle)
    imgs = list(imgs)
    labels = list(labels)
    tX, tY, vX, vY = split_data(imgs, labels)
    train_dataset = ImageData(tX, tY)
    val_dataset = ImageData(vX, vY)
    dataloaders = {
            'train': torch.utils.data.DataLoader(
                train_dataset, batch_size=batch_size, shuffle=True),
            'val': torch.utils.data.DataLoader(
                val_dataset, batch_size=batch_size, shuffle=True)
            }
    return dataloaders


