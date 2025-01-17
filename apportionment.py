import os
import sys
import xlrd
import stat
import time
import editpyxl
import logging
import argparse
import multiprocessing
from tqdm import tqdm
from pprint import pprint
from multiprocessing import Pool
import cgi
import graphing as gr

from src.settings import load_settings_from_sheet
from src.util import set_logging_level
from src.fetch_location_data import fetch_location_data
from src.evaluate_location import evaluate_location

APPORTIONMENT_RESULT_COLUMN = 5

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
    help='second positional argument, input xlsx filepath',
    nargs='?'
)
parser.add_argument(
    '--log',
    type=str,
    default='info',
    help='log level, ex: --log debug'
)


def apportionment(location_data: dict, settings: dict, memo: dict = {}) -> dict:
    '''
        Runs apportionment against the given locations in the input excel spreadsheet.

        Params:
            location_data (dict) :
                contains the amt of voters and the ballot length for each location,
            settings (dict) : sheet settings.

        Returns:
            (dict) : locations with the min feasible
                resource number and BatchAvg/BatchMaxAvg wait time.
    '''

    # NOTE: locations start at 1, not 0
    # print("HERE")    
    # print("loc data")
    # pprint(location_data)
    # print(settings['NUM_LOCATIONS'])
    # reads in location data from the spreadsheet
    location_params = [
        (location_data[i + 1], settings, memo)
        for i in range(settings['NUM_LOCATIONS'])
    ]

    # creates a pool of threads and assigns each location to a thread
    pool = Pool()
    return {
        i + 1: result
        for i, result in enumerate(tqdm(
            pool.imap(evaluate_location, location_params),
            total=len(location_params)
        ))
    }


if __name__ == '__main__':
    # WIP - trying to get data from form
    form = cgi.FieldStorage()
    ids = form.getvalue('id')
    print("HELLO")
    print(ids)

    multiprocessing.freeze_support()
    args = parser.parse_args()

    print(args)

    set_logging_level(args.log)
    logging.info(f'Program Initializing...')

    # =========================================================================
    # Setup to read from excel spreadsheet
    
    logging.info(f'reading {args.input_xlsx}')
    print("Current Path: ", os.getcwd())
    print("open_workbook target: ", args.input_xlsx)
    voting_config = xlrd.open_workbook(args.input_xlsx, on_demand=True)

    # get settings from input xlsx file
    temp = voting_config.sheet_by_name(u'options')
    settings = load_settings_from_sheet(voting_config.sheet_by_name(u'options'))

    # get voting location data from input xlsx file
    location_data = fetch_location_data(voting_config, settings)
    pprint(location_data)

    manager = multiprocessing.Manager()

    # =========================================================================

    # =========================================================================
    # WIP: Setup to read in a string

    # id = "1 2 3 4 5"
    # expectedVoters = "100 200 300 400 500"
    # eligibleVoters = "200 400 600 800 1000"
    # ballotLength = "5 7 6 9 12"

    # idT = id.split(" ")
    # exV = expectedVoters.split(" ")
    # elV = eligibleVoters.split(" ")
    # bL = ballotLength.split(" ")
    # locationData = {}

    # for i, x in enumerate(idT):
    #     print(i)
    #     tpl = {'Likely or Exp. Voters': int(exV[i]),  'Eligible Voters': int(elV[i]), 'Ballot Length Measure': int(bL[i])}
    #     locationData[int(x)] = tpl

    # print(locationData)
    # print(location_data)

    # =========================================================================

    # Main

    start_time = time.perf_counter()

    # execute apportionment
    try:
        results = apportionment(location_data, settings, manager.dict())
    except Exception as e:
        logging.info(f'fatal error')
        input()

    # pretty print the optimization results
    pprint(results)

    # write the results to the excel
    try:
        voting_config = editpyxl.Workbook()
        voting_config.open(args.input_xlsx)
        result_sheet = voting_config['locations']

        for index in results:
            cell = result_sheet.cell(row=index + 1, column=APPORTIONMENT_RESULT_COLUMN)
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

    # print runtime and graph for resources apportioned
    logging.critical(f'runtime: {time.perf_counter()-start_time}')
    logging.info('Done. Printing graph...')
    gr.graph_voting_plot(results)

    input("Press enter to exit.")


