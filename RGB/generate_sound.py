import random
from process_img import analyze_pixels
from pydub import AudioSegment, effects
from pydub.generators import Triangle, Square, Sine, Sawtooth
from pydub.playback import play
import threading
import os


def rgb_to_frequency(r, g, b, base_freq=0, max_freq=800):
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    frequency = base_freq + (r + g + b) / 3 * (max_freq - base_freq)
    return frequency

def gen_sound(pixel_data):
    track = AudioSegment.silent(duration=0)
    
    previous_tone = None

    for r, g, b in pixel_data:
        # Focus on deep sub-bass tones with a narrow frequency range
        frequency = rgb_to_frequency(r, g, b, base_freq=60, max_freq=200)
        duration = 600  # Long duration to blend tones together
        
        # Generate the primary bass tone using a sine wave
        bass_tone = Sine(frequency).to_audio_segment(duration=duration)
        
        # Apply a low-pass filter to remove any high-frequency components, focusing purely on sub-bass
        tone = bass_tone.low_pass_filter(200)
        
        # Smooth out transitions with a very long crossfade
        if previous_tone:
            track = track.append(tone, crossfade=300)  # Very long crossfade for seamless blending
        else:
            track += tone
        
        previous_tone = tone

    # Normalize the track to ensure consistent volume and apply a gain boost for a deep, rich sub-bass sound
    track = effects.normalize(track)
    track = track.low_pass_filter(80).apply_gain(+5)
    
    track.export("output_no_reverb.wav", format="wav")
    
    # Apply strong reverb using ffmpeg
    os.system('ffmpeg -i output_no_reverb.wav -af "aecho=0.8:0.8:100:0.2, aecho=0.8:0.8:200:0.15" output_with_reverb.wav')

    # Load the processed file back
    final_track = AudioSegment.from_file("output_with_reverb.wav")
    
    return final_track


def generate_and_play_sound(image_path):
    pixel_data = analyze_pixels(image_path)
    sound = gen_sound(pixel_data)
    sound = effects.normalize(sound)

    threading.Thread(target=play, args=(sound,)).start()
    
    return pixel_data, len(sound) 

if __name__ == "__main__":
    image_path = 'harmony.jpg'  
    generate_and_play_sound(image_path)
