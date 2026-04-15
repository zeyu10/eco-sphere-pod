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
from sensor_simulator import SensorSimulator
from ai_engine import (
    FishStressPredictor,
    FeedingOptimizer,
    PlantGrowthPredictor,
    EcosystemBalancer,
)

# =============================================
# ANSI color codes for terminal output
# =============================================
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"


def color_by_risk(risk_level):
    if risk_level in ("CRITICAL", "DANGER"):
        return RED
    elif risk_level in ("HIGH", "WARNING"):
        return YELLOW
    return GREEN


def print_header():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════╗
║          EcoSphere Pod — AI Ecosystem Intelligence              ║
║          Live Demo: Predictive Intelligence in Action           ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")


def print_phase(phase_num, title, description):
    print(f"""
{CYAN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase {phase_num}: {title}
  {description}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
""")


def print_sensor_line(data, fsi_result, eco_result):
    """Print one line of sensor data with AI analysis"""
    risk = fsi_result["risk_level"]
    color = color_by_risk(risk)
    eco_score = eco_result["ecosystem_score"]["overall"]
    eco_status = eco_result["status"]
    eco_color = color_by_risk(eco_status)
    
    print(
        f"{color}[{risk:>8}]{RESET} "
        f"Temp:{data['temperature']:5.1f}°C  "
        f"pH:{data['ph']:5.2f}  "
        f"DO:{data['do']:4.1f}  "
        f"NH3:{data['nh3']:5.3f}  "
        f"Turb:{data['turbidity']:5.1f}  "
        f"{DIM}│{RESET} "
        f"FSI:{color}{BOLD}{fsi_result['fsi_score']:5.1f}{RESET}  "
        f"Eco:{eco_color}{BOLD}{eco_score:5.1f}{RESET}"
    )


def print_alert(message):
    print(f"\n{RED}{BOLD}  ⚠  ALERT: {message}{RESET}\n")


def print_action(commands):
    """Print AI-generated control commands"""
    for actuator, cmd in commands.items():
        if cmd["action"] not in ("NORMAL", "MAINTAIN"):
            action_color = RED if "PAUSE" in cmd["action"] or "MAX" in cmd["action"] else YELLOW
            print(f"  {action_color}→ {actuator.upper()}: {cmd['action']}{RESET} — {cmd['reason']}")


def print_feeding_result(result):
    """Print feeding optimization result"""
    if result["action"] == "FEED":
        print(f"  {GREEN}→ FEED: {result['amount_grams']}g (servo: {result['servo_angle']}°){RESET}")
        print(f"    {DIM}{result['reason']}{RESET}")
    else:
        print(f"  {YELLOW}→ FEED DELAYED: {result['reason']}{RESET}")


def print_post_feed_eval(eval_result):
    """Print post-feeding evaluation"""
    eff = eval_result["efficiency"]
    color = GREEN if eff == "OPTIMAL" else YELLOW if "UNDER" in eff else RED
    print(f"\n  {BOLD}Post-Feeding Evaluation:{RESET}")
    print(f"  {color}→ Efficiency: {eff}{RESET}")
    print(f"    ΔNH3: +{eval_result['delta_nh3']:.4f} ppm")
    print(f"    Adjustment: {eval_result['adjustment_applied']:+.0%} → next feed factor: {eval_result['new_adjustment_factor']:.3f}")


def print_ecosystem_summary(eco_result):
    """Print ecosystem balance summary"""
    scores = eco_result["ecosystem_score"]
    status_color = color_by_risk(eco_result["status"])
    
    print(f"\n  {BOLD}Ecosystem Balance:{RESET}")
    print(f"  {status_color}Overall: {scores['overall']:.1f}/100 [{eco_result['status']}]{RESET}")
    print(f"    Water: {scores['water_quality']:.1f}  Fish: {scores['fish_health']:.1f}  Plant: {scores['plant_health']:.1f}")
    
    nf = eco_result["nutrient_flow"]
    direction = "↑ accumulating" if nf["net_accumulation_mg"] > 0 else "↓ deficit" if nf["net_accumulation_mg"] < 0 else "= balanced"
    print(f"    Nutrient flow: {nf['net_accumulation_mg']:+.3f} mg/day ({direction})")
    
    if eco_result["overrides"]:
        for override in eco_result["overrides"]:
            print(f"  {YELLOW}⚡ {override}{RESET}")


# =============================================
# Main Demo Flow
# =============================================
def run_demo():
    print_header()
    
    # Initialize all AI modules
    simulator = SensorSimulator(fish_species="tilapia")
    fsp = FishStressPredictor("tilapia")
    feeder = FeedingOptimizer(base_feed_grams=15.0, reference_temp=25.0)
    plant = PlantGrowthPredictor("lettuce")
    balancer = EcosystemBalancer()
    
    # Simulate some initial plant growth
    plant_result = plant.simulate_daily_growth(nitrate_ppm=45, light_hours=14, water_temp=25)
    
    try:
        # ==========================================
        # PHASE 1: Normal Operation (30 ticks)
        # ==========================================
        print_phase(1, "Normal Operation",
                    "System running healthy. All parameters within safe range.")
        
        print(f"{'':>10} {'Temp':>7} {'pH':>7} {'DO':>5} {'NH3':>7} {'Turb':>6}  {'':>1} {'FSI':>5} {'Eco':>5}")
        print(f"{'─' * 78}")
        
        for i in range(30):
            data = simulator.generate()
            history = simulator.get_history()
            
            fsi = fsp.analyze(data, history)
            nutrient_flow = balancer.calculate_nutrient_flow(
                daily_feed_grams=15.0, water_temp=data["temperature"],
                plant_growth_rate=plant_result["daily_growth_rate"]
            )
            eco = balancer.optimize(fsi, None, plant_result, nutrient_flow, data)
            
            print_sensor_line(data, fsi, eco)
            time.sleep(0.25)
        
        # ==========================================
        # PHASE 2: Feeding Event
        # ==========================================
        print_phase(2, "Smart Feeding Event",
                    "AI calculates optimal feed amount using Q10 metabolic scaling.")
        
        # Calculate feed amount
        latest = simulator.generate()
        feed_decision = feeder.calculate_feed_amount(
            current_temp=latest["temperature"],
            current_nh3=latest["nh3"],
            current_do=latest["do"]
        )
        print(f"\n  {BOLD}Feeding Decision:{RESET}")
        print_feeding_result(feed_decision)
        
        if feed_decision["action"] == "FEED":
            simulator.trigger_feeding(amount_grams=feed_decision["amount_grams"])
            pre_feed_nh3 = latest["nh3"]
        
        print(f"\n  {DIM}Monitoring post-feeding response...{RESET}\n")
        print(f"{'':>10} {'Temp':>7} {'pH':>7} {'DO':>5} {'NH3':>7} {'Turb':>6}  {'':>1} {'FSI':>5} {'Eco':>5}")
        print(f"{'─' * 78}")
        
        peak_nh3 = 0
        for i in range(40):
            data = simulator.generate()
            history = simulator.get_history()
            peak_nh3 = max(peak_nh3, data["nh3"])
            
            fsi = fsp.analyze(data, history)
            nutrient_flow = balancer.calculate_nutrient_flow(
                daily_feed_grams=feed_decision.get("amount_grams", 15),
                water_temp=data["temperature"],
                plant_growth_rate=plant_result["daily_growth_rate"]
            )
            eco = balancer.optimize(fsi, feed_decision, plant_result, nutrient_flow, data)
            
            print_sensor_line(data, fsi, eco)
            time.sleep(0.2)
        
        # Post-feeding evaluation
        if feed_decision["action"] == "FEED":
            eval_result = feeder.evaluate_post_feeding(pre_feed_nh3, peak_nh3, feed_decision["amount_grams"])
            print_post_feed_eval(eval_result)
        
        time.sleep(1)
        
        # ==========================================
        # PHASE 3: Crisis — Biofilter Failure
        # ==========================================
        print_phase(3, "CRISIS: Biofilter Failure Simulation",
                    "Ammonia rising, DO dropping. Watch the AI detect and respond.")
        
        simulator.trigger_crisis()
        
        print(f"{'':>10} {'Temp':>7} {'pH':>7} {'DO':>5} {'NH3':>7} {'Turb':>6}  {'':>1} {'FSI':>5} {'Eco':>5}")
        print(f"{'─' * 78}")
        
        last_alert_fsi = 0
        for i in range(80):
            data = simulator.generate()
            history = simulator.get_history()
            
            fsi = fsp.analyze(data, history)
            nutrient_flow = balancer.calculate_nutrient_flow(
                daily_feed_grams=15, water_temp=data["temperature"],
                plant_growth_rate=plant_result["daily_growth_rate"]
            )
            eco = balancer.optimize(fsi, None, plant_result, nutrient_flow, data)
            
            print_sensor_line(data, fsi, eco)
            
            # Print alerts at key thresholds
            if fsi["fsi_score"] >= 40 and last_alert_fsi < 40:
                print_alert(f"Fish Stress Index rising! FSI={fsi['fsi_score']:.0f} — {fsi['dominant_risk_factor']} trending dangerous")
                if fsi["predicted_danger_hours"] is not None:
                    print(f"  {YELLOW}⏱  Predicted danger in {fsi['predicted_danger_hours']:.1f} hours{RESET}")
            
            if fsi["fsi_score"] >= 60 and last_alert_fsi < 60:
                print_alert(f"HIGH RISK! FSI={fsi['fsi_score']:.0f}")
                print(f"  {BOLD}AI Ecosystem Balancer activating coordinated response:{RESET}")
                print_action(eco["coordinated_commands"])
            
            if fsi["fsi_score"] >= 80 and last_alert_fsi < 80:
                print_alert(f"CRITICAL! FSI={fsi['fsi_score']:.0f} — Emergency override!")
                print(f"  {RED}{BOLD}AI overriding all actuators:{RESET}")
                print_action(eco["coordinated_commands"])
                print_ecosystem_summary(eco)
            
            last_alert_fsi = fsi["fsi_score"]
            time.sleep(0.25)
        
        # Final summary
        print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════╗
║                      Demo Complete                              ║
╠══════════════════════════════════════════════════════════════════╣
║  ✓ Fish Stress Prediction: Z-score multi-parameter analysis     ║
║  ✓ Smart Feeding: Q10 metabolic scaling + closed-loop learning  ║
║  ✓ Ecosystem Balancer: Coordinated actuator control             ║
║  ✓ Predictive Warning: Detected crisis BEFORE critical levels   ║
║                                                                  ║
║  "We don't wait for the fish to get sick —                      ║
║   we predict it hours before it happens."                       ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    except KeyboardInterrupt:
        print(f"\n\n{DIM}Demo stopped.{RESET}")


if __name__ == "__main__":
    run_demo()
