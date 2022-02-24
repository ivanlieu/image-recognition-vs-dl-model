import torch
from torchvision import datasets, transforms
from torch import nn
import numpy as np

class cnnEvalModel():
    def __init__(self, modelFilePath):

        self.images = None
        self.labels = None
        self.logps = None
        self.output = None
        self.pred = None
        self.img = None
        self.imgOut = None

        # torch.manual_seed(0)  # set for repeatable result
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

        np.random.seed(0)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(self.device)

        mean, std = (0.5,), (0.5,)

        # Create a transform and normalise data
        transform = transforms.Compose([transforms.ToTensor(),
                                        transforms.Normalize(mean, std)
                                      ])
        # Download FMNIST test dataset and load test data
        self.testset = datasets.FashionMNIST('~/.pytorch/FMNIST/', download=True, train=False, transform=transform)
        self.testloader = torch.utils.data.DataLoader(self.testset, batch_size=1, shuffle=True) 

        self.modelPath = modelFilePath

        self.model = torch.jit.load(self.modelPath)
        self.model.eval()

    def denormalize(tensor):
        """denormalizes a supplied tensor and returns it"""
        tensor = tensor*0.5 + 0.5
        return tensor

    def runModel(self, count):
        """Runs the cnn model based on the iteration count for test set and converts model tensor outputs
        to regular python data types
            Accepts count as an integer"""

        tempCount = 0
        # iterating to the number of counts in arg count
        for batch, (tempImg, tempLabel) in enumerate(self.testloader, 1):
            
            tempCount += 1
            
            if tempCount == count:
                self.images = tempImg
                self.labels = tempLabel

                break

        # send image and label tensors to GPU memory
        self.images = self.images.to(self.device)
        self.labels = self.labels.to(self.device)

        # run model on loaded image and label data
        self.logps = self.model(self.images)

        # parse model output
        self.output = torch.exp(self.logps)
        self.pred = torch.argmax(self.output, 1)

        # copy 1-D tensor to cpu memory and convert to python integer
        self.pred = self.pred.cpu().item()
        self.labels = self.labels.cpu().item()

        # copy image data to cpu memory
        self.img = self.images.cpu()

    def runImagePlotData(self):
        """processes and returns image tensor data in a form ready to be plotted with matplotlib"""
        self.imgOut = self.img.view(28, -1)
        self.imgOut = cnnEvalModel.denormalize(self.imgOut)



