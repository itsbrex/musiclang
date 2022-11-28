
import itertools
import numpy as np

# Names of pitch classes to use (mostly ignoring spelling).
PITCH_CLASS_NAMES = [
    'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

PITCH_CLASS_DICT = {pitch: idx for idx, pitch in enumerate(PITCH_CLASS_NAMES)}


# Pitch classes in a key (rooted at zero).
KEY_PITCHES = [0, 2, 4, 5, 7, 9, 11]

# Pitch classes in each chord kind (rooted at zero).
CHORD_KIND_PITCHES = {
    '': [0, 4, 7],
    'm': [0, 3, 7],
    '+': [0, 4, 8],
    'dim': [0, 3, 6],
    'dim0': [0, 3, 6, 9],
    '7': [0, 4, 7, 10],
    'maj7': [0, 4, 7, 11],
    'm7': [0, 3, 7, 10],
    'm7b5': [0, 3, 6, 10],
}
ALL_CHORDS = [set(((np.asarray(CHORD_KIND_PITCHES[key]) + i) % 12).tolist()) for key in CHORD_KIND_PITCHES for i in range(12)]


CHORD_KINDS = CHORD_KIND_PITCHES.keys()
NO_CHORD = 'N.C.'
# All usable chords, including no-chord.
CHORDS = [NO_CHORD] + list(
    itertools.product(range(12), CHORD_KINDS))

# All key-chord pairs.
KEY_CHORDS = list(itertools.product(range(12), CHORDS))

# Maximum length of chord sequence to infer.
MAX_NUM_CHORDS = 1000

# MIDI programs that typically sound unpitched.
UNPITCHED_PROGRAMS = (
    list(range(96, 104)) + list(range(112, 120)) + list(range(120, 128)))

# Mapping from time signature to number of chords to infer per bar.
DEFAULT_TIME_SIGNATURE_CHORDS_PER_BAR = {
    (2, 2): 1,
    (2, 4): 1,
    (3, 4): 1,
    (4, 4): 2,
    (6, 8): 2,
}


MAJOR_PROFILE = [
6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88
]

MINOR_PROFILE = [
6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17
]


MELODIC_MINOR_PROFILE = [
6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,2.69,3.98,2.11,3.17
]


PROFILES = {
    'M': MAJOR_PROFILE,
    'm': MINOR_PROFILE,
    'mm': MELODIC_MINOR_PROFILE
}

PROFILES_RAW = {
    'm': [1, 0, 1, 1, -1, 1, 0, 1, 1, 0, 0, 1],
    'M': [1, 0, 1, -1, 1, 1, 0, 1, 0, 1, 0, 1],
    'mm':[1, 0, 1, 1, -1, 1, 0, 1, 0, 1, 0, 1]
}

PROFILE_M = np.asarray([1, 0.4, 0.1, 0.5, 0.8, 0.4, 0.1])
PROFILE_m = np.asarray([1, 0.3, 0.4, 0.5, 0.8, 0.4, 0.1])
PROFILE_mm = np.asarray([1, 0.3, 0.2, 0.5, 0.9, 0.2, 0.1])
PROFILE_M /= PROFILE_M.sum()
PROFILE_m /= PROFILE_m.sum()
PROFILE_mm /= PROFILE_mm.sum()

PROFILES_DEGREE = {
    'M': PROFILE_M,
    'm': PROFILE_m,
    'mm':  PROFILE_mm
}


TYPE = "type"
TIME = "time"
NOTE = "note"
VEL = "vel"
CHANNEL = "channel"
DURATION = "duration"
END_TIME = "end_time"
START_TIME = "start_time"
TRACK = "track"
VOICE = "voice"
ON = 1
OFF = 0


PATTERN_M = [(7, 'M'), (5, 'M'), (9, 'm'), (2, 'm'), (4, 'm'), (9, 'mm'), (2, 'mm'), (4, 'mm'), (0, 'm')]
PATTERN_M = [((pitch + 7 * i) % 12, mode) for i in range(12) for pitch, mode in PATTERN_M]
PATTERN_M1 = [f for f in PATTERN_M if f[1] != 'mm']
PATTERN_M2 = [f for f in PATTERN_M if f[1] == 'mm']
PATTERN_M = PATTERN_M1 + PATTERN_M2

PATTERN_M_dist = {key: (idx+1)/len(PATTERN_M) for idx, key in enumerate(PATTERN_M)}

PATTERN_m = [(0, 'aeolian'), (0, 'mm'), (7, 'm'), (5, 'm'), (10, 'M'), (8, 'M'), (7, 'mm'), (5, 'mm')]
PATTERN_m = [((pitch + 7 * i) % 12, mode) for i in range(12) for pitch, mode in PATTERN_m ]
PATTERN_m1 = [f for f in PATTERN_m if f[1] != 'mm']
PATTERN_m2 = [f for f in PATTERN_m if f[1] == 'mm']
PATTERN_m = PATTERN_m1 + PATTERN_m2

PATTERN_m_dist = {key: (idx+1)/len(PATTERN_m) for idx, key in enumerate(PATTERN_m)}

PATTERN_mm = PATTERN_m
PATTERN_mm_dist = {key: (idx+1)/len(PATTERN_mm) for idx, key in enumerate(PATTERN_mm)}


PATTERNS = {
    'm': PATTERN_m,
    'M': PATTERN_M,
    'mm': PATTERN_mm
}

PATTERNS_DICT = {
    'm': PATTERN_m_dist,
    'M': PATTERN_M_dist,
    'mm': PATTERN_mm_dist
}
