# DDC Meteorological Indices

This is the Danube Data Cube Meteorological Indices library, 
a python implementation for calculating common meteorological indices,
utilizing data cubes.

The following indices are available:
- SPI, Standardized Precipitation Index, utilizing both gamma and Pearson Type III distributions
- SPEI, Standardized Precipitation Evapotranspiration Index, utilizing both gamma and Pearson Type III distributions
- PDSI, Palmer Drought Severity Index
- PNI, Percentage of Normal Precipitation Index

### Installation
```
$ pip install ddc-indices
```

### Example
```
$ python

# Calculating the Standardized Precipitation Index (SPI)
>>> import xarray as xr
>>> from ddc_indices import DdcIndices
>>> from ddc_indices import SpiConfig

# import my dataset containing precipitation data
>>> dataset = xr.open_zarr('path_to_zarr')
>>> config = SpiConfig(variables={'prec': 'prec'}, periodicity='daily')
>>> spi = DdcIndices().initialize(dataset, config)
>>> spi.compute()
>>> spi.index

```
