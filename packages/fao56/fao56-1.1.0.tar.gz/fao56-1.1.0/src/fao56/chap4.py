def eq53(rn, g, temp, ws, es, ea, delta, gamma):
    """Hourly reference evapotranspiration

    Args:
        rn (float): [MJ.m-2.h-1] net radiation at the crop surface
        g (float): [MJ.m-2.h-1] soil heat flux density
        temp (float): [°C] mean air temperature at 2 m height
        ws (float): [m.s-1] wind speed at 2 m height
        es (float): [kPa] saturation vapor pressure
        ea (float): [kPa] actual vapor pressure
        delta (float): [kPa.°C-1] slope relation vapor pressure temperature
        gamma (float): [kPa.°C-1] psychrometric constant

    Returns:
        eto (float): [mm.day-1] reference evapotranspiration
    """
    num = 0.408 * delta * (rn - g) + gamma * 37 / (temp + 273) * ws * (es - ea)
    denom = delta + gamma * (1 + 0.34 * ws)

    return num / denom


def eq54(es, rh):
    """Actual vapour pressure.

    Args:
        es (float): [kPa] saturation vapor pressure
        rh (float): [%] relative humidity

    Returns:
        ea (float): [kPa] actual vapor pressure
    """
    return es * rh / 100
