"""Data Manager for Valuation Tool."""

from __future__ import absolute_import
import logging
import os

from quest_eras.quest_library.utilities.pomo.dms import DataManagementSystem
import quest_eras.quest_library.utilities.pomo.valuation.miso.data_processing_tools as dpt


class ValuationDMSMISO(DataManagementSystem):
    """
    A class for managing data for the energy storage valuation optimization functions.

    Class methods for each type of file to be loaded are included, extending from the get_data() method of the superclass.
    Each of these methods uses get_data() to retrieve the relevant data and loads the file and adds it to the DMS if the data is not loaded.
    An optional class method for calling each of the individual data methods can be included to form the necessary arguments and return the desired variables.

    :param home_path: A string indicating the relative path to where data is saved.
    """

    def __init__(self, home_path, **kwargs):
        DataManagementSystem.__init__(self, **kwargs)

        self.home_path = home_path
        self.delimiter = " @ "  # delimiter used to split information in id_key

    def get_node_name(self, node_id, ISO):
        """
        Retrieve the node name corresponding to the given node_id using the lookup table loaded during initialization.

        :param node_id: A string or int of a node ID.
        :return: The corresponding node name as a string.
        """
        # TODO: map node_id to node name

        return str(node_id)

    def get_miso_lmp_data(self, *args):
        """Retrieve LMP data for MISO (deprecated since 1.0)."""
        logging.info("DMS: Loading MISO DA-LMP")
        try:
            # attempt to access data if is already loaded
            lmp_da = self.get_data(*args)
        except KeyError:
            # load the data and add it to the DMS
            lmp_da = dpt.read_miso_da_lmp(*args)
            self.add_data(lmp_da, *args)
        finally:
            return lmp_da

    def get_miso_reg_data(self, *args):
        """Retrieve regulation data for MISO (deprecated since 1.0)."""
        logging.info("DMS: Loading MISO RegMCP")
        try:
            # attempt to access data if is already loaded
            RegMCP = self.get_data(*args)
        except KeyError:
            # load the data and add it to the DMS
            RegMCP = dpt.read_miso_reg_price(*args)
            self.add_data(RegMCP, *args)
        finally:
            return RegMCP

    def get_miso_data(self, year, month, nodeid):
        """Retrieve data for MISO."""
        path = os.path.join(self.home_path, "MISO")

        year = str(year)
        month = str(month)

        lmp_key = self.delimiter.join([path, year, month, nodeid, "LMP"])
        regmcp_key = self.delimiter.join([path, year, month, "MCP"])

        try:
            # attempt to access data if it is already loaded
            lmp_da = self.get_data(lmp_key)
            RegMCP = self.get_data(regmcp_key)
        except KeyError:
            # load the data and add it to the DMS
            lmp_da, RegMCP = dpt.read_miso_data(path, year, month, nodeid)

            self.add_data(lmp_da, lmp_key)
            self.add_data(RegMCP, regmcp_key)

        return lmp_da, RegMCP


# if __name__ == "__main__":
#     dms = ValuationDMS(save_name="valuation_dms.p", home_path="data")

#     # # ERCOT - data doesn't exist
#     # year = 2010
#     # month = 1
#     # settlement_point = 'HB_HOUSTON'

#     # spp_da, rd, ru = dms.get_ercot_data(year, month, settlement_point)

#     # # ERCOT
#     # year = 2010
#     # month = 12
#     # settlement_point = 'HB_HOUSTON'

#     # spp_da, rd, ru = dms.get_ercot_data(year, month, settlement_point)

#     # PJM
#     # year = 2016
#     # month = 5
#     # nodeid = 1

#     # lmp_da, MR, RA, RD, RegCCP, RegPCP = dms.get_pjm_data(year, month, nodeid)

#     # MISO
#     year = 2015
#     month = 3
#     nodeid = "AEC"

#     lmp_da, RegMCP = dms.get_miso_data(year, month, nodeid)
