import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import argparse
from sklearn.externals import joblib
from sklearn.svm import SVC
from PIL import Image
import logging
import re

from utils import args_types
from ml.descriptors import image_descriptors

def arg_parser() :

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser_name")
    
    train_parser = subparsers.add_parser("train")
    train_parser.add_argument("-t", "--train_list", type=args_types.existed_file, required=True,
        help="path to the training images")
    train_parser.add_argument("-o", "--output", required=True,
        help="name of output file with svm vector")
    train_parser.add_argument('--descr', choices=image_descriptors.keys(), default='LBP',
        help='Descriptor (default: LBP)')

    test_parser = subparsers.add_parser("test")
    test_parser.add_argument("-e", "--test_list", type=args_types.existed_file, required=True,
        help="path to the tesitng images")
    test_parser.add_argument("-s", "--svm_file", required=True,
        help="name of intput file with svm vector, if you use train/test this arg isn't required")

    train_test_parser = subparsers.add_parser("train/test")
    train_test_parser.add_argument("-t", "--train_list", type=args_types.existed_file, required=True,
        help="path to the training images")
    train_test_parser.add_argument("-e", "--test_list", type=args_types.existed_file, required=True,
        help="path to the tesitng images")
    train_test_parser.add_argument("-o", "--output", required=True,
        help="name of output file with svm vector")
    train_test_parser.add_argument('--descr', choices=image_descriptors.keys(), default='LBP',
        help='Descriptor (default: LBP)')

    return parser.parse_args()

if __name__ == '__main__' :
    
    args = arg_parser()
    action = args.subparser_name

    if action == "train" or action == "train/test" :

        print ("Collecting data")

        data = []
        labels = []

        reg = re.compile('^(.+) (\d+)$')

        with open(args.train_list) as train_file :

            for line in train_file :
                
                tmp_reg = reg.match(line)

                if not tmp_reg :
                    logging.warning("wrong line format:\n    " + line + " Skipped")
                    continue
    
                try :
                    image = Image.open(tmp_reg.groups()[0])
                except FileNotFoundError :
                    raise
    
                hist, _ = image_descriptors[args.descr](image)
    
                labels.append(tmp_reg.groups()[1])
                data.append(hist)

        print ("DONE")
        print ()
        print ("Training")
    
        model = SVC()
        model.fit(data, labels)
    
        joblib.dump(model, args.output, compress=9)

        print ("DONE")
        print ()
        
    if action == "test" or action == "train/test" :
    
        print ("Testing")
        count = 0
        count_right = 0
    
        if action == "train/test" :
            svm_file = args.output
        else :
            svm_file = args.input
    
        with open(svm_file, 'rb') as file :
            model = joblib.load(file)
        
        reg = re.compile('^(.+) (\d+)$')

        with open(args.test_list) as test_file :
    
            for line in test_file :

                count += 1
                tmp_reg = reg.match(line)

                if not tmp_reg :
                    logging.warning("wrong line format:\n    " + line + " Skipped")
                    continue

                try :
                    image = Image.open(tmp_reg.groups()[0])
                except FileNotFoundError :
                    raise
    
                hist, _ = image_descriptors[args.descr](image)
                prediction = model.predict([hist])[0]
            
                if prediction == tmp_reg.groups()[1] :
                    count_right += 1
        
        print ("DONE")
        print ()
    
        print ("accuracy is: " + str(round(count_right/count, 2)))