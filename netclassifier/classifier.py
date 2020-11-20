import torch.nn as nn
import torch.nn.functional as F


class Classifier(nn.Module):
    def __init__(self, imsize=128):
        super(Classifier, self).__init__()
        self.imsize = imsize
        self.conv1 = nn.Conv2d(3, 6, 5, padding=(2,2))
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5, padding=(2,2))
        self.fc1 = nn.Linear(int((imsize/4)) * int((imsize/4)) * 16, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 2)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = x.view(-1, int((self.imsize/4)) * int((self.imsize/4)) * 16)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
