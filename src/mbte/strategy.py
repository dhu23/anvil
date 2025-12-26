'''
Strategy abstract-base class
'''

from abc import ABC, abstractmethod
from mbte.events import Event, SignalEvent



class Strategy(ABC):
    '''
    The role of a strategy is to process external events and produces a
    trading signal that can be actioned by the portfolio
    '''
    @abstractmethod
    def on_event(self, event: Event) -> SignalEvent | None:
        pass