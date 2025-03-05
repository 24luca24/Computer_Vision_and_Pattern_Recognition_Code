import math
import numpy as np

#takes from the UI the image of the user and gamma from the slider
    #if gamma > 1 the image darkens
    #if gamma < 1 the image brightens
    #if gamma = 1.0, th e image remain unchanged
def gamma_correction(img, gamma):
    if img is None:
        print("provide an image")
        return None

    #normalize the image (0 to 1)
    img_normalized = img / 255.0

    #gamma transformation
    img_gamma_corrected = np.power(img_normalized, gamma)

    #rescale img to 0 - 255 range
    corrected_img = (img_gamma_corrected * 255).astype(np.uint8)
    return corrected_img

#increase contrast, while keeping intensity changes bijective (invertible)
def bijective_contrast_stretching(img, delta):
    if img is None:
        print("provide an image")
        return None
    
    img_normalized = img / 255.0
    img1 = 2*img_normalized - 1
    img2 = 1.2 * np.arctan(delta*img1) / np.arctan(delta)
    img3 = (img2 + 1)/2
    final_img = np.round(255*img3-0.5) 
    return final_img


