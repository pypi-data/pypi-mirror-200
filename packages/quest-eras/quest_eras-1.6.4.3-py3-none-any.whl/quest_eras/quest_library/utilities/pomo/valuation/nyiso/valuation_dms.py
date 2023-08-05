"""Data Manager for Valuation Tool."""

from __future__ import absolute_import
import os

from quest_eras.quest_library.utilities.pomo.dms import DataManagementSystem
import quest_eras.quest_library.utilities.pomo.valuation.nyiso.data_processing_tools as dpt


class ValuationDMSNYISO(DataManagementSystem):
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

    def get_nyiso_data(self, year, month, nodeid):
        """Retrieve data for NYISO."""
        path = os.path.join(self.home_path, "NYISO")
        # static_path = os.path.join(self.home_path, "_static")

        nodeid = str(nodeid)
        year = str(year)
        month = str(month)

        lbmp_key = self.delimiter.join([path, year, month, nodeid, "LBMP"])
        rcap_key = self.delimiter.join([path, year, month, "RegCAP"])

        try:
            # attempt to access data if it is already loaded
            lbmp_da = self.get_data(lbmp_key)
            rcap_da = self.get_data(rcap_key)
        except KeyError:
            # load the data and add it to the DMS
            lbmp_da, lbmp_rt, rcap_da, rcap_rt, rmov_da = dpt.read_nyiso_data(
                path, year, month, nodeid, typedat="both", RT_DAM="DAM"
            )

            self.add_data(lbmp_da, lbmp_key)
            self.add_data(rcap_da, rcap_key)

        return lbmp_da, rcap_da


if __name__ == "__main__":
    dms = ValuationDMS(save_name="valuation_dms.p", home_path="data")

    # # ERCOT - data doesn't exist
    # year = 2010
    # month = 1
    # settlement_point = 'HB_HOUSTON'

    # spp_da, rd, ru = dms.get_ercot_data(year, month, settlement_point)

    # # ERCOT
    # year = 2010
    # month = 12
    # settlement_point = 'HB_HOUSTON'

    # spp_da, rd, ru = dms.get_ercot_data(year, month, settlement_point)

    # PJM
    # year = 2016
    # month = 5
    # nodeid = 1

    # lmp_da, MR, RA, RD, RegCCP, RegPCP = dms.get_pjm_data(year, month, nodeid)

    # # MISO
    # year = 2015
    # month = 3
    # nodeid = "AEC"

    # lmp_da, RegMCP = dms.get_miso_data(year, month, nodeid)
