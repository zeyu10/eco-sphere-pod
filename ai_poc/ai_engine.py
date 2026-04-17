"""
EcoSphere Pod - AI Ecosystem Intelligence Engine
Implements the four AI modules described in AI_INTELLIGENCE.md:
  1. Fish Stress Prediction (Z-score + weighted FSI)
  2. Smart Feeding Optimizer (Q10 metabolic scaling + post-feed evaluation)
  3. Plant Growth Predictor (growth curve + bottleneck diagnosis)
  4. Ecosystem Balance Optimizer (nutrient flow model + coordinated control)
"""

import math
import statistics
from datetime import datetime


# =============================================
# Module 1: Fish Stress Prediction
# =============================================

class FishStressPredictor:
    """
    Multi-parameter Z-score analysis with weighted Fish Stress Index (FSI).
    Implements the MVP algorithm for physiological monitoring.
    """
    
    # Species-specific safe ranges and importance weights
    SPECIES_PROFILES = {
        "tilapia": {
            "safe_ranges": {
                "temperature": (24.0, 30.0),
                "ph": (6.5, 7.5),
                "do": (5.0, 9.0),
                "nh3": (0.0, 0.5),
                "turbidity": (5.0, 30.0),
            },
            "weights": {
                "temperature": 0.15,
                "ph": 0.15,
                "do": 0.25,   # DO is critical for respiration
                "nh3": 0.30,  # Ammonia toxicity is the primary acute risk
                "turbidity": 0.15,
            }
        },
        "goldfish": {
            "safe_ranges": {
                "temperature": (18.0, 24.0),
                "ph": (6.8, 7.6),
                "do": (6.0, 9.0),
                "nh3": (0.0, 0.3),
                "turbidity": (5.0, 25.0),
            },
            "weights": {
                "temperature": 0.20,
                "ph": 0.15,
                "do": 0.25,
                "nh3": 0.25,
                "turbidity": 0.15,
            }
        }
    }
    
    def __init__(self, species="tilapia"):
        self.species = species
        self.profile = self.SPECIES_PROFILES.get(species, self.SPECIES_PROFILES["tilapia"])
    
    def calculate_zscore(self, current_value, history_values):
        """Calculate Z-score: deviation from rolling mean in standard deviations"""
        if len(history_values) < 10:
            return 0.0
        
        mean = statistics.mean(history_values)
        stdev = statistics.stdev(history_values)
        
        if stdev < 0.001:  # Avoid division by zero for static sensors
            return 0.0
        
        return abs(current_value - mean) / stdev
    
    def calculate_trend(self, values, window=30):
        """
        Linear regression slope on recent values (units per tick).
        """
        recent = values[-window:] if len(values) >= window else values
        if len(recent) < 5:
            return 0.0
        
        n = len(recent)
        x_mean = (n - 1) / 2
        y_mean = statistics.mean(recent)
        
        numerator = sum((i - x_mean) * (recent[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator < 0.001:
            return 0.0
        
        return numerator / denominator
    
    def predict_danger_hours(self, current_value, trend_slope, safe_range):
        """
        Project time remaining until a parameter exits the safe boundary.
        """
        if abs(trend_slope) < 0.0001:
            return None 
        
        ticks_per_hour = 360  # Based on 10s sensor intervals
        
        if trend_slope > 0:
            distance = safe_range[1] - current_value
        else:
            distance = current_value - safe_range[0]
        
        if distance <= 0:
            return 0  # Already breached
        
        ticks_to_danger = distance / abs(trend_slope)
        hours_to_danger = ticks_to_danger / ticks_per_hour
        
        return round(hours_to_danger, 1)
    
    def analyze(self, current_data, history):
        """
        Main analysis function. Returns FSI (0-100) and risk breakdown.
        """
        params = ["temperature", "ph", "do", "nh3", "turbidity"]
        z_scores = {}
        trends = {}
        danger_windows = {}
        
        for param in params:
            param_history = [h[param] for h in history if param in h]
            current_val = current_data.get(param, 0)
            
            z_scores[param] = self.calculate_zscore(current_val, param_history)
            trends[param] = self.calculate_trend(param_history)
            
            safe_range = self.profile["safe_ranges"][param]
            danger_windows[param] = self.predict_danger_hours(
                current_val, trends[param], safe_range
            )
        
        # Weighted Fish Stress Index (FSI)
        weights = self.profile["weights"]
        raw_fsi = sum(weights[p] * z_scores[p] for p in params)
        
        # Normalize: Z-score of 5 roughly equals FSI 100
        fsi_score = min(100, raw_fsi * 20)
        
        weighted_contributions = {p: weights[p] * z_scores[p] for p in params}
        dominant_factor = max(weighted_contributions, key=weighted_contributions.get)
        
        valid_windows = {p: h for p, h in danger_windows.items() if h is not None and h < 24}
        nearest_danger = min(valid_windows.values()) if valid_windows else None
        
        if fsi_score >= 80:
            risk_level = "CRITICAL"
        elif fsi_score >= 60:
            risk_level = "HIGH"
        elif fsi_score >= 40:
            risk_level = "MODERATE"
        else:
            risk_level = "HEALTHY"
        
        action = self._generate_action(dominant_factor, fsi_score, current_data)
        
        return {
            "fsi_score": round(fsi_score, 1),
            "risk_level": risk_level,
            "dominant_risk_factor": dominant_factor,
            "z_scores": {p: round(z, 2) for p, z in z_scores.items()},
            "trends": {p: round(t, 5) for p, t in trends.items()},
            "predicted_danger_hours": nearest_danger,
            "recommended_action": action,
        }
    
    def _generate_action(self, factor, fsi, data):
        """Generate corrective actuator commands based on risk"""
        actions = {
            "nh3": {
                "actuator": "feeder",
                "command": "PAUSE" if fsi > 70 else "REDUCE_20PCT",
                "reason": f"Ammonia at {data.get('nh3', 0):.3f} ppm — reducing waste load"
            },
            "do": {
                "actuator": "pump",
                "command": "MAX_SPEED" if fsi > 70 else "INCREASE",
                "reason": f"DO at {data.get('do', 0):.1f} mg/L — increasing aeration"
            },
            "temperature": {
                "actuator": "heater",
                "command": "ADJUST",
                "reason": f"Temperature at {data.get('temperature', 0):.1f}°C — stabilizing thermal profile"
            },
            "ph": {
                "actuator": "pump",
                "command": "INCREASE",
                "reason": f"pH at {data.get('ph', 0):.2f} — increasing gas exchange for buffering"
            },
            "turbidity": {
                "actuator": "pump",
                "command": "INCREASE",
                "reason": f"Turbidity at {data.get('turbidity', 0):.1f} NTU — boosting filtration cycle"
            }
        }
        return actions.get(factor, {"actuator": "none", "command": "MONITOR", "reason": "Stable conditions"})


# =============================================
# Module 2: Smart Feeding Optimizer
# =============================================

class FeedingOptimizer:
    """
    Q10 metabolic scaling with post-feeding evaluation (closed-loop).
    """
    
    Q10 = 2.0  # Standard biological temperature coefficient
    
    def __init__(self, base_feed_grams=15.0, reference_temp=25.0):
        self.base_feed_grams = base_feed_grams
        self.reference_temp = reference_temp
        self.feed_history = [] 
        self.adjustment_factor = 1.0  # Dynamically learned adjustment
    
    def calculate_feed_amount(self, current_temp, current_nh3, current_do,
                               nh3_threshold=0.8, do_minimum=5.0):
        """
        1. Scaling: Adjust for metabolic rate (Temp)
        2. Gating: Check water quality thresholds
        3. Learning: Apply historical adjustment factor
        """
        scaling_factor = self.Q10 ** ((current_temp - self.reference_temp) / 10.0)
        calculated_amount = self.base_feed_grams * scaling_factor
        
        water_quality_ok = True
        delay_reason = None
        
        if current_nh3 > nh3_threshold:
            water_quality_ok = False
            delay_reason = f"Ammonia spikes at {current_nh3:.3f} ppm (threshold: {nh3_threshold})"
        
        if current_do < do_minimum:
            water_quality_ok = False
            delay_reason = f"Hypoxia risk: DO {current_do:.1f} mg/L (min: {do_minimum})"
        
        if not water_quality_ok:
            return {
                "action": "DELAY",
                "reason": delay_reason,
                "retry_after_minutes": 60,
                "amount_grams": 0,
                "servo_angle": 0,
            }
        
        final_amount = calculated_amount * self.adjustment_factor
        servo_angle = min(180, int(final_amount / self.base_feed_grams * 90))
        
        return {
            "action": "FEED",
            "amount_grams": round(final_amount, 1),
            "servo_angle": servo_angle,
            "water_temp": current_temp,
            "q10_scaling": round(scaling_factor, 3),
            "learned_adjustment": round(self.adjustment_factor, 3),
            "reason": f"Q10 scaled: {self.base_feed_grams}g × {scaling_factor:.2f} × {self.adjustment_factor:.2f} = {final_amount:.1f}g"
        }
    
    def evaluate_post_feeding(self, pre_feed_nh3, post_feed_nh3_peak, amount_fed):
        """
        Evaluates metabolic load vs input to update adjustment factor.
        """
        delta_nh3 = post_feed_nh3_peak - pre_feed_nh3
        
        if delta_nh3 > 0.5:
            efficiency = "OVERFED"
            adjustment = -0.15 
        elif delta_nh3 > 0.3:
            efficiency = "SLIGHTLY_OVER"
            adjustment = -0.08
        elif delta_nh3 < 0.05:
            efficiency = "UNDERFED"
            adjustment = +0.10 
        else:
            efficiency = "OPTIMAL"
            adjustment = 0
        
        self.adjustment_factor = max(0.5, min(1.5, self.adjustment_factor + adjustment))
        
        result = {
            "efficiency": efficiency,
            "delta_nh3": round(delta_nh3, 4),
            "adjustment_applied": adjustment,
            "new_adjustment_factor": round(self.adjustment_factor, 3),
            "amount_fed": amount_fed,
        }
        
        self.feed_history.append(result)
        return result


# =============================================
# Module 3: Plant Growth Predictor
# =============================================

class PlantGrowthPredictor:
    """
    Growth modeling with environmental bottleneck diagnosis.
    """
    
    GROWTH_CURVES = {
        "lettuce": {"daily_rate": 8.0, "days_to_harvest": 35, "min_nitrate": 40, "light_hours": 14},
        "basil": {"daily_rate": 6.5, "days_to_harvest": 42, "min_nitrate": 35, "light_hours": 12},
        "bok_choy": {"daily_rate": 7.0, "days_to_harvest": 30, "min_nitrate": 45, "light_hours": 14},
    }
    
    def __init__(self, plant_species="lettuce"):
        self.species = plant_species
        self.curve = self.GROWTH_CURVES.get(plant_species, self.GROWTH_CURVES["lettuce"])
        self.growth_log = []
        self.days_planted = 0
        self.current_size_pct = 0.0  # Percentage of full maturity
    
    def simulate_daily_growth(self, nitrate_ppm, light_hours, water_temp):
        self.days_planted += 1
        
        # Calculate limiting factors (Liebig's Law of the Minimum)
        nutrient_factor = min(1.0, nitrate_ppm / self.curve["min_nitrate"])
        light_factor = min(1.0, light_hours / self.curve["light_hours"])
        temp_factor = 1.0 if 20 <= water_temp <= 28 else max(0.3, 1 - abs(water_temp - 24) * 0.05)
        
        limiting = min(nutrient_factor, light_factor, temp_factor)
        actual_rate = self.curve["daily_rate"] * limiting
        
        self.current_size_pct = min(100, self.current_size_pct + actual_rate)
        
        bottleneck = self._diagnose_bottleneck(nutrient_factor, light_factor, temp_factor,
                                                 nitrate_ppm, light_hours, water_temp)
        
        days_to_harvest = (100 - self.current_size_pct) / actual_rate if actual_rate > 0.1 else None
        health_score = min(100, (actual_rate / self.curve["daily_rate"]) * 100)
        
        result = {
            "day": self.days_planted,
            "species": self.species,
            "current_size_pct": round(self.current_size_pct, 1),
            "daily_growth_rate": round(actual_rate, 2),
            "expected_rate": self.curve["daily_rate"],
            "growth_health_score": round(health_score, 1),
            "limiting_factors": {
                "nutrients": round(nutrient_factor, 2),
                "light": round(light_factor, 2),
                "temperature": round(temp_factor, 2),
            },
            "bottleneck": bottleneck,
            "predicted_days_to_harvest": round(days_to_harvest, 1) if days_to_harvest else None,
        }
        
        self.growth_log.append(result)
        return result
    
    def _diagnose_bottleneck(self, nut_f, light_f, temp_f, nitrate, light_h, temp):
        factors = {"nutrients": nut_f, "light": light_f, "temperature": temp_f}
        worst = min(factors, key=factors.get)
        
        if factors[worst] >= 0.9:
            return None 
        
        diagnoses = {
            "nutrients": {
                "factor": "low_nutrients",
                "detail": f"Nitrate at {nitrate:.0f} ppm, target {self.curve['min_nitrate']} ppm",
                "action": "Increase fish feeding to boost nitrate production"
            },
            "light": {
                "factor": "insufficient_light",
                "detail": f"Current {light_h:.0f}h/day, required {self.curve['light_hours']}h/day",
                "action": f"Extend lighting cycle by {self.curve['light_hours'] - light_h:.0f} hours"
            },
            "temperature": {
                "factor": "temperature_stress",
                "detail": f"Water temp {temp:.1f}°C outside optimal vegetative range",
                "action": "Check heater/cooler to maintain 22-26°C"
            }
        }
        return diagnoses[worst]


# =============================================
# Module 4: Ecosystem Balance Optimizer
# =============================================

class EcosystemBalancer:
    """
    Master coordinator: resolves conflicts between expert modules.
    """
    
    def __init__(self):
        self.history = []
    
    def calculate_nutrient_flow(self, daily_feed_grams, water_temp, plant_growth_rate,
                                 biofilter_age_days=30):
        """
        Flow balance: fish_waste - biofilter_conversion - plant_uptake
        """
        fish_waste_nh3 = daily_feed_grams * 0.03
        
        temp_efficiency = min(1.0, water_temp / 25.0)
        maturity_efficiency = min(1.0, biofilter_age_days / 30.0) 
        biofilter_conversion = fish_waste_nh3 * temp_efficiency * maturity_efficiency * 0.85
        
        plant_absorption = plant_growth_rate * 0.1 
        net_accumulation = fish_waste_nh3 - biofilter_conversion - plant_absorption
        
        return {
            "fish_waste_nh3_mg": round(fish_waste_nh3, 3),
            "biofilter_conversion_mg": round(biofilter_conversion, 3),
            "plant_absorption_mg": round(plant_absorption, 3),
            "net_accumulation_mg": round(net_accumulation, 3),
            "biofilter_efficiency": round(temp_efficiency * maturity_efficiency, 2),
        }
    
    def optimize(self, fsi_result, feeding_result, plant_result, nutrient_flow, current_sensors):
        commands = {
            "pump": {"action": "NORMAL", "reason": ""},
            "lighting": {"action": "MAINTAIN", "reason": ""},
            "feeder": {"action": "MAINTAIN", "reason": ""},
        }
        
        overrides = []
        
        # === Priority 1: Safety (Predictive Intervention) ===
        if fsi_result["fsi_score"] >= 40:
            commands["pump"] = {"action": "MAX_SPEED", "reason": "Preemptive stress response — maximizing oxygen"}
            commands["feeder"] = {"action": "PAUSE", "reason": "Risk detected — halting feed to protect water quality"}
            overrides.append("SAFETY: Elevated FSI, overriding growth goals")
        
        # === Priority 2: Nutrient Balance ===
        elif nutrient_flow["net_accumulation_mg"] > 0.5:
            commands["feeder"] = {"action": "REDUCE_20PCT", "reason": "Nitrate buildup detected"}
            commands["lighting"] = {"action": "EXTEND_2H", "reason": "Increasing plant consumption"}
            overrides.append("BALANCE: Surplus detected")
            
        elif nutrient_flow["net_accumulation_mg"] < -0.3:
            # Safety lock: Only increase feed if NH3 is verified low
            if current_sensors.get("nh3", 0) < 0.4:
                commands["feeder"] = {"action": "INCREASE_15PCT", "reason": "Nutrient deficit — optimizing for plants"}
                overrides.append("BALANCE: Deficit optimization")
            else:
                commands["feeder"] = {"action": "MAINTAIN", "reason": "Deficit exists but NH3 safety buffer is insufficient"}
                overrides.append("CONFLICT: Safety lock preventing feed increase")
        
        # === Calculate Ecosystem Health Scores ===
        water_score = max(0, 100 - (current_sensors.get("nh3", 0) / 1.0 * 50))
        fish_score = max(0, 100 - fsi_result["fsi_score"])
        plant_score = plant_result["growth_health_score"] if plant_result else 70
        
        overall = water_score * 0.35 + fish_score * 0.35 + plant_score * 0.30
        
        result = {
            "ecosystem_score": {
                "overall": round(overall, 1),
                "water_quality": round(water_score, 1),
                "fish_health": round(fish_score, 1),
                "plant_health": round(plant_score, 1),
            },
            "nutrient_flow": nutrient_flow,
            "coordinated_commands": commands,
            "overrides": overrides,
            "status": "CRITICAL" if overall < 40 else "WARNING" if overall < 60 else "GOOD" if overall < 80 else "EXCELLENT",
        }
        
        self.history.append(result)
        return result


# =============================================
# Quick Integration Test
# =============================================
if __name__ == "__main__":
    print("=" * 60)
    print("  Testing EcoSphere Intelligence Engine")
    print("=" * 60)
    
    # 1. Stress Prediction Test
    fsp = FishStressPredictor("tilapia")
    fake_history = [{"temperature": 25.0, "ph": 7.0, "do": 7.8, "nh3": 0.2, "turbidity": 15} for _ in range(30)]
    
    crisis_data = {"temperature": 28.0, "ph": 6.2, "do": 4.5, "nh3": 1.5, "turbidity": 40}
    res = fsp.analyze(crisis_data, fake_history)
    print(f"\n[STRESS TEST] Crisis FSI: {res['fsi_score']} ({res['risk_level']})")
    print(f"Action: {res['recommended_action']['reason']}")
    
    # 2. Feeding Test
    fo = FeedingOptimizer()
    warm = fo.calculate_feed_amount(28.0, 0.2, 7.5)
    print(f"\n[FEEDING TEST] 28°C scaling: {warm['amount_grams']}g ({warm['q10_scaling']}x factor)")
    
    # 3. Growth Test
    pg = PlantGrowthPredictor("lettuce")
    growth = pg.simulate_daily_growth(nitrate_ppm=10, light_hours=8, water_temp=24)
    print(f"\n[GROWTH TEST] Bottleneck: {growth['bottleneck']['detail']}")
    print(f"Advice: {growth['bottleneck']['action']}")

    print("\nAll English localized tests completed successfully.")
