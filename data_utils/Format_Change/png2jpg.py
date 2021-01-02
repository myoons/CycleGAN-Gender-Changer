from PIL import Image
import os

input_path = '/data/cycleGAN/datasets/background_remove/train/B'
output_path = '/data/cycleGAN/B/'

# Rename the Images
image_number = 1

for file in os.listdir(input_path):

    # Open Image
    im = Image.open(input_path + '/' + str(file))

    # converting to jpg 
    rgb_im = im.convert("RGB") 

    # exporting the image 
    rgb_im.save(output_path + "{}.jpg".format(str(image_number))) 

    image_number += 1