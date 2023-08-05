"""
Data and formalisms from FAO56 related to crop evapotranspiration
"""
# {# pkglts, src
# FYEO
# #}
# {# pkglts, version, after src
from . import version

__version__ = version.__version__
# #}

from .clean import eto_daily, eto_hourly, rs_daily, rs_hourly, sat_vap, vpd
