INHIBITED (only allowed < 100 kts)





UNINHIBITED (allowed any speed)




paste in below
        const failureEvents = [
            // ENG
            { text: "ENG 1 FIRE", inhibited: false, type: 'red' },
            { text: "ENG 2 FIRE", inhibited: false, type: 'red' },
            { text: "ENG 1 FAIL", inhibited: false, type: 'amber' },
            { text: "ENG 2 FAIL", inhibited: false, type: 'amber' },
            { text: "ENG 1 OIL PR LO", inhibited: false, type: 'amber' },
            { text: "ENG 2 OIL PR LO", inhibited: false, type: 'amber' },
            { text: "ENG 1 EGT OVERLIMIT", inhibited: true, type: 'amber' },
            { text: "ENG 2 EPR MODE FAULT", inhibited: true, type: 'amber' },
            { text: "ENG 1 N1 OVERLIMIT", inhibited: true, type: 'amber' },
            { text: "ENG 2 OIL HI TEMP", inhibited: true, type: 'amber' },
            { text: "ENG 1 REV UNLOCKED", inhibited: true, type: 'amber' },
            { text: "ENG 2 STALL", inhibited: true, type: 'amber' },
            { text: "ENG THRUST LOSS", inhibited: true, type: 'amber' },

            // SMOKE
            { text: "SMOKE FWD CARGO", inhibited: false, type: 'red' },

            // AIR
            { text: "AIR PACK 1 FAULT", inhibited: true, type: 'amber' },

            // HYD
            { text: "HYD Y SYS LO PR", inhibited: true, type: 'amber' },
            { text: "HYD B SYS LO PR", inhibited: true, type: 'amber' },
            { text: "HYD G SYS LO PR", inhibited: true, type: 'amber' },

            // F/CTL
            { text: "F/CTL PRIM 1 FAULT", inhibited: true, type: 'amber' },
            { text: "F/CTL L INR AIL FAULT", inhibited: true, type: 'amber' },
            { text: "F/CTL SEC 1 FAULT", inhibited: true, type: 'amber' },
            { text: "F/CTL SEC 2 FAULT", inhibited: true, type: 'amber' },

            // FUEL
            { text: "FUEL PUMP 2 LO PRESS", inhibited: true, type: 'amber' },

            // CREW OBSERVATION
            { text: "EGT OVERLIMIT (NO ECAM)", inhibited: false, type: 'crew' },
            { text: "N1 OVERSPEED (NO ECAM)", inhibited: false, type: 'crew' },
            { text: "LOUD BANG", inhibited: false, type: 'crew' },
            { text: "negative speed trend", inhibited: 'false', type: 'crew' },

            // WINDSHEAR
            { text: '"WINDSHEAR AHEAD"', inhibited: 'windshear', type: 'other' },
            { text: '"MONITOR RADAR DISPLAY"', inhibited: 'windshear', type: 'other' },

            // ATC
            { text: 'ATC: "STOP STOP STOP"', inhibited: false, type: 'other' },
        ];
