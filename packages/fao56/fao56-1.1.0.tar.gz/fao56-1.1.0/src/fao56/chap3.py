from math import acos, cos, exp, pi, sin, sqrt, tan

gsc = 0.082  # [MJ.m-2.min-1] solar constant


def eq7(z):
    """Atmospheric pressure.

    Args:
        z (float): [m] altitude above sea level

    Returns:
        P (float): [kPa] atmospheric pressure
    """
    return 101.3 * ((293 - 0.0065 * z) / 293) ** 5.26


def eq8(p):
    """Psychrometric constant

    Args:
        p (float): [kPa] atmospheric pressure

    Returns:
        gamma (float): [kPa.°C-1]
    """
    return 0.665e-3 * p


def eq11(temp):
    """Mean saturation vapour pressure

    Args:
        temp (float): [°C] air temperature

    Returns:
        es (float): [kPa]
    """
    return 0.6108 * exp(17.27 * temp / (temp + 237.3))


def eq13(temp):
    """Slope of saturation vapour pressure curve

    Args:
        temp (float): [°C] air temperature

    Returns:
        delta (float): [kPa.°C-1]
    """
    return 4098 * eq11(temp) / (temp + 237.3) ** 2


def eq21(dr, sunset_hour, latitude, delta):
    """Extraterrestrial radiation for daily periods.

    Args:
        dr (float): [-] inverse relative distance earth sun
        sunset_hour (float): [rad] sunset hour angle
        latitude (float): [rad]
        delta (float): [rad] solar declination

    Returns:
        Ra (float): [MJ.m-2.day-1]
    """
    corr = sunset_hour * sin(latitude) * sin(delta) + cos(latitude) * cos(delta) * sin(sunset_hour)
    return 24 * 60 / pi * gsc * dr * corr


def eq23(j):
    """Inverse relative distance Earth-Sun.

    Args:
        j (float): [-] number of the day in the year ranging from 1 (1 January)
                   to 365 or 366 (31 December)

    Returns:
        dr (float)
    """
    return 1 + 0.033 * cos(2 * pi * j / 365)


def eq24(j):
    """Solar declination.

    Args:
        j (float): [-] number of the day in the year ranging from 1 (1 January)
                   to 365 or 366 (31 December)

    Returns:
        delta (float)
    """
    return 0.409 * sin(2 * pi * j / 365 - 1.39)


def eq25(latitude, delta):
    """Sunset hour angle

    Args:
        latitude (float): [rad]
        delta (float): [-] solar declination

    Returns:
        omega_s (float): [rad]
    """
    return acos(-tan(latitude) * tan(delta))


def eq28(dr, omega1, omega2, latitude, delta):
    """Extraterrestrial radiation for daily periods.

    Args:
        dr (float): [-] inverse relative distance earth sun
        omega1 (float): [rad] solar time angle at beginning of period
        omega2 (float): [rad] solar time angle at end of period
        latitude (float): [rad]
        delta (float): [rad] solar declination

    Returns:
        Ra (float): [MJ.m-2.h-1]
    """
    corr = (omega2 - omega1) * sin(latitude) * sin(delta) + cos(latitude) * cos(delta) * (sin(omega2) - sin(omega1))
    return 12 * 60 / pi * gsc * dr * corr


def eq29(omega, t_length):
    """Solar time angle at beginning of period.

    Args:
        omega (float): [rad] solar time angle at midpoint of period
        t_length (float): [h] length of period

    Returns:
        omega1 (float): [rad]
    """
    return omega - pi * t_length / 24


def eq30(omega, t_length):
    """Solar time angle at end of period.

    Args:
        omega (float): [rad] solar time angle at midpoint of period
        t_length (float): [h] length of period

    Returns:
        omega1 (float): [rad]
    """
    return omega + pi * t_length / 24


def eq31(t, longitude_zone, longitude, sc):
    """Solar time angle at given time.

    Args:
        t (float): [h] standard clock time
        longitude_zone (float): [°] Longitude of the centre of the local time zone
        longitude (float): [°] longitude of measurement site
        sc (float): [h] seasonal correction for solar time

    Returns:
        omega (float): [rad]
    """
    return pi / 12 * ((t + 0.06667 * (longitude_zone - longitude) + sc) - 12)


def eq32(j):
    """Seasonal correction for solar time.

    Args:
        j (float): [-] number of the day in the year ranging from 1 (1 January)
                   to 365 or 366 (31 December)

    Returns:
        sc (float): [h]
    """
    b = 2 * pi * (j - 81) / 364  # eq33
    return 0.1645 * sin(2 * b) - 0.1255 * cos(b) - 0.025 * sin(b)


def eq34(omega_s):
    """Daylight hours.

    Args:
        omega_s (float): [rad] sunset hour angle

    Returns:
        N (float): [h]
    """
    return 24 * omega_s / pi


def eq37(ra, z):
    """Clear sky solar radiation.

    Args:
        ra (float): [MJ.m-2.day-1] Extraterrestrial radiation for daily periods
        z (float): [m] station elevation above sea level

    Returns:
        rso (float)
    """
    return (0.75 + 2e-5 * z) * ra


def eq38(rs, albedo=0.23):
    """Net shortwave radiation.

    Args:
        rs (float): [MJ.m-2.day-1] net solar or shortwave radiation
        albedo (float): [-] canopy reflection coefficient

    Returns:
        Rns (float):
    """
    return (1 - albedo) * rs


def eq39(t_min, t_max, ea, rs, rso):
    """Net outgoing longwave radiation

    Args:
        t_min (float): [K] min absolute temperature during the day
        t_max (float):  [K] max absolute temperature during the day
        ea (float): [kPa] actual vapor pressure
        rs (float): [MJ.m-2.day-1] solar radiation
        rso (float): [MJ.m-2.day-1] clear-sky radiation

    Returns:
        Rnl (float): [MJ.m-2.day-1]
    """
    alpha = 4.903e-9  # [MJ.K-4.m-2.day-1] Stefan-Boltzmann constant
    return alpha * (t_max ** 4 + t_min ** 4) / 2 * (0.34 - 0.14 * sqrt(ea)) * (1.35 * rs / rso - 0.35)
