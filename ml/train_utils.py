#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 13:36:01 2016

@author: chernov
"""

import json

import cv2
import numpy as np

def load_base(fn, dataset_dict=None):
    if dataset_dict:
        class_dict = json.load(open(dataset_dict, "r"))
        class_n = len(class_dict)
        a = np.loadtxt(fn, np.float32, delimiter=',',
                       converters={ 0 : lambda ch : class_dict[ch.decode()]})
        samples, responses = a[:,1:], a[:,0]

        return samples, responses, class_n
    else:
        a = np.loadtxt(fn, np.float32, delimiter=',')
        samples, responses = a[:,1:], a[:,0]
        return samples, responses


class LetterStatModel(object):
    train_ratio = 0.8

    def load(self, fn):
        self.model.load(fn)
    def save(self, fn):
        self.model.save(fn)

    def unroll_samples(self, samples):
        sample_n, var_n = samples.shape
        new_samples = np.zeros((sample_n * self.class_n, var_n+1), np.float32)
        new_samples[:,:-1] = np.repeat(samples, self.class_n, axis=0)
        new_samples[:,-1] = np.tile(np.arange(self.class_n), sample_n)
        return new_samples

    def unroll_responses(self, responses):
        if self.class_n  == 1:
            return responses
        sample_n = len(responses)
        new_responses = np.zeros(sample_n*self.class_n, np.int32)
        resp_idx = np.int32( responses + np.arange(sample_n)*self.class_n )
        new_responses[resp_idx] = 1
        return new_responses


class MLP(LetterStatModel):
    def __init__(self, class_n=10):
        self.model = cv2.ml.ANN_MLP_create()
        self.class_n = class_n

    def train(self, samples, responses):
        sample_n, var_n = samples.shape
        new_responses = self.unroll_responses(responses).reshape(-1, self.class_n)
        layer_sizes = np.int32([var_n, 100, 100, 20, self.class_n])

        self.model.setLayerSizes(layer_sizes)
        self.model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        self.model.setBackpropMomentumScale(0.0)
        self.model.setBackpropWeightScale(0.01)
        self.model.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 20, 0.01))
        self.model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)

        self.model.train(samples, cv2.ml.ROW_SAMPLE, np.float32(new_responses))

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)
        

class MLPFloat(LetterStatModel):
    def __init__(self):
        self.model = cv2.ml.ANN_MLP_create()

    def train(self, samples, responses):
        sample_n, var_n = samples.shape
        layer_sizes = np.int32([var_n, 100, 100, 1])

        self.model.setLayerSizes(layer_sizes)
        self.model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        self.model.setBackpropMomentumScale(0.0)
        self.model.setBackpropWeightScale(0.01)
        self.model.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 20, 0.01))
        self.model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)

        self.model.train(samples, cv2.ml.ROW_SAMPLE, np.float32(responses))

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp
        
        
def train_mlp_float(csv_file, outfile):
    samples, responses = load_base(csv_file)
    
    model = MLPFloat()
    
    train_n = int(len(samples)*model.train_ratio)
    
    model.train(samples[:train_n], responses[:train_n])

    print('testing...')
    err_train = np.abs(model.predict(samples[:train_n]).ravel() -
                                     responses[:train_n])
    train_rate = np.mean(err_train)
    err_test = np.abs(model.predict(samples[train_n:]).ravel() -
                                    responses[train_n:])
    test_rate = np.mean(err_test)
    print('train rate: %f  test rate: %f' % (train_rate, test_rate))
    
    model.save(outfile)


def train_mlp(csv_file, dict_file, outfile):
    samples, responses, class_n = load_base(csv_file, dict_file)
    
    model = MLP(class_n)
    
    train_n = int(len(samples)*model.train_ratio)
    
    model.train(samples[:train_n], responses[:train_n])

    print('testing...')
    train_rate = np.mean(model.predict(samples[:train_n]) == 
                                       responses[:train_n].astype(int))
    test_rate  = np.mean(model.predict(samples[train_n:]) == 
                                       responses[train_n:].astype(int))
    print('train rate: %f  test rate: %f' % (train_rate*100, test_rate*100))
    
    model.save(outfile)
