#importing required libraries
import skimage
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from skimage import exposure
import matplotlib.pyplot as plt

# reading the image
img = imread('a1.jpg')
plt.axis("off")
plt.imshow(img)
print(img.shape)

# resizing image
height = int(img.shape[0]/2)
resized_img = resize(img, (int(img.shape[0]/2), int(img.shape[1]/2)))
plt.axis("off")
plt.imshow(resized_img)
print(resized_img.shape)

#creating hog features
fd, hog_image = hog(resized_img, orientations=9, pixels_per_cell=(8, 8),
                	cells_per_block=(2, 2), visualize=True, multichannel=True)
plt.axis("off")
plt.imshow(hog_image, cmap="gray")

# save the images
plt.imsave("ip.jpg", hog_image, cmap="gray")