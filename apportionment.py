from pprint import pprint
from numpy import array
import xlrd
import time
import logging
import argparse
<<<<<<< HEAD
import warnings
from numba import jit
=======
import multiprocessing
>>>>>>> main
from tqdm import tqdm
from multiprocessing import Pool
<<<<<<< HEAD
from typing import List, Union, Optional
import src.global_var
=======

>>>>>>> main
from src.settings import Settings
from src.util import set_logging_level
from src.fetch_location_data import fetch_location_data
from src.evaluate_location import evaluate_location

parser = argparse.ArgumentParser()
parser.add_argument(
    'input_xlsx',
    type=str,
    default='voting_excel.xlsx',
    help='first positional argument, input xlsx filepath',
    nargs='?'
)
parser.add_argument(
    '--log',
    type=str,
    default='info',
    help='log level, ex: --log debug'
)


<<<<<<< HEAD
def apportionment(location_data: array, service_req: float = src.global_var.SERVICE_REQ) -> dict:
=======
def apportionment(location_data: dict, service_req: float = Settings.SERVICE_REQ) -> dict:
>>>>>>> main
    '''
        Runs apportionment against the given locations.

        Params:
            location_data (numpy array) :
                contains the amt of voters and the ballot length for each location,
            service_req (float) : max service requirement.

        Returns:
            (dict) : locations with the min feasible
                resource number and BatchAvg/BatchMaxAvg wait time.
    '''
    
    location_params = [
        (location_data[i], service_req)
        for i in range(Settings.NUM_LOCATIONS)
    ]

    pool = Pool()

    return {
        i : result
        for i, result in enumerate(tqdm(
            pool.imap(evaluate_location, location_params),
            total=len(location_params)
        ))
    }


if __name__ == '__main__':
    multiprocessing.freeze_support()
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

    results = apportionment(location_data)
    pprint(results)
    logging.critical(f'runtime: {time.perf_counter()-start_time}')
    logging.critical('Done.')
    input("Press enter to exit.")
