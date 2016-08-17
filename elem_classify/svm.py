import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import utils.version_check

from skimage import feature
import numpy as np
from sklearn.svm import LinearSVC
from imutils import paths    
import argparse
import cv2
import _pickle as cPickle
 
class lbp :
    def __init__(self, numPoints, radius):
        self.numPoints = numPoints
        self.radius = radius
 
    def describe(self, image, eps=1e-7):
        lbp = feature.local_binary_pattern(image, self.numPoints,
            self.radius, method="uniform")
        (hist, _) = np.histogram(lbp.ravel(),
            bins=np.arange(0, self.numPoints + 3),
            range=(0, self.numPoints + 2))

        hist = hist.astype("float")
        hist /= (hist.sum() + eps)
 
        return hist

def arg_parser() :
    ap = argparse.ArgumentParser()
    ap.add_argument("action", help="train, test, train/test")
    ap.add_argument("-t", "--train_list", default=None,
        help="path to the training images")
    ap.add_argument("-e", "--test_list", required=True, 
        help="path to the tesitng images")
    ap.add_argument("-o", "--output", default="data.svm",
        help="name of output file with svm vector")
    ap.add_argument("-i", "--input",
        help="name of intput file with svm vector")

    return vars(ap.parse_args())



args = arg_parser()

desc = lbp(24, 8)
data = []
labels = []

action = args["action"]

if (not(action == "train" or  action == "test" or action == "train/test")) :
    raise TypeError("Wrong action")

if(action == "train" or action == "train/test") :

    print("Training")

    if(args["train_list"] == None) :
        raise TypeError("Train file doesn't find")

    train = open(args["train_list"])

    for line in train :
        image = cv2.imread(line.split(" ")[0])

        if (isinstance(image, type(None))) :
            raise FileNotFoundError("Can't open image: " + line.split(" ")[0])

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = desc.describe(gray)
    
        labels.append(line.split(" ")[1])
        data.append(hist)

    model = LinearSVC(C=100.0)
    model.fit(data, labels)

    with open(args["output"], 'wb') as file :
        cPickle.dump(model, file)

    print("Training done")
    
if (action == "test" or action == "train/test") :

    print("Testing")
    count = 0
    count_right = 0

    test = open(args["train_list"])
    
    if (action == "train/test") :
        svm_file = args["output"]
    else :
        svm_file = args["input"]

    with open(svm_file, 'rb') as file :
        model = cPickle.load(file)

    for line in test :
    
        count += 1
    
        image = cv2.imread(line.split(" ")[0])

        if (isinstance(image, type(None))) :
            raise FileNotFoundError("Can't open image: " + line.split(" ")[0])

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = desc.describe(gray)
        prediction = model.predict(hist)[0]

        print (prediction, line.split(" ")[1])
    
        if(prediction == line.split(" ")[1]) :
            count_right += 1
    
    print ("Testing done")

    print("accuracy is: " + str(round(count_right/count, 2)))