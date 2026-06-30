import time
import random
import sys
import os

# ANSI Color Codes for Terminal Background Boxes
RED_BOX = "\033[41m\033[37m\033[1m"
AMBER_BOX = "\033[48;5;208m\033[37m\033[1m"
RESET = "\033[0m"

# Alert lists
# Uninhibited: all RED, can occur at any speed
uninhibited = [
    "ENG 1 FIRE",
    "ENG 2 FIRE",
    "ENG 1 FAIL",
    "ENG 2 FAIL",
    "ENG 1 OIL PR LO",
    "ENG 2 OIL PR LO",
    'ATC CALL: "CX123 STOP!"',
    "SMOKE FWD CARGO",
    "CREW OBSERVE EGT OVERLIMIT (NO ECAM)",
    "CREW OBSERVE N1 OVERSPEED (NO ECAM)",
    "CREW HEAR LOUD BANG", # may be stall or tire burst
]

# Inhibited: all AMBER, only occur below 100 KT
inhibited = [
    # AIR
    "AIR PACK 1 FAULT",
    # ENG
    "ENG 1 EGT OVERLIMIT",
    "ENG 2 EPR MODE FAULT",
    "ENG 1 N1 OVERLIMIT",
    "ENG 2 OIL HI TEMP",
    "ENG 1 REV UNLOCKED",
    "ENG 2 STALL",
    "ENG THRUST LOSS",
    # HYD
    "HYD Y SYS LO PR",
    "HYD B SYS LO PR",
    "HYD G SYS LO PR",
    # FUEL
    "FUEL PUMP 2 LO PRESS",
    # F/CTL
    "F/CTL L INR AILERON FAULT",
    "F/CTL SEC 1 FAULT",
    "F/CTL SEC 2 FAULT",
    "F/CTL PRIM 1 FAULT",
    # MISC
    '"WINDSHEAR AHEAD"',
    '"MONITOR RADAR DISPLAY"',
]

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def render_speed_tape(current_speed, v1_speed, vr_speed, max_speed):
    min_display_speed = 30.0
    tape_length = 60 
    speed_range = max_speed - min_display_speed
    
    pct = min(max((current_speed - min_display_speed) / speed_range, 0.0), 1.0)
    pointer_pos = int(pct * (tape_length - 1))
    
    v1_pct = min(max((v1_speed - min_display_speed) / speed_range, 0.0), 1.0)
    vr_pct = min(max((vr_speed - min_display_speed) / speed_range, 0.0), 1.0)
    
    v1_pos = int(v1_pct * (tape_length - 1))
    vr_pos = int(vr_pct * (tape_length - 1))
    
    tape_list = ["-"] * tape_length
    tape_list[v1_pos:v1_pos+2] = ["V", "1"]
    tape_list[vr_pos:vr_pos+2] = ["V", "R"]
    tape_list[pointer_pos] = "^"
    
    tape_line = "".join(tape_list)
    return f"[{tape_line}]  (Speed: {int(current_speed)} KT)"

def run_simulation():
    clear_screen()

    v1_speed = random.randint(135, 160)
    v1_vr_split = random.randint(5, 12)
    vr_speed = v1_speed + v1_vr_split
    max_speed = vr_speed + 20  

    print("="*50)
    print("A350/A330 TAKEOFF DECISION SIMULATOR")
    print(f"TAKEOFF TARGETS:    V1={v1_speed} KT, VR={vr_speed} KT (Split: {v1_vr_split} KT)")
    print("INSTRUCTIONS:       Decide to STOP [s] or GO [g] at any time.")
    print("="*50)
    input("\n[Press ENTER to Takeoff...]\n")

    speed = 0.0
    failure_triggered = False
    choice = None
    speed_at_failure = None
    speed_at_decision = None
    time_of_failure = None
    time_of_decision = None
    auto_rotated = False
    runway_vacated_status = "N/A"
    hundred_kts_called = False
    
    active_ecam_string = ""
    active_crew_call = ""
    active_callout = ""
    
    # Failure can occur at any speed above 5 KT, up to VR (always a failure)
    failure_speed = random.randint(5, vr_speed)
    
    # Select the alert and its colour based on speed band
    if failure_speed < 100:
        # below 100 KT: any alert from either list, all equally likely
        chosen_alert = random.choice(uninhibited + inhibited)
        alert_is_red = chosen_alert in uninhibited
    else:
        # at/above 100 KT: only uninhibited (red) alerts
        chosen_alert = random.choice(uninhibited)
        alert_is_red = True
    
    tick_rate = 0.1 
    
    # Takeoff roll block
    while speed < vr_speed:
        if speed < 30:
            thrust_factor = 0.4 + (speed / 30.0) * 0.6
        else:
            thrust_factor = 1.0
            
        base_thrust = 1.25 * thrust_factor
        drag = 0.000025 * (speed ** 2)
        acceleration = base_thrust - drag
        speed += acceleration
        
        # 100 KTS callout
        if speed >= 100 and not hundred_kts_called:
            hundred_kts_called = True
            active_callout = '\n\n"100 KTS"'
        
        if speed >= failure_speed and not failure_triggered:
            failure_triggered = True
            speed_at_failure = int(speed)
            time_of_failure = time.time()
            
            alert_text = f" {chosen_alert} "
            box_color = RED_BOX if alert_is_red else AMBER_BOX
            active_ecam_string = f"\n\n{box_color}{alert_text}{RESET}"

        # Clean frame layout configuration
        clear_screen()
        tape_output = render_speed_tape(speed, v1_speed, vr_speed, max_speed)
        print(f"{tape_output}{active_callout}{active_ecam_string}{active_crew_call}", flush=True)
        
        start_time = time.time()
        while time.time() - start_time < tick_rate:
            if choice is None:
                if os.name == 'nt': 
                    import msvcrt
                    if msvcrt.kbhit():
                        char = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                        if char in ['s', 'g']:
                            choice = char
                            time_of_decision = time.time()
                            speed_at_decision = int(speed)
                else: 
                    import select
                    rlist, _, _ = select.select([sys.stdin], [], [], 0.02)
                    if rlist:
                        char = sys.stdin.read(1).lower()
                        if char in ['s', 'g']:
                            choice = char
                            time_of_decision = time.time()
                            speed_at_decision = int(speed)

        # Handle post-decision rolling animation dynamically without hard cuts
        if choice == 's':
            active_crew_call = '\n\n"STOP"'
            while speed > 0:
                deceleration = random.uniform(2.5, 4.0)
                speed -= deceleration
                if speed < 0:
                    speed = 0
                clear_screen()
                tape_output = render_speed_tape(speed, v1_speed, vr_speed, max_speed)
                print(f"{tape_output}{active_callout}{active_ecam_string}{active_crew_call}", flush=True)
                time.sleep(0.05)
            break
            
        elif choice == 'g':
            active_crew_call = '\n\n"GO"'
            while speed < vr_speed:
                drag = 0.000025 * (speed ** 2)
                acceleration = 1.25 - drag
                speed += acceleration
                clear_screen()
                tape_output = render_speed_tape(speed, v1_speed, vr_speed, max_speed)
                print(f"{tape_output}{active_callout}{active_ecam_string}{active_crew_call}", flush=True)
                time.sleep(0.1)
            break

    # Handle automatic rotation if VR reached without input
    if choice is None:
        choice = 'g'
        auto_rotated = True
        clear_screen()
        tape_output = render_speed_tape(speed, v1_speed, vr_speed, max_speed)
        print(f"{tape_output}{active_callout}{active_ecam_string}", flush=True)
        print(f"\nROTATION: Aircraft reached VR ({vr_speed} KT) and rotated automatically.")

    # Intercept successful RTO before printing results box
    if choice == 's' and speed_at_decision <= v1_speed:
        print("\n")
        vacate_choice = ""
        while vacate_choice not in ['y', 'n']:
            vacate_choice = input("Do you want to vacate the runway? y/n: ").strip().lower()
        runway_vacated_status = "yes" if vacate_choice == 'y' else "no"

    print("\n" + "="*50)
    print(f"TAKEOFF TARGETS:    V1={v1_speed} KT, VR={vr_speed} KT")
    
    if failure_triggered:
        print(f"FAILURE:            {chosen_alert}")
        print(f"SPEED AT ECAM:      {speed_at_failure} KT")
    else:
        print(f"FAILURE:            NONE DETECTED")
        print(f"SPEED AT ECAM:      N/A")
        
    if failure_triggered and time_of_decision is not None:
        reaction_time_val = f"{time_of_decision - time_of_failure:.2f} seconds"
    else:
        reaction_time_val = "N/A"
        
    if choice == 's':
        if speed_at_decision > v1_speed:
            result_text = "OVERRUN (RTO>V1)"
        else:
            result_text = "SUCCESSFUL RTO"
    else:
        result_text = "GO (Continued Takeoff)"
        
    if auto_rotated:
        print("SPEED AT DECISION:  N/A")
    else:
        print(f"SPEED AT DECISION:  {speed_at_decision} KT")
        
    print(f"REACTION TIME:      {reaction_time_val}")
    print(f"RUNWAY VACATED:     {runway_vacated_status}")
    print(f"RESULT:             {result_text}")
    print("="*50 + "\n")

    # 3-second delay before flashing custom restart prompt
    time.sleep(0.5)
    input("[Press ENTER to restart...]")

if __name__ == "__main__":
    while True:
        run_simulation()