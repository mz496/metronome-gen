import numpy as np
import scipy
from scipy.io.wavfile import write

"""The sound to play on downbeats."""
DOWNBEAT_FILE = "./downbeat.wav"
"""The sound to play on everything that isn't a downbeat."""
OFFBEAT_FILE = "./offbeat.wav"
"""Length of output file, in seconds."""
OUTPUT_LENGTH_SECONDS = 3
"""BPM of the output file."""
OUTPUT_BEATS_PER_MINUTE = 150
"""Beats per measure (if this is n, a downbeat plays every n beats starting from the first)"""
OUTPUT_BEATS_PER_MEASURE = 4
"""Sample rate of the output file, in Hz."""
OUTPUT_RATE = 44100
"""Wait this many seconds before starting to play metronome sounds."""
OUTPUT_START_OFFSET_SECONDS = 0
"""File name of the output file."""
OUTPUT_FILENAME = "output.wav"

def copy_audio_into(src_arr, dest_arr, dest_start_index):
    if dest_start_index < 0 or dest_start_index >= len(dest_arr):
        raise Exception("Starting index {0} invalid for destination array of length {1}".format(starting_index, len(dest_arr)))

    dest_end_index = dest_start_index + len(src_arr)
    src_start_index = 0
    src_end_index = min(len(dest_arr) - dest_start_index, len(src_arr))
    dest_arr[dest_start_index:dest_end_index] = src_arr[src_start_index:src_end_index]

def main():
    (downbeat_audio_rate, downbeat_audio) = scipy.io.wavfile.read(DOWNBEAT_FILE)
    (offbeat_audio_rate, offbeat_audio) = scipy.io.wavfile.read(OFFBEAT_FILE)
    # TODO: handle different rates for these files
    # TODO: handle different number of channels for these files
    print(downbeat_audio_rate,downbeat_audio.shape)
    print(offbeat_audio_rate,offbeat_audio.shape)

    output_arr_length = OUTPUT_LENGTH_SECONDS * OUTPUT_RATE
    output_audio = None
    if downbeat_audio.shape[1] == 1 and offbeat_audio.shape[1] == 1:
        output_audio = np.zeros(output_arr_length)
    else:
        output_audio = np.zeros((output_arr_length, 2))

    # Samples per beat = (samples per minute) / (beats per minute)
    samples_per_beat = int((OUTPUT_RATE * 60) / OUTPUT_BEATS_PER_MINUTE)
    start_index = OUTPUT_START_OFFSET_SECONDS * OUTPUT_RATE
    beat_number = 1
    while start_index < output_arr_length:
        if (beat_number % OUTPUT_BEATS_PER_MEASURE) == 1:
            copy_audio_into(downbeat_audio, output_audio, start_index)
        else:
            copy_audio_into(offbeat_audio, output_audio, start_index)

        beat_number += 1
        start_index += samples_per_beat

    scipy.io.wavfile.write(OUTPUT_FILENAME, OUTPUT_RATE, output_audio)

if __name__=="__main__":
    main()