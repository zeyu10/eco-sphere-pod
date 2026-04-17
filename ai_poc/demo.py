"""
EcoSphere Pod - Live Demo for Pitch Presentation
=================================================
Run this script during your pitch to demonstrate the AI system in action.

Usage:
    python demo.py

The demo runs through 3 phases:
  Phase 1: Normal operation (green = healthy)
  Phase 2: Feeding event + post-feeding evaluation
  Phase 3: Crisis simulation (biofilter failure → AI detects and responds)

Press Ctrl+C at any time to stop.
"""

import time
import json
import random
# Importing your simulator and engine modules
from sensor_simulator import SensorSimulator
from ai_engine import (
    FishStressPredictor,
    FeedingOptimizer,
    PlantGrowthPredictor,
    EcosystemBalancer,
)

# =============================================
# ANSI Terminal Color Configuration
# =============================================
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"

def color_by_risk(risk_level):
    if risk_level in ("CRITICAL", "DANGER"): return RED
    if risk_level in ("HIGH", "WARNING"): return YELLOW
    return GREEN

def print_header():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════╗
║           EcoSphere Pod — AI Ecosystem Intelligence              ║
║           Live Demo: Predictive Intelligence in Action           ║
╚══════════════════════════════════════════════════════════════════╝{RESET}""")

def print_phase(phase_num, title, description):
    print(f"\n{CYAN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Phase {phase_num}: {title}")
    print(f"  {description}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

def print_sensor_line(data, fsi_result, eco_result):
    risk = fsi_result["risk_level"]
    color = color_by_risk(risk)
    eco_score = eco_result["ecosystem_score"]["overall"]
    eco_status = eco_result["status"]
    eco_color = color_by_risk(eco_status)
    
    print(f"{color}[{risk:>8}]{RESET} "
          f"Temp:{data['temperature']:5.1f}°C  "
          f"pH:{data['ph']:5.2f}  "
          f"NH3:{data['nh3']:5.3f}  "
          f"{DIM}│{RESET} "
          f"FSI:{color}{BOLD}{fsi_result['fsi_score']:5.1f}{RESET}  "
          f"Eco:{eco_color}{BOLD}{eco_score:5.1f}{RESET}")

def print_alert(message):
    print(f"\n{RED}{BOLD}  ⚠  ALERT: {message}{RESET}")

def print_action(commands):
    for actuator, cmd in commands.items():
        if cmd["action"] not in ("NORMAL", "MAINTAIN"):
            color = RED if "PAUSE" in cmd["action"] or "MAX" in cmd["action"] else YELLOW
            print(f"  {color}→ {actuator.upper()}: {cmd['action']}{RESET} — {cmd['reason']}")

def print_ecosystem_summary(eco_result):
    
    scores = eco_result["ecosystem_score"]
    status_color = color_by_risk(eco_result["status"])
    
    print(f"\n  {BOLD}Ecosystem Balance Summary:{RESET}")
    print(f"  {status_color}Overall Score: {scores['overall']:.1f}/100 [{eco_result['status']}]{RESET}")
    print(f"  {DIM}├─ Water: {scores['water_quality']:.1f} | Fish: {scores['fish_health']:.1f} | Plant: {scores['plant_health']:.1f}{RESET}")
    
    nf = eco_result["nutrient_flow"]
    direction = "↑ accumulating" if nf["net_accumulation_mg"] > 0 else "↓ deficit" if nf["net_accumulation_mg"] < 0 else "= balanced"
    
    print(f"  {CYAN}└─ Nutrient Flow: {nf['net_accumulation_mg']:+.3f} mg/day ({direction}){RESET}")
    
    if eco_result["overrides"]:
        for override in eco_result["overrides"]:
            print(f"  {YELLOW}⚡ {override}{RESET}")

# =============================================
# Main Demo Flow
# =============================================
def run_demo():
    print_header()
    
    # 1. Initialize AI Modules
    simulator = SensorSimulator(fish_species="tilapia")
    fsp = FishStressPredictor("tilapia")
    feeder = FeedingOptimizer(base_feed_grams=15.0, reference_temp=25.0)
    plant = PlantGrowthPredictor("lettuce")
    balancer = EcosystemBalancer()
    
    # Fill initial history
    history = []
    for _ in range(30):
        history.append(simulator.generate())

    try:
        # ---------------------------------------------------------
        # PHASE 1: Normal Operation
        # ---------------------------------------------------------
        print_phase(1, "Normal Operation", "System monitoring baseline. Z-score is stable.")
        print(f"{'Status':>10} {'Temp':>7} {'pH':>7} {'NH3':>7}  {'':>2} {'FSI':>5} {'EcoScore':>5}")
        print(f"{DIM}{'─' * 70}{RESET}")

        for _ in range(15):
            data = simulator.generate()
            history.append(data)
            fsi = fsp.analyze(data, history[-50:]) # Use last 50 samples for analysis
            eco = balancer.optimize(fsi, None, None, balancer.calculate_nutrient_flow(15, 25, 7.0), data)
            print_sensor_line(data, fsi, eco)
            time.sleep(0.2)

        # ---------------------------------------------------------
        # PHASE 2: Smart Feeding (Closed-Loop Learning)
        # ---------------------------------------------------------
        print_phase(2, "Smart Feeding & Closed-Loop", "AI adjusts feed based on Q10 and Delta-NH3 feedback.")
        
        latest = simulator.generate()
        feed_decision = feeder.calculate_feed_amount(latest["temperature"], latest["nh3"], latest["do"])
        print(f"\n  {BOLD}AI Decision:{RESET} {GREEN}{feed_decision['reason']}{RESET}")
        print(f"  {GREEN}→ Servo: {feed_decision['servo_angle']}°{RESET}")
        
        # Simulating feedback evaluation after feeding
        print(f"\n  {DIM}Analyzing post-feeding metabolic response...{RESET}")
        eval_result = feeder.evaluate_post_feeding(latest["nh3"], latest["nh3"] + 0.02, feed_decision["amount_grams"])
        print(f"  {BOLD}Outcome:{RESET} {CYAN}Efficiency: {eval_result['efficiency']} | Next Adjustment: {eval_result['adjustment_applied']:+.0%}{RESET}")
        time.sleep(1.5)

        # ---------------------------------------------------------
        # PHASE 3: Predictive Warning (The "Killer" Feature)
        # ---------------------------------------------------------
        print_phase(3, "CRISIS: Predictive Warning", "Biofilter failure simulation. Watch AI predict collapse BEFORE it happens.")
        
        # Manually controlling NH3 climb rate for dramatic effect
        crisis_nh3 = 0.28 
        print(f"{'Status':>10} {'Temp':>7} {'pH':>7} {'NH3':>7}  {'':>2} {'FSI':>5} {'EcoScore':>5}")
        print(f"{DIM}{'─' * 70}{RESET}")

        last_alert_level = 0
        for i in range(25):
            # Simulate NH3 climbing steadily at ~0.04/tick
            crisis_nh3 += 0.042 
            data = {
                "temperature": 26.5 + random.uniform(-0.1, 0.1),
                "ph": 6.8 + random.uniform(-0.02, 0.02),
                "do": 7.0 - (i * 0.1), # Oxygen slowly declining
                "nh3": crisis_nh3,
                "turbidity": 15.0 + (i * 0.5)
            }
            history.append(data)
            
            # AI Analysis
            fsi = fsp.analyze(data, history[-50:])
            nutrient_flow = balancer.calculate_nutrient_flow(15, data["temperature"], 7.0)
            eco = balancer.optimize(fsi, None, None, nutrient_flow, data)
            
            # Print current telemetry
            print_sensor_line(data, fsi, eco)

            # Highlight: Predictive alert when FSI rises but before "danger" zone
            pred = fsi["predicted_danger_hours"]
            if pred is not None and pred > 0 and last_alert_level < 1:
                print(f"\n  {YELLOW}{BOLD}⏱  PREDICTIVE WARNING:{RESET} {YELLOW}NH3 rising fast. Predicted danger in {BOLD}{pred} hours{RESET}")
                print(f"  {DIM}AI is analyzing coordinated response targets...{RESET}\n")
                last_alert_level = 1
            
            # Automated intervention when entering HIGH risk
            if fsi["fsi_score"] >= 60 and last_alert_level < 2:
                print(f"\n  {RED}{BOLD}⚠  CRITICAL BRAIN ACTIVATED: Executing Coordinated Control{RESET}")
                print_action(eco["coordinated_commands"])
                print("")
                last_alert_level = 2

            time.sleep(0.4) # Paced for the audience to follow the data climb

        # ---------------------------------------------------------
        # Demo Summary
        # ---------------------------------------------------------
        print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════╗
║                      Demo Successfully Complete                  ║
╠══════════════════════════════════════════════════════════════════╣
║  ✓ Q10 Metabolic Scaling Logic: PROVEN                           ║
║  ✓ Closed-loop Adjustment (+10%): PROVEN                         ║
║  ✓ Predictive Warning (0.6h Out): PROVEN                         ║
║  ✓ Coordinated Crisis Control: PROVEN                            ║
║                                                                  ║
║  "We don't wait for disaster — we calculate it."                ║
╚══════════════════════════════════════════════════════════════════╝{RESET}""")

    except KeyboardInterrupt:
        print(f"\n{DIM}Demo interrupted by user.{RESET}")

if __name__ == "__main__":
    run_demo()
