"""
EcoSphere Pod - Sensor Data Simulator
Generates realistic aquaponics sensor data with gradual crisis modeling.
Supports normal operation, feeding events, and progressive water quality degradation.
"""

import random
import time
import json
import math
from datetime import datetime

class SensorSimulator:
    """
    Simulates 6 sensor inputs for an EcoSphere Pod.
    Models realistic daily cycles, feeding impacts, and crisis scenarios.
    """
    
    def __init__(self, fish_species="tilapia", plant_species="lettuce"):
        self.fish_species = fish_species
        self.plant_species = plant_species
        self.tick = 0
        self.mode = "normal"  # normal, post_feeding, crisis
        self.crisis_severity = 0.0  # 0.0 to 1.0, gradually increases
        
        # Baseline parameters (species-specific)
        self.baselines = {
            "tilapia": {"temp": 26.0, "ph": 7.0, "do": 7.8, "nh3": 0.2, "turbidity": 15.0},
            "goldfish": {"temp": 22.0, "ph": 7.2, "do": 8.0, "nh3": 0.15, "turbidity": 12.0},
        }
        self.base = self.baselines.get(fish_species, self.baselines["tilapia"])
        
        # Historical data buffer (stores last N readings for trend analysis)
        self.history = []
        self.max_history = 360  # 1 hour at 10s intervals
        
        # Feeding state
        self.last_feed_tick = -999
        self.feed_amount_grams = 0
        
    def _daily_cycle(self, base_val, amplitude, phase_offset=0):
        """Simulate natural daily temperature/light cycle"""
        hour_angle = (self.tick * 10 / 3600) * 2 * math.pi / 24  # 10s per tick
        return base_val + amplitude * math.sin(hour_angle + phase_offset)
    
    def _add_noise(self, value, noise_pct=0.02):
        """Add realistic sensor noise"""
        noise = value * noise_pct * random.gauss(0, 1)
        return round(value + noise, 3)
    
    def trigger_feeding(self, amount_grams=15.0):
        """Simulate a feeding event"""
        self.last_feed_tick = self.tick
        self.feed_amount_grams = amount_grams
        self.mode = "post_feeding"
        
    def trigger_crisis(self):
        """
        Start gradual crisis: overfeeding + filter degradation.
        Crisis severity increases over time (not instant jump).
        """
        self.mode = "crisis"
        self.crisis_severity = 0.0
        
    def reset(self):
        """Return to normal operation"""
        self.mode = "normal"
        self.crisis_severity = 0.0
        self.history.clear()
        self.tick = 0
        
    def generate(self):
        """Generate one complete sensor reading"""
        self.tick += 1
        
        # --- Temperature: daily cycle (±1.5°C) ---
        temp = self._daily_cycle(self.base["temp"], 1.5, phase_offset=0)
        
        # --- pH: slight daily variation ---
        ph = self._daily_cycle(self.base["ph"], 0.15, phase_offset=math.pi/4)
        
        # --- Dissolved Oxygen: inversely related to temperature ---
        do = self.base["do"] - (temp - self.base["temp"]) * 0.3
        do = self._daily_cycle(do, 0.4, phase_offset=math.pi)  # higher at night
        
        # --- Ammonia: baseline + feeding impact ---
        nh3 = self.base["nh3"]
        
        # --- Turbidity: baseline ---
        turbidity = self.base["turbidity"]
        
        # === Post-feeding effects (gradual ammonia rise over 2-4 hours) ===
        ticks_since_feed = self.tick - self.last_feed_tick
        if ticks_since_feed > 0 and ticks_since_feed < 1440:  # within 4 hours (4*360)
            feed_factor = self.feed_amount_grams / 15.0  # normalize to standard portion
            
            # Ammonia rises, peaks at ~2 hours, then slowly recovers
            peak_tick = 720  # 2 hours
            if ticks_since_feed < peak_tick:
                # Rising phase
                nh3_boost = feed_factor * 0.4 * (ticks_since_feed / peak_tick)
            else:
                # Recovery phase
                recovery_progress = (ticks_since_feed - peak_tick) / 720
                nh3_boost = feed_factor * 0.4 * max(0, 1 - recovery_progress)
            
            nh3 += nh3_boost
            turbidity += feed_factor * 3 * max(0, 1 - ticks_since_feed / 360)
        
        # === Crisis mode: gradual degradation ===
        if self.mode == "crisis":
            self.crisis_severity = min(1.0, self.crisis_severity + 0.005)  # slow ramp
            
            # Ammonia climbs steadily (biofilter overwhelmed)
            nh3 += self.crisis_severity * 1.5
            
            # DO drops (bacterial oxygen consumption from decomposing food)
            do -= self.crisis_severity * 3.0
            
            # pH destabilizes
            ph -= self.crisis_severity * 0.8
            
            # Turbidity increases
            turbidity += self.crisis_severity * 25
            
            # Temperature slightly rises (decomposition is exothermic)
            temp += self.crisis_severity * 1.5
        
        # === Apply sensor noise ===
        reading = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pod_id": "POD_001",
            "temperature": round(self._add_noise(temp), 1),
            "ph": round(self._add_noise(ph), 2),
            "do": round(max(0.5, self._add_noise(do)), 1),
            "nh3": round(max(0.01, self._add_noise(nh3)), 3),
            "turbidity": round(max(1.0, self._add_noise(turbidity)), 1),
            "tick": self.tick,
            "mode": self.mode,
            "crisis_severity": round(self.crisis_severity, 3)
        }
        
        # Store in history buffer
        self.history.append(reading)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        return reading
    
    def get_history(self, last_n=None):
        """Return recent history for trend analysis"""
        if last_n:
            return self.history[-last_n:]
        return self.history


# =============================================
# Demo: Run simulator with crisis trigger
# =============================================
if __name__ == "__main__":
    sim = SensorSimulator(fish_species="tilapia")
    
    print("=" * 70)
    print("  EcoSphere Pod - Sensor Simulator Demo")
    print("  Press Ctrl+C to stop")
    print("=" * 70)
    
    try:
        for i in range(200):
            # Trigger feeding at tick 30
            if i == 30:
                print("\n>>> FEEDING EVENT: 20g dispensed")
                sim.trigger_feeding(amount_grams=20.0)
            
            # Trigger crisis at tick 100
            if i == 100:
                print("\n>>> CRISIS TRIGGERED: Biofilter failure simulation")
                sim.trigger_crisis()
            
            data = sim.generate()
            
            # Color-coded output
            nh3_warn = " ⚠️" if data["nh3"] > 0.8 else ""
            do_warn = " ⚠️" if data["do"] < 5.0 else ""
            
            print(f"[{data['mode']:>12}] "
                  f"Temp:{data['temperature']:5.1f}°C  "
                  f"pH:{data['ph']:5.2f}  "
                  f"DO:{data['do']:4.1f}mg/L{do_warn}  "
                  f"NH3:{data['nh3']:5.3f}ppm{nh3_warn}  "
                  f"Turb:{data['turbidity']:5.1f}NTU")
            
            time.sleep(0.3)  # speed up for demo (real: 10s)
            
    except KeyboardInterrupt:
        print("\n\nSimulator stopped.")
