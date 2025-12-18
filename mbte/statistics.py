from dataclasses import dataclass
import random
import math

@dataclass(frozen=True)
class GBMParameters:
    mu: float
    sigma: float

    def __post_init__(self):
        if self.mu is None or self.sigma is None:
            raise ValueError("parameters cannot be None")

        if self.sigma <= 0.0:
            raise ValueError("sigma must be positive")

    def generate_log_return(self, dt: float, rng: random.Random):
        '''
        generates log return:
        ln(P_1/P_0)  = ln(P_1) - ln(P_0)
                     = (mu - sigma**2 / 2) * dt + sigma * sqrt(dt) * epsilon
        where
            1. don't forgot the drift corection term
            2. epsilon ~ N(0, 1)
        '''
        return (
            (self.mu - self.sigma**2 / 2) * dt 
            + self.sigma * math.sqrt(dt) * rng.gauss(0.0, 1.0)
        )