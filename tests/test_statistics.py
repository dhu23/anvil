from mbte.geometric_brownian_motion import GBMParameters
import numpy as np
import pytest

def test_statistical_gbm():
    gbm_params = GBMParameters(0.001, 0.05)
    rng = np.random.default_rng(9)
    dt = 1
    log_returns = gbm_params.sample(10, dt, rng)
    log_returns