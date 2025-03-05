import cv2
import numpy as np
import math
import os

# -----------------------------------
# Provided Transformation Matrices
# -----------------------------------
def scaling_matrix(c):
    return np.array([[c, 0, 0],
                     [0, c, 0],
                     [0, 0, 1]])

def translation_matrix(tx, ty):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]])

def rotation_matrix(theta):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    return np.array([[cos_theta, -sin_theta, 0],
                     [sin_theta, cos_theta, 0],
                     [0, 0, 1]])

def vertical_shear_matrix(s):
    #Produces: x' = x + s*y, y' = y.
    return np.array([[1, s, 0],
                     [0, 1, 0],
                     [0, 0, 1]])

def horizontal_shear_matrix(s):
    #Produces: x' = x, y' = y + s*x.
    return np.array([[1, 0, 0],
                     [s, 1, 0],
                     [0, 0, 1]])

# -----------------------------------
# Generic Affine Transform with Bilinear Interpolation
# -----------------------------------
def apply_affine_transform(img, T, default=255):
    """
    Applies an affine transformation (given by 3x3 matrix T) to a grayscale image.
    Uses inverse mapping and bilinear interpolation.
    """
    rows, cols = img.shape
    T_inv = np.linalg.inv(T) #Compute inverse tranformation matrix
    output = np.full((rows, cols), default, dtype=img.dtype)
    
    for y in range(rows):
        for x in range(cols):
            pt = np.array([x, y, 1]) #Convert pixel into homogeneous coordinates
            src_pt = T_inv @ pt #Apply inverse transformation
            src_x, src_y = src_pt[0], src_pt[1] #Extract transformed coordinates
            
            #If the source coordinate is out-of-bounds, leave default.
            if src_x < 0 or src_x >= cols - 1 or src_y < 0 or src_y >= rows - 1:
                continue
            
            #Compute values of x, y to get points for bilinear interpolation
            x0 = int(math.floor(src_x))
            y0 = int(math.floor(src_y))
            x1 = x0 + 1
            y1 = y0 + 1

            #Weigths
            dx = src_x - x0
            dy = src_y - y0
            
            #Bilinear interpolation
            val = (img[y0, x0]*(1-dx)*(1-dy) +
                   img[y0, x1]*dx*(1-dy) +
                   img[y1, x0]*(1-dx)*dy +
                   img[y1, x1]*dx*dy)
            output[y, x] = int(round(val))
    return output

# -----------------------------------
# Main Program
# -----------------------------------

#Load the grayscale image.
A1 = cv2.imread("watch.pgm", cv2.IMREAD_GRAYSCALE)
if A1 is None:
    print("Error: Image not found or cannot be read. (watch)")
    exit()

#Get dimensions of the source image.
M1, N1 = A1.shape

#Create a larger canvas (double the size) filled with white (255).
M2, N2 = 2 * M1, 2 * N1
A2 = np.full((M2, N2), 255, dtype=np.uint8)

#Embed A1 at the center of A2.
x_offset = (N2 - N1) // 2
y_offset = (M2 - M1) // 2
A2[y_offset:y_offset+M1, x_offset:x_offset+N1] = A1

#Define the rotation angle 
theta = 25/180*math.pi

#Compute shear factors.
#The decomposition: R(theta) = Sx(tan(theta/2)) -> Sy(-sin(theta)) -> Sx(tan(theta/2))
shx = math.tan(theta / 2)  #Factor for horizontal shears.
shy = -math.sin(theta)       #Factor for vertical shear.

#Determine the center of the canvas.
rows, cols = A2.shape
center_x = cols // 2
center_y = rows // 2

#Build the composite transformation matrix.
#1) Translate so the center moves to the origin.
T_to_origin = translation_matrix(-center_x, -center_y)
#2) Translate back.
T_back = translation_matrix(center_x, center_y)
#3) Shear matrices.
Sx = vertical_shear_matrix(shx)   # x' = x + shx*y
Sy = horizontal_shear_matrix(shy)   # y' = y + shy*x

#Composite: first Sx, then Sy, then Sx again.
Composite = T_back @ Sx @ Sy @ Sx @ T_to_origin

#Apply the composite transformation.
img_rotated_shears = apply_affine_transform(A2, Composite)

#Display and save the final rotated image.
cv2.imshow("Rotated Image (Composite)", img_rotated_shears)

#Check if the folder exist and save there the image
output_folder = "transformation/generated_images"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "shear_rotation_result.pgm")
cv2.imwrite(output_path, img_rotated_shears)

# -----------------------------------
# Compare with Inverse Mapping Method
# -----------------------------------
# A_inverse_mapping = cv2.imread("generated_images/rotated_image_inverse_mapping.pgm", cv2.IMREAD_GRAYSCALE)

# if A_inverse_mapping is None:
#     print("Error: Image not found or cannot be read. (transformed)")
#     exit()

# # Resize Shear Image to Match Size of Inverse Mapping Result
# img_rotated_shears_resized = cv2.resize(img_rotated_shears, (A_inverse_mapping.shape[1], A_inverse_mapping.shape[0]), interpolation=cv2.INTER_LINEAR)

# # Compute absolute difference
# difference = np.abs(img_rotated_shears_resized.astype(np.int32) - A_inverse_mapping.astype(np.int32))

# # Compute average intensity difference
# average_difference = np.mean(difference)

# print(f"Average Intensity Difference: {average_difference}")

#To close the window showing the image
cv2.waitKey(0)
cv2.destroyAllWindows()