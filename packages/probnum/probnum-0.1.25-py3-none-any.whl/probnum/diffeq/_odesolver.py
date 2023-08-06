"""ODE solver interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import abc
import dataclasses
from typing import Iterable, Iterator, Optional, Union

import numpy as np

from probnum import problems
from probnum.diffeq import callbacks as callback_module  # see below
from probnum.typing import FloatLike

# From above:
# One of the argument to solve() is called 'callback',
# and we do not want to redefine variable namespaces.

CallbackType = Union[
    callback_module.ODESolverCallback, Iterable[callback_module.ODESolverCallback]
]
"""Callback interface type."""


class ODESolver(ABC):
    """Interface for ODE solvers in ProbNum."""

    def __init__(
        self,
        steprule,
        order,
    ):
        self.steprule = steprule
        self.order = order  # e.g.: RK45 has order=5, IBM(q) has order=q
        self.num_steps = 0

    def solve(
        self,
        ivp: problems.InitialValueProblem,
        stop_at: Iterable[FloatLike] = None,
        callbacks: Optional[CallbackType] = None,
    ):
        """Solve an IVP.

        Parameters
        ----------
        ivp
            Initial value problem.
        stop_at
            Time-points through which the solver must step. Optional. Default is None.
        callbacks
            Callbacks to happen after every accepted step.
        """
        times, rvs = [], []
        for state in self.solution_generator(ivp, stop_at=stop_at, callbacks=callbacks):
            times.append(state.t)
            rvs.append(state.rv)

        odesol = self.rvlist_to_odesol(times=times, rvs=rvs)
        return self.postprocess(odesol)

    def solution_generator(
        self,
        ivp: problems.InitialValueProblem,
        stop_at: Iterable[FloatLike] = None,
        callbacks: Optional[CallbackType] = None,
    ):
        """Generate ODE solver steps."""

        callbacks, stopper_state = self._process_event_inputs(callbacks, stop_at)

        state = self.initialize(ivp)
        yield state

        dt = self.steprule.firststep

        # Use state.ivp in case a callback modifies the IVP
        while state.t < state.ivp.tmax:
            if stopper_state is not None:
                dt, stopper_state = _adjust_time_step(stopper_state, t=state.t, dt=dt)

            state, dt = self.perform_full_step(state, dt)

            if callbacks is not None:
                for callback in callbacks:
                    state = callback(state)

            self.num_steps += 1
            yield state

    @staticmethod
    def _process_event_inputs(callbacks, stop_at_locations):
        """Process callbacks and time-stamps into a format suitable for solve()."""

        def promote_callback_type(cbs):
            return cbs if isinstance(cbs, abc.Iterable) else [cbs]

        if callbacks is not None:
            callbacks = promote_callback_type(callbacks)
        if stop_at_locations is not None:
            loc_iter = iter(stop_at_locations)
            time_stopper = _TimeStopperState(
                locations=loc_iter, next_location=next(loc_iter)
            )
        else:
            time_stopper = None
        return callbacks, time_stopper

    def perform_full_step(self, state, initial_dt):
        """Perform a full ODE solver step.

        This includes the acceptance/rejection decision as governed by error estimation
        and steprule.
        """
        dt = initial_dt
        step_is_sufficiently_small = False
        proposed_state = None
        while not step_is_sufficiently_small:
            proposed_state = self.attempt_step(state, dt)

            # Acceptance/Rejection due to the step-rule
            internal_norm = self.steprule.errorest_to_norm(
                errorest=proposed_state.error_estimate,
                reference_state=proposed_state.reference_state,
            )
            step_is_sufficiently_small = self.steprule.is_accepted(internal_norm)
            suggested_dt = self.steprule.suggest(
                dt, internal_norm, localconvrate=self.order + 1
            )

            # Get a new step-size for the next step
            if step_is_sufficiently_small:
                dt = min(suggested_dt, state.ivp.tmax - proposed_state.t)
            else:
                dt = min(suggested_dt, state.ivp.tmax - state.t)

        self.method_callback(state)
        return proposed_state, dt

    @abstractmethod
    def initialize(self, ivp):
        """Returns t0 and y0 (for the solver, which might be different to ivp.y0)"""
        raise NotImplementedError

    @abstractmethod
    def attempt_step(self, state, dt):
        """Compute a step from the current state to the next state with increment dt.

        This does not include the acceptance/rejection decision from the step-size
        selection. Therefore, if dt turns out to be too large, the result of
        attempt_step() will be discarded.
        """
        raise NotImplementedError

    @abstractmethod
    def rvlist_to_odesol(self, times, rvs):
        """Create an ODESolution object."""
        raise NotImplementedError

    # We disable the pylint warning, because subclasses _do_ use 'self'
    # but pylint does not seem to realize this.
    def postprocess(self, odesol):  # pylint: disable="no-self-use"
        """Process the ODESolution object before returning."""
        return odesol

    def method_callback(self, state):
        """Optional callback.

        Can be overwritten. Do this as soon as it is clear that the
        current guess is accepted, but before storing it. No return. For
        example: tune hyperparameters (sigma).
        """


@dataclasses.dataclass
class _TimeStopperState:
    locations: Iterator
    next_location: FloatLike


def _adjust_time_step(stopper_state, t, dt):
    if t >= stopper_state.next_location:
        try:
            next_location = next(stopper_state.locations)
        except StopIteration:
            next_location = np.inf
    else:
        next_location = stopper_state.next_location

    if t + dt > next_location:
        dt = next_location - t
    return dt, _TimeStopperState(
        locations=stopper_state.locations, next_location=next_location
    )
