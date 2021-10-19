import math
import logging
import numpy as np
from numba import njit
import pandas as pd
import scipy.stats as st
from statistics import mean
import time

from src.settings import Settings
from src.voter_sim import voter_sim


def voting_time_calcs(ballot_length: int) -> tuple:
    '''
        Calculates the min/mode/max/avg for a given ballot.

        Params:
            ballot_length (int) : ballot length for the location.

        Returns:
            (float) : vote time min,
            (float) : vote time mode,
            (float) : vote time max.
    '''
    min_voting_min = Settings.MIN_VOTING_MIN
    min_voting_mode = Settings.MIN_VOTING_MODE
    min_voting_max = Settings.MIN_VOTING_MAX
    min_ballot = Settings.MIN_BALLOT

    max_voting_min = Settings.MAX_VOTING_MIN
    max_voting_mode = Settings.MAX_VOTING_MODE
    max_voting_max = Settings.MAX_VOTING_MAX
    max_ballot = Settings.MAX_BALLOT

    # VotingProcessingMin = MinVotingProcessingMin + (MaxVotingProcessingMin - MinVotingProcessingMin) / (MaxBallot - MinBallot) * (Ballot - MinBallot)
    # VotingProcessingMode = MinVotingProcessingMode + (MaxVotingProcessingMode - MinVotingProcessingMode) / (MaxBallot - MinBallot) * (Ballot - MinBallot)
    # VotingProcessingMax = MinVotingProcessingMax + (MaxVotingProcessingMax - MinVotingProcessingMax) / (MaxBallot - MinBallot) * (Ballot - MinBallot)
    # AverageVotingProcessing = (VotingProcessingMin + VotingProcessingMode + VotingProcessingMax) / 3

    vote_min = \
        min_voting_min + \
        (max_voting_min - min_voting_min) / \
        (max_ballot - min_ballot) * \
        (ballot_length - min_ballot)

    vote_mode = \
        min_voting_mode + \
        (max_voting_mode - min_voting_mode) / \
        (max_ballot - min_ballot) * \
        (ballot_length - min_ballot)

    vote_max = \
        min_voting_max + \
        (max_voting_max - min_voting_max) / \
        (max_ballot - min_ballot) * \
        (ballot_length - min_ballot)

    return vote_min, vote_mode, vote_max


def create_hypotheses_df(num_h):
    '''
        This function creates a dataframe to store hypotheses testing results.

        Params:
            num_h () : TODO.

        Returns:
            TODO
    '''
    # This dataframe will contain 1 record per machine count
<<<<<<< HEAD
    res_cols = ['Machines', 'Feasible', 'BatchAvg', 'BatchAvgMax']
    
=======
    res_cols = ['Machines', 'Feasible', 'Avg', 'MaxAvg']
>>>>>>> main
    # Create an empty dataframe the same size as the locations dataframe
    
    voter_cols = np.zeros((num_h, len(res_cols)))
    # hyp_results = pd.DataFrame(voter_cols, columns=res_cols)
    # hyp_results['Machines'] = (hyp_results.index + 1).astype('int')
    # Populates the Machine count field

    for i in range(num_h):
        voter_cols[i][0] = i+1
    

    # return hyp_results
    return voter_cols


def izgbs(
    max_machines: int,
    start_machines: int,
    min_machines: int,
    sas_alpha_value: float,
    location_data: dict
):
    '''
        Main IZGBS function.

        Params:
            voting_location_num (int) : voting location number,
            max_machines (int) : maximum allowed number of machines,
            start_machines (int) : starting number of machines to test,
            min_machines (int) : minimum allowed number of machines,
            sas_alpha_value (float) : TODO,
            location_data (list) : location data.

        Returns:
            (pd.DataFrame) : feasability of each resource amt.
    '''
    # read in parameters from locations dataframe
    max_voters = location_data['Eligible Voters']
    ballot_length = location_data['Ballot Length Measure']
    arrival_rt = location_data['Arrival Mean']

    # calculate voting times
    vote_min, vote_mode, vote_max = voting_time_calcs(ballot_length)

    # create a dataframe for total number of machines
    feasible_df = create_hypotheses_df(max_machines)

    # start with the start value specified
    hypotheses_remain = True
    num_machines = start_machines
    cur_upper = max_machines
    cur_lower = min_machines

    while hypotheses_remain:
        logging.info(f'Current upper bound: {cur_upper}')
        logging.info(f'Current lower bound: {cur_lower}')
        logging.info(f'\tTesting with: {num_machines}')

        avg_wait_times = []
        max_wait_times = []

        # =====================================

        # TODO: put batch stuff back

        # TODO: use AKPI

        for _ in range(Settings.NUM_REPLICATIONS):
            # calculate voting times
            wait_times = voter_sim(
                max_voters=max_voters,
                vote_time_min=vote_min,
                vote_time_mode=vote_mode,
                vote_time_max=vote_max,
                arrival_rt=arrival_rt,
                num_machines=num_machines
            )

            avg_wait_times.append(mean(wait_times))
            max_wait_times.append(max(wait_times))

        # =====================================

        avg_wait_time_avg = mean(avg_wait_times)
        max_wait_time_avg = mean(max_wait_times)
        max_wait_time_std = np.std(max_wait_times)

        # populate results
<<<<<<< HEAD
        # feasible_df.loc[feasible_df.Machines == num_test, 'BatchAvg'] = avg_wait_time_avg
        # feasible_df.loc[feasible_df.Machines == num_test, 'BatchAvgMax'] = max_wait_time_avg

        
        
        
        
        feasible_df[:,2][feasible_df[:,0] == num_test] = avg_wait_time_avg
        feasible_df[:,3][feasible_df[:,0] == num_test] = max_wait_time_avg
        
        



=======
        feasible_df.loc[feasible_df.Machines == num_machines, 'BatchAvg'] = avg_wait_time_avg
        feasible_df.loc[feasible_df.Machines == num_machines, 'BatchMaxAvg'] = max_wait_time_avg
>>>>>>> main

        # calculate test statistic
        if max_wait_time_std > 0:  # NOTE: avoiding divide by 0 error
            z = (max_wait_time_avg - Settings.SERVICE_REQ + Settings.DELTA_INDIFFERENCE_ZONE) / max_wait_time_std
            p = st.norm.cdf(z)

            # feasible
            if p < sas_alpha_value:
                # move to lower half
<<<<<<< HEAD
                # feasible_df.loc[feasible_df.Machines >= num_test, 'Feasible'] = 1
                feasible_df[:,1][feasible_df[:,0] >= num_test] = 1
                cur_upper = num_test
                num_test = math.floor((cur_upper - cur_lower) / 2) + cur_lower
            else:
                # move to upper half
                # feasible_df.loc[feasible_df.Machines == num_test, 'Feasible'] = 0
                feasible_df[:,1][feasible_df[:,0] == num_test] = 0
                cur_lower = num_test
                num_test = math.floor((cur_upper - num_test) / 2) + cur_lower
        else:
            # move to lower half
            # feasible_df.loc[feasible_df.Machines >= num_test, 'Feasible'] = 1
            feasible_df[:,1][feasible_df[:,0] >= num_test] = 1
            cur_upper = num_test
            num_test = math.floor((cur_upper - cur_lower) / 2) + cur_lower
=======
                feasible_df.loc[feasible_df.Machines >= num_machines, 'Feasible'] = 1
                cur_upper = num_machines
                num_machines = math.floor((cur_upper - cur_lower) / 2) + cur_lower
            else:
                # move to upper half
                feasible_df.loc[feasible_df.Machines == num_machines, 'Feasible'] = 0
                cur_lower = num_machines
                num_machines = math.floor((cur_upper - num_machines) / 2) + cur_lower
        else:
            # move to lower half
            feasible_df.loc[feasible_df.Machines >= num_machines, 'Feasible'] = 1
            cur_upper = num_machines
            num_machines = math.floor((cur_upper - cur_lower) / 2) + cur_lower
>>>>>>> main

        # check if there are hypotheses left to test
        hypotheses_remain = cur_lower < cur_upper and cur_lower < num_machines < cur_upper

    logging.info(feasible_df)
    exit()
    return feasible_df
