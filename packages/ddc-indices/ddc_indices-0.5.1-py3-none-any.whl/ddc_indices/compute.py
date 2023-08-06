
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats

from .constants import Distribution, PniPeriods, SpeiPeriods, SpiPeriods


def compute_spi(data_prec: xr.DataArray,
                time_coverage_range: Tuple[pd.Timestamp, pd.Timestamp],
                time_reference_range: Tuple[pd.Timestamp, pd.Timestamp],
                period: SpiPeriods,
                distribution: Distribution,
                ref_months_list: List[int,],
                fitting_params: Optional[Tuple[xr.DataArray,
                                               xr.DataArray]] = None,
                index_name: str = 'SPI'
                ) -> Tuple[xr.DataArray, xr.DataArray, xr.DataArray]:
    """
    Calculates SPI (Standardized Precipitation Index).

    Args:
        data_prec (xr.DataArray): 3-D array of precipitation data as an
            xarray.DataArray. Must be monthly measurements.
        time_coverage_range (Tuple[pd.Timestamp, pd.Timestamp]): Time range tuple;
            (start time, end time).
        time_reference_range (Tuple[pd.Timestamp, pd.Timestamp]): Reference time range tuple;
            (start time, end time).
        period (SpiPeriods): Number of months, defining the period the SPI is
            calculated on, e.g. "MS3" in the case of SPI-3.
        distribution (Distribution): Distribution type to be used for the
            internal fitting/transform computation.
        ref_months_list (List[int,]): List of the reference months for which
            the SPI result attributed to.
        fitting_params (Union[None, Tuple[xr.DataArray, xr.DataArray]]):
            Pre-computed distribution fitting parameters.
        index_name (str, optional): Name of the result DataArray.

    Returns:
        Tuple[xr.DataArray, xr.DataArray, xr.DataArray]: Tuple of DataArrays
            containing the SPI result and fitting parameters.
    """

    array_list = []
    alpha_list = []
    theta_list = []

    data_rolling_sum = _get_rolling_sum(data_prec, period.value.get('value'))

    for ref_month in ref_months_list:

        indexes = _get_indexes(data=data_rolling_sum,
                               group_by=f"time.{period.value.get('unit')}",
                               group_index=ref_month)

        data_rolling_sum_i = data_rolling_sum.isel(time=indexes)

        data_rolling_sum_coverage_range = data_rolling_sum_i.sel(
            time=slice(time_coverage_range[0], time_coverage_range[1]))

        data_rolling_sum_reference_range = data_rolling_sum_i.sel(
            time=slice(time_reference_range[0], time_reference_range[1]))

        if distribution.value == Distribution.GAMMA.value:
            results = _fit_gamma(
                data_rolling_sum_coverage_range,
                data_rolling_sum_reference_range, fitting_params)
        else:
            raise NotImplementedError("Pearson correlation is not valid")

        array_list.append(results[0])
        alpha_list.append(results[1])
        theta_list.append(results[2])

    values = xr.concat(array_list, dim='time').chunk(
        chunks='auto').sortby('time')
    alpha = xr.concat(alpha_list, dim='time').chunk(chunks='auto')
    theta = xr.concat(theta_list, dim='time').chunk(chunks='auto')

    return (values.rename(index_name),
            alpha.rename('alpha'),
            theta.rename('theta'))


def compute_spei(data_prec: xr.DataArray,
                 data_pet: xr.DataArray,
                 time_coverage_range: Tuple[pd.Timestamp, pd.Timestamp],
                 time_reference_range: Tuple[pd.Timestamp, pd.Timestamp],
                 period: SpeiPeriods,
                 distribution: Distribution,
                 ref_months_list: List[int, ],
                 fitting_params: Optional[Tuple[xr.DataArray,
                                                xr.DataArray]] = None,
                 index_name: str = 'SPEI'
                 ) -> Tuple[xr.DataArray, xr.DataArray, xr.DataArray]:
    """
    Calculates SPEI (Standardized Precipitation Evapotranspiration Index).
    PET values are subtracted from the precipitation values to come up with an 
    array of (P - PET) values,
    which is then transformed similarly as SPI.

    Args:
        data_prec (xr.DataArray): 3-D array of precipitation data
            as an xarray.DataArray.
        data_pet (xr.DataArray): 3-D array of potential evapotranspiration
            data as an xarray.DataArray.
        time_coverage_range (Tuple[pd.Timestamp, pd.Timestamp]): Time range tuple
            (start time, end time).
        time_reference_range (Tuple[pd.Timestamp, pd.Timestamp]): Reference time range tuple
            (start time, end time).
        period (SpeiPeriods): Number of months, defining the period the SPEI is
            calculated on, e.g. "MS3" in the case of SPEI-3.
        distribution (Distribution): Distribution type to be used for
            the internal fitting/transform computation.
        ref_months_list (List[int, ]): List of the reference months for which
            the SPEI result attributed to.
        fitting_params (Union[None, Tuple[xr.DataArray, xr.DataArray]]):
            Pre-computed distribution fitting parameters.
        index_name (str, optional): Name of the result DataArray.

    Returns:
        Tuple[xr.DataArray, xr.DataArray, xr.DataArray]: Tuple of DataArrays
            containing the SPEI result and fitting parameters.
    """

    if data_prec.shape != data_pet.shape:
        raise ValueError("Incompatible precipitation and PET arrays")

    data = data_prec - data_pet + 1000.0

    return compute_spi(data, time_coverage_range, time_reference_range, period,
                       distribution, ref_months_list,
                       fitting_params, index_name=index_name)


def compute_pni(data_prec: xr.DataArray,
                time_coverage_range: Tuple[pd.Timestamp, pd.Timestamp],
                time_reference_range: Tuple[pd.Timestamp, pd.Timestamp],
                period: PniPeriods,
                ref_months_list: List[int, ],
                index_name: str = 'PNI') -> xr.DataArray:
    """
    Calculates PNI (Percent of Normal Index).

    Args:
        data_prec (xr.DataArray): 3-D array of precipitation data as
            an xarray.DataArray.
        time_coverage_range (Tuple[pd.Timestamp, pd.Timestamp]): Time range tuple
            (start time, end time).
        time_reference_range (Tuple[pd.Timestamp, pd.Timestamp]): Reference time range tuple
            (start time, end time).
        period (PniPeriods):  Number of days or months, defining the period the
            PNI is calculated on, e.g. "MS3" in the case of PNI-3.
        ref_months_list (Set[int, ]): List of the reference months for which
            the SPEI result attributed to.
        index_name (str, optional): Name of the result DataArray.

    Returns:
        xr.DataArray: DataArrays containing the PNI result.
    """

    array_list = []

    data_rolling_sum = _get_rolling_sum(data_prec, period.value.get('value'))

    for ref_month in ref_months_list:

        indexes = _get_indexes(
            data_rolling_sum, group_by="time.month", group_index=ref_month)
        data_rolling_sum_i = data_rolling_sum.isel(time=indexes)

        data_rolling_sum_coverage_range = data_rolling_sum_i.sel(
            time=slice(time_coverage_range[0], time_coverage_range[1]))
        data_rolling_sum_reference_range = data_rolling_sum_i.sel(
            time=slice(time_reference_range[0], time_reference_range[1]))

        # get the mean for the corresponding time_steps
        reference_data_rolling_mean = data_rolling_sum_reference_range.groupby(
            f"time.{period.value.get('unit')}").mean(dim='time')
        reference_data_rolling_mean = reference_data_rolling_mean.rename(
            {period.value.get('unit'): "band"})

        time_steps = data_rolling_sum_coverage_range.groupby(  #! Error is here
            f"time.{period.value.get('unit')}").groups.keys()
        percent_of_normal = xr.zeros_like(data_rolling_sum_coverage_range)
        for i in list(time_steps):
            indexes = _get_indexes(
                data_rolling_sum_coverage_range,
                group_by=f"time.{period.value.get('unit')}", group_index=i)
            data_sel = data_rolling_sum_coverage_range.isel(time=indexes)
            percent_of_normal[indexes, :, :] = (
                data_sel / reference_data_rolling_mean.sel(band=i))

        array_list.append(percent_of_normal)

    values = xr.concat(array_list, dim='time').chunk(
        chunks='auto').sortby("time")

    return values.rename(index_name)


def compute_pdsi():
    """Calculates PDSI (Palmer Drought Severity Index)."""
    raise NotImplementedError("PDSI is not implemented yet")


# --- Utility functions ---

def _get_rolling_sum(data: xr.DataArray,
                     period: int) -> xr.Dataset:
    """
    Get rolling sums.
    """

    # Calculate moving mean
    data_rolling_sum = data.rolling(
        time=period, center=False, min_periods=1).sum(skipna=False)
    return data_rolling_sum


def _get_indexes(data: xr.DataArray,
                 group_by: str,
                 group_index: int) -> List:
    """Get the indexes of groupby select."""

    indexes = data.groupby(group_by).groups[group_index]
    return sorted(indexes)


def _get_gamma_params(data: xr.DataArray) -> Tuple[xr.DataArray, xr.DataArray]:
    """
    Calculates gamma fitting parameters alpha and theta.
    """

    data_w = data.where(data != 0)  # Replacing 0 values with np.nan
    data_mean = data_w.mean(dim='time')  # Mean along the time axis
    data_log = np.log(data_w)  # Natural log of moving average

    a_param = np.log(data_mean) - data_log.sum('time')/data_log.sizes['time']

    alpha = (1/(4*a_param))*(1+(1+((4*a_param)/3))**0.5)
    theta = data_mean/alpha

    return alpha, theta


def _fit_gamma(data: xr.DataArray,
               reference_data: xr.DataArray,
               fitting_params: Union[None, Tuple[xr.DataArray, xr.DataArray]]
               ) -> Tuple[xr.DataArray, ...]:
    """
    Fit values to a gamma distribution and transform the values to
    corresponding normalized sigmas.
    """

    # Calculate fitting parameters if not provided
    alpha, theta = fitting_params or _get_gamma_params(reference_data)

    # find the percentage of zero values for each time step
    zeros = (data == 0).sum(axis=0)
    probabilities_of_zero = zeros / data.shape[0]

    # Gamma Distribution (CDF)
    def gamma_func(data, alpha, theta):
        return stats.gamma.cdf(data, a=alpha, scale=theta)

    gamma = xr.apply_ufunc(gamma_func, data, alpha, theta, dask='allowed')

    # (normalize including the probability of zero
    gamma_adj = (gamma * (1 - probabilities_of_zero)) + probabilities_of_zero

    # Standardized Precipitation Index (Inverse of CDF)
    def norm_func(data):
        return stats.norm.ppf(data, loc=0, scale=1)

    # loc is mean and scale is standard dev.
    norm = xr.apply_ufunc(norm_func, gamma_adj, dask='allowed')

    return norm, alpha, theta
