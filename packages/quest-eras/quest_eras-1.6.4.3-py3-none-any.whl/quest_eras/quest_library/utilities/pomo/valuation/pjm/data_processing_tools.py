"""Market data processing tools."""
# from __future__ import absolute_import
# from xlrd.biffh import XLRDError

import pandas as pd
import numpy as np
import os
import logging


def read_nodeid(fname, iso):
    """Read node id from an excel file and return as a list."""
    from xlrd import open_workbook

    wb = open_workbook(filename=fname)
    ws = wb.sheet_by_name(iso)
    nodeid = []
    for i in range(1, ws.nrows - 1):
        cell = ws.cell(i, 0)
        text = str(cell.value)
        text = text.replace(".0", "")
        nodeid += [text]
    return nodeid


def read_pjm_data(fpath, year, month, nodeid):
    """Read the historical LMP, regulation capacity, and regulation service (mileage) prices in PJM and returns NumPy ndarrays for those three prices.

    :param fpath: The path to the root of the PJM data directory
    :type fpath: str
    :param year: Year of data to read
    :type year: int or str
    :param month: Month of data to read
    :type month: int or str
    :return: daLMP, RegCCP, RegPCP: Hourly LMP and regulation capacity/performance clearing price values.
    :rtype: NumPy ndarrays
    """
    daLMP = np.array([])
    RegCCP = np.array([])
    RegPCP = np.array([])
    rega = np.array([])
    regd = np.array([])
    mr = np.array([])

    if isinstance(month, str):
        month = int(month)

    if isinstance(year, str):
        year = int(year)

    if isinstance(nodeid, str):
        nodeid = int(nodeid)

    fnameLMP = "{0:d}{1:02d}_dalmp_{2:d}.csv".format(year, month, nodeid)
    fnameREG = "{0:d}{1:02d}_regp.csv".format(year, month)
    fnameMILEAGE = "{0:d}{1:02d}_regm.csv".format(year, month)

    fname_path_LMP = os.path.join(fpath, "LMP", str(nodeid), str(year), fnameLMP)
    fname_path_REG = os.path.join(fpath, "REG", str(year), fnameREG)
    fname_path_MILEAGE = os.path.join(fpath, "MILEAGE", str(year), fnameMILEAGE)

    try:
        dfLMP = pd.read_csv(fname_path_LMP, index_col=False)
        daLMP = dfLMP["total_lmp_da"].values
    except FileNotFoundError:
        logging.warning(
            "read_pjm_data: No LMP data matching input parameters found, returning empty array. (got {fname}, {year}, {month}, {nodeid})".format(
                fname=fnameLMP, year=year, month=month, nodeid=nodeid
            )
        )

    try:
        dfREG = pd.read_csv(fname_path_REG, index_col=False)
        RegCCP = dfREG["rmccp"].values
        RegPCP = dfREG["rmpcp"].values
    except FileNotFoundError:
        logging.warning(
            "read_pjm_data: No REG data matching input parameters found, returning empty array. (got {fname}, {year}, {month})".format(
                fname=fnameREG, year=year, month=month
            )
        )

    try:
        dfMILEAGE = pd.read_csv(fname_path_MILEAGE, index_col=False)
        dfMILEAGE["MILEAGE RATIO"] = dfMILEAGE["regd_hourly"] / dfMILEAGE["rega_hourly"]

        # TODO: Handling NaNs/missing data intelligently. The current method just fills forward.
        rega = (
            dfMILEAGE["rega_hourly"]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(method="ffill")
            .values
        )
        regd = (
            dfMILEAGE["regd_hourly"]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(method="ffill")
            .values
        )
        mr = (
            dfMILEAGE["MILEAGE RATIO"]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(method="ffill")
            .values
        )
    except FileNotFoundError:
        logging.warning(
            "read_pjm_data: No MILEAGE data matching input parameters found, returning empty array. (got {fname}, {year}, {month})".format(
                fname=fnameMILEAGE, year=year, month=month
            )
        )

    return daLMP, mr, rega, regd, RegCCP, RegPCP


def read_pjm_da_lmp(fname, node_name):
    """Read PJM day-ahead LMP file and return the NumPy ndarray corresponding to the hourly LMP at node_name.

    :param fname: A string containing the path to the relevant day-ahead LMP file.
    :param node_name: A string containing the name of the pricing node of interest.
    :return: LMP: A NumPy ndarray containing the hourly LMP at node-name.
    """
    # read in the .csv file
    df = pd.read_csv(fname, low_memory=False)

    # filter rows by node_name
    col2 = df.axes[1][2]
    pnode_ix = df.index[df[col2] == node_name]
    df1 = df.iloc[pnode_ix, :]

    # filter Total LMP columns
    df2 = df1[df1.axes[1][7:79:3]]

    # convert to NumPy ndarray, ravel, and remove NaNs
    LMP = np.ravel(df2.astype("float").values)
    LMP = LMP[~np.isnan(LMP)]

    return LMP


def read_pjm_reg_signal(fname):
    """
    Read PJM regulation signal file at and return the NumPy ndarray corresponding to the hourly integrated signal.

    :param fname: A string containing the path to the relevant regulation signal file.
    :return: RU, RD: NumPy ndarrays containing the hourly integrated regulation up/down signals.
    """
    # read in the Excel file
    df = pd.read_excel(fname, skip_footer=1)

    # create DateTime indexing to facilitate resampling
    dt_ix = pd.date_range("2017-11-01", periods=30 * 60 * 24, freq="2S")
    df.index = dt_ix

    # define function for performing hourly integration
    def _hourly_integration(array_like):
        # ZOH integration
        dt = 2.0 / (60 * 60)
        return np.sum(array_like) * dt

    # use resample to apply hourly integration
    df1 = df.resample(rule="H", closed="left").apply(_hourly_integration)

    # convert DataFrame to NumPy ndarray and ravel
    REG = np.ravel(df1.astype("float").values, "F")

    # assign reg up/down values appropriately based on sign of regulation signal
    RU = REG * (REG >= 0)
    RD = REG * (REG < 0)

    return RU, RD


def read_pjm_mileage(fname, month):
    """
    Read PJM historical regulation market data file at fname and returns the NumPy ndarrays for mileage data.

    :param fname: A string containing the path to the relevant historic regulation market data file.
    :param month: An int corresponding to the month of interest (1: Jan., 2: Feb., etc.)
    :return: Mileage_Ratio, RegA_milage, RegD_mileage: NumPy ndarrays containing computed mileage ratio and RegA/RegD hourly mileage signals.
    """
    # read in the Excel file and parse the relevant worksheet
    wkbk = pd.ExcelFile(fname)
    df = wkbk.parse(month)

    # replace "UNAPPROVED" entries with previous filled value
    df.fillna(method="ffill", inplace=True)

    # compute hourly mileage ratio
    # TODO: what do infinite mileage ratio? (REGA = 0)
    df["MILEAGE RATIO"] = df["REGD_HOURLY"] / df["REGA_HOURLY"]

    RegA_mileage = df["REGA_HOURLY"].values
    RegD_mileage = df["REGD_HOURLY"].values
    Mileage_Ratio = df["MILEAGE RATIO"].values

    return Mileage_Ratio, RegA_mileage, RegD_mileage


def read_pjm_reg_price(fname, month):
    """
    Read PJM historical ancillary services data file and return the NumPy ndarrays for regulation clearing prices.

    :param fname: A string containing the path to the relevant historical ancillary services data file.
    :param month: An int corresponding to the month of interest (1: Jan., 2: Feb., etc.)
    :return: RegCCP, RegPCP: NumPy ndarrays containing hourly regulation capacity/performance clearing price values.
    """
    # read in the Excel file and parse relevant worksheet
    wkbk = pd.ExcelFile(fname)
    df = wkbk.parse(month)

    # parse the relevant service
    df1 = df[df["SERVICE"] == "REG"]

    # DLS hour gives NaN
    df1.fillna(method="ffill", inplace=True)

    RegCCP = df1["REG_CCP"].values
    RegPCP = df1["REG_PCP"].values

    return RegCCP, RegPCP