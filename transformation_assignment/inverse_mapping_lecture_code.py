# Set the stage
import cv2
import numpy as np
import math
import os

# Read and view an image
A1 = cv2.imread("watch.pgm", cv2.IMREAD_GRAYSCALE)

# Get height and width of source image
M1 = A1.shape[0]
N1 = A1.shape[1]

# Set height and width of target image
M2 = M1
N2 = N1
A2 = np.zeros((M2,N2))

# Set default intensity to white
A2[:,:] = 255

# Translate image centre of A1 to origin
T1 = np.array(
[[1,0,-M1/2],
 [0,1,-N1/2],
 [0,0,1]])

# Rotate about origin by 25 degrees 
theta = 25/180*math.pi
c = math.cos(theta)
s = math.sin(theta)
R = np.array(
[[c,-s, 0],
 [s, c, 0],
 [0, 0, 1]])

# Translate origin to image centre of A2
T2 = np.array(
[[1,0,M2/2],
 [0,1,N2/2],
 [0,0,1]])

# Transformation that rotates A1 by theta about its centre
# and maps to the centre of A2
A = np.matmul(T2,np.matmul(R,T1))

# Invert A
A = np.linalg.inv(A)

# Transformation with inverse mapping and bilinear interpolation
for i in range(0,M2):
  for j in range(0,N2):
    # coordinates of the (i,j)-th pixel in A2
    x = i + 0.5
    y = j + 0.5
    # convert to homegeneous coordinates
    p = np.array([x,y,1])
    # transform with matrix A
    q = np.matmul(A,p)
    # coordinates in A1
    x = q[0]
    y = q[1]
    # bilinear interpolation
    k = round(x) - 1
    l = round(y) - 1
    u = x - k - 0.5
    v = y - l - 0.5
    if ((k >= 0) and (k < M1-1) and (l >= 0) and (l < N1-1)):
      A2[i,j] = round( (1-v) * ( (1-u)*A1[k,l] + u*A1[k+1,l] ) + v * ( (1-u)*A1[k,l+1] + u*A1[k+1,l+1] ) )

#Display and save the final rotated image.
cv2.imshow("Rotated Image", A2)

#Check if the folder exist and save there the image
output_folder = "transformation/generated_images"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "rotated_image_inverse_mapping.pgm")
cv2.imwrite(output_path, A2)

cv2.waitKey(0)
cv2.destroyAllWindows()