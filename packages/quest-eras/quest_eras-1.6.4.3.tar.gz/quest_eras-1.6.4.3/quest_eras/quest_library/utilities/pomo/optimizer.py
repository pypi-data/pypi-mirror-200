"""Optimizer abstract class."""

from abc import ABCMeta, abstractmethod
import logging
import pyutilib
import pyomo.environ as pom
from pyomo.opt import TerminationCondition
from six import with_metaclass

# from pyomo.environ import *


class Optimizer(with_metaclass(ABCMeta)):
    """Abstract base class for Pyomo ConcreteModel optimization framework."""

    def __init__(self, solver="glpk"):
        self._model = pom.ConcreteModel()
        self._solver = solver

        self._results = None

    @property
    def model(self):
        """Create a Pyomo ConcreteModel."""
        return self._model

    @property
    def solver(self):
        """Specify the name of the solver for Pyomo to use."""
        return self._solver

    @property
    def results(self):
        """Return results in a DataFrame containing indices, decision variables, model parameters and derived quantities."""
        return self._results

    @abstractmethod
    def _set_model_param(self):
        """Assign model parameters and their default values to the model."""
        pass

    @abstractmethod
    def _set_model_var(self):
        """Initialize model decision variables for the model."""
        pass

    @abstractmethod
    def instantiate_model(self):
        """Instantiate the model and assign Optimizer attributes to model attributes."""
        pass

    @abstractmethod
    def populate_model(self):
        """Set model parameters, variables, and an ExpressionsBlock object for defining objectives and constraints."""
        pass

    def solve_model(self):
        """Solve the model using the specified solver."""
        if self.solver == "neos":
            opt = pom.SolverFactory("cbc")
            solver_manager = pom.SolverManagerFactory("neos")
            results = solver_manager.solve(self.model, opt=opt)
        else:
            solver = pom.SolverFactory(self.solver)
            results = solver.solve(self.model, tee=False, keepfiles=False)

        assert results.solver.termination_condition.key == "optimal"

        self._process_results()

    @abstractmethod
    def _process_results(self):
        """Compute derived quantities of interest and creating the results DataFrame."""
        pass

    @abstractmethod
    def get_results(self):
        """Return the results DataFrame plus any other quantities of interest."""
        pass

    def run(self):
        """Instantiate, create, and solve the optimizer model based on provided information.

        Use if no steps are needed between constructing the model and solving it.
        """
        self.instantiate_model()
        self.populate_model()

        if self.solver == "neos":
            opt = pom.SolverFactory("cbc")
            solver_manager = pom.SolverManagerFactory("neos")
            results = solver_manager.solve(self.model, opt=opt)
        else:
            solver = pom.SolverFactory(self.solver)

            try:
                solver.available()
            except pyutilib.common._exceptions.ApplicationError as e:
                logging.error("Optimizer: {error}".format(error=e))
            else:
                results = solver.solve(self.model, tee=True, keepfiles=False)

        try:
            assert results.solver.termination_condition == TerminationCondition.optimal
        except AssertionError:
            logging.error(
                "Optimizer: An optimal solution could not be obtained. (solver termination condition: {0})".format(
                    results.solver.termination_condition.key
                )
            )
            raise (
                AssertionError(
                    "An optimal solution could not be obtained. (solver termination condition: {0})".format(
                        results.solver.termination_condition.key
                    )
                )
            )
        else:
            self._process_results()

        return self.get_results()

    def set_model_parameters(self, **kwargs):
        """Set model parameters in kwargs to their respective values."""
        for kw_key, kw_value in kwargs.items():
            logging.info(
                "Optimizer: Setting {param} to {value}".format(
                    param=kw_key, value=kw_value
                )
            )
            setattr(self.model, kw_key, kw_value)
            setattr(self.model, kw_key, kw_value)
            setattr(self.model, kw_key, kw_value)
            setattr(self.model, kw_key, kw_value)
