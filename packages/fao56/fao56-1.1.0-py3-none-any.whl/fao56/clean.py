"""
Cleaner API for some important equations in the book
"""
from datetime import datetime
from math import pi, radians, sqrt

from .chap2 import eq6
from .chap3 import eq11, eq13, eq21, eq23, eq24, eq25, eq28, eq29, eq30, eq32, eq37, eq38, eq39, eq7, eq8
from .chap4 import eq53, eq54


def sat_vap(temp):
    """Saturated vapor pressure

    Args:
        temp (float): [°C] air or organtemperature

    Returns:
        (float): [kPa] Saturated vapor pressure
    """
    return eq11(temp)


def vpd(t_air, rh, t_max=None, rh_max=None):
    """Vapour pressure deficit

    Args:
        t_air (float): [°C] average temperature (or min if t_max is given)
        rh (float): [%] average air humidity (or min is rh_max is given)
        t_max (float): [°C] maximum air temperature
        rh_max (float): [%] maximum air humidity

    Returns:
        vpd (float): [kPa]
    """
    t_min = t_air
    if t_max is None:
        t_max = t_air

    rh_min = rh
    if rh_max is None:
        rh_max = rh

    es_min = eq11(t_min)
    es_max = eq11(t_max)

    ea_min = eq54(es_min, rh_max)
    ea_max = eq54(es_max, rh_min)

    return (es_max + es_min) / 2 - (ea_max + ea_min) / 2


def rs_daily(date, latitude, altitude=0.):
    """Clear sky daily irradiance

    Args:
        date (datetime): Day of computation
        latitude (float): [°] Latitude
        altitude (float): [m] altitude of place

    Returns:
        rso (float): [W.m-2] average radiation during 24h
    """
    doy = (date - datetime(date.year, 1, 1)).days + 1
    dr = eq23(doy)
    decli = eq24(doy)
    sunset_hour = eq25(radians(latitude), decli)

    ra = eq21(dr, sunset_hour, radians(latitude), decli)
    return eq37(ra, altitude) * 1e6 / (24 * 3600)


def rs_hourly(date, latitude, longitude, altitude=0., sunset=None):
    """Clear sky daily irradiance

    Args:
        date (datetime): UTC, beginning of interval, assuming solar time if longitude=0
        latitude (float): [°] Latitude
        longitude (float): [°] Longitude
        altitude (float): [m] altitude of place
        sunset (float): [rad] sunset hour angle, if None, will be computed

    Returns:
        rso (float): [W.m-2] average radiation during 1h
    """
    day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    doy = (day - datetime(date.year, 1, 1)).days + 1
    dr = eq23(doy)
    decli = eq24(doy)
    if sunset is None:
        sunset = eq25(radians(latitude), decli)

    sunrise = -sunset  # by definition in hour angles

    t = (date - day).total_seconds() / 3600 + 0.5  # mid interval
    sc = eq32(doy)
    omega = pi / 12 * ((t + 24 * longitude / 360 + sc) - 12)  # eq31
    omega1 = eq29(omega, 1)
    omega2 = eq30(omega, 1)
    if omega2 <= sunrise:
        return 0.

    if omega1 >= sunset:
        return 0.

    omega1 = max(sunrise, omega1)
    omega2 = min(sunset, omega2)

    ra = eq28(dr, omega1, omega2, radians(latitude), decli)

    return eq37(ra, altitude) * 1e6 / 3600


def eto_daily(date, latitude, altitude, t_air, rh, rs, ws, t_max=None, rh_max=None, atm_pressure=None):
    """Daily reference evapotranspiration.

    Args:
        date (datetime): Day of computation
        latitude (float): [°] Latitude
        altitude (float): [m] altitude of place
        t_air (float): [°C] average temperature (or min if t_max is given)
        rh (float): [%] average air humidity (or min is rh_max is given)
        rs (float): [W.m-2] Daily average solar radiation
        ws (float): [m.s-1] Wind speed at 2 meters above ground
        t_max (float): [°C] maximum air temperature
        rh_max (float): [%] maximum air humidity
        atm_pressure (float): [kPa] Atmospheric pressure

    Returns:
        ETo (float): [mm.day-1] Reference evapotranspiration
    """
    t_min = t_air
    if t_max is None:
        t_max = t_air

    rh_min = rh
    if rh_max is None:
        rh_max = rh

    if atm_pressure is None:
        atm_pressure = eq7(altitude)

    # psychrometric_constant
    gamma = eq8(atm_pressure)

    # Saturation vapor pressure
    es_min = eq11(t_min)
    es_max = eq11(t_max)
    es = (es_min + es_max) / 2.

    # Actual vapor pressure in the air
    ea = (eq54(es_min, rh_max) + eq54(es_max, rh_min)) / 2

    t_mean = (t_max + t_min) / 2

    # Derivative of es [kPa.°C-1]
    delta = eq13(t_mean)

    # net radiation
    rso = rs_daily(date, latitude, altitude) * 24 * 3600e-6  # [W.m-2] to [MJ.m-2.day-1]
    rs = min(rs * 24 * 3600e-6, rso)  # limit measured radiation to clear sky theoretical one
    rns = eq38(rs)

    rnl = eq39(t_min + 273.15, t_max + 273.15, ea, rs, rso)
    rn = max(0., rns - rnl)
    g = 0.

    return eq6(rn, g, t_mean, ws, es, ea, delta, gamma)


def eto_hourly(date, latitude, longitude, altitude, t_air, rh, rs, ws, g=0., atm_pressure=None):
    """Daily reference evapotranspiration.

    Args:
        date (datetime): UTC, beginning of interval, assuming solar time if longitude=0
        latitude (float): [°] Latitude
        longitude (float): [°] Longitude
        altitude (float): [m] altitude of place
        t_air (float): [°C] Mean air temperature
        rh (float): [%] Hourly mean relative humidity (between 0 and 100)
        rs (float): [W.m-2] Hourly average solar radiation
        ws (float): [m.s-1] Wind speed at 2 meters above ground
        g (float): [W.m-2] Ground heat flux
        atm_pressure (float): [kPa] Atmospheric pressure

    Returns:
        ETo (float): [mm.h-1] Reference evapotranspiration
    """
    if atm_pressure is None:
        atm_pressure = eq7(altitude)

    # psychrometric_constant
    gamma = eq8(atm_pressure)

    # Saturation vapor pressure
    es = eq11(t_air)

    # Actual vapor pressure in the air
    ea = eq54(es, rh)

    # Derivative of es [kPa.°C-1]
    delta = eq13(t_air)

    # net radiation
    rso = rs_hourly(date, latitude, longitude, altitude) * 3600e-6  # [W.m-2] to [MJ.m-2.h-1]
    rs = min(rs * 3600e-6, rso)  # limit measured radiation to clear sky theoretical one
    rns = eq38(rs)
    if rso < 1e-6:
        sky_cover_effect = 1.
    else:
        sky_cover_effect = (1.35 * rs / rso - 0.35)

    sigma = 2.043e-10  # [MJ.K-4.m-2.h-1] Stefan-Boltzmann constant
    # eq39 modified for hourly
    rnl = sigma * (t_air + 273.15) ** 4 * (0.34 - 0.14 * sqrt(ea)) * sky_cover_effect

    rn = max(0., rns - rnl)

    return eq53(rn, g * 3600e-6, t_air, ws, es, ea, delta, gamma)
