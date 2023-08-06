"""Base package for Cypress Creek Renewables Utilities
"""

__version__ = "0.2.0"

from collections import namedtuple
from datetime import (
    date,
    datetime
)
import numpy as np
import pandas as pd
from pandas.core.indexes.base import Index

# Custom type definitions
DateLike = datetime|date
ListLike = list|set|Index
SeriesLike = np.ndarray|pd.Series
Numeric = int|float

# Custom data structures
DaylightParams = namedtuple('DaylightParams', ['lat', 'lon', 'tz'])
ProjectModelParams = namedtuple('ProjectModelParams', ['project_name', 'ccr_id', 'folder', 'tz', 'lat', 'lon',
                                             'elevation', 'mwdc', 'racking', 'tilt_gcr', 'max_angle',
                                             'temp_coef', 'a_module', 'b_module', 'delta_tcnd'])

from ccrenew import (
    ccr,
    data_determination
)

# Custom exceptions
class AWSError(Exception):
    pass
class FileNotFoundError(Exception):
    pass
class FileOpenError(Exception):
    pass


print('Pulling df_keys from Smartsheets...')
all_df_keys = ccr.get_df_keys(retired=True)