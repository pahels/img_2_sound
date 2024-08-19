import random
from process_img import analyze_pixels
from pydub import AudioSegment, effects
from pydub.generators import Triangle, Square, Sine
from pydub.playback import play
import threading

def rgb_to_frequency(r, g, b, base_freq=50, max_freq=800):
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    frequency = base_freq + (r + g + b) / 3 * (max_freq - base_freq)
    return frequency

def gen_sound(pixel_data):
    track = AudioSegment.silent(duration=0)
    
    previous_tone = None

    for r, g, b in pixel_data:
        # Lower the base frequency for a deeper, more calming tone
        frequency = rgb_to_frequency(r, g, b, base_freq=40, max_freq=120)
        duration = 300  # Increase duration for a slower, meditative pace
        
        # Sine wave for a soothing bass tone
        bass_tone = Sine(frequency).to_audio_segment(duration=duration)
        
        # Add a harmonic tone using Triangle wave, only if frequency is above a threshold
        if frequency > 80:
            harmonic = Triangle(frequency * 1.5).to_audio_segment(duration=duration).apply_gain(-10)
            tone = bass_tone.overlay(harmonic)
        else:
            tone = bass_tone
        
        # Apply a higher low-pass filter to allow more mid-tones, reducing scratchiness
        tone = tone.low_pass_filter(300)
        
        # Apply a gentle high-pass filter to remove very low-end rumble
        tone = tone.high_pass_filter(40)
        
        # Smooth out transitions with a longer crossfade
        if previous_tone:
            track = track.append(tone, crossfade=150)
        else:
            track += tone
        
        previous_tone = tone

    # Normalize and apply a slight gain for a richer sound
    track = effects.normalize(track)
    track = track.low_pass_filter(300).apply_gain(+1)
    
    # Apply a soft reverb for an ethereal, meditative feel
    track = track.fade_out(duration=500)  # Smooth fade-out at the end
    
    return track

def generate_and_play_sound(image_path):
    pixel_data = analyze_pixels(image_path)
    sound = gen_sound(pixel_data)
    sound = effects.normalize(sound)

    threading.Thread(target=play, args=(sound,)).start()
    
    return pixel_data, len(sound) 

if __name__ == "__main__":
    image_path = 'alien.png'  
    generate_and_play_sound(image_path)
