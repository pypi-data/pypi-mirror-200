from concurrent.futures import (
    as_completed,
    ProcessPoolExecutor)
from functools import partial
import os
import time
import traceback


def process_pool(kwargslist):

    # We'll use half of the available processors for the machine to not completely bog it down.
    max_workers = int(os.cpu_count()/2)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # We'll set up `process_batch` as a partial so it will execute in parallel for each set of kwargs in the kwargslist
        process_project = partial(_process_batch)
        futures = [executor.submit(process_project, **kwargs) for kwargs in kwargslist]
        for future in as_completed(futures):
            result = future.result()
            project_name = result['project_name']
            error_info = result['error_info']
            project_num = result['project_num']
            project_total = result['project_total']
            project_time = result['project_time']
            batch_time = result['batch_time']
            if error_info:
                print('*************************************************************************************************************************')
                print("***** ERROR *****")
                print("***** ERROR *****")
                print(f'    Error encountered while processing "{project_name}". Project #{project_num} of {project_total}. Error details: {error_info}')
                print("***** ERROR *****")
                print("***** ERROR *****")
                print('*************************************************************************************************************************')
            else:
                print('*************************************************************************************************************************')
                print(f"Completed {project_name}. Project #{project_num} of {project_total} processed. Time to process: {project_time:.2f}s. Total elapsed time: {batch_time:.2f}s")
                print('*************************************************************************************************************************')
        
        return futures


def _process_batch(**kwargs):
    project_start = time.time()

    # Collect kwargs
    session = kwargs.get('session')
    data_source = kwargs.get('data_source')
    project_name = kwargs.get('project_name')
    reprocess = kwargs.get('reprocess')
    data_sub = kwargs.get('data_sub')
    use_solcast = kwargs.get('use_solcast')
    project_num = kwargs.get('project_num')
    project_total = kwargs.get('project_total')
    batch_start = kwargs.get('batch_start')

    # Initialize new session
    session = session(data_source=data_source)

    # Process project
    project = session.process_project(project_name=project_name, reprocess=reprocess, data_sub=data_sub, use_solcast=use_solcast)
    project_time = time.time()-project_start
    batch_time = time.time()-batch_start

    # Return dict for parsing the results
    return {'project_list': session.project_list.items(),
            'project_name': project_name,
            'project_num': project_num,
            'error_info': project.error_info,
            'project_total': project_total,
            'project_time': project_time,
            'batch_time': batch_time
    }


def export_pool(kwargslist):

    # We'll use half of the available processors for the machine to not completely bog it down.
    max_workers = int(os.cpu_count()/2)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # We'll set up `process_batch` as a partial so it will execute in parallel for each set of kwargs in the kwargslist
        export_project = partial(_export_batch)
        futures = [executor.submit(export_project, **kwargs) for kwargs in kwargslist]
        for future in as_completed(futures):
            # Collect results for updating progress
            result = future.result()
            project_name = result['project_name']
            error_info = result['error_info']
            project_num = result['project_num']
            project_total = result['project_total']
            project_time = result['project_time']
            batch_time = result['batch_time']

            if error_info:
                print('*************************************************************************************************************************')
                print("***** ERROR *****")
                print("***** ERROR *****")
                print(f"    Error encountered while exporting {project_name}. Project #{project_num} of {project_total}. Error details: {error_info}")
                print("***** ERROR *****")
                print("***** ERROR *****")
                print('*************************************************************************************************************************')
            else:
                print('*************************************************************************************************************************')
                print(f"Completed {project_name}. Project #{project_num} of {project_total} exported. Time to export: {project_time:.2f}s. Total elapsed time: {batch_time:.2f}s")
                print('*************************************************************************************************************************')
        
        return futures


def _export_batch(**kwargs):
    project_start = time.time()

    # Collect kwargs
    session = kwargs.get('session')
    data_source = kwargs.get('data_source')
    project_name = kwargs.get('project_name')
    func_args = kwargs.get('func_args')
    project_num = kwargs.get('project_num')
    project_total = kwargs.get('project_total')
    batch_start = kwargs.get('batch_start')

    # Initialize new session
    session = session(data_source=data_source)

    # Process project
    error_info = ''
    try:
        session.export_project(project_name=project_name, **func_args)
    except:
        error_info = traceback.format_exc()

    project_time = time.time()-project_start
    batch_time = time.time()-batch_start

    # Return dict for parsing the results
    return {'project_list': session.project_list.items(),
            'project_name': project_name,
            'error_info': error_info,
            'project_num': project_num,
            'project_total': project_total,
            'project_time': project_time,
            'batch_time': batch_time
    }