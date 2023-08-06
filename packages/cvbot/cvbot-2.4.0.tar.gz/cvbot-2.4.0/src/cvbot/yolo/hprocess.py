from utils.datasets import letterbox
import numpy as np
from torch import from_numpy, cuda
from torch import device as _device
from torchvision.transforms import transforms


def _process(img, stride):
    nimg = img.copy()
    nimg = letterbox(nimg, 640, stride=stride)[0]

    # Convert
    nimg = nimg[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    nimg = np.ascontiguousarray(nimg)

    return nimg

def _cprocess(im0, sz):
    img = im0[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416

    device = _device("cuda:0" if cuda.is_available() else "cpu")

    img = np.ascontiguousarray(img)
    img = from_numpy(img).to(device)

    rtrans  = transforms.Resize((sz, sz))
    hftrans = transforms.RandomHorizontalFlip()
    ntrans  = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))

    img = img.float()
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    img = rtrans(img) 
    img = hftrans(img) 
    img = ntrans(img) 

    return img
