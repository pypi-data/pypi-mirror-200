
import math
import numpy as np
import pandas as pd
import xarray as xr


_SOLAR_CONSTANT = 0.0820

_LATITUDE_RADIANS_MIN = np.deg2rad(-90.0)
_LATITUDE_RADIANS_MAX = np.deg2rad(90.0)

_SOLAR_DECLINATION_RADIANS_MIN = np.deg2rad(-23.45)
_SOLAR_DECLINATION_RADIANS_MAX = np.deg2rad(23.45)

_SUNSET_HOUR_ANGLE_RADIANS_MIN = 0.0
_SUNSET_HOUR_ANGLE_RADIANS_MAX = np.deg2rad(180)


def _solar_declination(day_of_year: np.ndarray) -> np.ndarray:
    """
    Calculate solar declination from day of the year.
    Based on FAO equation 24 in Allen et al (1998).

    Args:
        day_of_year (np.ndarray): Array of day of year integers
            between 1 and 365 or 366).

    Raises:
        ValueError: If values of the array is not within the range [1-366].

    Returns:
        np.ndarray: Solar declination [radians]
    """

    if not np.all(np.logical_and(day_of_year >= 1, day_of_year <= 366)):
        raise ValueError(
            "Elements of day_of_year must be in the range [1-366].")

    return 0.409 * np.sin((2.0 * math.pi / 365.0) * day_of_year - 1.39)


def _sunset_hour_angle(latitude_radians: np.ndarray,
                       solar_declination_radians: np.ndarray) -> np.ndarray:
    """
    Calculate sunset hour angle (*Ws*) from latitude and solar declination.
    Based on FAO equation 25 in Allen et al (1998).

    Args:
        latitude_radians (np.ndarray): Latitude in radians,
            must have shape of (n_x, 1).
        solar_declination_radians (np.ndarray): Solar declination in radians,
            must have shape of (n_y).

    Returns:
        np.ndarray: Sunset hour angle in radians, with shape of (n_x, n_y).
    """

    if not np.all(np.logical_and(latitude_radians >= _LATITUDE_RADIANS_MIN,
                                 latitude_radians <= _LATITUDE_RADIANS_MAX)):
        raise ValueError(
            f"Elements of latitude_radians are outside of valid range:"
            f"[{_LATITUDE_RADIANS_MIN} to {_LATITUDE_RADIANS_MAX}].")

    if not np.all(np.logical_and(
            solar_declination_radians >= _SOLAR_DECLINATION_RADIANS_MIN,
            solar_declination_radians <= _SOLAR_DECLINATION_RADIANS_MAX)):

        raise ValueError(
            f"Elements of solar_declination_radians are outside of valid range:"
            f"[{_SOLAR_DECLINATION_RADIANS_MIN} to"
            f"{_SOLAR_DECLINATION_RADIANS_MAX}].")

    cos_sunset_hour_angle = - \
        np.tan(latitude_radians) * np.tan(solar_declination_radians)

    return np.arccos(np.clip(cos_sunset_hour_angle, -1, 1))


def _inv_rel_dist_earth_sun(day_of_year: np.ndarray) -> np.ndarray:
    """
    Calculate the inverse relative distance between earth and sun from
    day of the year. Based on FAO equation 23 in Allen et al (1998)

    Args:
        day_of_year (np.ndarray): Array of day of year integers
            between 1 and 365 or 366).

    Returns:
        np.ndarray: Inverse relative distance between earth and the sun.
    """
    if not np.all(np.logical_and(day_of_year >= 1, day_of_year <= 366)):
        raise ValueError(
            "Elements of day_of_year must be in the range [1-366].")

    return 1 + (0.033 * np.cos((2.0 * math.pi / 365.0) * day_of_year))


def _et_rad(latitude_radians: np.ndarray,
            solar_declination_radians: np.ndarray,
            sunset_hour_angle_radians: np.ndarray,
            inv_rel_dist: np.ndarray) -> np.ndarray:
    """
    Estimate daily extraterrestrial radiation (*Ra*, 'top of the atmosphere
    radiation').

    Based on equation 21 in Allen et al (1998). If monthly mean radiation is
    required make sure *sol_dec*. *sha* and *irl* have been calculated using
    the day of the year that corresponds to the middle of the month

    Args:
        latitude_radians (np.ndarray): Latitude in radians,
            must have shape of (n_x, 1).
        solar_declinations_radians (np.ndarray): Solar declination [radians],
            with shape of (n_y).
        sunset_hour_angle_radians (np.ndarray): Sunset hour angle [radians],
            with shape of (n_x, n_y).
        inv_rel_dist (np.ndarray): Inverse relative distance between
            earth and the sun.

    Returns:
        np.ndarray: Daily extraterrestrial radiation [MJ m-2 day-1].
    """

    if not np.all(np.logical_and(latitude_radians >= _LATITUDE_RADIANS_MIN,
                                 latitude_radians <= _LATITUDE_RADIANS_MAX)):
        raise ValueError(
            f"Elements of latitude_radians are outside of valid range:"
            f"[{_LATITUDE_RADIANS_MIN} to {_LATITUDE_RADIANS_MAX}].")

    if not np.all(np.logical_and(
            solar_declination_radians >= _SOLAR_DECLINATION_RADIANS_MIN,
            solar_declination_radians <= _SOLAR_DECLINATION_RADIANS_MAX)):

        raise ValueError(
            f"Elements of solar_declination_radians are outside of valid range:"
            f"[{_SOLAR_DECLINATION_RADIANS_MIN} to"
            f"{_SOLAR_DECLINATION_RADIANS_MAX}].")

    if not np.all(np.logical_and(
            sunset_hour_angle_radians >= _SUNSET_HOUR_ANGLE_RADIANS_MIN,
            sunset_hour_angle_radians <= _SUNSET_HOUR_ANGLE_RADIANS_MAX)):

        raise ValueError(
            f"Elements of sunset_hour_angle_radians are outside of valid range:"
            f"[{_SUNSET_HOUR_ANGLE_RADIANS_MIN} to"
            f"{_SUNSET_HOUR_ANGLE_RADIANS_MAX}].")

    tmp1 = (24.0 * 60.0) / math.pi
    tmp2 = sunset_hour_angle_radians * \
        np.sin(latitude_radians) * np.sin(solar_declination_radians)
    tmp3 = (
        np.cos(latitude_radians)
        * np.cos(solar_declination_radians)
        * np.sin(sunset_hour_angle_radians)
    )

    return (tmp1 * _SOLAR_CONSTANT * inv_rel_dist * (tmp2 + tmp3))


def eto_hargreaves(dataset: xr.Dataset,
                   temp_keys: dict) -> xr.DataArray:
    """
    Estimate potential evapotranspiration over grass (ETo) using the Hargreaves
    equation. Based on equation 52 in Allen et al (1998).

    Data must be in a WGS84 coordinate system with coordinates names of must be 
    either 'lat' or 'y' for latitude and 'lon' or 'x' for longitude.
    Args:
        dataset (xr.Dataset): Dataset containing the daily temperatures [deg C].
        temp_keys (dict): Dictionary setting the keys of the min,
            max and optionally the mean temperature variable names,
            e.g. {'min': 'temp_min', 'max': 'temp_max', 'mean': 'temp_mean'}

    Returns:
        xr.DataArray: Potential evapotranspiration over grass (ETo) [mm day-1]
    """

    lat_var_name = 'lat' if 'lat' in dataset.dims else 'y'
    lon_var_name = 'lon' if 'lon' in dataset.dims else 'x'

    if lat_var_name and lon_var_name not in dataset.dims:
        raise KeyError("Invalid spatial coordinate dimension names. "
                       "Spatial coordinates names of either 'lat' or 'y' for "
                       "latitude and 'lon' or 'x' for longitude.")

    def _date_str_to_dayofyear(date: str):
        return pd.Timestamp(date).day_of_year

    day_of_year_arr = np.array(list(map(_date_str_to_dayofyear,
                                        dataset['time'].values)))
    solar_declination = _solar_declination(day_of_year_arr)

    latitude_rad = dataset[lat_var_name].values * math.pi / 180
    latitude_rad.shape = (latitude_rad.size, 1)
    sunset_hour_angle = _sunset_hour_angle(latitude_rad, solar_declination)

    inv_rel_distance = _inv_rel_dist_earth_sun(day_of_year_arr)

    et_radiation = _et_rad(latitude_rad, solar_declination,
                           sunset_hour_angle, inv_rel_distance)

    et_radiation = np.transpose(np.ones((dataset[lon_var_name].size, 1, 1))
                                * et_radiation)
    try:
        min_var_name = temp_keys['min']
        max_var_name = temp_keys['max']
        mean_var_name = temp_keys.get('mean')

        if mean_var_name is None:
            dataset['temp_mean'] = (
                dataset[min_var_name] + dataset[max_var_name]) / 2
            mean_var_name = 'temp_mean'

        pet = (0.0023 * (dataset[mean_var_name] + 17.8) *
               (dataset[max_var_name] - dataset[min_var_name]) ** 0.5
               * 0.408 * et_radiation)

    except KeyError as error:
        raise KeyError("Invalid variable keys.")

    except Exception as error:
        raise ValueError(
            "Coudn't calculate potential evapotranspiration.") from error

    return pet.compute()
