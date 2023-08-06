from functools import partial

import numpy as np
from skimage import exposure


def flatfield_correction(img, lf, df):
    fd_diff = lf - df
    return (img - df) * np.mean(fd_diff) / fd_diff


gamma_correction = exposure.adjust_gamma

normalize = partial(exposure.rescale_intensity, out_range=(0., 1.))
