"""Example for running valuation simulations."""
from __future__ import absolute_import

import logging
import matplotlib.pyplot as plt

from op_handler import ValuationOptimizerHandler as val_op


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
    handler = val_op(
        solver_name="glpk",
        data_path="[Add data path here]",
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
