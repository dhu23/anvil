# Anvil (MBTE)
Minimal Back-Testing Engine

## Core Concepts

### Price Series
- time
- price (or OHLC)
- optional volume

### Signal
- function of past prices only
- outputs desired position (e.g. -1, 0, +1)

### Execution Model
- lag (signal at t executes at t+1)
- transaction costs
- slippage (fixed or proportional)

### Portfolio Accounting
- positoins
- cash
- P&L
- returns

### Metrics
- cumulative return
- drawdown
- Sharpe (simple)
- turnover


## Absolute Must-have Constraints

### Zero-signal test
- signal = 0 alaways gives PnL=0, costs=0, Sharpe=0
- otherwise it is a failure

### Random-signal test
- signal in {-1, +1} set randomly, expects negative PnL after costs, and Sharpe is around 0 or < 0
- if it makes money it is a bug

### Known-failure test
- moving average crossover on pure random walk, should not produce persistent alpha
- otherwise it is a bug or leakage


## Things to avoid
### Over-engineering too early 
- engines
- abstractions
- frameworks

### Jumping to Production realism
- order book simulation
- queue position modeling
- latency modeling


## Architectural Design

The system revolves around event processing. There are components that produce
and consume events. There is exactly one event stream/queue. Market data, clock
ticks and execution outcomes are all events. 

### Who "owns" time?
Time is subtle. 

There are three distinct responsibilities that often get conflated:
- Who decides what the next timestamp is?
- Who enforces event ordering by time?
- Who exposes "current time" to the system?

The answers are:
- The event queue owns time ordering.
- The clock owns current time.
- Event producers propose timestamps. 


### Design consequence
- Clock is global, mutable state. It is a consumer, not a driver
- Portfolio state is mutable
- Strategy state may be mutable
- Keeping all consumers in a single thread
- The queue is not FIFO, it is a priority queue by timestamp
 

### Who schedules "market close"? 
A: The market data event store schedules it. 

### What happens when the queue is empty?
A: If the event queue is empty, ask external data producers (time+market) for
the enxt event.
 

### Diagram
MarketEventSource   ─┐
                     │
ExecutionSimulator  ─┼─> EventQueue -> Engine -> Components
                     │
Strategy / Portfolio ┘
