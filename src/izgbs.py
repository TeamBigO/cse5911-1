import math
import logging
import numpy as np
import scipy.stats as st
from statistics import mean
from src.voter_sim import voter_sim
from src.AKPIp1 import AKPIp1

def voting_time_calcs(ballot_length: int, settings: dict) -> tuple:
    '''
        Calculates the min/mode/max/avg for a given ballot.

        Params:
            ballot_length (int) : ballot length for the location,
            settings (dict) : sheet settings.

        Returns:
            (float) : vote time min,
            (float) : vote time mode,
            (float) : vote time max.
    '''
    vote_min = \
        settings['MIN_VOTING_MIN'] + \
        (settings['MAX_VOTING_MIN'] - settings['MIN_VOTING_MIN']) / \
        (settings['MAX_BALLOT'] - settings['MIN_BALLOT']) * \
        (ballot_length - settings['MIN_BALLOT'])

    vote_mode = \
        settings['MIN_VOTING_MODE'] + \
        (settings['MAX_VOTING_MODE'] - settings['MIN_VOTING_MODE']) / \
        (settings['MAX_BALLOT'] - settings['MIN_BALLOT']) * \
        (ballot_length - settings['MIN_BALLOT'])

    vote_max = \
        settings['MIN_VOTING_MAX'] + \
        (settings['MAX_VOTING_MAX'] - settings['MIN_VOTING_MAX']) / \
        (settings['MAX_BALLOT'] - settings['MIN_BALLOT']) * \
        (ballot_length - settings['MIN_BALLOT'])

    return vote_min, vote_mode, vote_max


def izgbs(
    max_machines: int,
    start_machines: int,
    min_machines: int,
    location_data: dict,
    settings: dict,
    memo: dict = {}
) -> dict:
    '''
        Main IZGBS function.

        Params:
            max_machines (int) : maximum allowed number of machines,
            start_machines (int) : starting number of machines to test,
            min_machines (int) : minimum allowed number of machines,
            location_data (list) : location data,
            settings (dict) : sheet settings,
            memo (dict) : memoization dict.

        Returns:
            (dict) : feasability of each resource amount.
    '''
    # read in parameters from locations dataframe
    max_voters = location_data['Eligible Voters']
    expected_voters = location_data['Likely or Exp. Voters']
    ballot_length = location_data['Ballot Length Measure']

    # calculate voting times
    vote_min, vote_mode, vote_max = voting_time_calcs(ballot_length, settings)
    sas_alpha_value = settings['ALPHA_VALUE'] / math.log2(settings['MAX_MACHINES'] - 1)

    # create a dataframe for total number of machines
    feasible_dict = {
        num_m + 1: {
            'Machines': num_m + 1,
            'Feasible': 0,
            'BatchAvg': 0,
            'BatchMaxAvg': 0,
        }
        for num_m in range(min_machines, max_machines)
    }

    # start with the start value specified
    hypotheses_remain = True
    num_machines = start_machines
    cur_upper = max_machines
    cur_lower = min_machines

    while hypotheses_remain:
        logging.info(f'Current upper bound: {cur_upper}')
        logging.info(f'Current lower bound: {cur_lower}')
        logging.info(f'\tTesting with: {num_machines}')

        # NOTE: this is the inputs to voter_sim(), comma delimited (ballot_length is effectively vote_min/mode/max)
        # NOTE: these all `should` be ints, so '10.0' vs '10' should not be a problem
        key = f'{max_voters},{expected_voters},{ballot_length},{num_machines}'

        # check in memo to see if it already exists, and pull it if so
        if key in memo:
            avg_wait_time_avg, max_wait_time_avg, max_wait_time_std = memo[key]
        else:
            # initialize arrays for batching
            batch_avg_wait_times = [[] for _ in range(settings['NUM_BATCHES'])]
            batch_max_wait_times = [[] for _ in range(settings['NUM_BATCHES'])]

            # =====================================

            # calculate voting times
            for i in range(settings['NUM_REPLICATIONS']):
                wait_times = voter_sim(
                    max_voters=max_voters,
                    expected_voters=expected_voters,
                    vote_time_min=vote_min,
                    vote_time_mode=vote_mode,
                    vote_time_max=vote_max,
                    num_machines=num_machines,
                    settings=settings
                )

                batch_avg_wait_times[i % settings['NUM_BATCHES']].append(mean(wait_times))
                batch_max_wait_times[i % settings['NUM_BATCHES']].append(max(wait_times))

            # =====================================

            # take the batch data and average it
            avg_wait_times = [
                mean(batch)
                for batch in batch_avg_wait_times
            ]
            max_wait_times = [
                mean(batch)
                for batch in batch_max_wait_times
            ]

            # collect statistics
            avg_wait_time_avg = mean(avg_wait_times)
            max_wait_time_avg = mean(max_wait_times)
            max_wait_time_std = np.std(max_wait_times)

            # add the result to the memo
            memo[key] = (avg_wait_time_avg, max_wait_time_avg, max_wait_time_std)

        # populate results
        feasible_dict[num_machines]['BatchAvg'] = avg_wait_time_avg
        feasible_dict[num_machines]['BatchMaxAvg'] = max_wait_time_avg

        # calculate test statistic (p) using traditional binary search
        if max_wait_time_std > 0:  # NOTE: > 0, avoiding divide by 0 error
            z = (max_wait_time_avg - settings['SERVICE_REQ'] + settings['DELTA_INDIFFERENCE_ZONE']) / (max_wait_time_std / math.sqrt(settings['NUM_BATCHES']))
            p = st.norm.cdf(z)

            if p < sas_alpha_value:
                # move to lower half
                for m in feasible_dict:
                    if m >= num_machines:
                        feasible_dict[m]['Feasible'] = 1

                cur_upper = num_machines
                num_machines = math.floor((cur_upper - cur_lower) / 2) + cur_lower
            else:
                # move to upper half
                cur_lower = num_machines
                num_machines = math.floor((cur_upper - num_machines) / 2) + cur_lower
        else:
            # NOTE: this will always be reached if settings['NUM_BATCHES'] == 1 - can cause weird behavior
            # move to lower half
            for m in feasible_dict:
                if m >= num_machines:
                    feasible_dict[m]['Feasible'] = 1

            cur_upper = num_machines
            num_machines = math.floor((cur_upper - cur_lower) / 2) + cur_lower

        # check if there are hypotheses left to test
        hypotheses_remain = cur_lower < cur_upper and cur_lower < num_machines < cur_upper

    logging.info(feasible_dict)

    # start verifying the results with AKPI
    print('\nVerifying results for', location_data, ' using AKPI...')

    # first check the accuracy of the result
    avg_wait1, max_wait1 = AKPIp1(
        sas_alpha_value=sas_alpha_value,
        max_voters=max_voters,
        expected_voters=expected_voters,
        vote_min=vote_min,
        vote_mode=vote_mode,
        vote_max=vote_max,
        num_machines=num_machines+1,
        settings=settings
    )

    # if the result is within service requirements, check 1 machine less to make sure there is not a more optimal solution
    # if the result is not within service requirements, check 1 machine more
    if max_wait1 <= settings['SERVICE_REQ'] :
        if num_machines != 1 :
            avg_wait2, max_wait2 = AKPIp1(
            sas_alpha_value=sas_alpha_value,
            max_voters=max_voters,
            expected_voters=expected_voters,
            vote_min=vote_min,
            vote_mode=vote_mode,
            vote_max=vote_max,
            num_machines=num_machines,
            settings=settings
        )
        else:
            print('\nWarning: Voting locations cannot have less than 2 machines (', location_data, ')')
            avg_wait2 = -1
            max_wait2 = -1
    else:
        avg_wait2, max_wait2 = AKPIp1(
            sas_alpha_value=sas_alpha_value,
            max_voters=max_voters,
            expected_voters=expected_voters,
            vote_min=vote_min,
            vote_mode=vote_mode,
            vote_max=vote_max,
            num_machines=num_machines+2,
            settings=settings
        )

    # bundle the results into tuples
    akpiVerification = (avg_wait1, max_wait1)
    akpiAlternative = (avg_wait2, max_wait2)

    return feasible_dict, num_machines, akpiVerification, akpiAlternative
