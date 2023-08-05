"""Data Manager for Valuation Tool."""

from __future__ import absolute_import
import logging
import os

from quest_eras.quest_library.utilities.pomo.dms import DataManagementSystem
import quest_eras.quest_library.utilities.pomo.valuation.ercot.data_processing_tools as dpt


class ValuationDMSERCOT(DataManagementSystem):
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

    def get_ercot_spp_data(self, id_key):
        """Retrieve DAM-SPP data for ERCOT."""
        logging.info("DMS: Loading ERCOT DA-SPP")
        try:
            # attempt to access data if it is already loaded
            spp_da = self.get_data(id_key)
        except KeyError:
            # load the data and add it to the DMS

            # deconstruct id_key to obtain args for read function
            spp_da = dpt.read_ercot_da_spp(*id_key.split(self.delimiter))
            self.add_data(spp_da, id_key)
        finally:
            return spp_da

    def get_ercot_ccp_data(self, id_key):
        """Retrieve DAM-CCP data for ERCOT."""
        logging.info("DMS: Loading ERCOT DA-CCP")
        try:
            # attempt to access data if it is already loaded
            REGUP = self.get_data(id_key + self.delimiter + "REGUP")
            REGDN = self.get_data(id_key + self.delimiter + "REGDN")
        except KeyError:
            # load the data and add it to the DMS

            # deconstruct id_key to obtain args for read function
            REGDN, REGUP = dpt.read_ercot_da_ccp(*id_key.split(self.delimiter)[:2])

            self.add_data(REGUP, id_key + self.delimiter + "REGUP")
            self.add_data(REGDN, id_key + self.delimiter + "REGDN")
        finally:
            return REGDN, REGUP

    def get_ercot_data(self, year, month, settlement_point):
        """Retrieve data for ERCOT."""
        # construct file name paths
        path = os.path.join(self.home_path, "ERCOT")  # path to data_bank root

        if isinstance(month, int):
            month = str(month)

        spp_fpath = os.path.join(path, "SPP", str(year))

        try:
            for filename in os.listdir(spp_fpath):
                if filename.lower().endswith(".xlsx"):
                    fname = filename
        except ValueError as e:
            raise (e)

        spp_fname = os.path.join(spp_fpath, fname)

        ccp_fpath = os.path.join(path, "CCP", str(year))

        try:
            for filename in os.listdir(ccp_fpath):
                if filename.lower().endswith(".csv"):
                    fname = filename
        except ValueError as e:
            raise (e)

        ccp_fname = os.path.join(ccp_fpath, fname)

        # construct identifier keys
        spp_id = self.delimiter.join([spp_fname, month, settlement_point])
        ccp_id = self.delimiter.join([ccp_fname, month])

        # retrieve data
        spp_da = self.get_ercot_spp_data(spp_id)
        rd, ru = self.get_ercot_ccp_data(ccp_id)

        return spp_da, rd, ru


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
