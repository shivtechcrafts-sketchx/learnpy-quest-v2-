import os
import wave
import math
import struct
import random

# =========================
# CONFIG
# =========================
SAMPLE_RATE = 44100
SOUNDS_DIR = os.path.join("assets", "sounds")
os.makedirs(SOUNDS_DIR, exist_ok=True)

# =========================
# AUDIO HELPERS
# =========================
def clamp(value, min_value=-1.0, max_value=1.0):
    return max(min(value, max_value), min_value)

def save_wav(filename, samples):
    filepath = os.path.join(SOUNDS_DIR, filename)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)       # mono
        wf.setsampwidth(2)       # 16-bit
        wf.setframerate(SAMPLE_RATE)

        frames = bytearray()
        for sample in samples:
            sample = clamp(sample)
            int_sample = int(sample * 32767.0)
            frames.extend(struct.pack('<h', int_sample))

        wf.writeframes(frames)
    print(f"Generated: {filepath}")

def sine_wave(freq, duration, volume=0.5):
    total_samples = int(SAMPLE_RATE * duration)
    return [
        volume * math.sin(2 * math.pi * freq * t / SAMPLE_RATE)
        for t in range(total_samples)
    ]

def square_wave(freq, duration, volume=0.4):
    total_samples = int(SAMPLE_RATE * duration)
    return [
        volume * (1.0 if math.sin(2 * math.pi * freq * t / SAMPLE_RATE) >= 0 else -1.0)
        for t in range(total_samples)
    ]

def noise_wave(duration, volume=0.2):
    total_samples = int(SAMPLE_RATE * duration)
    return [
        volume * random.uniform(-1.0, 1.0)
        for _ in range(total_samples)
    ]

def apply_fade(samples, fade_in=0.01, fade_out=0.03):
    total = len(samples)
    fade_in_samples = int(SAMPLE_RATE * fade_in)
    fade_out_samples = int(SAMPLE_RATE * fade_out)

    for i in range(min(fade_in_samples, total)):
        samples[i] *= (i / fade_in_samples)

    for i in range(min(fade_out_samples, total)):
        idx = total - i - 1
        samples[idx] *= (i / fade_out_samples)

    return samples

def mix_tracks(*tracks):
    max_len = max(len(track) for track in tracks)
    mixed = [0.0] * max_len

    for track in tracks:
        for i in range(len(track)):
            mixed[i] += track[i]

    # normalize
    max_amp = max(abs(x) for x in mixed) if mixed else 1.0
    if max_amp > 1.0:
        mixed = [x / max_amp for x in mixed]

    return mixed

def concat_tracks(*tracks):
    output = []
    for track in tracks:
        output.extend(track)
    return output

def silence(duration):
    return [0.0] * int(SAMPLE_RATE * duration)

# =========================
# SOUND GENERATORS
# =========================
def generate_correct():
    # Happy rising tones
    a = sine_wave(660, 0.12, 0.4)
    b = sine_wave(880, 0.12, 0.4)
    c = sine_wave(1040, 0.18, 0.35)
    sound = concat_tracks(a, b, c)
    sound = apply_fade(sound, 0.005, 0.04)
    save_wav("correct.wav", sound)

def generate_wrong():
    # Descending buzzy tones
    a = square_wave(400, 0.12, 0.25)
    b = square_wave(280, 0.15, 0.25)
    c = square_wave(180, 0.18, 0.2)
    sound = concat_tracks(a, b, c)
    sound = apply_fade(sound, 0.005, 0.05)
    save_wav("wrong.wav", sound)

def generate_key_pickup():
    # Quick bright pickup sparkle
    a = sine_wave(1200, 0.06, 0.3)
    b = sine_wave(1600, 0.06, 0.25)
    c = sine_wave(2000, 0.08, 0.2)
    sound = concat_tracks(a, b, c)
    sound = apply_fade(sound, 0.003, 0.03)
    save_wav("key_pickup.wav", sound)

def generate_door_open():
    # Mechanical-ish unlock + low whoosh
    click1 = square_wave(500, 0.05, 0.18)
    click2 = square_wave(700, 0.04, 0.15)
    low_tone = sine_wave(180, 0.25, 0.18)
    hiss = noise_wave(0.20, 0.04)

    part1 = concat_tracks(click1, silence(0.02), click2)
    part2 = mix_tracks(low_tone, hiss)

    sound = concat_tracks(part1, silence(0.02), part2)
    sound = apply_fade(sound, 0.003, 0.05)
    save_wav("door_open.wav", sound)

def generate_bg_music():
    """
    Simple retro ambient loop:
    Repeating soft synth tones.
    Approx 8 seconds.
    """
    sequence = [
        220, 277, 330, 277,
        196, 247, 294, 247,
        220, 277, 330, 392,
        196, 247, 294, 330
    ]

    note_duration = 0.45
    gap = 0.02
    track = []

    for freq in sequence:
        base = sine_wave(freq, note_duration, 0.10)
        overtone = sine_wave(freq * 2, note_duration, 0.03)
        pulse = square_wave(freq / 2, note_duration, 0.02)
        note = mix_tracks(base, overtone, pulse)
        note = apply_fade(note, 0.01, 0.08)
        track.extend(note)
        track.extend(silence(gap))

    # Light ambient hum underneath
    hum = sine_wave(110, len(track) / SAMPLE_RATE, 0.02)
    music = mix_tracks(track, hum)
    music = apply_fade(music, 0.05, 0.2)
    save_wav("bg_music.wav", music)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("Generating LearnPy Quest sound assets...\n")
    generate_correct()
    generate_wrong()
    generate_key_pickup()
    generate_door_open()
    generate_bg_music()
    print("\nAll sound files generated successfully in assets/sounds/")