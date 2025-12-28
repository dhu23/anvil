

from abc import ABC, abstractmethod
from mbte.event_processing import EventProcessor
from mbte.events import Event, FillEvent, OrderEvent, SignalEvent


class Strategy(ABC):
    '''
    The role of a strategy is to process external events and produces a
    trading signal that can be actioned by the portfolio
    '''
    @abstractmethod
    def on_event(self, event: Event) -> SignalEvent | None:
        pass


class Portfolio(ABC):
    @abstractmethod
    def on_signal(self, signal: SignalEvent) -> OrderEvent | None:
        pass

    @abstractmethod
    def on_fill(self, fill: FillEvent) -> OrderEvent | None:
        pass


class Execution(ABC):
    @abstractmethod
    def receive(self, order: OrderEvent) -> None:
        pass


class MbteProcessor(EventProcessor):
    def __init__(
            self, 
            strategy: Strategy, 
            portfolio: Portfolio, 
            execution: Execution,
    ):
        self._strategy = strategy
        self._portfolio = portfolio
        self._execution = execution

    def process(self, event: Event) -> None:
        # process the event to generate signal
        signal = self._strategy.on_event(event)
        if signal is None:
            return
        
        # process the signal event
        order = self._portfolio.on_signal(signal)
        if order is None:
            return

        # trade the order out        
        self._execution.receive(order)
