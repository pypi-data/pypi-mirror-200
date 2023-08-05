"""Market data processing tools."""
# from __future__ import absolute_import
# from xlrd.biffh import XLRDError

import pandas as pd
import numpy as np
import os
import calendar
import logging


def read_spp_data(fpath, year, month, node, typedat="both"):
    """Read the historical LMP, regulation capacity, and regulation service (mileage) prices and return NumPy ndarrays for those three prices.

    :param fpath: A string containing the path to the relevant historical ancillary services data file.
    :param year: An int corresponding to the year of interest
    :param month: An int corresponding to the month of interest (1: Jan., 2: Feb., etc.)
    :param node: A string with the name of the node in SPP
    :param typedat: xxxxxx xxxxxxx
    :param RT_DAM: xxxxxxxxx xxxx
    :return: daLMP, daMCPRU, daMCPRD: NumPy ndarrays containing hourly LMP as well as regulation up and down prices for the SPP market
    """
    daLMP = np.empty([0])
    daMCPRU = np.empty([0])
    daMCPRD = np.empty([0])

    if isinstance(month, str):
        month = int(month)

    if isinstance(year, str):
        year = int(year)
    # if isinstance(node, str):
    #     node = int(node)

    ############################################################################################
    # TODO: path_nodes_file is a folder to adjust when integrating it to QuESt
    path_nodes_file = "_static"
    pathf_nodeszones = os.path.join(fpath, path_nodes_file, "nodes_spp.csv")
    print(pathf_nodeszones)
    df_nodes = pd.read_csv(pathf_nodeszones, index_col=False, encoding="cp1252")
    df_nodes_x = df_nodes.loc[df_nodes["Node ID"] == node, :]

    if df_nodes_x.empty:
        print("The node does NOT exists in SPP")
        # raise ValueError('Not a valid bus number!!!')
        return daLMP, daMCPRU, daMCPRD
    else:
        nodetype = df_nodes_x.iloc[0, 2]
        if nodetype == "Location":
            # print('It is a Location node')
            bus_loc = ["location", "SL"]
        elif nodetype == "Bus":
            # print('It is a Bus node')
            bus_loc = ["bus", "B"]

    # TODO: figure out the reserve zone for each node, for SPP there are 5 reserve zones and there should be a correspondance with the nodes
    ResZone = 1
    ############################################################################################

    # Read only the DA market

    ndaysmonth = calendar.monthrange(year, month)
    ndaysmonth = int(ndaysmonth[1])

    for ix in range(ndaysmonth):
        day_x = ix + 1

        fnameLMP_DA = "DA-LMP-{0:s}-{1:d}{2:02d}{3:02d}0100.csv".format(
            bus_loc[1], year, month, day_x
        )
        fnameMCP_DA = "DA-MCP-{0:d}{1:02d}{2:02d}0100.csv".format(year, month, day_x)

        fname_path_LMP_DA = os.path.join(
            fpath, "LMP", "DAM", bus_loc[0], str(year), str(month).zfill(2), fnameLMP_DA
        )
        fname_path_MCP_DA = os.path.join(
            fpath, "MCP", "DAM", str(year), str(month).zfill(2), fnameMCP_DA
        )

        if typedat == "lmp" or typedat == "both":
            # DA-LMP-B-201707010100.csv
            # DA-LMP-SL-201707010100.csv
            try:
                df_daLMP = pd.read_csv(fname_path_LMP_DA, index_col=False)
            except FileNotFoundError:
                daLMP = np.empty([0])
                logging.warning(
                    "read_spp_data: LMP file missing, returning empty array."
                )
                break

            daLMP_node_x = df_daLMP.loc[df_daLMP["Pnode"] == node, ["LMP"]]
            daLMP = np.append(daLMP, daLMP_node_x.values)
            if daLMP_node_x.empty:
                return np.empty([0]), np.empty([0]), np.empty([0])

        if typedat == "mcp" or typedat == "both":
            # DA-MCP-201707010100.csv
            try:
                df_daMCP = pd.read_csv(fname_path_MCP_DA, index_col=False)
            except FileNotFoundError:
                daMCPRU = np.empty([0])
                daMCPRD = np.empty([0])
                logging.warning(
                    "read_spp_data: MCP file missing, returning empty arrays."
                )
                break

            # print('Warning -reserve zone not figured out!!!')
            daMCPRU_node_x = df_daMCP.loc[
                df_daMCP["Reserve Zone"] == ResZone, ["RegUP"]
            ]
            daMCPRD_node_x = df_daMCP.loc[
                df_daMCP["Reserve Zone"] == ResZone, ["RegDN"]
            ]

            daMCPRU = np.append(daMCPRU, daMCPRU_node_x.values)
            daMCPRD = np.append(daMCPRD, daMCPRD_node_x.values)

    return daLMP, daMCPRU, daMCPRD