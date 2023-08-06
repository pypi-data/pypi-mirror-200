from __future__ import annotations
import awswrangler as wr
import boto3
from dateutil import parser
import pandas as pd
from pathlib import Path
from multiprocessing.pool import ThreadPool
import os
import s3fs
import time

from ccrenew import (
    all_df_keys as df_keys,
    ccr,
    DateLike,
    Numeric,
    ProjectModelParams,
    AWSError,
)

s3_client = boto3.client('s3')
athena_client = boto3.client("athena")

RAW_DATA_BUCKET = 'perfdatadev.ccrenew.com'
BUCKET_PREFIX_SATELLITE = "5min_archive/Solcats/"
BUCKET_PREFIX_MEASURED = "5min_archive/PF/"
ATHENA_STAGING_DIR = "s3://cypress-perfeng-datalake-onprem-us-west-2/Temp/Athena_Results/"

# https://preview-docs.solcast.com.au/

def query_athena(query:str, database:str, params:list):
    query_response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": database},
        ExecutionParameters=params,
        ResultConfiguration={
            "OutputLocation": ATHENA_STAGING_DIR,
            "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
        },
    )
    while True:
        try:
            # This function only loads the first 1000 rows
            athena_client.get_query_results(
                QueryExecutionId=query_response["QueryExecutionId"]
            )
            break
        except Exception as err:
            if "not yet finished" in str(err):
                time.sleep(0.001)
            else:
                raise err

    results_filename = query_response['QueryExecutionId'] + '.csv'
    results_filepath = ATHENA_STAGING_DIR+results_filename

    df = pd.read_csv(results_filepath)

    return df

def get_sat_weather(project_name:str, start:str|DateLike, end:str|DateLike,
                    convert:bool = False, pool_size:int = 6):
    """
    Query data from AWS to use in irradiance calculations
    
    Args:
        start (str or DateLike): Start date for the data request.
        end (str or DateLike): Start date for the data request.
        convert (bool): Option to convert weather units based on project's config file.
        pool_size (int): Number of threads to use when pulling data directly from S3.
    
    Returns
        df_weather (pd.DataFrame): Weather for the project over the specified days.
    """
    ccr_id, folder = _get_params(project_name)

    if isinstance(start, str):
        start = parser.parse(start)
    if isinstance(end, str):
        end = parser.parse(end)

    df_weather = query_athena(
        query="""SELECT  local_datetime
                        ,ghi
                        ,dni
                        ,dhi
                        ,air_temp
                        ,wind_speed_10m
                   FROM raw_data
                  WHERE ccr_id=?
                    AND local_datetime>=?
                    AND local_datetime<=?
               ORDER BY local_datetime;""",
        params=[f"'{ccr_id}'",
                f"CAST('{start.strftime('%Y-%m-%d')}' AS DATE)",
                f"CAST('{end.strftime('%Y-%m-%d')}' AS DATE)"
                ],
        database='solcast')

    # Drop duplicate dates - most common during DST change in the fall where we re-do 2 AM
    df_weather = df_weather.set_index('local_datetime') # type: ignore
    df_weather.index = pd.to_datetime(df_weather.index)
    df_weather = df_weather[~df_weather.index.duplicated()]

    if df_weather.empty:
        raise AWSError(f"Error querying weather data from AWS")
    else:
        df_weather = df_weather.rename(columns={'wind_speed_10m': 'Wind_speed',
                                                'air_temp': 'Tamb',
                                                'ghi': 'sat_ghi'})

        if convert:
            # Convert units
            folder = folder
            config_file = project_name + r'_Plant_Config_MACRO.xlsm'
            config_path = Path(ccr.file_project) / folder / project_name / 'Plant_Config_File' / config_file
            xl=pd.ExcelFile(config_path)
            df_config=xl.parse('Unit_Tab')
            
            #temp units
            temps = df_config.loc[df_config['Var_ID'].str.contains('amb')]['Convert_Farenheit_to_Celcius'].sum()
            temps += df_config.loc[df_config['Var_ID'].str.contains('mod')]['Convert_Farenheit_to_Celcius'].sum()
            if temps > 0:
                df_weather['Tamb'] = df_weather['Tamb']*float((9/5.))+32.0
                df_weather['Tmod'] = df_weather['Tmod']*float((9/5.))+32.0
            else:
                df_weather['Tamb'] = df_weather['air_temp']
                
            #wind units
            winds = df_config.loc[df_config['Var_ID'].str.contains('speed')]['Convert_mph_to_mps'].sum()
            if winds > 0:
                df_weather['Wind_speed'] = df_weather['wind_speed_10m']*float(2.23694)
            else:
                df_weather['Wind_speed'] = df_weather['wind_speed_10m']

    return df_weather

def get_project_ghi(project_name:str, start:str|DateLike, end:str|DateLike,
                    ghi_index:int = 0, pool_size:int = 6):
    ccr_id, _ = _get_params(project_name)
    keys, (start, end) = _generate_keys(ccr_id, start, end, 'project_ghi')
    df_project_ghi = _s3_pool(pool_size=pool_size, keys=keys)
    ghi_col = [col for col in df_project_ghi.columns if 'GHI' in col][ghi_index]
    df_project_ghi = df_project_ghi[[ghi_col]].rename(columns={ghi_col: 'proj_ghi'})

    return df_project_ghi

def _make_satellite_key(CCR_ID, date):
    return BUCKET_PREFIX_SATELLITE + CCR_ID + "/" + "sat_weather_" + date.strftime('%Y-%m-%d') + ".csv"

def _make_project_key(CCR_ID, date):
    return BUCKET_PREFIX_MEASURED + CCR_ID + "/" + "main_" + date.strftime('%Y-%m-%d') + ".csv"

def _retrieve_df(key):
    fs = s3fs.S3FileSystem(anon=False)
    path = "s3://{b}/{k}".format(b=RAW_DATA_BUCKET, k=key)
    try:
        with fs.open(path, 'rb') as f:
            df = pd.read_csv(f, index_col = 0, parse_dates = True)
            df = df.loc[~df.index.duplicated(), :]
    except FileNotFoundError:
        df = pd.DataFrame()
    return df

def _get_project_model_params(project_name:str) -> ProjectModelParams:

    df_proj_keys = df_keys.query("Project == @project_name").to_dict('records')[0]

    project_params = ProjectModelParams(
        project_name,
        df_proj_keys['CCR_ID'],
        df_proj_keys['Folder'],
        f"US/{df_proj_keys['Timezone']}",
        df_proj_keys['GPS_Lat'],
        df_proj_keys['GPS_Long'],
        df_proj_keys['Elevation'],
        df_proj_keys['MWDC'],
        df_proj_keys['Racking'],
        df_proj_keys['Tilt/GCR'],
        df_proj_keys['Max_angle'],
        df_proj_keys['Temp_Coeff_Pmax'],
        df_proj_keys['a_module'],
        df_proj_keys['b_module'],
        df_proj_keys['Delta_Tcnd'],
    )

    return project_params

def _get_params(project_name:str):
    project_params = df_keys.query("index == @project_name").to_dict(orient='records')[0]
    ccr_id = project_params['CCR_ID']
    folder = project_params['Folder']

    return ccr_id, folder

def _generate_keys(ccr_id:str, start:str|DateLike, end:str|DateLike, type: str):
    if isinstance(start, str):
        start = parser.parse(start)
    if isinstance(end, str):
        end = parser.parse(end)
    date_range = pd.date_range(start, end, normalize=True)

    if type == 'satellite':
        keys = [_make_satellite_key(ccr_id, date) for date in date_range]
    else:
        keys = [_make_project_key(ccr_id, date) for date in date_range]

    return keys, (start, end)

def _s3_pool(pool_size, keys):
    pool_size = 6
    pool = ThreadPool(pool_size)
    day_df_list = pool.map(_retrieve_df, keys)
    pool.close()
    pool.join()
    
    df_sat_weather = pd.concat(day_df_list, axis=0)
    return df_sat_weather

