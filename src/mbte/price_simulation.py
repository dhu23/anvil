# Generate simulated prices

import math
import random

from mbte.statistics import GBMParameters


def generate_gbm_price(
        init_price: float, num: int, gbm_params: GBMParameters, rng: random.Random
):
    ret = [init_price]
    log_returns = []
    current_price = init_price
    dt = 1
    for _ in range(num - 1):
        r = gbm_params.generate_log_return(dt, rng)
        log_returns.append(r)
        current_price = current_price * math.exp(r)
        ret.append(current_price)
    return ret


