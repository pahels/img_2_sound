import cv2
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import butter, filtfilt

def generate_noise(noise_type, length, sample_rate):
    if noise_type == 'pink':
        # Generate deep blue noise with rhythm
        return generate_deep_blue_noise_with_rhythm(length, sample_rate)
    elif noise_type == 'blue':
        noise = np.random.normal(0, 1, int(length * sample_rate))
        pink_noise = np.cumsum(noise)
        return pink_noise / np.max(np.abs(pink_noise))
    elif noise_type == 'brown':
        noise = np.random.normal(0, 1, int(length * sample_rate))
        brown_noise = np.cumsum(noise)
        return brown_noise / np.max(np.abs(brown_noise))

# New function for generating deep blue noise with rhythm
def generate_deep_blue_noise_with_rhythm(length, sample_rate, rhythm_freq=2):
    # Generate blue noise
    noise = np.random.normal(0, 1, int(length * sample_rate))
    blue_noise = np.diff(noise)
    blue_noise = np.concatenate(([blue_noise[0]], blue_noise))

    # Apply a low-pass filter to create a deeper sound
    b, a = butter(1, 0.1, btype='low', analog=False)
    deep_blue_noise = filtfilt(b, a, blue_noise)
    
    # Create a rhythmic pattern by modulating the amplitude
    t = np.linspace(0, length, len(deep_blue_noise), False)
    rhythm = 0.5 * (1 + np.sin(2 * np.pi * rhythm_freq * t))
    deep_blue_noise_with_rhythm = deep_blue_noise * rhythm
    
    return deep_blue_noise_with_rhythm / np.max(np.abs(deep_blue_noise_with_rhythm))

# Function to map HSV values to sound properties
def map_hsv_to_sound(h, s, v, sample_rate):
    # Map hue to noise type
    if h < 60:
        noise_type = 'blue'
    elif h < 120:
        noise_type = 'pink'
    elif h < 180:
        noise_type = 'brown'
    else:
        noise_type = 'blue'  # Default noise if needed

    # Map saturation to frequency (we'll use it as a simple modulator)
    frequency = s / 255.0 * 1000 + 200  # Frequency between 200 Hz and 1200 Hz

    # Map value to amplitude
    amplitude = v / 255.0

    # Generate noise
    length = 0.1  # Length of sound for each pixel (0.1 seconds)
    noise = generate_noise(noise_type, length, sample_rate)

    # Ensure t and noise are the same length
    t = np.linspace(0, length, len(noise), False)
    sound = amplitude * np.sin(2 * np.pi * frequency * t) * noise

    return sound

# Main function to process the image and generate the sound
def image_to_sound(image_path, output_wav_path):
    # Load image and convert to HSV
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Initialize sound array
    sample_rate = 44100  # CD quality sample rate
    sound_array = np.array([])

    # Process each pixel or block of pixels
    height, width, _ = hsv_image.shape
    block_size = 20  # Process in blocks of 20x20 pixels

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = hsv_image[y:y + block_size, x:x + block_size]
            h = np.mean(block[:, :, 0])
            s = np.mean(block[:, :, 1])
            v = np.mean(block[:, :, 2])

            # Generate sound for the block
            block_sound = map_hsv_to_sound(h, s, v, sample_rate)
            sound_array = np.concatenate((sound_array, block_sound))

    # Normalize the sound array
    sound_array = np.int16(sound_array / np.max(np.abs(sound_array)) * 32767)

    # Save to WAV file
    write(output_wav_path, sample_rate, sound_array)

# Example usage
image_path = 'alien.png'
output_wav_path = 'output_sound.wav'
print("starting")
image_to_sound(image_path, output_wav_path)
print("done")