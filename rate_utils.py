import os
import inspect
from time import sleep

import cv2
from selenium import webdriver

from assert_utils import is_image, is_tuple
from pixel_difference import *


SLEEPING_TIME = 3   #sec.
DEFAULT_SCRN_PATH = '.temporary_sreenshot'


#DO NOT FORGOT TO CLOSE BROWSER AFTER USING!
Driver = webdriver.Firefox

def make_screenshot(url, path=DEFAULT_SCRN_PATH, driver=None):
    ''' 
    Save screenshot of page with url to path 
    
    Parameters
    ----------
    @url   <str>  URL of page, which should be save
    @path  <str>  Specify path, where img 
                                should be saved, if you want to save it
    driver <selenium.webdriver.Remote> Specify if you don't want to 
                                                    create a new driver
    ----------
    Return <cv2.image>  Screenshot class 'numpy.ndarray'
    '''
    assert isinstance(url, str)
    assert isinstance(path, str)
    assert isinstance(driver, webdriver.Remote) or driver is None

    driver_sp = driver is not None
    need_save = (path != DEFAULT_SCRN_PATH)

    if not driver_sp:
        driver = Driver() 
    try:
        driver.get(url)
        sleep(SLEEPING_TIME)
        driver.get_screenshot_as_file(path)
    finally:
        if not driver_sp:
            driver.close()

    img = cv2.imread(path)
    if not need_save:
        os.remove(DEFAULT_SCRN_PATH) #remove img, if the path 
                                                #hasn't been specified
    return img

def get_html_source(url, path=None, driver=None):
    ''' 
    Save screenshot of page with url to path

    Parameters
    ----------
    @url   <str>  URL of page, which should be save
    @path  <str>  Specify path, where html source 
                                should be saved, if you want to save it
    @driver <selenium.webdriver.Remote> Specify if you don't want to
                                                    create a new driver
    ----------
    Return <str> HTML source
    '''
    
    driver_specifyed = driver is not None
    need_save = path is not None

    assert isinstance(url, str)
    assert isinstance(path, str) or not need_save
    assert isinstance(driver, webdriver.Remote) or not driver_specifyed

    if not driver_specifyed:
        driver = Driver() 
    try:
        driver.get(url)
        sleep(SLEEPING_TIME)
        html_source = driver.page_source
    finally:
        if not driver_specifyed:
            driver.close()
    if need_save:
        with open(path , 'w') as f:
            f.write(html_source)
    return html_source

def resize_img_w(img, new_w):
    ''' 
    This is the function that aims to change width of img, 
    without changing the aspect ratio.

    Parameters
    ----------
    @img    <cv2.image>  Image to resize
    @new_w  <int>        Width of the new image.If new_w = 0 - no resize
    ----------
    Return <cv2.image>  Resized image
    '''
    assert isinstance(new_w, int)
    assert is_image(img)

    if new_w == 0:
        return img
    scale = new_w / img.shape[1]
    return cv2.resize(img, None, fx=scale, fy=scale)

def img_pixel_comparise(sample, img, width=300
                                    , max_diff_func=max_diff_func_color
                                    , diff_func=diff_func_color):
    '''
    This is the function that aims to compute percentage of 
    matched pixels in a two given images.

    Parameters
    ----------
    @sample  <cv2.image>  Sample image
    @img     <cv2.image>  Image for comparison
    @width   <int>        Width of resized image, before comparise.
                            If 0 - no resize
    @max_diff_func
            <function>   Compute max pixels difference
                         Takes 2 pixels and return <int>
    @diff_func 
            <function>   Compute pexels difference
                         Takes 2 pixels and return <int>
    -   ---------
    Return  <float>      Percentage of matching from [0, 1]
    '''
    assert is_image(sample) and is_image(img)
    assert isinstance(width ,int)
    assert inspect.isfunction(max_diff_func)
    assert inspect.isfunction(diff_func)
    
    
    h, w = sample.shape[0], sample.shape[1]
    img = cv2.resize(img, (w, h))
    img = resize_img_w(img, width)
    sample = resize_img_w(sample, width)
    h, w = sample.shape[0], sample.shape[1]
    max_diff = 0.0
    diff = 0.0
    for x in range(h):
        for y in range(w):
           max_diff += max_diff_func(sample[x][y], img[x][y]) 
           diff += diff_func(sample[x][y], img[x][y]) 
    return 1.0 - diff / max_diff

def html_pixel_comparise(sample_path, html_path):
    ''' 
    This is the function that aims to compute percentage of matched 
    pixels in a two given images. Both images is generating 
    from html code.

    Parameters
    ----------
    @sample_path  <cv2.image>  Path to the sample image
    @html_path    <cv2.image>  Path to the html code 
                                                of image to comparison
    ----------
    Return       <float>      Percentage of matching from [0, 1]
    '''
    assert isinstance(sample_path, str)
    assert isinstance(html_path, str)

    driver = Driver()
    try:
        img = make_screenshot(html_path, driver=driver)
        sample = make_screenshot(sample_path, driver=driver)
    finally:
        driver.close()

    return img_pixel_comparise(sample, img)

def img_edges_comparise(sample, img, tresholds=(50, 100), width=50):
    ''' 
    This is the function that aims to compute percentage of 
    matched in a two given images.

    Parameters
    ----------
    @sample     <cv2.image>  Sample image
    @img        <cv2.image>  Image for comparison
    @tresholds  <(int, int)> Thresholds for the hysteresis procedure.
    @width      <int>        Width of resized image, before comparise.
                            If 0 - no resize
    ----------
    Return  <float>      Percentage of matching from [0, 1]
    '''
    assert is_image(sample) and is_image(img)
    assert is_tuple(tresholds, 2, int)
    assert isinstance(width, int)
    
    h, w = sample.shape[0], sample.shape[1]
    img = cv2.resize(img, (w, h))
    treshold1, treshold2 = tresholds
    img_edges = cv2.Canny(img, treshold1, treshold2)
    smp_edges = cv2.Canny(sample, treshold1, treshold2)
    return img_pixel_comparise(smp_edges, img_edges
                                    , max_diff_func=max_diff_func_edges
                                    , diff_func=diff_func_color)

def compare_img_with_html(sample_path, html_path, img_comp_func):
    ''' 
    This is the function that aims to compute percentage of 
    matched pixels in a two given images. Sample image is reading from 
    specified path. Image for comparison is generating from html code.

    Parameters
    ----------
    @sample_path    <cv2.image>  Path to the sample image
    @html_path      <cv2.image>  Path to the html code 
                                                of image to comparison
    @img_comp_func  <function>   Function which takes two image and 
                                                        compare them
    ----------
    Return          <float>      Percentage of matching from [0, 1]
    '''
    assert isinstance(sample_path, str)
    assert isinstance(html_path, str)
    assert inspect.isfunction(img_comp_func)

    sample = cv2.imread(sample_path)
    img = make_screenshot(html_path)
    return img_comp_func(sample, img)
