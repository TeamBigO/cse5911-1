<<<<<<< HEAD
from posixpath import join
from pandas.core.frame import DataFrame

import sys
=======
>>>>>>> main
import xlrd
import math
import time
import logging
import argparse
<<<<<<< HEAD
import numpy as np
import pandas as pd
from numba import njit
=======
import warnings

>>>>>>> main
from tqdm import tqdm
<<<<<<< HEAD
from concurrent.futures import ThreadPoolExecutor
=======
from pprint import pprint
>>>>>>> main
from multiprocessing import Pool
from typing import List, Union, Optional

from src.settings import Settings
from src.util import set_logging_level
from src.fetch_location_data import fetch_location_data
from src.evaluate_location import evaluate_location
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning, NumbaWarning

warnings.simplefilter('ignore', category=NumbaWarning)
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

parser = argparse.ArgumentParser()
parser.add_argument(
    'input_xlsx',
    type=str,
    help='first positional argument, input xlsx filepath'
)
parser.add_argument(
    '--log',
    type=str,
    default='info',
    help='log level, ex: --log debug'
)

def apportionment(location_data: dict) -> dict:
    '''
        Runs apportionment against the given locations.

        Params:
            location_data (dict) :
                contains the amt of voters and the ballot length for each location.

        Returns:
            (dict) : locations with the min feasible
                resource number and BatchAvg/BatchMaxAvg wait time.
    '''
<<<<<<< HEAD
    res_cols = ['Resource', 'Exp. Avg. Wait Time', 'Exp. Max. Wait Time']
    # Create an empty dataframe the same size as the locations dataframe
    voter_cols = np.zeros((vote_locs, len(res_cols)))
    
    loc_results = pd.DataFrame(voter_cols, columns=res_cols)
    # Populates the location ID field
    loc_results['Locations'] = (loc_results.index + 1).astype('str')
    return loc_results


def populate_result_df(results: list, result_df: DataFrame) -> None:
    '''
        Store IZGBS run results in loc_df_results.

        Params:
            results (list) : lists of result from izgbs,
            result_df (DataFrame) : an empty dataframe intended to host results.

        Returns:
            None.
    '''
    for result in results:
        result_df.loc[
            result_df.Locations == str(result['i']),
            'Resource'
        ] = result['Resource']
=======
    # NOTE: locations start at 1, not 0
    location_params = [
        location_data[i + 1]
        for i in range(Settings.NUM_LOCATIONS)
    ]
>>>>>>> main

    pool = Pool()

    return {
        i + 1: result
        for i, result in enumerate(tqdm(
            pool.imap(evaluate_location, location_params),
            total=len(location_params)
        ))
    }


if __name__ == '__main__':
    args = parser.parse_args()

    set_logging_level(args.log)

    # =========================================================================
    # Setup

    logging.info(f'reading {args.input_xlsx}')
    voting_config = xlrd.open_workbook(args.input_xlsx)

    # get voting location data from input xlsx file
    location_data = fetch_location_data(voting_config)

    # =========================================================================
    # Main

    start_time = time.perf_counter()

<<<<<<< HEAD
    location_params = [
        [location_data, i]
        for i in range(1, Settings.NUM_LOCATIONS)
    ]
    

    '''
    # attempt to use various multiprocess techniques for speed testing

    # attemp 1
    pool = Pool()
    results = pool.map(evaluate_location, location_params);
    pool.close()
    pool.join()
    resutls = [entry for result in results for entry in result]

    # attempt 2
    with ThreadPoolExecutor(12) as ex:
        results =[
            result 
            for result in tqdm(
                ex.map(evaluate_location, location_params),
                total=len(location_params)
            )
        ]
    '''
    pool = Pool()
    results = [
        result 
        for result in tqdm(
            pool.imap(evaluate_location, location_params),
            total=len(location_params)
        )
    ]
    
    populate_result_df(results, loc_df_results)
=======
    for location in location_data.values():
        location['NUM_MACHINES'] = Settings.MAX_MACHINES

    results = apportionment(location_data)
>>>>>>> main

    pprint(results)

    logging.critical(f'runtime: {time.perf_counter()-start_time}')
    logging.critical('Done.')
