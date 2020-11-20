import torch
import torchvision.transforms as transforms
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os

class ImageLoader:
    def __init__(self, device='cpu'):
        self.imsize = 128 # TODO: change back
        self.device = device
        if self.device != 'cpu':
            self.imsize = 512
        self.loader = transforms.Compose([
            transforms.CenterCrop(self.imsize),
            transforms.ToTensor()])
    def load_img(self, image_name):
        image = Image.open(image_name)
        if image_name[-3:] == 'png':
            image = image.convert('RGB')
        image = self.loader(image).unsqueeze(0)
        if image.shape[1] == 4: image = image[:,:3,:,:]
        return image.to(self.device, torch.float)
    def unload_img(self):
        return transforms.ToPILImage()
    def imconvert(self, tensor, title=None):
        image = tensor.cpu().clone()
        image = image.squeeze(0)
        image = self.unload_img()(image)
        return image
    def load_images(self, files):
        images = []
        labels = []
        categories = [files + x for x in os.listdir(files) if x[0] != '.']
        for c in range(len(categories)):
            catimgs = os.listdir(categories[c])
            catimgs = [categories[c] + '/' + x for x in catimgs if x[0] != '.']
            for fname in catimgs:
                image = self.load_img(fname)
                images.append(image)
                labels.append(c)
        return images, labels



