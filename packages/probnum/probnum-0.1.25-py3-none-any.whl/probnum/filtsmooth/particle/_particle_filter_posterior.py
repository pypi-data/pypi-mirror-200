"""Particle filtering posterior."""

from typing import Optional

import numpy as np

from probnum import randvars
from probnum.filtsmooth import _timeseriesposterior
from probnum.typing import ArrayLike, FloatLike, ShapeLike


class ParticleFilterPosterior(_timeseriesposterior.TimeSeriesPosterior):
    """Posterior distribution of a particle filter.."""

    def __call__(self, t):
        raise NotImplementedError("Particle filters do not provide dense output.")

    # The methods below are not implemented (yet?).

    def interpolate(self, t: FloatLike) -> randvars.RandomVariable:
        raise NotImplementedError

    def sample(
        self,
        rng: np.random.Generator,
        t: Optional[ArrayLike] = None,
        size: Optional[ShapeLike] = (),
    ) -> np.ndarray:
        raise NotImplementedError("Sampling is not implemented.")

    def transform_base_measure_realizations(
        self,
        base_measure_realizations: np.ndarray,
        t: Optional[ArrayLike] = None,
    ) -> np.ndarray:
        raise NotImplementedError(
            "Transforming base measure realizations is not implemented."
        )
