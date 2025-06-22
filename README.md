# Welcome to **sonistream**
#### A simple steganography tool used to embed data into audio files using amplitude modulation, useful in making CTFs and signal analysis.

---

### Demo Video -> [Youtube | sonistream](https://youtu.be/KtCTDkwWSJI)
Music selection: [Doing Damage by Dollshade](https://www.bensound.com/royalty-free-music/track/doing-damage-energic-rock)

## Sections
1. [Quick Start](#quick-start)
2. [How it Works](#how-it-works)
3. [How to Solve](#how-to-solve)
4. [Resource Links](#resource-links)

## Quick Start

#### 1. Ensure you have python and librosa
```bash
# For apt-based systems
sudo apt update
sudo apt install python3 python3-pip
```
```
pip install librosa
```

#### 2. Modify script parameters

```python
# in build.py

template_f = "music/doingdamage.wav"
pt = "Flag{G0_Tr0j4n5}"
start_second = 10
amp_factor = 1  # in dB (how easy to detect, higher is easier)

trial_f = "out/challenge.wav"
diff_f = "out/sanitycheck.wav"

#morse settings (in seconds)
dot_pulse = 0.05
dash_pulse = 3 * dot_pulse
gap = 2 * dot_pulse
space_pulse = 5 * dot_pulse
```

#### 3. Build challenge
```bash
python build.py
```

## How it Works

Audio wave have 2 primary metrics, amplitude (think loudness) and frequency (think pitch). Sonistream screws the amplitude of a wave to encode morse data. Imagine ripples in water, when two meet, they combine to make a resulting ripple/wave.

Imagine a wave of aplitude of 2 meets a wave of amplitude 3, the resulting wave has an amplitude of 5.
```
2 + 3 = 5
```

Now image that we create an inverted wave of -2 and play it along side our wave of amplitude 2... The waves will cancel out and we'll be left with **_silence_**.
```
2 + (-2) = 0
```

This is the basic principle behiend noise canceling headphones. Listen for incomming ambient sound, create an inverted wave (targeting the junk), and play it alongside our music.

## How to Solve

How to solve a sonistream challenge:
1. Download [Audacity](https://www.audacityteam.org/download/)
2. Import the challenge audio file into Audacity (given in ctf problem)
3. Locate the source audio file of the song and import it into Audacity (OSINT)
4. Invert either the challenge file or the source file (Effect -> Special -> Invert)
5. Play/Export the entire project, the audio waves will cancel out leaving you with morse code
6. Convert Data -> From Morse Code -> From Hex to get ASCII ([CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Morse_Code('Space','Line%20feed')From_Hex('Auto')&input=Li4uLi0gLS4uLi4gLS4uLi4gLS4tLiAtLi4uLiAuLS0tLSAtLi4uLiAtLS4uLiAtLS4uLiAtLi4uIC4uLi4tIC0tLi4uIC4uLi0tIC0tLS0tIC4uLi4uIC4uLS4gLi4uLi4gLi4uLi0gLS0uLi4gLi4tLS0gLi4uLS0gLS0tLS0gLS4uLi4gLi0gLi4uLS0gLi4uLi0gLS4uLi4gLiAuLi4tLSAuLi4uLiAtLS4uLiAtLi4&ieol=CRLF&oeol=CRLF
) example)

## Resource Links

[How To: Noise Cancelling Headphones](https://audiouniversityonline.com/noise-cancelling-headphones/)

[CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Morse_Code('Space','Line%20feed')From_Hex('Auto')&input=Li4uLi0gLS4uLi4gLS4uLi4gLS4tLiAtLi4uLiAuLS0tLSAtLi4uLiAtLS4uLiAtLS4uLiAtLi4uIC4uLi4tIC0tLi4uIC4uLi0tIC0tLS0tIC4uLi4uIC4uLS4gLi4uLi4gLi4uLi0gLS0uLi4gLi4tLS0gLi4uLS0gLS0tLS0gLS4uLi4gLi0gLi4uLS0gLi4uLi0gLS4uLi4gLiAuLi4tLSAuLi4uLiAtLS4uLiAtLi4&ieol=CRLF&oeol=CRLF)

[Librosa: Example Gallery](https://librosa.org/librosa_gallery/)

[How to use Audacity](https://manual.audacityteam.org/man/how_to_use_audacity.html)