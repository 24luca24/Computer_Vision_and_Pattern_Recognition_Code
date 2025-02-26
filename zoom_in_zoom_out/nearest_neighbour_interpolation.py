import cv2
import numpy as np
import math

#Read and view an image
A1 = cv2.imread("watch.pgm", cv2.IMREAD_GRAYSCALE)

#Check if the image is loaded correctly
if A1 is None:
    print("Error: Image not found or cannot be read.")
    exit()

cv2.imshow("Orginal Image", A1)

#Get height and width of source image
M1, N1 = A1.shape

#Set height and width of target image
c = 0.5 #Scale factor (reduce dimension of the image by half) 
M2 = round(c * M1)
N2 = round(c * N1)
A2 = np.zeros((M2, N2))

#Nearest neighbour interpolation
for i in range(0, M2):
    for j in range(0 + N2):
        x = (i + 0.5) * M1/M2  #(c = M1/M2)
        y = (j + 0.5) * N1/N2 #Calculates the y-coordinate in the original image based on the column index j of the new grid.
        k = math.floor(x) #Convert floating to integer -> gives the index of the closest pixel in the original image
        l = math.floor(y)
        A2[i, j] = A1[k, l]

cv2.imshow("Shrinked Image", A2)
cv2.imwrite("shrinked_image_neighboor_interpolation.pgm", A2)

#Keep the window open until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()