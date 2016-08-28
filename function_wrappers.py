import inspect

import cv2
from selenium import webdriver

from rate_utils import make_screenshot
from assert_utils import is_existed_path

#DO NOT FORGOT TO CLOSE BROWSER AFTER USING!
Driver = webdriver.Firefox

def img_path(img1_path, img2_path, func, swap=False):
    ''' 
    This is the function that aims to call specifyed function by path.

    Parameters
    ----------
    @sample_path  <cv2.image>  Path to image
    @html_path    <str>        Path to html code of image to comparison
    @func         <function>   Function, which takes two images
    @swap         <bool>       Swap images 
    ----------
    Return          <float>      Percentage of matching from [0, 1]
    '''
    assert is_existed_path(img1_path)
    assert is_existed_path(img2_path)
    assert inspect.isfunction(func)
    
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if swap:
        return func(img2, img1)
    return func(img1, img2)

def img_path_and_html(image_path, html_path, func, swap=False):
    ''' 
    This is the function that aims to call specifyed function 
    by path of the first one and html of the second one.

    Parameters
    ----------
    @sample_path  <cv2.image>  Path to image
    @html_path    <str>        Path to html code of image to comparison
    @func         <function>   Function, which takes two images
    @swap         <bool>       Swap images 
    ----------
    Return          <float>      Percentage of matching from [0, 1]
    '''
    assert is_existed_path(image_path)
    assert inspect.isfunction(func)
    
    image = cv2.imread(image_path)
    scrn  = make_screenshot(html_path)
    
    if swap:
        return func(scrn, image)
    return func(image, scrn)


def img_html(html1_path, html2_path):
    '''
    This is the function that aims to call specifyed function 
    by path of the first one and html of the second one.

    Parameters
    ----------
    @sample_path  <cv2.image>  Path to image
    @html_path    <str>        Path to html code of image to comparison
    @func         <function>   Function, which takes two images
    @swap         <bool>       Swap images 
    ----------
    Return          <float>      Percentage of matching from [0, 1]
    '''
    assert inspect.isfunction(func)
    
    driver = Driver()
    try:
        scrn1  = make_screenshot(html1_path, driver=driver)
        scrn2  = make_screenshot(html2_path, driver=driver)
    finally:
        driver.close()
    
    if swap:
        return func(scrn2, scrn1)
    return func(scrn1, scrn2)
