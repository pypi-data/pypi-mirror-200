from datetime import datetime, timedelta
from pathlib import Path

import pytest
from pandas import read_csv

from fao56.clean import eto_daily, eto_hourly, rs_daily, rs_hourly, vpd


def test_eto_daily_compare_to_fig18():
    # longitude = 12.11
    latitude = -5.33
    altitude = 20  # [m]

    # read table
    table_pth = Path(__file__).parent / "etp_table_chap4_fig18.txt"
    with open(table_pth) as f:
        lines = [line.strip() for line in f.readlines() if len(line.strip()) > 0]

    # perform comparison
    for month_ind, line in enumerate(lines[2:]):
        month, t_min, t_max, humidity, wind, sunshine, radiation, eto_ref = line.split()
        date = datetime(2016, month_ind + 1, 1)
        eto = eto_daily(date,
                        latitude,
                        altitude,
                        float(t_min),
                        float(humidity),
                        float(radiation) * 1e6 / (24 * 3600),  # [MJ.m-2.day-1] to [W.m-2]
                        float(wind) * 1000 / (24 * 3600),  # [km.day-1] to [m.s-1]
                        float(t_max))

        assert eto == pytest.approx(float(eto_ref), abs=0.18)


def test_vpd_compare_to_ex18():
    # example 18, FAO, chap.4
    t_max = 21.5
    t_min = 12.3
    rh_max = 84
    rh_min = 63

    assert vpd(t_min, rh_min, t_max, rh_max) == pytest.approx(0.589, abs=1e-3)


def test_vpd_compare_to_ex19():
    # example 19, FAO, chap.4
    t_air = 28
    rh = 90
    assert vpd(t_air, rh) == pytest.approx(0.378, abs=1e-3)

    t_air = 38
    rh = 52
    assert vpd(t_air, rh) == pytest.approx(3.180, abs=1e-3)


def test_rs_daily_compare_to_ex18():
    # example 18, FAO, chap.4
    day = datetime(2017, 7, 6)
    latitude = 50.8
    altitude = 100
    rso = rs_daily(day, latitude, altitude)

    rs_ref = 30.90 * 1e6 / (24 * 3600)  # [MJ.m-2.day-1] to [W.m-2]
    assert rso == pytest.approx(rs_ref, abs=1e-1)


def test_rs_hourly_compare_to_ex19():
    # example 19, FAO, chap.4
    latitude = 16 + 13 / 60  # 16°13'N
    longitude = -(16 + 15 / 60)  # 16°15'W
    altitude = 8

    date = datetime(2017, 10, 1, 14) + timedelta(hours=1)  # correction for time zone wrong in fao
    rso = rs_hourly(date, latitude, longitude, altitude)
    rs_ref = 2.658 * 1e6 / 3600  # [MJ.m-2.h-1] to [W.m-2]
    assert rso == pytest.approx(rs_ref, abs=1e-1)

    date = datetime(2017, 10, 1, 2) + timedelta(hours=1)  # correction for time zone wrong in fao
    rso = rs_hourly(date, latitude, longitude, altitude)
    assert rso == pytest.approx(0, abs=1e-1)


def test_eto_daily_compare_to_ex18():
    # example 18, FAO, chap.4
    t_max = 21.5
    t_min = 12.3
    rh_max = 84
    rh_min = 63

    ws = 2.078
    day = datetime(2017, 7, 6)
    latitude = 50.8
    altitude = 100  # [m]
    rs = 22.07 * 1e6 / (24 * 3600)  # [MJ.m-2.day-1] to [W.m-2]

    eto = eto_daily(day, latitude, altitude, t_min, rh_min, rs, ws, t_max, rh_max)
    assert eto == pytest.approx(3.88, abs=1e-2)


def test_eto_daily_handles_bad_radiation_values():
    t_max = 21.5
    t_min = 12.3
    rh = 75
    ws = 2.078
    day = datetime(2017, 7, 6)
    latitude = 50.8
    altitude = 100  # [m]
    rso = rs_daily(day, latitude, altitude)

    eto_ref = eto_daily(day, latitude, altitude, t_min, rh, rso, ws, t_max)

    # check that etp is cropped for too big values of rg
    for s in (0.1, 0.5, 0.99, 1., 1.1, 2.):
        eto = eto_daily(day, latitude, altitude, t_min, rh, rso * s, ws, t_max)
        assert eto <= eto_ref


def test_eto_daily_is_always_positive():
    latitude = 45
    df_climate = read_csv(Path(__file__).parent / "climate.csv", sep=";", comment="#", index_col='date',
                          parse_dates=True)

    for date, w in df_climate.iterrows():
        rs = w["rg"] * 1e4 / 3600  # [J.cm-2] to [W.m-2]
        assert eto_daily(date, latitude, 0., w["tmin"], w["rh"], rs, w["ws"], w["tmax"]) >= 0


def test_eto_hourly_compare_to_ex19():
    # example 19, FAO, chap.4
    latitude = 16 + 13 / 60  # 16°13'N
    longitude = -(16 + 15 / 60)  # 16°15'W
    altitude = 8

    date = datetime(2017, 10, 1, 14) + timedelta(hours=1)  # correction for time zone wrong in fao

    t_air = 38  # [°C]
    rh = 52  # [%}
    ws = 3.3  # [m.s-1]
    rs = 2.450 * 1e6 / 3600  # [MJ.m-2.h-1] to [W.m-2]
    g = 0.175 * 1e6 / 3600  # [MJ.m-2.h-1] to [W.m-2]

    eto = eto_hourly(date, latitude, longitude, altitude, t_air, rh, rs, ws, g=g)
    assert eto == pytest.approx(0.63, abs=1e-2)
