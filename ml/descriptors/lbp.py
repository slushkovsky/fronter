import PIL.Image
import numpy as np
from skimage.feature import local_binary_pattern
import cv2

from ml.descriptors import img_descriptor

@img_descriptor('LBP')
def lbp(img:        np.ndarray, 
        dimensions: int        = 24, 
        radius:     int        = 8,
        eps:        int        =1e-7) -> np.array:
    '''
      LBP (Local binary pattern descriptor)     
    '''

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lbp = local_binary_pattern(gray, dimensions, radius, method="uniform")

    (hist, _) = np.histogram(lbp.ravel(),
            bins=np.arange(0, dimensions + 3),
            range=(0, dimensions + 2))

    hist = hist.astype("float")
    hist /= (hist.sum() + eps)

    return hist