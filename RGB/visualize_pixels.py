import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from generate_sound import generate_and_play_sound
from process_img import analyze_pixels, resize_image, GROUP_SIZE

def visualize_pixels(image_path, block_size=GROUP_SIZE):
    # Generate sound and get pixel data
    pixel_data, sound_duration = generate_and_play_sound(image_path)
    
    # Load and resize the image
    image = resize_image(image_path)
    
    fig, ax = plt.subplots()
    im = ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    height, width, _ = image.shape
    
    # Rectangle
    rect = plt.Rectangle((0, 0), block_size, block_size, fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)

    def init():
        rect.set_visible(False)
        return rect,

    def update(frame):
        y = (frame * block_size) // width * block_size
        x = (frame * block_size) % width
        
        if x < width and y < height:
            rect.set_xy((x, y))
            rect.set_visible(True)
        
        return rect,

    total_frames = len(pixel_data)
    interval = sound_duration / total_frames if total_frames > 0 else 50

    ani = FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True, interval=interval)
    plt.show()

if __name__ == "__main__":
    image_path = 'alien.png'  
    visualize_pixels(image_path)
