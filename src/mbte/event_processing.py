'''
Event Processing related implementations
'''

from abc import ABC, abstractmethod 
from mbte.clock import Clock
from mbte.events import Event, InternalSchedulingEvent
import heapq
from collections import namedtuple


class EventStore(ABC):
    '''
    EventStore that owns the generation and sequencing of events 
    that drive back-testing computation. 

    Such events are external events imposed on the system, including 
    clock/time advancing, market data events for example. Generated 
    order execution or signals are not part of the store's responsibility.
    We can track somewhere there but they are not replayed into the system.

    A subclass of EventStore should own the logic of generating 
    data events and be responsible of the right sequencing. It should be fully
    aware of the relevant time stamping for the strategy it targets.  
    '''
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def peek(self) -> Event | None:
        '''
        Docstring for peek
        
        :param self: Description
        :return: Description
        :rtype: Event | None
        '''
        pass

    @abstractmethod
    def pop(self) -> Event | None:
        '''
        Docstring for pop
        
        :param self: Description
        :return: Description
        :rtype: Event | None
        '''
        pass


class EventProcessor(ABC):
    @abstractmethod
    def process(event: Event):
        pass


class MbtePriorityQueue(object):
    '''
    Docstring for MbtePriorityQueue
    
    :var Illustration: Description
    :var Implementation: Description
    '''
    def __init__(self):
        self._queue = []

    def add(self, key, value):
        heapq.heappush(self._queue, (key, value))

    def pop(self):
        if self._queue:
            return heapq.heappop(self._queue)
        else:
            return None
        
    def peek(self):
        if self._queue:
            return self._queue[0]
        else:
            return None


EventStoreItem = namedtuple('EventStoreItem', ['event', 'event_store'])
ScheduledItem = namedtuple('ScheduleItem', ['event', 'schedule_id'])


class EventSequencerError(RuntimeError):
    pass


class EventSequencer(object):
    '''
    EventSequencer manages multiple EventStore objects and presents produced
    events in the system in a properly sorted way, by sequence number, 
    timestamp or anything that's comparable. 

    In addtion, EventSequencer also takes on the responsibility to manauge 
    ad-hoc scheduling events that out-of-order scneario can happen due to 
    strategy logic. 
    
    Illustration of Normal EventStore streams:
    For example, we can have two EventStore, one generates market data and
    one generates portfolio sell off event. The events are lazily proposed
    in the following sequence in a simulation run:
    Market Data: 
        MD-1: 2025-12-24 9:30AM  Market Open Price
        MD-2: 2025-12-24 1:30PM  Market Close Price
    Portfolio Event Data:
        P-1: 2025-12-24 9:35AM  Build Portfolio
        P-2: 2025-12-25 1:25PM  Liquidate Portfolio
    The EventQueue object is responsible for generate the following sequence 
        MD-1, P-1, P-2, MD-2 

    Illustration of ad-hoc scheduling:
    The strategy might want to schedule a trading event at 10:00AM after
    processing MD-1, however after P-1, it decides to add another scheduled
    event at 9:50AM. Due to the addition of the second event is out of order,
    allowing these events to go directly to participating the ordering of the
    EventSequencer internal priority queue can nicely resolve the issue without
    introducing any complexity.
    
    Implementation:
    It uses an algorithm that does a k-way merge of sorted data streams. 
    Each EventStore can lazily propose the next event to be inserted into a
    priority queue that  
    '''
    
    def __init__(
            self,
            sim_clock: Clock, 
            event_stores: list[EventStore], 
            event_processor: EventProcessor
    ):
        self._sim_clock = sim_clock
        self._event_stores = list(event_stores)
        self._event_processor = event_processor

        self._merger_queue = MbtePriorityQueue()
        self._internal_scheduling_id = 1
        self._scheduled_id_set = set()

        self._init_queue()

    def schedule(self) -> int:
        raise RuntimeError("not implemented")
    
    def cancel(self, schedule_id: int) -> bool:
        raise RuntimeError("not implemented")

    def run(self):
        # keep running event by event util it is done
        while self._run_once():
            pass

    def _init_queue(self):
        for event_store in self._event_stores:
            if not self._replenish_from_store(event_store):
                raise EventSequencerError(
                    f'no event in event store {event_store.name()}'
                )

    def _replenish_from_store(self, event_store: EventStore) -> bool:
        head = event_store.pop()
        if head is None:
            return False
        
        # put the next one from the event store into the merge queue
        self._merger_queue.add(
            head.timestamp, 
            EventStoreItem(event=head, event_store=event_store)
        )
        return True

    def _get_schedule_id(self):
        ret = self._internal_scheduling_id
        self._internal_scheduling_id += 1
        return ret
    
    def _schedule(self, event: InternalSchedulingEvent):
        self._merger_queue.add(
            event.timestamp,
            ScheduledItem(event=event, schedule_id=self._get_schedule_id())
        )

    def _run_once(self) -> bool:
        head = self._merger_queue.pop()
        if head is None:
            return False
        
        if isinstance(head, ScheduledItem):
            self._process_event(head.event)
            self._scheduled_id_set.remove(head.schedule_id)
        elif isinstance(head, EventStoreItem):
            self._process_event(head.event)
            self._replenish_from_store(head.event_store)               
        else:
            return False
        
    def _process_event(self, event: Event):
        if self._sim_clock.now() > event.timestamp:
            return 
        self._sim_clock.set_time(event.timestamp)
        self._event_processor.process(event)
        