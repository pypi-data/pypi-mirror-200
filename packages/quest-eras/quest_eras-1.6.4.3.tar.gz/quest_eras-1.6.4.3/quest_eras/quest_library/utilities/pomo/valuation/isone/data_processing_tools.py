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

def read_isone_data(fpath, year, month, nodeid):
    """Read ISONE historical LMP, regulation capacity, and regulation service (mileage) prices and return NumPy ndarrays for those three prices.

    :param fpath: A string containing the path to the relevant historical ancillary services data file.
    :param year: An int corresponding to the year of interest
    :param month: An int corresponding to the month of interest (1: Jan., 2: Feb., etc.)
    :return: daLMP, RegCCP, RegPCP: NumPy ndarrays containing hourly LMP as well as regulation capacity/performance clearing price values.
    """
    if isinstance(month, str):
        month = int(month)

    if isinstance(year, str):
        year = int(year)

    if isinstance(nodeid, (int, float, complex)):
        nodeid = str(nodeid)

    if year < 2018:
        if year == 2017 and month == 12:
            fnameLMP = "{0:d}{1:02d}_fmlmp_{2:s}.csv".format(year, month, nodeid)
            fnameRCP = "{0:d}{1:02d}_fmrcp.csv".format(year, month)
        else:
            fnameLMP = "{0:d}{1:02d}_dalmp_{2:s}.csv".format(year, month, nodeid)
            fnameRCP = "{0:d}{1:02d}_rcp.csv".format(year, month)
    else:
        fnameLMP = "{0:d}{1:02d}_fmlmp_{2:s}.csv".format(year, month, nodeid)
        fnameRCP = "{0:d}{1:02d}_fmrcp.csv".format(year, month)

    fname_path_LMP = os.path.join(fpath, "LMP", str(nodeid), str(year), fnameLMP)
    fname_path_RCP = os.path.join(fpath, "RCP", str(year), fnameRCP)
    fname_path_MILEAGE = os.path.join(fpath, "MileageFile.xlsx")

    daLMP = np.empty([0])
    RegCCP = np.empty([0])
    RegPCP = np.empty([0])
    miMULT = np.empty([0])

    try:
        dfLMP = pd.read_csv(fname_path_LMP, index_col=False)
        daLMP = dfLMP["LmpTotal"].values
    except FileNotFoundError:
        logging.warning(
            "read_isone_data: No LMP data matching input parameters found, returning empty array. (got {fname}, {year}, {month}, {nodeid})".format(
                fname=fnameLMP, year=year, month=month, nodeid=nodeid
            )
        )

    try:
        if year > 2014:
            if year == 2015 and month < 4:
                dfRCP = pd.read_csv(fname_path_RCP, index_col=False)
                RegCCP = dfRCP["RegClearingPrice"].values
                RegPCP = []
            else:
                dfRCP = pd.read_csv(fname_path_RCP, index_col=False)
                RegCCP = dfRCP["RegCapacityClearingPrice"].values
                RegPCP = dfRCP["RegServiceClearingPrice"].values

                dataF_mileage_file = pd.read_excel(
                    fname_path_MILEAGE,
                    sheet_name="Energy Neutral Trinary",
                    usecols=["Fleet ATRR dispatch [MW]"],
                )
                dataF_mileage_file = dataF_mileage_file.append(
                    pd.DataFrame([-10] * 15, columns=["Fleet ATRR dispatch [MW]"]),
                    ignore_index=True,
                )  # Change number of data points to 24 hours; doesn't change mileage

                #   AGC setpoints given every 4 seconds, take the total mileage for each hour; total of one day of mileage
                hours = [i for i in range(len(dataF_mileage_file.index) // 900)]

                mileage_day = []
                for hour in hours:
                    dataF_mileage_hour = dataF_mileage_file[
                        900 * hour : 900 * (hour + 1)
                    ]  # Every 900 values represents an hour (900*4 = 3600)
                    mileage_hour = 0
                    for i in range(len(dataF_mileage_hour.index)):
                        if i == len(dataF_mileage_hour.index) - 1:
                            break

                        if (
                            not dataF_mileage_hour.iloc[i, 0]
                            == dataF_mileage_hour.iloc[i + 1, 0]
                        ):
                            mileage_hour += (
                                abs(
                                    dataF_mileage_hour.iloc[i, 0]
                                    - dataF_mileage_hour.iloc[i + 1, 0]
                                )
                                / 10
                            )

                    mileage_day.append(mileage_hour)

                dataF_mileage_day = pd.DataFrame(
                    mileage_day, columns=["Trinary Mileage"]
                )

                #   have one days worth of data, need one months worth
                days = len(daLMP) // 24
                mileage_mult = pd.DataFrame(columns=["Trinary Mileage"])
                for day in range(days):
                    mileage_mult = mileage_mult.append(
                        dataF_mileage_day, ignore_index=True
                    )
                #   if the len are offset, make them match
                if not len(daLMP) == len(mileage_mult):
                    diff = len(daLMP) - len(mileage_mult)

                    for i in range(diff):
                        mileage_mult = mileage_mult.append(
                            dataF_mileage_day.iloc[i], ignore_index=True
                        )

                miMULT = mileage_mult["Trinary Mileage"].values
        else:
            dfRCP = pd.read_csv(fname_path_RCP, index_col=False)
            RegCCP = dfRCP["RegClearingPrice"].values
            RegPCP = []

    except FileNotFoundError:
        logging.warning(
            "read_isone_data: No ASP data matching input parameters found, returning empty array. (got {fname}, {year}, {month})".format(
                fname=fnameRCP, year=year, month=month
            )
        )

    return daLMP, RegCCP, RegPCP, miMULT