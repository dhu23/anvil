'''
Portfolio
'''

from typing import Any
from mbte.events import Event, FillEvent, OrderNew, SignalEvent


class Portfolio(object):
    def __init__(self, positiions):
        self._positions = dict(positiions)

    def on_signal(self, signal: SignalEvent) -> OrderNew | None:
        pass

    def on_fill(self, fill: FillEvent):
        pass