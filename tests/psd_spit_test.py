import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from utils.psd import psd_to_images
from PIL import Image

import unittest
from psd_tools.exceptions import Error as psd_error
from PIL import ImageChops

class TestPsdParser(unittest.TestCase) :
    def test_file(self) :

        images = psd_to_images('test.psd', True)
        self.assertIsInstance(images, type(i for i in range(1)), 'Function \'psd_to_images\' returns not generator')


        count = 0
        for i in images :
            count += 1
        self.assertEqual(count, 3, 'Function \'psd_to_images\' returns another number of layers, then in test file')
        
        test_images = []
        isTrueImg = False
        images = psd_to_images('test.psd', True)

        for i in (range(3)) :
            test_images.append(Image.open('resources/merged_' + str(i) + '.png'))
        
        for image in images :

            for img in test_images :
                if(ImageChops.difference(image, img).getbbox() is None) :
                    isTrueImg = True
                    break

            self.assertTrue(isTrueImg, 'Function \'psd_to_images\' returns another images, then in test file. merge_group=True')
            isTrueImg = False


        test_images = []
        images = psd_to_images('test.psd', False)

        for i in (range(4)) :
            test_images.append(Image.open('resources/un_merged_' + str(i) + '.png'))
        
        for image in images :
            for img in test_images :
                if(ImageChops.difference(image, img).getbbox() is None) :
                    isTrueImg = True
                    break
                    
            self.assertTrue(isTrueImg, 'Function \'psd_to_images\' returns another images, then in test file. merge_group=False')
            isTrueImg = False


    def test_fails(self) :
        try :
            for img in psd_to_images('not_psd.file') :
                self.assertTrue(False, 'Problems with FileNotFoundError exeption ')

        except FileNotFoundError :
            pass

        try :
            for img in psd_to_images('testNotPsd.psd') :
                self.assertTrue(False, 'Problems with psd_error exeption, when file is not in .psd extention')

        except psd_error :
            pass