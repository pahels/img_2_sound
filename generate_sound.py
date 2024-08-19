from process_img import analyze_pixels
from pydub import AudioSegment
from pydub.generators import Sine

def rgb_to_frequency(r, g, b):
    # RBG bvalues (0-255) to frequency range (20Hz to 2000 Hz)
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    frequency = 20 + (r + g + b) / 3 * (2000 - 20)
    return frequency

def gen_sound(pixel_data):
    track = AudioSegment.silent(duration = 0) #begin with silence
    for r, g, b in pixel_data:
        frequency = rgb_to_frequency(r, g, b)
        duration = 100  # Duration of each tone in milliseconds
        tone = Sine(frequency).to_audio_segment(duration=duration)
        track += tone

    return track

image_path = 'harmony.jpg'  # Replace with your image file
pixel_data = analyze_pixels(image_path)
print("starting")
sound = gen_sound(pixel_data)
sound.export("output.wav", format = 'wav')
print("done")
