import cv2
import numpy as np

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
c = 0.5
M2 = round(c * M1)
N2 = round(c * N1)
A2 = np.zeros((M2, N2))

#Bilinear Interpolation
for i in range(0, M2):
    for j in range(0, N2):
        x = (i + 0.5) * M1/M2
        y =(j + 0.5) * M1/M2
        k = round(x) - 1
        l = round(y) - 1
        k = min(max(k,  0), M1 - 2) #Make sure that k and k+1 and
        l = min(max(l, 0), N1 - 2)  #l and l+1 are in the valid range
        u = x - k - 0.5
        v = y - l - 0.5
        A2[i,j] = round( (1-v) * ( (1-u)*A1[k,l] + u*A1[k+1,l] ) + v * ( (1-u)*A1[k,l+1] + u*A1[k+1,l+1] ) )

cv2.imshow("Shrinked Image", A2)
cv2.imwrite("shrinked_image_bilinear_interpolation.pgm", A2)

#Keep the window open until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()