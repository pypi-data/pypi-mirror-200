# -*- coding: utf-8 -*-
"""
Module to coordinate processing of CCRenew Dashboard projects.
"""
from __future__ import annotations

import boto3
import builtins
from ccrenew.dashboard.utils.logging_conf import get_logging_config
from datetime import datetime
from dateutil import parser
import logging
import logging.config
from matplotlib.pyplot import waitforbuttonpress
import os
import pandas as pd
from pandas.io.sql import SQLTable
from pathlib import Path
import pickle
import s3fs
import sys
import time
import traceback
from typing import Iterable
import warnings

from ccrenew import (
    __version__,
    ccr,
    all_df_keys,
    ListLike
)
from ccrenew.dashboard import (
    DataPlatformDirs,
    func_timer,
    get_modified_time,
    make_s3_filepath
)
from ccrenew.dashboard import Plotter
from ccrenew.dashboard.project import Project
from ccrenew.dashboard.utils.df_tools import df_update_join
import ccrenew.dashboard.utils.dashboard_utils as utils
import ccrenew.dashboard.utils.project_neighbors as neighbs

from ccrenew.dashboard.data_processing.batch_process import (
    export_pool,
    process_pool)
    

# Create boto s3 client
s3_client = boto3.client('s3')

# suppress warnings about "A value is trying to be set on a copy of a slice from a DataFrame."
pd.set_option('mode.chained_assignment', None)

# Initialize logger
# Get logging configuration from the logging.conf file in the same directory as this file
username = os.getenv('username')
dashboard_folder = ccr.file_project
# log_filename = '{}_dashboard-{}.log'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), username)
# log_config = os.path.join(dashboard_folder, 'Python_Functions', 'logging.conf')
# log_file = os.path.join(dashboard_folder, 'Python_Functions', '_old', 'logs', log_filename)
# LOGGING_CONFIG = get_logging_config(log_file)
# logging.config.dictConfig(LOGGING_CONFIG)

# Create logger
# logger = logging.getLogger(__name__)
# logger.info('Beginning Dashboard Session')

def _execute_insert(self, conn, keys, data_iter):
    #print "Using monkey-patched _execute_insert"
    data = [dict((k, v) for k, v in zip(keys, row)) for row in data_iter]

    # Python 2 compatibility:
    try:
        conn.execute(self.insert_statement().values(data))
    except AttributeError:
        conn.execute(self.table.insert().values(data))
    

SQLTable._execute_insert = _execute_insert # type: ignore

    
class DashboardSession:
    """Main orchestrator for processing, plotting, and exporting data for projects (i.e. sites).

    Args:
        project_list (str or list): List of [Projects][ccrenew.dashboard.project.Project] to initialize when initializing the session.
        data_cutoff_date (str or datetime, optional): The last date you want to analyze. Defaults to the current date the dashboard is being run.
        data_source (str, optional): The location where project data is stored.
            Default is current year Sharepoint data. To pull S3 data add 's3' to the input. See below for examples.
        
    `data_source` examples:
    
    | data_source      | Explanation                  |
    |------------------|------------------------------|
    | `None`           | Current year Sharepoint data |
    | `'s3'`           | Current year S3 data         |
    | `'2022_data_'`   | 2022 Sharepoint data         |
    | `'2022_data_s3'` | 2022 S3 data                 |
    """

    # Instantiate globals as class variables
    df_keys = all_df_keys.copy()
    __version__ = __version__

    print('Pulling diagnostic comments from Smartsheets...')
    # Smartsheet comments from previous reporting months. I'm going to hardcode Jan 2021 as the earliest date (column index 69 - Nice) but we can change that easily
    df_ss_comments = ccr.get_ss_as_df('2819883898562436', drop_col_1=False, start_col=69, index_col='Project')

    # Site lists
    tracker_sites = ['5840 Buffalo Road', 'Alexis', 'ATOOD II', 'Bar D', 'Barnhill Road Solar', 'Bay Branch',
                     'Bonanza', 'Bovine Solar', 'Bronson', 'Cascade', 'Chisum', 'Copperfield', 'Curie',
                     'Eddy II', 'Gaston II', 'Griffin', 'Grove Solar (NC)', 'Grove', 'Hardison Farm',
                     'Hopewell Friends', 'Hyline', 'IS - 46 Tracker', 'IS 67', 'Lampwick', 'Leggett Solar',
                     'Mars', 'Neff', 'Nimitz', 'Open Range', 'Palmetto Plains', 'Prince George 1',
                     'Prince George 2', 'Railroad', 'Shoe Creek', 'Siler', 'Simba', 'Springfield', 'Sterling',
                     'Thunderegg', 'Vale', 'Wagyu', 'Warren', 'Wendell', 'West Moore II', 'Yellow Jacket']
    battery_ac_funds = ['LGE']
    battery_ac_sites = df_keys.query("Fund in @battery_ac_funds").index.tolist()
    battery_dc_sites = ['Salt Point', 'Dubois', 'Landau II', 'Clendenin A']
    
    # Type annotations & docstrings for documentation
    df_keys: pd.DataFrame
    """Metadata for all projects."""
    df_ss_comments: pd.DataFrame
    """DataFrame with Smartsheet comments."""
    battery_ac_funds: list
    """Funds with projects with AC batteries."""
    battery_ac_sites: list
    """Projects with AC batteries."""
    battery_dc_sites: list
    """Projects with DC batteries."""
    tracker_sites: list
    """Projects with tracker-type racking."""

    def __init__(self, project_list:str|ListLike|None=None, data_cutoff_date:str|datetime|None=None,
                 data_source:str|None=None, **kwargs):

        print('Initializing DashboardSession...')
        
        # Initialize a dict to store projects - key = project name; value = project object
        # utils.project_dict() overrides the __repr__ method of dict to pretty print the projects when you call it
        self.project_list = utils.project_dict()

        # Add projects to the session if provided
        if project_list:
            if isinstance(project_list, (str, ListLike)):
                self.add_projects(project_list)
            else:
                print('`project_list` must be a string or list. The projects provided were not added to the DashboardSession. Please try again in the initialized DashboardSession.')

        # Parse & add data_cutoff_date if provided. Default to current date if not provided or error during parsing 
        if data_cutoff_date:
            try:
                self.data_cutoff_date = parser.parse(data_cutoff_date) # type: ignore
            except:
                self.data_cutoff_date = datetime.today()
        else:
            self.data_cutoff_date = datetime.today()

        def set_data_source(data_source:str|None) -> None:
            if data_source:
                self.data_source = data_source
            else:
                self.data_source = f"{datetime.now().year}_data_"

        self.data_platform_dirs = DataPlatformDirs(ccr.file_project,
                                                   's3://cypress-perfeng-datalake-dev-us-west-2/Raw/HourlyResolution/')

        set_data_source(data_source)
        if 's3' in self.data_source.lower():
            data_source = self.data_source.replace(' ', '').replace('s3', '')
            set_data_source(data_source)
            self.dashboard_dir = self.data_platform_dirs.s3
            self.data_platform = 's3'
        else:
            self.dashboard_dir = self.data_platform_dirs.sharepoint
            self.data_platform = 'sharepoint'

        # Get snow dataframe
        self.raw_snow_df, self.snow_file = utils.get_snow_df(dashboard_folder, self.data_source, file_format='csv', data_platform=self.data_platform)

        # Create list for projects that have errored out
        self.errored_projects = {}

        # List of plotter objects for different projects
        self.plotters = {}

        # Type annotations & docstrings for documentation
        self.project_list: dict
        """List of [Projects][ccrenew.dashboard.project.Project] that
        have been initialized & added to the
        [DashboardSession][ccrenew.dashboard.session.DashboardSession] instance."""
        self.data_platform: str
        """Backend architecture of the source data for a project. Either `s3` or `sharepoint`."""
        self.data_source: str
        """Location of the source data for projects based on production year."""
        self.raw_snow_df: pd.DataFrame
        """Snow data."""
        self.data_cutoff_date: datetime
        """Last day to process data."""
        self.errored_projects: dict
        """List of [Projects][ccrenew.dashboard.project.Project] that have encountered
        errors while processing & their error messages."""
        self.plotters: dict
        """List of projects that have been plotted & their plots."""

    def __repr__(self):
        return 'DashboardSession object with {} projects'.format(len(self.project_list))


    def __str__(self):
        return 'DashboardSession object with {} projects'.format(len(self.project_list))


    def get_project(self, project_name:str|Project, get_neighbors:bool=True, report_type:str = 'monthly') -> Project:
        """
        Return a [Project][ccrenew.dashboard.project.Project] object given a project name.

        Args:
            project_name (str or Project): Name of a [Project][ccrenew.dashboard.project.Project] to return from the
                [DashboardSession][ccrenew.dashboard.session.DashboardSession] instance.
                If project does not yet exist in the session, it will be added then returned.
            get_neighbors (bool, optional): Flag to add & initialize neighbor [Projects][ccrenew.dashboard.project.Project].
            report_type (str): Method for processing the project. Options are `monthly`, `ul`, or `weekly`.

        Returns:
            Project object for the given the project name.
                If the project does not exist in the session when the call is made, the project will be initialized & returned.
        """
        if isinstance(project_name, Project):
            project = project_name
        else:
            try:
                project = self.project_list[project_name]
            except KeyError:
                project = self.add_project(project_name, get_neighbors=get_neighbors, report_type=report_type)
 
        return project


    def add_project(self, project_name:str|Project|ListLike, get_neighbors:bool = True, report_type:str = 'monthly') -> Project:
        """Adds & initializes a [Project][ccrenew.dashboard.project.Project]
        to a [DashboardSession][ccrenew.dashboard.session.DashboardSession] instance.

        Args:
            project_name (str or Project): The name of the project to add to the [DashboardSession][ccrenew.dashboard.session.DashboardSession] instance.
            get_neighbors (bool): Flag to add & initialize neighbor [Projects][ccrenew.dashboard.project.Project].
            report_type (str): Method for processing the project. Options are `monthly`, `ul`, or `weekly`.
        """
        # Type validation
        if not isinstance(project_name, (str, ListLike, Project)):
            raise TypeError("`project_name` must be a string, Project object, or Python list! Please reformat input and try again.")

        # Determine behavior based on what was passed to method
        if isinstance(project_name, ListLike):
            print(f"A list was supplied to the `add_project` method. The method will return the first project in the list that was successfully added to the `DashboardSession`.")
            project_list = list(project_name)
            project = self.add_projects(project_list, get_neighbors=get_neighbors, report_type=report_type)
        elif project_name in self.project_list:
            project = self.project_list[project_name]
        elif isinstance(project_name, Project):
            project = project_name
            self.project_list[project.project_name] = project
        else:
            project = self.__initialize_project(project_name, get_neighbors=get_neighbors, report_type=report_type)
            if not project.error_info:
                self.project_list[project.project_name] = project

        return project
    

    def add_projects(self, project_list:ListLike|str|Project, get_neighbors:bool = True, report_type:str = 'monthly') -> Project:
        """Calls [add_project()][ccrenew.dashboard.session.DashboardSession.add_project] for each project in a list.

        Args:
            project_list (list, str): list of project names to add & initialize to the [DashboardSession][ccrenew.dashboard.session.DashboardSession] instance.
            get_neighbors (bool): See [add_project()][ccrenew.dashboard.session.DashboardSession.add_project].
            report_type (str): See [add_project()][ccrenew.dashboard.session.DashboardSession.add_project].
        """
        if isinstance(project_list, (str, Project)):
            project = self.add_project(project_list, get_neighbors=get_neighbors, report_type=report_type)
            return project
        elif isinstance(project_list, ListLike):
            successful_projects = []
            for project_name in project_list:
                project = self.add_project(project_name, get_neighbors=get_neighbors, report_type=report_type)
                if project.error_info:
                    print(f"Could not add {project_name} to the `DashboardSession` instance. See error below:")
                    print(project.error_info)
                    continue
                else:
                    successful_projects.append(project)
            
            # Return the first successful project from the list
            project = successful_projects[0]

            return project

        else:
            raise TypeError("`project_list` must be a string, Project object, or Python list! Please reformat input and try again.")
                

    def __initialize_project(self, project_name:str, get_neighbors:bool = True, report_type:str = 'monthly'):
        """Initializes a project object with metadata

        Args:
            project_name (str): Name of a project to initialize.
            get_neighbors (bool): Flag to add & initialize neighbor projects.
            report_type (str): Method for processing the project. Options are `monthly`, `ul`, or `weekly`.

        Returns:
            Project: An initialized Project object
        """

        try:
            df_proj_keys = self.df_keys.query("Project == @project_name").to_dict('records')[0]
            df_proj_ss_comments = self.df_ss_comments.query("index == @project_name").to_dict('records')[0]
        except IndexError:
            # Log that project was not found
            warn_msg = '"{}" not found in df keys. Please verify the project is present in df keys & the spelling is correct and try again'.format(project_name)
            print(warn_msg)
            # logger.warn(warn_msg)
            df_proj_keys = {'Racking': 'None'}
            df_proj_ss_comments = {}
            proj_init_dict = {'error_info': warn_msg}

        # Get neighbor projects
        if get_neighbors:
            neighbor_list = self.__get_neighbors(project_name)
        else:
            neighbor_list = {}

        # Set battery/tracker attributes
        Battery_AC_site = project_name in self.battery_ac_sites
        Battery_DC_site = project_name in self.battery_dc_sites
        Tracker_site = df_proj_keys['Racking'] == 'Tracker'
        
        proj_init_dict = {}
        proj_init_dict['project_name'] = project_name
        proj_init_dict['df_proj_keys'] = df_proj_keys
        proj_init_dict['df_proj_ss_comments'] = df_proj_ss_comments
        proj_init_dict['dashboard_dir'] = self.dashboard_dir
        proj_init_dict['data_cutoff_date'] = self.data_cutoff_date
        proj_init_dict['data_platform'] = self.data_platform
        proj_init_dict['data_platform_dirs'] = self.data_platform_dirs
        proj_init_dict['data_source'] = self.data_source
        proj_init_dict['report_type'] = report_type
        proj_init_dict['Battery_AC_site'] = Battery_AC_site
        proj_init_dict['Battery_DC_site'] = Battery_DC_site
        proj_init_dict['Tracker_site'] = Tracker_site
        proj_init_dict['raw_snow_df'] = self.raw_snow_df
        proj_init_dict['snow_file'] = self.snow_file
        proj_init_dict['snow_file'] = self.snow_file
        proj_init_dict['neighbor_list'] = neighbor_list

        try:
            project = Project(proj_init_dict)
        except:
            print(f"**** {project_name} errored during initialization and will not be added to the DashboardSession.")
            proj_init_dict['error_info'] = traceback.format_exc()
            project = Project(proj_init_dict)

        return project
    

    def __get_neighbors(self, project_name:str):
        # Find all neighbors that satisfy the distance and equipment requirements
        all_neighbors = neighbs.find_nearby_projects(project_name, print_data=False, include_retired=False).index.tolist()
        poa_neighbors = neighbs.find_nearby_similar_projects(project_name, print_data=False, include_retired=False).index.tolist()
        
        # Then remove the search project from the list
        # (Sometimes it will return an empty list if there is some data missing in `df_keys`) so we need to check if it returned a non-empty list first
        try:
            all_neighbors.remove(project_name)
        except ValueError:
            pass
        try:
            poa_neighbors.remove(project_name)
        except ValueError:
            pass

        # We'll create a neighbor_list dictionary
        # Value=True: we can use it for POA data sub
        # Value=False: we can only use it for weather data sub
        neighbor_list = {project_name: True if project_name in poa_neighbors else False for project_name in all_neighbors}

        # If the project has neighbors, we'll add them to the DashboardSession instance
        # Set get_neighbors to False so we don't get neighbors of neighbors of neighbors etc.
        if neighbor_list:
            for neighbor in neighbor_list.copy():
                try:
                    self.add_project(neighbor, get_neighbors=False)
                except:
                    neighbor_list.pop(neighbor)
        
        return neighbor_list


    def process_project(self, project_name:str|Project|ListLike, reprocess:bool = False, datasub:bool = False,
                        use_solcast:bool = True, report_type:str = 'monthly', **kwargs) -> Project:
        """
        Process data for the given [Project][ccrenew.dashboard.project.Project].

        Args:
            project_name (str or Project): The name of the [Project][ccrenew.dashboard.project.Project] to process.
            reprocess (bool): Whether to reprocess the data. This option will likely
                be uncommon as any changes to a [Project's][ccrenew.dashboard.project.Project] config file or powertrack file will
                automatically reprocess that data. This could be used if any changes are made
                outside of the config/powertrack file or a change is made to a neighbor.
            datasub (bool): Option to use automatic data substitution algorithm.
            use_solcast (bool): Option to use Solcast data in data sub process. `datasub`
                must be set to `True` for this option to take effect.
            report_type (str): Method for processing the project. Options are `monthly`, `ul`, or `weekly`.
        Returns:
            Processed Project object.
        """
        if isinstance(project_name, ListLike):
            # If we call this method with a list we'll default to series processing & return the first project in the list
            project_list = list(project_name)
            self.process_projects(project_list=project_list, method='series', reprocess=reprocess,
                                  datasub=datasub, use_solcast=use_solcast, report_type=report_type, **kwargs)

            project = self.project_list[project_list[0]]
            
            return project

        elif isinstance(project_name, (str, Project)):
            start = time.time()

            # Get project object
            project = self.get_project(project_name, report_type=report_type)
            if project.errored:
                print(f"{project.project_name} errored. Error details:\n{project.error_info}")
                return project
            
            # If the project has already been added to the session but we want to run it with a different process method
            # We'll update the process method & force the config file to reload
            if project.report_type != report_type:
                project.report_type = report_type
                project.last_update_config = datetime.fromtimestamp(0)

            # Pull the last updated dates from the filesystem for the config, bool, & Powertrack files
            try:
                last_update_config_file = get_modified_time(project.config_filepath, self.data_platform, 'file')
                last_update_bool_file = get_modified_time(project.bool_filepath, self.data_platform, 'file')
                last_update_powertrack_file = get_modified_time(project.powertrack_filepath, self.data_platform, 'file')
            except:
                self.__update_project_filepaths(project)
                last_update_config_file = get_modified_time(project.config_filepath, self.data_platform, 'file')
                last_update_bool_file = get_modified_time(project.bool_filepath, self.data_platform, 'file')
                last_update_powertrack_file = get_modified_time(project.powertrack_filepath, self.data_platform, 'file')

            # Check if the config, bool, or Powertrack files have been updated.
            # If not we don't need to process.
            if reprocess:
                project.last_update_config = datetime.fromtimestamp(0)
                project.last_update_bool = datetime.fromtimestamp(0)
                project.last_update_powertrack = datetime.fromtimestamp(0)
            if any([project.last_update_config != last_update_config_file,
                    project.last_update_bool != last_update_bool_file,
                    project.last_update_powertrack != last_update_powertrack_file]):

                # Pull config and/or Powertrack data
                self.__prepare_source_data(project)
            else:
                if project.processed:
                    print('{} already processed'.format(project.project_name))

                    return project

            # Process data - update neighbor sensors first then process the project
            print(f'Processing {project_name}....')
            # project.neighbor_list = self.__get_neighbors(project_name)
            self.__get_neighbor_sensor_data(project)
            failed_neighbors = []
            for neighbor_name in project.neighbor_list:
                try:
                    neighbor = self.project_list[neighbor_name]
                    self.__prepare_source_data(neighbor)
                    neighbor._calculate_native_sensor_averages()
                except:
                    print(f"Neighbor for {project.project_name} failed while processing")
                    print(f"Neighbor name: {neighbor_name}")
                    print(f"Error message: {traceback.format_exc()}")
                    failed_neighbors.append(neighbor_name)

                    continue

            for neighbor_name in failed_neighbors:
                del project.neighbor_list[neighbor_name]

            neighbor_sensor_data = {self.project_list[neighbor].project_name: self.project_list[neighbor].df_sensors_native_avg for neighbor in project.neighbor_list}

            try:
                project._process_data(neighbor_sensor_data=neighbor_sensor_data,
                                      datasub=datasub, use_solcast=use_solcast)
            except Exception:
                print('\n')
                print('###########################')
                print(f"{project.project_name} not processed. See below for error information. Error message can also be found in the Project's error_info attribute")
                print(traceback.format_exc())
                print('###########################')

                project.last_update_powertrack = datetime.fromtimestamp(0)
                project.errored = True
                project.error_info = traceback.format_exc()

                return project
            project.processed = True
            project.errored = False

            print('{} successfully processed. Processing time: {:.2f}s'.format(project.project_name, time.time()-start))

            return project
        else:
            raise TypeError("`project_name` must be a string or Project object! Please reformat input and try again.")
    
    
    def process_projects(self, project_list:str|Project|list, method:str = 'series', reprocess:bool = False,
                         datasub:bool = False, use_solcast:bool = True, report_type:str = 'monthly', **kwargs):
        """Calls [process_project()][ccrenew.dashboard.session.DashboardSession.process_project] for each
        [Project][ccrenew.dashboard.project.Project] in a list.

        Args:
            project_list (list): List of [Project][ccrenew.dashboard.project.Project] names process.
            method (str): Option to perform processing operations in `series` or `parallel`.
        
        *See [process_project()][ccrenew.dashboard.session.DashboardSession.process_project] for information on other arguments.
        """
        if isinstance(project_list, (str, Project)):
            project_name = project_list
            project = self.process_project(project_name, reprocess=reprocess, datasub=datasub,
                                           use_solcast=use_solcast, report_type=report_type)
            return project

        elif isinstance(project_list, list):
            if len(project_list) == 1:
                project_name = project_list[0]
                project = self.process_project(project_name, reprocess=reprocess, datasub=datasub,
                                               use_solcast=use_solcast, report_type=report_type)
                return project
            
            else:
                start = time.time()
                successful_projects = []
                errored_projects = []

                if method == 'series':
                    for i, project_name in enumerate(project_list):
                        project = self.process_project(project_name, reprocess=reprocess, datasub=datasub, use_solcast=use_solcast)
                        if not project or project.errored:
                            print(f"{project_name} encountered an error while processing.")
                            errored_projects.append(project_name)

                            continue

                        elapsed = time.time() - start
                        print('*******************************************************')
                        print(f'{project_name} complete. {i+1} of {len(project_list)} projects completed. Total elapsed time: {elapsed:2f}s')
                        print('*******************************************************')
                        successful_projects.append(project.project_name)

                elif __name__ == 'ccrenew.dashboard.session':
                    # We'll use half of the available processors for the machine to not completely bog it down.
                    max_workers = int(os.cpu_count()/2) # type: ignore
                    print(f"Processing {len(project_list)} projects with {min(max_workers, len(project_list))} workers.")
                    print("Progress messages from workers will be suppressed in an interactive session.")
                    print("Projects will report success upon completion and may not complete in the order in which they were submitted.")

                    # Construct a dict of kwargs for each project to pass to `process_pool`
                    if self.data_platform == 's3':
                        data_source = self.data_source + 's3'
                    else:
                        data_source = self.data_source

                    kwargslist =  [{"project_name": project_name,
                                    "session": DashboardSession,
                                    "data_source": data_source,
                                    "reprocess": reprocess,
                                    "datasub": datasub,
                                    "use_solcast": use_solcast,
                                    "project_num": i+1,
                                    "project_total": len(project_list),
                                    "batch_start": start
                                    } for i, project_name in enumerate(project_list)]

                    # Results are a list of Future objects, where we can get the results of the function call from `.result()`
                    results = process_pool(kwargslist)

                    for result in results:
                        processed_project_list = result.result()['project_list']
                        for project_dict in processed_project_list:
                            try:
                                project_name, project = project_dict
                                # If the project is already processed in the parent session we won't add it
                                if project_name in self.project_list and self.project_list[project_name].processed:
                                    pass
                                else:
                                    self.project_list[project_name] = project
                                
                            except:
                                continue

                        exported_project_name = result.result()['project_name']
                        exported_project = self.project_list[exported_project_name]
                        if exported_project.errored:
                            errored_projects.append(exported_project_name)
                        else:
                            successful_projects.append(exported_project_name)

                elapsed = time.time() - start
                print(f"\n{len(successful_projects)} projects successfullly processed.\n{len(errored_projects)} errored. Elapsed time: {elapsed:.2f}s.\n")
                print(f"Errored projects: {errored_projects}")
       
        else:
            raise TypeError("`project_list` must be a string or Python list! Please reformat input and try again.")


    def process_all_projects(self, method:str = 'parallel', reprocess:bool = True, datasub:bool = False,
                             use_solcast:bool = True, report_type:str = 'monthly', **kwargs):
        """
        Processes all projects in the [project_list][ccrenew.dashboard.session.DashboardSession.project_list]
        for the [DashboardSession][ccrenew.dashboard.session.DashboardSession] instance.

        *See [process_project()][ccrenew.dashboard.session.DashboardSession.process_project] for information on function arguments.
        """
        project_list = list(self.project_list.keys())
        self.process_projects(project_list, method=method, reprocess=reprocess,
                              datasub=datasub, use_solcast=use_solcast, report_type=report_type)
    

    def export_project(self, project_name:str|ListLike, server:str = 'dev', dest:str|list = 'all',
                       report_type:str = 'monthly', use_solcast:bool = True, save_pickle:bool = True, **kwargs) -> None:
        """
        Export project to desired location(s).

        Args:
            project_name (str or Project): Name of a project to export.
            server (str): Environment . Options are `prod` or `dev`, or `datasub`.
            dest (str or list): Option to export only certain parts of the project. `all` will export to all of the below destinations **except bool**.
            report_type (str): Option to select which report type to run. Options are `monthly`, `ul`, and `weekly`.
            save_pickle (bool): Option to save pickle after exporting.
            **kwargs: Optional arguments passed to [process_project()][ccrenew.dashboard.session.DashboardSession.process_project].

        `dest` Options

        | dest      | Description                                                              |
        |-----------|--------------------------------------------------------------------------|
        |  `excel`  | Export dataframes to Excel dashboard template.                           |
        |   `df`    | Export dataframe to the `Dataframes` folder of the project's [project_directory][ccrenew.dashboard.project.Project.project_directory], S3, and Bartertown PostgreSQL database. See below for export locations based on `server` selection. |
        | `summary` | Export monthly summary data to S3 and Bartertown PostgreSQL database. See below for export locations based on `server` selection. |
        |  `snow`   | Export [snow_data][ccrenew.dashboard.project.Project.snow_data] and [snow_coverage][ccrenew.dashboard.project.Project.snow_coverage] dataframes to S3. |
        |  `bool`   | Export bool file to the `Plant_Config_File` directory of the project's [project_directory][ccrenew.dashboard.project.Project.project_directory]. |

        `server` SQL Destinations

        |   server   | `df`                  | `summary`               |
        |------------|-----------------------|-------------------------|
        |   `prod`   | am_processed_data     | am_summary_data         |
        |   `dev`    | am_processed_data_dev | am_summary_data         |
        | `datasub`  | am_processed_data_dev | am_summary_data_datasub |

        `server` S3 Destinations

        |   server   | bucket                                         | `df` prefix          | `summary` prefix      |
        |------------|------------------------------------------------|----------------------|-----------------------|
        |   `prod`   | s3://cypress-perfeng-datalake-dev-us-west-2    | Curated/HourlyLosses | Curated/MonthlyLosses |
        |   `dev`    | s3://cypress-perfeng-datalake-onprem-us-west-2 | Curated/HourlyLosses | Curated/MonthlyLosses |
        | `datasub`  | s3://cypress-perfeng-datalake-onprem-us-west-2 | Curated/HourlyLosses | Curated/MonthlyLosses |
        """
        # Pass function arguments to `export_projects()`.
        # Remove `self`, i.e. the DashboardSession instance
        func_args = locals().copy()
        func_args.pop('self')

        if isinstance(project_name, ListLike):
            # Rename project_name to project_list for `export_projects`
            func_args.pop('project_name')
            func_args['project_list'] = list(project_name)
            self.export_projects(**func_args)

        elif isinstance(project_name, (str, Project)):
            project = self.get_project(project_name, report_type=report_type)
            if project.errored:
                raise Exception(f"{project.project_name} errored. Error details:\n{project.error_info}")

            # If we're only exporting the bool file then we don't need to process
            if dest != 'bool':
                func_args['save_pickle'] = False
                datasub = False
                if server == 'datasub':
                    datasub = True
                self.process_project(project_name, datasub=datasub, use_solcast=use_solcast,
                                     report_type=report_type, **kwargs)

            func_args.pop('project_name')
            project.export(**func_args)
            print(f"{project.project_name} successfully exported.")
        else:
            raise TypeError("`project_name` must be a string or Project object! Please reformat input and try again.")

  
    def export_projects(self, project_list:ListLike|str, method:str = 'series', server:str = 'dev',
                        dest:str|list = 'all', report_type:str = 'monthly', use_solcast:bool = True,
                        save_pickle:bool = True, **kwargs) -> None:
        """Calls [export_project()][ccrenew.dashboard.session.DashboardSession.export_project] for each
        [Project][ccrenew.dashboard.project.Project] in a list.

        Args:
            project_list (list): List of [Project][ccrenew.dashboard.project.Project] names process.
            method (str): Option to export in `series` or `parallel`.
        
        *See [export_project()][ccrenew.dashboard.session.DashboardSession.export_project] for information on other arguments.
        """
        # Store function arguments in case we need to pass them to `export_project()`.
        # Argument 0 is `self` so we'll pass arguments 1 and on
        func_args = locals().copy()
        func_args.pop('self')
        method = func_args.pop('method')

        if isinstance(project_list, (str, Project)):
            # Rename project_list to project_name for `export_project`
            func_args.pop('project_list')
            func_args['project_name'] = project_list
            self.export_project(**func_args)

        elif isinstance(project_list, ListLike):
            # If a list was passed, we'll pop the project list & use the remaining args
            project_list = list(func_args.pop('project_list'))

            if len(project_list) == 1:
                project_name = project_list[0]
                self.export_project(project_name, **func_args)

            else:
                start = time.time()
                successful_projects = []
                errored_projects = []

                if method == 'series':
                    for i, project_name in enumerate(project_list):
                        try:
                            self.export_project(project_name, **func_args)
                        except:
                            errored_projects.append(project_name)
                            continue
                    
                        elapsed = time.time() - start
                        print('*******************************************************')
                        print(f'{project_name} complete. {i+1} of {len(project_list)} projects exported. Total elapsed time: {elapsed:2f}s')
                        print('*******************************************************')
                        successful_projects.append(project_name)
                
                elif __name__ == 'ccrenew.dashboard.session':

                    # We'll use half of the available processors for the machine to not completely bog it down.
                    max_workers = int(os.cpu_count()/2) # type: ignore
                    print(f"Exporting {len(project_list)} projects with {min(max_workers, len(project_list))} workers.")
                    print("Progress messages from workers will be suppressed in an interactive session.")
                    print("Projects will report success upon completion and may not complete in the order in which they were submitted.")

                    # Construct a dict of kwargs for each project to pass to `process_pool`
                    if self.data_platform == 's3':
                        data_source = self.data_source + 's3'
                    else:
                        data_source = self.data_source

                    kwargslist =  [{"project_name": project_name,
                                    "session": DashboardSession,
                                    "data_source": data_source,
                                    "func_args": func_args,
                                    "project_num": i+1,
                                    "project_total": len(project_list),
                                    "batch_start": start
                                    } for i, project_name in enumerate(project_list)]

                    # Results are a list of Future objects, where we can get the results of the function call from `.result()`
                    results = export_pool(kwargslist)
                    for result in results:
                        all_projects = result.result()['project_list']
                        for project_dict in all_projects:
                            try:
                                project_name, project = project_dict
                                # If the project is already processed in the parent session we won't add it
                                if project_name in self.project_list and self.project_list[project_name].processed:
                                    pass
                                else:
                                    self.project_list[project_name] = project

                            except:
                                continue

                        exported_project_name = result.result()['project_name']
                        exported_project = self.project_list[exported_project_name]
                        if exported_project.errored:
                            errored_projects.append(exported_project_name)
                        else:
                            successful_projects.append(exported_project_name)

                elapsed = time.time() - start
                print(f"\n{len(successful_projects)} projects successfullly exported.\n{len(errored_projects)} errored. Elapsed time: {elapsed:.2f}s.\n")
                print(f"Errored projects: {errored_projects}")

        else:
            raise TypeError("`project_list` must be a string or Python list! Please reformat input and try again.")


    def remove_project(self, project_name:str) -> None:
        """Remove the selected project from the active session.

        Args:
            project_name (str): The name of the [Project][ccrenew.dashboard.project.Project]
                to remove from the [DashboardSession][ccrenew.dashboard.session.DashboardSession] instance.
        """
        del self.project_list[project_name]

    def get_ss_comments(self, project_name:str, num_comments: int|None=None) -> None:
        """Prints Smartsheet comments for the [Project][ccrenew.dashboard.project.Project].

        Args:
            project_name (str): Name of the [Project][ccrenew.dashboard.project.Project] to pull comments for.
            num_comments (int, optional): Number of comments to show, starting from the
                most recent. I.e. `5` will show the most recent 5 comments in the
                Smartsheet. Defaults to None, which will show all comments starting in Jan 2021.
        """
        project = self.get_project(project_name, get_neighbors=False)
        project.get_ss_comments(num_comments=num_comments)


    def save_pickle(self, project_name, store_plots=False):
        """Saves the [Project][ccrenew.dashboard.project.Project] to a serialized pickle in its
        [project_directory][ccrenew.dashboard.project.Project.project_directory].

        Args:
            project_name (str or Project): The name of the [Project][ccrenew.dashboard.project.Project] to pickle.
            store_plots (bool, optional): Option to store any plots that have been drawn with the project to the pickle.

        Raises:
            TypeError: if the wrong type is supplied to `project_name`.
        """
        if isinstance(project_name, list) and not isinstance(project_name, str):
            self.save_pickles(project_name, store_plots=store_plots)
        elif isinstance(project_name, (str, Project)):
            project = self.process_project(project_name)
            project.save_pickle(store_plots=store_plots)
        else:
            raise TypeError("`project_name` must be a string or Project object! Please reformat input and try again.")


    def save_pickles(self, project_list, store_plots=False):
        """Calls [pickle_project()][ccrenew.dashboard.session.DashboardSession.pickle_project]
        for each [Project][ccrenew.dashboard.project.Project] in a list.

        Args:
            project_list (list, str, or Project): List of [Project][ccrenew.dashboard.project.Project] names to pickle.
            store_plots (bool, optional): See [pickle_project()][ccrenew.dashboard.session.DashboardSession.pickle_project].
        """
        if isinstance(project_list, (str, Project)):
            project_name = project_list
            self.save_pickle(project_name, store_plots=store_plots)
        elif isinstance(project_list, list):
            for i, project_name in enumerate(project_list):
                print('*******************************************************')
                print(f'Pickling {project_name} - Project {i+1} of {len(project_list)}.')
                print('*******************************************************')
                self.save_pickle(project_name, store_plots=store_plots)
        else:
            raise TypeError("`project_list` must be a string or Python list! Please reformat input and try again.")


    def pickle_project(self, project_name, store_plots=False):
        """Alias for [save_pickle][ccrenew.dashboard.session.DashboardSession.save_pickle].
        
        Raises:
            FutureWarning: This method will be deprecated in a future version. Use [save_pickle][ccrenew.dashboard.session.DashboardSession.save_pickle] instead.
        """

        warnings.warn('pickle_project will be deprecated in a future version. Please use `save_pickle` instead', FutureWarning)
        self.save_pickle(project_name, store_plots=store_plots)


    def pickle_projects(self, project_list, store_plots=False):
        """Alias for [save_pickles][ccrenew.dashboard.session.DashboardSession.save_pickles].
        Raises:
            FutureWarning: This method will be deprecated in a future version. Use [save_pickle][ccrenew.dashboard.session.DashboardSession.save_pickle] instead.
        warnings.warn('pickle_project will be deprecated in a future version. Please use `save_pickles` instead', FutureWarning)
        """
        self.save_pickles(project_list, store_plots=store_plots)


    def load_pickle(self, project_name, year=None, data_cutoff_date=None, show_plots=False):
        """Loads a pickled [Project][ccrenew.dashboard.project.Project] from file.

        Args:
            project_name (str): The name of the [Project][ccrenew.dashboard.project.Project] to load.
            year (int, optional): Deprecated. Year for the pickle will always load the year to match the session.
            data_cutoff_date (str or datetime): Cutoff date for the [Project][ccrenew.dashboard.project.Project]. When
                loading a project that was pickled some time ago the [data_cutoff_date][ccrenew.dashboard.session.DashboardSession.data_cutoff_date]
                could prevent the data from loading to the current date. Default is None,
                which will reset the [data_cutoff_date][ccrenew.dashboard.session.DashboardSession.data_cutoff_date] to the current day.
            show_plots (bool, optional): Option to show plots if pickle was stored with plots saved.
        """
        year = self.data_source.split('_')[0]
        try:
            project_directory = self.df_keys.query("Project == @project_name")['Folder'].item()
        except IndexError:
            # Log that project was not found
            warn_msg = '"{}" not found in df keys. Please verify the project is present in df keys & the spelling is correct and try again'.format(project_name)
            print(warn_msg)
            # logger.warn(warn_msg)
            return

        pickle_jar = os.path.join(self.dashboard_dir,
                                  project_directory,
                                  project_name,
                                  'Pickle_Jar')
        
        pickle_name = utils.picklefy_project_name(project_name)
        pickle_file = year + "_" + pickle_name + ".pickle"
        pickle_path = os.path.join(pickle_jar, pickle_file)
        
        if self.data_platform == 's3':
            pickle_path = Path(pickle_path).as_posix().replace('s3:/', 's3://')
            fs = s3fs.S3FileSystem()
            open = fs.open
        else:
            open = builtins.open

        with open(pickle_path, 'rb') as f:
            project = pickle.load(f) # type: ignore

        # Check if project version matches session version & re-process if not
        try:
            if project.__version__ != self.__version__:
                project = self.process_project(project_name)
        except:
            project = self.process_project(project_name)

        # Remove plotter object if show_plots=False
        if not show_plots and project.plotter:
            project.plotter.close_plots()

        # Update filepaths to work for any user
        project.dashboard_dir = self.dashboard_dir
        project = self.__update_project_filepaths(project)

        # Update data cutoff date if not explicitly supplied
        if data_cutoff_date:
            try:
                self.data_cutoff_date = parser.parse(data_cutoff_date)
            except:
                self.data_cutoff_date = datetime.today()
        else:
            self.data_cutoff_date = datetime.today()

        # Add project to project_list
        self.project_list[project_name] = project

        # Load neighbor pickles if possible
        # `config_neighbor_sensors` is a set so we'll grab a copy of that & add in `neighbor_sensors`
        all_neighbors = project.config_neighbor_sensors.copy()
        all_neighbors.update(project.neighbor_list)
        for neighbor in all_neighbors:
            if neighbor not in self.project_list:
                self.load_pickle(neighbor)

        return project


    def load_pickles(self, project_list, year=None, data_cutoff_date=None, show_plots=False):
        """Calls [load_pickle()][ccrenew.dashboard.session.DashboardSession.load_pickle]
        for each [Project][ccrenew.dashboard.project.Project] in a list.

        Args:
            project_list (list): List of project names to load.
            year (int): See [load_pickle()][ccrenew.dashboard.session.DashboardSession.load_pickle]
            data_cutoff_date (str or datetime): See [load_pickle()][ccrenew.dashboard.session.DashboardSession.load_pickle]
            show_plots (bool): See [load_pickle()][ccrenew.dashboard.session.DashboardSession.load_pickle]
        """
        if isinstance(project_list, str):
            project_name = project_list
            self.load_pickle(project_name, year=year, data_cutoff_date=data_cutoff_date, show_plots=show_plots)
            return
        elif isinstance(project_list, list):
            for project_name in project_list:
                try:
                    project = self.load_pickle(project_name, year=year, data_cutoff_date=data_cutoff_date, show_plots=show_plots)
                    if project:
                        project.plotter.plot_list = {}
                except:
                    print(f"Error loading pickle for {project_name}")
                    print(traceback.format_exc())

                    continue
        else:
            raise TypeError("`project_name` must be a string or Python list! Please reformat input and try again.")


    def draw_plots(self, project_name:str|Project|ListLike, plot_order=[], reprocess:bool = False,
                        datasub:bool = False, use_solcast:bool = True, *args, **kwargs):
        """Draws plots for the given project.

        Args:
            project_name (str, Project, or list): A project name or list of project names
                to draw plots on for analysis. If a list is supplied it will plot
                the projects one-by-one. The user must press a button in the final
                plot of each project to move on to the next one.
            plot_order (list or str, optional): A list of plots to draw. This can
                be any number of plots from one to all. Defaults to None, which will draw the below plots in the order listed.
            reprocess (bool): Whether to reprocess the data. This option will likely
                be uncommon as any changes to a [Project's][ccrenew.dashboard.project.Project] config file or powertrack file will
                automatically reprocess that data. This could be used if any changes are made
                outside of the config/powertrack file or a change is made to a neighbor.
            datasub (bool): Option to use automatic data substitution algorithm.
            use_solcast (bool): Option to use Solcast data in data sub process. `datasub`
                must be set to `True` for this option to take effect.

        Default Plot Order

        | Plot Alias                | Plot Description                                          |
        |---------------------------|-----------------------------------------------------------|
        |    ``xplot_pwr_poa``      |    Crossplot of power meter & POA data                    |
        |    ``xplot_temp``         |    Crossplot of power meter & POA data, colored by Tamb   |
        |    ``temps``              |    Tcell temperature comparison                           |
        |    ``inv``                |    Inverters                                              |
        |    ``pr``                 |    Hourly Performance Ratio                               |
        |    ``8760``               |    Meter Corrected vs 8760                                |
        |    ``weather``            |    Weather sensors                                        |
        |    ``mtr_corrected``      |    Meter corrections                                      |
        |    ``mtr_dif``            |    Meter correction dif                                   |
        |    ``poas``               |    POA sensors                                            |
        |    ``pwr_poa``            |    Power meter & POA Avg timeseries plot                  |
        |    ``ghi``                |    GHI sensors                                            |
        |    ``irrad``              |    POA & GHI sensors                                      |
        |    ``tz``                 |    Timezone check                                         |
        |    ``losses``             |    Losses  by type                                        |
        |    ``poa_corr``           |    POA correlation check                                  |

        Other Optional Plots

        | Plot Alias                | Plot Description                                          |
        |---------------------------|-----------------------------------------------------------|
        |    ``meters``             |    Original & corrected power and cumulative meters       |
        |    ``native``             |    Native POA/GHI/Tamb/Tmod/Wind sensor subplots          |

        Keyword Args:
            mth (int): The month to show on the Power vs POA crossplot. Defaults to current month.
            default_tool (str): The default tool for navigating around the plots. Options
                are `zoom` and `pan`. Defaults to `zoom`.
            redraw (bool): Option to force the session to redraw the plots.
            open_folder (bool): Option to open the project's folder on the filesystem. Defaults to False.
            close_plots (bool, str, or list): Option to close all or selected open plots.
                If set to True all plots will be closed. If a plot alias or list of plot
                aliases are provided only those plots will be closed. Defaults to True.
            min_date (int, str, or datetime): Option to set a minimum date on the timeseries
                plots. If an integer is supplied the minimum date will be se to that
                many days previous to the current date. If a datetime or string representation
                of a datetime is supplied it will set the minimum date to that date. Defaults to None.
            fullscreen (bool): Option to show plots as fullscreen. Defaults to True.
            screen (int): 1-based index of screen to draw plots on. I.e. a workstation
                with 3 monitors would accept 1, 2, or 3 as an argument.
            poa_onboarding (bool): Plots POA correlation for all months instead of the
                selected month. Defaults to False.
        """
        if isinstance(project_name, (str, Project)):
            redraw = kwargs.get('redraw', False)
            project = self.process_project(project_name, reprocess=reprocess, datasub=datasub, use_solcast=use_solcast)
            neighbor_sensor_data = {self.project_list[neighbor].project_name: self.project_list[neighbor].df_sensors_native_avg for neighbor in project.neighbor_list}
            try:
                if project.errored:
                    raise Exception(f'{project.project_name} encountered an error while processing. Plots cannot be drawn at the moment. Error details:\n{project.error_info}')
            except AttributeError:
                project.errored = False

            try:
                plotter = self.plotters[project_name]
            except KeyError:
                plotter = Plotter(project, neighbor_sensor_data)
                self.plotters[project_name] = plotter

            plotter._update_plotter_neighbors(neighbor_sensor_data)

            if not redraw:
                # Check if the project has an active plotter object & if the plot order is the same
                if plotter.plot_list == plot_order:
                    print('Plots already drawn. Add a new plot to the `plot_list` attribute or set `redraw` = True if you\'d like to redraw the current plots')
                else:
                    plotter.draw_plots(plot_order=plot_order, *args, **kwargs)
            else:
                plotter.draw_plots(plot_order=plot_order, *args, **kwargs)

        elif isinstance(project_name, ListLike):
            project_list = list(project_name)
            project_count = len(project_list)
            for i, project_nm in enumerate(project_list):
                project = self.get_project(project_nm, get_neighbors=False)
                self.draw_plots(project.project_name, *args, **kwargs)
                try:
                    print('Press any key in the last plot window to show plots for {}'.format(project_list[i+1]))
                except IndexError:
                    print('Last plot in the list')
                while True:
                    if i+1 == project_count:
                        break
                    if waitforbuttonpress():
                        break


                
    def __update_project_filepaths(self, project):
        """Sets filepaths for config file, Powertrack file, and Pickle Jar

        Args:
            project (Project): A `ccrenew.dashboard.project.Project`

        Returns:
            Project: a `ccrenew.dashboard.project.Project` with updated filepaths
        """
        # Build filename for config file
        project.config_filepath = project._find_config_file()     

        # Build filename for bool file
        project.bool_filepath = project._find_bool_file()     

        # Build filename for Powertrack file
        project.powertrack_filepath, project.powertrack_csv = project._find_powertrack_file()

        # Build filename for Powertrack csv

        # Check for pickle jar folder & create if it doesn't exist
        project.pickle_jar = project._find_pickle_jar() 
        
        return project
    

    def __prepare_source_data(self, project):

        # Make sure filepath references are correct for config, bool, & Powertrack files + Pickle Jar
        self.__update_project_filepaths(project)

        # If the config file hasn't been updated it will use the data that's already been pulled
        # If the config file has been updated it will read the file & update the data
        self.__update_project_config(project)

        # If the bool file hasn't been updated it will use the data that's already been pulled
        # If the bool file has been updated it will read the file & update the data
        project._load_bool_file()

        # If the powertrack file hasn't been updated it will use the data that's already been pulled
        # If the powertrack file has been updated it will read the file & update the data
        project.load_production_data()

        # fetch_solcast_data()
    

    def __update_project_config(self, project):
        
        # Store the list of sensors before pulling the config file
        sensors = project.Get_Sensor
        project._parse_config_file()

        # Check if new neighbor sensors have been added to the config & pull them if so
        if not sensors.equals(project.Get_Sensor):
            project._find_neighbor_sensors()
            self.__get_neighbor_sensor_data(project)
            
            
    def __get_neighbor_sensor_data(self, project):
        for neighbor_name in project.config_neighbor_sensors:
            # Update production data from neighbor
            try:
                neighbor = self.get_project(neighbor_name, get_neighbors=False)
            except KeyError:
                print(f'Neighbor for {project.project_name} not found: {neighbor_name}. Sensor data for the neighbor will be blank. Check logs to determine why neighbor was not added to DashboardSession')
                continue
            except Exception as e:
                print(f'Neighbor for {project.project_name} errored: {neighbor_name}. Sensor data for the neighbor will be blank. Check logs to determine why neighbor was not added to DashboardSession.\nError details: {e}')
                continue
            
            # Reload neighbor's config or powertrack files if needed
            self.__prepare_source_data(neighbor)

            # Find the columns needed from the neighbor
            sensor_cols = project.Get_Sensor.loc[project.Get_Sensor['Source'] == neighbor_name, 'Value'].tolist()

            # Get the columns from the neighbor
            try:
                neighbor_df = neighbor.df.reindex(index=project.df.index, columns=sensor_cols)
            # If the production data hasn't been loaded for the project
            except AttributeError:
                neighbor.load_production_data()
                neighbor_df = neighbor.df.reindex(index=project.df.index, columns=sensor_cols)
            # If the neighbor errored out during initialization we'll just create a blank df for the neighbor
            except NameError:
                neighbor_cols = [col + '_' + neighbor_name for col in sensor_cols]
                project.df = project.df.reindex(columns = project.df.columns.tolist() + neighbor_cols)
                project.df_sensor_ON = project.df_sensor_ON.reindex(columns = project.df_sensor_ON.columns.tolist() + neighbor_cols)
                return

            neighbor_df.rename(columns=lambda x: str(x) + '_' + neighbor_name, inplace=True)
            neighbor_sensor_ON = neighbor.df_sensor_ON.reindex(index=project.df_sensor_ON.index, columns=sensor_cols)
            neighbor_sensor_ON.columns = neighbor_df.columns.tolist()

            # Add neighbor columns from config file
            project.df = df_update_join(project.df, neighbor_df)
            project.df_sensor_ON = df_update_join(project.df_sensor_ON, neighbor_sensor_ON)
            project.df_sensor_ON = project.df_sensor_ON.reindex(columns=project.df.columns.tolist())

            # Add the neighbor columns to the positional references
            project._locate_column_positions()
