'''
Back-testing processor that controls 
- plumbing and sequencing data/event flow
- clock advancement
- owning components in the full system

The Processor should 
'''

from mbte.event_processing import EventStore
from mbte.events import EventType
from mbte.execution import Execution
from mbte.portfolio import Portfolio
from mbte.strategy import Strategy

import heapq

class Processor(object):
    def __init__(
            self, 
            event_stores: list[EventStore], 
            strategy: Strategy, 
            portfolio: Portfolio,
            execution: Execution
    ):
        self._event_stores = event_stores
        self._strategy = strategy
        self._portfolio = portfolio
        self._execution = execution

        self._setup_priority_queue()

    def _setup_priority_queue(self):
        pass

    def run(self):
        while self._event_store.has_event():
            event = self._event_store.next_event()
            if event is None:
                continue

            # process the event to generate signal
            signal = self._strategy.on_event(event)
            if signal is None:
                continue
        
            # process trading event signal
            order = self._portfolio.on_signal(signal)
            
            if order is None:
                continue

            # trade the order
            self._execution.send(order)
            
## A timestamp ordered priority queue
