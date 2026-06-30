# Failure Selection Plan

## Goal

Define a clear, data-driven failure selection model for the simulator.

The recommended approach is **event-first selection**, using event metadata to determine eligible speed bands.

---

## Current model

The code currently chooses a failure speed first, then filters candidate failures by the event `inhibited` metadata:
- `false` → allowed at any speed
- `true` → treated as inhibited above the high-speed cutoff
- `'windshear'` → treated as inhibited above 100 KT

This works, but it is effectively a speed-first model.

---

## Recommended event-first model

### Steps

1. Choose a failure event first.
2. Use the event's metadata to determine its allowed speed band.
3. Sample the failure speed from that band.
4. Apply any additional restrictions based on `VR` or other conditions.

### Benefits

- clearer semantics: event definitions determine where they can happen
- easier to add event-specific constraints
- better support for weighted event selection
- more natural for modeling specific failures like `negative speed trend`

---

## Event metadata design

### Minimal schema

Each event can include fields such as:
- `text` — alert text
- `inhibited` — eligibility rule key
- `type` — red/amber/crew/other
- optional: `minSpeed`, `maxSpeed`, `maxSpeedType`

### Example metadata

```js
{
  text: "EGT OVERLIMIT (NO ECAM)",
  inhibited: false,
  type: 'crew'
},
{
  text: "AIR PACK 1 FAULT",
  inhibited: 'below_100',
  type: 'amber'
},
{
  text: 'ATC: "STOP STOP STOP"',
  inhibited: false,
  type: 'other'
},
{
  text: 'negative speed trend',
  inhibited: 'neg_trend',
  type: 'crew'
}
```

### Expanded rule examples

- `false` → any speed
- `true` → limited by the current high-speed cutoff (e.g. only below 100 KT)
- `'windshear'` → allowed in the 0–100 KT band, with special semantics
- `'neg_trend'` → allowed from 60 KT up to VR
- `'pre_vr_only'` → allowed from 60 KT up to VR
- `'below_100'` → allowed from 0 KT up to 100 KT

---

## Practical implementation

### 1. Choose the event

Pick a failure event from the `failureEvents` list, optionally with weights.

### 2. Determine the allowed speed band

Map `event.inhibited` to speed constraints. For example:
- `false` → `[5, VR]`
- `true` → `[5, 100]`
- `'windshear'` → `[5, 100]`
- `'neg_trend'` → `[60, VR]`

### 3. Sample speed

Randomly select a failure speed from the event's allowed band.

### 4. Fallback handling

If the chosen event has no valid band for the current scenario, resample another event or choose a safe default.

---

## Why this is a better plan

This approach retains your existing inhibited metadata, but uses it as the primary rule source rather than as a filter after the speed decision.

It makes adding new event types much easier, because each event can define its own eligibility semantics.

It also better supports cases like `negative speed trend`, where the event should be limited to a specific speed band rather than simply "not allowed above some cutoff."