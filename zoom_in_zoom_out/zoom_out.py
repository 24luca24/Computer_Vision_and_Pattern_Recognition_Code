import cv2
import numpy as np

A1 = cv2.imread("watch.pgm", cv2.IMREAD_GRAYSCALE)

#Check if the image is loaded correctly
if A1 is None:
    print("Error: Image not found or cannot be read.")
    exit()

cv2.imshow("Orginal Image", A1)

#Get height and width of source image
M1, N1 = A1.shape

#Set height and width of target image
z = 2
M2 = round(M1/z)
N2 = round(N1/z)
A2 = np.zeros((M2, N2))

#Zoom out
for i in range(0, M2):
    for j in range(0, N2):
        for k in range (0, z):
            for l in range(0, z):
                A2[i, j] += A1[z * i +k, z * j + l]
A2 /= pow(z, 2)

cv2.imshow("Shrinked Image", A2)
cv2.imwrite("shrinked_image.pgm", A2)

#Keep the window open until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()