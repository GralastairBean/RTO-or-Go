# RTO or GO? Project Reference

## Overview

This project is a takeoff decision simulator that models an Airbus-style reject-takeoff (RTO) vs. continue-takeoff decision.

The simulator includes both browser-based and terminal-based versions:
- `scripts/browser_v2.html` — main browser simulator with graphical speed tape, event log, audio, controls, and results summary.
- `scripts/terminal_v2.py.py` — terminal simulator with ASCII speed tape, ECAM alerts, keyboard input, and console summary.
- `scripts/browser_v1.html` and `scripts/terminal_v1.py` — earlier/simpler versions of the same idea.

## Purpose

The simulation tests the decision logic around:
- stopping if a failure occurs before `V1`
- continuing takeoff if already past `V1`
- automatic rotation if no decision happens before `VR`

It simulates realistic V-speed generation, callouts, ECAM alerts, and outcome classification.

## Core Algorithm

### 1. Generate V-speeds

- `V1` is randomly generated between `135` and `160` knots.
- `VR` is `V1 + split`, where `split` is randomly `5` to `12` knots.
- `maxSpeed` is set to `VR + 20` for display range.

### 2. Choose a failure event

- A `failureSpeed` is randomly selected between `5` knots and `VR`.
- A failure event is chosen from a list of alerts, each with metadata such as:
  - `text`
  - `inhibited` status
  - `type` (`red`, `amber`, `crew`, `other`)
- Event eligibility depends on speed:
  - `< 80 KT` allows all events.
  - `80–99 KT` excludes inhibited amber events.
  - `>= 100 KT` allows only non-inhibited critical events.

### 3. Simulate speed buildup

- Speed increases over time using a physics-inspired model:
  - initial low-speed thrust ramp-up
  - drag proportional to `speed^2`
  - acceleration = thrust − drag
- In browser: uses `requestAnimationFrame()`.
- In terminal: uses timed loops and `sleep()`.

### 4. Trigger events and callouts

- When `speed >= failureSpeed`, the selected event triggers exactly once.
- When `speed >= 100 KT`, a `"100 KTS"` callout logs.
- When `speed >= V1`, a `"VEE ONE"` callout logs (browser version).
- If `GO` is selected and `speed >= VR`, rotation is handled.

### 5. Accept decision input

- The user can choose:
  - `STOP` (`s` key/button)
  - `GO` (`g` key/button)
- `speedAtDecision` and `timeOfDecision` are recorded.

### 6. Resolve outcome

- `STOP` causes deceleration until speed reaches zero.
- If stop decision occurs before or at `V1`, the user may choose whether to vacate the runway.
- `GO` continues acceleration and leads to takeoff if `VR` is reached.
- If no decision occurs before `VR`, the browser version auto-rotates.

## Outcome Classification

Result values include:
- `SUCCESSFUL RTO`
- `OVERRUN (RTO > V1)`
- `TAKEOFF`
- `TAKEOFF (LATE ROTATION)`
- `OVERRUN (NO ROTATE)`

The summary includes:
- V1 and VR speeds
- failure event description
- speed at failure
- speed at decision
- reaction time
- runway vacated status
- result classification

## Key Files

- `scripts/browser_v2.html`
  - full graphical simulation UI
  - event log
  - speed tape rendering
  - failure event selection and simulation loop
  - button and keyboard controls
  - summary display
- `scripts/terminal_v2.py.py`
  - console simulation
  - ASCII speed tape
  - keyboard polling
  - ECAM-style alert display
- `scripts/browser_v1.html` and `scripts/terminal_v1.py`
  - earlier simulator versions

## Notes for Next Agent

- Treat this as a training/demo simulation, not real avionics logic.
- Key state variables are:
  - `speed`
  - `v1`, `vr`, `maxSpeed`
  - `failureSpeed`, `failureAlert`
  - `choice`, `phase`, `failureTriggered`
- The control flow is:
  1. initialize run state
  2. simulate speed roll
  3. trigger any event
  4. accept pilot decision
  5. transition to stop/go phase
  6. present final summary

## Running the Project

- Browser version: open `scripts/browser_v2.html` in a browser or serve the workspace via HTTP.
- Terminal version: run `python scripts/terminal_v2.py.py`.
