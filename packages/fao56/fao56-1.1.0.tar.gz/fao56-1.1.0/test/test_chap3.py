from datetime import datetime
from math import radians

import pytest
from fao56.chap3 import eq11, eq13, eq21, eq23, eq24, eq25, eq34, eq38, eq39, eq8


def test_eqs_compare_to_ex17():
    date = datetime(1998, 4, 15)
    latitude = 13 + 44 / 60  # 50°48’N
    t_max = 34.8  # [°C]
    t_min = 25.6  # [°C]
    ea = 2.85  # [kPa]

    atm_pressure = 101.3  # [kPa]

    t_mean = (t_max + t_min) / 2
    delta = eq13(t_mean)
    assert delta == pytest.approx(0.246, abs=1e-3)

    gamma = eq8(atm_pressure)
    assert gamma == pytest.approx(0.0674, abs=1e-4)

    es_max = eq11(t_max)
    assert es_max == pytest.approx(5.56, abs=1e-2)

    es_min = eq11(t_min)
    assert es_min == pytest.approx(3.28, abs=1e-2)

    doy = (date - datetime(date.year, 1, 1)).days + 1
    dr = eq23(doy)
    decli = eq24(doy)
    sunset_hour = eq25(radians(latitude), decli)

    ra = eq21(dr, sunset_hour, radians(latitude), decli)
    assert ra == pytest.approx(38.06, abs=1e-2)

    n = eq34(sunset_hour)
    assert n == pytest.approx(12.31, abs=1e-1)

    rs = 22.65  # [MJ.m-2.day-1]
    rns = eq38(rs)
    assert rns == pytest.approx(17.44, abs=1e-2)

    rso = 28.54  # [MJ.m-2.day-1]
    rnl = eq39(t_min + 273.15, t_max + 273.15, ea, rs, rso)
    assert rnl == pytest.approx(3.11, abs=1e-2)


def test_eqs_compare_to_ex18():
    date = datetime(1998, 7, 6)
    latitude = 50 + 48 / 60  # 50°48’N
    t_max = 21.5  # [°C]
    t_min = 12.3  # [°C]

    atm_pressure = 100.1  # [kPa]

    t_mean = (t_max + t_min) / 2
    delta = eq13(t_mean)
    assert delta == pytest.approx(0.122, abs=1e-3)

    gamma = eq8(atm_pressure)
    assert gamma == pytest.approx(0.0666, abs=1e-4)

    es_max = eq11(t_max)
    assert es_max == pytest.approx(2.564, abs=1e-3)

    es_min = eq11(t_min)
    assert es_min == pytest.approx(1.431, abs=1e-3)

    doy = (date - datetime(date.year, 1, 1)).days + 1
    dr = eq23(doy)
    decli = eq24(doy)
    sunset_hour = eq25(radians(latitude), decli)

    ra = eq21(dr, sunset_hour, radians(latitude), decli)
    assert ra == pytest.approx(41.09, abs=1e-2)

    n = eq34(sunset_hour)
    assert n == pytest.approx(16.1, abs=1e-1)

    rs = 22.07  # [MJ.m-2.day-1]
    rns = eq38(rs)
    assert rns == pytest.approx(17.0, abs=1e-2)

    ea = 1.409  # [kPa]
    rso = 30.9  # [MJ.m-2.day-1]
    rnl = eq39(t_min + 273.15, t_max + 273.15, ea, rs, rso)
    assert rnl == pytest.approx(3.71, abs=1e-2)
