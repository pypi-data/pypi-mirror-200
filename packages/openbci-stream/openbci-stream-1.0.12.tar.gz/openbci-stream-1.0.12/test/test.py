from openbci_stream.utils import HDF5Reader
from matplotlib import pyplot as plt
import numpy as np


filename = 'record-03_22_23-11_04_00.h5'

with HDF5Reader(filename) as reader:

    reader.markers
    reader.generate_bad_markers()

    eeg = reader.eeg

    eeg
