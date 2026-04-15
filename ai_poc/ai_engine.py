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
    Multi-parameter Z-score analysis with weighted Fish Stress Index.
    MVP algorithm from AI_INTELLIGENCE.md Section 3.1.
    """
    
    # Species-specific safe ranges and weights
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
                "do": 0.25,   # DO is most critical for fish survival
                "nh3": 0.30,  # Ammonia toxicity is the #1 killer
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
        """Calculate Z-score: how many standard deviations from the rolling mean"""
        if len(history_values) < 10:
            return 0.0
        
        mean = statistics.mean(history_values)
        stdev = statistics.stdev(history_values)
        
        if stdev < 0.001:  # avoid division by zero
            return 0.0
        
        return abs(current_value - mean) / stdev
    
    def calculate_trend(self, values, window=30):
        """
        Linear regression slope on recent values.
        Positive = rising, negative = falling.
        Returns slope per tick (units/tick).
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
        Project how many hours until value exits safe range.
        Based on current trend direction and velocity.
        """
        if abs(trend_slope) < 0.0001:
            return None  # no significant trend
        
        ticks_per_hour = 360  # 10s intervals
        
        if trend_slope > 0:
            # Rising: when will it exceed upper bound?
            distance = safe_range[1] - current_value
        else:
            # Falling: when will it drop below lower bound?
            distance = current_value - safe_range[0]
        
        if distance <= 0:
            return 0  # already outside safe range
        
        ticks_to_danger = distance / abs(trend_slope)
        hours_to_danger = ticks_to_danger / ticks_per_hour
        
        return round(hours_to_danger, 1)
    
    def analyze(self, current_data, history):
        """
        Main analysis function.
        Returns Fish Stress Index (0-100) with risk breakdown.
        """
        params = ["temperature", "ph", "do", "nh3", "turbidity"]
        z_scores = {}
        trends = {}
        danger_windows = {}
        
        for param in params:
            # Extract history for this parameter
            param_history = [h[param] for h in history if param in h]
            current_val = current_data.get(param, 0)
            
            # Z-score calculation
            z_scores[param] = self.calculate_zscore(current_val, param_history)
            
            # Trend analysis
            trends[param] = self.calculate_trend(param_history)
            
            # Danger window projection
            safe_range = self.profile["safe_ranges"][param]
            danger_windows[param] = self.predict_danger_hours(
                current_val, trends[param], safe_range
            )
        
        # Weighted FSI calculation
        weights = self.profile["weights"]
        raw_fsi = sum(weights[p] * z_scores[p] for p in params)
        
        # Normalize to 0-100 (Z-score of 5 = FSI 100)
        fsi_score = min(100, raw_fsi * 20)
        
        # Identify dominant risk factor
        weighted_contributions = {p: weights[p] * z_scores[p] for p in params}
        dominant_factor = max(weighted_contributions, key=weighted_contributions.get)
        
        # Find nearest danger window
        valid_windows = {p: h for p, h in danger_windows.items() if h is not None and h < 24}
        nearest_danger = min(valid_windows.values()) if valid_windows else None
        
        # Determine risk level
        if fsi_score >= 80:
            risk_level = "CRITICAL"
        elif fsi_score >= 60:
            risk_level = "HIGH"
        elif fsi_score >= 40:
            risk_level = "MODERATE"
        else:
            risk_level = "HEALTHY"
        
        # Generate recommended action
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
        """Generate specific corrective action based on dominant risk"""
        actions = {
            "nh3": {
                "actuator": "feeder",
                "command": "PAUSE" if fsi > 70 else "REDUCE_20PCT",
                "reason": f"Ammonia at {data.get('nh3', 0):.3f} ppm — reduce nutrient input"
            },
            "do": {
                "actuator": "pump",
                "command": "MAX_SPEED" if fsi > 70 else "INCREASE",
                "reason": f"DO at {data.get('do', 0):.1f} mg/L — increase water circulation"
            },
            "temperature": {
                "actuator": "heater",
                "command": "ADJUST",
                "reason": f"Temperature at {data.get('temperature', 0):.1f}°C — stabilize"
            },
            "ph": {
                "actuator": "pump",
                "command": "INCREASE",
                "reason": f"pH at {data.get('ph', 0):.2f} — increase circulation for buffering"
            },
            "turbidity": {
                "actuator": "pump",
                "command": "INCREASE",
                "reason": f"Turbidity at {data.get('turbidity', 0):.1f} NTU — boost filtration"
            }
        }
        return actions.get(factor, {"actuator": "none", "command": "MONITOR", "reason": "Continue monitoring"})


# =============================================
# Module 2: Smart Feeding Optimizer
# =============================================

class FeedingOptimizer:
    """
    Q10 metabolic scaling with post-feeding evaluation.
    MVP algorithm from AI_INTELLIGENCE.md Section 3.2.
    """
    
    Q10 = 2.0  # biological temperature coefficient
    
    def __init__(self, base_feed_grams=15.0, reference_temp=25.0):
        self.base_feed_grams = base_feed_grams
        self.reference_temp = reference_temp
        self.feed_history = []  # stores past feeding outcomes
        self.adjustment_factor = 1.0  # learned from post-feed evaluation
    
    def calculate_feed_amount(self, current_temp, current_nh3, current_do,
                               nh3_threshold=0.8, do_minimum=5.0):
        """
        Dynamic feeding calculation:
        1. Q10 metabolic scaling based on water temperature
        2. Water quality gate check
        3. Apply learned adjustment from past feeding outcomes
        """
        # Step 1: Q10 metabolic scaling
        scaling_factor = self.Q10 ** ((current_temp - self.reference_temp) / 10.0)
        calculated_amount = self.base_feed_grams * scaling_factor
        
        # Step 2: Water quality pre-check
        water_quality_ok = True
        delay_reason = None
        
        if current_nh3 > nh3_threshold:
            water_quality_ok = False
            delay_reason = f"Ammonia elevated at {current_nh3:.3f} ppm (threshold: {nh3_threshold})"
        
        if current_do < do_minimum:
            water_quality_ok = False
            delay_reason = f"DO too low at {current_do:.1f} mg/L (minimum: {do_minimum})"
        
        if not water_quality_ok:
            return {
                "action": "DELAY",
                "reason": delay_reason,
                "retry_after_minutes": 60,
                "amount_grams": 0,
                "servo_angle": 0,
            }
        
        # Step 3: Apply learned adjustment
        final_amount = calculated_amount * self.adjustment_factor
        
        # Convert to servo angle (0-180 degrees, proportional to amount)
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
        Closed-loop learning: evaluate feeding outcome and adjust future amounts.
        Called 2-4 hours after each feeding event.
        """
        delta_nh3 = post_feed_nh3_peak - pre_feed_nh3
        
        if delta_nh3 > 0.5:
            efficiency = "OVERFED"
            adjustment = -0.15  # reduce future feeds by 15%
        elif delta_nh3 > 0.3:
            efficiency = "SLIGHTLY_OVER"
            adjustment = -0.08
        elif delta_nh3 < 0.05:
            efficiency = "UNDERFED"
            adjustment = +0.10  # increase future feeds by 10%
        else:
            efficiency = "OPTIMAL"
            adjustment = 0
        
        # Update learned adjustment factor
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
    Growth curve modeling with bottleneck diagnosis.
    MVP algorithm from AI_INTELLIGENCE.md Section 3.3.
    (Camera image analysis simulated via growth parameters)
    """
    
    # Expected growth rates (% leaf area increase per day) under ideal conditions
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
        self.current_size_pct = 0.0  # 0% to 100% (harvest-ready)
    
    def simulate_daily_growth(self, nitrate_ppm, light_hours, water_temp):
        """
        Calculate actual daily growth based on environmental conditions.
        In real system, this would use camera image analysis.
        """
        self.days_planted += 1
        
        # Calculate growth limiting factors
        nutrient_factor = min(1.0, nitrate_ppm / self.curve["min_nitrate"])
        light_factor = min(1.0, light_hours / self.curve["light_hours"])
        temp_factor = 1.0 if 20 <= water_temp <= 28 else max(0.3, 1 - abs(water_temp - 24) * 0.05)
        
        # Actual growth = ideal rate × worst limiting factor
        limiting = min(nutrient_factor, light_factor, temp_factor)
        actual_rate = self.curve["daily_rate"] * limiting
        
        self.current_size_pct = min(100, self.current_size_pct + actual_rate)
        
        # Bottleneck diagnosis
        bottleneck = self._diagnose_bottleneck(nutrient_factor, light_factor, temp_factor,
                                                nitrate_ppm, light_hours, water_temp)
        
        # Harvest date prediction
        if actual_rate > 0.1:
            remaining_pct = 100 - self.current_size_pct
            days_to_harvest = remaining_pct / actual_rate
        else:
            days_to_harvest = None  # growth stalled
        
        # Health score (actual vs expected)
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
        """Identify the specific limiting factor"""
        factors = {"nutrients": nut_f, "light": light_f, "temperature": temp_f}
        worst = min(factors, key=factors.get)
        
        if factors[worst] >= 0.9:
            return None  # all factors adequate
        
        diagnoses = {
            "nutrients": {
                "factor": "low_nutrients",
                "detail": f"Nitrate at {nitrate:.0f} ppm, target {self.curve['min_nitrate']} ppm",
                "action": "Increase fish feeding to boost nutrient production"
            },
            "light": {
                "factor": "insufficient_light",
                "detail": f"Current {light_h:.0f}h/day, required {self.curve['light_hours']}h/day",
                "action": f"Extend smart lighting by {self.curve['light_hours'] - light_h:.0f} hours"
            },
            "temperature": {
                "factor": "temperature_stress",
                "detail": f"Water temp {temp:.1f}°C outside optimal range",
                "action": "Adjust heater to maintain 22-26°C"
            }
        }
        return diagnoses[worst]


# =============================================
# Module 4: Ecosystem Balance Optimizer
# =============================================

class EcosystemBalancer:
    """
    Master coordinator: nutrient flow modeling + multi-objective optimization.
    Sits above the three expert modules and resolves conflicts.
    MVP algorithm from AI_INTELLIGENCE.md Section 3.4.
    """
    
    def __init__(self):
        self.history = []
    
    def calculate_nutrient_flow(self, daily_feed_grams, water_temp, plant_growth_rate,
                                 biofilter_age_days=30):
        """
        Material balance equation:
        net = fish_waste_production - biofilter_conversion - plant_absorption
        """
        # Fish waste production (approx 3% of feed becomes ammonia)
        fish_waste_nh3 = daily_feed_grams * 0.03
        
        # Biofilter conversion (temperature-dependent nitrifying bacteria)
        # Efficiency peaks at 25°C, drops below 15°C
        temp_efficiency = min(1.0, water_temp / 25.0)
        maturity_efficiency = min(1.0, biofilter_age_days / 30.0)  # takes ~30 days to mature
        biofilter_conversion = fish_waste_nh3 * temp_efficiency * maturity_efficiency * 0.85
        
        # Plant absorption (proportional to growth rate)
        plant_absorption = plant_growth_rate * 0.1  # simplified nutrient uptake model
        
        net_accumulation = fish_waste_nh3 - biofilter_conversion - plant_absorption
        
        return {
            "fish_waste_nh3_mg": round(fish_waste_nh3, 3),
            "biofilter_conversion_mg": round(biofilter_conversion, 3),
            "plant_absorption_mg": round(plant_absorption, 3),
            "net_accumulation_mg": round(net_accumulation, 3),
            "biofilter_efficiency": round(temp_efficiency * maturity_efficiency, 2),
        }
    
    def optimize(self, fsi_result, feeding_result, plant_result, nutrient_flow, current_sensors):
        """
        Master coordination logic.
        Resolves conflicts between expert modules and issues unified commands.
        """
        commands = {
            "pump": {"action": "NORMAL", "reason": ""},
            "lighting": {"action": "MAINTAIN", "reason": ""},
            "feeder": {"action": "MAINTAIN", "reason": ""},
        }
        
        overrides = []
        
        # === Priority 1: Safety override (FSI critical) ===
        if fsi_result["fsi_score"] >= 80:
            commands["pump"] = {"action": "MAX_SPEED", "reason": "Critical fish stress — maximize oxygenation"}
            commands["feeder"] = {"action": "PAUSE_24H", "reason": "Critical stress — stop all feeding"}
            overrides.append("SAFETY: FSI critical, overriding all other recommendations")
        
        # === Priority 2: Nutrient balance ===
        elif nutrient_flow["net_accumulation_mg"] > 0.5:
            # Nutrient buildup — risk of ammonia spike
            commands["feeder"] = {"action": "REDUCE_20PCT", "reason": "Nutrient accumulation — reduce input"}
            commands["lighting"] = {"action": "EXTEND_2H", "reason": "Boost plant absorption to consume excess nutrients"}
            commands["pump"] = {"action": "INCREASE", "reason": "Improve circulation for filtration"}
            overrides.append("BALANCE: Nutrient surplus detected, reducing feed + boosting absorption")
            
        elif nutrient_flow["net_accumulation_mg"] < -0.3:
            # Nutrient deficit — plants starving
            commands["feeder"] = {"action": "INCREASE_15PCT", "reason": "Nutrient deficit — plants need more"}
            overrides.append("BALANCE: Nutrient deficit, increasing feed for plant nutrition")
        
        # === Priority 3: Plant growth optimization (only if no safety/balance issues) ===
        if plant_result and plant_result.get("bottleneck") and not overrides:
            bottleneck = plant_result["bottleneck"]
            if bottleneck["factor"] == "insufficient_light":
                commands["lighting"] = {"action": "EXTEND_2H", "reason": bottleneck["action"]}
            elif bottleneck["factor"] == "low_nutrients":
                # Check: can we safely increase feeding?
                if current_sensors["nh3"] < 0.5 and fsi_result["fsi_score"] < 40:
                    commands["feeder"] = {"action": "INCREASE_10PCT", "reason": "Safe to increase for plant nutrition"}
                else:
                    overrides.append("CONFLICT: Plants need more nutrients but water quality cannot support increased feeding")
        
        # === Calculate ecosystem score ===
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
# Quick Test
# =============================================
if __name__ == "__main__":
    # Test Fish Stress Predictor
    print("=" * 60)
    print("  Testing Fish Stress Predictor")
    print("=" * 60)
    
    fsp = FishStressPredictor("tilapia")
    
    # Generate fake history (30 normal readings)
    fake_history = []
    import random
    for i in range(30):
        fake_history.append({
            "temperature": 25.0 + random.gauss(0, 0.5),
            "ph": 7.0 + random.gauss(0, 0.1),
            "do": 7.8 + random.gauss(0, 0.3),
            "nh3": 0.2 + random.gauss(0, 0.05),
            "turbidity": 15.0 + random.gauss(0, 2),
        })
    
    # Test with normal data
    normal_data = {"temperature": 25.5, "ph": 7.1, "do": 7.5, "nh3": 0.25, "turbidity": 16}
    result = fsp.analyze(normal_data, fake_history)
    print(f"\nNormal: FSI={result['fsi_score']}, Risk={result['risk_level']}")
    
    # Test with crisis data
    crisis_data = {"temperature": 28.0, "ph": 6.2, "do": 4.5, "nh3": 1.5, "turbidity": 40}
    result = fsp.analyze(crisis_data, fake_history)
    print(f"Crisis: FSI={result['fsi_score']}, Risk={result['risk_level']}, "
          f"Factor={result['dominant_risk_factor']}")
    print(f"Action: {result['recommended_action']}")
    
    # Test Feeding Optimizer
    print("\n" + "=" * 60)
    print("  Testing Feeding Optimizer")
    print("=" * 60)
    
    fo = FeedingOptimizer(base_feed_grams=15.0, reference_temp=25.0)
    
    warm = fo.calculate_feed_amount(current_temp=28.0, current_nh3=0.2, current_do=7.5)
    print(f"\nWarm water (28°C): {warm['amount_grams']}g — {warm['reason']}")
    
    cold = fo.calculate_feed_amount(current_temp=18.0, current_nh3=0.2, current_do=7.5)
    print(f"Cold water (18°C): {cold['amount_grams']}g — {cold['reason']}")
    
    bad_water = fo.calculate_feed_amount(current_temp=25.0, current_nh3=1.2, current_do=7.5)
    print(f"Bad water (NH3=1.2): {bad_water['action']} — {bad_water['reason']}")
    
    print("\n  All tests passed!")
