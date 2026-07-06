# Current Event and Speed Selection Logic

1. The script starts with a list of possible failure events.
   - Each event has an associated allowed-speed range.
   - Some events may have no explicit range and are treated as available at any speed.

2. When a failure is selected, the script first picks one event at random from the full event list.

3. It then defines a global valid speed window:
   - minimum speed: 5 kt
   - maximum speed: VR - 5 kt

4. For the chosen event, it calculates the overlap between:
   - the event's allowed-speed range, and
   - the global window of 5 to VR - 5.

5. If that overlap is valid, the script randomly picks a speed from that overlap.

6. If the overlap is not valid, the script falls back to a basic default speed.

## In summary

- choose an event randomly
- compute the allowed speed overlap for that event
- choose a speed randomly from that overlap (or use a fallback if needed)

# Weights & Bias

## Event Weighting

- The above will result in equal chance of any event occuring, this may not be the desired result as low speed (< 80 kts) events are simple to solve (stop).
- The weighting system introdcues a weight for the initial failure selection...
    - if allowed: { min: 0, max: 80 } then weight = 0.5 (reduce > 80 kt inhibited alerts)
    - if allowed: { min: 101, max: 125 } then weight = 1.5 (increase speed discrepancy issues)
    - else: weight = 1.0 (all other events have a standard weight)
- This means 0 - 80 kt inhibited failures will occur only ~ 1/3 of the time.

## Speed Bias

- Even with the Event Weighting, allowed: null events can occur at any speed and therefore we will see them often occuring below 80 kts which again is too simple to solve (stop).
- A Speed Bias is then introduced to tend to push the randomly selected speed higher.
- Speed bias currently set to 3.0

## event_distribution

- html script that allows you to tweak the weigth and bias and see the results.
- Current best settings give a good mix, more high speed anb ambiguous events (speed discrepancy, observe high EGT after inhibit) etc...
    - 0-80 weight = 0.5
    - 101-125 weight = 1.1
    - speed bias = 3.0