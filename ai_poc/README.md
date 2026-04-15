# AI Proof of Concept (PoC)

> Proof of concept implementation for the EcoSphere Pod AI Intelligence Layer.
> See [AI_INTELLIGENCE.md](../AI_INTELLIGENCE.md) for the full technical specification.

## Quick Start

```bash
cd ai_poc
python demo.py
```

No external dependencies required — runs on Python 3.8+ standard library only.

## Files

| File | Description |
| --- | --- |
| `sensor_simulator.py` | Realistic sensor data generator with daily cycles, feeding response curves, and gradual crisis modeling |
| `ai_engine.py` | Four AI modules: Fish Stress Predictor (Z-score FSI), Feeding Optimizer (Q10 scaling), Plant Growth Predictor, Ecosystem Balancer |
| `demo.py` | Live demo script for pitch presentation — runs through normal → feeding → crisis phases with color-coded terminal output |

## Demo Phases

The `demo.py` script runs three phases automatically:

1. **Normal Operation** — System running healthy, all parameters within safe range (green output)
2. **Smart Feeding Event** — AI calculates optimal feed amount using Q10 metabolic scaling, then monitors post-feeding ammonia response
3. **Crisis Simulation** — Biofilter failure causes gradual ammonia rise and DO drop. Watch the AI detect the pattern and issue coordinated emergency responses

## AI Modules Demonstrated

### Fish Stress Prediction
- Z-score anomaly detection on 24-hour rolling window
- Weighted composite Fish Stress Index (0-100)
- Multi-parameter trend analysis with danger window projection
- Species-specific baseline calibration (tilapia, goldfish)

### Smart Feeding Optimizer
- Q10 biological temperature coefficient for metabolic scaling
- Water quality gate (ammonia/DO pre-check before feeding)
- Post-feeding evaluation with closed-loop learning
- Adaptive adjustment factor that improves over time

### Plant Growth Predictor
- Growth curve modeling with species-specific expected rates
- Multi-factor bottleneck diagnosis (nutrients, light, temperature)
- Harvest date prediction based on actual vs expected growth

### Ecosystem Balance Optimizer
- Nutrient flow material balance equation
- Multi-objective optimization (water quality vs fish health vs plant growth)
- Conflict resolution: overrides individual module recommendations when necessary
- Coordinated actuator commands (pump + lighting + feeder as one system)

## Architecture Alignment

This PoC implements the MVP Phase algorithms from `AI_INTELLIGENCE.md`:
- Statistical methods (Z-score, linear regression, weighted scoring)
- Expert rules with priority-based conflict resolution
- Closed-loop learning for feeding optimization
- Material balance equation for ecosystem modeling

The Post-Launch ML models (LSTM, XGBoost, MobileNetV2 CNN) are documented in `AI_INTELLIGENCE.md` Section 2.2 and will be implemented after collecting sufficient real-world data.
