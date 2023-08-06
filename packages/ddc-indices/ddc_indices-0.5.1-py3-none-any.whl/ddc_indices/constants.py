
from enum import Enum
import pandas as pd


FITTED_INDEX_VALID_MIN = -3.09

FITTED_INDEX_VALID_MAX = 3.09

DEFAULT_BBOX = (15.0, 44.0, 24.0, 50.0)

DEFAULT_PERIOD = ["MS3"]

DEFAULT_REF_MONTHS_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

VALID_REF_MONTHS_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

DEFAULT_COVERAGE_TIME_RANGE = ('1971-01-01',
                               pd.Timestamp.today().strftime("%Y-%m-%d"))
DEFAULT_REFERENCE_TIME_RANGE = ('1971-01-01', '2000-12-31')

DEFAULT_CRS = "EPSG:4326"

CRS_ID_TO_URI = {
    "EPSG:4326": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "WGS84": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "http://www.opengis.net/def/crs/EPSG/0/4326": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "EPSG:3857": "https://www.opengis.net/def/crs/EPSG/0/3857",
    "https://www.opengis.net/def/crs/EPSG/0/3857": "https://www.opengis.net/def/crs/EPSG/0/3857",
    "EPSG:23700": "https://www.opengis.net/def/crs/EPSG/0/23700",
    "EOV": "https://www.opengis.net/def/crs/EPSG/0/23700",
    "https://www.opengis.net/def/crs/EPSG/0/23700": "https://www.opengis.net/def/crs/EPSG/0/23700",
}

class Periodicity(Enum):
    """
    Enumeration type for specifying dataset periodicity,
    "monthly" indicates an array of monthly values,
    "daily" indicates an array of daily values.
    """
    daily = {"name": "daily",
             "frequency": "D"}
    monthly = {"name": "monthly",
               "frequency": "M"}


class Distribution(Enum):
    """
    Enumeration type for distribution fittings used for SPI and SPEI.
    """
    GAMMA = 'gamma'
    PEARSON = 'pearson'


class SpiPeriods(Enum):
    """
    Enumeration type for SPI time periods.
    """

    MS1 = {"period": "1MS",
           "value": 1,
           "unit": "month"}

    MS2 = {"period": "2MS",
           "value": 2,
           "unit": "month"}

    MS3 = {"period": "3MS",
           "value": 3,
           "unit": "month"}

    MS6 = {"period": "6MS",
           "value": 6,
           "unit": "month"}

    MS9 = {"period": "9MS",
           "value": 9,
           "unit": "month"}

    MS12 = {"period": "12MS",
            "value": 12,
            "unit": "month"}

    MS24 = {"period": "24MS",
            "value": 24,
            "unit": "month"}


class SpeiPeriods(Enum):
    """
    Enumeration type for SPEI time periods.
    """

    MS1 = {"period": "1MS",
           "value": 1,
           "unit": "month"}

    MS2 = {"period": "2MS",
           "value": 2,
           "unit": "month"}

    MS3 = {"period": "3MS",
           "value": 3,
           "unit": "month"}

    MS6 = {"period": "6MS",
           "value": 6,
           "unit": "month"}

    MS9 = {"period": "9MS",
           "value": 9,
           "unit": "month"}

    MS12 = {"period": "12MS",
            "value": 12,
            "unit": "month"}

    MS24 = {"period": "24MS",
            "value": 24,
            "unit": "month"}


class PniPeriods(Enum):
    """
    Enumeration type for PNI time periods.
    """

    D30 = {"period": "30D",
           "value": 30,
           "unit": "day"}

    D60 = {"period": "60D",
           "value": 60,
           "unit": "day"}

    MS1 = {"period": "1MS",
           "value": 1,
           "unit": "month"}

    MS2 = {"period": "2MS",
           "value": 2,
           "unit": "month"}

    MS3 = {"period": "3MS",
           "value": 3,
           "unit": "month"}

    MS6 = {"period": "6MS",
           "value": 6,
           "unit": "month"}

    MS9 = {"period": "9MS",
           "value": 9,
           "unit": "month"}

    MS12 = {"period": "12MS",
            "value": 12,
            "unit": "month"}

    MS24 = {"period": "24MS",
            "value": 24,
            "unit": "month"}
