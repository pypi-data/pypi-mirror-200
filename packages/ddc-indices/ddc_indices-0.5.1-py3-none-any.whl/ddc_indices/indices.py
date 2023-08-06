from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from os import PathLike
from typing import Dict, List, MutableMapping, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import zarr
from dask.delayed import Delayed
from pydantic import ValidationError
from xarray.backends import ZarrStore

from .compute import compute_pni, compute_spei, compute_spi
from .config import IndexConfig, PdsiConfig, PniConfig, SpeiConfig, SpiConfig
from .constants import (DEFAULT_BBOX, DEFAULT_PERIOD, DEFAULT_REF_MONTHS_LIST,
    DEFAULT_COVERAGE_TIME_RANGE, DEFAULT_REFERENCE_TIME_RANGE, Periodicity)
from .errors import (DataValidationError, IndexCalculationError,
                     IndexConfigurationError)
from .eto import eto_hargreaves
from .metadata import DDC_INDICES_METADATA


class DdcIndices:
    """
    A container for implemented indices.

    Use DdcIndices().initialize() method to initialize the desired index.
    Note: You must support a valid xarray dataset and an IndexConfig object.

    """

    def __init__(self):
        self._indices = {}

        def _register(key: str, index: Index):
            self._indices[key] = index

        _register('SPI', Spi)
        _register('SPEI', Spei)
        _register('PNI', Pni)
        _register('PDSI', Pdsi)

    def initialize(self, dataset: xr.Dataset, config: IndexConfig) -> Index:
        """
        Initialize a DdcIndices instance. Currently supported indices are:
        SPI, SPEI, PNI and PDSI.

        Args:
            dataset (xr.Dataset): 3-D dataset of containing meteorological data
                as an xarray.Dataset. Must be daily or monthly measurements.
                Also, dimensions should be either 
                (time, lat, lon) or (time, x, y).
            config (IndexConfig): Index configuration object.

        Examples:
            # Create an SpiConfig object
            >>> variables = {'prec': 'prec'}
            >>> periodicity = 'daily'
            >>> config = SpiConfig(variables=variables,
                                   periodicity=periodicity)
            # Create an SPI index object
            >>> spi = DdcIndices().initialize(dataset, config)

        """
        try:
            index = self._indices[config.name.upper()]
        except (KeyError, AttributeError) as err:
            raise IndexConfigurationError(
                'Invalid index configuration.') from err

        return index(dataset, config)

    @staticmethod
    def describe_indices(name: Optional[str] = None):
        """Description of available indices.

        Args:
            name (Optional[str]): Name of the specific index.
                Fore example 'SPI'.
        """

        if name:
            return DDC_INDICES_METADATA.get('name')

        return DDC_INDICES_METADATA


class Index(ABC):
    """Abstract interface for various meteorological index calculations."""

    @abstractmethod
    def compute(self) -> None:
        """Compute index."""

    @staticmethod
    def save_to_zarr(dataset: xr.Dataset,
                     store: Union[MutableMapping, str, PathLike[str]],
                     chunks: Optional[Union[int, Dict, Tuple]] = 'auto',
                     mode: Optional[List["w", "w-", "a", "r+"]] = None,
                     **kwargs) -> Union[ZarrStore, Delayed]:
        """
        Write dataset to a zarr group.
        Uses xarray.Dataset.to_zarr method.

        Args:
            dataset (xr.Dataset): Dataset to write to zarr.
            store (Union[MutableMapping, str, PathLike[str]]): Store or path to
                directory in local or remote file system.
            chunk (Union[int, Dict, Tuple, 'auto']): Chunk sizes along each
                dimension, e.g., 5 or {'x': 5, 'y': 5}. If chunks=’auto’,
                dask chunks are created based on the variable’s zarr chunks.
                If chunks=None, zarr array data will lazily convert to numpy
                arrays upon access. This accepts all the chunk
                specifications as Dask does.
            mode (Optional[List["w", "w-", "a", "r+"]]): “w” means create
                (overwrite if exists); “w-” means create (fail if exists);
                “a” means override existing variables
                (create if does not exist); “r+” means modify existing array
                values only (raise an error if any metadata or shapes
                would change). The default mode is “a” if append_dim is set.
                Otherwise, it is “r+” if region is set and w- otherwise.

        Keyword Args:
            **kwargs: Additional keyword arguments. See 'xarray.Dataset.to_zarr'
                properties, under
                https://docs.xarray.dev/en/stable/generated/xarray.Dataset.to_zarr.html.

        Returns:
            Union[ZarrStore, Delayed]: ZarrStore if compute is True,
                dask.delayed.Delayed otherwise.
        """

        dataset = dataset.chunk(chunks=chunks)
        if mode == 'a':
            root = zarr.group(store)
            time_coverage_start = root.attrs.get('time_coverage_start')
            if time_coverage_start:
                dataset.attrs['time_coverage_start'] = time_coverage_start
        dataset.to_zarr(store, mode=mode, compute=True, **kwargs)

    @staticmethod
    def validate_dataset(dataset: xr.Dataset) -> xr.Dataset:

        if not isinstance(dataset, xr.Dataset):
            raise ValueError("Invalid data, type must be xr..Dataset.")
        # Rename lat/lon style dim names to y/x
        if set(dataset.dims) == {'time', 'lat', 'lon'}:
            dataset = dataset.rename({'lat': 'y', 'lon': 'x'})

        if set(dataset.dims) == {'time', 'y', 'x'}:
            dataset = dataset.transpose('time', 'y', 'x').chunk(
                chunks='auto').sortby('time')
        else:
            raise ValueError(f"Dimensions {dataset.dims} are unrecognizable. "
                             "Please follow the convention of (time, lat, lon) or "
                             "(time, x, y) as dimension size, names and order.")

        return dataset

    @staticmethod
    def get_default_arguments() -> Dict:
        """
        Static method for returning the default arguments, applied either 
        at index configuration or index calculation.

        Returns:
            Dict: Default arguments.
        """

        return {
            "DEFAULT_BBOX": DEFAULT_BBOX,
            "DEFAULT_PERIOD": DEFAULT_PERIOD,
            "DEFAULT_REF_MONTHS_LIST": DEFAULT_REF_MONTHS_LIST,
            "DEFAULT_COVERAGE_TIME_RANGE": DEFAULT_COVERAGE_TIME_RANGE,
            "DEFAULT_REFERENCE_TIME_RANGE": DEFAULT_REFERENCE_TIME_RANGE,
        }

    @ staticmethod
    def get_colormap(cmap: plt.colors.LinearSegmentedColormap = plt.cm.RdBu,
                     vmin: int = -4,
                     vmax: int = 4) -> Dict:
        """
        Static method for returning the default colormap settings, suitable
        for displaying meteorological indices.
        Pass, these into xarray.Dataarray.plot()

        Returns:
            Dict: Valid arguments.

        Examples:
            # plot a dataarray
            >>> dataarray.plot(**Index.get_colormap())

        """

        return {
            'cmap': cmap,
            'vmin': vmin,
            'vmax': vmax
        }


class Spi(Index):
    """
    Class for calculating the Standardized Precipitation Index.

    """

    def __init__(self, dataset: xr.Dataset, config: SpiConfig):
        """
        Initialize index instance.

        Args:
            dataset (xr.Dataset): 3-D dataset of containing precipitation data
                as an xarray.Dataset. Must be daily or monthly measurements.
            config (SpiConfig): Config object for SPI.
                Must be an instance of ddc_indices.config.SpiConfig.

        """

        if config.name != "SPI":
            raise IndexConfigurationError(
                'config must be an instance of SpiConfig')

        try:
            dataset = self.validate_dataset(dataset=dataset)
        except ValueError as err:
            raise DataValidationError('Invalid dataset') from err

        try:
            config.configure(dataset)
        except (ValueError, ValidationError) as err:
            raise IndexConfigurationError(
                'Invalid index configuration') from err

        dataset = self._prepare_dataset(dataset, config)

        self._dataset = dataset.compute()
        self._config = config
        self._index = None
        self._params = None

    def compute(self) -> None:
        """
        Calculate SPI index based in configuration.

        Raises:
            IndexCalculationError: Error while calculating index.
        """
        prec_var_name = self._config.variables.get('prec')

        result_ds = xr.Dataset()
        alpha_ds = xr.Dataset()
        theta_ds = xr.Dataset()

        # Compute SPI for each period
        for period in self._config.periods:
            var_name = f"SPI_{period.value.get('period')}"
            alpha_name = f"alpha_{period.value.get('period')}"
            theta_name = f"theta_{period.value.get('period')}"

            try:
                result, alpha, theta = compute_spi(
                    data_prec=self._dataset[prec_var_name],
                    time_coverage_range=self._config.time_coverage_range.time_range,
                    time_reference_range=self._config.time_reference_range.time_range,
                    period=period,
                    ref_months_list=self._config.ref_months,
                    distribution=self._config.distribution,
                    fitting_params=None)

                print(f"calculated {var_name}")

            except Exception as error:
                raise IndexCalculationError(
                    "Could not calculate index.") from error

            result_ds[var_name] = (result if self._config.index_valid_range is None
                                   else result.clip(
                                       min=self._config.index_valid_range[0],
                                       max=self._config.index_valid_range[1],
                                       keep_attrs=True))
            alpha_ds[alpha_name] = alpha
            theta_ds[theta_name] = theta

            # Append local metadata (i.e. for data variable)
            result_ds[var_name].attrs = self._get_local_metadata(
                period.value.get('period'),
                self._config.distribution.value)

        # Append global metadata (i.e. for dataset)
        result_ds.attrs = self._get_global_metadata(self._config)

        self._index = result_ds
        self._params = {'alpha': alpha_ds, 'theta': theta_ds}

    @staticmethod
    def _prepare_dataset(dataset: xr.Dataset, config: SpiConfig) -> xr.Dataset:
        prec_var_name = config.variables.get('prec')
        if dataset[prec_var_name].min() < 0:
            dataset[prec_var_name] = dataset[prec_var_name].clip(
                min=0.0, max=None, keep_attrs=True)

        if config.bbox.bbox != (
            float(dataset.x.min()), float(dataset.y.min()),
            float(dataset.x.max()), float(dataset.y.max())
        ):

            x_mask = (dataset.x >= config.bbox.minx) & (
                dataset.x <= config.bbox.maxx)
            y_mask = (dataset.y >= config.bbox.miny) & (
                dataset.y <= config.bbox.maxy)
            x_idx = np.where(x_mask)
            y_idx = np.where(y_mask)
            # have to select based of index/position because of upper-left, lower-left indexing
            dataset = dataset.isel(x=x_idx[0], y=y_idx[0])

        # Resample if needed
        if config.periodicity.name == (Periodicity.daily.name and
                                       config.periods[0].value['unit'] == "month"):
            dataset = dataset.resample(time='1MS').sum(
                dim='time', skipna=False).chunk(chunks='auto')
            warnings.warn(
                "periodicity is daily -- resampling data to monthly")
        elif config.periodicity == Periodicity.monthly and config.periods[0].value['unit'] == "day":
            raise IndexCalculationError(
                "Invalid combination of data periodicity and period "
                "-- Can't resample monthly periodicity to daily periods")

        return dataset

    @staticmethod
    def _get_local_metadata(period_name: str,
                            distribution_name: str) -> Dict:
        return {
            "long_name": f"{period_name} Standardized Precipitation Index, "
            f"based on {distribution_name} fitting",
            "standard_name": f"spi_{period_name.lower()}_{distribution_name}",
            "units": "None",
        }

    @staticmethod
    def _get_global_metadata(config: SpiConfig) -> Dict:
        return {
            "Conventions": "CF-1.9",
            "title": "Standardized Precipitation Index",
            "date_created": pd.Timestamp.now().isoformat(),
            "time_coverage_start": str(config.time_coverage_range.start_time),
            "time_coverage_end": str(config.time_coverage_range.end_time),
            "time_reference_start": str(config.time_reference_range.start_time),
            "time_reference_end": str(config.time_reference_range.end_time),
            "bbox": config.bbox.get_bbox_str()
        }

    @property
    def dataset(self) -> xr.Dataset:
        """Get the dataset object for this instance.

        Returns:
            xr.Dataset: The dataset object.
        """
        return self._dataset

    @property
    def config(self) -> SpiConfig:
        """Get the configuration object for this instance.

        Returns:
            SpiConfig: The index configuration object.
        """
        return self._config

    @property
    def index(self) -> xr.Dataset:
        """Get the calculated meteorological index for this instance.

        Returns:
            xr.Dataset: The meteorological index object.
        """
        return self._index

    @property
    def params(self) -> Dict:
        """Get additional results for this instance.

        Returns:
            Dict: Dictionary of additional results.
        """
        return self._params


class Spei(Index):
    """
    Class for calculating the Standardized Precipitation
    Evapotranspiration Index.

    Class method for calculating the Standardized Precipitation
    Evapotranspiration Index.
    PET values are subtracted from the precipitation values to
    come up with an array of (P - PET) values, which is then
    transformed similarly as SPI.

    Data fetched from DDC, it is advised to calculate the PET values first.
    The program will estimate the evapotranspiration using
    the Hargreaves equation. More information at:
    ddc_met_indices.eto.eto_hargreaves
    """

    def __init__(self, dataset: xr.Dataset, config: SpeiConfig):
        """
        Initialize index instance.

        Args:
            dataset (xr.Dataset): 3-D dataset of containing precipitation 
                and evapotranspiration data as an xarray.Dataset.
                Must be daily or monthly measurements.
            config (SpeiConfig): Config object for SPEI.
                Must be an instance of ddc_indices.config.SpeiConfig.
        """

        if config.name != "SPEI":
            raise IndexConfigurationError(
                'config must be an instance of SpeiConfig')

        try:
            dataset = self.validate_dataset(dataset=dataset)
        except ValueError as err:
            raise DataValidationError('Invalid dataset') from err

        try:
            config.configure(dataset)
        except (ValueError, ValidationError) as err:
            raise IndexConfigurationError(
                'Invalid index configuration') from err

        dataset = self._prepare_dataset(dataset, config)

        if not config.variables.get('eto'):
            dataset = self._estimate_eto(dataset, config)
            config.variables['eto'] = 'eto'

        self._dataset = dataset.compute()
        self._config = config
        self._index = None
        self._params = None

    def compute(self):
        """
        Calculate SPEI index based in configuration.

        Raises:
            IndexCalculationError: Error while calculating index.
        """
        prec_var_name = self._config.variables.get('prec')
        eto_var_name = self._config.variables.get('eto')

        result_ds = xr.Dataset()
        alpha_ds = xr.Dataset()
        theta_ds = xr.Dataset()

        # Compute SPEI for each period
        for period in self._config.periods:
            var_name = f"SPEI_{period.value.get('period')}"
            alpha_name = f"alpha_{period.value.get('period')}"
            theta_name = f"theta_{period.value.get('period')}"

            try:
                result, alpha, theta = compute_spei(
                    data_prec=self._dataset[prec_var_name],
                    data_pet=self._dataset[eto_var_name],
                    time_coverage_range=self._config.time_coverage_range.time_range,
                    time_reference_range=self._config.time_reference_range.time_range,
                    period=period,
                    ref_months_list=self._config.ref_months,
                    distribution=self._config.distribution,
                    fitting_params=None)

                print(f"calculated {var_name}")

            except Exception as error:
                raise IndexCalculationError(
                    "Could not calculate index.") from error

            result_ds[var_name] = (result if self._config.index_valid_range is None
                                   else result.clip(
                                       min=self._config.index_valid_range[0],
                                       max=self._config.index_valid_range[1],
                                       keep_attrs=True))
            alpha_ds[alpha_name] = alpha
            theta_ds[theta_name] = theta

            # Append local metadata (i.e. for data variable)
            result_ds[var_name].attrs = self._get_local_metadata(
                period.value.get('period'),
                self._config.distribution.value)

        # Append global metadata (i.e. for dataset)
        result_ds.attrs = self._get_global_metadata(self._config)

        self._index = result_ds
        self._params = {'alpha': alpha_ds, 'theta': theta_ds}

    @staticmethod
    def _estimate_eto(dataset: xr.Dataset, config: SpeiConfig):
        """
        Estimate potential evapotranspiration over grass (ETo) using
        the Hargreaves equation. Based on equation 52 in Allen et al (1998).
        Result is attributed to self.dataset['eto'] variable.
        """
        try:
            temp_var_name = {'min': config.variables['temp_min'],
                             'max': config.variables['temp_max'],
                             'mean': config.variables.get('temp_mean')}
        except KeyError as err:
            raise ValueError('Min and/or max temperature variables '
                             'not found -- To estimate '
                             'evapotranspiration, dataset must'
                             'contain minimum and maximum temperature') from err
        try:
            dataset['eto'] = eto_hargreaves(dataset, temp_var_name)
            return dataset

        except ValueError as error:
            raise IndexCalculationError(
                "Couldn't calculate evapotranspiration") from error

    @staticmethod
    def _prepare_dataset(dataset: xr.Dataset, config: SpeiConfig) -> xr.Dataset:
        prec_var_name = config.variables.get('prec')
        eto_var_name = config.variables.get('eto')
        if dataset[prec_var_name].min() < 0:
            dataset[prec_var_name] = dataset[prec_var_name].clip(
                min=0.0, max=None, keep_attrs=True)

        if eto_var_name in dataset.variables:
            if dataset[eto_var_name].min() < 0:
                dataset[eto_var_name] = dataset[eto_var_name].clip(
                    min=0.0, max=None, keep_attrs=True)

        if config.bbox.bbox != (
            float(dataset.x.min()), float(dataset.y.min()),
            float(dataset.x.max()), float(dataset.y.max())
        ):

            x_mask = (dataset.x >= config.bbox.minx) & (
                dataset.x <= config.bbox.maxx)
            y_mask = (dataset.y >= config.bbox.miny) & (
                dataset.y <= config.bbox.maxy)
            x_idx = np.where(x_mask)
            y_idx = np.where(y_mask)
            # have to select based of index/position because of upper-left, lower-left indexing
            dataset = dataset.isel(x=x_idx[0], y=y_idx[0])

        # Resample if needed
        if config.periodicity.name == (Periodicity.daily.name and
                                       config.periods[0].value['unit'] == "month"):
            dataset = dataset.resample(time='1MS').sum(
                dim='time', skipna=False).chunk(chunks='auto')
            warnings.warn(
                "periodicity is daily -- resampling data to monthly")
        elif config.periodicity == Periodicity.monthly and config.periods[0].value['unit'] == "day":
            raise IndexCalculationError(
                "Invalid combination of data periodicity and period "
                "-- Can't resample monthly periodicity to daily periods")

        return dataset

    @staticmethod
    def _get_local_metadata(period_name: str,
                            distribution_name: str) -> Dict:
        return {
            "long_name": f"{period_name} Standardized Precipitation Evapotranspiration Index, "
            f"based on {distribution_name} fitting",
            "standard_name": f"spei_{period_name.lower()}_{distribution_name}",
            "units": "None",
        }

    @staticmethod
    def _get_global_metadata(config: SpeiConfig) -> Dict:
        return {
            "Conventions": "CF-1.9",
            "title": "Standardized Precipitation Evapotranspiration Index",
            "date_created": pd.Timestamp.now().isoformat(),
            "time_coverage_start": str(config.time_coverage_range.start_time),
            "time_coverage_end": str(config.time_coverage_range.end_time),
            "time_reference_start": str(config.time_reference_range.start_time),
            "time_reference_end": str(config.time_reference_range.end_time),
            "bbox": config.bbox.get_bbox_str()
        }

    @property
    def dataset(self) -> xr.Dataset:
        """Get the dataset object for this instance.

        Returns:
            xr.Dataset: The dataset object.
        """
        return self._dataset

    @property
    def config(self) -> SpiConfig:
        """Get the configuration object for this instance.

        Returns:
            SpiConfig: The index configuration object.
        """
        return self._config

    @property
    def index(self) -> xr.Dataset:
        """Get the calculated meteorological index for this instance.

        Returns:
            xr.Dataset: The meteorological index object.
        """
        return self._index

    @property
    def params(self) -> Dict:
        """Get additional results for this instance.

        Returns:
            Dict: Dictionary of additional results.
        """
        return self._params


class Pni(Index):

    """
    Class for calculating the Percent of Normal Index.
    """

    def __init__(self, dataset: xr.Dataset, config: PniConfig):
        """
        Initialize index instance.

        Args:
            dataset (xr.Dataset): 3-D dataset of containing precipitation data
                as an xarray.Dataset. Must be daily or monthly measurements.
            config (PniConfig): Config object for PNI.
                Must be an instance of ddc_indices.config.PniConfig.

        """

        if config.name != "PNI":
            raise IndexConfigurationError(
                'config must be an instance of PniConfig')

        try:
            dataset = self.validate_dataset(dataset=dataset)
        except ValueError as err:
            raise DataValidationError('Invalid dataset') from err

        try:
            config.configure(dataset)
        except (ValueError, ValidationError) as err:
            raise IndexConfigurationError(
                'Invalid index configuration') from err

        dataset = self._prepare_dataset(dataset, config)

        self._dataset = dataset.compute()
        self._config = config
        self._index = None
        self._params = None

    def compute(self):
        """
        Calculate PNI index based in configuration.

        Raises:
            IndexCalculationError: Error while calculating index.
        """

        prec_var_name = self._config.variables.get('prec')

        result_ds = xr.Dataset()

        # Compute PNI for each period
        for period in self._config.periods:
            var_name = f"PNI_{period.value.get('period')}"

            try:
                result = compute_pni(
                    data_prec=self._dataset[prec_var_name],
                    time_coverage_range=self._config.time_coverage_range.time_range,
                    time_reference_range=self._config.time_reference_range.time_range,
                    period=period,
                    ref_months_list=self._config.ref_months)

                print(f"calculated {var_name}")

            except Exception as error:
                raise IndexCalculationError(
                    "Could not calculate index.") from error

            result_ds[var_name] = (result if self._config.index_valid_range is None
                                   else result.clip(
                                       min=self._config.index_valid_range[0],
                                       max=self._config.index_valid_range[1],
                                       keep_attrs=True))

            # Append local metadata (i.e. for data variable)
            result_ds[var_name].attrs = self._get_local_metadata(
                period.value.get('period'))

        # Append global metadata (i.e. for dataset)
        result_ds.attrs = self._get_global_metadata(self._config)

        self._index = result_ds

    @staticmethod
    def _prepare_dataset(dataset: xr.Dataset, config: SpiConfig) -> xr.Dataset:
        prec_var_name = config.variables.get('prec')
        if dataset[prec_var_name].min() < 0:
            dataset[prec_var_name] = dataset[prec_var_name].clip(
                min=0.0, max=None, keep_attrs=True)

        if config.bbox.bbox != (
            float(dataset.x.min()), float(dataset.y.min()),
            float(dataset.x.max()), float(dataset.y.max())
        ):

            x_mask = (dataset.x >= config.bbox.minx) & (
                dataset.x <= config.bbox.maxx)
            y_mask = (dataset.y >= config.bbox.miny) & (
                dataset.y <= config.bbox.maxy)
            x_idx = np.where(x_mask)
            y_idx = np.where(y_mask)
            # have to select based of index/position because of upper-left, lower-left indexing
            dataset = dataset.isel(x=x_idx[0], y=y_idx[0])

        # Resample if needed
        if config.periodicity.name == (Periodicity.daily.name and
                                       config.periods[0].value['unit'] == "month"):
            dataset = dataset.resample(time='1MS').sum(
                dim='time', skipna=False).chunk(chunks='auto')
            warnings.warn(
                "periodicity is daily -- resampling data to monthly")
        elif config.periodicity == Periodicity.monthly and config.periods[0].value['unit'] == "day":
            raise IndexCalculationError(
                "Invalid combination of data periodicity and period "
                "-- Can't resample monthly periodicity to daily periods")

        return dataset

    @staticmethod
    def _get_local_metadata(period_name: str) -> Dict:
        return {
            "long_name": f"{period_name} Percent of Normal Index",
            "standard_name": f"pni_{period_name.lower()}",
            "units": "None",
        }

    @staticmethod
    def _get_global_metadata(config: PniConfig) -> Dict:
        return {
            "Conventions": "CF-1.9",
            "title": "Percent of Normal Index",
            "date_created": pd.Timestamp.now().isoformat(),
            "time_coverage_start": str(config.time_coverage_range.start_time),
            "time_coverage_end": str(config.time_coverage_range.end_time),
            "time_reference_start": str(config.time_reference_range.start_time),
            "time_reference_end": str(config.time_reference_range.end_time),
            "bbox": config.bbox.get_bbox_str()
        }

    @property
    def dataset(self) -> xr.Dataset:
        """Get the dataset object for this instance.

        Returns:
            xr.Dataset: The dataset object.
        """
        return self._dataset

    @property
    def config(self) -> SpiConfig:
        """Get the configuration object for this instance.

        Returns:
            SpiConfig: The index configuration object.
        """
        return self._config

    @property
    def index(self) -> xr.Dataset:
        """Get the calculated meteorological index for this instance.

        Returns:
            xr.Dataset: The meteorological index object.
        """
        return self._index


class Pdsi(Index):
    """
    Class for calculating the Palmer Drought Severity Index.

    """

    def __init__(self, dataset: xr.Dataset, config: PdsiConfig):
        """
        Initialize index instance.

        Args:
            dataset (xr.Dataset): 3-D dataset of containing precipitation data
                as an xarray.Dataset. Must be daily or monthly measurements.
            config (PdsiConfig): Config object for PDSI.
                Must be an instance of ddc_indices.config.PdsiConfig.

        """
        raise NotImplementedError('PDSI is not available yet.')

    def compute(self):
        pass
