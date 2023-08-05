"""Market data processing tools."""
# from __future__ import absolute_import
# from xlrd.biffh import XLRDError

import pandas as pd
import numpy as np
import os
import logging


def read_caiso_data(fpath, year, month, nodeid):
    """Read the historical LMP, regulation up/down and regulation mileage up/down and return NumPy ndarrays for those three prices.

    :param fpath: The path to the root of the PJM data directory
    :type fpath: str
    :param year: Year of data to read
    :type year: int or str
    :param month: Month of data to read
    :type month: int or str
    :param nodeid: ID of the node to read
    :type nodeid: str
    :return: daLMP, RegCCP, RegPCP: Hourly LMP and regulation capacity/performance clearing price values.
    :rtype: NumPy ndarrays

    Note-
    1. For CAISO certain prices have:
    _CAISO
    _CAISO_EXP
    _NP26
    _NP26_EXP
    _SP26
    _SP26_EXP

    2. we only use the _CAISO_EXP ones for mileage prices as they are the only ones

    AS_CAISO_EXP_RD_CLR_PRC
    AS_CAISO_EXP_RU_CLR_PRC

    AS_CAISO_EXP_RMD_CLR_PRC
    AS_CAISO_EXP_RMU_CLR_PRC
    """
    daLMP = np.empty([0])
    daREGU = np.empty([0])
    daREGD = np.empty([0])
    daRMU = np.empty([0])
    daRMD = np.empty([0])
    RMU_MM = np.empty([0])
    RMD_MM = np.empty([0])
    RMU_PACC = np.empty([0])
    RMD_PACC = np.empty([0])

    if isinstance(month, str):
        month = int(month)

    if isinstance(year, str):
        year = int(year)

    # Names examples:
    # 201601_dalmp_LAKESID2_7_UNITS-APND.csv
    # 201601_asp.csv
    # 201601_regm.csv
    fnameLMP = "{0:d}{1:02d}_dalmp_{2:s}.csv".format(year, month, nodeid)
    fnameASP = "{0:d}{1:02d}_asp.csv".format(year, month)
    fnameMILEAGE = "{0:d}{1:02d}_regm.csv".format(year, month)

    fname_path_LMP = os.path.join(fpath, "LMP", str(nodeid), str(year), fnameLMP)
    fname_path_ASP = os.path.join(fpath, "ASP", str(year), fnameASP)
    fname_path_MILEAGE = os.path.join(fpath, "MILEAGE", str(year), fnameMILEAGE)

    try:
        dfLMP = pd.read_csv(fname_path_LMP, index_col=False)
        daLMP = dfLMP["LMP"].values
    except FileNotFoundError:
        logging.warning(
            "read_caiso_data: No LMP data matching input parameters found, returning empty array. (got {fname}, {year}, {month}, {nodeid})".format(
                fname=fnameLMP, year=year, month=month, nodeid=nodeid
            )
        )

    try:
        dfASP = pd.read_csv(fname_path_ASP, index_col=False)
        daREGU = dfASP["AS_CAISO_EXP_RU_CLR_PRC"].values
        daREGD = dfASP["AS_CAISO_EXP_RD_CLR_PRC"].values
        daRMU = dfASP["AS_CAISO_EXP_RMU_CLR_PRC"].values
        daRMD = dfASP["AS_CAISO_EXP_RMD_CLR_PRC"].values

    except FileNotFoundError:
        logging.warning(
            "read_caiso_data: No ASP data matching input parameters found, returning empty array. (got {fname}, {year}, {month})".format(
                fname=fnameASP, year=year, month=month
            )
        )

    try:
        dfMIL_ACC = pd.read_csv(fname_path_MILEAGE, index_col=False)
        RMU_MM = dfMIL_ACC["RMU_SYS_MIL_MUL"].values
        RMD_MM = dfMIL_ACC["RMD_SYS_MIL_MUL"].values
        RMU_PACC = dfMIL_ACC["RMU_SYS_PERF_ACC"].values
        RMD_PACC = dfMIL_ACC["RMD_SYS_PERF_ACC"].values

    except FileNotFoundError:
        logging.warning(
            """read_caiso_data: No MILEAGE and PERFORMANCE ACCURACY data matching input parameters found, returning empty array.
            (got {fname}, {year}, {month})""".format(
                fname=fnameMILEAGE, year=year, month=month
            )
        )

    return daLMP, daREGU, daREGD, daRMU, daRMD, RMU_MM, RMD_MM, RMU_PACC, RMD_PACC