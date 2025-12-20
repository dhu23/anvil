'''
Geometric Brownian Motion (GBM)
'''

from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class GBMParameters:
    mu: float
    sigma: float

    def __post_init__(self):
        if self.mu is None or self.sigma is None:
            raise ValueError("parameters cannot be None")

        if self.sigma <= 0.0:
            raise ValueError("sigma must be positive")


def log_returns(gbm_params: GBMParameters, n: int, dt: float, rng):
    '''
    generates a total count of n i.i.d log return:
    ln(P_1/P_0) = ln(P_1) - ln(P_0)
                = (mu - sigma**2 / 2) * dt + sigma * sqrt(dt) * epsilon
    where
        1. don't forgot the drift corection term
        2. epsilon ~ N(0, 1)
    '''
    return rng.normal(
        loc=(gbm_params.mu - gbm_params.sigma**2 / 2) * dt,
        scale=gbm_params.sigma * math.sqrt(dt),
        size=n,
    )