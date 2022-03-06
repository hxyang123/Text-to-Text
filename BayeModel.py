# Useful libraries
import os
import torch
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision

import matplotlib.pyplot as plt
from torchvision import datasets, models, transforms
from torch.utils.data import TensorDataset
import torchvision.transforms as transforms
from torch.utils.data.sampler import SubsetRandomSampler
import matplotlib.pyplot as plt
from PIL import Image


def __main__(img_path):
            
    trans = transforms.Compose([transforms.Resize((224,224)), transforms.ToTensor()])

    #set = torchvision.datasets.ImageFolder(img_path, transform=trans)
    #load = torch.utils.data.DataLoader(set, batch_size=1,num_workers=1,shuffle=True)

    def image_loader(image_name):
        """load image, returns cuda tensor"""
        image = Image.open(image_name)
        image = image.convert('RGB')
        image = trans(image).float()
        image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
        return image  #assumes that you're using GPU

    image = image_loader(img_path)


    #load model
    import torchvision.models
    alexnet = torchvision.models.alexnet(pretrained=True)

    # features = ... load precomputed alexnet.features(img) ...
    class ANN(nn.Module):
        #Since the features are already in place, we will only need a fully connected neural network for the classification
        #I would use three fully connected layers with 2 hidden layers
        #We don't need convolution layer to extract the already extracted features
        def __init__(self):
            self.name = "ANN"
            super(ANN, self).__init__()
            self.fc1 = nn.Linear(256*6*6, 300)
            self.fc2 = nn.Linear(300, 80)
            self.fc3 = nn.Linear(80,15)
            
        def forward(self,x):
            x = x.view(-1,256*6*6)
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x


    best_model = ANN()
    best_model_path = "baye_model"
    #best_model_path = path + "Models/best_model"
    state = torch.load(best_model_path)
    best_model.load_state_dict(state)


    #classify image

    classes = ['0','1','2','3','4','5','6','7','8','9','10','100','1000','10 000','10 000 000']

    features = alexnet.features(image)

    features_tensor = torch.from_numpy(features.detach().numpy())
    #print(features_tensor.shape)
    output = best_model(features_tensor)

    possible_index = np.argwhere(output[0].detach().numpy()>0)
    possible_index = possible_index.T.squeeze(0)

    np_out = output.detach().numpy().squeeze(0)
    out = np_out[possible_index]

    pred = output.max(1, keepdim=True)[1]

    pred_accuracy = out.sum()

    output_str = "Possible numbers:\n"
    
    for i in range(possible_index.shape[0]):
        output_str = output_str + "Number: {0} ".format(classes[possible_index[i]]) + "Confidence: {0}%\n".format(round(out[i]/pred_accuracy*100,2))
    '''
    plt.imshow(np.transpose(image.squeeze(0), (1,2,0)))
    plt.title("Prediction: {0}, Confidence: {1}%".format(classes[pred], round(np_out[pred]/pred_accuracy*100,2)), fontsize = 14)
    print(output_str)
    plt.show()
    '''
    return image, classes[pred], img_path, output_str


