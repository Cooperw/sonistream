'''
a. Cooper Wiegand
https://github.com/cooperw/sonistream

A simple steganography tool used to embed data into audio files using amplitude modulation, useful in making CTFs and signal analysis.


How to solve a sonistream challenge:
1. Download [Audacity](https://www.audacityteam.org/download/)
2. Import the challenge audio file into Audacity (given in ctf problem)
3. Locate the source audio file of the song and import it into Audacity (OSINT)
4. Invert either the challenge file or the source file (Effect -> Special -> Invert)
5. Play/Export the entire project, the audio waves will cancel out leaving you with morse code
6. Convert Data -> From Morse Code -> From Hex to get ASCII ([CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Morse_Code('Space','Line%20feed')From_Hex('Auto')&input=Li4uLi0gLS4uLi4gLS4uLi4gLS4tLiAtLi4uLiAuLS0tLSAtLi4uLiAtLS4uLiAtLS4uLiAtLi4uIC4uLi4tIC0tLi4uIC4uLi0tIC0tLS0tIC4uLi4uIC4uLS4gLi4uLi4gLi4uLi0gLS0uLi4gLi4tLS0gLi4uLS0gLS0tLS0gLS4uLi4gLi0gLi4uLS0gLi4uLi0gLS4uLi4gLiAuLi4tLSAuLi4uLiAtLS4uLiAtLi4&ieol=CRLF&oeol=CRLF
) example)

'''

import librosa
import soundfile as sf
import os

template_f = "music/doingdamage.wav"
pt = "Flag{G0_Tr0j4n5}"
start_second = 10
amp_factor = 1  # in dB (how easy to detect, higher is easier)

trial_f = "out/challenge.wav"
diff_f = "out/sanitycheck.wav"
os.makedirs("out", exist_ok=True)

#morse settings (in seconds)
dot_pulse = 0.05
dash_pulse = 3 * dot_pulse
gap = 2 * dot_pulse
space_pulse = 5 * dot_pulse

def morse(msg):
    morse_code = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
        'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': ' ', ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
        '(': '-.--.', ')': '-.--.-'
    }
    morse = ''
    for char in msg:
        if char.upper() in morse_code:
            morse += morse_code[char.upper()] + ' '
        else:
            print(f"[Warning]: Character '{char}' not found in Morse code dictionary.")
    return morse

def adjust_volume(y, sr,start_second, amp_duration, amp_factor):
    start_frame = int(start_second * sr)
    end_frame = min(len(y), int((start_second + amp_duration) * sr))
    linear_amp_factor = 10**(amp_factor / 20)
    y[start_frame:end_frame] *= linear_amp_factor
    return y, sr

def overlay_audio_with_inversion(input_audio1, input_audio2, output_path):
    y1, sr1 = librosa.load(input_audio1, sr=None)
    y2, sr2 = librosa.load(input_audio2, sr=None)
    if len(y1) != len(y2):
        min_len = min(len(y1), len(y2))
        y1 = y1[:min_len]
        y2 = y2[:min_len]
    y1_inverted = -y1
    y_combined = y1_inverted + y2
    y_combined /= max(abs(y_combined))
    sf.write(output_path, y_combined, sr1)

def trim_audio(y, sr, start_sec, end_sec):
    trimmed_y = y[int(start_sec * sr):int(end_sec * sr)]
    return trimmed_y, sr

ct_hex = hex(int.from_bytes(pt.encode(), 'big'))[2:]
ct_morse = morse(ct_hex)

print(ct_hex)
print(ct_morse)

y, sr = librosa.load(template_f, sr=None)
cursor = start_second
for char in ct_morse:
    amp_duration = 0
    if char == '.':
        amp_duration = dot_pulse
        adjust_volume(y, sr, cursor, amp_duration, amp_factor)
    elif char == '-':
        amp_duration = dash_pulse
        adjust_volume(y, sr, cursor, amp_duration, amp_factor)
    else:
        amp_duration = space_pulse
        adjust_volume(y, sr, cursor, amp_duration, 0)
    cursor += amp_duration + gap
y_t, sr_t = trim_audio(y, sr, 0, int(cursor+2))
sf.write(trial_f, y_t, sr_t)

overlay_audio_with_inversion(template_f, trial_f, diff_f)

print(f"Origional Size: {int(os.path.getsize(template_f) / 1024.)} kb")
print(f"Payload Size: {int(os.path.getsize(trial_f) / 1024.)} kb")
