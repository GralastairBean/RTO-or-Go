# Current Event and Speed Selection Logic

This document describes the logic currently used by the script.

## Current behavior

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
