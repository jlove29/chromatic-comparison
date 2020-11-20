import torch
import torch.optim as optim
import torch.nn as nn
import os
import imutils
import load_data
from classifier import Classifier

loader = imutils.ImageLoader()
path = './../images/scrapers/datasets/'
paths = [path + x for x in os.listdir(path)]
dataloaders = load_data.load_data(path, loader)

model = Classifier(imsize=128)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

nepochs = 100
for epoch in range(nepochs):
    running_loss = 0.0
    for i, data in enumerate(dataloaders['train'], 0):
        inputs, labels = data
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if i % 20 == 19:
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 20))
            running_loss = 0.0
PATH = './trained-models/model.pth'
torch.save(model.state_dict(), PATH)

dataiter = iter(dataloaders['val'])
images, labels = dataiter.next()
outputs = model(images)
_, predicted = torch.max(outputs, 1)
print(predicted)
print(labels)
