from __future__ import annotations
import base64
from collections.abc import Callable
from io import BytesIO
import functools
from matplotlib import pyplot as plt
from numbers import Number
import pandas as pd
from pvlib.location import Location
import numpy as np
from scipy.interpolate import CubicSpline
from scipy import stats
from scipy.signal import find_peaks
from statistics import geometric_mean
from typing import (
    TYPE_CHECKING,
    TypedDict
)
from typing_extensions import Unpack

if TYPE_CHECKING:
    from ccrenew.pvmodel import ProjectModel

class SensorData(TypedDict):
    df: pd.DataFrame
    pv_model: ProjectModel

def daylight(func:Callable):
    @functools.wraps(func)
    def calc_daylight_hours(**kwargs: Unpack[SensorData]):
        # Collect df & project to determine daylight hours
        df = kwargs.get('df')
        pv_model = kwargs.get('pv_model')
        project_location = pv_model.location

        # Calculate daylight hours
        tz = project_location.tz
        times = df.index.tz_localize(tz, nonexistent='shift_backward', ambiguous='NaT') # type: ignore
        df_suntimes = project_location.get_sun_rise_set_transit(times, method='spa')[['sunrise', 'sunset']]
        df_suntimes.index = pd.DatetimeIndex(df_suntimes.index)
        df = df.loc[df_suntimes.query("index.dt.hour >= sunrise.dt.hour and index.dt.hour <= sunset.dt.hour+1").index.tz_localize(None)] # type: ignore
        kwargs['df'] = df

        # Pass df with only daylight hours to the function
        result = func(**kwargs)

        return result

    return calc_daylight_hours

def comms(df:pd.DataFrame)-> pd.DataFrame:
    return df.isnull()

def zeroes(df:pd.DataFrame) -> pd.DataFrame:
    return df == 0

@daylight
def daylight_zeroes(*, df:pd.DataFrame, pv_model:ProjectModel) -> pd.DataFrame:
    """
    Return zero values during daylight hours.

    Args:
        df (pd.DataFrame): Dataframe of project readings.
        pv_model (ProjectModel): [PV model][ccrenew.pv_model.ProjectModel] for the project built on the pvlib package.

    Returns:
        pd.DataFrame A set of bool values based on zeroes.
    """
    return zeroes(df)

def frozen(df:pd.DataFrame, window:str|int|None = None) -> pd.DataFrame:
    """ 'cutoff_limit' is minimum amount of time values must be unchanged to be considered frozen. 
    This parameters can be provided in the ContractParameters class in the config script. 
    The default is to use the minimum timedelta found in the DAS data."""
    if not window:
        return (df != 0) & (df.diff() == 0)
    if isinstance(window, str):
        df_freq = pd.infer_freq(df.index) # type: ignore
        window_range = 2*pd.Timedelta(window) - pd.Timedelta(df_freq) # type: ignore
        window_range = window_range/df_freq # type: ignore
    elif isinstance(window, Number):
        window_range = window
    else:
        raise TypeError('cutoff_limit for frozen values must be a number representing window size or a string in format ##min')
    
    lookback = df.rolling(window=window_range).apply(lambda x: np.all(x==x[0]), raw=True)
    forward_indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=window_range)
    lookforward = df.rolling(window=forward_indexer).apply(lambda x: np.all(x==x[0]), raw=True)
    frozen = lookback.fillna(0) + lookforward.fillna(0)

    return frozen > 0

def frozen_center(df:pd.DataFrame, window:str|int|None = None) -> pd.DataFrame:
    """ 'cutoff_limit' is minimum amount of time values must be unchanged to be considered frozen. 
    This parameters can be provided in the ContractParameters class in the config script. 
    The default is to use the minimum timedelta found in the DAS data.  """
    if not window:
        return (df != 0) & (df.diff() == 0)
    if isinstance(window, str):
        df_freq = pd.infer_freq(df.index) # type: ignore
        window_range = 2*pd.Timedelta(window) - pd.Timedelta(df_freq) # type: ignore
    elif isinstance(window, Number):
        window_range = window
    else:
        raise TypeError('cutoff_limit for frozen values must be a number representing window size or a string in format ##min')

    frozen = df.rolling(window_range, center=True).apply(lambda x: np.all(x == x[0]), raw=True) # type: ignore

    return frozen == 1

@daylight
def daylight_frozen(*, df:pd.DataFrame, pv_model:ProjectModel, window:str|int|None = None) -> pd.DataFrame:
    return frozen(df, window)

def negatives(df:pd.DataFrame, cols:list=[]) -> pd.DataFrame:
    df = df.copy()
    if cols:
        df = df[cols] < 0
    else:
        df = df <0
    return df

def decreasing(df:pd.DataFrame) -> pd.DataFrame:
    return df.diff() < 0

def band_pass(df:pd.DataFrame, col_limits:list[tuple]) -> pd.DataFrame:
    df=df.copy()
    for col, limits in col_limits:
        df.loc[:,col] = (df[col].lt(limits[0])) | (df[col].gt(limits[1]))

    return df

@daylight
def daylight_poa_mistracking(*, df:pd.DataFrame, pv_model:ProjectModel, add_sparklines:bool = False, degree:int = 8):
    return poa_mistracking(df, add_sparklines, degree)

def poa_mistracking(df: pd.DataFrame, add_sparklines:bool = False, degree: int=8) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.copy()
    poa_cols = [col for col in df.columns if 'Solcast' not in col]

    # Create columns for data sub stats by day
    linreg_rval_poa = [col + ' rPOA' for col in poa_cols]
    linreg_slope_poa = [col + ' mPOA' for col in poa_cols]
    linreg_rval_ghi = [col + ' rGHI' for col in poa_cols]
    linreg_slope_ghi = [col + ' mGHI' for col in poa_cols]
    days = df.resample('D').first().index # type: ignore
    datasub_stats = pd.DataFrame(index=days, columns=linreg_rval_poa+linreg_slope_poa+linreg_rval_ghi+linreg_slope_ghi)
            
    if add_sparklines:
        pd.set_option('display.max_colwidth', -1)
        pd.set_option('display.max_seq_items', -1)

        sparkline_cols = [col + ' Data' for col in poa_cols]
        datasub_stats = datasub_stats.reindex(columns=list(datasub_stats.columns)+sparkline_cols)

    for day, df_daily in df.groupby(df.index.date): # type: ignore
        x = df_daily.index.hour

        # Find peaks for Solcast data
        y_solcast_raw = df_daily['Solcast POA']
        y_solcast = y_solcast_raw.fillna(0)
        fit_solcast = np.poly1d(np.polyfit(x, y_solcast, degree))

        x_fit = np.linspace(x[0], x[-1], 100)
        y_fit_solcast = fit_solcast(x_fit)

        # Count the number of hours that are above half the maximum value for the series
        # Trackers will have more hours above this value than non-trackers
        count_max_50_solcast = (y_solcast>y_solcast_raw.max()/2).sum()
        max_66_solcast = y_solcast_raw.max()*2/3

        # Only consider peaks that are at least 2/3rds as high as the maximum
        peaks_solcast, _ = find_peaks(y_fit_solcast, height=max_66_solcast)
        peak_count_solcast = len(peaks_solcast)

        # Loop through POA columns to find peaks
        for col in poa_cols:
            solcast_poa = df_daily['Solcast POA']
            solcast_ghi = df_daily['Solcast GHI']
            y_raw = df_daily[col]
            y = y_raw.fillna(0)
            fit = np.poly1d(np.polyfit(x, y, degree))

            x_fit = np.linspace(x[0], x[-1], 100)
            y_fit = fit(x_fit)

            # Calculate % of max values for use in calculations
            count_max_50 = (y_raw>y_raw.max()/2).sum()
            max_66 = y_raw.max()*2/3

            # Only consider peaks that are at least 2/3rds as high as the maximum
            peaks, _ = find_peaks(y_fit, height=max_66)
            peak_count = len(peaks)

            # If only 1 peak & Solcast shows more than 1, we'll consider it mistracking
            # If the number of points above 50% max for Solcast vs Native is 2 or more, we'll consider it mistracking
            if peak_count < 2 and peak_count_solcast >= 2:
                df.loc[df.index.date==day, col] = True # type: ignore
            elif count_max_50_solcast - count_max_50 > 1:
                df.loc[df.index.date==day, col] = True # type: ignore
            else:
                df.loc[df.index.date==day, col] = False # type: ignore
            
            # Linear Regression
            # Remove any nans
            nans_poa = solcast_poa[solcast_poa.isna()].index
            nans_poa = nans_poa.union(y_raw[y_raw.isna()].index)
            nans_ghi = solcast_ghi[solcast_ghi.isna()].index
            nans_ghi = nans_ghi.union(y_raw[y_raw.isna()].index)
            solcast_poa = solcast_poa.drop(nans_poa)
            solcast_ghi = solcast_ghi.drop(nans_ghi)
            y_poa = y_raw.drop(nans_poa)
            y_ghi = y_raw.drop(nans_ghi)

            # Calculate regression coefficients
            try:
                linreg_poa = stats.linregress(solcast_poa, y_poa)
                poa_rvalue = linreg_poa.rvalue # type: ignore
                poa_slope = linreg_poa.slope # type: ignore
            except:
                poa_rvalue = 0
                poa_slope = 0
            
            try:
                linreg_ghi = stats.linregress(solcast_ghi, y_ghi)
                ghi_rvalue = linreg_ghi.rvalue # type: ignore
                ghi_slope = linreg_ghi.slope # type: ignore
            except:
                ghi_rvalue = 0
                ghi_slope = 0

            # Populate regression results for the day
            day_str = day.strftime('%Y%m%d')
            update_cols = [c for c in datasub_stats.columns if col in c and 'Data' not in c]
            datasub_stats.loc[day_str, update_cols] = (poa_rvalue, # type: ignore
                                                       poa_slope,  # type: ignore
                                                       ghi_rvalue, # type: ignore
                                                       ghi_slope)  # type: ignore
            
            if add_sparklines:
                pd.set_option('display.max_colwidth', -1)
                pd.set_option('display.max_seq_items', -1)

                def sparkline(solcast, poa, figsize=(4, 2), **kwargs):
                    x = range(len(solcast))
                    fig, ax = plt.subplots(figsize=figsize, **kwargs)
                    ax.plot(x, poa)
                    ax.plot(x, solcast, linestyle='dashed')

                    for k,v in ax.spines.items():
                        v.set_visible(False)
                    ax.set_xticks([])
                    ax.set_yticks([])    
                    
                    img = BytesIO()
                    plt.savefig(img)
                    img.seek(0)
                    plt.close()
                    return '<img src="data:image/png;base64,{}"/>'.format(base64.b64encode(img.read()).decode())
                
                # map the sparkline function over the data column
                # and store back in the column sparklines
                # df[col+' Data'] = df[['Solcast POA', col]].apply(tuple, axis=1).map(sparkline)
                datasub_stats.loc[day_str, col+' Data'] = sparkline(solcast_poa, y_poa)

                # _repr_html_ escapes HTML so manually handle the rendering
                # HTML(spark.to_html(escape=False))

    # Drop Solcast columns
    df = df.filter(regex='^(?!.*Solcast).*$', axis=1).astype(bool)

    return df, datasub_stats

def spline_filter(df:pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df_bool = ~df.isna()
    for col in df.columns:
        non_nulls = df[col][df[col].notna()]
        x = non_nulls.index.values.astype('float')
        y = non_nulls.values
        cs = CubicSpline(x, y)
        deriv = cs(x, 1)
        deriv_mean = np.mean(deriv)
        stdev = np.std(deriv)
        y = (deriv < -2.5*stdev) | (deriv > 2.5*stdev)
        bool_col = pd.DataFrame(index=pd.to_datetime(x), data={col: y})
        df_bool.update(bool_col)
    df_bool = df_bool.astype(bool)

    return df_bool


if __name__ == '__main__':
    dates = pd.date_range('2023-1-1 00:00', '2023-6-1 00:00', freq='5T')
    values = list(range(len(dates)))

    data = np.array([values, values, values, values, values]).T
    df = pd.DataFrame(index=dates, data=data)
    df.loc[df.index < '2023-01-01 00:10'] = 1
    df.loc[(df.index > '2023-01-01 00:20') & (df.index < '2023-01-01 01:00')] = 1
    df.loc[(df.index > '2023-01-01 01:10') & (df.index < '2023-01-01 01:40')] = -1
    s = df.iloc[:,[0]]
    frozen(s, '15T')