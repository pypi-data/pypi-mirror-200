"""Market data processing tools."""
# from __future__ import absolute_import
# from xlrd.biffh import XLRDError

import pandas as pd
import numpy as np
import os
import calendar
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

def read_miso_da_lmp(fname, node_name):
    """
    Read MISO day-ahead LMP file and return the NumPy ndarray corresponding to the hourly LMP at node_name.

    :param fname: A string containing the path to the relevant day-ahead LMP file.
    :param node_name: A string containing the name of the pricing node of interest.
    :return: LMP: A NumPy ndarray containing the hourly LMP at node-name.
    """
    # parse fname for month and year values
    month = int(fname[-2:])
    year = int(fname[-6:-2])

    nday = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    if year % 4 == 0:
        nday[2] = 29

    LMP = np.empty([0])
    for day in range(1, nday[month] + 1):

        if (year <= 2014) or (year == 2015 and month <= 2):
            fname_ = fname + str(day).zfill(2) + "_da_lmp.csv"
        else:
            fname_ = fname + str(day).zfill(2) + "_da_exante_lmp.csv"

        df = pd.read_csv(fname_, skiprows=4, low_memory=False)
        # filter rows by node_name
        col1 = df.axes[1][0]
        col3 = df.axes[1][2]
        pnode_ix1 = df.index[df[col1] == node_name]
        df1 = df.iloc[pnode_ix1, :]

        # find LMP values
        pnode_ix2 = df1.index[df1[col3] == "LMP"]
        df2 = df.iloc[pnode_ix2, :]

        # filter Total LMP columns
        df3 = df2[df2.axes[1][3:27]]

        # convert to NumPy ndarray, ravel, and remove NaNs
        LMP_day = np.ravel(df3.astype("float").values)
        LMP_day = LMP_day[~np.isnan(LMP_day)]
        LMP = np.append(LMP, LMP_day)

    return LMP


def read_miso_reg_price(fname):
    """
    Read MISO historical ancillary services data file at fname and returns the NumPy ndarrays for regulation clearing prices.

    :param fname: A string containing the path to the relevant historical ancillary services data file.
    :return: RegMCP: NumPy ndarrays containing hourly regulation capacity/mileage clearing price values.
    """
    # parse fname for month and year values
    month = int(fname[-2:])
    year = int(fname[-6:-2])

    nday = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    if year % 4 == 0:
        nday[2] = 29

    RegMCP = np.empty([0])

    for day in range(1, nday[month] + 1):
        if (year <= 2014) or (year == 2015 and month <= 2):
            fname_ = fname + str(day).zfill(2) + "_asm_damcp.csv"
        else:
            fname_ = fname + str(day).zfill(2) + "_asm_exante_damcp.csv"

        # read in the .csv file
        df = pd.read_csv(fname_, skiprows=4, nrows=7, low_memory=False)

        # find SERREGMCP values
        col3 = df.axes[1][2]
        pnode_ix1 = df.index[df[col3] == "SERREGMCP"]
        df1 = df.iloc[pnode_ix1, :]
        df2 = df1[df1.axes[1][3:27]]

        # convert to NumPy ndarray, ravel, and remove NaNs
        RegMCP_day = np.ravel(df2.astype("float").values)
        RegMCP_day = RegMCP_day[~np.isnan(RegMCP_day)]
        RegMCP = np.append(RegMCP, RegMCP_day)

    return RegMCP

def read_miso_data(fpath, year, month, nodeid):
    """Read the daily MISO data files and returns the NumPy ndarrays for LMP and MCP.

    :param fpath: root of the MISO data folder
    :type fpath: str
    :param year: year of data
    :type year: int or str
    :param month: month of data
    :type month: int or str
    :param nodeid: pricing node ID
    :type nodeid: str
    :return: arrays of data specified
    :rtype: NumPy ndarrays
    """
    LMP = np.array([])
    RegMCP = np.array([])

    _, n_days_month = calendar.monthrange(int(year), int(month))

    for day in range(1, n_days_month + 1):
        # Read daily files.
        date_str = "{year}{month}{day}".format(
            year=year, month=str(month).zfill(2), day=str(day).zfill(2)
        )

        if (int(year) <= 2014) or (int(year) == 2015 and int(month) <= 2):
            lmp_fname = os.path.join(
                fpath,
                "LMP",
                str(year),
                str(month).zfill(2),
                "{prefix}_da_lmp.csv".format(prefix=date_str),
            )
            mcp_fname = os.path.join(
                fpath,
                "MCP",
                str(year),
                str(month).zfill(2),
                "{prefix}_asm_damcp.csv".format(prefix=date_str),
            )
        else:
            lmp_fname = os.path.join(
                fpath,
                "LMP",
                str(year),
                str(month).zfill(2),
                "{prefix}_da_exante_lmp.csv".format(prefix=date_str),
            )
            mcp_fname = os.path.join(
                fpath,
                "MCP",
                str(year),
                str(month).zfill(2),
                "{prefix}_asm_exante_damcp.csv".format(prefix=date_str),
            )

        # LMP file.
        try:
            df = pd.read_csv(lmp_fname, skiprows=4, low_memory=False)
        except FileNotFoundError:
            logging.warning("read_miso_data: LMP file missing, returning empty array.")
            break

        # Filter rows by node_name.
        col1 = df.axes[1][0]
        col3 = df.axes[1][2]
        pnode_ix1 = df.index[df[col1] == nodeid]
        df1 = df.iloc[pnode_ix1, :]

        # Find LMP values.
        pnode_ix2 = df1.index[df1[col3] == "LMP"]
        df2 = df.iloc[pnode_ix2, :]

        # Filter Total LMP columns.
        df3 = df2[df2.axes[1][3:27]]

        if len(df3) == 0:
            LMP = np.array([])
            logging.warning(
                "read_miso_data: A daily LMP file is missing required data, returning empty array."
            )
            break

        # Convert to NumPy ndarray, ravel, and remove NaNs.
        LMP_day = np.ravel(df3.astype("float").values)
        LMP_day = LMP_day[~np.isnan(LMP_day)]
        LMP = np.append(LMP, LMP_day)

        # MCP file.
        try:
            df = pd.read_csv(mcp_fname, skiprows=4, nrows=7, low_memory=False)
        except FileNotFoundError:
            RegMCP = np.array([])
            logging.warning("read_miso_data: MCP file missing, returning empty array.")
            break

        # Find SERREGMCP values.
        col3 = df.axes[1][2]
        pnode_ix1 = df.index[df[col3] == "SERREGMCP"]
        df1 = df.iloc[pnode_ix1, :]
        df2 = df1[df1.axes[1][3:27]]

        # convert to NumPy ndarray, ravel, and remove NaNs
        RegMCP_day = np.ravel(df2.astype("float").values)
        RegMCP_day = RegMCP_day[~np.isnan(RegMCP_day)]
        RegMCP = np.append(RegMCP, RegMCP_day)

    return LMP, RegMCP