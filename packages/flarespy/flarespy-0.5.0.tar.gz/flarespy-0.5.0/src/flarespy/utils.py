import warnings

import joblib
import numpy as np
import pandas as pd
from tsfresh.feature_extraction import extract_features

from . import PACKAGEDIR

MODEL_PATH = PACKAGEDIR / "data" / "model.dat"
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)
    RFC_MODEL = joblib.load(MODEL_PATH)

CANDIDATES_COLUMNS = [
    "i_start",
    "i_peak",
    "i_stop",
    "t_start",
    "t_peak",
    "t_stop",
    "sso",
    "flare_prob",
    "snr",
    "amp",
    "dur",
    "ed",
    "energy",
]

FC_PARAMETERS = {
    "abs_energy": None,
    "first_location_of_maximum": None,
    "index_mass_quantile": [{"q": 0.5}],
    "kurtosis": None,
    "length": None,
    "maximum": None,
    "root_mean_square": None,
    "skewness": None,
    "standard_deviation": None,
}


def get_flare_probability(time, flux):
    time *= 1440
    data = pd.DataFrame({"time": time - time.min(), "flux": flux})
    data_id = np.ones(len(data), dtype=int)
    data.insert(0, "id", data_id)
    feature = extract_features(
        data,
        column_id="id",
        column_sort="time",
        default_fc_parameters=FC_PARAMETERS,
        disable_progressbar=True,
        n_jobs=0,
    )

    return RFC_MODEL.predict_proba(feature)[0][0]


def extend(time, flux, t_start, t_stop, t_max_extend, n_sigma=1, n_left=1, n_right=1, mode=1):
    indexes_range = np.nonzero((time >= t_start - t_max_extend) & (time <= t_stop + t_max_extend))[0]
    i_start = np.nonzero(time == t_start)[0][0]
    i_stop = np.nonzero(time == t_stop)[0][0]

    # left
    if mode == 1:
        while (flux[i_start - n_left : i_start] > n_sigma).any() and i_start > indexes_range[0]:
            i_start -= 1
            if i_start < n_left:
                i_start = 0
                break
        i_start = max(0, i_start - 1, indexes_range[0])
    elif mode == -1:
        while (flux[i_start - n_left : i_start] < n_sigma).any() and i_start > indexes_range[0]:
            i_start -= 1
            if i_start < n_left:
                i_start = 0
                break
        i_start = max(0, i_start - 1, indexes_range[0])

    # right
    if mode == 1:
        while (flux[i_stop + 1 : i_stop + 1 + n_right] > n_sigma).any() and i_stop < indexes_range[-1]:
            i_stop += 1
            if i_stop + 1 + n_right > time.size:
                i_stop = time.size - 1
                break
        i_stop = min(time.size - 1, i_stop + 1, indexes_range[-1])
    elif mode == -1:
        while (flux[i_stop + 1 : i_stop + 1 + n_right] < n_sigma).any() and i_stop < indexes_range[-1]:
            i_stop += 1
            if i_stop + 1 + n_right > time.size:
                i_stop = time.size - 1
                break
        i_stop = min(time.size - 1, i_stop + 1, indexes_range[-1])

    return time[i_start], time[i_stop]


def find_consecutive(indexes, n_consecutive, gap=1, data=None):
    if data is None:
        grouped_data = np.split(indexes, np.nonzero(np.diff(indexes) > gap)[0] + 1)
    else:
        grouped_data = np.split(indexes, np.nonzero(np.diff(data[indexes]) > gap)[0] + 1)

    grouped_consecutive_data = [x for x in grouped_data if x.size >= n_consecutive]

    if len(grouped_consecutive_data):
        i_start_array = np.array([x[0] for x in grouped_consecutive_data], dtype=int)
        i_stop_array = np.array([x[-1] for x in grouped_consecutive_data], dtype=int)
        return i_start_array, i_stop_array
    else:
        return None, None


def fill_gaps(time, flux, cadenceno):
    """Fill gaps in the data by interpolation."""

    newdata = {}

    dt = time - np.median(np.diff(time)) * cadenceno
    ncad = np.arange(cadenceno[0], cadenceno[-1] + 1, 1)
    in_original = np.in1d(ncad, cadenceno)
    ncad = ncad[~in_original]
    ndt = np.interp(ncad, cadenceno, dt)

    ncad = np.append(ncad, cadenceno)
    ndt = np.append(ndt, dt)
    ncad, ndt = ncad[np.argsort(ncad)], ndt[np.argsort(ncad)]
    ntime = ndt + np.median(np.diff(time)) * ncad
    newdata["cadenceno"] = ncad

    nflux = np.zeros(len(ntime))
    nflux[in_original] = flux
    nflux[~in_original] = np.interp(ntime[~in_original], time, flux)

    return ntime, nflux
