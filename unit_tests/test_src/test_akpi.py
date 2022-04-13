from audioop import avg
import pytest

from src.settings import default_settings
from src.AKPIp1 import AKPIp1


def test_akpi_type():
    settings = default_settings()

    avgWait, maxWait = AKPIp1(
        0.5,
        1000,
        500,
        6,
        8,
        12,
        200,
        settings
    )

    assert type(avgWait) == float
    assert type(maxWait) == float


def test_akpi_possible():
    settings = default_settings()

    avgWait, maxWait = AKPIp1(
        0.5,
        1000,
        500,
        6,
        8,
        12,
        200,
        settings
    )

    assert maxWait < settings['SERVICE_REQ']


def test_akpi_impossible():
    settings = default_settings()

    avgWait, maxWait = AKPIp1(
        0.5,
        10000,
        5000,
        6,
        8,
        12,
        5,
        settings
    )

    assert maxWait >= settings['SERVICE_REQ']



def test_akpi_low_voters():
    settings = default_settings()

    avgWait, maxWait = AKPIp1(
        0.5,
        100,
        25,
        6,
        8,
        12,
        200,
        settings
    )

    assert maxWait < settings['SERVICE_REQ']


def test_akpi_high_voters():
    settings = default_settings()

    avgWait, maxWait = AKPIp1(
        0.5,
        10000,
        5000,
        6,
        8,
        12,
        200,
        settings
    )

    assert maxWait < settings['SERVICE_REQ']


def test_akpi_low_voting_times():
    settings = default_settings()

    avgWait, maxWait = AKPIp1(
        0.5,
        5000,
        2500,
        2,
        4,
        6,
        200,
        settings
    )

    assert maxWait < settings['SERVICE_REQ']


def test_akpi_high_voting_times():
    settings = default_settings()

    avgWait, maxWait = AKPIp1(
        0.5,
        5000,
        2500,
        8,
        12,
        16,
        200,
        settings
    )

    assert maxWait < settings['SERVICE_REQ']