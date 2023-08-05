"""Objective and Contraints Class."""

from __future__ import absolute_import
import pyomo.environ as pom
import math


class ExpressionsBlock:
    """Create blocks for objective and constraint functions and assigns them to the Pyomo model.

    Note-
    1. Time step is 1 hour
    2. The state of charge is actually the state of energy in MWh except for the intial and final state of charge.
    3. The intial and final state of charge are in percent.
    """

    def __init__(self, market_type):
        self._market_type = market_type

    @property
    def market_type(self):
        """Market to create blocks for."""
        return self._market_type

    @market_type.setter
    def market_type(self, value):
        self._market_type = value

    def set_expressions(self, model):
        """Generate the objective and constraint expressions for model."""
        block_obj = pom.Block()
        model.objectives = block_obj

        block_con = pom.Block()
        model.constraints = block_con

        if self.market_type == "arbitrage":
            self._objective_arb(block_obj)
            self._constraints_arb(block_con)
        elif self.market_type == "pfp":
            self._objective_nyiso_pfp(block_obj)
            self._constraints_nyiso_pfp(block_con)
        else:
            raise ValueError("Invalid market type specified!")

    def _objective_arb(self, block):
        eq_objective_arb(block)

    def _constraints_arb(self, block):
        eq_stateofcharge_arb(block)
        eq_stateofcharge_initial(block)
        eq_stateofcharge_final(block)
        ineq_stateofcharge_minimum(block)
        ineq_stateofcharge_maximum(block)
        ineq_power_limit(block)
        
    def _objective_nyiso_pfp(self, block):
        eq_objective_nyiso_pfp(block)

    def _constraints_nyiso_pfp(self, block):
        eq_stateofcharge_nyiso_pfp(block)
        eq_stateofcharge_initial(block)
        eq_stateofcharge_final(block)
        ineq_stateofcharge_minimum_reserve_oneprod(block)
        ineq_stateofcharge_maximum_reserve_oneprod(block)
        ineq_power_limit_oneprod(block)

#############################
# Arbitrage only ############
#############################


def eq_objective_arb(m):
    """Formulate net revenue over the time horizon for arbitrage only."""
    mp = m.parent_block()

    _expr = sum(
        (mp.price_electricity[t] * mp.q_d[t] - mp.price_electricity[t] * mp.q_r[t])
        * math.e ** (-t * mp.R)
        for t in mp.time
    )

    mp.objective_expr += _expr
    m.objective_rt = pom.Expression(expr=_expr)


def eq_stateofcharge_arb(m):
    """Formulate state of charge for storage device in participating in arbitrage only."""
    mp = m.parent_block()

    def _eq_stateofcharge_arb(_m, t):
        return (
            mp.Self_discharge_efficiency * mp.s[t]
            + mp.Round_trip_efficiency * mp.q_r[t]
            - mp.q_d[t]
            == mp.s[t + 1]
        )

    m.stateofcharge = pom.Constraint(mp.time, rule=_eq_stateofcharge_arb)


def ineq_power_limit(m):
    """Limit the energy charged and discharged at each timestep to the device power rating."""
    mp = m.parent_block()

    def _ineq_power_limit(_m, t):
        return mp.Power_rating >= mp.q_r[t] + mp.q_d[t]

    m.power_limit = pom.Constraint(mp.time, rule=_ineq_power_limit)

#################################
#   NYISO Pay-for-Performance  ##
#            FW                ##
#################################
def eq_objective_nyiso_pfp(m):
    """Formulate net revenue over the time horizon for pay-for-performance in the NYISO market."""
    mp = m.parent_block()

    _expr = sum(
        (
            mp.price_electricity[t] * mp.q_d[t]
            - mp.price_electricity[t] * mp.q_r[t]
            + mp.price_electricity[t] * mp.fraction_reg_up[t] * mp.q_reg[t]
            - mp.price_electricity[t] * mp.fraction_reg_down[t] * mp.q_reg[t]
            + mp.q_reg[t] * mp.price_regulation[t] * (1 - 1.1 * (1 - mp.perf_score[t]))
        )
        * math.e ** (-t * mp.R)
        for t in mp.time
    )

    mp.objective_expr += _expr
    m.objective_rt = pom.Expression(expr=_expr)


def eq_stateofcharge_nyiso_pfp(m):
    """Formulate state of charge for storage device in NYISO market."""
    mp = m.parent_block()

    def _eq_stateofcharge_nyiso_pfp(_m, t):
        return (
            mp.Self_discharge_efficiency * mp.s[t]
            + mp.Round_trip_efficiency * mp.q_r[t]
            - mp.q_d[t]
            + mp.Round_trip_efficiency * mp.fraction_reg_down[t] * mp.q_reg[t]
            - mp.fraction_reg_up[t] * mp.q_reg[t]
            == mp.s[t + 1]
        )

    m.stateofcharge = pom.Constraint(mp.time, rule=_eq_stateofcharge_nyiso_pfp)

##################################
#          Generic              ##
#     Equality Constraints      ##
##################################


def eq_stateofcharge_initial(m):
    """Set the initial state of energy equal to the inital state of charge time the energy capacity."""
    mp = m.parent_block()

    def _eq_stateofcharge_initial(_m, t):
        if not t == 0:
            return pom.Constraint.Skip
        else:
            return mp.s[t] == mp.State_of_charge_init * mp.Energy_capacity

    m.stateofcharge_initial = pom.Constraint(
        mp.soc_time, rule=_eq_stateofcharge_initial
    )


def eq_stateofcharge_final(m):
    """Set the final state of energy equal to the inital state of energy."""
    mp = m.parent_block()

    def _eq_stateofcharge_final(_m, t):
        if not t == mp.soc_time[-1]:
            return pom.Constraint.Skip
        else:
            return mp.s[t] == mp.State_of_charge_init * mp.Energy_capacity

    m.stateofcharge_final = pom.Constraint(mp.soc_time, rule=_eq_stateofcharge_final)


##################################
#          Generic              ##
#   Inequality Constraints      ##
##################################


def ineq_stateofcharge_minimum(m):
    """Keep the state of energy of the energy storage device above the minimum at any given time."""
    mp = m.parent_block()

    def _ineq_stateofcharge_minimum(_m, t):
        return mp.s[t] >= mp.State_of_charge_min * mp.Energy_capacity

    m.stateofcharge_minimum = pom.Constraint(
        mp.soc_time, rule=_ineq_stateofcharge_minimum
    )


def ineq_stateofcharge_maximum(m):
    """Keep the state of energy of the energy storage device below the maximum at any given time."""
    mp = m.parent_block()

    def _ineq_stateofcharge_maximum(_m, t):
        return mp.s[t] <= mp.State_of_charge_max * mp.Energy_capacity

    m.stateofcharge_maximum = pom.Constraint(
        mp.soc_time, rule=_ineq_stateofcharge_maximum
    )


def ineq_stateofcharge_minimum_reserve_oneprod(m):
    """Keep the state of energy of the energy storage device above (the minimum + a minimum reserve amount) at any given time.

    Note-
    1. The minimum state of charge is defined by the storage operator following operational/safety/longevity guidelines.
    2. The minimum reserve amount is required by the market so that a resource has enough energy ready to be called upon for discharging.
    """
    mp = m.parent_block()

    def _ineq_stateofcharge_minimum(_m, t):
        return (
            mp.s[t + 1]
            >= mp.Reserve_reg_min  # The number of hrs that storage device can at least discharge at q_reg rate.
            * mp.q_reg[t]
            + mp.State_of_charge_min * mp.Energy_capacity
        )

    m.stateofcharge_minimum = pom.Constraint(mp.time, rule=_ineq_stateofcharge_minimum)


def ineq_stateofcharge_maximum_reserve_oneprod(m):
    """Keep the state of energy of the energy storage device below (the maximum + a headroom) at any given time, accounting for penalty aversion parameters.

    Note-
    1. The maximum state of charge is defined by the storage operator following operational/safety/longevity guidelines.
    2. The headroom is required by the market so that a resource has enough space ready to be called upon for charging.
    """
    mp = m.parent_block()

    def _ineq_stateofcharge_maximum(_m, t):
        return (
            mp.s[t + 1]
            <= mp.State_of_charge_max * mp.Energy_capacity
            - mp.Round_trip_efficiency
            * mp.Reserve_reg_max  # The number of hrs that storage device can at least charge at q_reg rate.
            * mp.q_reg[t]
        )

    m.stateofcharge_maximum = pom.Constraint(mp.time, rule=_ineq_stateofcharge_maximum)

def ineq_power_limit_oneprod(m):
    """Limit the energy charged and discharged at each timestep to the device power rating."""
    mp = m.parent_block()

    def _ineq_power_limit_oneprod(_m, t):
        return mp.Power_rating >= mp.q_r[t] + mp.q_d[t] + mp.q_reg[t]

    m.power_limit = pom.Constraint(mp.time, rule=_ineq_power_limit_oneprod)