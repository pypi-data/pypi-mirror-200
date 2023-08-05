"""Market data processing tools."""
# from __future__ import absolute_import
# from xlrd.biffh import XLRDError

import pandas as pd
import numpy as np
import os
import calendar
import logging


def read_nyiso_data(fpath, year, month, nodeid, typedat="both", RT_DAM="both"):
    """
    Read NYISO historical LBMP, regulation capacity, and regulation movement prices and return NumPy ndarrays for those three prices.

    :param fpath: The path to the root of the NYISO data directory
    :type fpath: str
    :param year: Year of data to read
    :type year: int or str
    :param month: Month of data to read
    :type month: int or str
    :param nodeid: ID of the node to read
    :type nodeid: int or str
    :return: daLBMP, rtLBMP, daCAP, rtCAP, rtMOV: Hourly LBMP and regulation capacity/movement clearing price values.
    :rtype: NumPy ndarraysx
    """
    ############################################################

    daLBMP = np.empty([0])
    rtLBMP = np.empty([0])
    daCAP = np.empty([0])
    rtCAP = np.empty([0])
    rtMOV = np.empty([0])

    if isinstance(month, str):
        month = int(month)

    if isinstance(year, str):
        year = int(year)

    if isinstance(nodeid, str):
        nodeid = int(nodeid)

    ############################################################################################
    # folderfile = fpath
    # TODO: path_nodes_file is a folder to adjust when integrating it to QuESt
    # path_nodes_file = 'C:/Users/fwilche/Documents/data_bank/NYISO/'
    path_nodes_file = "_static"
    pathf_nodeszones = os.path.join(fpath, path_nodes_file, "nodes_nyiso.csv")
    print(pathf_nodeszones)
    df_nodeszones = pd.read_csv(pathf_nodeszones, index_col=False)
    df_nodeszones_x = df_nodeszones.loc[df_nodeszones["Node ID"] == nodeid, :]

    if df_nodeszones_x.empty:
        print("The node does NOT exists in NYISO")
        # raise ValueError('Not a valid bus number!!!')
        return daLBMP, rtLBMP, daCAP, rtCAP, rtMOV
    else:
        if df_nodeszones_x.iloc[0, 0] == df_nodeszones_x.iloc[0, 2]:
            print("It's a zone node")
            zoneid = nodeid
            zone_gen = "zone"
        else:
            print("It's a gen node")
            zoneid = df_nodeszones_x.iloc[0, 2]
            zone_gen = "gen"
    print("Identified zone:")
    print(zoneid)
    ############################################################################################

    ndaysmonth = calendar.monthrange(year, month)
    ndaysmonth = int(ndaysmonth[1])

    for ix in range(ndaysmonth):
        day_x = ix + 1
        date_str = str(year) + str(month).zfill(2) + str(day_x).zfill(2)
        # print(date_str)

        fnameLBMP_DA = date_str + "damlbmp_" + zone_gen + ".csv"
        fnameASP_DA = date_str + "damasp.csv"

        fnameLBMP_RT = date_str + "realtime_" + zone_gen + ".csv"
        fnameASP_RT = date_str + "rtasp.csv"

        fname_path_LBMP_DA = os.path.join(
            fpath, "LBMP", "DAM", zone_gen, str(year), str(month).zfill(2), fnameLBMP_DA
        )
        fname_path_ASP_DA = os.path.join(
            fpath, "ASP", "DAM", str(year), str(month).zfill(2), fnameASP_DA
        )

        fname_path_LBMP_RT = os.path.join(
            fpath, "LBMP", "RT", zone_gen, str(year), str(month).zfill(2), fnameLBMP_RT
        )
        fname_path_ASP_RT = os.path.join(
            fpath, "ASP", "RT", str(year), str(month).zfill(2), fnameASP_RT
        )

        if typedat == "asp" or typedat == "both":
            # 20170201damasp.csv
            # 20180501rtasp.csv
            if RT_DAM == "RT" or RT_DAM == "both":
                try:
                    df_file = pd.read_csv(fname_path_ASP_RT, index_col=False)
                except FileNotFoundError:
                    rtCAP = np.empty([0])
                    rtMOV = np.empty([0])
                    logging.warning(
                        "read_nyiso_data: RT ASP file missing, returning empty array."
                    )
                    break

                if (
                    (year >= 2016 and month >= 6 and day_x >= 23)
                    or (year >= 2016 and month >= 7)
                    or (year >= 2017)
                ):
                    # NYCA Regulation Capacity ($/MWHr) - for newest type of data
                    df_file_rtCAP = df_file.loc[
                        df_file["PTID"] == zoneid, ["NYCA Regulation Capacity ($/MWHr)"]
                    ]
                    rtCAP = np.append(rtCAP, df_file_rtCAP.values)
                    # NYCA Regulation Movement ($/MW)
                    df_file_rtMOV = df_file.loc[
                        df_file["PTID"] == zoneid, ["NYCA Regulation Movement ($/MW)"]
                    ]
                    rtMOV = np.append(rtMOV, df_file_rtMOV.values)
                elif (
                    (year >= 2001 and month >= 10 and day_x >= 0)
                    or (year >= 2001 and month >= 11)
                    or (
                        year >= 2002
                        and not (
                            (year >= 2016 and month >= 6 and day_x >= 23)
                            or (year >= 2016 and month >= 7)
                            or (year >= 2017)
                        )
                    )
                ):
                    df_file_rtCAP = df_file["East Regulation ($/MWHr)"]
                    rtCAP = np.append(rtCAP, df_file_rtCAP.values)
                    df_file_rtMOV = df_file[" NYCA Regulation Movement ($/MW)"]
                    rtMOV = np.append(rtMOV, df_file_rtMOV.values)
                    # RT ancillary services for NYISO start on July 2004

            if RT_DAM == "DAM" or RT_DAM == "both":
                try:
                    df_file = pd.read_csv(fname_path_ASP_DA, index_col=False)
                except FileNotFoundError:
                    daCAP = np.empty([0])
                    logging.warning(
                        "read_nyiso_data: DA ASP file missing, returning empty array."
                    )
                    break

                if (
                    (year >= 2016 and month >= 6 and day_x >= 23)
                    or (year >= 2016 and month >= 7)
                    or (year >= 2017)
                ):
                    df_file_daCAP = df_file.loc[
                        df_file["PTID"] == zoneid, ["NYCA Regulation Capacity ($/MWHr)"]
                    ]
                    daCAP = np.append(daCAP, df_file_daCAP.values)
                elif (
                    (year >= 2001 and month >= 10 and day_x >= 0)
                    or (year >= 2001 and month >= 11)
                    or (
                        year >= 2002
                        and not (
                            (year >= 2016 and month >= 6 and day_x >= 23)
                            or (year >= 2016 and month >= 7)
                            or (year >= 2017)
                        )
                    )
                ):
                    df_file_daCAP = df_file["East Regulation ($/MWHr)"]
                    daCAP = np.append(daCAP, df_file_daCAP.values)
                else:
                    df_file_daCAP = df_file["Regulation ($/MWHr)"]
                    daCAP = np.append(daCAP, df_file_daCAP.values)

        if typedat == "lbmp" or typedat == "both":
            # 20170201damlbmp_gen.csv
            # 20170201damlbmp_zone.csv
            # 20170201realtime_gen.csv
            if RT_DAM == "RT" or RT_DAM == "both":
                try:
                    df_rtLBMP = pd.read_csv(fname_path_LBMP_RT, index_col=False)
                except FileNotFoundError:
                    rtLBMP = np.empty([0])
                    logging.warning(
                        "read_nyiso_data: RT LMP file missing, returning empty array."
                    )
                    break

                rtLBMP_node_x = df_rtLBMP.loc[
                    df_rtLBMP["PTID"] == nodeid, ["LBMP ($/MWHr)"]
                ]
                rtLBMP = np.append(rtLBMP, rtLBMP_node_x.values)
                if rtLBMP_node_x.empty:
                    return (
                        np.empty([0]),
                        np.empty([0]),
                        np.empty([0]),
                        np.empty([0]),
                        np.empty([0]),
                    )

            if RT_DAM == "DAM" or RT_DAM == "both":
                try:
                    df_daLBMP = pd.read_csv(fname_path_LBMP_DA, index_col=False)
                except FileNotFoundError:
                    daLBMP = np.empty([0])
                    logging.warning(
                        "read_nyiso_data: DA LMP file missing, returning empty array."
                    )
                    break

                daLBMP_node_x = df_daLBMP.loc[
                    df_daLBMP["PTID"] == nodeid, ["LBMP ($/MWHr)"]
                ]
                daLBMP = np.append(daLBMP, daLBMP_node_x.values)
                if daLBMP_node_x.empty:
                    return (
                        np.empty([0]),
                        np.empty([0]),
                        np.empty([0]),
                        np.empty([0]),
                        np.empty([0]),
                    )

    return daLBMP, rtLBMP, daCAP, rtCAP, rtMOV