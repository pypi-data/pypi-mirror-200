"""Example for running valuation simulations."""
from __future__ import absolute_import

# import sys

# sys.path.append("C:/work/quest-library/")
import logging
from datetime import datetime
import calendar
import pyutilib
import matplotlib.pyplot as plt

import quest_eras.quest_library.utilities.pomo.valuation.caiso.valuation_optimizer as caiso_op
from quest_eras.quest_library.utilities.pomo.valuation.caiso.valuation_dms import (
    ValuationDMSCAISO,
)
import quest_eras.quest_library.utilities.pomo.valuation.ercot.valuation_optimizer as ercot_op
from quest_eras.quest_library.utilities.pomo.valuation.ercot.valuation_dms import (
    ValuationDMSERCOT,
)
import quest_eras.quest_library.utilities.pomo.valuation.isone.valuation_optimizer as isone_op
from quest_eras.quest_library.utilities.pomo.valuation.isone.valuation_dms import (
    ValuationDMSISONE,
)
import quest_eras.quest_library.utilities.pomo.valuation.miso.valuation_optimizer as miso_op
from quest_eras.quest_library.utilities.pomo.valuation.miso.valuation_dms import (
    ValuationDMSMISO,
)
import quest_eras.quest_library.utilities.pomo.valuation.nyiso.valuation_optimizer as nyiso_op
from quest_eras.quest_library.utilities.pomo.valuation.nyiso.valuation_dms import (
    ValuationDMSNYISO,
)
import quest_eras.quest_library.utilities.pomo.valuation.pjm.valuation_optimizer as pjm_op
from quest_eras.quest_library.utilities.pomo.valuation.pjm.valuation_dms import (
    ValuationDMSPJM,
)
import quest_eras.quest_library.utilities.pomo.valuation.spp.valuation_optimizer as spp_op
from quest_eras.quest_library.utilities.pomo.valuation.spp.valuation_dms import (
    ValuationDMSSPP,
)


class ValuationOptimizerHandler:
    """A handler for creating and solving ValuationOptimizer instances as requested."""

    solved_ops = []

    def __init__(self, solver_name, data_path, **kwargs):
        self._solver_name = solver_name
        self.caiso_dms = ValuationDMSCAISO(data_path, **kwargs)
        self.ercot_dms = ValuationDMSERCOT(data_path, **kwargs)
        self.isone_dms = ValuationDMSISONE(data_path, **kwargs)
        self.miso_dms = ValuationDMSMISO(data_path, **kwargs)
        self.nyiso_dms = ValuationDMSNYISO(data_path, **kwargs)
        self.pjm_dms = ValuationDMSPJM(data_path, **kwargs)
        self.spp_dms = ValuationDMSSPP(data_path, **kwargs)

    @property
    def solver_name(self):
        """The name of the solver for Pyomo to call."""
        return self._solver_name

    @solver_name.setter
    def solver_name(self, value):
        self._solver_name = value

    def process_requests(self, requests, *args, **kwargs):
        """Generates and solves ValuationOptimizer models based on the given requests."""
        iso = requests["iso"]
        market_type = requests["market type"]
        node_id = str(requests["node id"])
        node_name = self.caiso_dms.get_node_name(node_id, iso)
        param_set = requests.get("param set", [None])

        solved_requests = []

        handler_status = set()

        for month, year in requests["months"]:
            param_set_iterator = iter(param_set)
            continue_param_loop = True

            while continue_param_loop:
                try:
                    params = next(param_set_iterator)
                except StopIteration:
                    break

                if iso == "PJM":
                    from quest_eras.quest_library.utilities.pomo.valuation.pjm.valuation_optimizer import (
                        IncompatibleDataException,
                    )  # find a better solution

                    lmp_da, MR, RA, RD, RegCCP, RegPCP = self.pjm_dms.get_pjm_data(
                        year, month, node_id
                    )
                    op = pjm_op.ValuationOptimizerPJM(market_type=market_type)

                    op.price_electricity = lmp_da
                    op.mileage_mult = MR
                    op.price_regulation = RegCCP
                    op.price_reg_service = RegPCP
                elif iso == "ERCOT":
                    from quest_eras.quest_library.utilities.pomo.valuation.ercot.valuation_optimizer import (
                        IncompatibleDataException,
                    )  # find a better solution

                    lmp_da, rd, ru = self.ercot_dms.get_ercot_data(
                        year, month, node_name
                    )
                    op = ercot_op.ValuationOptimizerERCOT(market_type=market_type)

                    op.price_electricity = lmp_da
                    op.price_reg_up = ru
                    op.price_reg_down = rd
                elif iso == "MISO":
                    from quest_eras.quest_library.utilities.pomo.valuation.miso.valuation_optimizer import (
                        IncompatibleDataException,
                    )  # find a better solution

                    lmp_da, regMCP = self.miso_dms.get_miso_data(year, month, node_name)
                    op = miso_op.ValuationOptimizerMISO(market_type=market_type)

                    op.price_electricity = lmp_da
                    op.price_regulation = regMCP
                elif iso == "ISONE":
                    from quest_eras.quest_library.utilities.pomo.valuation.isone.valuation_optimizer import (
                        IncompatibleDataException,
                    )  # find a better solution

                    daLMP, RegCCP, RegPCP, miMULT = self.isone_dms.get_isone_data(
                        year, month, node_id
                    )
                    op = isone_op.ValuationOptimizerISONE(market_type=market_type)

                    op.price_electricity = daLMP
                    op.price_regulation = RegCCP
                    op.price_reg_service = RegPCP
                    op.mileage_mult = miMULT
                elif iso == "NYISO":
                    from quest_eras.quest_library.utilities.pomo.valuation.nyiso.valuation_optimizer import (
                        IncompatibleDataException,
                    )  # find a better solution

                    lbmp_da, rcap_da = self.nyiso_dms.get_nyiso_data(
                        year, month, node_id
                    )
                    op = nyiso_op.ValuationOptimizerNYISO(market_type=market_type)

                    op.price_electricity = lbmp_da
                    op.price_regulation = rcap_da
                elif iso == "SPP":
                    from quest_eras.quest_library.utilities.pomo.valuation.spp.valuation_optimizer import (
                        IncompatibleDataException,
                    )  # find a better solution

                    lmp_da, mcpru_da, mcprd_da = self.spp_dms.get_spp_data(
                        year, month, node_name
                    )
                    op = spp_op.ValuationOptimizerSPP(market_type=market_type)

                    op.price_electricity = lmp_da
                    op.price_reg_up = mcpru_da
                    op.price_reg_down = mcprd_da
                elif iso == "CAISO":
                    from quest_eras.quest_library.utilities.pomo.valuation.caiso.valuation_optimizer import (
                        IncompatibleDataException,
                    )  # find a better solution

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
                    ) = self.caiso_dms.get_caiso_data(year, month, node_name)
                    op = caiso_op.ValuationOptimizerCAISO(market_type=market_type)

                    op.price_electricity = lmp_da
                    op.price_reg_up = aspru_da
                    op.price_reg_down = asprd_da
                    op.price_reg_serv_up = asprmu_da
                    op.price_reg_serv_down = asprmd_da
                    op.mileage_mult_ru = rmu_mm
                    op.mileage_mult_rd = rmd_mm
                    op.perf_score_ru = (
                        rmu_pacc  # TODO: give the option to the user to override this
                    )
                    op.perf_score_rd = rmd_pacc
                else:
                    logging.error("ValOp Handler: Invalid ISO provided.")
                    raise ValueError(
                        "Invalid ISO provided to ValuationOptimizer handler."
                    )

                if params:
                    op.set_model_parameters(**params)
                else:
                    continue_param_loop = False

                try:
                    solved_op = self._solve_model(op)
                except pyutilib.common._exceptions.ApplicationError as e:
                    logging.error("Op Handler: {error}".format(error=e))

                    if "No executable found" in e.args[0]:
                        # Could not locate solver executable
                        handler_status.add(
                            "* The executable for the selected solver could not be found; please check your installation."
                        )
                    else:
                        handler_status.add(
                            "* ({0} {1}) {2}. The problem may be infeasible.".format(
                                month, year, e.args[0]
                            )
                        )
                except IncompatibleDataException as e:
                    # Data exception raised by ValuationOptimizer
                    logging.error(e)
                    handler_status.add(
                        "* ({0} {1}) The time series data has mismatched sizes.".format(
                            month, year
                        )
                    )
                except AssertionError as e:
                    # An optimal solution could not be found as reported by the solver
                    logging.error("Op Handler: {error}".format(error=e))
                    handler_status.add(
                        "* ({0} {1}) An optimal solution could not be found; the problem may be infeasible.".format(
                            month, year
                        )
                    )
                else:
                    solved_op = self._save_to_solved_ops(
                        solved_op, iso, market_type, node_name, year, month, params
                    )
                    solved_requests.append(solved_op)

        logging.info("Op Handler: Finished processing requested jobs.")
        return solved_requests, handler_status

    def _solve_model(self, op):
        op.solver = self.solver_name
        op.run()

        return op

    @staticmethod
    def _save_to_solved_ops(op, iso, market_type, node_name, year, month, param_set):
        # time_finished = datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')
        time_finished = datetime.now().strftime("%b %d, %Y %H:%M:%S")
        name = " | ".join(
            [
                time_finished,
                str(node_name),
                str(year),
                calendar.month_abbr[int(month)],
                repr(param_set),
            ]
        )

        results_dict = {}

        results_dict["name"] = name
        results_dict["optimizer"] = op
        results_dict["iso"] = iso
        results_dict["market type"] = market_type
        results_dict["year"] = year
        results_dict["month"] = calendar.month_name[int(month)]
        results_dict["node"] = node_name
        if param_set:
            results_dict["params"] = param_set
        results_dict["time"] = time_finished
        results_dict["label"] = " ".join(
            [
                str(node_name),
                str(year),
                calendar.month_abbr[int(month)],
                repr(param_set),
            ]
        )

        ValuationOptimizerHandler.solved_ops.append(results_dict)

        return (name, op)

    def get_solved_ops(self):
        """Returns the list of solved Optimizer objects in reverse chronological order."""
        return_list = reversed(self.solved_ops)

        return return_list


if __name__ == "__main__":
    with open("valuation_optimizer.log", "w"):
        pass

    logging.basicConfig(
        filename="valuation_optimizer.log",
        format="[%(levelname)s] %(asctime)s: %(message)s",
        level=logging.INFO,
    )

    params = [
        {
            "Power_rating": 2,  # MW
            "Energy_capacity": 4,  # MWh
            "Self_discharge_efficiency": 1,
            "R": 0,  # Interest rate [hour^-1]
            "Round_trip_efficiency": 0.85,
            "Reserve_reg_min": 0,  # Fraction of q_reg bid to increase state of charge minimum by.
            "Reserve_reg_max": 1,  # Fraction of q_reg bid to decrease state of charge maximum by.
            "State_of_charge_min": 0,  # Fraction of energy capacity representing the minimum state of charge.
            "State_of_charge_max": 1,  # Fraction of energy capacity representing the maximum state of charge.
            "State_of_charge_init": 0.5,  # Initial state of charge as a fraction of energy capacity.
        }
    ]

    requests_PJM = {
        "iso": "PJM",
        "node id": 1,  # PJM-rTO
        "market type": ["arbitrage", "pfp"],
    }

    requests_MISO = {
        "iso": "MISO",
        "node id": "MICHIGAN.HUB",
        "market type": ["arbitrage", "pfp"],
    }

    requests_ISONE = {
        "iso": "ISONE",
        "node id": 4004,  # CONNECTICUT HUB
        "market type": ["arbitrage", "pfp"],
    }

    requests_NYISO = {
        "iso": "NYISO",
        "node id": 61761,  # NYC ZONE
        "market type": ["arbitrage", "pfp"],
    }

    requests_CAISO = {
        "iso": "CAISO",
        "node id": "TH_SP15_GEN-APND",  # SOUTH HUB
        "market type": ["arbitrage", "pfp"],
    }

    requests_SPP = {
        "iso": "SPP",
        "node id": "AECI",
        "market type": ["arbitrage", "pfp"],
    }

    requests_ERCOT = {
        "iso": "ERCOT",
        "node id": "HB_HOUSTON",
        "market type": ["arbitrage", "pfp"],
    }

    months = [(1, 2018), (2, 2018), (3, 2018)]
    requests = [
        requests_PJM,
        requests_MISO,
        requests_ISONE,
        requests_NYISO,
        requests_CAISO,
        requests_SPP,
        requests_ERCOT,
    ]
    handler = ValuationOptimizerHandler(
        solver_name="glpk",
        data_path="apps/valuation/data/",
        save_name="valuation_dms.p",
    )

    for request in requests:
        request["param set"] = params
        request["months"] = months
        market_types = request["market type"]
        for market_type in market_types:
            request["market type"] = market_type

            handler.process_requests(request)

    solved_ops = handler.get_solved_ops()

    results_dict = {
        "PJM": [],
        "MISO": [],
        "ISONE": [],
        "NYISO": [],
        "CAISO": [],
        "SPP": [],
        "ERCOT": [],
    }

    for result in solved_ops:
        if result["iso"] == "PJM":
            results_dict["PJM"].append(result)
        elif result["iso"] == "MISO":
            results_dict["MISO"].append(result)
        elif result["iso"] == "ISONE":
            results_dict["ISONE"].append(result)
        elif result["iso"] == "NYISO":
            results_dict["NYISO"].append(result)
        elif result["iso"] == "CAISO":
            results_dict["CAISO"].append(result)
        elif result["iso"] == "SPP":
            results_dict["SPP"].append(result)
        elif result["iso"] == "ERCOT":
            results_dict["ERCOT"].append(result)

    fig_ls = []
    for iso in results_dict:
        fig, ax = plt.subplots()
        arb = []
        pfp = []
        for result in results_dict[iso]:
            if result["market type"] == "arbitrage":
                arb.append((result["month"], result["optimizer"].gross_revenue))
            else:
                pfp.append((result["month"], result["optimizer"].gross_revenue))

        ax.bar(
            x=[date[0] for date in arb],
            height=[date[1] for date in arb],
            width=-0.5,
            align="edge",
            color=["blue"],
        )
        ax.bar(
            x=[date[0] for date in pfp],
            height=[date[1] for date in pfp],
            width=0.5,
            align="edge",
            color=["orange"],
        )
        ax.legend()
        ax.set_title("{} Gross Revenue 2018".format(iso))
        ax.set_ylabel("$")
        fig_ls.append((fig, ax))
        fig_ls.append((fig, ax))
        fig_ls.append((fig, ax))
