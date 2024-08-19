''' 
this program processes each pixel, which is the first step to generating sound 
'''

import cv2

def resize_image(image_path, scale_percent=50):
    image = cv2.imread(image_path)
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def analyze_pixels(img, block_size = 20):
    image = resize_image(img)
    height, width, _ = image.shape
    pixel_data = []
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = image[y:y+block_size, x:x+block_size]
            r = block[:, :, 0].mean()
            g = block[:, :, 1].mean()
            b = block[:, :, 2].mean()
            pixel_data.append((int(r), int(g), int(b)))
    return pixel_data

'''
#example usage
image_path = 'alien.png'  # Replace with your image file
pixel_data = analyze_pixels(image_path)
print(pixel_data[:10])
'''
