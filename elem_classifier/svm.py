import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import argparse
import cv2
import _pickle as cPickle
from ml.descriptors import image_descriptors
from utils import args_types
from PIL import Image
from sklearn.svm import LinearSVC
import logging

def arg_parser() :
    ap = argparse.ArgumentParser()
    ap.add_argument("action", help="train, test, train/test")
    ap.add_argument("-t", "--train_list", type=args_types.existed_file, default=None,
        help="path to the training images")
    ap.add_argument("-e", "--test_list", type=args_types.existed_file,
        help="path to the tesitng images")
    ap.add_argument("-o", "--output",
        help="name of output file with svm vector")
    ap.add_argument("-i", "--input",
        help="name of intput file with svm vector, if you use train/test this arg isn't required")
    ap.add_argument('--descr', choices=image_descriptors.keys(), default='LBP', 
        help='Descriptor (default: LBP)')

    return vars(ap.parse_args())



args = arg_parser()

action = args["action"]

if (not(action == "train" or  action == "test" or action == "train/test")) :
    raise TypeError("Wrong action")

if(action == "train" or action == "train/test") :

    print("Collecting data")

    if(args["train_list"] == None) :
        raise TypeError("Train file " + args["train_list"] + " doesn't find")

    train = open(args["train_list"])
    
    data = []
    labels = []

    for line in train :
        try:
            image = Image.open(line.split(" ")[0])
        except FileNotFoundError:
            raise

        if (isinstance(image, type(None))) :
            raise FileNotFoundError("Can't open image: " + line.split(" ")[0])

        hist, _= image_descriptors[args['descr']](image)

        labels.append(line.split(" ")[1])
        data.append(hist)

    print("DONE")
    print()
    print("Training")


    model = LinearSVC(C=100.0)
    model.fit(data, labels)

    if (args["output"] == None) :
        logging.warning("Missing name of output data. Default filename is \"data.svm\"")
        args["output"] = 'data.svm'

    with open(args["output"], 'wb') as file :
        cPickle.dump(model, file)

    print("DONE")
    print()
    
if (action == "test" or action == "train/test") :

    print("Testing")
    count = 0
    count_right = 0

    if(args["test_list"] == None) :
        raise TypeError("Test file " + args["test_list"] + " doesn't find")

    test = open(args["train_list"])
    
    if (action == "train/test") :
        svm_file = args["output"]
    else :
        svm_file = args["input"]

    with open(svm_file, 'rb') as file :
        model = cPickle.load(file)

    for line in test :
    
        count += 1
    
        try:
            image = Image.open(line.split(" ")[0])
        except FileNotFoundError:
            raise

        if (isinstance(image, type(None))) :
            raise FileNotFoundError("Can't open image: " + line.split(" ")[0])

        hist, _ = image_descriptors[args['descr']](image)
        prediction = model.predict([hist])[0]
    
        if(prediction == line.split(" ")[1]) :
            count_right += 1
    
    print ("DONE")
    print()

    print("accuracy is: " + str(round(count_right/count, 2)))