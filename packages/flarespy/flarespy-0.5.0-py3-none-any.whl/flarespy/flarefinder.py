import warnings
import logging

import lightkurve as lk
import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.stats import mad_std
from astropy.utils.exceptions import AstropyUserWarning
from astroquery.exceptions import TableParseError
from astroquery.gaia import Gaia
from astroquery.jplhorizons import Horizons
from astroquery.mast import Catalogs
from astroquery.simbad import Simbad
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import MaxNLocator
from retrying import retry
from wotan import flatten

from .utils import (
    CANDIDATES_COLUMNS,
    extend,
    fill_gaps,
    find_consecutive,
    get_flare_probability,
)

logging.getLogger("astroquery").setLevel(logging.WARNING)

CUSTOM_SIMBAD = Simbad()
CUSTOM_SIMBAD.add_votable_fields("otype")
CUSTOM_SIMBAD.add_votable_fields("otypes")

Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
Gaia.ROW_LIMIT = -1

CVs = ["CataclyV*", "CataclyV*_Candidate", "Nova", "Nova_Candidate"]

# Zero point TESS flux (from Sullivan 2017)
TESS_FLUX0 = 4.03e-6 * u.erg / u.s / u.cm**2


def load_from_lightkurve(lc):
    with warnings.catch_warnings():
        warnings.simplefilter("error", category=lk.LightkurveWarning)

        try:
            lc.meta["ZERO_CENTERED"] = False
            negative_ratio = (lc.flux.value < -30).nonzero()[0].size / lc.flux.nonzero()[0].size
            if negative_ratio > 0.1:
                raise lk.LightkurveWarning
            lc = lc.normalize()
        except lk.LightkurveWarning:
            try:
                lc = lc.select_flux("sap_flux").normalize()
            except lk.LightkurveWarning:
                lc.meta["ZERO_CENTERED"] = True
                lc.flux += lc.flux.std() - lc.flux.min()
                lc = lc.normalize()

    flc = FlareLightCurve(lc)

    return flc


class FlareLightCurve(lk.LightCurve):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta["candidates"] = None

    def _generate_model(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            pg = self.to_periodogram()
            period = pg.period_at_max_power.value
            snr = pg.max_power / np.nanmedian(pg.power)

            if period < 10 and snr > 5:
                pg = self.to_periodogram(
                    minimum_period=max(period - 0.2, 0.01),
                    maximum_period=period + 0.2,
                    oversample_factor=1000,
                )
                period = pg.period_at_max_power.value
            else:
                period = -999

            self.meta["PERIOD"] = period

        if 0.05 < period < 2:
            period_array = np.array([1, 2, 4]) * period
            std_array = np.zeros_like(period_array)
            folded_lc_list = []
            trend_folded_flux_list = []

            for i, period in enumerate(period_array):
                folded_lc = self.fold(period)
                detrended_folded_flux, trend_folded_flux = flatten(
                    folded_lc.time.value,
                    folded_lc.flux,
                    method="median",
                    window_length=period / 50,
                    return_trend=True,
                )
                std_array[i] = np.nanstd(detrended_folded_flux)
                folded_lc_list.append(folded_lc)
                trend_folded_flux_list.append(trend_folded_flux)

            std_array *= 0.75 ** np.arange(len(period_array))[::-1]
            index = std_array.argmin()
            self.meta["PERIOD"] = period_array[index]
            trend_folded_flux = trend_folded_flux_list[index]
            folded_lc = folded_lc_list[index]

            return trend_folded_flux[folded_lc.time_original.argsort()] - 1
        return 0

    def _mask_eclipse(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=AstropyUserWarning)

            sigma = mad_std(self.flux, ignore_nan=True)
            eclipse_mask = self.flux < np.nanmedian(self.flux) - 3 * sigma
            if hasattr(self.flux, "mask"):
                eclipse_mask = np.logical_xor(eclipse_mask, self.flux.mask)

            i_start_array, i_stop_array = find_consecutive(
                np.nonzero(eclipse_mask)[0],
                3,
                gap=1.2 * self.meta["TIMEDEL"],
                data=self.time.value,
            )

            lc = self.copy()
            if i_start_array is not None:
                if i_start_array.size > 3 and lc.time.value[i_start_array[0]] < lc.time.value[i_stop_array[-1]] - 10:
                    for i in range(i_start_array.size):
                        t_start = self.time.value[i_start_array[i]]
                        t_stop = self.time.value[i_stop_array[i]]
                        duration = t_stop - t_start
                        t_start_ext, t_stop_ext = extend(
                            lc.time.value,
                            (lc.flux - 1) / sigma,
                            t_start,
                            t_stop,
                            duration,
                            n_sigma=0,
                            mode=-1,
                        )
                        lc.flux[(self.time.value >= t_start_ext) & (self.time.value <= t_stop_ext)] = np.nan

            self.meta["eclipse_mask"] = np.isnan(lc.flux)

        return lc

    def _extend_multiple_events(self, i_start_array, i_stop_array, max_extend_indexes=45):
        i_start_ext_array = np.zeros_like(i_start_array)
        i_stop_ext_array = np.zeros_like(i_stop_array)

        lc = self.copy()
        lc.flux[self.eclipse_mask] = np.nan
        lc = lc.remove_nans()

        for i in range(i_start_array.size):
            i_start = i_start_array[i]
            t_start = self.time.value[i_start]
            i_stop = i_stop_array[i]
            t_stop = self.time.value[i_stop]

            t_max_extend = (max_extend_indexes + 0.2) * self.meta["TIMEDEL"]
            t_start_ext, t_stop_ext = extend(
                lc.time.value,
                lc.standardized_flux,
                t_start,
                t_stop,
                t_max_extend,
                n_right=2,
            )
            i_start_ext_array[i] = np.nonzero(self.time.value == t_start_ext)[0][0]
            i_stop_ext_array[i] = np.nonzero(self.time.value == t_stop_ext)[0][0]

        i_overlap = np.nonzero(i_start_ext_array[1:] <= i_stop_ext_array[:-1])[0] + 1
        i_overlap_start, i_overlap_stop = find_consecutive(i_overlap, 1)

        if i_overlap_start is not None:
            i_stop_ext_array[i_overlap_start - 1] = i_stop_ext_array[i_overlap_stop]
            i_start_ext_array = np.delete(i_start_ext_array, i_overlap)
            i_stop_ext_array = np.delete(i_stop_ext_array, i_overlap)

        return i_start_ext_array, i_stop_ext_array

    def _standardize(self):
        flux_series = pd.Series(self.detrended_flux.value, index=pd.DatetimeIndex(self.time.datetime))

        rolling_window = flux_series.rolling(pd.Timedelta(2, unit="d"), center=True)
        rolling_std = rolling_window.apply(mad_std, kwargs={"ignore_nan": True})
        rolling_std[np.isnan(self.detrended_flux.value)] = np.nan

        standardized_flux = (self.detrended_flux.value - 1) / rolling_std

        self.add_columns([rolling_std, standardized_flux], names=["rolling_std", "standardized_flux"])

    @retry(stop_max_attempt_number=5)
    def _query_object_type_from_simbad(self):
        """Query object info from Simbad."""

        with warnings.catch_warnings():
            warnings.simplefilter("error", category=UserWarning)
            try:
                query_result = CUSTOM_SIMBAD.query_object(self.label)
            except TableParseError:
                try:
                    obj_coord = SkyCoord(self.ra, self.dec, unit=(u.deg, u.deg), frame="icrs")
                    query_result = CUSTOM_SIMBAD.query_region(obj_coord, radius=3 * u.arcsec)
                    if len(query_result) > 1:
                        simbad_coords = SkyCoord(
                            query_result["RA"].data.data,
                            query_result["DEC"].data.data,
                            unit=(u.hourangle, u.deg),
                        )
                        distance = obj_coord.separation(simbad_coords)
                        query_result = query_result[distance.value.argmin()]
                except TableParseError:
                    query_result = None

        if query_result is None:
            self.meta["otype"] = "/"
        else:
            self.meta["otype"] = query_result["OTYPE"][0]
            if "CV*" in query_result["OTYPES"][0].split("|"):
                self.meta["otype"] = "CataclyV*"

    @retry(stop_max_attempt_number=5)
    def _calculate_stellar_luminosity(self):
        # Query parallax from Gaia DR3
        coord = SkyCoord(self.ra, self.dec, unit="deg", frame="icrs", equinox="J2000")
        radius = u.Quantity(5, u.arcsec)
        try:
            gaia_dr3_data = Gaia.cone_search_async(coord, radius).get_results()[0]
            plx = gaia_dr3_data["parallax"]
            if hasattr(plx, "mask"):
                plx = np.nan
        except IndexError:
            plx = np.nan

        # Query TESS mag from TIC
        tic_data = Catalogs.query_object(self.label, radius=0.02, catalog="TIC")
        tic_data.add_index("ID")
        try:
            target_row = tic_data.loc[str(self.ticid)]
            t_mag = target_row["Tmag"]
        except KeyError:
            t_mag = np.nan

        # Calculate stellar luminosity
        if np.isnan(plx) or np.isnan(t_mag):
            self.meta["lum"] = np.nan
        else:
            plx /= 1000
            dist = 1 / plx * u.pc
            flux = 10 ** (-t_mag / 2.5) * TESS_FLUX0
            lum = 4 * np.pi * dist.to(u.cm) ** 2 * flux
            self.meta["lum"] = lum.value

    @retry(stop_max_attempt_number=5)
    def _is_sso(self, i_peak: int, radius: float = 8):
        """Check if a candidate is caused by a Solar System Object (SSO) encounter."""

        mask = np.zeros_like(self.time, dtype=bool)
        mask[i_peak] = True

        try:
            res = self.query_solar_system_objects(cadence_mask=mask, radius=radius * 21 / 3600, show_progress=False)
        except OSError:
            res = self.query_solar_system_objects(
                cadence_mask=mask,
                radius=radius * 21 / 3600,
                cache=False,
                show_progress=False,
            )

        if res is not None:
            ap_mag = np.zeros(len(res))
            for row in res.itertuples():
                try:
                    obj = Horizons(
                        id=row.Name.strip(),
                        location="500@-95",
                        epochs=row.epoch,
                        id_type="smallbody",
                    )
                    eph = obj.ephemerides(quantities=9)
                except ValueError:
                    obj = Horizons(
                        id=row.Num,
                        location="500@-95",
                        epochs=row.epoch,
                        id_type="smallbody",
                    )
                    eph = obj.ephemerides(quantities=9)
                try:
                    ap_mag[row.Index] = eph["V"].value
                except KeyError:
                    ap_mag[row.Index] = eph["Tmag"].value
            if (ap_mag < 19).any():
                return True

        return False

    def _is_at_edge(self, i_start: int, i_stop: int, window: float = 0.1):
        """Check if a candidate is at the edge of the lightcurve."""

        time = self.time[np.isfinite(self.standardized_flux)].value
        t_start = self.time.value[i_start]
        t_stop = self.time.value[i_stop]

        before = np.nonzero((time > t_start - window) & (time < t_start))[0]
        after = np.nonzero((time > t_stop) & (time < t_stop + window))[0]

        return False if (before.size and after.size) else True

    def detrend(self, window_length=0.3):
        """Detrend the lightcurve."""

        self._query_object_type_from_simbad()

        masked_lc = self._mask_eclipse()
        model_flux = self._generate_model()
        detrended_flux, trend_flux = flatten(
            self.time.value,
            masked_lc.flux - model_flux,
            method="biweight",
            window_length=window_length,
            return_trend=True,
        )
        trend_flux += model_flux
        self.add_columns(
            [detrended_flux * self.flux.unit, trend_flux * self.flux.unit],
            names=["detrended_flux", "trend_flux"],
        )
        self._standardize()

    def find_candidates(self, n_sigma: float = 3, n_consecutive: int = 2):
        """Find the candidates of flares."""

        if self.otype not in CVs:
            i_outliers = np.nonzero(self.standardized_flux > n_sigma)[0]

            i_start_array, i_stop_array = find_consecutive(
                i_outliers,
                n_consecutive,
                gap=1.2 * self.meta["TIMEDEL"],
                data=self.time.value,
            )

            if i_start_array is not None:
                i_start_ext_array, i_stop_ext_array = self._extend_multiple_events(i_start_array, i_stop_array)

                at_edge = np.zeros_like(i_start_ext_array, dtype=bool)
                for i in range(at_edge.size):
                    at_edge[i] = self._is_at_edge(i_start_ext_array[i], i_stop_ext_array[i])

                if not at_edge.all():
                    i_start_ext_array = i_start_ext_array[~at_edge]
                    i_stop_ext_array = i_stop_ext_array[~at_edge]

                    i_peak_array = np.copy(i_start_ext_array)
                    for i in range(i_start_ext_array.size):
                        i_peak = self.standardized_flux[i_start_ext_array[i] : i_stop_ext_array[i] + 1].argmax()
                        i_peak_array[i] += i_peak

                    self.candidates = pd.DataFrame(columns=CANDIDATES_COLUMNS)
                    self.candidates.i_start = i_start_ext_array
                    self.candidates.i_peak = i_peak_array
                    self.candidates.i_stop = i_stop_ext_array
                    self.candidates.t_start = self.time.value[i_start_ext_array]
                    self.candidates.t_peak = self.time.value[i_peak_array]
                    self.candidates.t_stop = self.time.value[i_stop_ext_array]

    def detect_sso(self):
        """Detect if the candidates are caused by SSO encounters."""

        if self.candidates is not None:
            sso = np.zeros(len(self.candidates), dtype=bool)
            for row in self.candidates.itertuples():
                sso[row.Index] = self._is_sso(row.i_peak)

            self.candidates.sso = sso

    def calculate_parameters(self):
        """Calculate the parameters of the candidates."""

        if self.candidates is not None:
            proba_array = np.zeros(len(self.candidates))
            snr_array = np.zeros(len(self.candidates))
            for row in self.candidates.itertuples():
                lc_candidate = self[row.i_start : row.i_stop + 1].remove_nans("standardized_flux")
                time = lc_candidate.time.value
                flux = lc_candidate.standardized_flux.value

                if not (np.diff(lc_candidate.cadenceno) == 1).all():
                    time, flux = fill_gaps(time, flux, lc_candidate.cadenceno)

                if flux.size >= 4:
                    proba_array[row.Index] = round(get_flare_probability(time, flux), 3)
                snr_array[row.Index] = round(np.max(flux), 2)

            self.candidates.flare_prob = proba_array
            self.candidates.snr = snr_array

            if not self.meta["ZERO_CENTERED"]:
                amp = np.zeros(len(self.candidates))
                dur = np.zeros(len(self.candidates))
                ed = np.zeros(len(self.candidates))
                self._calculate_stellar_luminosity()

                n_row = 0
                for row in self.candidates.itertuples():
                    time = self.time.value[row.i_start : row.i_stop + 1]
                    flux = self.detrended_flux[row.i_start : row.i_stop + 1]
                    amp[n_row] = np.nanmax(flux) - 1
                    dur[n_row] = (time[-1] - time[0]) * 1440
                    mask = np.isnan(flux)
                    ed[n_row] = np.trapz(flux[~mask] - 1, x=time[~mask] * 86400)
                    n_row += 1

                self.candidates.amp = np.round(amp, 3)
                self.candidates.dur = np.round(dur, 1)
                self.candidates.ed = np.round(ed, 2)
                if np.isnan(self.lum):
                    self.candidates.energy = np.full(len(self.candidates), np.nan)
                else:
                    energy = ed * self.lum
                    self.candidates.energy = [np.format_float_scientific(x, precision=2) for x in energy]

    def find_flares(self):
        self.detrend()
        self.find_candidates()
        self.detect_sso()
        self.calculate_parameters()

    def output_data(self, folder):
        if self.candidates is not None:
            output = self.candidates.copy()

            output.insert(0, "label", self.label)
            output.insert(1, "sector", self.sector)
            output.t_start = np.round(self.candidates.t_start, 7)
            output.t_peak = np.round(self.candidates.t_peak, 7)
            output.t_stop = np.round(self.candidates.t_stop, 7)

            output.to_csv(
                folder / "{}-S{}.csv".format(self.label.replace(" ", ""), self.sector),
                index=False,
            )

    def plot_candidates(self, figure_folder, threshold=0.5):
        """Plot the candidates."""

        if self.candidates is not None:
            t_extend = 30.2 * self.meta["TIMEDEL"]
            finite_mask = np.isfinite(self.standardized_flux)

            self.candidates.loc[self.candidates.sso, "flare_prob"] = -999
            cond_list = [
                self.candidates.flare_prob >= threshold,
                self.candidates.flare_prob == -999,
            ]
            candidate_type_array = np.select(cond_list, ["flare", "sso"], "non-flare")
            color_array = np.select(cond_list, ["tab:red", "tab:orange"], "tab:gray")
            with plt.style.context(lk.MPLSTYLE):
                for row in self.candidates.itertuples():
                    candidate_type = candidate_type_array[row.Index]
                    color = color_array[row.Index]
                    figure_subfolder = figure_folder / candidate_type
                    figure_subfolder.mkdir(exist_ok=True)

                    fig = plt.figure(figsize=(14, 4))

                    ax_label = fig.add_subplot(111)
                    ax_label.spines[["top", "bottom", "left", "right"]].set_visible(False)
                    ax_label.set_xlabel("Time - 2457000 [BTJD days]")
                    ax_label.set_ylabel("Normalized Flux")
                    ax_label.minorticks_off()

                    ax_original_lc = fig.add_subplot(221)
                    self.scatter(ax=ax_original_lc, label="")
                    self.plot(
                        ax=ax_original_lc,
                        column="trend_flux",
                        color="tab:red",
                        label="",
                    )
                    ax_original_lc.set_xlabel("")
                    ax_original_lc.set_ylabel("")
                    ax_original_lc.set_xticklabels([])

                    ax_detrended_lc = fig.add_subplot(223)
                    self.scatter(ax=ax_detrended_lc, column="detrended_flux", label="")
                    ax_detrended_lc.plot(self.time.value, 1 + 3 * self.rolling_std, lw=1, c="tab:gray")

                    for element in self.candidates.itertuples():
                        alpha = 0.8 if row.Index == element.Index else 0.3

                        event_flux = self.detrended_flux[slice(element.i_start, element.i_stop + 1)]
                        extra_fill_region = (np.nanmax(event_flux) - np.nanmin(event_flux)) / 20
                        fill_lower_lim = np.nanmin(event_flux) - extra_fill_region
                        fill_upper_lim = np.nanmax(event_flux) + extra_fill_region

                        ax_detrended_lc.fill_between(
                            [element.t_start - 0.06, element.t_stop + 0.06],
                            fill_lower_lim,
                            fill_upper_lim,
                            facecolor=color_array[element.Index],
                            alpha=alpha,
                        )

                        ax_detrended_lc.annotate(
                            element.Index + 1,
                            (element.t_start - 0.5, fill_upper_lim),
                            c=color_array[element.Index],
                            alpha=alpha,
                        )

                    ax_detrended_lc.set_xlim(*ax_original_lc.get_xlim())
                    ax_detrended_lc.set_xlabel("")
                    ax_detrended_lc.set_ylabel("")

                    ax_event = fig.add_subplot(122)
                    ax_event.axhline(3, c="tab:gray", lw=1)
                    ax_event.axhline(1, c="tab:gray", ls="--", lw=1)
                    if candidate_type == "sso":
                        box_str = f"Cand {row.Index + 1}, {candidate_type}"
                    else:
                        box_str = (
                            f"Cand {row.Index + 1}, {candidate_type}\n"
                            f"flare prob: {row.flare_prob}\n"
                            f"snr: {row.snr}\n"
                            f"amp: {row.amp}\n"
                            f"dur: {row.dur} m\n"
                            f"ed: {row.ed} s\n"
                            f"{row.energy} erg"
                        )
                    at = AnchoredText(
                        box_str,
                        loc="upper right",
                        frameon=True,
                        prop={"multialignment": "right"},
                    )
                    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
                    ax_event.add_artist(at)

                    i_plot = (
                        (self.time.value >= row.t_start - t_extend)
                        & (self.time.value <= row.t_stop + t_extend)
                        & finite_mask
                    )
                    i_event = np.zeros_like(self.time.value, dtype=bool)
                    i_event[row.i_start : row.i_stop + 1] = True
                    i_event = i_event & finite_mask
                    self[i_plot].plot(
                        ax=ax_event,
                        column="standardized_flux",
                        label="",
                        lw=1,
                        ms=5,
                        marker=".",
                    )
                    self[i_event].plot(
                        ax=ax_event,
                        column="standardized_flux",
                        color=color,
                        label="",
                        lw=1.5,
                        ms=5,
                        marker=".",
                    )

                    ax_event.xaxis.set_major_locator(MaxNLocator(5))
                    ax_event.yaxis.set_major_locator(MaxNLocator(integer=True))
                    ax_event.set_xlim(
                        row.t_start - t_extend + self.meta["TIMEDEL"],
                        row.t_stop + t_extend - self.meta["TIMEDEL"],
                    )
                    if self.standardized_flux[i_plot].min() < -8:
                        ax_event.set_ylim(bottom=-8)
                    ax_event.set_xlabel("")
                    ax_event.set_ylabel("Standardized Flux")
                    ax_event.ticklabel_format(useOffset=False)
                    ax_event.yaxis.set_label_position("right")
                    ax_event.yaxis.tick_right()

                    ax_label.set_yticks(ax_detrended_lc.get_yticks())
                    ax_label.tick_params(
                        colors="w",
                        which="both",
                        top=False,
                        bottom=False,
                        left=False,
                        right=False,
                    )

                    period = "{:.2f}d".format(self.period) if self.period > 0 else "/"
                    title = f"{self.label}, Sector {self.sector}, {self.otype}, P={period}"

                    plt.suptitle(title, y=0.94, fontsize=15)
                    plt.subplots_adjust(hspace=0.05, wspace=0.012)

                    figure_path = figure_subfolder / "{}-S{}-{}.png".format(
                        self.label.replace(" ", ""), self.sector, round(row.t_peak, 7)
                    )
                    plt.savefig(figure_path, bbox_inches="tight")
                    plt.close()
