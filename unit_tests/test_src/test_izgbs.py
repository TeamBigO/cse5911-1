import pytest

from src.settings import default_settings
from src.izgbs import izgbs, voting_time_calcs

#good
def test_voting_time_calcs_default1():
    _min, _mode, _max = voting_time_calcs(10, default_settings())

    assert _min == 6 and _mode == 10 and _max == 20

#this will take a while due to the checks. the dict before settings is the location data. #are the eligible voters not backwards?
def test_izgbs_full_run1():
    settings = default_settings()

    results = izgbs(
        200,
        100,
        1,
        {
            'Eligible Voters': 1000,
            'Likely or Exp. Voters': 2000,
            'Ballot Length Measure': 10
        },
        settings
    )
    #modified to add [0]. also added a 0 to both eligible voters and likely voters. 
    assert type(results[0]) == dict

#added 0 to end of numbers of voters.
def test_izgbs_atleast_one_feasible():
    settings = default_settings()

    results = izgbs(
        200,
        100,
        1,
        {
            'Eligible Voters': 1000,
            'Likely or Exp. Voters': 2000,
            'Ballot Length Measure': 10
        },
        settings
    )

    assert any(v['Feasible'] for v in results[0].values())


def test_izgbs_no_infeasible_after_first_feasible():
    settings = default_settings()

    results = izgbs(
        200,
        100,
        1,
        {
            'Eligible Voters': 1000,
            'Likely or Exp. Voters': 2000,
            'Ballot Length Measure': 10
        },
        settings
    )

    results = list(results[0].values())
    first_feasible = None

    for i, res in enumerate(results):
        if res['Feasible']:
            first_feasible = i
            break

    assert all(res['Feasible'] for res in results[first_feasible:])

#this one is taking a long time. was (1,2,3)
def test_izgbs_can_return_all_infeasible():
    settings = default_settings()

    results = izgbs(
        27,
        25,
        23,
        {
            'Eligible Voters': 10000,
            'Likely or Exp. Voters': 20000,
            'Ballot Length Measure': 100
        },
        settings
    )

    assert not any(v['Feasible'] for v in results[0].values())

#this one will also take a long long time.
#was 4, 3, 1
def test_izgbs_all_feasible_with_inf_service_req():
    settings = default_settings()

    settings['SERVICE_REQ'] = float('inf')

    results = izgbs(
        27,
        25,
        23,
        {
            'Eligible Voters': 10000,
            'Likely or Exp. Voters': 20000,
            'Ballot Length Measure': 100
        },
        settings
    )

    assert all(v['Feasible'] for v in results[0].values())


def test_izgbs_feasible_dict_size_determined_by_num_machines():
    settings = default_settings()

    upper = 400
    lower = 10
    results = izgbs(
        upper,
        11,
        lower,
        {
            'Eligible Voters': 10000,
            'Likely or Exp. Voters': 20000,
            'Ballot Length Measure': 100
        },
        settings
    )

    assert len(results[0]) == upper - lower


def test_izgbs_feasible_dict_contains_correct_machine_nums():
    settings = default_settings()

    upper = 400
    lower = 10
    results = izgbs(
        upper,
        11,
        lower,
        {
            'Eligible Voters': 10000,
            'Likely or Exp. Voters': 20000,
            'Ballot Length Measure': 100
        },
        settings
    )

    assert list(results[0].keys()) == [*range(lower + 1, upper + 1)]


def test_izgbs_bad_start_raises_1():
    settings = default_settings()

    with pytest.raises(Exception):
        izgbs(
            400,
            3,
            10,
            {
                'Eligible Voters': 10000,
                'Likely or Exp. Voters': 20000,
                'Ballot Length Measure': 100
            },
            settings
        )


def test_izgbs_bad_start_raises_2():
    settings = default_settings()

    with pytest.raises(Exception):
        izgbs(
            400,
            403,
            10,
            {
                'Eligible Voters': 10000,
                'Likely or Exp. Voters': 20000,
                'Ballot Length Measure': 100
            },
            settings
        )