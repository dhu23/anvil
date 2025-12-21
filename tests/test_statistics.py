from mbte import gbm
import numpy as np
import pytest


def test_gbm_statistical_property():
    # population mean of the log returns would be 0
    # population std of the log returns would be 1
    # log returns of this distrubtion is N(0, 1)
    gbm_params = gbm.GBMParameters(0.5, 1)
    rng = np.random.default_rng(9)
    dt = 1

    mean = gbm.gbm_log_return_mean(gbm_params, dt)
    std = gbm.gbm_log_return_std(gbm_params, dt)
    print(f'population mean={mean}, std={std}
    
    # use abs tolarence for small values
    assert 0 == pytest.approx(mean, abs=0.05)
    assert 1 == pytest.approx(std, rel=0.05)

    # sampling 10000 data point from population
    log_returns = gbm.log_returns(gbm_params, 10000, dt, rng)
    sample_mean = np.mean(log_returns)
    sample_std = np.std(log_returns)
    print(f'sample mean={sample_mean}, std={sample_std}')

    assert 0 == pytest.approx(sample_mean, abs=0.05)
    assert 1 == pytest.approx(sample_std, rel=0.05)

    # test sampling mean std (CLT)
    # in this case the stdev of the mean of sampling should be std/100

    sample_means = [
        np.mean(gbm.log_returns(gbm_params, 10000, dt, rng)) 
        for _ in range(10000)
    ]

    mean_of_sample_means = np.mean(sample_means)
    std_of_sample_means = np.std(sample_means)
    print(f'sample mean distribution, mean={mean_of_sample_means}, std={std_of_sample_means}')

    assert 0 == pytest.approx(mean_of_sample_means, abs=0.05)
    assert 0.01 == pytest.approx(std_of_sample_means, rel=0.05)
