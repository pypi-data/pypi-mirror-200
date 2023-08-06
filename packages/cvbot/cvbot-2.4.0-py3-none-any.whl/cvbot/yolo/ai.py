from os import getcwd, chdir, listdir
from sys import path
from os.path import join, dirname, isfile
from cv2 import cvtColor, COLOR_BGRA2BGR
from .detect import init_model as _init_model
from .detect import detect as _detect 
from .hprocess import _cprocess
from torch import max as _max
import pickle

classifiers = {}

def init_model(path):
    #print(join(getcwd(), path))
    _init_model(path)
#
#    fd = join(MDLS, obj)
#    clfr = join(fd, "{}_{}.pth".format(obj, state))
#    if isfile(clfr):
#        with open(clfr, "rb") as f:
#            classifiers[state] = pickle.load(f)
#            classifiers[state].eval()
#
#        return
#
#    print("Classifier not found in imported classifiers for [{}]".format(obj))

def detect_states(snp, states=[]):
    res = {}

    if len(states):
        trg = list(filter(lambda x: x[0] in states, classifiers.items()))
    else:
        trg = classifiers.items()
    
    for state, clfr in trg:
        outputs = clfr(_cprocess(cvtColor(snp.img, COLOR_BGRA2BGR), clfr.size))
        _, pred = _max(outputs.data, 1)
        res[state] = clfr.names[int(pred)]

    return res

def detect(im, thresh=0.25):
    img = cvtColor(im.img, COLOR_BGRA2BGR)
    results = _detect(img, thresh)

    for i in range(len(results)):
        result = results[i]
        x, y, w, h = result[0][0], result[0][1], result[0][2] - result[0][0], result[0][3] - result[0][1]
        results[i] = (x, y, w, h), result[1:]

    return results
