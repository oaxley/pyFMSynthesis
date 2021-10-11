#!/usr/bin/env python

#----- imports
from __future__ import annotations
from typing import Any, Dict

import numpy as np
import simpleaudio as sa


#----- globals
SAMPLING_FREQUENCY = 44100              # sampling at 44,100 Hz


#----- functions
def fmSynthesis(formula: str, values: Dict[str, Any], volume: float = 1.0, duration: int = 3) -> None:
    """Performs FM Synthesis

    Args:
        formula: the trigonometric formula to use for the FM Synthesis
        values : values needed to compute the FM synthesis
        volume : gain/volume once the FM synthesis is done
        duration: length in seconds for the note
    """
    # generate the time sampling values evenly spaced
    t: np.ndarray = np.linspace(0, duration, SAMPLING_FREQUENCY*duration, False)

    # build the local vars from the dictionary values
    for k in values:
        try:
            globals()[k] = eval(values[k])
        except TypeError:
            globals()[k] = values[k]

    
    # evaluate the formula
    y: np.ndarray = eval(formula)

    # ensure that highest value is in 16-bit range
    audio: np.ndarray = volume * (y * (2**15 - 1) / np.max(np.abs(y)))
    audio = audio.astype(np.int16)

    # start the playback
    play_obj = sa.play_buffer(audio, 1, 2, SAMPLING_FREQUENCY)
    play_obj.wait_done()


#----- begin

# simple 440Hz note 
fmSynthesis('A*np.sin(2*np.pi*fc*t)', {'A': 100, 'fc': 440})

# adding two sin waves
fmSynthesis('(A*np.sin(2*np.pi*fc*t + B*np.sin(2*np.pi*fm*t)))', 
            {
                'A': 1,
                'B': .96,
                'fc': 220,
                'fm': 220*8,
            },
            0.25)


# adding three sin waves
fmSynthesis('A*np.sin(2*np.pi*f1*t + B*np.sin(2*np.pi*f2*t + C*np.sin(2*np.pi*f3*t)))', 
            {
                'f1': 100,
                'f2': 200,
                'f3': 400,
                'A': 1,
                'B': '0.75*np.sin(2*np.pi*440*t)',
                'C': '0.95*np.cos(2*np.pi*110*t)'
            }, volume=0.25)
