"""Data Manager for Valuation Tool."""

from __future__ import absolute_import
import logging
import os

from quest_eras.quest_library.utilities.pomo.dms import DataManagementSystem
import quest_eras.quest_library.utilities.pomo.valuation.pjm.data_processing_tools as dpt


class ValuationDMSPJM(DataManagementSystem):
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

        # with open(os.path.abspath(os.path.join(self.home_path, '..', 'es_gui', 'apps', 'valuation', 'definitions', 'nodes.json')), 'r') as fp:
        #     self.NODES = json.load(fp)

        # self.node_names = pd.read_excel(self.home_path+'nodeid.xlsx', sheetname=None)
        self.delimiter = " @ "  # delimiter used to split information in id_key

    def get_node_name(self, node_id, ISO):
        """
        Retrieve the node name corresponding to the given node_id using the lookup table loaded during initialization.

        :param node_id: A string or int of a node ID.
        :return: The corresponding node name as a string.
        """
        # TODO: map node_id to node name

        return str(node_id)

    def get_pjm_lmp_data(self, *args):
        """Retrieve LMP data for PJM (deprecated since 1.0)."""
        logging.info("DMS: Loading PJM DA-LMP")
        try:
            # attempt to access data if it is already loaded
            lmp_da = self.get_data(*args)
        except KeyError:
            # load the data and add it to the DMS
            lmp_da = dpt.read_pjm_da_lmp(*args)
            self.add_data(lmp_da, *args)
        finally:
            return lmp_da

    def get_pjm_reg_price_data(self, *args):
        """Retrieve regulation price data for PJM (deprecated since 1.0)."""
        logging.info("DMS: Loading PJM regulation prices")
        try:
            # attempt to access data if it is already loaded
            RegCCP = self.get_data(*args + ("RegCCP",))
            RegPCP = self.get_data(*args + ("RegPCP",))
        except KeyError:
            # load the data and add it to the DMS
            RegCCP, RegPCP = dpt.read_pjm_reg_price(*args)
            self.add_data({"RegCCP": RegCCP, "RegPCP": RegPCP}, *args)
        finally:
            return RegCCP, RegPCP

    def get_pjm_mileage_data(self, *args):
        """Retrieve regulation mileage data for PJM (deprecated since 1.0)."""
        logging.info("DMS: Loading PJM mileage data")
        try:
            # attempt to access data if it is already loaded
            MR = self.get_data(*args + ("MR",))
            RA = self.get_data(*args + ("RA",))
            RD = self.get_data(*args + ("RD",))
        except KeyError:
            # load the data and add it to the DMS
            MR, RA, RD = dpt.read_pjm_mileage(*args)
            self.add_data({"MR": MR, "RA": RA, "RD": RD}, *args)
        finally:
            return MR, RA, RD

    def get_pjm_reg_signal_data(self, *args):
        """Retrieve regulation signal data for PJM (deprecated since 1.0)."""
        logging.info("DMS: Loading PJM regulation signal")
        try:
            # attempt to access data if it is already loaded
            RUP = self.get_data(*args + ("RegUp",))
            RDW = self.get_data(*args + ("RegDown",))
        except KeyError:
            # load the data and add it to the DMS
            RUP, RDW = dpt.read_pjm_reg_signal(*args)
            self.add_data({"RegUp": RUP, "RegDown": RDW}, *args)
        finally:
            return RUP, RDW

    def get_pjm_data(self, year, month, nodeid):
        """Retrieve data for PJM."""
        path = os.path.join(self.home_path, "PJM")

        nodeid = str(nodeid)
        year = str(year)
        month = str(month)

        lmp_key = self.delimiter.join([path, year, month, nodeid, "SPP"])
        mr_key = self.delimiter.join([path, year, month, "MR"])
        ra_key = self.delimiter.join([path, year, month, "RA"])
        rd_key = self.delimiter.join([path, year, month, "RD"])
        rccp_key = self.delimiter.join([path, year, month, "RegCCP"])
        rpcp_key = self.delimiter.join([path, year, month, "RegPCP"])

        try:
            # attempt to access data if it is already loaded
            lmp_da = self.get_data(lmp_key)
            MR = self.get_data(mr_key)
            RA = self.get_data(ra_key)
            RD = self.get_data(rd_key)
            RegCCP = self.get_data(rccp_key)
            RegPCP = self.get_data(rpcp_key)
        except KeyError:
            # load the data and add it to the DMS
            lmp_da, MR, RA, RD, RegCCP, RegPCP = dpt.read_pjm_data(
                path, year, month, nodeid
            )

            self.add_data(lmp_da, lmp_key)
            self.add_data(MR, mr_key)
            self.add_data(RA, ra_key)
            self.add_data(RD, rd_key)
            self.add_data(RegCCP, rccp_key)
            self.add_data(RegPCP, rpcp_key)

        return lmp_da, MR, RA, RD, RegCCP, RegPCP


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
