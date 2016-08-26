import PIL.Image
import numpy as np
from skimage.feature import local_binary_pattern

from ml.descriptors import img_descriptor

@img_descriptor('LBP')
def lbp(img:        PIL.Image, 
        dimensions: int        = 8, 
        radius:     int        = 8, 
        bins:       int        = 40) -> (np.array, np.array):
    '''
      LBP (Local binary pattern descriptor)     
    '''

    gray = img.convert('L')
    np_img = np.asarray(gray)

    lbp = local_binary_pattern(gray, dimensions, radius, method="uniform")
    
    # if __DEBUG__:
    #     lbp_bytes = lbp.astype(np.float)/lbp.max()
    #     lbp_bytes = (lbp_bytes * 255).astype(np.uint8)
    #     cv2.imshow("LBP Features", lbp_bytes)
    
    hist, bins = np.histogram(lbp.ravel(), bins)
    hist = hist/hist.max()
    
    return hist, bins