

SPI_METADATA = {
    "name": "SPI",
    "long_name": "Standardized Precipitation Index",
    "description":"The Standardized Precipitation Index (SPI) is a widely used "
                  "index to characterize meteorological drought on a range of "
                  "timescales. It quantifies observed precipitation as a "
                  "standardized departure from a selected probability "
                  "distribution function that models the raw precipitation data. "
                  "The raw precipitation data are typically fitted to a gamma or "
                  "a Pearson Type III distribution, and then transformed to a "
                  "normal distribution. The SPI values can be interpreted as the "
                  "number of standard deviations by which the observed anomaly "
                  "deviates from the long-term mean. "
                  "(https://climatedataguide.ucar.edu/climate-data/"
                  "standardized-precipitation-index-spi)"
}

SPEI_METADATA = {
    "name": "SPEI",
    "long_name": "Standardized Precipitation Evapotranspiration Index",
    "description": "The Standardized Precipitation Evapotranspiration Index (SPEI) "
                   "is an extension of the widely used Standardized Precipitation Index (SPI). "
                   "The SPEI is designed to take into account both precipitation "
                   "and potential evapotranspiration. " 
                   "(https://climatedataguide.ucar.edu/climate-data/"
                   "standardized-precipitation-evapotranspiration-index-spei)"

}

PNI_METADATA = {
    "name": "PNI",
    "long_name": "Percent of Normal Index",
    "description": ""

}

PDSI_METADATA = {
    "name": "PDSI",
    "long_name": "Palmer Drought Severity Index",
    "description": "The Palmer Drought Severity Index (PDSI) uses readily "
                   "available temperature and precipitation data to estimate "
                   "relative dryness. It is a standardized index that generally "
                   "spans -10 (dry) to +10 (wet). Maps of operational agencies "
                   "like NOAA typically show a range of -4 to +4, but more "
                   "extreme values are possible. The PDSI has been reasonably "
                   "successful at quantifying long-term drought. "
                   "As it uses temperature data and a physical water balance model, "
                   "it can capture the basic effect of global warming on drought "
                   "through changes in potential evapotranspiration. "
                   "Monthly PDSI values do not capture droughts on time scales "
                   "less than about 12 months; more pros and cons are discussed "
                   "in the Expert Guidance. (https://climatedataguide.ucar.edu/"
                   "climate-data/palmer-drought-severity-index-pdsi)"

}

DDC_INDICES_METADATA = {
    "SPI": SPI_METADATA,
    "SPEI": SPEI_METADATA,
    "PNI": PNI_METADATA,
    "PDSI": PDSI_METADATA}
