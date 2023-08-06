# functions to emulate common image editor adjustment functions
import numpy as np


def exposure(img, val):
    return img * 2 ** val


def shadows(img, val):
    """Adapted from:
    https://gist.github.com/HViktorTsoi/8e8b0468a9fb07842669aa368382a7df"""
    shadow_val = 1. + val / 100. * 2
    shadow_mid = 3. / 10.
    shadow_region = np.clip(1. - img / shadow_mid, 0, 1)
    shadow_region[np.where(img >= shadow_mid)] = 0
    return (1 - shadow_region) * img + shadow_region * (
            1 - np.power(1 - img, shadow_val))
