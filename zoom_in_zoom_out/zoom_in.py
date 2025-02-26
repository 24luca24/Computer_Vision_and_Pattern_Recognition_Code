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
z = 2
M2 = z * M1
N2 = z * N1
A2 = np.zeros((M2, N2)) #Create an empty black image of the double of the size of the orginal picture

#Zoom-in
for i in range(0, M1):
    for j in range(0, N1):
        for k in range(0, z): #Repeat each row z times
            for l in range(0, z): #Repeat each row l times
                A2[z * i + k, z * j + l] = A1[i, j]

#Force window to match actual image size
cv2.imshow("Zoomed Image", A2) #Since this doesn't work as aspected on VSCode, the following stastement save the image with the new dimension
cv2.imwrite("zoomed_image.pgm", A2)

#Keep the window open until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()