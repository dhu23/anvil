from mbte.event_processing import MbtePriorityQueue
import random

def _assert_pop(pq: MbtePriorityQueue):
    root = pq.peek() 
    if root is None:
        assert pq.pop() is None
    else:
        assert pq.pop() == root
    return root


def test_priority_queue():
    pq = MbtePriorityQueue()

    # nothing to pop when it is empty
    assert pq.peek() is None
    assert pq.pop() is None

    # add node
    pq.add(1, "value 1")
    assert pq.peek() == (1, "value 1")

    pq.add(0, "value 0")
    assert pq.peek() == (0, "value 0")

    pq.add(2, "value 2")
    assert pq.peek() == (0, "value 0")
    
    assert (0, "value 0") == _assert_pop(pq)
    assert (1, "value 1") == _assert_pop(pq)
    assert (2, "value 2") == _assert_pop(pq)
    

def test_priority_queue_random():
    for _ in range(5):
        _test_priority_queue_random(100)

    
def _test_priority_queue_random(total):
    nums = list(range(total))
    random.shuffle(nums)

    pq = MbtePriorityQueue()

    current_min = None
    for n in nums:
        current_min = n if current_min is None else min(n, current_min)
        pq.add(n, f'value {n}')

    for i in range(total):
        assert (i, f'value {i}') == _assert_pop(pq)
    
    assert pq.peek() is None