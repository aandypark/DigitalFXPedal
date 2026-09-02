import numpy as np
from scipy.io import wavfile

sample_rate, audio = wavfile.read("../Audio/guitarSample.wav")

if len(audio.shape) > 1:
    audio = audio[:, 0]

# Convert to float
audio = audio.astype(np.float32)

# Normalize to [-1, 1]
audio /= np.max(np.abs(audio))

# Convert to signed 16-bit integers
audio_int16 = (audio * 32767).astype(np.int16)

# Create C header
with open("../audio/guitar_data.h", "w") as f:

    f.write("#ifndef GUITAR_DATA_H\n")
    f.write("#define GUITAR_DATA_H\n\n")

    f.write(f"#define GUITAR_SAMPLE_RATE {sample_rate}\n")
    f.write(f"#define GUITAR_NUM_SAMPLES {len(audio_int16)}\n\n")

    f.write("const int16_t guitar_data[GUITAR_NUM_SAMPLES] = {\n")

    for i, sample in enumerate(audio_int16):
        if i % 12 == 0:
            f.write("    ")

        f.write(str(sample))

        if i != len(audio_int16) - 1:
            f.write(", ")

        if i % 12 == 11:
            f.write("\n")

    f.write("\n};\n\n")
    f.write("#endif\n")

print("Created guitar_data.h")
print("Sample rate:", sample_rate)
print("Samples:", len(audio_int16))