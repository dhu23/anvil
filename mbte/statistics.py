from dataclasses import dataclass
import random
import math

@dataclass(frozen=True)
class GeometricBrownianMotionParameters:
    mu: float
    sigma: float

    def __post_init__(self):
        if self.sigma <= 0.0:
            raise ValueError("sigma must be positive")

    def generate(self, dt):
        '''
        generates ln(P_1) - ln(P_0) = mu * dt + sigma * sqrt(dt) * epsilon
        '''
        return self.mu * dt + self.sigma * math.sqrt(dt) * random.gauss()
 
    def next_value(self, current_value, dt):
        return current_value * math.exp(self.generate(dt))
