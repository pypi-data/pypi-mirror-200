"""Market data processing tools."""
# from __future__ import absolute_import
# from xlrd.biffh import XLRDError

import pandas as pd
import numpy as np
import calendar
import logging


def read_ercot_da_spp(fname, month, settlement_point):
    """
    Read the day-ahead Ercot historical energy prices from file and return the NumPy ndarray corresponding to the hourly price at settlement_point.

    :param fname: string giving location of DAM SPPs (day-ahead market settlement point prices, a.k.a LMPs) file
    :type fname: str
    :param month: which month to read data for; (int) [1, 12] OR (str) ['1', '12']
    :type month: int or str
    :param settlement_point: string giving settlement point name (hub or load zone)
    :type settlement_point: str
    :return spp_da: NumPy ndarray with SPPs for month and settlement point
    :rtype: NumPy ndarray
    """
    spp_da = np.array([])

    # if month is provided as an int, map it to the correct calendar month
    if isinstance(month, int):
        month_abbr = calendar.month_abbr(month)
    elif isinstance(month, str):
        month_ix = int(month)
        month_abbr = calendar.month_abbr[month_ix]

    # Retrieve the correct worksheet for the month.
    wkbk = pd.ExcelFile(fname)
    wkbk_sheetnames = [name[:3] for name in wkbk.sheet_names]

    try:
        wkst_ix = wkbk_sheetnames.index(month_abbr)
    except ValueError:
        # The worksheet for the requested month does not exist.
        logging.warning(
            """read_ercot_da_spp: Could not load data (the specified month of data could not be found in the given file), returning empty array.
            (got {fname},{month}, {settlement_point})""".format(
                fname=fname, month=month, settlement_point=settlement_point
            )
        )
        return spp_da
    else:
        df = wkbk.parse(wkst_ix)

        # filter DataFrame by settlement_point and extract series
        df0 = df.loc[df["Settlement Point"] == settlement_point]
        df1 = df0["Settlement Point Price"]

        # convert to NumPy array and remove NaN
        spp_da = df1.astype("float").values
        spp_da = spp_da[~np.isnan(spp_da)]

    return spp_da


def read_ercot_da_ccp(fname, month):
    """
    Read the day-ahead Ercot capacity clearing prices from file and returns NumPy ndarrays corresponding to the hourly regdn and regup prices.

    :param fname:
    :param month: which month to read data for; (int) [1, 12] OR (str) ['1', '12']

    :param fname: string giving location of DAM CCPs file
    :type fname: str
    :param month: which month to read data for; (int) [1, 12] OR (str) ['1', '12']
    :type month: int or str
    :return: NumPy ndarrays with regdn and regup CCPs for month
    :rtype: Numpy ndarrays
    """
    regdn = np.array([])
    regup = np.array([])

    # if month is provided as an int, map it to the correct calendar month
    if isinstance(month, int):
        month_ix = month
    elif isinstance(month, str):
        month_ix = int(month)

    # Read .csv and generate a Series for the month from "Delivery Date" column.
    df = pd.read_csv(fname, low_memory=False)
    series_month = pd.to_datetime(df["Delivery Date"]).dt.month

    # Filter DataFrame by month.
    df1 = df.loc[series_month == month_ix]

    if len(df1) > 0:
        regdn = df1["REGDN"].astype("float").values
        regdn = regdn[~np.isnan(regdn)]

        try:
            regup = (
                df1["REGUP "].astype("float").values
            )  # why is there an extra space in the key
        except KeyError:
            regup = df1["REGUP"].astype("float").values
        finally:
            regup = regup[~np.isnan(regup)]
    else:
        logging.warning(
            "read_ercot_da_ccp: No data matching input parameters found, returning empty array. (got {fname}, {month})".format(
                fname=fname, month=month
            )
        )

    return regdn, regup