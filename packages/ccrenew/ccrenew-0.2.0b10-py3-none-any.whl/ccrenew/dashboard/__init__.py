"""
Package for working with Cypress Creek Renewables Dashboard process
"""
import warnings

from pandas.errors import PerformanceWarning
warnings.simplefilter(action='ignore', category=(FutureWarning, PerformanceWarning)) # type: ignore
warnings.filterwarnings(action='ignore', message='divide by zero')

import boto3
from collections import namedtuple
from datetime import datetime
import os
from pathlib import Path


# Create boto s3 client
s3_client = boto3.client('s3')

# Initilize custom mappings
Colmap = namedtuple('Colmap', ['col_list', 'col_avg'])
DataPlatformDirs = namedtuple('DataPlatformDirs', ['sharepoint', 's3'])
S3FilePath = namedtuple('S3FilePath', ['bucket', 'key'])


def make_s3_filepath(filepath:str|Path, obj_type:str) -> S3FilePath:
    filepath = Path(filepath)
    filepath_parts = filepath.parts
    bucket = filepath_parts[1]
    key = '/'.join(filepath_parts[2:])

    # Add a trailing slash for S3 folders
    if obj_type == 'folder':
        key = key + '/'

    s3_filepath = S3FilePath(bucket, key)

    return s3_filepath

def get_modified_time(filepath:str|Path, data_platform:str, obj_type:str='file'):
    if data_platform == 's3':
        s3_filepath = make_s3_filepath(filepath, obj_type=obj_type)
        s3_file = s3_client.get_object(Bucket=s3_filepath.bucket, Key=s3_filepath.key)
        modified_time = s3_file['LastModified']
    else:
        modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))

    return modified_time


print('Importing DashboardSession')
from ccrenew import (
    all_df_keys,
    cloud_data
)
from ccrenew.dashboard.utils.dashboard_utils import func_timer
from ccrenew.data_determination import daylight
from ccrenew.dashboard.plotting.plots import Plotter
from ccrenew.dashboard.session import DashboardSession
from ccrenew.dashboard.project import Project
from ccrenew.dashboard.utils.project_neighbors import (
    find_nearby_projects,
    find_nearby_similar_projects,
    find_similar_projects
)


# Helper functions
class Helpers:
    def __init__(self):
        self.df_keys = all_df_keys
        self.find_nearby_projects = find_nearby_projects
        self.find_nearby_similar_projects = find_nearby_similar_projects
        self.find_similar_projects = find_similar_projects
        self.get_sat_weather = cloud_data.get_sat_weather
        self.daylight = daylight

helpers = Helpers()
