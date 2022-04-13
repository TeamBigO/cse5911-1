import math

from src.izgbs import izgbs

def evaluate_location(inputs: tuple) -> dict:
    '''
        Runs IZGBS (Indifference Zone Generated Binary Search) on a specified location.

        Params:
            inputs (tuple) : location data, settings, memo.

        Returns:
            (dict) : results.
    '''
    location_data, settings, memo = inputs

    best_result = {}

    # set start value to half the ceiling
    start_val = math.ceil((settings['MAX_MACHINES'] - 1) / 2)

    # run IZBGS on current parameters
    loc_res, num_machines, akpiVerification, akpiAlternative = izgbs(
        settings['MAX_MACHINES'],
        start_val,
        settings['MIN_MACHINES'],
        location_data,
        settings,
        memo
    )

    # create feasible matrix
    loc_feas = []

    # if results are feasible, add them to the feasible matrix
    for key, value in loc_res.items():
        if value['Feasible'] == 1:
            loc_feas.append(value)

    # if there are feasible results
    if len(loc_feas) > 0:
        machines_value = []

        for result in loc_feas:
            machines_value.append(result['Machines'])

        # find fewest feasible machines
        mach_min = min(machines_value)

        # keep the feasible setup with the fewest number of machines
        loc_feas_min = {}

        for key, value in loc_res.items():
            if value['Machines'] == mach_min:
                loc_feas_min = value
                break

        # populate overall results with info for this location
        best_result['Resource'] = mach_min
        best_result['Exp. Avg. Wait Time'] = loc_feas_min['BatchAvg']
        best_result['Exp. Max. Wait Time'] = loc_feas_min['BatchMaxAvg']

    else:
        # no feasible setups, find lowest wait time (should work out to be max machines allowed)
        max_avg = []
        min_index = 0

        for key, result in loc_res.items():
            max_avg.append(result['BatchMaxAvg'])
            min_index = key

        loc_res_min = loc_res[min_index]

        # populate overall results with info for this location
        best_result['Resource'] = loc_res_min['Machines']
        best_result['Exp. Avg. Wait Time'] = loc_res_min['BatchAvg']
        best_result['Exp. Max. Wait Time'] = loc_res_min['BatchMaxAvg']

    # populate AKPI results with returned AKPI info
    best_result['AKPI Check AVG'] = akpiVerification[0]
    best_result['AKPI Check MAX'] = akpiVerification[1]
    best_result['AKPI ALT AVG'] = akpiAlternative[0]
    best_result['AKPI ALT MAX'] = akpiAlternative[1]

    # check the result against the alternative and replace the result if the alternative is better
    if akpiAlternative[1] < settings['SERVICE_REQ'] and akpiAlternative[0] > 0:
        best_result['Resource'] = num_machines
        best_result['Exp. Avg. Wait Time'] = akpiAlternative[0]
        best_result['Exp. Max. Wait Time'] = akpiAlternative[1]
        print('\nAKPI Alternative was selected for', location_data)

    return best_result
