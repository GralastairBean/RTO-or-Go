# RTO or Go (Takeoff Decision Simulator)

## Overview

## How to Use
- You must press Go or STOP
- If you don't press GO the aircraft will not rotate... you have to make a decision!

## How it Works
- Randomly generates v-speeds
- Randomly chooses a failure
- Checks allowed speed for this failure
- Chooses a speed between the allowed values for that failure as well as a global rule of 5 kt - VR-5 kt

### v-speed generation
v1 is randomly generated between 135 and 160 (to be confirmed)
`v1 = rnd(135, 160);`
vr is then generatede based off the v1 (as it cannot be lower)
`vr = rnd(v1 + 5, 170);`
split (vr-v1) is calculated for display only

### Failures
- Lots of failures are inhibited above 80 kts which is quite slow and the general idea is that for any ECAM up to 80 kts you would stop. So there isn't a lot of value in adding the large number of total failures the vast majority of which are inhibited below 80. The real value is in those failures not inhibited and in non-ECAM events like noises, calls, over-temp/speed without ECAM at high speed.

### Takeoff Inhibit
- Vast majority inhibited > 80 kts.
- PWS inhibited > 100 kts.
- The simulator only generates events between 5 and VR-5 kts because you need to press GO to rotate.

## Supported Types
- Current implementation is 330 only
- Step 2 will be to add 350 which will be very similar.
- Need to seperate type specific from generic
- Later we can look at adding other types.

