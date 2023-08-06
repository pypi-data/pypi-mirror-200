# -*- coding: utf-8 -*-
"""
Module to store and process data related to CCRenew solar projects.
"""
from __future__ import annotations

import boto3
from datetime import datetime
from dateutil.parser import parse
import io
from IPython.display import HTML
import itertools
import logging
import logging.config
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from pathlib import Path
import pickle
import s3fs
import scipy.stats as sct
import shutil
from sqlalchemy import (
    delete,
    MetaData,
    Table
)
from sqlalchemy.sql import extract
import sys
from typing import Iterable, Union
import xlsxwriter
import xlsxwriter.utility

from ccrenew import (
    __version__,
    ccr,
    DateLike,
    Numeric,
    FileNotFoundError,
    FileOpenError
)
from ccrenew.dashboard import (
    Colmap,
    S3FilePath,
    func_timer,
    get_modified_time,
    make_s3_filepath,
    Plotter
)

import ccrenew.data_determination as det

import ccrenew.dashboard.data_processing.BV_pp_deg as batt
import ccrenew.dashboard.data_processing.Correct_POI_data_v01 as poi
import ccrenew.dashboard.data_processing.Correct_Meter_data_v08_smartercheck as meter_correct
import ccrenew.dashboard.data_processing.Performance_Guarantees_v01 as perf
import ccrenew.dashboard.data_processing.Plant_Availability_v16_bbsc as plant_ava
import ccrenew.dashboard.data_processing.Rate_Structure_Python_with_DST_v07 as rates
import ccrenew.dashboard.data_processing.snow_loss_functions_v3 as snow
import ccrenew.dashboard.data_processing.Table_by_Rate_Schedule_v01 as rate_table
import ccrenew.dashboard.data_processing.weather_adjusted_functions_v03 as weather

import ccrenew.dashboard.utils.dashboard_utils as utils
import ccrenew.dashboard.utils.df_tools as df_tools
import ccrenew.dashboard.utils.project_neighbors as neighbs

from ccrenew.pvmodel.project_model import ProjectModel


# Create boto s3 client
s3_client = boto3.client('s3')

# suppress warnings about "A value is trying to be set on a copy of a slice from a DataFrame."
pd.set_option('mode.chained_assignment', None)

# Create logger
# logger = logging.getLogger(__name__)
# logger = logging.getLogger(__name__)


class PowertrackFileException(Exception):
    pass

class Project:
    """An object representing a project (i.e. site). This should never be initialized\
        outside of a [DashboardSession][ccrenew.dashboard.session.DashboardSession] instance,
        which coordinates the processing of [proj_init_dict][ccrenew.dashboard.project.Project.proj_init_dict].

    Args:
        proj_init_dict (dict): A dictionary of metadata to pass to the `Project` for initialization.
    """
    
    # Initialize class variables
    Gstc:int = 1000
    report_type_map = {'monthly': 'Monthly', 'ul': 'UL Monthly', 'weekly': 'Weekly'}

    def __init__(self, proj_init_dict:dict):

        # Initialize Project name
        self.project_name = proj_init_dict['project_name']

        # Store the version for checking when loading a pickle
        self.__version__ = __version__

        # Processed flag that we'll turn to true once we process the data
        self.processed = False

        # Errored flag that will warn us when a project has encountered an error in processing
        self.errored = False

        # Error info for a project that encounters an error
        self.error_info = proj_init_dict.get('error_info', dict())
        if self.error_info:
            print(f"{self.project_name} Errored. Error details: {self.error_info}")
            self.errored = True
            return

        # List to note neighbor sensors once we've added them
        self.config_neighbor_sensors = set()
        
        # Project properties passed from DashboardSession
        self.df_proj_keys = proj_init_dict['df_proj_keys']
        self.df_proj_ss_comments = proj_init_dict['df_proj_ss_comments']
        self.dashboard_dir = proj_init_dict['dashboard_dir']
        self.data_cutoff_date = proj_init_dict['data_cutoff_date']
        self.data_platform = proj_init_dict['data_platform']
        self.data_platform_dirs = proj_init_dict['data_platform_dirs']
        self.data_source = proj_init_dict['data_source']
        self.report_type = proj_init_dict['report_type']
        self.Battery_AC_site = proj_init_dict['Battery_AC_site']
        self.Battery_DC_site = proj_init_dict['Battery_DC_site']
        self.Tracker_site = proj_init_dict['Tracker_site']
        self.raw_snow_df = proj_init_dict['raw_snow_df']
        self.snow_file = proj_init_dict['snow_file']
        self.neighbor_list = proj_init_dict['neighbor_list']

        # Project year based on `data_source`
        self.year = int(self.data_source.split('_')[0])

        # Get information for the project from DF keys
        # `self.df_proj_keys` is the appropriate row from `df_keys` as a dictionary
        self.project_directory = self.df_proj_keys['Folder']
        self.lat = self.df_proj_keys['GPS_Lat']
        self.lon = self.df_proj_keys['GPS_Long']
        self.tz = f"US/{self.df_proj_keys['Timezone']}"
        self.MWAC = self.df_proj_keys['MWAC']
        try:
            self.publish_date = parse(self.df_proj_keys['PerfData_Publish_Date']).date()
        except:
            self.publish_date = datetime(2023, 1, 1).date()

        # PV model object for pvlib functionality
        self.pv_model = ProjectModel(self.project_name)    

        # Build filename for config file
        self.config_filepath = self._find_config_file()     

        # Get last update time for config file - we will use this to check if config file has been updated
        self.last_update_config = datetime.fromtimestamp(0)

        # Build filename for bool file
        self.bool_filepath = self._find_bool_file()     

        # Get last update time for bool file, will use it the same as config
        self.last_update_bool = datetime.fromtimestamp(0)

        # Build filename for Powertrack file
        self.powertrack_filepath, self.powertrack_csv = self._find_powertrack_file()

        # Initialize powertrack update time, will use it the same as config
        self.last_update_powertrack = datetime.fromtimestamp(0)

        # Check for pickle jar folder & create if it doesn't exist
        self.pickle_jar = self._find_pickle_jar()
        
        # Initialize other instance variables
        self.config_sheets = {}
        self.config_column_map = pd.Series()
        self.colnames_ccr = []
        self.colnames_das = []
        self.df = pd.DataFrame()
        self.df_Pvsyst = pd.DataFrame()
        self.df_sensor_ON = pd.DataFrame()
        self.df_bool = pd.DataFrame()
        self.df_sensors = pd.DataFrame()
        self.df_sensors_native_avg = pd.DataFrame()
        self.df_solcast = pd.DataFrame()

        # Finish initializing project
        # FIXME: update error handling when can't find config file
        self._parse_config_file()
        self._load_bool_file()
        self._map_columns()
        self._find_neighbor_sensors()
        self.__get_project_parameters()
        self.__read_degradation_profile()

        # Plotter object to store dashboard plots
        self.plotter = Plotter(self)


        # Type annotations & docstrings for documentation
        self.project_name: str
        """The string representation of the [Project][ccrenew.dashboard.project.Project] name.
            This should match the 'Project' field in [df_keys][ccrenew.dashboard.session.DashboardSession.df_keys]."""
        self.proj_init_dict: dict
        """Metadata related to the project generated by the [DashboardSession][ccrenew.dashboard.session.DashboardSession]
            from which it was initialized."""
        self.df_proj_keys: dict
        """The subset of [df_keys][ccrenew.dashboard.session.DashboardSession.df_keys]
            corresponding to the [Project][ccrenew.dashboard.project.Project] instance."""
        self.df_proj_ss_comments: dict
        """The comments entered into the Dashboard Startup Notes Smartsheet"""
        self.processed: bool
        """Flag to denote if the Project has been processed."""
        self.errored: bool
        """Flag to denote if the Project has errored out during processing."""
        self.error_info: str
        """Information on the error that caused the Project to error during processing."""
        self.project_directory: str
        """Folder in the Dashboard file structure where the project data lives."""
        self.pickle_jar: str
        """Directory where the Project's pickle files are stored."""
        self.config_filepath: str
        """Filepath for the Project's config file."""
        self.last_update_config: datetime
        """Timestamp of the last update to the config file. This is used to
            check if it needs to be re-loaded from the filesystem."""
        self.bool_filepath: str
        """Filepath for the Project's bool file based on the year."""
        self.last_update_bool: datetime
        """Timestamp of the last update to the bool file. This is used to
            check if it needs to be re-loaded from the filesystem."""
        self.powertrack_filepath: str
        """Filepath for the Project's Powertrack file."""
        self.last_update_powertrack: datetime
        """Timestamp of the last update to the powertrack file. This is used to
            check if it needs to be re-loaded from the filesystem."""
        self.config_sheets: dict
        """Dictionary of `DataFrame`s for each sheet in the config file."""
        self.colnames_ccr: list
        """CCR standard column names for data fields."""
        self.colnames_das: list
        """Original column names from the DAS."""
        self.pv_model: ProjectModel
        """A model for the project based on the `pvlib` package."""
        self.plotter: Plotter
        """An object to store dashboard plots"""
        self.config_neighbor_sensors: set
        """A list of neighbor sensors that are available to the project.
        These are set with the `Get_Sensor` keyword on the `data` tab of the config file"""
        self.neighbor_list: dict
        """List of neighbors that meet the criteria for data substitution.
        
        * Default Criteria:
            * Distance: $<=$ 10 miles
            * Same racking OEM
            * Fixed tilt:
                * Same module tilt
            * Tracker:
                * GCR $+/-$ 0.05
        """
        self.df: pd.DataFrame
        """Main source of hourly data."""
        self.df_Pvsyst: pd.DataFrame
        """Projected hourly values for the year, aka the '8760'."""
        self.P_exp: pd.Series
        """Expected weather-adjusted hourly meter production values."""
        self.df_sensor_ON: pd.DataFrame
        """Boolean table to specify if a meter or sensor should be used or ignored."""
        self.df_bool: pd.DataFrame
        """Boolean table generated from bool file in project's config folder."""
        self.df_sensors: pd.DataFrame
        """Native sensors for the project."""
        self.df_sensors_native_avg: pd.DataFrame
        """Average of the native sensors for the project."""
        self.df_solcast: pd.DataFrame
        """Solcast data for the project."""
        self.snow_data: pd.DataFrame
        """Calculated snowfall inches by day for the project."""
        self.snow_coverage: pd.Series
        """Snow coverage for the project."""
        self.lat: float
        """Project latitude."""
        self.lon: float
        """Project longitude."""
        self.tz: str
        """Project timezone from the Olson timezone database."""
        self.MWAC: float
        """Nameplate AC rating of the project."""
        self.Battery_AC_site: bool
        """Flag denoting a project with AC battery storage"""
        self.Battery_DC_site: bool
        """Flag denoting a project with DC battery storage"""
        self.Tracker_site: bool
        """Flag denoting a project with tracker-type racking"""


    def __repr__(self):
        return f'{self.report_type_map[self.report_type]} Project object for {self.project_name}'

    
    def __str__(self):
        return f'{self.report_type_map[self.report_type]} Project object for {self.project_name}'


    def _parse_config_file(self):
        """Reads data from config file & parses each sheet into a dataframe"""
        # Read variables from Plant Configuration File
        # `self.config_sheets` will store all the sheets from the config file as a dictionary
        if self.last_update_config == get_modified_time(self.config_filepath, self.data_platform, 'file'):
            return

        try:
            print("Loading config file for {}".format(self.project_name))
            self.config_sheets = pd.read_excel(self.config_filepath, sheet_name=None)
        except Exception:
            error_num = sys.exc_info()[1].errno # type: ignore
            if error_num == 2:
                error_msg = 'Config file not found for {}. Please verify the following file exists and try again: {}'.format(self.project_name, self.config_filepath)
                # logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            elif error_num == 13:
                error_msg = 'Config file is open for {}. Please close the file and try again'.format(self.project_name)
                # logger.error(error_msg)
                raise FileOpenError(error_msg)
            else:
                raise Exception()
        
        # Set all sheets of the config file to instance variables

        ################ `data` tab ###############
        self.df_config = self.config_sheets['data'].fillna(0)

        # Create dictionary of config parameters
        df_config_dict = self.df_config.to_dict('list')
        self.config_dict = dict(zip(df_config_dict['Name'], df_config_dict['Value']))

        ############# `Column_ID` tab #############
        # `colnames_ccr` is a list of the CCR column names
        # `colnames_das` is a list of the original column names from the project's DAS
        col_id_sheet = self.config_sheets['Column_ID']

        # Python 2 compatibility - old versions of Pandas would read the first column as the index, with new versions we have to set it explicitly
        if col_id_sheet.index.inferred_type == 'integer':
            col_id_sheet = col_id_sheet.set_index(col_id_sheet.columns[0])

        self.config_column_map = col_id_sheet.iloc[2,:]
        self.colnames_ccr = self.config_column_map.index.tolist()
        self.colnames_das = self.config_column_map.values.tolist() # type: ignore
        self.non_error_cols = [col for col in self.colnames_ccr if 'ERROR' not in col]

        ########## `Sensor_Offline` tab ###########
        self.sensor_OFF = self.config_sheets['Sensor_Offline'].reset_index()

        ############## `Unit_Tab` tab #############
        self.Convert_Units = self.config_sheets['Unit_Tab']

        ################ `8760` tab ###############
        # Only run UL or weekly for CCR owned projects
        if self.df_proj_keys['Owner'] != 'CCR':
            self.report_type = 'monthly'

        # Option to run UL or weekly reports
        if self.report_type.lower() == 'monthly':
            self.df_Pvsyst = self.config_sheets['8760'].fillna(0)
        else:
            self.df_Pvsyst = self.config_sheets['UL_8760'].fillna(0)
        self.df_Pvsyst.loc[self.df_Pvsyst['Year 0 Actual Production (kWh)'] < 0, 'Year 0 Actual Production (kWh)'] = 0

        # Create date index from date column
        try:
            self.df_Pvsyst.loc[:, 'date'] = pd.to_datetime(self.df_Pvsyst.loc[:, 'date'])
            self.df_Pvsyst.set_index('date', inplace=True)
        except KeyError:
            pass

        # Get capacity & neighbor sensor params
        self.OFF_PEAK = self.config_dict['OFF_PEAK']
        self.CAPACITY_ON_PEAK_SUMMER = self.config_dict['CAPACITY_ON_PEAK_SUMMER']
        self.CAPACITY_ON_PEAK_NON_SUMMER = self.config_dict['CAPACITY_ON_PEAK_NON_SUMMER']
        self.Get_Sensor = self.df_config.loc[(self.df_config['Name'].str.lower() == 'get_sensor'), :]
        
        # Update last config update timestamp
        self.last_update_config = get_modified_time(self.config_filepath, self.data_platform, 'file')


    def _load_bool_file(self):
        try:
            if self.last_update_bool != get_modified_time(self.bool_filepath, self.data_platform, 'file'):
                self.df_bool = pd.read_csv(self.bool_filepath, index_col=0, parse_dates=True)
                self.last_update_bool = get_modified_time(self.bool_filepath, self.data_platform, 'file')
        except:
            pass


    def _map_columns(self):

        def get_col_locs(df_cols, colref):
            col_locs = [col for col in df_cols if colref in col]
            return col_locs

        # Read in column names from powertrack csv file - we won't read any rows since we just need the column names.
        try:
            raw_df = pd.read_csv(self.powertrack_csv, index_col=0, nrows=0)
        except:
            self.load_production_data()
            raw_df = pd.read_csv(self.powertrack_csv, index_col=0, nrows=0)


        # Create column mappings based on sensor type
        raw_df_cols = raw_df.columns
        tamb_cols = get_col_locs(raw_df_cols, 'Tamb')
        tmod_cols = get_col_locs(raw_df_cols, 'Tmod')
        wind_cols = get_col_locs(raw_df_cols, 'Wind_speed')
        temp_cols = tamb_cols + tmod_cols
        weather_cols = temp_cols + wind_cols
        poa_cols = get_col_locs(raw_df_cols, 'POA')

        self.col_ref = {'Tamb_cols': tamb_cols,
                        'Tmod_cols': tmod_cols,
                        'Wind_cols': wind_cols,
                        'Temp_cols': temp_cols,
                        'Weather_cols': weather_cols,
                        'POA_cols': poa_cols,
                        'Sensor_cols': weather_cols + poa_cols}

        self.sensor_colmap = [Colmap(self.col_ref['Tamb_cols'], 'Tamb_avg'),
                              Colmap(self.col_ref['Tmod_cols'], 'Tmod_avg'),
                              Colmap(self.col_ref['Wind_cols'], 'Wind_speed'),
                              Colmap(self.col_ref['POA_cols'], 'POA_avg')]

    
    def _find_neighbor_sensors(self):
        """Loops through all neighbor sensors listed in the config file and adds the
        `Project` to `neighbor_sensors`"""
        # TODO: check here if project already exists in DashboardSession & load it if not
        for neighbor_name in self.Get_Sensor['Source'].unique().tolist():
            self.config_neighbor_sensors.add(neighbor_name)
            
            
    def __get_project_parameters(self):
        """Checks that base parameters are present in `df_keys` & pulls the parameters from the config file if not"""
        params = [self.df_proj_keys['MWDC'], 
                  self.df_proj_keys['Delta_Tcnd'],
                  self.df_proj_keys['Temp_Coeff_Pmax'],
                  self.df_proj_keys['a_module'],
                  self.df_proj_keys['b_module']
                  ]
        # Check if any parameters are not present
        if not np.isnan(params).any():
            self.Pstc_KW, self.Delta_Tcnd, self.Temp_Coeff_Pmax, self.a_module, self.b_module = params
            self.Pstc_KW = self.Pstc_KW * 1000  # MW to kW
            self.Temp_Coeff_Pmax = self.Temp_Coeff_Pmax / 100.0  # % to decimal
        # Pull parameters from config file if any are not present
        else:
            print("*** df_keys INFO NOT COMPLETE for {} ***".format(self.project_name))
            logging.warn("df_keys INFO NOT COMPLETE for {} ***".format(self.project_name))
            self.Pstc_KW = self.config_dict['Pstc_KW']
            self.Delta_Tcnd = self.config_dict['Delta_Tcnd']
            self.Temp_Coeff_Pmax = self.config_dict['Temp_Coeff_Pmax']
            self.a_module = self.config_dict['a_module']
            self.b_module = self.config_dict['b_module']
        
        # Check if Placed In Service date exits
        if self.df_proj_keys['PIS'] == self.df_proj_keys['PIS']:
            self.PIS_date = self.df_proj_keys['PIS']
        else:
            self.PIS_date = datetime(2050, 1, 1)  # fake date
            # NOTE: warn on this - it's needed for degradation profile
            print('*** PIS Date Load failed for {} ***'.format(self.project_name))
            logging.warn('*** PIS Date Load failed for {} ***'.format(self.project_name))

        # Check if Final Completion date exists
        if self.df_proj_keys['FC'] == self.df_proj_keys['FC']:
            self.SC_Date = self.df_proj_keys['FC']
        else:
            self.SC_Date = datetime(2050, 1, 1)  # fake date
            # QUESTION: is FC Date important? Do we need to fill it out? Do we need to warn about it?
            # NOTE: Don't need to log this - comment out for now in case CCR starts to develop projects
            print('*** FC Date Load failed for {} ***'.format(self.project_name))
            logging.warn('*** FC Date Load failed for {} ***'.format(self.project_name))
        
        # Get `clipping_KW` based on max value on the 8760
        self.clipping_KW = self.df_Pvsyst['Year 0 Actual Production (kWh)'].max()

        # Calculate ASTM linear regression coef to calculate Weather adjusted values
        self.var_astm = ['Year 0 Actual Production (kWh)', 'POA (W/m2)', 'Wind Velocity (m/s)', 'Ambient Temperature']
        self.df_coef, self.df_coef_RC = weather.generate_linear_coeff_table_v3(self.df_Pvsyst, self.var_astm, self.clipping_KW)

        # Find empty months
        if not self.df_coef.loc[:, self.df_coef.sum() == 0].empty:
            aux = self.df_coef.loc[:, self.df_coef.sum() == 0]
            # Find typical values to replace bad ones
            avg = self.df_coef.loc[:, self.df_coef.sum() != 0].mean(axis=1)

            # Edit months that failed
            for col in aux.columns:
                self.df_coef.loc[:, col] = avg
            print ("Edited ASTM test - no data for months: " + ",".join(aux.columns))
            logging.warn("Edited ASTM test - no data for months: " + ",".join(aux.columns))


    def __read_degradation_profile(self):
        """Generates the degradation profile for the `Project` based on hardware & years in service"""
        # Create empty dataframe to store profile
        self.Deg = pd.DataFrame(index=range(41))

        # Initialize `Capacity` column to zero & set year 1 to 100%
        self.Deg['Capacity'] = 0.0
        self.Deg['Capacity'][0] = 1.0

        # Find degradation rows
        Deg_Read = [s for s in self.df_config['Name'] if "-ENG- -DEG- AC Energy De-Rate Year" in s]
        
        # Extract year from string
        year_str = [x[35:37] for x in Deg_Read]
        year_ = [int(y) for y in year_str]

        # Add degradation for the corresponding year
        for i in range(len(Deg_Read)):
            self.Deg['Capacity'][year_[i]] = self.df_config[self.df_config['Name'] == Deg_Read[i]]['Value'].values[0]

        # find if any elements are 0. Any matches trigger else condition
        # QUESTION: Do we want to exit the run if the degradation profile fails??
        # NOTE: warn but still run
        if np.any(self.Deg['Capacity'] == 0):
            # Set all degradation values to 100%
            self.Deg['Capacity'] = 1
            print('*** Degradation profile failed for {} ***'.format(self.project_name))

        # Fix year index to properly to 0.0, 0.5, 1.5 index steps per Jeff Webber spreadsheet
        self.Deg.set_index(np.append([0], np.arange(0.5, 40.5, 1)), inplace=True)


    def _find_config_file(self) -> str:
        # Build filename for config file
        config_filename = self.project_name + r'_Plant_Config_MACRO.xlsm'
        config_filepath = os.path.join(self.dashboard_dir,
                                        self.project_directory,
                                        self.project_name,
                                       'Plant_Config_File',
                                        config_filename)

        config_filepath = Path(config_filepath)

        if self.data_platform == 's3':
            # Convert Windows-type filepath to use forwards slashes like a normal
            config_filepath = config_filepath.as_posix().replace('s3:/', 's3://')
            s3_filepath = make_s3_filepath(config_filepath, obj_type='file')
            try:
                s3_client.get_object(Bucket=s3_filepath.bucket, Key=s3_filepath.key)
            except:
                raise RuntimeError("*** No config file on S3 found for {}, skipping project. Check that filepath exists: {}".format(self.project_name, config_filepath))
            
        else:
            if not config_filepath.is_file():
                raise RuntimeError("*** No config file on Sharepoint found for {}, skipping project. Check that filepath exists: {}".format(self.project_name, config_filepath))

            config_filepath = str(config_filepath)

        return config_filepath


    def _find_bool_file(self):
        # Build filename for bool file
        bool_filename = f"{self.year}_{self.project_name}_BOOL.csv"
        bool_filepath = os.path.join(self.dashboard_dir,
                                     self.project_directory,
                                     self.project_name,
                                     'Plant_Config_File',
                                     bool_filename)

        bool_filepath = Path(bool_filepath)

        if self.data_platform == 's3':
            # Convert Windows-type filepath to use forwards slashes like a normal
            bool_filepath = bool_filepath.as_posix().replace('s3:/', 's3://')
        else:
            bool_filepath = str(bool_filepath)

        return bool_filepath


    def _find_powertrack_file(self):
        # Find Powertrack folder
        self.data_AE_dir = os.path.join(self.dashboard_dir,
                                        self.project_directory,
                                        self.project_name,
                                        'Powertrack_data')
        
        if self.data_platform == 's3':
            s3_filepath = make_s3_filepath(self.data_AE_dir, obj_type='folder')
            all_pt_files = s3_client.list_objects(Bucket=s3_filepath.bucket, Prefix=s3_filepath.key)
            powertrack_filename = [f['Key'] for f in all_pt_files['Contents'] if self.data_source in f['Key']][0]
            powertrack_filename = Path(powertrack_filename).name
        else:
            self.data_AE_all_files = [f for f in os.listdir(self.data_AE_dir) if os.path.isfile(os.path.join(self.data_AE_dir, f))]
            powertrack_filename = [s for s in self.data_AE_all_files if self.data_source in s][0]

        # TODO: check on error handling here if we can't find the Powertrack file
        if len(powertrack_filename) == 0:
            raise PowertrackFileException("*** No Powertrack file found for {}, skipping project".format(self.project_name))

        # Build filename for Powertrack file
        powertrack_filepath = Path(self.dashboard_dir) / self.project_directory / self.project_name / 'Powertrack_data' / powertrack_filename
        powertrack_csv = Path(powertrack_filepath).parent / f"{self.year}_hourly_{self.project_name}.csv"

        if self.data_platform == 's3':
            # Convert Windows-type filepath to use forwards slashes like a normal
            powertrack_filepath = powertrack_filepath.as_posix().replace('s3:/', 's3://')
            powertrack_csv = powertrack_csv.as_posix().replace('s3:/', 's3://')
        else:
            powertrack_filepath = str(powertrack_filepath)
            powertrack_csv = str(powertrack_csv)
        
        return powertrack_filepath, powertrack_csv


    def _find_pickle_jar(self):
        # Check for pickle jar folder & create if it doesn't exist
        pickle_jar = os.path.join(self.dashboard_dir,
                                       self.project_directory,
                                       self.project_name,
                                       'Pickle_Jar')

        pickle_jar = Path(pickle_jar)

        if self.data_platform == 's3':
            # Check that Pickle Jar exists & create folder if not
            s3_filepath = make_s3_filepath(pickle_jar, obj_type='folder')
            try:
                s3_client.get_object(Bucket=s3_filepath.bucket, Key=s3_filepath.key)
            except:
                s3_client.put_object(Bucket=s3_filepath.bucket, Key=s3_filepath.key)

            # Convert Windows-type filepath to use forwards slashes like a normal
            pickle_jar = pickle_jar.as_posix().replace('s3:/', 's3://')
        else:
            if not pickle_jar.is_dir():
                pickle_jar.mkdir()

            pickle_jar = str(pickle_jar)
        
        return pickle_jar


    def load_production_data(self):
        """Loads production data from the Project's Powertrack file.
        If file has already been loaded, it will check
        [last_update_powertrack][ccrenew.dashboard.project.Project.last_update_powertrack]
        against the last updated timestamp on the file system to determine if it needs
        to reload the data from the file system or use the previously loaded data in the Project object.
        """

        # Read Powertrack data
        # If the powertrack file has been updated since we last loaded production
        # we'll read the data from Excel & store a copy in df_powertrack
        # If it hasn't been updated we'll just use the powertrack copy we loaded previously
        try:
            last_update_powertrack_file = get_modified_time(self.powertrack_filepath, self.data_platform, 'file')
        except:
            self.powertrack_filepath, self.powertrack_csv = self._find_powertrack_file()
            last_update_powertrack_file = get_modified_time(self.powertrack_filepath, self.data_platform, 'file')
        
        if self.last_update_powertrack != last_update_powertrack_file:
            self.__load_from_source(self.powertrack_filepath)
        else:
            # If we try to load from `df_powertrack` and it doesn't exist we'll need to load from source
            try:
                self.df = self.df_powertrack.copy()
                self.df.set_index(pd.to_datetime(self.df.index))
                print('Using previously loaded Powertrack file for {}'.format(self.project_name))
            except AttributeError:
                self.__load_from_source(self.powertrack_filepath)
            
        # Find native sensors, used to find DAS_ON instead of all sensors.
        # Avoids using Get_Sensor data from another site
        val = ['Meter_kw_', 'POA', 'GHI', 'Wind_speed', 'Inv_kw_', 'Inv_kwnet', 'Tmod', 'Tamb']
        self.pos_Native = [s for s in self.df.columns if any([x in s for x in val])]

        # Convert production data to hourly values
        # Replace any blank strings with NaN
        self.df = self.df.replace(r'^\s*$', np.nan, regex=True)
        self.df = self.df.resample('h').mean()

        # Initialize & populate sensor_ON dataframe
        self.df_sensor_ON = pd.DataFrame(columns=self.df.columns.tolist(), index=self.df.index).fillna(True).astype(bool)

        # Initialize POA_source column & disable any faulty sensors defined in the config file
        self.df.loc[:, 'POA_source'] = 'Native'
        self._config_disable_sensors()

        # Fetch solcast data - this will only query data from AWS once for a project, if it's already loaded data it won't do it again.
        self._fetch_solcast_data()


    def __load_from_source(self, filepath):
        print('Loading Powertrack data for {}'.format(self.project_name))
        # Load data from Excel
        try:
            self.df = pd.read_excel(filepath, sheet_name='Sheet1', skiprows=0, index_col=0)
        except IOError as e:
            error_num = e.errno
            if error_num == 2:
                error_msg = 'Powertrack file not found for {}. Please verify the following file exists and try again: {}'.format(self.project_name, self.config_filepath)
                # logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            elif error_num == 13:
                error_msg = 'Powertrack file is open for {}. Please close the file and try again'.format(self.project_name)
                # logger.error(error_msg)
                raise FileOpenError(error_msg)
            else:
                error_msg = e
                raise Exception(error_msg)

        # Curtail date to max of `data_cutoff_date`
        self.df = self.df.loc[self.df.index < self.data_cutoff_date, :]

        # Apply CCR column names to df
        self.colnames_ccr = self.config_column_map.index.tolist()
        self.colnames_das = self.config_column_map.values.tolist() # type: ignore
        self.non_error_cols = [col for col in self.colnames_ccr if 'ERROR' not in col]

        # This top case happens if some columns are removed from the
        # Powertrack file after the COLUMN_ID tab has been set up in the config file
        if len(self.df.columns) < len(self.colnames_ccr):
            list1 = self.df.columns.tolist()
            list2 = self.colnames_das
            list1_upper = [x.upper() for x in list1]
            list2_upper = [x.upper() for x in list2]
            ind_list_position = [i for i, item in enumerate(list2_upper) if item in list1_upper]
            self.colnames_ccr = [self.colnames_ccr[i] for i in ind_list_position]
            self.df.columns = self.colnames_ccr
            self.non_error_cols = [col for col in self.colnames_ccr if 'ERROR' not in col]
        else:
            self.df.columns = self.colnames_ccr

        # Remove error columns
        self.df = self.df.reindex(columns=self.non_error_cols)

        # Copy columns if necessary - most commonly used to map inverters to meters
        # at sites where we don't have standalone meters & use the inverters as a proxy
        Copy_Sensor = self.df_config.loc[(self.df_config['Name'].str.lower() == 'copy_sensor'), :]
        Copy_from = Copy_Sensor['Value'].values.tolist() # type: ignore
        Copy_to = Copy_Sensor['Source'].values.tolist() # type: ignore
        for _from, _to in zip(Copy_from, Copy_to):
            self.df[_to] = self.df[_from]
            self.colnames_ccr = self.colnames_ccr + [_to]

        # Locate columns
        self._locate_column_positions()

        # Perform any unit conversions needed
        self._convert_sensor_units()

        # Update the last updated date for the powertrack file
        self.last_update_powertrack = get_modified_time(self.powertrack_filepath, self.data_platform, 'file')
        self.df_powertrack = self.df.copy()

        # Write to csv
        self.df.to_csv(self.powertrack_csv)


    def _fetch_solcast_data(self):
        # If solcast data hasn't been loaded from AWS or the indexes of the main df & df_solcast don't match - load data
        if self.df_solcast.empty:
            start_date = self.df.index[0]
            end_date = self.df.index[-1]

            fetch_ghi = False
            if self.pos_GHI:
                fetch_ghi = True
            df_solcast = self.pv_model.run_bluesky(start_date, end_date, resample=True, fetch_ghi=fetch_ghi) # type: ignore

            # Rename to match sensor avg columns & replace NaNs
            self.df_solcast = df_solcast.rename(columns={'Tamb': 'Tamb_avg', 'Tmod': 'Tmod_avg',
                                                         'poa': 'POA_avg', 'ghi': 'GHI_avg'})

  
    def _locate_column_positions(self):
        # Find Meters
        self.pos_Meter = [s for s in self.df.columns if 'Meter_kw_' in s]
        # Find CUM Meters
        self.pos_Meter_Cum = [s for s in self.df.columns if 'Meter_kwhnet_' in s]
        # search for POA sensors and generate avg.
        self.pos_POA = [s for s in self.df.columns if 'POA' in s and s != 'POA_source']
        # search for GHI sensors and generate avg
        self.pos_GHI = [s for s in self.df.columns if 'GHI' in s]
        #   Wind speed in m/s.  Also Energy gives wind speed in Km/h
        self.pos_Wind = [s for s in self.df.columns if 'Wind_speed' in s]
        #   Find Inverters
        self.pos_Inv = [s for s in self.df.columns if 'Inv_kw_' in s]
        self.pos_Inv_cum = [s for s in self.df.columns if 'Inv_kwnet_' in s]

        #  Convert all Temperature sensor in Celcius if needed
        self.pos_Tmod = [s for s in self.df.columns if 'Tmod' in s]
        self.pos_Tamb = [s for s in self.df.columns if 'Tamb' in s]
        self.pos_Temperature = self.pos_Tamb + self.pos_Tmod

        #  Main meter site cols - battery sites only
        self.pos_POI_Meter = [s for s in self.df.columns if 'POI_kw_' in s]
        self.pos_POI_Meter_Cum = [s for s in self.df.columns if 'POI_kwhnet_' in s]

        #  Battery site cols
        self.pos_BatteryAC = [s for s in self.df.columns if 'BatteryAC_kw_' in s]
        self.pos_BatteryAC_del = [s for s in self.df.columns if 'BatteryAC_kwhdel_' in s]
        self.pos_BatteryAC_rec = [s for s in self.df.columns if 'BatteryAC_kwhrec_' in s]

        # Find all tracker position sensors
        self.pos_Tracker = [s for s in self.df.columns if 'Tracker_position' in s]
        

    def _convert_sensor_units(self):
        """

        """
        # Perform unit conversions that are found in the configuration file
        if np.any(['Convert_Multiply' in s for s in list(self.Convert_Units.columns)]):
            Convert_custom = self.Convert_Units.loc[~self.Convert_Units['Convert_Multiply'].isnull(), ['Var_ID', 'Convert_Multiply']]
            for index, row in Convert_custom.iterrows():
                self.df[row['Var_ID']] = self.df[row['Var_ID']] * row['Convert_Multiply']

        # Convert sensor units
        Convert_Temperature = self.Convert_Units.loc[self.Convert_Units['Convert_Farenheit_to_Celcius'] == True, 'Var_ID'].values.tolist() # type: ignore
        for t_sensor in Convert_Temperature:
            self.df[t_sensor] = (self.df[t_sensor] - 32.0) * 5.0 / 9.0

        Convert_wind = self.Convert_Units.loc[self.Convert_Units['Convert_mph_to_mps'] == True, 'Var_ID'].values.tolist() # type: ignore
        for wind in Convert_wind:
            self.df[wind] = self.df[wind] * 0.44704


    def get_columns(self):
        """Prints out CCR column names with their location in the Project's
        Powertrack file and a map to its DAS column name.
        """
        intake = self.pos_Meter + self.pos_Meter_Cum + self.pos_Inv + self.pos_Inv_cum
        columns_df=pd.DataFrame(data={'Column':[],'Position':[],'OG Name':[]})
        #lists out the column names and index for the lists. 
        for x in intake: 
            try:
                column=x
                position=xlsxwriter.utility.xl_col_to_name(self.colnames_ccr.index(x)+1)
                og=self.colnames_das[self.colnames_ccr.index(x)]
                temp=pd.DataFrame(data={'Column':[column],'Position':[position],'OG Name':[og]})
                columns_df=columns_df.append(temp)
            except IndexError:
                continue

        print('\n')
        print('Column locations for {}:'.format(self.project_name))
        print(columns_df[['Column','Position','OG Name']])
        print('\n')


    def get_sensors(self):
        """Prints out the location of POA & weather sensors in a Project's
        Powertrack file and a map to its DAS column name.
        """
        columns_df=pd.DataFrame(data={'Column':[],'Position':[],'OG Name':[]})
        for x in self.pos_POA: #lists out the column names and index for the lists.
            if len(x) < 7:
                column=x
                position=xlsxwriter.utility.xl_col_to_name(self.colnames_ccr.index(x)+1)
                og=self.colnames_das[self.colnames_ccr.index(x)]
                temp=pd.DataFrame(data={'Column':[column],'Position':[position],'OG Name':[og]})
                columns_df=columns_df.append(temp)
        for x in self.pos_Temperature: #lists out the column names and index for the lists.
            if len(x) < 7:
                column=x
                position=xlsxwriter.utility.xl_col_to_name(self.colnames_ccr.index(x)+1)
                og=self.colnames_das[self.colnames_ccr.index(x)]
                temp=pd.DataFrame(data={'Column':[column],'Position':[position],'OG Name':[og]})
                columns_df=columns_df.append(temp)
        for x in self.pos_Wind: #lists out the column names and index for the lists.
            if len(x) < 13:
                column=x
                position=xlsxwriter.utility.xl_col_to_name(self.colnames_ccr.index(x)+1)
                og=self.colnames_das[self.colnames_ccr.index(x)]
                temp=pd.DataFrame(data={'Column':[column],'Position':[position],'OG Name':[og]})
                columns_df=columns_df.append(temp)
        columns_df = columns_df.set_index('Column')
        print('\n')
        print('Sensor locations for {}:'.format(self.project_name))
        print(columns_df[['Position','OG Name']])
        print('\n')


    def get_ss_comments(self, num_comments: int|None=None):
        """Prints Smartsheet comments for the Project

        Args:
            num_comments (int): Number of comments to show, starting from the
                most recent. Defaults to None, which will show all comments.
        """
        
        # Remove 'test' column if present
        try:
            del self.df_proj_ss_comments['test']
        except KeyError:
            pass

        # Print out the number of comments provided or all comments if not provided
        if num_comments:
            comment_list = list(self.df_proj_ss_comments.items())[-num_comments:]
        else:
            comment_list = list(self.df_proj_ss_comments.items())
        for dt, comment in comment_list:
            print(dt + ': ', comment)
    

    def get_datasub_stats(self, add_sparklines:bool = True) -> pd.DataFrame|HTML:
        """Returns statistics from a daily linear regression on Solcast POA & GHI values.

        Returns:
            pd.DataFrame: Linear regression statistics for each day the analysis was run.
                <ul>
                    <li>`rPOA`: The R-value in relation to the Solcast POA</li>
                    <li>`mPOA`: The slope in relation to the Solcast POA</li>
                    <li>`rGHI`: The R-value in relation to the Solcast GHI</li>
                    <li>`mGHI`: The slope in relation to the Solcast GHI</li>
                </ul>
        """

        poa_cols = self.col_ref['POA_cols']
        df_poa = self.df[poa_cols]
        df_poa_w_sol = df_poa.join(self.df_solcast[['POA_avg', 'GHI_avg']].rename(columns={'POA_avg': 'Solcast POA',
                                                                                           'GHI_avg': 'Solcast GHI'}))

        # Find trackers that aren't tracking
        tracker_poa, datasub_stats = det.daylight_poa_mistracking(df=df_poa_w_sol, pv_model=self.pv_model, add_sparklines=add_sparklines, degree=8) # type: ignore
        if add_sparklines:
            # _repr_html_ escapes HTML so manually handle the rendering
            datasub_stats = HTML(datasub_stats.to_html(escape=False))

        return datasub_stats


    def find_nearby_projects(self, dist:int = 10, print_data:bool = True, include_retired:bool = False, df:pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """Creates a list of Projects within a certain distance of the reference Project.

        Args:
            dist (int): Number of miles to search around the reference Project`
            print_data (bool): Option to print the data in the console. If False,
                the DataFrame will be returned without printing out the contents.
            include_retired (bool): Option to include retired Projects in the search.
            df (Dataframe): DataFrame containing sitenames & lat/longs.
                Defaults to [df_keys][ccrenew.dashboard.session.DashboardSession.df_keys] if
                no df provided.

        Returns:
            Information about all Projects within the specified distance from the reference Project.
        """
        ns = neighbs.find_nearby_projects(self.project_name, dist, print_data, include_retired, df)
        return ns
    

    def find_nearby_similar_projects(self, dist:int=10, print_data:bool=True, include_retired:bool=False, df:pd.DataFrame=pd.DataFrame()) -> pd.DataFrame:
        """Creates a list of Projects within a certain distance of the reference
        Project that share similar racking properties. 

        * Similar Racking Criteria:
            * Same racking OEM
            * Fixed tilt:
                * Same module tilt
            * Tracker:
                * GCR $+/-$ 0.05
    
        Args:
            dist (int): See [find_nearby_projects()][ccrenew.dashboard.project.Project.find_nearby_projects]
            print_data (bool): See [find_nearby_projects()][ccrenew.dashboard.project.Project.find_nearby_projects]
            include_retired (bool): See [find_nearby_projects()][ccrenew.dashboard.project.Project.find_nearby_projects]
            df (Dataframe): See [find_nearby_projects()][ccrenew.dashboard.project.Project.find_nearby_projects]

        Returns:
            Information about all Project within a certain distance
                of the reference Project that share similar racking properties.
        """
        nss = neighbs.find_nearby_similar_projects(self.project_name, dist, print_data, include_retired, df=df)
        return nss


    def run_bluesky(self, start: DateLike|None=None, end: DateLike|None=None, tran_ghi: str='add',
                convert: bool=False, resample: bool=True, ghi_index: int=0, axis_tilt: int=0,
                surface_albedo: float=0.2, plot: bool=True, pool_size: int=6) -> None:
        """
        Pulls irradiance & weather data from Solcast for the Project & date range.

        Args:
            start (str or datetime): The start date for Solcast data. Default
                will set it to the first day of the current month.
            end (str or datetime): The end date for Solcast data. Default will
                set it to the day before the current date. Known by some as yesterday.
            tran_ghi (str): Option to run the script to transpose GHI for POA.
                
                * Options:
                    * `add` to add it to the df_cats dataframe.
                    * `only` to pull just the transposed GHI & not df_cats.
                    * `none` to pull just df_cats.

            plot (bool): Option to draw plots of the data from solcast.

        Returns:
            df_solcast (pd.DataFrame): The Solcast irradiance & weather data.
        """
        func_args = locals().copy()
        func_args.pop('self')
        # if self.df_solcast.empty:
        #     self.df_solcast = blu.get_weather_data()
        # df_cats = utils.run_bluesky(self.project_name, **func_args)
        print("`Project.run_bluesky()` not currently implemented. Please use `Project.pvmodel.run_bluesky()`")
        # return df_cats


    def generate_power_from_invoice(self, start:str|datetime, stop:str|datetime, total_energy:Numeric, clipping_limit:Numeric|None=None) -> pd.DataFrame:
        """Generates power based upon [P_exp][ccrenew.dashboard.project.Project.P_exp].
        User needs to ensure that all weather and irradiance data are filled in before running this script.

        Args:
            start (str or datetime): Start date for calculations.
            stop (str or datetime): End date for calculations.
            total_energy (Number): Total energy (per meter) from the invoice to fill in over the date range.
            clipping_limit (Number): Upper limit (per meter) to limit production.

        Returns:
            The calculated power data for the interval provided.
        """
        if not clipping_limit:
            clipping_limit = self.clipping_KW
        #use expected power (or POA though expected power is probs better)
        # QUESTION: DO WE WANT TO USE POWER OR POA HERE?
        #power_proportions will have a sum of 1, it represents what portion of power is contained in that hour
        power_proportions=self.df['P_exp'][start:stop]/(self.df['P_exp'][start:stop].sum())
        # power_proportions=project.df['POA_avg'][start:stop]/(project.df['POA_avg'][start:stop].sum())

        #get difference between curated power and actual invoiced to aim for 0
        remainder=total_energy
        #initiate a power_iterative term, its really the power when you remove points over clipping
        power_i= power_proportions*0
        
        #iteratively spread production over the month based on expected until remainder is near 0
        i = 0
        power_data = pd.DataFrame()
        while remainder >(total_energy/(10*10**8)): #while loop instead of for because i am seeking a goal, not an amount of iterations
            power_data=(power_proportions*remainder)+power_i
            power_i=power_data.clip(upper=clipping_limit) #gets rid of points over clipping
            remainder=(power_data-power_i).sum()
            i+=1
            if i > 10000:
                break
            
        print('\n')
        print('Power data successfully generated for {}'.format(self.project_name))
        print('\n')
        return power_data


    def plot_meters(self):
        """Plots all meters for the Project"""
        # We'll check if the project is processed & process it if not.
        # We won't flip the processed flag because we don't have neighbor data from a session
        if not self.processed:
            self._load_bool_file()
            self.load_production_data()
            self._process_data(neighbor_sensor_data={}, datasub=False, use_solcast=False)
            self.last_update_powertrack = datetime.fromtimestamp(0)
        self.plotter.draw_plots(plot_order='meters', close_plots=False)


    def plot_snow(self):
        """Plots snow data for the Project"""
        # We'll check if the project is processed & process it if not.
        # We won't flip the processed flag because we don't have neighbor data from a session
        if not self.processed:
            self._load_bool_file()
            self.load_production_data()
            self._process_data(neighbor_sensor_data={}, datasub=False, use_solcast=False)
            self.last_update_powertrack = datetime.fromtimestamp(0)
        self.plotter.draw_plots(plot_order='snow', close_plots=False)


    def save_pickle(self, store_plots=False):
        """Saves the Project object to a pickle in the
        [project_directory][ccrenew.dashboard.project.Project.project_directory].
        """
        if not store_plots and self.plotter:
            self.plotter.plot_list = {}
        year = self.year
        pickle_name = utils.picklefy_project_name(self.project_name)
        pickle_file = str(year) + "_" + pickle_name + ".pickle"
        pickle_path_sharepoint = Path(self.data_platform_dirs.sharepoint) / self.project_directory / self.project_name / 'Pickle_Jar' / pickle_file
        pickle_path_s3 = Path(self.data_platform_dirs.s3) / self.project_directory / self.project_name / 'Pickle_Jar' / pickle_file
        pickle_path_s3 = pickle_path_s3.as_posix().replace('s3:/', 's3://')
        
        with open(pickle_path_sharepoint, 'wb') as f:
            pickle.dump(self, f)
        
        fs = s3fs.S3FileSystem()
        with fs.open(pickle_path_s3, 'wb') as f:
            pickle.dump(self, f)


    def get_tracker_ava(self) -> pd.DataFrame:
        """Calculates tracker ava for the Project.

        Returns:
            Tracker ava.
        """
        # create an empty df to avoid issues with sites w/o data
        start = '1/1/'+str(self.year)
        end = '12/31/'+str(self.year)
        index = pd.date_range(start, end)
        columns = [u'Ava', u'Ava NaN', u'Ava No Interp', u'Ava Variance', u'Date', u'Site', u'Type']
        df_hist = pd.DataFrame(index=index, columns=columns)

        # get sites that actually have data
        tracker_prefix = 'Tracker_data_pf/Ava_History/'
        bucket = 'perfdatadev.ccrenew.com'
        key = tracker_prefix+self.project_name+'.csv'
        df_hist2 = utils.retrieve_s3_df(bucket, key)
        if len(df_hist2) > 0:
            df_hist2 = df_hist2.set_index(pd.to_datetime(df_hist2['Date']))
            df_hist2 = df_hist2[df_hist2.index.year == self.year] # type: ignore
            # combine together and resample
            df_hist = df_hist.combine_first(df_hist2)

            df_hist = df_hist.resample('M').mean()
        else:
            df_hist = df_hist.resample('M').asfreq()

        df_hist = df_hist[['Ava', 'Ava NaN', 'Ava No Interp', 'Ava Variance']]
        df_hist.columns = ['tracker_ava', 'tracker_ava_nan', 'tracker_ava_interpremoved', 'tracker_variance_ava']
        df_hist.loc[df_hist.index < '7/1/2020'] = np.nan
        return df_hist

    
    def export(self, server: str, dest: Union[str, list], save_pickle: bool, report_type:str, **kwargs) -> None:
        """
        Export project to desired location(s).

        Args:
            server (str): SQL table to export to. Options are `prod` or `dev`.
            dest (str or list): Option to export only certain parts of the project.
                `all` will export to all of the below destinations **except bool**.
            save_pickle (bool): Option to save pickle after exporting.

        `dest` Options

        | dest      | Description                                                              |
        |-----------|--------------------------------------------------------------------------|
        |  `excel`  | Export dataframes to Excel dashboard template.                          |
        |   `df`    | Export dataframe to the `Dataframes` folder of the project's [project_directory][ccrenew.dashboard.project.Project.project_directory], S3, and Bartertown PostgreSQL database. |
        | `summary` | Export monthly summary data to S3 and Bartertown PostgreSQL database.   |
        |  `snow`   | Export [snow_data][ccrenew.dashboard.project.Project.snow_data] and [snow_coverage][ccrenew.dashboard.project.Project.snow_coverage] dataframes to S3. |
        |  `bool`   | Export bool file to the `Plant_Config_File` directory of the project's [project_directory][ccrenew.dashboard.project.Project.project_directory]. |
        """
        # Add positionals to kwargs
        kwargs['server'] = server
        kwargs['dest'] = dest
        kwargs['save_pickle'] = save_pickle
        kwargs['report_type'] = report_type

        def call_func(func, **kwargs):
            func(**kwargs)

        export_dict = {
            'excel': self._export_excel,
            'df': self._export_df,
            'summary': self._export_summary,
            'snow': self._export_snow,
            'weekly': self._export_weekly,
            'bool': self._export_bool
        }
        if server == 'datasub':
            dest = 'summary'
        
        if report_type == 'weekly':
            dest = ['summary', 'weekly']
        else:
            export_dict.pop('weekly')

        if dest == 'all':
            export_dict.pop('bool')
            for func in export_dict.values():
                call_func(func, **kwargs)
        else:
            if isinstance(dest, str):
                func = export_dict[dest]
                call_func(func, **kwargs)
            elif isinstance(dest, Iterable):
                for d in dest:
                    func = export_dict[d]
                    call_func(func, **kwargs)
            else:
                raise TypeError("`dest` must be a string or list. Please update input and resubmit.")
        
        if dest == 'bool':
            save_pickle = False

        if save_pickle:
            self.save_pickle()


    def _export_excel(self, **kwargs) -> None:
        """
        Exports Dataframes to Excel dashboard template in the project's [project_directory][ccrenew.dashboard.project.Project.project_directory].

        Args:
            server (str): Option to insert data to prod or dev environments.
                <ul>
                    <li><code>dev</code> will export the data to Excel to test if any errors then delete the file.</li>
                    <li><code>test</code> will export the Excel sheet to the project's <code>project_directory</code></li>
                </ul>

        """
        server = kwargs.get('server')
        report_type = kwargs.get('report_type')

        template_filename = 'Dashboard_v07.xlsx'
        self.metadata = pd.DataFrame([], index=[1])
        self.metadata['date'] = str(datetime.now())
        self.metadata['username'] = os.getenv('username')
        self.metadata['version'] = sys.version
        try:
            self.metadata['filename'] = __file__
        except:
            self.metadata['filename'] = 'console'
        self.metadata['weather_adjusted_functions'] = weather.generate_Tcell.__module__
        self.metadata['Table_by_Rate_Schedule'] = rate_table.generate_table_variable_by_rev_schedule_v02.__module__
        self.metadata['Plant_Availability'] = plant_ava.calculate_inverter_availability_and_loss.__module__
        self.metadata['Correct_Meter_data'] = meter_correct.Correct_Meter_with_Inv_data_v01.__module__
        self.metadata['Rate_Structure_Python_with_DST'] = rates.generate_Rate_column.__module__
        self.metadata['Performance_Guarantees'] = perf.USB1_performance_guarantee.__module__
        self.metadata['snow_loss_functions'] = snow.timeseries.__module__
        self.metadata['Snow data file'] = self.snow_file
        self.metadata['df.index[0]'] = self.df.index[0]
        self.metadata['df.index[-1]'] = self.df.index[-1]
        self.metadata['pandas'] = pd.__version__
        self.metadata['dashboard template'] = template_filename
        self.metadata = self.metadata.T

        df_dict = {'PVsyst': self.df_Pvsyst_2_month,
                   'OM_Summary': self.OM_data,
                   'data_month': self.df_month_3,
                   'Table_gen': self.table_gen,
                   'Table_rev': self.table_rev,
                   'data_day': self.df_d2,
                   'Guarantee': self.df_perf,
                   'Metadata': self.metadata}
        # sheet_name_save = ['PVsyst', 'OM_Summary', 'data_month', 'Table_gen',
        #                    'Table_rev', 'data_day', 'Guarantee', 'Metadata']

        # Build filename for Excel output
        if self.project_name == 'Old Pageland Monroe Road Solar Farm':
            project_name = 'Old Pageland'
        else:
            project_name = self.project_name

        ts = datetime.now().strftime("%Y-%m-%d-T%H%M%m")
        s3_filename = project_name + '_' + ts +'.xlsx'
        sharepoint_filename = project_name + '.xlsx'

        if report_type.lower() == 'ul':
            s3_filename = s3_filename.replace('.xlsx', '_UL.xlsx')
            sharepoint_filename = sharepoint_filename.replace('.xlsx', '_UL.xlsx')

        if server.lower() != 'prod':
            s3_filename = s3_filename.replace('.xlsx', '_COPY.xlsx')
            sharepoint_filename = sharepoint_filename.replace('.xlsx', '_COPY.xlsx')

        # Create a copy of template in sharepoint
        dashboard_root_dir = Path(self.data_platform_dirs.sharepoint)
        template_filepath = dashboard_root_dir / 'Python_Functions' / 'Dashboard_Template' / template_filename
        output_dir = dashboard_root_dir / self.project_directory / self.project_name
        output_template = shutil.copy(template_filepath, output_dir)
        output_filepath = output_dir / sharepoint_filename
        try:
            os.rename(output_template, output_filepath)
        except FileExistsError:
            os.remove(output_filepath)
            os.rename(output_template, output_filepath)

        # Write data to file on sharepoint
        df_tools.dfs_to_excel(output_filepath, df_dict)

        # Store copy on S3 with export timestamp
        s3_filepath = Path(self.data_platform_dirs.s3) / self.project_directory / self.project_name / s3_filename
        s3_filepath = make_s3_filepath(s3_filepath, obj_type='file')
        bucket = s3_filepath.bucket
        key = s3_filepath.key
        s3_client.upload_file(output_filepath, Bucket=bucket, Key=key)

        if server != 'prod':
            os.remove(output_filepath)
            s3_client.delete_object(Bucket=bucket, Key=key)

    def _export_df(self, **kwargs) -> None:
        """
        Export dataframe to the `Dataframes` folder of the project's [project_directory][ccrenew.dashboard.project.Project.project_directory], S3, and Bartertown PostgreSQL database.

        Args:
            server (str): Option to insert data to prod or dev environments.
                <ul>
                    <li><code>dev</code> corresponds to <code>dev_analytic.am_processed_data_dev</code> and <code>cypress-perfeng-datalake-onprem-us-west-2</code>.</li>
                    <li><code>prod</code> corresponds to <code>dev_analytic.am_processed_data</code> and <code>cypress-perfeng-datalake-dev-us-west-2</code>.</li>
                </ul>
        """
        server = kwargs.get('server')
        report_type = kwargs.get('report_type')

        # PostgreSQL initialization
        engine = ccr.get_sql_engine()
        metadata = MetaData()

        #  Save to Dataframes folder on S3
        df_filename = self.data_source + self.project_name + '.csv'
        df_filepath = Path(self.data_platform_dirs.s3) / self.project_directory / self.project_name / 'Dataframes' / df_filename
        df_filepath = df_filepath.as_posix().replace('s3:/', 's3://')
        
        if report_type.lower() == 'ul':
            df_filepath = df_filepath.replace('.csv', '_UL_.csv')

        if server != 'prod':
            df_filepath = df_filepath.replace('.csv', '_COPY.csv')
            self.df[[x for x in self.df.columns if 'ERROR' not in x]].to_csv(df_filepath)
            s3_filepath = make_s3_filepath(df_filepath, obj_type='file')
            s3_client.delete_object(Bucket=s3_filepath.bucket, Key=s3_filepath.key)
        else:
            self.df[[x for x in self.df.columns if 'ERROR' not in x]].to_csv(df_filepath)
        
        if report_type.lower() == 'monthly':
            #send data to SQL
            def restructure(df):
                cols = df.columns.tolist()
                df['timestamp'] = pd.to_datetime(df.index)
                df2 = pd.melt(df, id_vars = ['timestamp'], value_vars = cols)
                return df2
            
            #only use relevant cols
            cols=['Inv_losses','Grid_losses','Snow_losses','Meter_Corrected_2']
            
            #STONE
            #turn off losses on single inverter sites if meter_Corrected_2 > 0
            if len(self.pos_Inv) == 1:
                self.losses.loc[(self.losses['Meter_Corrected_2'] > 0), 'Inv_losses'] = 0
            
            
            df_SQLhourly = restructure(self.losses[cols])
            df_SQLhourly['site_name'] = self.project_name
            #drop non float/int rows in value
            df_SQLhourly_2 = df_SQLhourly.loc[df_SQLhourly['value'].apply(lambda x: type(x) in [float, int]), :]
            
            # Specify which table to use in Bartertown
            if server.lower() == 'prod':
                table_name = 'am_processed_data'
            else:
                table_name = 'am_processed_data_dev'

            # Hacky way of upserting - we'll remove existing rows here
            table = Table(table_name, metadata, autoload=True, autoload_with=engine, schema='dev_analytic')
            stmt = delete(table).where(table.c.site_name == self.project_name).where(extract('year', table.c.timestamp) == self.year)
            engine.execute(stmt)

            # Then insert rows here
            df_SQLhourly_2.to_sql(name=table_name, con=engine, schema='dev_analytic',
                                if_exists='append', index=False, chunksize=None, dtype=None)
            
            # Export data to S3
            upload_df=self.losses[cols]
            upload_df['site_name']=self.project_name
            upload_df['datetime']=upload_df.index       
            upload_df=upload_df[['datetime']+cols+['site_name']]
            if server.lower() == 'prod':
                folder = f's3://cypress-perfeng-datalake-dev-us-west-2/Curated/HourlyLosses/year={self.year}'
            else: 
                folder = f's3://cypress-perfeng-datalake-onprem-us-west-2/Curated/HourlyLosses/year={self.year}'
            filename = f'{self.year}_data_{self.project_name}_am_processed_data_sql.csv'
            df_tools.write_to_s3(upload_df, folder, filename)

    
    def _export_summary(self, **kwargs) -> None:
        """Exports monthly summary data to S3 and Bartertown PostgreSQL database.

        Args:
            server (str): Option to insert data to prod or dev table.
                <ul>
                    <li><code>dev</code> corresponds to <code>dev_analytic.am_summary_data_dev</code> and <code>cypress-perfeng-datalake-onprem-us-west-2</code>.</li>
                    <li><code>prod</code> corresponds to <code>dev_analytic.am_summary_data</code> and <code>cypress-perfeng-datalake-dev-us-west-2</code>.</li>
                    <li><code>datasub</code> corresponds to <code>dev_analytic.am_summary_data_datasub</code> and <code>cypress-perfeng-datalake-onprem-us-west-2</code>.</li>
                <ul>
        """
        server = kwargs.get('server')
        report_type = kwargs.get('report_type')

        # PostgreSQL initializatioo
        engine = ccr.get_sql_engine()
        metadata = MetaData()

        df_tracker_ava = self.get_tracker_ava()
        df_toSQL = pd.concat(
            [self.df_Pvsyst_2_month[[u'KWh_adj_by_days', 'NREL_Weather_Adj_%']],
                self.df_month_2[['Plant_Perf_%', 'Snow_Adj_%', 'Grid_Ava_%', 'Inv_Ava_%', 'Meter_Corrected_2', 'PR_Plant']],
                self.df_Pvsyst_2_month['PR_IE_P50_PR'],
                self.df_month_2[['diff_PR_%', 'Project_IPR_%', 'Project_OPR_%', 'Project_OPR_Temp_%']],
                self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj'],
                self.df_month_2[['diff_weather_$', 'diff_Plant_Perf_$', 'diff_snow_$', 'diff_Grid_ava_$', 'diff_Inv_ava_$', 'Meter_Corrected_2_rev', 'diff_all_$', 'AC_Capacity_%', 'DC_Capacity_%', 'Monthly Probability of Exceedence']],
                self.df_Pvsyst_2_month['POA (W/m2)'],
                self.df_month_2[['POA_avg', 'Perf_Test_Pass']],
                self.df_Pvsyst_2_month[['POA_%', 'GHI_%', 'Model_Irradiance_Index', 'Post SC Date', 'Pvsyst_POA_weighted_Tcell']],
                self.df_month_2[['OPR_notemp', 'POA_weighted_Tcell', 'PR_notemp']],
                self.df_Pvsyst_2_month[['Pvsyst_PR_notemp', 'IE_AC_batt_eff_%', 'IE_AC_batt_rev_gain', 'Revenue_IE_POI']],
                self.df_month_2[['AC_batt_eff_%', 'AC_batt_eff_index_%', 'AC_batt_rev_gain', 'AC_batt_rev_index_%', 'diff_AC_batt_$', 'POI_Corrected_2', 'POI_rev', 'ac_battery_flag', 'Modeled_AC_batt_rev_gain', 'Modeled_AC_batt_rev_index_%', 'Modeled_AC_rev_target', 'OM_uptime']],
                self.df_Pvsyst_2_month[['POI Output (kWh)', 'Weather_prorate', 'days_month_5', 'Nominal_Noclip_Weather_Adj', 'Nominal_NoclipNoTemp_Weather_Adj', 'ie_clipping_dcimpact', 'ie_clipping_astmimpact']],
                self.df_month_2[['measured_clipping_dcimpact', 'measured_clipping_astmimpact', 'night_flag', 'POA_regress_flag', 'borrowed_data', 'inv_cum_check', 'poi_limit_flag', 'snowfall', 'snow_coverage_5', 'snow_coverage_energy']],
                self.OM_data2,
                df_tracker_ava],
            axis=1)

        df_toSQL['meter_check'] = (df_toSQL['Meter_Corrected_2'] / self.df_month_3['AE_Meter'].replace(0, np.nan)) - 1
        df_toSQL[['KWh_adj_by_days', 'Meter_Corrected_2', 'POA (W/m2)', 'POA_avg', 'POI_Corrected_2']] = \
            df_toSQL[['KWh_adj_by_days', 'Meter_Corrected_2', 'POA (W/m2)', 'POA_avg', 'POI_Corrected_2']]/1000

        # filter by months with no data, then filter for FC
        df_toSQL.loc[df_toSQL[u'KWh_adj_by_days'] == 0, :] = 0
        df_toSQL_FC = df_toSQL.copy()
        df_toSQL_FC.loc[self.df_Pvsyst_2_month['Post SC Date'] == 0, :] = 0

        # correct index
        df_toSQL.index = df_toSQL.index.strftime('%b') #type: ignore
        df_toSQL_FC.index = df_toSQL.index

        # create Total row. Combination of sums and sumproducts
        df_toSQL_total = pd.DataFrame([], columns=df_toSQL.columns.tolist(), index=['Total'])
        df_toSQL_total_FC = df_toSQL_total.copy()

        sum_var = [
            'KWh_adj_by_days', 'Meter_Corrected_2', 'Revenue_IE_P50_days_adj',
            'diff_weather_$', 'diff_Plant_Perf_$', 'diff_snow_$', 'diff_Grid_ava_$',
            'diff_Inv_ava_$', 'Meter_Corrected_2_rev', 'diff_all_$', u'POA (W/m2)',
            'POA_avg', 'Revenue_IE_POI', 'diff_AC_batt_$', 'POI_Corrected_2', 'POI_rev',
            'POI Output (kWh)', 'weather_ad_exp_prod_kwh', 'estimated_loss', 'weather_losses_kwh',
            'grid_ava_kwh', 'inv_ava_kwh', 'snow_loss_kwh', 'plant_perf_kwh']
        df_toSQL_total[sum_var] = df_toSQL[sum_var].sum().values
        df_toSQL_total_FC[sum_var] = df_toSQL_FC[sum_var].sum().values

        dot_var = [
            'NREL_Weather_Adj_%', 'Plant_Perf_%', 'Snow_Adj_%', 'Grid_Ava_%',
            'Inv_Ava_%', 'PR_Plant', 'PR_IE_P50_PR', 'diff_PR_%', 'Project_IPR_%',
            'Project_OPR_%', 'Project_OPR_Temp_%', 'AC_Capacity_%', 'DC_Capacity_%',
            'POA_%', 'GHI_%', 'Model_Irradiance_Index', 'Post SC Date', 'PR_notemp',
            'OPR_notemp', 'POA_weighted_Tcell', 'Pvsyst_PR_notemp', 'Pvsyst_POA_weighted_Tcell',
            'meter_check', 'IE_AC_batt_eff_%', 'IE_AC_batt_rev_gain', 'AC_batt_eff_%',
            'AC_batt_eff_index_%', 'AC_batt_rev_gain', 'AC_batt_rev_index_%',
            'ac_battery_flag', 'Modeled_AC_batt_rev_gain', 'Modeled_AC_batt_rev_index_%',
            'Modeled_AC_rev_target', 'OM_uptime', 'Weather_prorate', 'days_month_5',
            'Nominal_Noclip_Weather_Adj', 'Nominal_NoclipNoTemp_Weather_Adj',
            'ie_clipping_dcimpact', 'ie_clipping_astmimpact', 'measured_clipping_dcimpact',
            'measured_clipping_astmimpact', 'night_flag', 'POA_regress_flag', 'inv_cum_check',
            'poi_limit_flag', 'ovp_insolation', 'ovp_production']

        # Hacky way to avoid DivideByZero error - set scalar to pandas Series & cast zeroes to np.nan
        for var in dot_var:
            df_toSQL_total[var] = ((df_toSQL[var] * df_toSQL['KWh_adj_by_days']) / pd.Series(df_toSQL['KWh_adj_by_days'].sum()).replace(0, np.nan).values[0]).sum()
            df_toSQL_total_FC[var] = ((df_toSQL_FC[var] * df_toSQL_FC['KWh_adj_by_days']) / pd.Series(df_toSQL_FC['KWh_adj_by_days'].sum()).replace(0, np.nan).values[0]).sum()

        # TODO: fix probability of excedence total
        df_toSQL_total['Post SC Date'] = 0
        df_toSQL_total_FC['Post SC Date'] = 1

        # append
        df_toSQL = df_toSQL.append(df_toSQL_total)[df_toSQL.columns.tolist()].fillna(0)

        #df_toSQL_FC = df_toSQL_FC.append(df_toSQL_total_FC)[df_toSQL.columns.tolist()].fillna(0)
        df_toSQL = df_toSQL.append(df_toSQL_total_FC)[df_toSQL.columns.tolist()].fillna(0)

        # add cols
        df_toSQL['Year'] = [self.year] * len(df_toSQL)
        df_toSQL['Site_name'] = [self.project_name] * len(df_toSQL)
        df_toSQL['month'] = df_toSQL.index

        column_map = {'AC_Capacity_%': 'ac_capacity_5',
                    'DC_Capacity_%': 'dc_capacity_5',
                    'Grid_Ava_%': 'grid_ava_5',
                    'Inv_Ava_%': 'inv_ava_5',
                    'Monthly Probability of Exceedence': 'monthly_probability_of_exceedence',
                    'NREL_Weather_Adj_%': 'nrel_weather_adj_5',
                    'POA (W/m2)': 'poa_wm2',
                    'Plant_Perf_%': 'plant_perf_5',
                    'Post SC Date': 'post_fc',
                    'Project_IPR_%': 'project_ipr_5',
                    'Project_OPR_%': 'project_opr_5',
                    'Project_OPR_Temp_%': 'project_opr_temp_5',
                    'Snow_Adj_%': 'snow_adj_5',
                    'diff_PR_%': 'diff_pr_5',
                    'POA_%': 'poa_5',
                    'GHI_%': 'ghi_5',
                    'Model_Irradiance_Index': 'model_irradiance_index',
                    'POA_weighted_Tcell': 'poa_weighted_tcell',
                    'OPR_notemp': 'opr_notemp',
                    'Pvsyst_POA_weighted_Tcell': 'pvsyst_poa_weighted_tcell',
                    'PR_notemp': 'pr_notemp',
                    'Pvsyst_PR_notemp': 'pvsyst_pr_notemp',
                    'IE_AC_batt_eff_%': 'ie_ac_batt_eff_5',
                    'AC_batt_eff_%': 'ac_batt_eff_5',
                    'AC_batt_eff_index_%': 'ac_batt_eff_index_5',
                    'AC_batt_rev_index_%': 'ac_batt_rev_index_5',
                    'Modeled_AC_batt_rev_index_%': 'modeled_ac_batt_rev_index_5',
                    'POI Output (kWh)': 'om_unadjusted_p50_kwh',
                    'WAP_5': 'WAP_5'}

        df_toSQL['ccr_id'] = self.df_proj_keys['CCR_ID']
        df_toSQL['WAP_5'] = df_toSQL['Project_IPR_%'] / df_toSQL['NREL_Weather_Adj_%'].replace(0, np.nan) / df_toSQL['Snow_Adj_%'].replace(0, np.nan)
        df_toSQL = df_toSQL.rename(columns=column_map)
        df_toSQL = df_toSQL.rename(columns=lambda s: s.lower())
        df_toSQL['row_created_date']=str(datetime.now())

        # Specify which table to use in Bartertown
        if server.lower() == 'prod':
            table_name = 'am_summary_data'
        elif server.lower() == 'datasub':
            table_name = 'am_summary_data_datasub'
        else:
            table_name = 'am_summary_data_dev'
        
        if report_type.lower() in ['ul', 'weekly']:
            table_name = 'am_summary_data_UL'

        # Hacky way of upserting - we'll remove existing rows here
        table = Table(table_name, metadata, autoload=True, autoload_with=engine, schema='dev_analytic')
        stmt = delete(table).where(table.c.site_name == self.project_name).where(table.c.year == self.year)
        engine.execute(stmt)

        # Then insert rows here
        df_toSQL.to_sql(name=table_name,
                        con=engine,
                        schema='dev_analytic',
                        if_exists='append',
                        index=False,
                        chunksize=None,
                        dtype=None
        )
        
        # Export data to S3
        df_toSQL.index.rename('month', inplace=True)
        df_toSQL.drop(columns='year', inplace=True)
        df_toSQL = df_toSQL.replace([np.inf, -np.inf], 999999999)

        if report_type.lower() == 'monthly':
            if server.lower() == 'prod':
                folder = f's3://cypress-perfeng-datalake-dev-us-west-2/Curated/MonthlyLosses/year={self.year}'
            else:
                folder = f's3://cypress-perfeng-datalake-onprem-us-west-2/Curated/MonthlyLosses/year={self.year}'
            filename = f'{self.year}_data_{self.project_name}_sql_summary.csv'
            df_tools.write_to_s3(df_toSQL, folder, filename)


    def _export_weekly(self, **kwargs) -> None:
        server = kwargs.get('server')

        #todo: weekly reporting
        df_Pvsyst_m = self.df_Pvsyst_2_month[['DC_corrected_PVsyst_WA', 'POI Output (kWh)']]
        df_Pvsyst_m.index = df_Pvsyst_m.index.month
        df_Pvsyst_m['days'] = self.df_Pvsyst_2.groupby('month')['POA (W/m2)'].count() / 24
        df_Pvsyst_daily = df_Pvsyst_m[['DC_corrected_PVsyst_WA', 'POI Output (kWh)']].divide( df_Pvsyst_m['days'], axis=0)
        
        
        df_daily = self.df.resample('d').sum()
        for x in df_Pvsyst_daily.columns:
            df_daily[x] = df_daily.index.to_series().dt.month.map(df_Pvsyst_daily[x])
        
        df_daily = df_daily.loc[df_daily.index > '2020-01-01'] #leap year causes this to get messed up, 366 days / 7 doesn't play nicely
        #df_weekly = df_daily.resample('7D').sum()
        df_weekly = df_daily.resample('W-SAT').sum() 
        
        df_weekly['NREL_Weather_Adj_%'] = df_weekly['DC_corrected_WA'] / df_weekly['DC_corrected_PVsyst_WA']
        df_weekly['Weather_KWh'] = df_weekly['POI Output (kWh)'].multiply(df_weekly['NREL_Weather_Adj_%'])
        
        #  Calculate Percentages for Dashboard
        df_weekly['Inv_Ava_%'] = df_weekly['Meter_Corrected_2'].div(df_weekly['Meter_&_ava']).fillna(1)
        df_weekly['Grid_Ava_%'] = df_weekly['Meter_&_ava'].div(df_weekly['Meter_&_ava_&_grid']).fillna(1)
        df_weekly['Snow_Adj_%'] = df_weekly['Meter_&_ava_&_grid'].div(df_weekly['Meter_losses&snow']).fillna(1)
        df_weekly['Plant_Perf_%'] = df_weekly['Meter_losses&snow'].div(df_weekly['Weather_KWh']).fillna(0).replace(np.inf, 1).replace(-np.inf, 1)

        # Select appropriate columns
        df_weekly = df_weekly[['POI Output (kWh)','Meter_Corrected_2','Meter_&_ava',
                               'Meter_&_ava_&_grid', 'Meter_losses&snow', 'Weather_KWh',
                               'NREL_Weather_Adj_%', 'Inv_Ava_%', 'Grid_Ava_%', 'Snow_Adj_%', 'Plant_Perf_%']]

        # Build filepath
        week_folder = os.path.join(self.dashboard_dir, 'Python_Functions', 'Other Scripts', 'Weekly reporting', 'results', self.project_name)
        weekly_filepath = os.path.join(week_folder, self.data_source + '.csv')

        if self.data_platform == 's3':
            weekly_filepath = Path(weekly_filepath).as_posix().replace('s3:/', 's3://')
        
        if server != 'prod':
            weekly_filepath = weekly_filepath.replace('.csv', '_COPY.csv')
            df_weekly.to_csv(weekly_filepath)
            s3_filepath = make_s3_filepath(weekly_filepath, obj_type='file')
            s3_client.delete_object(Bucket=s3_filepath.bucket, Key=s3_filepath.key)
        else:
            df_weekly.to_csv(weekly_filepath)
   
    
    def _export_snow(self, **kwargs) -> None:
        """
        Exports [snow_data][ccrenew.dashboard.project.Project.snow_data] and
        [snow_coverage][ccrenew.dashboard.project.Project.snow_coverage] dataframes to S3.
        
        Args:
            server (str): Snow data will only be exported if `server` == `prod`.
        """
        server = kwargs.get('server')

        # Only export when running in prod
        if server == 'prod':
            folder = f's3://perfdatadev.ccrenew.com/snow_projects/{self.project_name}'
            snow_data_filename = f'{self.data_source}snow_data_project.csv'
            snow_coverage_filename = f'{self.data_source}snow_coverage_project.csv'
            df_tools.write_to_s3(self.snow_data, folder, snow_data_filename, index=True)
            df_tools.write_to_s3(self.snow_coverage, folder, snow_coverage_filename, index=True, header=False)

    
    def _export_bool(self, **kwargs) -> None:
        """
        Export the bool file for the project.

        Args:
            server (str): `prod` will update the BOOL file in the `Plant_Config_File` directory of the project's
                [project_directory][ccrenew.dashboard.project.Project.project_directory].
                `dev` will create a temporary file to test the export functionality then delete it.
        """
        server = kwargs.get('server')

        # Update bool file
        self._update_bool()

        if server != 'prod':
            if self.data_platform == 's3':
                filepath = self.bool_filepath.replace('.csv', '_COPY.csv')
                s3_filepath = make_s3_filepath(filepath, obj_type='file')
                self.df_bool.to_csv(filepath)
                s3_client.delete_object(Bucket=s3_filepath.bucket, Key=s3_filepath.key)
            else:
                dev_filepath = self.bool_filepath.replace('.csv', '_COPY.csv')
                self.df_bool.to_csv(dev_filepath)
                os.remove(dev_filepath)
        else:
            self.df_bool.to_csv(self.bool_filepath)


    def _update_bool(self) -> None:
        """
        Generate bool data if bool file is not available.
        """
        # Load new production data if available & export to `powertrack_csv`
        self.load_production_data()
        self.__config_column_fix()

        # Set reference to sensor columns
        temp_cols = self.col_ref['Temp_cols']
        wind_cols = self.col_ref['Wind_cols']
        weather_cols = self.col_ref['Weather_cols']
        poa_cols = self.col_ref['POA_cols']
        sensor_cols = self.col_ref['Sensor_cols']

        # Subset sensor data to everything after the publish date
        df_sensors = self.df.query("index.dt.date > @self.publish_date").reindex(columns=sensor_cols).copy()

        # Store sensor data in the project object for the whole history
        self.df_sensors = self.df.reindex(columns=sensor_cols)
        if df_sensors.empty:
            return

        # Assign certain columns to appropriate dfs
        df_weather = df_sensors[weather_cols]
        df_poa = df_sensors[poa_cols]
        df_poa_w_sol = df_poa.join(self.df_solcast[['POA_avg', 'GHI_avg']].rename(columns={'POA_avg': 'Solcast POA',
                                                                                           'GHI_avg': 'Solcast GHI'}))

        # Apply data determination steps
        # Find all values reporting NaN
        comms = det.comms(df_sensors)

        # Find all values reporting outside the supplied band
        band_pass = det.band_pass(df_sensors, [(temp_cols, (-30, 120)),
                                              (wind_cols, (0, 67)),
                                              (poa_cols, (0, 1800))]
                                            )
        # Find all frozen values - separate POA from weather to ignore nighttime values for POA
        frozen_window_size = 3
        frozen_weather = det.frozen(df=df_weather, window=frozen_window_size)
        frozen_poa = det.daylight_frozen(df=df_poa, pv_model=self.pv_model, window=frozen_window_size) # type: ignore

        # Find all zeroes during daylight hours for POAs
        zeroes_poa = det.daylight_zeroes(df=df_poa, pv_model=self.pv_model)
        
        # Find trackers that aren't tracking
        if self.Tracker_site:
            tracker_poa, datasub_stats = det.daylight_poa_mistracking(df=df_poa_w_sol, pv_model=self.pv_model, add_sparklines=False, degree=8) # type: ignore
            poa = frozen_poa+zeroes_poa+tracker_poa
        else:
            poa = frozen_poa+zeroes_poa

        # We'll come back to implement some more complex logic later
        # spline_filter = det.spline_filter(df_sensors)

        # Combine the comms & band pass dfs
        df_bool = comms+band_pass

        # Add frozen weather values
        df_bool[weather_cols] = df_bool[weather_cols] + frozen_weather

        # Add POA columns
        poa = poa.reindex(index = df_bool.index).fillna(False)
        df_bool[poa_cols] = df_bool[poa_cols] + poa
        
        # Set `self.df_bool` equal to calculated bool if empty. Update if exists.
        if self.df_bool.empty:
            self.df_bool = ~df_bool
        else:
            # Update column order of self.df_bool to Tamb-Tmod-Wind-POA
            # Add rows to self.df_bool if df_bool has more dates since df.update only works as a left join
            self.df_bool = self.df_bool.reindex(columns = df_bool.columns, index=df_bool.index)
            self.df_bool.update(~df_bool, overwrite=True)
        
        self.df_bool = self.df_bool.astype(bool)


    def _process_data(self, neighbor_sensor_data:dict, datasub:bool, use_solcast:bool):
        """Processes data for the project"""
        # TODO: update for reprocessing only to run the methods that update the required data

        print('Processing data for {}'.format(self.project_name))
        # Update df_sensor_ON based on config file
        self._config_disable_sensors()

        # Configure PVSyst
        self.__pvsyst_adjustments()

        # Calculate monthly
        self.__calculate_monthly()

        # Fix columns before data gets used anywhere
        self.__config_column_fix()

        # Find sensor anomalies based on simple hard-coded rules
        self.__find_sensor_anomalies()

        self.df = self.df.fillna(0)

        # Correct POI data for battery sites
        if self.Battery_AC_site:
            self.__correct_poi()

        # Correct meter data using `Correct_Meter_data_v08_smartercheck.Correct_Meter_with_Inv_data_v01`
        self.__correct_meter_data()
    
        # Calculate averages for the sensors on the site using `df_sensor_ON`
        self.__config_sensor_average_updates()

        # Calculate averages for the native sensors using bool file
        self._calculate_native_sensor_averages()

        # Perform data substitution based on bool file & available neighbor sensors
        if self.year >= 2023 and datasub:
            self._calculate_datasub_sensor_averages(neighbor_sensor_data, use_solcast=use_solcast)

        # These next ones are pretty self explanatory
        self.__calculate_tcell()
        self.df = self.df.fillna(0)
        self.__calculate_availability()
        self.__calculate_snow_data()
        self.__calculate_PR()
        self.__calculate_losses()
        self.__calculate_revenue('initial')
        self.__calculate_weather_adjustments()
        self.__calculate_revenue('weather_adjusted')
        self.__calculate_dashboard_percentages()
        self.__verify_performance()

        # Calculate metrics for diagnostics
        self.__calculate_project_metrics()


    def _config_disable_sensors(self):
        """
        This function manipulates df_sensor_ON to change when a field should be used in future calculations
        Args:
            sensor_OFF: df of the sensor offline sheet of the config file
            df_sensor_ON: df of all the possible fields in the data. True, False or, Negative POA, or Not updating    
        """
        # This first line is a hacky way to get some config lines to work when you want to turn off a sensor before or after a certain hour
        # E.g. if you have shading in the morning or afternoon
        # We just end up deleting it after this for loop but it's needed in rare cases
        # I know you want to remove it, just don't
        self.df_sensor_ON['Hour'] = self.df_sensor_ON.index.hour

        # Loop through Sensor OFF sheet in the config file & turn off designated sensors
        ignore_ids = ["grid", "curtailment", "site ava", "column fix", "weather fix"]
        for i, row in self.sensor_OFF.query("Var_ID not in @ignore_ids").iterrows():
            sensor = row['Var_ID']
            s = row['start date']
            e = row['end date']

            # Set dates with -1 to last date in df
            if (e == -1) | (e == pd.to_datetime('1899-12-30')):
                e = self.df.index[-1]
            
            if str(row['#']).lower() == 'eval':
                # This is where we do that silly hack listed above the for loop to turn off certain hours
                filter = self.df_sensor_ON[self.df_sensor_ON.eval(row['description']) & (self.df_sensor_ON.index >= s) & (self.df_sensor_ON.index <= e)].index
            else:
                filter = self.df_sensor_ON[(self.df_sensor_ON.index >= s) & (self.df_sensor_ON.index <= e)].index
        
            self.df_sensor_ON.loc[filter, sensor] = False
            if sensor in self.col_ref['POA_cols']:
                self.df.loc[filter, 'POA_source'] = 'Config'

        # And now remove the 'Hour' column
        self.df_sensor_ON = self.df_sensor_ON.drop('Hour', axis=1)


    def __pvsyst_adjustments(self):

        # Add Tcell column. The function is in the weather adjusted function that are imported at the top of the script.
        self.df_Pvsyst['Tcell'] = weather.generate_Tcell(self.df_Pvsyst['POA (W/m2)'],
                                                 self.df_Pvsyst['Ambient Temperature'],
                                                 self.df_Pvsyst['Wind Velocity (m/s)'],
                                                 self.a_module,
                                                 self.b_module,
                                                 self.Delta_Tcnd)

        # Calculate average cell temperature for the year
        # (See NREL paper here: https://www.nrel.gov/docs/fy13osti/57991.pdf)
        Gpoa_x_Tcell = self.df_Pvsyst['POA (W/m2)'].values * self.df_Pvsyst['Tcell'].values
        self.Tcell_typ_avg = np.sum(Gpoa_x_Tcell) / self.df_Pvsyst['POA (W/m2)'].sum()

        # For PVsyst we need to shift the columns to adjust for DST.
        # It also deletes the last value. It is from the following year
        (self.df_Pvsyst_2, _,
        self.rates_year, self.normal_rate_flag) = rates.generate_Rate_column(self.project_name,
                                                                             self.config_filepath,
                                                                             shift_DST=None,
                                                                             year=self.year,
                                                                             data_platform=self.data_platform)
        self.df_Pvsyst_2 = self.df_Pvsyst_2.iloc[:-1, :]
        self.rates_year = self.rates_year.iloc[:-1, :]

        # Also need to remove Feb 29, to match PVsyst file.
        self.df_Pvsyst_2 = self.df_Pvsyst_2[~((self.df_Pvsyst_2.index.month == 2) & (self.df_Pvsyst_2.index.day == 29))]

        # Adjust df_Pvsyst index to match the year that we're running
        # (the year in the config file may be in the past, when the 8760 was generated)
        self.df_Pvsyst.index = self.df_Pvsyst_2.index

        # Insert Pvsyst degradation before calculating rates and PR. Not needed before weather corrected function
        # Set pvsyst datastart to January first regardless of AE dataset start
        PVsyst_start = datetime(int(self.df.index.year[0]), 1, 1)
        Deg_months = (PVsyst_start.year - self.PIS_date.year) * 12 + PVsyst_start.month - self.PIS_date.month

        if Deg_months > 0:  # site turned on last year
            Deg_array = np.arange(0, 40*12, 1/12.0)[Deg_months:Deg_months+12]
        else:  # site turned on this calandar year or in the future
            if Deg_months < -12:
                Deg_array = np.zeros(12)
            else:
                Deg_months = Deg_months*-1
                Deg_array = np.arange(0, 1, 1/12.0)[:(12-Deg_months)]
                Deg_array = list(Deg_array)
                Deg_array = list(np.arange(Deg_months)*0) + Deg_array

        # Create montly degradation profile based on linear interporlation of yearly deg factors
        Deg_Pvsyst = np.interp(Deg_array, self.Deg.index, self.Deg['Capacity'].values)

        # Create column for non-derated values
        self.df_Pvsyst['kWh_ORIGINAL'] = self.df_Pvsyst['Year 0 Actual Production (kWh)']

        # Initialize derate column
        self.df_Pvsyst['Degradation_Derate'] = 1

        # Set monthly degredation factor from linear interp above
        for i in range(1, 13):
            self.df_Pvsyst.loc[self.df_Pvsyst.index.month == i, 'Degradation_Derate'] = Deg_Pvsyst[i-1]
        self.df_Pvsyst['Year 0 Actual Production (kWh)'] = \
            self.df_Pvsyst['Year 0 Actual Production (kWh)'].multiply(self.df_Pvsyst['Degradation_Derate'])

        # Calculate temperature corrected DC energy based on NREL paper
        self.df_Pvsyst = weather.calculate_DC_Corrected_PVsyst(
                                                       self.df_Pvsyst,
                                                       self.Pstc_KW,
                                                       self.Gstc,
                                                       self.Temp_Coeff_Pmax,
                                                       self.Tcell_typ_avg,
                                                       self.clipping_KW)

        # also apply degradation to gen_no_clipping
        self.df_Pvsyst['Gen_NO_Clipping_PVsyst'] = self.df_Pvsyst['Gen_NO_Clipping_PVsyst'].multiply(self.df_Pvsyst['Degradation_Derate'])

        col_pvsyst = [i for i in self.df_Pvsyst.columns if i.lower() not in ('month', 'day', 'hour')]

        self.df_Pvsyst_2 = pd.concat([self.df_Pvsyst_2, self.df_Pvsyst[col_pvsyst]], axis=1)
        self.df_Pvsyst_2['POA_weighted_Tcell'] = self.df_Pvsyst['Tcell'] * self.df_Pvsyst_2['POA (W/m2)']

        if self.Battery_AC_site:
            PVsyst_degradation_hours = (datetime(self.year, 1, 1) - self.PIS_date).total_seconds() / 3600
            df_battery = batt.Run_AC_Batt(self.df_Pvsyst_2['Year 0 Actual Production (kWh)'], self.df_Pvsyst_2['Rates'], PVsyst_degradation_hours)

            df_battery_pp = batt.AC_Batt_PP(self.df_Pvsyst_2, df_battery)

            self.df_Pvsyst_2['POI Output (kWh)'] = df_battery_pp['POI_no_night']
            self.df_Pvsyst_2['POI_ORIGINAL'] = self.df_Pvsyst_2['POI Output (kWh)']
        else:
            self.df_Pvsyst_2['POI_ORIGINAL'] = self.df_Pvsyst_2['kWh_ORIGINAL']
            self.df_Pvsyst_2['POI Output (kWh)'] = self.df_Pvsyst_2['Year 0 Actual Production (kWh)']

        # Calculate flat payments/fees
        self.df_Pvsyst_2['Revenue_IE_P50'] = \
            self.df_Pvsyst_2['Year 0 Actual Production (kWh)'].multiply(self.df_Pvsyst_2['Rates'], axis="index") + self.df_Pvsyst_2['Flat']
        self.df_Pvsyst_2['Revenue_IE_POI'] = \
            self.df_Pvsyst_2['POI Output (kWh)'].multiply(self.df_Pvsyst_2['Rates'], axis="index") + self.df_Pvsyst_2['Flat']


    def __calculate_monthly(self):
        # Calculate monthly DF
        self.df_Pvsyst_2_month = self.df_Pvsyst_2.resample('M').sum()
        self.df_Pvsyst_2_month['POA_weighted_Tcell'] /= self.df_Pvsyst_2_month['POA (W/m2)']
        self.df_Pvsyst_2_month['Blended_Rate'] = self.df_Pvsyst_2_month[['Revenue_IE_P50']].div(self.df_Pvsyst_2_month['Year 0 Actual Production (kWh)'].replace(0, np.nan), axis="index")
        self.df_Pvsyst_2_month['Blended_POI_rate'] = self.df_Pvsyst_2_month[['Revenue_IE_POI']].div(self.df_Pvsyst_2_month['Year 0 Actual Production (kWh)'].replace(0, np.nan), axis="index")
        self.df_Pvsyst_2_month['PR_IE_P50'] = self.df_Pvsyst_2_month[['Year 0 Actual Production (kWh)']].div(self.df_Pvsyst_2_month['DC_corrected_PVsyst'].replace(0, np.nan), axis="index")
        self.df_Pvsyst_2_month['PR_IE_P50_PR'] = self.df_Pvsyst_2_month[['Gen_NO_Clipping_PVsyst']].div(self.df_Pvsyst_2_month['DC_corrected_PVsyst_PR'].replace(0, np.nan), axis="index")
        
  
    def __config_column_fix(self):
        '''
        this function, added 12/10/2020 (and some time after, sorry I'm slow),
        intends to provide an option to alter the AE file from the config file.
        Options here include allowing for setting 1 column equal to the sum of others,
        doing a dif on the cumulative meter or building a cumulative from a power column.
        To do "trip" this function put "column fix" in the Var_ID column on sensor offline page
        '''
        # Loop through rows in the Sensor_Offline sheet of the config file
        for i, row in self.sensor_OFF.iterrows():
            option = row['Var_ID']
            end_date = row['end date']
            end_date = self.df.index[-1] if end_date == -1 else end_date
            if pd.to_datetime(end_date) > self.df.index[-1]:
                end_date = str(self.df.index[-1])
            func_choice = row['#']
            func_outcome = row['description']
            start_date = row['start date']

            if option.lower() not in ['column fix', 'weather fix']:
                continue
            if self.df.index[0].year in set(pd.date_range(start_date, end_date, freq='d').year):
                if start_date.year != self.df.index[0].year:
                    # set s to start of current year if before current year
                    start_date = self.df.index[0]

                if option.lower() == 'column fix':
                    if func_choice.lower() == 'eval':
                        # do simple eval functions
                        # this(needing df_temporary on all these) is hacky and I hate it,
                        # but it wasn't working doing an inplace=True on a loc version of df. so this works

                        # .eval using basic arithmetic functions, because of that when there is a NaN value,
                        # it fails to do the eval. need to fillna(0) during the temporary
                        df_temp2 = self.df.copy()
                        columns =  [func_outcome.split('=')[0].strip()] + [col.strip() for col in func_outcome.split('=')[1].split('+')]
                        for column in columns:
                            try:
                                df_temp2[column] = df_temp2[column].fillna(0)
                            except:
                                continue

                        # do the eval
                        try:
                            df_temporary = df_temp2.eval(func_outcome)
                        except (RuntimeError, ValueError):
                            df_temporary = df_temp2.eval(func_outcome, engine='python')

                        # change only the desired column so the rest is not changed from NaN
                        self.df.loc[start_date:end_date, func_outcome.split('=')[0].strip()] = df_temporary[func_outcome.split('=')[0].strip()].loc[start_date:end_date]

                    elif func_choice.lower() == 'dif_cum':
                        # Will do this by creating a net_meter.shift(1) column.
                        # Dif in cumulative is then net_meter-net_meter_shift.
                        # Delete net_meter_shift afterwards
                        # FOR SOME REASON "s" IS READ AS error.225 INSTEAD OF THE DATE. IT WORKS WHEN RUN LINE BY LINE SO IDK WHAT IS HAPPENING
                        df_temporary = self.df.copy()
                        fix_column_split = func_outcome.split(',')

                        # Cum column
                        fix_column = fix_column_split[1]
                        # Power column
                        func_outcome = fix_column_split[0]

                        # Shift column
                        shift_column = fix_column + '_shifted'
                        df_temporary[shift_column] = df_temporary[fix_column].shift(1)
                        df_temporary[func_outcome] = \
                            df_temporary[fix_column] - df_temporary[shift_column]

                        # Set to NAN if the cumulative or the shift cumulative column is missing
                        df_temporary.loc[df_temporary[fix_column].isnull(), func_outcome] = df_temporary[fix_column]
                        df_temporary.loc[df_temporary[shift_column].isnull(), func_outcome] = df_temporary[shift_column]
                        df_temporary = df_temporary.drop(columns=shift_column)
                        self.df.loc[(self.df.index >= start_date) & (self.df.index <= end_date)] = \
                            df_temporary.loc[(df_temporary.index >= start_date) & (df_temporary.index <= end_date)]

                    elif func_choice.lower() == 'build_cum':
                        fix_column_split = func_outcome.split(',')
                        fix_column = fix_column_split[1]
                        func_outcome = fix_column_split[0]

                        if pd.isna(self.df[fix_column].loc[start_date]):
                            print('''-------------
                            SELECTED START DATE {} FOR BUILDING CUMULATIVE METER IS NAN. 
                            CHOOSE NEW DATE IN CONFIG
                            --------------'''.format(start_date))
                            self.df[fix_column].loc[start_date:].fillna(0)
                        df_temporary = self.df[fix_column].fillna(
                            0).loc[start_date] + self.df[func_outcome].loc[start_date:].fillna(0).cumsum()

                        self.df.loc[start_date:end_date, fix_column] = df_temporary.loc[start_date:end_date]

                elif option.lower() == 'weather fix':
                    fix_type = func_choice.lower()
                    if fix_type == 'tran_ghi': 
                        print('Using Solcast GHI Transposed to POA')
                        try:
                            self.df['POA_1'][(self.df.index >= start_date) & (self.df.index <= end_date)] = self.df_solcast['proj_ghi_poa'][start_date:end_date]
                        except KeyError:
                            raise Exception('Unable to transpose GHI for {}. Please review project or update config file and run again.'.format(self.project_name))
                        except ValueError as e:
                            raise Exception(f'Error pulling Solcast data for {self.project_name}: {e}')
                        
                    elif fix_type == 'sat_poa': 
                        print('Using Solcast POA')
                        try:
                            self.df['POA_1'][(self.df.index >= start_date) & (self.df.index <= end_date)] = self.df_solcast['sat_poa'][start_date:end_date]
                        except ValueError as e:
                            raise Exception(f'Error pulling Solcast data for {self.project_name}: {e}')
                        
                    elif fix_type == 'sat_tamb': 
                        print('Using Solcast Ambient Temp')
                        try:
                            self.df['Tamb_1'][(self.df.index >= start_date) & (self.df.index <= end_date)] = self.df_solcast['Tamb_avg'][start_date:end_date]
                        except ValueError as e:
                            raise Exception(f'Error pulling Solcast data for {self.project_name}: {e}')
                        
                    elif fix_type == 'sat_tmod': 
                        print('Using Solcast Ambient Temp and Wind to make Tmod')
                        try:
                            self.df['Tmod_1'][(self.df.index >= start_date) & (self.df.index <= end_date)] = self.df_solcast['Tmod_avg'][start_date:end_date]
                        except ValueError as e:
                            raise Exception(f'Error pulling Solcast data for {self.project_name}: {e}')
                        
                    elif fix_type == 'sat_wind': 
                        print('Using Solcast Wind Speed')
                        try:
                            self.df['Wind_speed_1'][(self.df.index >= start_date) & (self.df.index <= end_date)] = self.df_solcast['Wind_speed'][start_date:end_date]
                        except ValueError as e:
                            raise Exception(f'Error pulling Solcast data for {self.project_name}: {e}')

            else:
                continue  # this continues if s and e both occur in a previous year

 
    def __find_sensor_anomalies(self):
        #   Add function to find sensors with anomalies
        for s in self.pos_Temperature:
            self.df_sensor_ON.loc[self.df[s].isnull(), [s]] = "Missing data NAN"
            # 0 deg is clear sign sensor is broken for deg F
            self.df_sensor_ON.loc[self.df[s] <= -30, [s]] = "Negative Temp"
            # set unreasonabley high temp. Usual max is 150 deg F
            self.df_sensor_ON.loc[self.df[s] > 120, [s]] = "Too high Temp"
            # added by Saurabh on 4/11/18
            self.df_sensor_ON.loc[((self.df[s].diff(1) == 0) & (self.df[s].diff(-1) == 0)), [s]] = 'Not Updating'
            # create flag column that allows for easier numerical 1/0 indexing
            aux = self.df_sensor_ON[[s]] == 'Not Updating'
            rolling_indices = aux[s].rolling(window=3, center=True, min_periods=1).sum() > 0
            self.df_sensor_ON.loc[rolling_indices, [s]] = 'Not Updating'

        for s in self.pos_Wind:
            self.df_sensor_ON.loc[self.df[s].isnull(), [s]] = "Missing data NAN"
            # less than 0 not possible for wind sensor
            self.df_sensor_ON.loc[self.df[s] < 0, [s]] = "Negative Wind"
            # set unreasonable ceiling for m/s
            self.df_sensor_ON.loc[self.df[s] > 67, [s]] = "Too High above 67 m/s"

        for s in self.pos_POA:
            self.df_sensor_ON.loc[self.df[s].isnull(), [s]] = "Missing data NAN"
            # less than 0 not possible for POA
            self.df_sensor_ON.loc[self.df[s] < 0, [s]] = "Negative POA"
            # set unreasonable ceiling for W/m2
            self.df_sensor_ON.loc[self.df[s] > 1800, [s]] = "Too high - above 1800"
            # added by Saurabh on 4/11/18
            self.df_sensor_ON.loc[((self.df[s].diff(1) == 0) & (self.df[s].diff(-1) == 0)), [s]] = 'Not Updating'
            # create flag column that allows for easier numerical 1/0 indexing
            aux = self.df_sensor_ON[[s]] == 'Not Updating'
            rolling_indices = aux[s].rolling(window=3, center=True, min_periods=1).sum() > 0
            self.df_sensor_ON.loc[rolling_indices, [s]] = 'Not Updating'

        for s in self.pos_GHI:
            self.df_sensor_ON.loc[self.df[s].isnull(), [s]] = "Missing data NAN"
            # less than 0 not possible for POA
            self.df_sensor_ON.loc[self.df[s] < 0, [s]] = "Negative GHI"
            # set unreasonable ceiling for W/m2
            self.df_sensor_ON.loc[self.df[s] > 1800, [s]] = "Too high - above 1800"

        for s in self.pos_Meter:  # Need to do the meter fix function before any of this checking
            self.df_sensor_ON.loc[self.df[s] > self.clipping_KW * 1.2, [s]] = "Over nameplate threshold"
            self.df_sensor_ON.loc[self.df[s] < self.clipping_KW * - 0.02, [s]] = "Below negative 2% threshold"
            self.df_sensor_ON.loc[self.df[s].isnull(), [s]] = "Missing data NAN"

        for s in self.pos_POI_Meter:
            self.df_sensor_ON.loc[self.df[s] > self.clipping_KW * 2.1, [s]] = "Way over nameplate threshold"
            self.df_sensor_ON.loc[self.df[s] < self.clipping_KW * - 0.02, [s]] = "Below negative 2% threshold"
            self.df_sensor_ON.loc[self.df[s].isnull(), [s]] = "Missing data NAN"

        for s in self.pos_Meter_Cum + self.pos_POI_Meter_Cum:
            self.df_sensor_ON.loc[self.df[s].isnull(), [s]] = "Missing data NAN"

        for s in self.pos_Inv:
            self.df.loc[self.df[s] < 0, [s]] = 0  # inverters should not display below 0
            
    
    def __correct_poi(self):
        # TODO: update this error log deal to use logging module
        df_POI_ok, draker_flags, error_log = \
            poi.Correct_POI_data_v01(self.df,
                                     self.pos_POI_Meter,
                                     self.pos_POI_Meter_Cum,
                                     self.df_Pvsyst_2,
                                     self.clipping_KW,
                                     self.df_sensor_ON)
        df_POI_ok = df_POI_ok.clip(lower=0)
        self.df_POI_ORIGINAL = self.df[self.pos_POI_Meter + self.pos_POI_Meter_Cum]
        self.df_POI_ORIGINAL.rename(columns=lambda x: x+'_ORIGINAL', inplace=True)
        df_POI_ok.rename(columns=lambda x: x[:-3], inplace=True)
        self.df = self.df.drop(self.pos_POI_Meter, 1)

        #  add Original POI and Corrected one
        self.df = pd.concat([self.df, self.df_POI_ORIGINAL, df_POI_ok], axis=1, join='inner')
        self.df['POI_Corrected_2'] = self.df[self.pos_POI_Meter].sum(axis=1)
        

    def __correct_meter_data(self):
        if self.project_name in ['Innovative Solar 6, LLC', 'Colchester', 'Franklin', 'Morgan Solar 2']:
            import ccrenew.dashboard.data_processing.Correct_Meter_data_v08_IS6 as meter_alt
            df_Meter_OK, self.draker_flags, error_log = \
                meter_alt.Correct_Meter_with_Inv_data_v01(self.df,
                                                          self.pos_Meter,
                                                          self.pos_Meter_Cum,
                                                          self.clipping_KW,
                                                          self.df_sensor_ON)
        else:
            df_Meter_OK, self.draker_flags, error_log = \
                meter_correct.Correct_Meter_with_Inv_data_v01(self.df,
                                                              self.pos_Meter,
                                                              self.pos_Meter_Cum,
                                                              self.clipping_KW,
                                                              self.df_sensor_ON)

        # TODO: update this error log deal to use logging module
        # error_log.loc[:, [u'Site_name', u'year']] = [self.project_name, self.year]
        # error_master = error_master.append(error_log)

        # Create new columns in main df to delineate original vs corrected meter values
        self.df_Meter_ORIGINAL = self.df[self.pos_Meter + self.pos_Meter_Cum]
        self.df_Meter_ORIGINAL.rename(columns=lambda x: x+'_ORIGINAL', inplace=True)
        self.pos_Meter_ORIGINAL = [s for s in self.df_Meter_ORIGINAL.columns if 'Meter_kw_' in s]
        self.pos_Meter_Cum_ORIGINAL = [s for s in self.df_Meter_ORIGINAL.columns if 'Meter_kwhnet_' in s]

        df_Meter_OK.rename(columns=lambda x: x[:-3], inplace=True)
        self.df = self.df.drop(self.pos_Meter, 1)
        #  add Original Meter and Corrected one
        self.df = pd.concat([self.df, self.df_Meter_ORIGINAL, df_Meter_OK], axis=1, join='inner')
        #  remove changed values from PR calculation
        self.Meter_delta = np.subtract(self.df[self.pos_Meter], self.df_Meter_ORIGINAL[self.pos_Meter_ORIGINAL]).sum(axis=1)

        # remove off hours after meter delta
        for s in self.pos_Meter:
            self.df.loc[self.df[s] < 0, s] = 0

        # Sum Meters
        # QUESTION: Is there a reason we aren't using `df_sensor_ON` here like for the cum meters?
        # NOTE: leave as is
        aux = self.df[self.pos_Meter].sum(axis=1)
        self.df['Meter'] = aux.values

        # Sum Cum Meters
        aux = self.df[self.pos_Meter_Cum][self.df_sensor_ON[self.pos_Meter_Cum] == True].sum(axis=1)
        self.df['Meter_cum'] = aux.values

        # check if the cum meter is calculated with 2 or more sensors.
        # identify when one sensor is bad and corrects accordingly.
        # Actually this is wrong & only sets the cum meter sum to a single meter & is overwritten anyways
        # if len(self.pos_Meter_Cum) > 1:
            # self.__correct_multiple_cum_meters()

        # For single inverter sites set meter = inverter if meter is zero & vice-versa
        if len(self.pos_Inv) == 1:
            self.df.loc[(self.df[self.pos_Inv[0]] == 0) & (self.df[self.pos_Meter[0]] > 0), self.pos_Inv[0]] = self.df[self.pos_Meter[0]]
            self.df.loc[(self.df[self.pos_Meter[0]] == 0) & (self.df[self.pos_Inv[0]] > 0), self.pos_Meter[0]] = self.df[self.pos_Inv[0]]


    def __config_sensor_average_updates(self):
        # Average POA sensors
        aux = self.df[self.pos_POA][self.df_sensor_ON[self.pos_POA] == True].mean(axis=1)
        self.df['POA_avg'] = aux.values

        # Average GHI sensors
        aux = self.df[self.pos_GHI][self.df_sensor_ON[self.pos_GHI] == True].mean(axis=1)
        self.df['GHI_avg'] = aux.values

        # Average wind speed sensors in m/s. (Also Energy gives wind speed in Km/h)
        aux = self.df[self.pos_Wind][self.df_sensor_ON[self.pos_Wind] == True].mean(axis=1)
        self.df['Wind_speed'] = aux.values

        # Average Tamb sensors
        aux = self.df[self.pos_Tmod][self.df_sensor_ON[self.pos_Tmod] == True].mean(axis=1)
        self.df['Tmod_avg'] = aux.values

        # Average Tamb sensors
        aux = self.df[self.pos_Tamb][self.df_sensor_ON[self.pos_Tamb] == True].mean(axis=1)
        self.df['Tamb_avg'] = aux.values


    def _calculate_native_sensor_averages(self):
        """
        Calculate average values for native sensors based on bool file.
        """
        native_col_groups = [zip(tup.col_list, itertools.repeat(tup.col_avg)) for tup in self.sensor_colmap]
        native_col_dict = {key: val for items in native_col_groups for key, val in items}

        df_bool_nan = self.df_bool.replace(False, np.nan)
        try:
            native_df = self.df[self.df_bool.columns]*df_bool_nan
        except KeyError:
            print(f"*** WARNING: {self.project_name} {str(sys.exc_info()[1]).replace(' not in index', '')} exists in BOOL file but not in Powertrack file. Please updated BOOL file to ensure consistent columns.")
            consistent_cols = self.df_bool.columns.intersection(self.df.columns)
            self.df_bool = self.df_bool.reindex(columns=consistent_cols)
            df_bool_nan = df_bool_nan.reindex(columns=consistent_cols)
            native_df = self.df[self.df_bool.columns]*df_bool_nan

        self.df_sensors_native_avg = native_df.groupby(native_col_dict, axis=1).mean()


    def _calculate_datasub_sensor_averages(self, neighbor_sensor_avgs: dict = {}, use_solcast=False):
        """
        Calculate sensor averages based on bool file.

        Args:
            neighbor_sensor_avgs: Dict of neighbor name & sensor average df pairs.
            get_solcast: Option to query Athena for solcast data to use in data sub.
        """
        if self.df_sensors_native_avg.empty:
            self._calculate_native_sensor_averages()
        df_sensors_avg = self.df_sensors_native_avg.copy()

        # Add any columns for sensors that are missing, i.e. if a project doesn't have a wind sensor
        # This will add a column of nans to be filled in with neighbor or solcast
        avg_cols = [col.col_avg for col in self.sensor_colmap]
        df_sensors_avg = df_sensors_avg.reindex(columns=avg_cols)

        # Exclude any rows that were changed in the config file
        try:
            # First exclude any rows that where the native sensors were turned off
           df_sensors_avg = df_sensors_avg[self.df['POA_source'] != 'Config']
        except KeyError:
            pass

        # Next exclude any rows where a neighbor was turned on
        neighbor_poa_cols = list(np.setdiff1d(self.pos_POA, self.col_ref['POA_cols']))
        neighbor_poa_dates = (self.df_sensor_ON[neighbor_poa_cols] == True).any(axis=1)
        df_sensors_avg = df_sensors_avg.loc[~neighbor_poa_dates]
        self.df.loc[neighbor_poa_dates, 'POA_source'] = 'Config'
        
        # Check if `POA_source` column has assuming all Natives are good until changed
        # The rows where the config file didn't update would be NaN but now they're 0 due to the df.fillna(0) calls
        try:
            self.df['POA_source'] = self.df['POA_source'].replace([0, np.nan], 'Native')
        except KeyError:
            self.df['POA_source'] = 'Native'
        any_nulls = df_sensors_avg.isna().any().any()

        while any_nulls:
            for neighbor_name, df_neighbor_avg in neighbor_sensor_avgs.items():
                # Check if the neighbor satisfies the conditions for using POA
                if self.neighbor_list[neighbor_name]:
                    # Use POA data
                    neighbor_dates = df_sensors_avg[df_sensors_avg['POA_avg'].isnull()].index
                    self.df.loc[neighbor_dates, 'POA_source'] = neighbor_name
                    df_sensors_avg = df_sensors_avg.fillna(df_neighbor_avg)
                else:
                    # Remove POA column if present
                    try:
                        non_poa = df_sensors_avg.drop('POA_avg', axis=1)
                        non_poa = non_poa.fillna(df_neighbor_avg.drop('POA_avg', axis=1))
                    except:
                        non_poa = non_poa.fillna(df_neighbor_avg)
                    df_sensors_avg.update(non_poa)

                any_nulls = df_sensors_avg[avg_cols].isna().any().any()

            # Pull solcast data if specified
            if use_solcast:
                # Update df_sensors_avg with solcast data
                null_dates = df_sensors_avg[df_sensors_avg['POA_avg'].isnull()].index
                solcast_dates = self.df_solcast.index.intersection(null_dates)
                self.df.loc[solcast_dates, 'POA_source'] = 'Solcast'
                df_sensors_avg = df_sensors_avg.fillna(self.df_solcast)
            
            any_nulls = False

        if self.Tracker_site:
            df_poa = self.df.loc[:, self.col_ref['POA_cols']]
            df_poa_w_sol = df_poa.join(self.df_solcast[['POA_avg', 'GHI_avg']].rename(columns={'POA_avg': 'Solcast POA',
                                                                                               'GHI_avg': 'Solcast GHI'}))
            tracker_poa, datasub_stats = det.daylight_poa_mistracking(df=df_poa_w_sol, pv_model=self.pv_model, add_sparklines=False, degree=8) # type: ignore
            tracker_dates = tracker_poa[tracker_poa.all(axis=1)].index
            self.df.loc[tracker_dates, 'POA_source'] = self.df.loc[tracker_dates, 'POA_source'] + ' MT'

        df_sensors_avg = df_sensors_avg.astype(float)
        self.df.update(df_sensors_avg)

    
    def __calculate_tcell(self):
        # Calculate Tcell from ambient temperature & Tcell from module temperature
        self.df['POA_avg'] = self.df['POA_avg'].fillna(0)
        self.df['Tcell_AMB'] = weather.generate_Tcell(self.df['POA_avg'],
                                              self.df['Tamb_avg'],
                                              self.df['Wind_speed'],
                                              self.a_module,
                                              self.b_module,
                                              self.Delta_Tcnd)
        self.df['Tcell_MOD'] = weather.generate_Tcell_from_Tmod(self.df['POA_avg'],
                                                        self.df['Tmod_avg'],
                                                        self.Delta_Tcnd)

        # Fill Tcell using module temp first
        self.df['Tcell'] = self.df['Tcell_MOD']
        # Use Tcell from ambient temp when possible
        self.df.loc[(self.df['Tamb_avg'] > 0) & (self.df['Wind_speed'] > 0), ['Tcell']] = self.df['Tcell_AMB']


    def __calculate_availability(self):
        # System Availability
        self.df['Meter_cum'] = self.df['Meter_cum'].values + self.df['Meter'].values
        pos_Zoneamps = [s for s in self.df.columns if 'Zoneamps' in s]
        meter_cum_corrected = [0]

        # QUESTION: is this the same procedure as calculating the meter corrected for multiple meters? (line 1088 in original file)
        for i in range(1, len(self.df['Meter_cum'])):
            if self.df['Meter_cum'][i] == 0:
                meter_cum_corrected.append(meter_cum_corrected[i-1] + self.df['Meter'][i])
            else:
                meter_cum_corrected.append(self.df['Meter_cum'][i])

        #
        aux2 = pd.DataFrame()
        aux2['Meter_cum_OLD'] = self.df['Meter_cum']
        aux2['Meter_cum_FIXED'] = meter_cum_corrected
        #
        coef_Zoneamps = pd.DataFrame(self.df[pos_Zoneamps].values, columns=pos_Zoneamps)
        coef_Zoneamps_sum = coef_Zoneamps.sum(axis=1)
        #
        coef_AVA = pd.DataFrame()
        coef_AVA = self.df[['Meter', 'Meter_cum']]
        coef_AVA['coef_AVA'] = 0
        coef_AVA.loc[(coef_AVA['Meter'] == 0) & (coef_AVA['Meter_cum'] == 1) & (coef_Zoneamps_sum == 0), 'coef_AVA'] = 1
        #
        aux2['Meter_cum_FIXED_Corrected'] = aux2['Meter_cum_FIXED'].multiply(coef_AVA['coef_AVA'])
        #
        self.df['Meter_cum'] = aux2['Meter_cum_FIXED_Corrected']

        # calculate DAS_ON for ava function using native sensors
        self.df['DAS_ON'] = self.df[self.pos_Native].sum(axis=1)
        self.df.loc[self.df['DAS_ON'] != 0, 'DAS_ON'] = 1

        # Find empty months
        if not self.df_coef.loc[:, self.df_coef.sum() == 0].empty:
            aux = self.df_coef.loc[:, self.df_coef.sum() == 0]
            # Find typical values to replace bad ones
            avg = self.df_coef.loc[:, self.df_coef.sum() != 0].mean(axis=1)

            # Edit months that failed
            for col in aux.columns:
                self.df_coef.loc[:, col] = avg
            print ("Edited ASTM test - no data for months: " + ",".join(aux.columns))
            logging.warn("Edited ASTM test - no data for months: " + ",".join(aux.columns))
            
        self.P_exp = weather.create_ASTM_column(self.df, self.df_coef)

        #  Remove Clipping from the data
        self.P_exp[self.P_exp > self.clipping_KW] = self.clipping_KW
        self.df['P_exp'] = self.P_exp
        self.ava = plant_ava.calculate_inverter_availability_and_loss(self.df, self.df_Pvsyst, self.P_exp)

        ava_col = ['AVA_Energy_loss', 'Meter_&_ava', 'Grid_loss', 'Meter_cum_corrected_2', 'Meter_Corrected_2']
        self.df[ava_col] = self.ava[ava_col]

        cum_meter_offset = self.df_Meter_ORIGINAL.drop(self.pos_Meter_ORIGINAL, 1).sum(axis=1).subtract(self.df['Meter_cum_corrected_2']).median()

        # Add offset value to match meter
        self.df['Meter_cum_corrected_2'] = self.df['Meter_cum_corrected_2'].add(cum_meter_offset)

        if not self.Battery_AC_site:
            self.df['POI_Corrected_2'] = self.df['Meter_Corrected_2']
            self.df['POI_modeled'] = self.df['POI_Corrected_2']
        else:
            degradation_hours = (self.df.index[0] - self.PIS_date).total_seconds() / 3600

            df_battery_meas = batt.Run_AC_Batt(self.df['Meter_Corrected_2'],
                                          self.rates_year.loc[self.df.index, 'Rates'],
                                          degradation_hours)
            df_battery_pp_meas = batt.AC_Batt_PP(self.df, df_battery_meas)
            self.df['POI_modeled'] = df_battery_pp_meas['POI_no_night']

        #  Calculate DC-corrected for ratio of Weather increased
        clipping_Point_DC_corrected_PVsyst = \
            self.df_Pvsyst.loc[self.df_Pvsyst['DC_corrected_PVsyst_PR'] == 0.0, 'DC_corrected_PVsyst_WA'].max()
        self.df = weather.calculate_DC_Corrected(self.df,
                                         'Meter_Corrected_2',
                                         self.Pstc_KW,
                                         self.Gstc,
                                         self.Temp_Coeff_Pmax,
                                         self.Tcell_typ_avg,
                                         clipping_Point_DC_corrected_PVsyst)

        # Calculate Meter including what is lost due to Availability
        self.df['Meter_&_ava'] = self.ava['Meter_&_ava']
        self.df['Meter_&_ava_&_grid'] = self.df['Meter_&_ava'] + self.df['Grid_loss']

        # Manually fix times of grid caused outages
        self.curtailment_flags = []
        for i, row in self.sensor_OFF.loc[self.sensor_OFF['Var_ID'].str.lower() == "curtailment", :].iterrows():
            # date_list = pd.date_range(start = row['start date'], end = row['end date'], freq = 'h')
            date_list = self.df.loc[row['start date']: row['end date'], :].index
            self.df.loc[date_list, 'Meter_&_ava'] = self.df['Meter_Corrected_2']
            # fix grid_loss and ava_energy_loss
            self.df.loc[date_list, 'Grid_loss'] = self.df['AVA_Energy_loss']
            self.curtailment_flags = self.curtailment_flags + list(date_list)

        # Manually fix times where site is down and it's NOT grid outage
        self.loss_swap_flags = []
        for i, row in self.sensor_OFF.loc[self.sensor_OFF['Var_ID'].str.lower() == "site ava", :].iterrows():
            date_list = self.df.loc[row['start date']: row['end date'], :].index
            # turn grid loss to inv ava
            self.df.loc[date_list, 'Meter_&_ava'] = self.df['Meter_&_ava_&_grid']
            self.df.loc[date_list, 'AVA_Energy_loss'] = self.df['Grid_loss']
            self.loss_swap_flags = self.loss_swap_flags + list(date_list)

        self.df['Grid_loss'] = (self.df['Meter_&_ava_&_grid'] - self.df['Meter_&_ava']).clip(lower=0)
        self.df['AVA_Energy_loss'] = ( self.df['Meter_&_ava'] - self.df['Meter_Corrected_2']).clip(lower=0)


    def __calculate_snow_data(self):
        self.snow_data = snow.timeseries(self.raw_snow_df,
                               self.df.index,
                               self.lat,
                               self.lon)

        self.snow_coverage = \
            snow.coverage_v3(self.df,
                        self.snow_data,
                        self.df['Tmod_avg'] - self.df['POA_avg'] * np.exp(self.a_module + self.b_module * self.df['Wind_speed']),
                        self.data_source,
                        self.project_name)
        self.snow_times = self.snow_coverage[self.snow_coverage > 0].index


    def __calculate_PR(self):
        # create expected PR value based on monthly average
        # Resample to start of month
        df_IE = self.df_Pvsyst_2_month['PR_IE_P50'].resample('MS').mean()
        df_IE = df_IE.loc[df_IE.index < self.df.index[-1]]
        df_temporary = pd.Series(df_IE[-1], index=[self.df.index[-1]])
        df_IE = df_IE.append(df_temporary).resample('h').pad()

        # estimate AC kwh based on this ratio
        self.df['P_exp_NREL'] = self.df['DC_corrected'] * df_IE
        self.df.loc[self.df['P_exp_NREL'] > self.clipping_KW, 'P_exp_NREL'] = self.clipping_KW

        # kill ava == 0 spikes on snow days
        self.df.loc[(self.ava['AVA'] == 0) &
            (self.df_sensor_ON[self.pos_Inv] == True).any(axis=1) &
            self.df.index.isin(self.snow_times) &
            (~self.df.index.isin(self.loss_swap_flags)) &
            (self.df['Meter_&_ava'] > self.df['Meter_Corrected_2']), 'Meter_&_ava'] = self.df['Meter_Corrected_2']
        self.df['Meter_&_ava_&_grid'] = self.df['Meter_&_ava'] + self.df['Grid_loss']

        # remove meter adjustments from PR calculation 10/18/16
        # Keep times where meter == inverter sum
        self.Meter_delta[(self.Meter_delta != 0) & np.isclose(self.df['Meter_Corrected_2'], self.ava['Inv_sum'])] = 0

        # remove individual meter corrections
        self.df.loc[(self.Meter_delta != 0), ['DC_corrected_PR', 'Gen_NO_Clipping']] = 0

        # remove draker correction
        self.df.loc[self.draker_flags, ['DC_corrected_PR', 'Gen_NO_Clipping']] = 0

        # remove times designated as curtailment in config file
        self.df.loc[self.curtailment_flags, ['DC_corrected_PR', 'Gen_NO_Clipping']] = 0
        
        # Remove when temperature data is invalid
        self.df.loc[(self.df_sensor_ON[self.pos_Temperature] != True).all(axis=1), ['DC_corrected_PR', 'Gen_NO_Clipping']] = 0


    def __calculate_losses(self):
        self.df['Meter_losses&snow'] = self.df['Meter_&_ava_&_grid']
        self.df.loc[self.snow_times, 'Meter_losses&snow'] = self.P_exp
        self.df.loc[self.df['Meter_losses&snow'] < self.df['Meter_&_ava_&_grid'], 'Meter_losses&snow'] = self.df['Meter_&_ava_&_grid']
        self.df['snow_losses'] = self.df['Meter_losses&snow'] - self.df['Meter_&_ava_&_grid']
        self.df['Meter_losses&snow'] = self.df['Meter_losses&snow'].astype(float)

        # Calculate losses df
        self.losses = self.df[['Meter_Corrected_2']].copy()
        self.losses.loc[:, 'Inv_losses'] = self.df.loc[:, 'Meter_&_ava'] - self.df.loc[:, 'Meter_Corrected_2']
        self.losses.loc[:, 'Grid_losses'] = self.df.loc[:, 'Meter_&_ava_&_grid'] - self.df.loc[:, 'Meter_&_ava']
        self.losses.loc[:, 'Snow_losses'] = self.df.loc[:, 'Meter_losses&snow'] - self.df.loc[:, 'Meter_&_ava_&_grid']


    def __calculate_revenue(self, method):
        def initial_hourly():
            self.rates_year_i = self.rates_year['Rates'][self.df.index[0]:self.df.index[-1]]
            flat_year_i = self.rates_year['Flat'][self.df.index[0]:self.df.index[-1]]
            self.df['Rates'] = self.rates_year_i
            self.df['Energy_Peak'] = self.rates_year['Energy_Peak']
            self.df['Capacity_Peak'] = self.rates_year['Capacity_Peak']
            self.df['Meter_Corrected_2_rev'] = (self.rates_year_i * self.df['Meter_Corrected_2']) + flat_year_i
            self.df['Meter_&_ava_rev'] = (self.rates_year_i * self.df['Meter_&_ava']) + flat_year_i
            self.df['Meter_&_ava_&_grid_rev'] = (self.rates_year_i * self.df['Meter_&_ava_&_grid']) + flat_year_i
            self.df['Meter_losses&snow_rev'] = (self.rates_year_i * self.df['Meter_losses&snow']) + flat_year_i
            self.df['POI_Corrected_2_rev'] = (self.rates_year_i * self.df['POI_Corrected_2']) + flat_year_i
            self.df['POI_modeled_rev'] = (self.rates_year_i * self.df['POI_modeled']) + flat_year_i

        def weather_adjusted_monthly():
            #  Calculate Revenue.
            #  With the NREL method, Revenue due to Weather is calculated with monthly %
            #
            self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj'] = \
                self.df_Pvsyst_2_month['Revenue_IE_POI'].multiply(self.df_Pvsyst_2_month['%_days_month'], axis="index")

            #  Adjust Weather Revenue
            self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj_&_Weather'] = \
                self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj'].multiply(self.df_Pvsyst_2_month['NREL_Weather_Adj_%'], axis="index")

            # make solar version as well
            self.df_Pvsyst_2_month['Revenue_IE_meterOnly_days_adj'] = \
                self.df_Pvsyst_2_month['Revenue_IE_P50'].multiply(
                    self.df_Pvsyst_2_month['%_days_month'], axis="index").multiply(
                        self.df_Pvsyst_2_month['NREL_Weather_Adj_%'], axis="index")
                    
        if method == 'initial':
            initial_hourly()
        if method == 'weather_adjusted':
            weather_adjusted_monthly()

        # TODO: battery POI/meter swap
        if self.Battery_AC_site:
            self.df['POI_kWH'] = self.df['POI_Corrected_2']
            self.df['POI_rev'] = self.df['POI_Corrected_2_rev']

        else:
            self.df['POI_kWH'] = self.df['Meter_Corrected_2']
            self.df['POI_rev'] = self.df['Meter_Corrected_2_rev']
            

    def __calculate_weather_adjustments(self):
        #  Count Days per month showing in Power Track
        day_points_full_year = self.df_Pvsyst['POA (W/m2)'].resample('M').count() / 24.0

        # find the % of the month measured in df, based on POA data per hour
        # Calculate average POA for each month
        aux_pivot = pd.pivot_table(self.df_Pvsyst,
                                    values='POA (W/m2)',
                                    index='Hour',
                                    columns='Month',
                                    aggfunc=np.mean)
        # Calculate total POA for each month
        aux_pivot_sum = pd.pivot_table(self.df_Pvsyst,
                                        values='POA (W/m2)',
                                        index='Month',
                                        aggfunc=np.sum)
        aux_percent = aux_pivot.copy()

        aux_percent = aux_pivot.div(pd.Series(aux_pivot_sum.T.values[0], index=aux_pivot.columns).replace(0, np.nan), axis=1)
        
        # Unpivot dataframe
        stack = aux_percent.T.stack().reset_index().rename(columns={'level_0': 'Month', 0: 'percent_month'})

        # create frame to merge with. Has correct index column which is important
        df_input_index = self.df.index
        df_aux = pd.DataFrame({'Month': df_input_index.month,
                               'Hour': df_input_index.hour},
                                index=df_input_index)
        df_aux['timestamp'] = df_aux.index

        df_merged = pd.merge(df_aux, stack, on=['Month', 'Hour'])
        df_merged.set_index('timestamp', drop=True, inplace=True)

        self.df['percent_month'] = df_merged['percent_month']
        aux_temp = pd.concat([self.df['percent_month'], self.df_Pvsyst], axis=1).fillna(0)

        self.df_Pvsyst_2_month['%_days_month'] = aux_temp['percent_month'].resample('m').sum()

        self.df_Pvsyst_2_month['KWh_adj_by_days'] = \
            self.df_Pvsyst_2_month['Year 0 Actual Production (kWh)'].multiply(self.df_Pvsyst_2_month['%_days_month'])

        # -->  NREL  Weather adjusted needs DC_Corrected once the Meter is corrected in Ava functions.
        #
        #  There is a problem when all values are  = 0 and the Meter corrected is corrected with PVsyst values.
        #  the Weather adjusted function does not capture this effect, and therefore the Plant Performance is
        # higher than it should be.  We corrected reducing the number of days in the month.
        #
        # 09/16/2016  added >15 to fix Happy Solar issue.  Meter is positive at night.
        #
        aux_correction = self.df[(self.df['DC_corrected_WA'] == 0) & (self.df['Meter_Corrected_2'] > 15) & (self.df['Grid_loss'] == 0)]['Meter_Corrected_2']
        aux_correction_2 = aux_correction.resample('M').count() / 12.0  # Sunny days are considered 12 h
        aux_correction_2_percentage = pd.concat([day_points_full_year, aux_correction_2], axis=1)
        aux_correction_2_percentage = aux_correction_2_percentage['Meter_Corrected_2'].div(aux_correction_2_percentage['POA (W/m2)'].replace(0, np.nan)).fillna(0)

        #  To correct Weather adjusted values.  There is an issue when the Grid loss gets corrected
        #   PVsyst % values need to increase to move up weather % and lower Plant Performance
        #  See Kenansville 2 Solar Farm,  Month = April
        aux_correction_11 = self.df[(self.df['DC_corrected_WA'] == 0) & (self.df['Grid_loss'] > 0)]['Meter_Corrected_2']
        aux_correction_22 = aux_correction_11.resample('M').count() / 12  # Sunny days are considered 12 h
        aux_correction_22_percentage = pd.concat([day_points_full_year, aux_correction_22], axis=1)
        aux_correction_22_percentage = aux_correction_22_percentage['Meter_Corrected_2'].div(aux_correction_22_percentage['POA (W/m2)'].replace(0, np.nan)).fillna(0)

        filtered_flags = [x for x in self.loss_swap_flags if self.df.loc[x, 'DC_corrected_WA'] == 0]
        ls = list(aux_correction.index) + list(aux_correction_11.index) + filtered_flags

        new_correction = 1 - (self.df.loc[ls, 'Meter_losses&snow'].resample('m').sum().fillna(0) / self.df['Meter_losses&snow'].resample('m').sum())
        aux_weather_k = pd.concat([self.df_Pvsyst_2_month[u'POA (W/m2)'], new_correction], axis=1).fillna(1).iloc[:, 1]
        self.aux_new_k = aux_weather_k * self.df_Pvsyst_2_month['%_days_month']
        #  By doing this, all the Revenue gets changed.  NOt correct!

        aux_WA_PVsyst = pd.DataFrame()
        aux_WA_PVsyst['DC_corrected_PVsyst_WA'] = self.df_Pvsyst_2_month['DC_corrected_PVsyst_WA'].multiply(self.aux_new_k)
        aux_WA_measured = self.df['DC_corrected_WA'].resample('M').sum()
        aux_WA = pd.concat([aux_WA_PVsyst, aux_WA_measured], axis=1).fillna(0)
        self.df_Pvsyst_2_month['NREL_Weather_Adj_%'] = aux_WA['DC_corrected_WA'].div(aux_WA['DC_corrected_PVsyst_WA'].replace(0, np.nan)).fillna(0)

        # ASTM
        P_exp_month = self.P_exp.resample('M').sum()
        #
        self.df_Pvsyst_2_month['ASTM_Weather_Adj_%'] = P_exp_month.div(self.df_Pvsyst_2_month['KWh_adj_by_days'].replace(0, np.nan)).fillna(0)
        # POA Ratios
        self.df_Pvsyst_2_month['POA_adj_by_days'] = self.df_Pvsyst_2_month['POA (W/m2)'].multiply(self.aux_new_k)
        self.df_Pvsyst_2_month['GHI_adj_by_days'] = self.df_Pvsyst_2_month['GHI (W/m2)'].multiply(self.aux_new_k)
        #
        self.POA_month = self.df['POA_avg'].resample('M').sum()
        #
        self.df_Pvsyst_2_month['POA_%'] = self.POA_month.div(self.df_Pvsyst_2_month['POA_adj_by_days'].replace(0, np.nan)).fillna(0)
        self.df_Pvsyst_2_month['GHI_%'] = self.df['GHI_avg'].resample('M').sum().div(self.df_Pvsyst_2_month['GHI_adj_by_days'].replace(0, np.nan)).fillna(0)


    def __calculate_dashboard_percentages(self):
        # Create Monthly Dataframes
        df = self.df.copy().drop(columns='POA_source').astype(float)
        self.df_month = df.resample('M').sum()

        #  Calculate Plant PR
        self.df_month['PR_Plant'] = self.df_month['Gen_NO_Clipping'].div(self.df_month['DC_corrected_PR'].replace(0, np.nan), axis="index")

        self.df_month_2 = pd.DataFrame(index=self.df_Pvsyst_2_month.index)
        self.df_month_2 = pd.concat([self.df_month_2, self.df_month], axis=1).fillna(0)
        pvsyst_var = ['KWh_adj_by_days', 'NREL_Weather_Adj_%',
                    'Revenue_IE_P50_days_adj', 'Revenue_IE_P50_days_adj_&_Weather']
        self.df_month_2[pvsyst_var] = self.df_Pvsyst_2_month[pvsyst_var]
        self.df_month_2['Weather_KWh'] = self.df_month_2['KWh_adj_by_days'].multiply(self.df_month_2['NREL_Weather_Adj_%'])

        #  Calculate Percentages
        self.df_month_2['Inv_Ava_%'] = self.df_month_2['Meter_Corrected_2'].div(self.df_month_2['Meter_&_ava'].replace(0, np.nan)).fillna(1)
        self.df_month_2['Grid_Ava_%'] = self.df_month_2['Meter_&_ava'].div(self.df_month_2['Meter_&_ava_&_grid'].replace(0, np.nan)).fillna(1)
        self.df_month_2['Snow_Adj_%'] = self.df_month_2['Meter_&_ava_&_grid'].div(self.df_month_2['Meter_losses&snow'].replace(0, np.nan)).fillna(1)
        self.df_month_2['Plant_Perf_%'] = self.df_month_2['Meter_losses&snow'].div(self.df_month_2['Weather_KWh'].replace(0, np.nan)).fillna(0).replace(np.inf, 1).replace(-np.inf, 1)
        self.df_month_2['diff_PR_%'] = self.df_month_2['PR_Plant'] - self.df_Pvsyst_2_month['PR_IE_P50_PR']
        self.df_month_2['Project_IPR_%'] = self.df_month_2['POI_kWH'].div(self.df_Pvsyst_2_month['KWh_adj_by_days'].replace(0, np.nan)).fillna(0)

        #  modified on 2016/09/22 to eliminate the effect of Grid Ava on OPR.  OPR should not include Gri
        self.df_month_2['Project_OPR_%'] = self.df_month_2['Project_IPR_%'].div((self.df_Pvsyst_2_month['POA_%'] * self.df_month_2['Grid_Ava_%']).replace(0, np.nan)).fillna(0).replace(np.inf, 0).replace(-np.inf, 0)
        self.df_month_2['Project_OPR_Temp_%'] = self.df_month_2['PR_Plant'].div(self.df_Pvsyst_2_month['PR_IE_P50_PR']).fillna(0)

        self.df_month_2['AC_batt_eff_%'] = self.df_month_2['POI_kWH'].div(self.df_month_2['Meter_Corrected_2'].replace(0, np.nan))
        self.df_Pvsyst_2_month['IE_AC_batt_eff_%'] = self.df_Pvsyst_2_month['POI Output (kWh)'].div(self.df_Pvsyst_2_month['Year 0 Actual Production (kWh)'].replace(0, np.nan))
        self.df_month_2['AC_batt_eff_index_%'] = self.df_month_2['AC_batt_eff_%'].div(self.df_Pvsyst_2_month['IE_AC_batt_eff_%'].replace(0, np.nan))

        self.df_month_2['AC_batt_rev_gain'] = self.df_month_2['POI_rev'].div(self.df_month_2['Meter_Corrected_2_rev'].replace(0, np.nan)).fillna(1)
        self.df_Pvsyst_2_month['IE_AC_batt_rev_gain'] = self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj_&_Weather'].div(self.df_Pvsyst_2_month['Revenue_IE_meterOnly_days_adj'].replace(0, np.nan)).fillna(1)
        self.df_month_2['AC_batt_rev_index_%'] = self.df_month_2['AC_batt_rev_gain'].div(self.df_Pvsyst_2_month['IE_AC_batt_rev_gain'].replace(0, np.nan)).fillna(1)

        self.df_month_2['Modeled_AC_batt_rev_gain'] = self.df_month_2['POI_modeled_rev'].div(self.df_month_2['Meter_Corrected_2_rev'].replace(0, np.nan)).fillna(1)
        self.df_month_2['Modeled_AC_batt_rev_index_%'] = self.df_month_2['Modeled_AC_batt_rev_gain'].div(self.df_Pvsyst_2_month['IE_AC_batt_rev_gain']).replace(0, np.nan).fillna(1)

        self.df_month_2['Modeled_AC_rev_target'] = self.df_month_2['POI_rev'].div(self.df_month_2['POI_modeled_rev'].replace(0, np.nan))

        #  Calculate Revenue Differences
        self.df_month_2['diff_weather_$'] = \
            self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj_&_Weather'] - self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj']

        self.df_month_2['diff_Inv_ava_$'] = \
            (self.df_month_2['Meter_Corrected_2_rev'] - self.df_month_2['Meter_&_ava_rev']).multiply(self.df_Pvsyst_2_month['IE_AC_batt_rev_gain'])
        self.df_month_2['diff_Grid_ava_$'] = \
            (self.df_month_2['Meter_&_ava_rev'] - self.df_month_2['Meter_&_ava_&_grid_rev']).multiply(self.df_Pvsyst_2_month['IE_AC_batt_rev_gain'])

        self.df_month_2['diff_snow_$'] = \
            (self.df_month_2['Meter_&_ava_&_grid_rev'] - self.df_month_2['Meter_losses&snow_rev']).multiply(self.df_Pvsyst_2_month['IE_AC_batt_rev_gain'])
        self.df_month_2['diff_AC_batt_$'] = \
            (self.df_month_2['POI_rev'] - self.df_month_2['Meter_Corrected_2_rev']) - \
                (self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj_&_Weather'] - self.df_Pvsyst_2_month['Revenue_IE_meterOnly_days_adj'])

        self.df_month_2['diff_Plant_Perf_$'] = \
            (self.df_month_2['POI_rev'] - self.df_month_2[
                ['diff_snow_$', 'diff_Grid_ava_$', 'diff_Inv_ava_$', 'diff_AC_batt_$']
                    ].sum(axis=1)) - self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj_&_Weather']

        self.df_month_2['diff_all_$'] = self.df_month_2['POI_rev'] -  self.df_Pvsyst_2_month['Revenue_IE_P50_days_adj']

        old_cum = self.df_Meter_ORIGINAL.iloc[:, np.arange(len(self.pos_Meter),
                                                           len(self.pos_Meter) + len(self.pos_Meter_Cum))
                                              ].sum(axis=1)
        old_cum = old_cum[old_cum != 0]
        self.df_month_2['AE_Meter'] = old_cum.resample('M').last() - old_cum.resample('M').first()

        day_points = self.df['POA_avg'].resample('M').count() / 24.0
        self.df_month_2 = pd.concat([self.df_month_2, day_points.rename('Days_counted')], axis=1).fillna(0)
        self.df_month_2['AC_Capacity_%'] = self.df_month_2['POI_kWH'] / (self.clipping_KW * 24 * self.df_month_2['Days_counted'])
        self.df_month_2['DC_Capacity_%'] = self.df_month_2['POI_kWH'] / (self.Pstc_KW * 24 * self.df_month_2['Days_counted'])

        # Calculate probability as a normal distribution
        # x=measured; loc=mean; scale = standard deviation
        self.df_month_2['Monthly Probability of Exceedence'] = \
            sct.norm.sf(x=self.df_Pvsyst_2_month['GHI_%'] * self.df_Pvsyst_2_month['GHI_adj_by_days'],
                        loc=self.df_Pvsyst_2_month['GHI_adj_by_days'],
                        scale=self.df_Pvsyst_2_month['GHI_adj_by_days'] * .10)

        # comparing poa-weighted tcell against 8760 equivalent
        # and calculating non-temperature-adjusted PRs
        df['DC_corrected_PR_notemp'] = 0
        # exclude times when DC_corrected_PR has been filtered (ie, equals zero)
        df.loc[df['DC_corrected_PR'] != 0, 'DC_corrected_PR_notemp'] = self.Pstc_KW * (df['POA_avg'] / self.Gstc)

        self.df_month_2['PR_notemp'] = np.nan
        self.df_month_2.loc[df['POA_avg'].resample('m').count().index, 'PR_notemp'] = \
            df['Gen_NO_Clipping'].resample('m').sum() / df['DC_corrected_PR_notemp'].resample('m').sum()

        aux = df['POA_avg'] * df['Tcell']
        self.df_month_2['POA_weighted_Tcell'] = aux.resample('m').sum() / df['POA_avg'].resample('m').sum()
        self.df_Pvsyst['DC_corrected_PVsyst_PR_notemp'] = 0

        # exclude times when DC_corrected_PVsyst_PR has been filtered (ie, equals zero)
        self.df_Pvsyst.loc[self.df_Pvsyst['DC_corrected_PVsyst_PR'] != 0,
                    'DC_corrected_PVsyst_PR_notemp'] = self.Pstc_KW * (self.df_Pvsyst['POA (W/m2)'] / self.Gstc)

        self.df_Pvsyst_2_month['Pvsyst_PR_notemp'] = \
            self.df_Pvsyst['Gen_NO_Clipping_PVsyst'].resample('m').sum() / self.df_Pvsyst['DC_corrected_PVsyst_PR_notemp'].resample('m').sum()

        aux = self.df_Pvsyst['POA (W/m2)'] * self.df_Pvsyst['Tcell']
        self.df_Pvsyst_2_month['Pvsyst_POA_weighted_Tcell'] = \
            aux.resample('m').sum() / self.df_Pvsyst['POA (W/m2)'].resample('m').sum()

        self.df_month_2['OPR_notemp'] = self.df_month_2['PR_notemp'] / self.df_Pvsyst_2_month['Pvsyst_PR_notemp']

        self.df_month_2['ac_battery_flag'] = self.Battery_AC_site * 1

        # Calculate capacity test
        var_meas = ['Meter_Corrected_2', 'POA_avg', 'Wind_speed', 'Tamb_avg']
        df_meas, df_meas_RC = weather.generate_linear_coeff_table_v2(self.df[var_meas], var_meas, self.clipping_KW)
        if not df_meas.empty:
            # prep columns
            df_coef_trans = pd.DataFrame(columns = [int(x) for x in self.df_coef.columns])
            df_meas.columns = [int(x) for x in df_meas.columns]
            df_meas_RC.columns = [int(x) for x in df_meas_RC.columns]
            # prep for dataframe math
            df_coef_trans = self.df_coef[df_meas.columns.tolist()].T
            df_meas = df_meas.T
            df_meas_RC = df_meas_RC.T
            # find scores
            aux_meas = df_meas_RC['POA']*(df_meas['E']+df_meas['E2']*df_meas_RC['POA'] +
                                        df_meas['ET']*df_meas_RC['T']+df_meas['Ev']*df_meas_RC['Wind'])
            aux_ie = df_meas_RC['POA']*(df_coef_trans['E']+df_coef_trans['E2']*df_meas_RC['POA'] +
                                        df_coef_trans['ET']*df_meas_RC['T']+df_coef_trans['Ev']*df_meas_RC['Wind'])
            capacity_scores = pd.DataFrame((aux_meas / aux_ie).values, index=self.df_month.index, columns=['Capacity_result'])
        else:
            capacity_scores = pd.DataFrame([], index=self.df_month.index, columns=['Capacity_result'])
        self.df_month_2['Capacity_result'] = capacity_scores

    
    def __verify_performance(self):
        self.df_month_2['Perf_Test_Pass'] = 1
        guarantee_id = self.df_proj_keys['Guarantee_ID']
        self.df_perf = \
            pd.DataFrame([], columns=['Guar_freq', 'Gaur_range', 'USB1', 'kwh_guar',
                                      'kwh_pro', 'usb_years', 'kwh_pro_deg', 'kwh_meas',
                                      'kwh_meas_poa', 'kwh_meas_ghi', 'USB1_target',
                                      'USB_result', 'REGIONS', 'reg_IPR', 'reg_OPR',
                                      'reg_target', 'reg_result', 'SOL', 'sol_IPR_weather',
                                      'sol_target', 'sol_result', 'IDP', 'IDP_mechanical_ava',
                                      'IDP_target_ava', 'IDP_pass', 'SCEG', 'SCEG_kwh_guar',
                                      'SCEG_kwh_guar_grid_85_proration', 'SCEG_kwh_measured',
                                      'SCEG_kwh_proration_factor', 'SCEG_perf_guar_result'])

        if str(guarantee_id) != "nan":
            if guarantee_id == "USB1":
                guarantee_input = float(self.df_proj_keys['Guarantee_input'])
                self.df_perf, guarantee_result = perf.USB1_performance_guarantee(self.df,
                                                                       len(self.df_month),
                                                                       self.df_Pvsyst,
                                                                       self.PIS_date,
                                                                       guarantee_input,
                                                                       self.df_perf)
            elif guarantee_id == 'SCEG':
                self.df_perf, guarantee_result = perf.SCEG_performance_guarantee(self.project_name,
                                                                       self.df,
                                                                       self.df_Pvsyst,
                                                                       self.PIS_date,
                                                                       self.df_perf,
                                                                       data_platform=self.data_platform)
            elif guarantee_id == "Regions_OPR":
                guarantee_input = pd.to_datetime(self.df_proj_keys['Guarantee_input'])
                self.df_perf, guarantee_result = perf.Regions_performance_guarantee(self.df,
                                                                          self.df_month_2,
                                                                          self.df_Pvsyst,
                                                                          self.df_Pvsyst_2_month,
                                                                          guarantee_input,
                                                                          self.df_perf)
            elif guarantee_id == "Sol_OPR":
                self.df_perf, guarantee_result = perf.Sol_performance_guarantee(self.df_month_2,
                                                                      self.df_Pvsyst_2_month,
                                                                      self.df_perf)
            elif guarantee_id == "IDP_MAG":
                self.df_perf, guarantee_result = perf.IDP_performance_guarantee(self.ava, self.df_perf)
            else:
                raise RuntimeError("Unknown Guarantee ID for " + self.project_name + ": " + guarantee_id)
            self.df_month_2['Perf_Test_Pass'] = guarantee_result
        self.df_perf = self.df_perf.fillna('')

        # curtailed sites will have their PP unfairly decreased, so we move the losses to grid availability
        for i, row in self.sensor_OFF.query('Var_ID == "grid"').iterrows():
            s = row['start date']
            e = row['end date']
            print(e)
            if e == -1:
                e = self.df_month_2.index[-1]
            e = e.to_period('M').to_timestamp('M')

            # generate all months between start and end -- dates look like '2017-01-31' (end of month) to match self.df_month_2.index
            curtailment_dates = pd.date_range(start=s, end=e, freq='M')
            for date in self.df_month_2.index:
                if date in curtailment_dates:
                    print("using curtailment for the month of", date)
                    self.df_month_2.loc[date, 'Grid_Ava_%'] = \
                        self.df_month_2.loc[date, 'Grid_Ava_%'] + (self.df_month_2.loc[date, 'Plant_Perf_%'] - 1)
                    self.df_month_2.loc[date, 'Plant_Perf_%'] = 1
                    self.df_month_2.loc[date, 'diff_Grid_ava_$'] = \
                        self.df_month_2.loc[date, 'diff_Grid_ava_$'] + self.df_month_2.loc[date, 'diff_Plant_Perf_$']
                    self.df_month_2.loc[date, 'diff_Plant_Perf_$'] = 0

    
    def __calculate_project_metrics(self):
        var_col = ['Wind_speed', 'Meter', 'Meter_cum', 'POA_avg', 'Tmod_avg', 'Tamb_avg',
                   'Tcell_AMB', 'Tcell_MOD', 'Tcell', 'DC_corrected', 'DC_corrected_PR',
                   'DC_corrected_WA', 'Gen_NO_Clipping', 'AVA_Energy_loss', 'Grid_loss',
                   'Meter_cum_corrected_2', 'Meter_Corrected_2', 'Meter_&_ava',
                   'Meter_&_ava_&_grid', 'Rates', 'Meter_Corrected_2_rev', 'Meter_&_ava_rev',
                   'Meter_&_ava_&_grid_rev', 'PR_Plant', 'KWh_adj_by_days', 'NREL_Weather_Adj_%',
                   'Revenue_IE_P50_days_adj', 'Revenue_IE_P50_days_adj_&_Weather', 'Weather_KWh',
                   'Inv_Ava_%', 'Grid_Ava_%', 'Plant_Perf_%', 'diff_PR_%', 'Project_IPR_%',
                   'Project_OPR_%', 'Project_OPR_Temp_%', 'diff_Inv_ava_$', 'diff_Grid_ava_$',
                   'diff_weather_$', 'diff_Plant_Perf_$', 'diff_all_$', 'AE_Meter',
                   'AC_Capacity_%', 'DC_Capacity_%', 'Monthly Probability of Exceedence',
                   'Perf_Test_Pass', 'Capacity_result', 'Snow_Adj_%', 'diff_snow_$',
                   'POA_weighted_Tcell', 'AC_batt_eff_%', 'AC_batt_eff_index_%',
                   'AC_batt_rev_gain', 'AC_batt_rev_index_%', 'diff_AC_batt_$',
                   'POI_Corrected_2', 'POI_rev', 'ac_battery_flag', 'Modeled_AC_batt_rev_gain',
                   'Modeled_AC_batt_rev_index_%', 'Modeled_AC_rev_target', 'OM_uptime']

        # Calculate OM uptime
        # Create average POA data in case of grid outage
        # Replaced ava.AVA with ava.OM_Uptime
        aux = pd.concat([self.df[['Meter_Corrected_2',
                                  'Meter_&_ava',
                                  'Meter_&_ava_&_grid',
                                  'Meter_losses&snow',
                                  'POA_avg',
                                  'percent_month']],
                         self.ava['OM_Uptime']], axis=1)
        aux['month'] = aux.index.month
        aux['ind'] = aux.index

        multiply = self.df_Pvsyst_2_month[['POA (W/m2)']]
        multiply['month'] = multiply.index.month

        aux2 = pd.merge(aux, multiply, on='month').set_index('ind', drop=True)

        aux2.index.name = None
        aux2['estimated_POA'] = aux2['POA (W/m2)'] * aux2['percent_month']

        # when POA data is not available, use estimate data
        aux2.loc[~(self.df_sensor_ON[self.pos_POA] == True).any(axis=1), 'POA_avg'] = aux2['estimated_POA']

        # filter and calculate uptime
        aux3 = aux2.copy()

        # Filter out config grid outage
        aux3 = aux3.loc[~aux3.index.isin(self.curtailment_flags), :]

        # filtered out grid outage
        aux3 = aux3.loc[aux3['Meter_&_ava_&_grid'] == aux3['Meter_&_ava'], :]
        aux3 = aux3.loc[aux3['POA_avg'] > 100, :]  # poa filter
        aux3 = aux3.loc[~((aux3['OM_Uptime'] == 0) & (aux3['Meter_&_ava'] == aux3['Meter_Corrected_2'])), :]
        self.df_month_2['OM_uptime'] = aux3['OM_Uptime'].resample('m').mean()
        self.df_month_2['OM_uptime'] = self.df_month_2['OM_uptime'].fillna(1)

        self.df_month_3 = self.df_month_2[var_col].fillna(0)

        #  Calculate Energy generated based on rate
        #  Use NREL Weather adj % to create PVsyst Revenue
        self.df_Pvsyst_2['NREL_Weather_Adj_coef'] = 0
        self.df_Pvsyst_2['NREL_Weather_Adj_days_%'] = 0

        for mh in range(1, 13):
            self.df_Pvsyst_2.loc[self.df_Pvsyst.index.month == mh,
                            'NREL_Weather_Adj_coef'] = self.df_Pvsyst_2_month['NREL_Weather_Adj_%'].values[mh-1]
            self.df_Pvsyst_2.loc[self.df_Pvsyst.index.month == mh,
                            'NREL_Weather_Adj_days_%'] = self.df_Pvsyst_2_month['%_days_month'].values[mh-1]

        self.df_Pvsyst_2['NREL_Weather_Adj_Kwh'] = self.df_Pvsyst_2['NREL_Weather_Adj_days_%'].multiply(
            self.df_Pvsyst_2['Year 0 Actual Production (kWh)'])

        # Added flat payments/fees
        self.df_Pvsyst_2['NREL_Weather_Adj_Kwh_$'] = \
            self.df_Pvsyst_2['NREL_Weather_Adj_Kwh'].multiply(self.df_Pvsyst_2['Rates'], axis="index") + self.df_Pvsyst_2['Flat']

        if self.normal_rate_flag:  # are you using normal 3 price rate, or custom 8760 rate?
            self.table_gen = \
                rate_table.generate_table_variable_by_rev_schedule_v02(self.rates_year_i,
                                                            self.df,
                                                            'POI_kWH',
                                                            self.df_Pvsyst_2,
                                                            'NREL_Weather_Adj_Kwh',
                                                            self.df_config,
                                                            self.df_month_2,
                                                            self.df_Pvsyst_2_month)
            self.table_rev = \
                rate_table.generate_table_variable_by_rev_schedule_v02(self.rates_year_i,
                                                            self.df,
                                                            'POI_rev',
                                                            self.df_Pvsyst_2,
                                                            'NREL_Weather_Adj_Kwh_$',
                                                            self.df_config,
                                                            self.df_month_2,
                                                            self.df_Pvsyst_2_month)
        else:
            self.table_gen = pd.DataFrame(np.zeros([12, 6]), index=self.df_Pvsyst_2_month.index)
            self.table_rev = self.table_gen

        # Post SC Date correction
        # 10/26/16 create an 1 or 0 if after the SC date. Used for reporting
        self.df_Pvsyst_2_month['Post SC Date'] = 0
        self.df_Pvsyst_2_month.loc[(self.df_Pvsyst_2_month.index > self.SC_Date + pd.offsets.MonthEnd(0)), 'Post SC Date'] = 1
        self.df_Pvsyst_2_month['Model_Irradiance_Index'] = \
            (self.df_Pvsyst_2_month['POA_%'] / self.df_Pvsyst_2_month['GHI_%']).replace(np.inf, 0).fillna(0)

        # correct the column ordering
        col_reorder = ['Holiday', 'month', 'DST', 'weekday', 'Peak_day', 'ON_Peak', 'Summer', 'Energy_Peak',
                    'Capacity_Peak', 'Rates', 'Flat', u'POA (W/m2)', u'GHI (W/m2)', 'kWh_ORIGINAL',
                    u'Year 0 Actual Production (kWh)', 'DC_corrected_PVsyst', 'DC_corrected_PVsyst_PR',
                    'DC_corrected_PVsyst_WA', 'Gen_NO_Clipping_PVsyst', 'Revenue_IE_P50', 'Blended_Rate',
                    'PR_IE_P50', 'PR_IE_P50_PR', '%_days_month', 'KWh_adj_by_days', 'NREL_Weather_Adj_%',
                    'ASTM_Weather_Adj_%', 'POA_adj_by_days', 'GHI_adj_by_days', 'POA_%', 'GHI_%',
                    'Revenue_IE_P50_days_adj', 'Revenue_IE_P50_days_adj_&_Weather', 'Post SC Date',
                    'Model_Irradiance_Index', 'POA_weighted_Tcell', 'Pvsyst_PR_notemp', 'Pvsyst_POA_weighted_Tcell',
                    'IE_AC_batt_eff_%', 'IE_AC_batt_rev_gain', 'Revenue_IE_POI', 'POI_ORIGINAL', 'POI Output (kWh)']

        self.df_Pvsyst_2_month = self.df_Pvsyst_2_month[col_reorder]

        #    SEND TO EXCEL

        # ---------------
        #  Send day values
        df_d = self.df.resample('D').sum()
        var_col = ['POA_avg', 'POI_kWH', 'Meter_cum_corrected_2']
        #
        Prod_adj = self.P_exp
        Prod_adj_day = Prod_adj.resample('D').sum()

        # measured NREL PR
        NREL_OPR_day = pd.DataFrame(self.df[['Gen_NO_Clipping', 'DC_corrected_PR']]).resample('d').sum()
        NREL_OPR_day['Meas_PR'] = NREL_OPR_day['Gen_NO_Clipping'].div(NREL_OPR_day['DC_corrected_PR'].replace(0, np.nan)).fillna(0)
        # expected NREL PR
        PR_day = pd.DataFrame(self.df_Pvsyst_2_month['PR_IE_P50']).resample('MS').mean()
        aux = pd.DataFrame([PR_day['PR_IE_P50'][-1]], index=[PR_day.index.max() +
                        pd.offsets.MonthEnd()], columns=PR_day.columns)
        PR_day = PR_day.append(aux)
        PR_day = PR_day['PR_IE_P50'].resample('d').pad()

        # Changed due to pandas deprecating `join_axes`
        # NREL_OPR_day = pd.concat([NREL_OPR_day, PR_day], axis=1, join_axes=[df_d.index])
        NREL_OPR_day = pd.concat([NREL_OPR_day, PR_day], axis=1).reindex(df_d.index)

        # Changed due to pandas deprecating `join_axes`
        # self.df_d2 = pd.concat([df_d[var_col], Prod_adj_day, NREL_OPR_day], axis=1, join_axes=[df_d.index])
        self.df_d2 = pd.concat([df_d[var_col], Prod_adj_day, NREL_OPR_day], axis=1).reindex(df_d.index)


        # Diagnostic Metrics
        # NOTE: diagnostic metrics - weather bool ~ weather_prorate; day bool ~ days_month_5
        self.df_Pvsyst_2_month['Weather_prorate'] = self.aux_new_k
        self.df_Pvsyst_2_month['days_month_5'] = self.df_Pvsyst_2_month['%_days_month']
        self.df_Pvsyst_2_month['Nominal_Noclip_Weather_Adj'] = \
            self.df['DC_corrected'].resample('M').sum().div((self.df_Pvsyst_2_month['DC_corrected_PVsyst'].multiply(self.aux_new_k)).replace(0, np.nan)).fillna(0)

        self.df['DC_nominal'] = self.Pstc_KW * self.df['POA_avg']/self.Gstc
        self.df_Pvsyst['DC_nominal_PVsyst'] = self.Pstc_KW * self.df_Pvsyst['POA (W/m2)']/self.Gstc
        self.df_Pvsyst_2_month['Nominal_NoclipNoTemp_Weather_Adj'] = \
            self.df['DC_nominal'].resample('M').sum().div((self.df_Pvsyst['DC_nominal_PVsyst'].resample('M').sum().multiply(self.aux_new_k)).replace(0, np.nan)).fillna(0)

        # clipping effect for measured
        self.df_month_2['measured_clipping_dcimpact'] = \
            self.df['DC_corrected_WA'].resample('M').sum().div(self.df['DC_corrected'].resample('M').sum().replace(0, np.nan)).fillna(1)

        # clipping effect for IE
        self.df_Pvsyst_2_month['ie_clipping_dcimpact'] = \
            self.df_Pvsyst_2_month['DC_corrected_PVsyst_WA'].div(self.df_Pvsyst['DC_corrected_PVsyst'].resample('M').sum().replace(0, np.nan)).fillna(1)

        # ASTM clipping effect for measured
        IE_coef, IE_coef_RC = weather.generate_linear_coeff_table_v3(self.df_Pvsyst, self.var_astm, self.clipping_KW)

        # find empty months
        if not IE_coef.loc[:, IE_coef.sum() == 0].empty:
            aux = IE_coef.loc[:, IE_coef.sum() == 0]
            # find typical values to replace bad ones
            avg = IE_coef.loc[:, IE_coef.sum() != 0].mean(axis=1)

            # edit months that failed
            for col in aux.columns:
                IE_coef.loc[:, col] = avg

        P_astm = weather.create_ASTM_column(self.df, IE_coef)
        self.df_month_2['measured_clipping_astmimpact'] = \
            P_astm.clip(upper=self.clipping_KW).resample('M').sum().div(P_astm.resample('M').sum().replace(0, np.nan)).fillna(1)
        # ASTM measured effect for IE
        TIE_coef = IE_coef.T
        self.df_Pvsyst_2['month'] = self.df_Pvsyst_2.index.month
        aux_pvsyst = pd.merge(self.df_Pvsyst_2, TIE_coef,left_on='month', right_index=True)
        aux_pvsyst['astm'] = aux_pvsyst['POA (W/m2)'] * \
            (aux_pvsyst['E'] + aux_pvsyst['E2']*aux_pvsyst['POA (W/m2)'] +
             aux_pvsyst['ET']*aux_pvsyst['Ambient Temperature'] +
             aux_pvsyst['Ev']*aux_pvsyst['Wind Velocity (m/s)'])
        self.df_Pvsyst_2_month['ie_clipping_astmimpact'] = \
            aux_pvsyst['astm'].clip(upper=self.clipping_KW).resample('M').sum().div(aux_pvsyst['astm'].resample('M').sum().replace(0, np.nan))

        # SPA Night flag, interp at night
        self.df_filt = self.df[['Meter_Corrected_2', 'POA_avg']].copy()
        self.df_filt['interp_check'] = 0

        # choosing conditional value of 10 in arbitrary sense
        # Meter correct 2 interp issues
        self.df_filt.loc[(self.df_filt['Meter_Corrected_2'] > 10) & ((self.df_filt.index.hour < 6) | (self.df_filt.index.hour > 20)), 'interp_check'] = 1
        
        # POA interp issues
        self.df_filt.loc[(self.df_filt['POA_avg'] > 5) & ((self.df_filt.index.hour < 6) | (self.df_filt.index.hour > 20)), 'interp_check'] = 1
        self.df_filt['Hour Index Copy'] = self.df_filt.index.hour
        self.df_month_2['night_flag'] = self.df_filt['interp_check'].resample('m').sum()+1

        # POI limit/PPA limit flag
        self.df_month_2['poi_limit_flag'] = (self.df['Meter_Corrected_2'] > self.MWAC*1000 * 1.01).astype(float).resample('m').sum()

        # Sensor Diagnostic Test
        # create poa list with only POAs on the site, not imported ones
        pos_POA_native = [x for x in self.pos_Native if 'POA' in x]

        # Keep only real values
        scatter = self.df[pos_POA_native][self.df_sensor_ON[pos_POA_native] == True]

        def slope_check(scatter):
            slope_list = []

            # Column to compare against
            ind = scatter.columns.tolist()[0]
            for poa_native in scatter.columns.tolist():
                if poa_native == 'month':
                    continue

                # remove nans in either col, messes up regression
                aux = scatter.loc[~scatter[[ind, poa_native]].isnull().any(axis=1)]
                if aux.empty:
                    slope_list.append((1, 1))
                else:
                    try:
                        slope, intercept, r_value, p_value, std_err = sct.linregress(aux[ind], aux[poa_native])
                    except:
                        slope, r_value = (1, 1)
                    slope_list.append((slope, r_value))

            df_slope_values = pd.DataFrame(slope_list, columns=['slope', 'r2'])
            df_slope_values['error'] = df_slope_values['slope'].fillna(1)
            df_slope_values['diff'] = (1-(df_slope_values['error'] - 1).abs()) * df_slope_values['r2']**2

            # using .min() doesn't capture bad values above 1
            return df_slope_values.loc[df_slope_values['diff'].idxmin(), 'error']

        self.df_month_2['POA_regress_flag'] = scatter.resample('M').apply(slope_check)

        # neighbor data
        non_native = [x for x in self.pos_POA + self.pos_Temperature + self.pos_Wind if x not in self.pos_Native]

        # True implies not filtered. If borrowed sensors have any value above 0, then it was used and flags need to be raised
        df_borrowed_sensors = \
            self.df[non_native][self.df_sensor_ON[non_native] == True].fillna(0).resample('M').sum() > 0

        if non_native == []:
            self.df_month_2['borrowed_data'] = ''
            self.df_month_2['nearby_sensor_flag'] = 1

        else:
            df_borrowed_sensors['nearby_sensor_flag'] = 1
            df_borrowed_sensors.loc[df_borrowed_sensors[non_native].any(axis=1), 'nearby_sensor_flag'] = 2
            self.df_month_2['nearby_sensor_flag'] = df_borrowed_sensors['nearby_sensor_flag']

            active = df_borrowed_sensors[non_native]
            df_borrowed_sensors['flag'] = active.apply(lambda row: ";".join(active.columns[row]), axis=1)
            self.df_month_2['borrowed_data'] = df_borrowed_sensors['flag']
            self.df_month_2['borrowed_data'] = self.df_month_2['borrowed_data'].fillna('')

        # inverter cum meter checks
        self.df['inv_cum'] = self.df[self.pos_Inv_cum].sum(axis=1)
        aux = self.df.loc[self.df['inv_cum'] != 0, ['inv_cum', 'Meter_cum_corrected_2']]

        self.df_month_2['inv_cum_check'] = \
            (aux['Meter_cum_corrected_2'].resample('M').last() - 
             aux['Meter_cum_corrected_2'].resample('M').first()
             ).div(aux['inv_cum'].resample('M').last() - aux['inv_cum'].resample('M').first())
        self.df_month_2['inv_cum_check'] = \
        self.df_month_2['inv_cum_check'].replace([np.nan, np.inf, -np.inf], 0) - 1

        # snow paper data
        self.df_month_2['snowfall'] = self.snow_data.resample('m').sum()

        # Remove night & non-data points
        self.df_month_2['snow_coverage_5'] = self.snow_coverage.loc[self.df['POA_avg'] > 5].resample('m').mean()
        self.df_month_2['snow_coverage_energy'] = self.snow_coverage.multiply(self.df.P_exp).resample('m').sum().divide(self.df_month_2['Meter_losses&snow'].replace(0, np.nan))

        # Find differences between meter corrected & site meter
        d = 'Meter_kwhdel'
        self.del_dif=((self.df_month_2.Meter_Corrected_2 / (self.df[[x for x in self.df.columns if d in x]].sum(1).resample('m').last() - self.df[[x for x in self.df.columns if d in x]].sum(1).resample('m').first())) -1) *100
        p = 'Meter_kwhrec'
        self.rec_dif=((self.df_month_2.Meter_Corrected_2 / (self.df[[x for x in self.df.columns if p in x]].sum(1).resample('m').last() - self.df[[x for x in self.df.columns if p in x]].sum(1).resample('m').first())) -1) *100
        self.dif=(((self.df_month_3.Meter_Corrected_2/self.df_month_3.AE_Meter)-1)*100)

        # Create OM Summary DF
        OM_POI = self.df_month_2['POI_Corrected_2']
        OM_P50 = self.df_Pvsyst_2_month['POI Output (kWh)']
        OM_Weather_adj = self.df_month_2['NREL_Weather_Adj_%'] * OM_P50
        OM_Production_Diff = (OM_POI-OM_P50)/OM_P50
        OM_Losses = OM_POI*np.nan

        OM_POA = self.POA_month/1000
        OM_POA_P50 = self.df_Pvsyst_2_month['POA (W/m2)']/1000
        OM_POA_Diff = (OM_POA-OM_POA_P50)/OM_POA_P50

        OM_Inv_Ava = self.df_month_2['Inv_Ava_%']
        OM_Ava = self.df_month_2['OM_uptime']
        OM_OPR = self.df_month_2['Project_OPR_Temp_%']
        OM_Batt = self.df_month_2['Modeled_AC_rev_target']

        # added for the waterfall numbers
        OM_IE_P50 = OM_P50
        OM_Weather_adj_kwh = (self.df_month_2['NREL_Weather_Adj_%']-1) * OM_P50
        OM_INV_ava_kwh = self.df_month_2['Meter_Corrected_2'] - self.df_month_2['Meter_&_ava']
        OM_Grid_ava_kwh = self.df_month_2['Meter_&_ava'] - self.df_month_2['Meter_&_ava_&_grid']
        OM_snow_losses_kwh = self.df_month_2['Meter_&_ava_&_grid'] - self.df_month_2['Meter_losses&snow']
        OM_plant_perf_kwh = self.df_month_2['Meter_losses&snow'] - OM_Weather_adj
        OM_Meter_production_kwh = OM_POI
        OM_Losses = OM_Grid_ava_kwh+OM_INV_ava_kwh+OM_snow_losses_kwh
        OM_gap = OM_POI * np.nan

        # added 6.29.2020
        OM_WAP = OM_POI / OM_P50 / self.df_month_2['NREL_Weather_Adj_%']/self.df_month_2['Snow_Adj_%']
        OM_WAP = self.df_month_2['Project_IPR_%'] / self.df_month_2['NREL_Weather_Adj_%']/self.df_month_2['Snow_Adj_%']

        self.OM_data = pd.concat([
            OM_POI, OM_P50, OM_Weather_adj, OM_Production_Diff, OM_Losses, OM_POA,
            OM_POA_P50, OM_POA_Diff, OM_Inv_Ava, OM_Ava, OM_OPR, OM_WAP, OM_Batt,
            OM_gap, OM_IE_P50, OM_Weather_adj_kwh, OM_Grid_ava_kwh, OM_INV_ava_kwh,
            OM_snow_losses_kwh, OM_plant_perf_kwh, OM_Meter_production_kwh], axis=1)
        self.OM_data = self.OM_data.fillna('')

        #ADDED 3/11/2020##################################################################
        self.OM_data.columns = [
            'POI_Corrected_2', 'POI Output (kWh)', 'weather_ad_exp_prod_kwh',
            'ovp_production', 'estimated_loss', 'POA_avg', 'POA (W/m2)',
            'ovp_insolation', 'Inv_Ava_%', 'OM_uptime', 'Project_OPR_Temp_%',
            'Weather_Adjusted_performance', 'Modeled_AC_rev_target', 'POI_Corrected_2',
            'POI Output (kWh)', 'weather_losses_kwh', 'grid_ava_kwh', 'inv_ava_kwh',
            'snow_loss_kwh', 'plant_perf_kwh', 'POI_Corrected_2']

        # get just the necessary columns that aren't already given to O&M
        self.OM_data2 = self.OM_data[[
            'weather_ad_exp_prod_kwh', 'ovp_production', 'estimated_loss',
            'ovp_insolation', 'weather_losses_kwh', 'grid_ava_kwh', 'inv_ava_kwh',
            'snow_loss_kwh', 'plant_perf_kwh']]
