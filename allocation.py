import os
import sys
import xlrd
import time
import logging
import argparse
import editpyxl
import multiprocessing
from pprint import pprint
import graphing as gr

from src.settings import load_settings_from_sheet
from apportionment import apportionment
from src.util import set_logging_level
from src.fetch_location_data import fetch_location_data

ALLOCATION_RESULT_COLUMN = 6

# parser for parameters when running from command line
parser = argparse.ArgumentParser()
parser.add_argument(
    'dir',
    type=str,
    default=os.getcwd(),
    help='first positional argument, input working dir',
    nargs='?'
)
parser.add_argument(
    'input_xlsx',
    type=str,
    default='voting_excel.xlsm',
    #default='voting_excel.xlsm',
    help='first positional argument, input xlsx filepath',
    nargs='?'
)
parser.add_argument(
    '--log',
    type=str,
    default='info',
    help='log level, ex: --log debug'
)


def allocation(location_data: dict, settings: dict, memo: dict = {}) -> dict:
    '''
        Main function for Allocation.
        Makes use of apportionment to keep service reqs close.

        Params:
            location_data (dict) : location data from xlsx,
            settings (dict) : sheet settings,
            memo (dict) : memoization dict.

        Returns:
            (dict) : allocation results by location with expected wait times.
    '''
    print(f'allocation - machines available: {settings["NUM_MACHINES"]}')

    upper_service_req = 500
    lower_service_req = 1
    current_total = 0
    num_iterations = 0
    
    
    while num_iterations < settings['MAX_ITERATIONS'] and \
            abs(settings['NUM_MACHINES'] - current_total) > settings['ACCEPTABLE_RESOURCE_MISS']:
        # next service req to try
        settings['SERVICE_REQ'] = (upper_service_req + lower_service_req) * 0.5

        # running apportionment on all locations
        logging.critical(f'allocation - running apportionment with service req: {settings["SERVICE_REQ"]:.2f}')
        
        results = apportionment(location_data, settings, memo)
        print(results) #Testing
        # collecting new total
        current_total = sum(res['Resource'] for res in results.values())
        logging.critical(f'allocation - used {current_total} machines at service req: {settings["SERVICE_REQ"]:.2f}')

        # updating upper or lower bound
        if settings['NUM_MACHINES'] > current_total:
            upper_service_req = settings['SERVICE_REQ']
        else:
            lower_service_req = settings['SERVICE_REQ']

        num_iterations += 1

    # NOTE: could rerun final service_req 2 or more times here for guarantee
    return results


if __name__ == '__main__':
    multiprocessing.freeze_support()

    args = parser.parse_args()

    set_logging_level(args.log)

    # =========================================================================
    # Setup

    logging.info(f'reading {args.input_xlsx}')
    voting_config = xlrd.open_workbook(args.input_xlsx)

    # get settigns from input xlsx file
    settings = load_settings_from_sheet(voting_config.sheet_by_name(u'options'))

    # get voting location data from input xlsx file
    location_data = fetch_location_data(voting_config, settings)

    manager = multiprocessing.Manager()

    # =========================================================================
    # Main

    start_time = time.perf_counter()

    # execute allocation
    results = allocation(location_data, settings, manager.dict())

    # pretty print the optimization results
    pprint(results)

    # write the results to the excel
    try:
        voting_config = editpyxl.Workbook()
        voting_config.open(args.input_xlsx)
        result_sheet = voting_config.active

        for index in results:
            cell = result_sheet.cell(row=index + 1, column=ALLOCATION_RESULT_COLUMN)
            cell.value = results[index]['Resource']

        tmp_name = f'{args.input_xlsx}-tmp'
        voting_config.save(tmp_name)
        os.remove(args.input_xlsx)
        os.rename(tmp_name, args.input_xlsx)
        os.system('start excel.exe ' + args.input_xlsx)
    except Exception as ex:
        logging.critical(f'runtime: {time.perf_counter()-start_time}')
        print('err: ', ex)
        print('Printing graph...')
        # graphing plots
        gr.graph_voting_plot(results)
        input("Press enter to exit.")
        sys.exit()

    # print runtime and graph for resources allocated
    logging.critical(f'runtime: {time.perf_counter()-start_time}')
    logging.info('Done. Printing graph...')
    gr.graph_voting_plot(results)

    input("Press enter to exit.")
