from states import CLFF, CWD
from time import sleep
from os import listdir, system
from os.path import join, isdir, isfile
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.transforms import transforms
import torch.nn as nn
import torch
import torch.nn.functional as F
from torch.optim import Adam
from torch.autograd import Variable
import pickle


MDLS  = join(CWD[:-8], "custom_models")

def save_prefs(bs, eps, imsz):
    """
    int, int, int -> bool
    Write given Batch Size and Epochs values to the preferences file
    Return False - Save process wasn't successful
    """
    try:
        with open(join(CLFF, "pref.txt"), "w") as f:
            f.write("{},{},{}".format(bs, eps, imsz))
        return True
    except:
        return False

def read_prefs():
    """
    None -> int, int, int
    Read Batch Size and Epochs values from the preferences file
    """
    with open(join(CLFF, "pref.txt"), "r") as f:
        return [int(x) for x in f.read().split(",")]

# Define a convolution neural network
class Network(nn.Module):
    def __init__(self, n_clss, sz):
        super(Network, self).__init__()
        
        self.network = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(128, 256, kernel_size = 3, stride = 1, padding = 1),
            nn.ReLU(),
            nn.Conv2d(256,256, kernel_size = 3, stride = 1, padding = 1),
            nn.ReLU(),
            nn.MaxPool2d(2,2),
            
            nn.Flatten(),
            nn.Linear(256 * ((sz // 8) ** 2), 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512 , n_clss)
        )

        self.names = []
        self.size = sz

    def forward(self, input):
        return self.network(input) 

def testAccuracy(model, ldr, device):
    model.eval()
    accuracy = 0.0
    total = 0.0
    
    with torch.no_grad():
        for data in ldr:
            images, labels = data
            images = images.to(device)
            labels = labels.to(device)
            # run the model on the test set to predict labels
            outputs = model(images)
            # the label with the highest energy will be our prediction
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            accuracy += (predicted == labels).sum().item()
    
    # compute the accuracy over all test images
    accuracy = (100 * accuracy / total)
    return(accuracy)

def saveModel(model, path, obj, state):
    file = join(path, "{}_{}.pth".format(obj, state))
    with open(file, "wb") as f:
        pickle.dump(model, f)

def train(path, obj, state):
    """
    str, str -> bool
    Train a classifier using images and labels in 'path' 
    """
    global transformations

    btchsz, epochs, imgsz = read_prefs()

    transformations = transforms.Compose([
        transforms.Resize((imgsz, imgsz)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])


    try:
        trn_ldr = DataLoader(ImageFolder(join(path, "train"), transform=transformations), batch_size=btchsz, shuffle=True)
        tst_ldr = DataLoader(ImageFolder(join(path,  "test"), transform=transformations), batch_size=btchsz, shuffle=True)

        model = Network(len(listdir(join(path, "train"))), imgsz)
        loss_fn = nn.CrossEntropyLoss()
        optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

        best_accuracy = 0.0

        # Define your execution device
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print("The model will be running on", device, "device")
        # Convert model parameters and buffers to CPU or Cuda
        model.to(device)
        model.names = list(sorted(listdir(join(path, "train"))))

        for epoch in range(epochs):  # loop over the dataset multiple times
            running_loss = 0.0
            running_acc = 0.0
            model.train()

            for i, (images, labels) in enumerate(trn_ldr, 0):
                # get the inputs
                images = Variable(images.to(device))
                labels = Variable(labels.to(device))

                # zero the parameter gradients
                optimizer.zero_grad()
                # predict classes using images from the training set
                outputs = model(images)
                # compute the loss based on model output and real labels
                loss = loss_fn(outputs, labels)
                # backpropagate the loss
                loss.backward()
                # adjust parameters based on the calculated gradients
                optimizer.step()

                # Let's print statistics for every 10 images
                running_loss += loss.item()     # extract the loss value
                if i % 10 == 9:    
                    # print every 10 (twice per epoch) 
                    print('[%d, %5d] loss: %.3f' %
                        (epoch + 1, i + 1, running_loss / 10))
                    # zero the loss
                    running_loss = 0.0

            # Compute and print the average accuracy fo this epoch when tested over all 10000 test images
            accuracy = testAccuracy(model, tst_ldr, device)
            print('For epoch', epoch+1,'the test accuracy over the whole test set is %d %%' % (accuracy))
            
            # we want to save the model if the accuracy is the best
            if accuracy > best_accuracy:
                saveModel(model, path, obj, state)
                best_accuracy = accuracy

        print("\n Best accuracy is %d%%\n" % (best_accuracy))
        return True
    except Exception as e:
        print(e)
        return False


def train_classifier():
    """
    None -> bool
    Train a classifer for an object given by the user
    """
    obj = ""
    while obj == "":
        obj = input("\nWhat object to train classifiers for? ")

    state = ""
    while state == "":
        state = input("\nWhich state for [{}] you want to train? ".format(obj))

    fldr = join(CLFF, obj) 
    if isdir(fldr):
        stp = join(fldr, state)
        stlbls = join(stp, "labels.txt")
        clsfr = join(stp, "{}_{}.pth".format(obj, state))
        if isfile(stlbls):
            if isfile(clsfr):
                ans = input("\nA classifier is already trained for object [{}] and state [{}], do you want to overwrite it? (y/n) ".format(obj, state))
                if ans != "y":
                    return True
                elif system('del "{}"'.format(clsfr)) == 0:
                    print("\nPreparing files for training...")
                    sleep(10)
                else:
                    return False

            if train(stp, obj, state):
                return True
        else:
            print("\n Image preparation wasn't complete, please add state [{}] again".format(state))

    return False

def import_model(fd, mpth, obj):
    """
    str, str, str -> bool
    Copy and save the trained model from given paths to the main folder
    Return False - Import wasn't successful
    """
    try:
        tgfl = join(MDLS, obj, mpth[(len(fd) + 1):])

        if system('copy "{}" "{}"'.format(mpth, tgfl)) == 0:
            return True 
    except:
        pass

    return False


def import_classifier():
    """
    None -> bool
    Import the last trained classifiers
    Return False - Import wasn't successful 
    """
    obj = ""
    while obj == "":
        obj = input("\nWhat object to import a classifier for? ")

    state = ""
    while state == "":
        state = input("\nWhich state classifier for [{}] do you want to import? ".format(obj))

    fldr = join(CLFF, obj, state)
    mfl = join(fldr, "{}_{}.pth".format(obj, state))
    if isdir(fldr):
        if isfile(mfl):
            return import_model(fldr, mfl, obj)

    return False
