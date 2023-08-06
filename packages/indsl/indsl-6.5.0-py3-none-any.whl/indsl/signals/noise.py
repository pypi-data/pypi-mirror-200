from typing import Optional

import numpy as np
import pandas as pd

from ..type_check import check_types


@check_types
def white_noise(
    data: pd.Series,
    snr_db: float = 30,
    seed: Optional[int] = None,
) -> pd.Series:
    """Add white noise.

    Adds white noise to the original data using a given signal-to-noise ratio (SNR).

    Args:
        data: Time series
        snr_db: SNR.
            Signal-to-noise ratio (SNR) in decibels. SNR is a comparison of the level of a signal to the level of
            background noise. SNR is defined as the ratio of signal power to noise power. A ratio higher than 1
            indicates more signal than noise. Defaults to 30.
        seed: Seed.
            A seed (integer number) to initialize the random number generator. If left empty, then a fresh,
            unpredictable value will be generated. If a value is entered, the exact random noise will be generated if
            the time series data and date range are not changed.

    Returns:
        pandas.Series: Output
            Original data plus white noise.
    """
    data_power = data.var()
    # Linear SNR
    snr = 10.0 ** (snr_db / 10.0)
    noise_power = data_power / snr
    rng = np.random.default_rng(seed)
    white_noise = np.sqrt(noise_power) * rng.standard_normal(len(data))

    return data + white_noise
