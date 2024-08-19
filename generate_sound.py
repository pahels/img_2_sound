from process_img import analyze_pixels
from pydub import AudioSegment, effects
from pydub.generators import Triangle
from pydub.playback import play
import threading

def rgb_to_frequency(r, g, b, base_freq=50, max_freq=800):
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    frequency = base_freq + (r + g + b) / 3 * (max_freq - base_freq)
    return frequency

'''def add_reverb(audio_segment, delay=100, decay=0.5):
    reverb = audio_segment
    for i in range(1, 5):
        echo = audio_segment - i * 6
        silence = AudioSegment.silent(duration=delay * i)
        reverb = reverb.overlay(echo, position=len(silence))
    return reverb'''

def gen_sound(pixel_data):
    track = AudioSegment.silent(duration=0)
    for r, g, b in pixel_data:
        frequency = rgb_to_frequency(r, g, b)
        duration = 100
        tone = Triangle(frequency).to_audio_segment(duration=duration)
        harmonic = Triangle(frequency * 1.5).to_audio_segment(duration=duration).apply_gain(-8)
        tone = tone.overlay(harmonic)
        #tone = add_reverb(tone)
        tone = tone.low_pass_filter(600)
        track += tone
    return track

def generate_and_play_sound(image_path):
    pixel_data = analyze_pixels(image_path)
    sound = gen_sound(pixel_data)
    sound = effects.normalize(sound)
    
    # Play sound in a separate thread
    threading.Thread(target=play, args=(sound,)).start()
    
    return pixel_data, len(sound)  # Return pixel data and sound duration

if __name__ == "__main__":
    image_path = 'harmony.jpg'
    generate_and_play_sound(image_path)
