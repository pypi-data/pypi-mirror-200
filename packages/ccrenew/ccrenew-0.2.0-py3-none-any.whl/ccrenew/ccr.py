# -*- coding: utf-8 -*-

import numpy as np
import os
import pandas as pd
import re
import smartsheet
from sqlalchemy import create_engine


username = os.path.split(os.path.expanduser("~"))[1]
if username == 'Kevin Anderson':
    # back in my day, C drives were good enough for anyone
    file_project = os.path.join(r'C:\Users', username, r'Box Sync\Cypress Creek Renewables\Asset Management\8) Production Data\_Dashboard_Project')
elif username == 'blumenthal':
    file_project = r'C:\Users\blumenthal\Cypress Creek Renewables\AM-Performance - _Dashboard_Project'
    
elif username == 'Ryan':
    # the co-worker so nice, we elif'd him twice
    file_project = r'E:\Box Sync\Cypress Creek Renewables\Asset Management\8) Production Data\_Dashboard_Project'

elif username == 'MartinWaters':
    file_project = r'C:\Users\MartinWaters\Box Sync\Cypress Creek Renewables\Asset Management\8) Production Data\_Dashboard_Project'
    
elif username == 'EricFitch':
    # RIP
    file_project = r'C:\Users\EricFitch\Box Sync\Cypress Creek Renewables\Asset Management\8) Production Data\_Dashboard_Project'
    
elif username == 'ChristopherDowns':
    file_project=r'C:\Users\ChristopherDowns\Cypress Creek Renewables\AM-Performance - Documents\_Dashboard_Project'
    
elif username == 'PerfEng':
    file_project = r'C:\Users\PerfEng\Cypress Creek Renewables\AM-Performance - Documents\_Dashboard_Project'
    
elif username == 'corey.pullium':
    file_project = r'C:\Users\corey.pullium\Cypress Creek Renewables\AM-Performance - Documents\_Dashboard_Project'
    
elif username == 'MelissaFrench':
    file_project = r'C:\Users\MelissaFrench\Box Sync\Cypress Creek Renewables\Asset Management\8) Production Data\_Dashboard_Project'

elif username == 'StoneHayden':
    file_project = r'C:\Users\StoneHayden\Cypress Creek Renewables\AM-Performance - _Dashboard_Project'
    
elif username == 'PradeepAmireddy':
    file_project = r'C:\Users\PradeepAmireddy\Cypress Creek Renewables\AM-Performance - _Dashboard_Project'
    
elif username == 'AnnaSchmackers':
    file_project = r'C:\Users\AnnaSchmackers\Cypress Creek Renewables\AM-Performance - Documents\_Dashboard_Project'

elif username == 'LukeSain':
    file_project = r'C:\Users\LukeSain\OneDrive - Cypress Creek Renewables\Documents - AM-Performance\_Dashboard_Project'

elif username == 'AndrewCurthoys':
    file_project = r'C:\Users\AndrewCurthoys\Cypress Creek Renewables\AM-Performance - Documents\_Dashboard_Project'

else:
    # saurabh because he likes the D drive better. 
    # Wait...why do I have to be the 'else'. I demand to be the 'if'
    # dude you put yourself there, idk what you're complaining about
    # malarky! there is a plot against me. and I don't mean one of the dashboard variety.
    # typical asset-management performance engineer, playing the victim when he tilted the POA himself
    # RIP
    file_project = r'D:\Box Sync\Cypress Creek Renewables\Asset Management\8) Production Data\_Dashboard_Project'

file_production_data = os.path.split(file_project)[0]
    
def get_sql_engine():
    sql_username = os.environ['BARTERTOWN_USERNAME']
    sql_password = os.environ['BARTERTOWN_PASSWORD']
    encoding_dict = {
        ':': '%3A',
        '/': '%2F',
        '?': '%3F',
        '#': '%23',
        '[': '%5B',
        ']': '%5D',
        '@': '%40',
        '!': '%21',
        '$': '%24',
        '&': '%26',
        "'": '%27',
        '(': '%28',
        ')': '%29',
        '*': '%2A',
        '+': '%2B',
        ',': '%2C',
        ';': '%3B',
        '=': '%3D',
        '%': '%25',
        ' ': '%20',
    }
    pattern = re.compile('|'.join(re.escape(key) for key in encoding_dict.keys()))
    sql_password = pattern.sub(lambda x: encoding_dict[x.group()], sql_password)
    
    host = 'bartertown.cbnrsntwaejm.us-west-2.rds.amazonaws.com'
    port = '5432'
    db = 'thunderdome'
    
    url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'
    url = url.format(sql_username, sql_password, host, port, db)
    
    engine = create_engine(url,pool_pre_ping=True)
    return engine

def get_ss_as_df(sheet_id, drop_col_1=True, start_col=None, index_col=None):
    # API_TOKEN is user-specific, so SS will block you from accessing 
    # sheets that you don't have permissions for
    API_TOKEN = os.environ['SMARTSHEET_TOKEN']

    # Initialize API client
    ss_client = smartsheet.Smartsheet(API_TOKEN)

    # by default, the SS functions will return error objects if you do something wrong 
    # (eg query a nonexistent sheet), instead of raising exceptions
    # if you ask me, that's crazy.  so we tell it to raise exceptions instead
    ss_client.errors_as_exceptions(True)

    cols = ss_client.Sheets.get_columns(sheet_id)
    col_ids, colnames = zip(*((col.id, col.title) for col in cols.result[start_col:]))

    # If an number is provided for the index col we'll find that index in the result list and assign it as the index
    if isinstance(index_col, (int, float)):
        index_col_id, index_colname = cols.result[index_col].id, cols.result[index_col].title
    # If a string is provided for the index col we'll find that column name & assign it as the index
    elif isinstance(index_col, str):
        for col in cols.result:
            if col.title == index_col:
                index_col_id, index_colname = col.id, col.title

    # Add index column to the col list if present
    try:
        col_ids = (index_col_id,) + col_ids # type: ignore
        colnames = (index_colname,) + colnames # type: ignore
    except NameError:
        pass
        
    # Get sheet
    sheet = ss_client.Sheets.get_sheet(sheet_id, column_ids=list(col_ids))
    
    # extract out the cell values into a df
    values = [[cell.value for cell in row.cells] for row in sheet.rows]
    df = pd.DataFrame(values)

    # Drop empty rows
    df = df.dropna(how='all')
    # Fill empty values with np.nan
    df = df.fillna(np.nan)
    
    # df has the data, but the column names are just numbers
    df.columns = list(colnames)

    # bring the index over
    df.index = range(len(df)) # type: ignore
    if drop_col_1:
        del df['Column1']
    
    # Set index if provided
    if index_col:
        df = df.set_index(index_colname) # type: ignore

    return df

def get_df_keys(retired=False):
    # df_keys SS ID
    sheet_id = '8659171076794244'
    all_df_keys = get_ss_as_df(sheet_id)
    all_df_keys = all_df_keys.set_index('Project')
    for col in ['PIS', 'FC']:
        all_df_keys[col] = pd.to_datetime(all_df_keys[col])
        
    if not retired:
        df_keys = all_df_keys.loc[all_df_keys['Retired'] != True, :]
    else:
        df_keys = all_df_keys

    return df_keys
