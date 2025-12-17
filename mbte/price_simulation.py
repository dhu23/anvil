# Generate simulated prices
# flavors of simulation supported include the following
# 1. flat price
# 2. 

import itertools
import math

from mbte.statistics import GeometricBrownianMotionParameters


def generate_flat(price, num):
    return list(itertools.repeat(price, num))


def generate_random_walk(
        init_price: float, num: int, params: GeometricBrownianMotionParameters
):
    ret = [init_price]
    current_price = init_price
    for _ in range(num - 1):
        current_price = params.next_value(current_price, 1)
        ret.append(current_price)
    return ret


def generate_mean_reversion():
    pass

