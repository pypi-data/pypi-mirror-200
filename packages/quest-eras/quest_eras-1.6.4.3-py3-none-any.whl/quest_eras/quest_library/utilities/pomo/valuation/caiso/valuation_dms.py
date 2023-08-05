"""Data Manager for Valuation Tool."""

from __future__ import absolute_import
import os

from quest_eras.quest_library.utilities.pomo.dms import DataManagementSystem
import quest_eras.quest_library.utilities.pomo.valuation.caiso.data_processing_tools as dpt


class ValuationDMSCAISO(DataManagementSystem):
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

    def get_caiso_data(self, year, month, nodeid):
        """Retrieve data for CAISO."""
        path = os.path.join(self.home_path, "CAISO")

        year = str(year)
        month = str(month)

        lmp_key = self.delimiter.join([path, year, month, nodeid, "LMP"])
        aspru_key = self.delimiter.join([path, year, month, "ASPRU"])
        asprd_key = self.delimiter.join([path, year, month, "ASPRD"])
        asprmu_key = self.delimiter.join([path, year, month, "ASPRMU"])
        asprmd_key = self.delimiter.join([path, year, month, "ASPRMD"])
        rmu_mm_key = self.delimiter.join([path, year, month, "RMU_MM"])
        rmd_mm_key = self.delimiter.join([path, year, month, "RMD_MM"])
        rmu_pacc_key = self.delimiter.join([path, year, month, "RMU_PACC"])
        rmd_pacc_key = self.delimiter.join([path, year, month, "RMD_PACC"])

        try:
            # attempt to access data if it is already loaded
            lmp_da = self.get_data(lmp_key)
            aspru_da = self.get_data(aspru_key)
            asprd_da = self.get_data(asprd_key)
            asprmu_da = self.get_data(asprmu_key)
            asprmd_da = self.get_data(asprmd_key)
            rmu_mm = self.get_data(rmu_mm_key)
            rmd_mm = self.get_data(rmd_mm_key)
            rmu_pacc = self.get_data(rmu_pacc_key)
            rmd_pacc = self.get_data(rmd_pacc_key)
        except KeyError:
            # load the data and add it to the DMS
            # lmp_da, MR, RA, RD, RegCCP, RegPCP = read_pjm_data(path, year, month, nodeid)
            (
                lmp_da,
                aspru_da,
                asprd_da,
                asprmu_da,
                asprmd_da,
                rmu_mm,
                rmd_mm,
                rmu_pacc,
                rmd_pacc,
            ) = dpt.read_caiso_data(path, year, month, nodeid)

            self.add_data(lmp_da, lmp_key)
            self.add_data(aspru_da, aspru_key)
            self.add_data(asprd_da, asprd_key)
            self.add_data(asprmu_da, asprmu_key)
            self.add_data(asprmd_da, asprmd_key)
            self.add_data(rmu_mm, rmu_mm_key)
            self.add_data(rmd_mm, rmd_mm_key)
            self.add_data(rmu_pacc, rmu_pacc_key)
            self.add_data(rmd_pacc, rmd_pacc_key)

        return (
            lmp_da,
            aspru_da,
            asprd_da,
            asprmu_da,
            asprmd_da,
            rmu_mm,
            rmd_mm,
            rmu_pacc,
            rmd_pacc,
        )

    ####################################################################################################################


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
