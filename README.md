# MoveWise

**Reinforcement Learning for Behaviorally-Aware Mobility-as-a-Service**

[![CI](https://github.com/Sajjad-Shahali/RL-Mobility-Optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/Sajjad-Shahali/RL-Mobility-Optimizer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ed.svg)](https://docs.docker.com/compose/)

> NEXUS 2026 Hackathon -- Politecnico di Torino

**Authors:** Ali Vaezi, Sajjad Shahali, Kiana Salimi

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Architecture](#architecture)
- [RL Engine](#rl-engine)
- [React Frontend](#react-frontend)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Training Results](#training-results)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Impact Summary](#impact-summary)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

MoveWise is a Mobility-as-a-Service (MaaS) platform that combines a **Deep Q-Network** recommendation engine with a **React + Three.js** frontend to nudge car-dependent users toward sustainable multimodal transport. The system integrates all transport modes (public transit, e-scooters, bike-sharing, carpooling) into a single application with unified payment, personalized route ranking, and behavioral nudging powered by reinforcement learning.

The RL engine is grounded in a formal mathematical formulation (`RL_MaaS_Formulation_v3`) that brings together:

- **Generalized Cost (GC) theory** with context-dependent Value of Time
- **Prospect Theory** (Kahneman and Tversky, 1979) with loss aversion parameter mu = 2.25
- **HUR behavioral model** (Habits, Utility, Rationality) for user acceptance modeling
- **Phased adoption** that gradually transitions users from car dependency to multimodal mobility

---

## Problem Statement

Urban transportation accounts for 30% of total EU greenhouse gas emissions (European Environment Agency, 2024). In the Turin metropolitan area:

| Issue | Scale |
|---|---|
| Daily commuters driving alone | 72% |
| Average car idle time | 96% of the day |
| True monthly car cost (perceived: EUR 60) | EUR 510 |
| CO2 per 30 km car commute | 4.2 kg/day |
| EU annual congestion cost | EUR 270 billion |

Existing mobility apps solve route planning but do not address the behavioral and economic barriers to sustainable transport adoption: habit inertia, cost misperception, information asymmetry, fragmented ticketing, and lack of positive reinforcement.

MoveWise addresses these barriers through a multi-pronged approach combining AI personalization, economic transparency, insurance-linked incentives, and gamification.

### What is MaaS?

Mobility-as-a-Service (MaaS) is a paradigm shift in urban transport. Instead of owning a vehicle, users access a spectrum of transport options -- public transit, e-scooters, bike-sharing, carpooling, and on-demand rides -- through a single digital platform with unified payment and seamless journey planning.

Key MaaS principles implemented in MoveWise:

1. **Integration** -- All transport modes (GTT buses, Trenitalia trains, Voi/Lime e-scooters, ToBike, carpooling) under one roof
2. **Personalisation** -- AI-powered route ranking based on individual preferences, habits, and behavioral profile
3. **Unified Payment** -- One QR code for tap-in/tap-out across all modes; digital wallet with budget tracking
4. **Subscription Models** -- Pay-as-you-go, monthly PT bundle (EUR 49/mo), or Premium (EUR 65/mo with insurance)
5. **Behavioral Nudging** -- Gamification, social proof, loss framing, and commitment devices to encourage adoption

---

## Architecture

```text
+---------------------------+       HTTP/JSON        +---------------------------+
|    React Frontend         | <--------------------> |    RL Engine (FastAPI)     |
|    (Vite + Three.js)      |    /api/routes          |    Double DQN Agent       |
|                           |    /api/nudge/select    |    Nudge Q-Network        |
|  - Route Planner          |    /api/user/profile    |    GC Ranker              |
|  - QR Payment             |    /api/user/trip       |    HUR Acceptance Model   |
|  - Gamification           |    /api/carbon          |    Environment (MDP)      |
|  - Insurance Hub          |    /api/adoption        |    Training Pipeline      |
|  - Carpool Matching       |                         |                           |
+---------------------------+                         +---------------------------+
        |                                                       |
        | Port 5173                                             | Port 8000
        +-------------------------------------------------------+
                              Docker Compose
```

---

## RL Engine

The `rl_engine/` module is a complete Python implementation of the RL formulation described in `RL_MaaS_Formulation_v3.tex`. It replaces the static mock data with live, trained RL decisions.

### Formulation Summary

| Component | Implementation | Reference |
|---|---|---|
| State Space | 18 dimensions (habit, eco-sensitivity, loss aversion, phase, weather, trip type, engagement, ...) | v3 Eq. 3 |
| Action Space | Compound: 7 transport modes x 7 nudge types = 49 actions | v3 Sec. 7.2 |
| Reward | 5-component: -[w1 GC + w2 CO2 + w3 Psi_behavior + w4 Phi_constraints] + w5 Revenue | v3 Eq. 4 |
| GC Function | Multi-component with transfer penalties (3.5 EUR, Wardman 2004), productivity-adjusted VOT | v3 Sec. 5 |
| Prospect Theory | Loss aversion mu = 2.25 (switching costs amplified) | v3 Sec. 5 |
| Behavioral Model | HUR acceptance: habit resistance + utility + eco-motivation + nudge effectiveness | v3 Sec. 6 |
| Habit Decay | H_t = H_0 * exp(-alpha * green_trips) | v3 Eq. 2 |
| Phase Adoption | 4-phase progressive mode unlocking (constraint C10) | v3 Sec. 8 |
| Nudge Agent | Separate Q-network: Nudge*(i,t) = argmax Q_hat(s, nudge; theta_nudge) | v3 Eq. 5 |
| Data Quality | C11 constraint: prefer modes generating observable QR data | v3 Eq. 6 |

### Generalized Cost

The GC function decomposes the cost of each transport mode into:

```
GC = Time_cost + Monetary_cost + Transfer_penalty + Reliability_penalty
     + Comfort_penalty + Walking_penalty + Environmental_cost
     + Weather_penalty + Peak_penalty
```

Each component uses context-dependent parameters. The Value of Time (VOT) is adjusted for productivity: time on a train where the user can study is valued differently than time spent driving.

A Prospect Theory adjustment amplifies the perceived cost of switching away from the status quo (car), reflecting the empirical finding that losses are felt 2.25x more strongly than equivalent gains.

### Transport Modes

Seven modes are defined for the Caselle Torinese to Orbassano corridor (approximately 11 km):

| Mode | Travel Time | Cost | CO2/trip | Phase |
|---|---|---|---|---|
| Car (Passenger) | 45 min | EUR 5.00 | 4.20 kg | 0 |
| Car (Driver) | 45 min | EUR 5.00 | 4.20 kg | 0 |
| P&R + Train | 40 min | EUR 3.75 | 2.10 kg | 0 |
| E-Scooter + Train + Walk | 30 min | EUR 4.20 | 0.84 kg | 1 |
| Bus + Train + Walk | 38 min | EUR 2.80 | 1.60 kg | 0 |
| Carpool + Walk | 29 min | EUR 2.70 | 2.10 kg | 2 |
| Walk + Train + Bike | 40 min | EUR 2.50 | 0.21 kg | 1 |

Emission factors from EEA 2024: Car 140 g/km, Bus 68 g/km, Train 14 g/km, E-Scooter 22 g/km.

### Nudge Strategies

Seven behavioral nudge types are implemented, based on Thaler and Sunstein (2008):

| Nudge | Mechanism | Example |
|---|---|---|
| Default Green | Default Effect | Green option shown first |
| Social Proof | Conformity | "87% of students on your route take the train" |
| Loss Frame | Prospect Theory | "You are losing EUR 450/month on hidden car costs" |
| Carbon Budget | Salience | Monthly carbon usage visualization |
| Streak Reminder | Commitment | "5-day green streak, keep it going" |
| Commitment Device | Foot-in-door | "Try PT for 1 week, free ride back if not satisfied" |
| Anchoring | Anchoring bias | "Car: EUR 510/mo vs PT: EUR 55/mo" |

---

## React Frontend

The frontend is a fully interactive prototype built with React 18, Vite 5, Three.js, and Leaflet. It demonstrates the complete user experience within an iPhone-style phone frame.

### Core Screens

| Screen | Description |
|---|---|
| Home | Services grid, RL-powered trip suggestion, adoption journey progress |
| Trips | Route planner with four smart tabs (Best for You, Cheapest, Fastest, Greenest), 3D route arc, origin/destination inputs |
| Pay | QR tap-in/tap-out payment, expandable journey timeline, digital wallet, subscription plans |
| Rankings | Leaderboard, active challenges, badge collection, rewards catalog, 3D emissions skyline |
| Profile | Priority levels, 14 travel preferences, RL behavioral profile (HUR visualization), true cost calculator, carbon budget |
| Insurance | Premium calculator, 8 coverage toggles, parking finder, AI chatbot, claims center |
| Carpool | Peer matching with route overlap, Leaflet map, ride history, safety features |

### Onboarding

- GDPR-compliant consent prompt with 6 legal articles
- 9-step interactive tutorial with 3D robot assistant
- Persistent consent and tutorial state via localStorage

---

## Getting Started

### Prerequisites

- Python 3.9+ with pip
- Node.js 18+ with npm
- Docker and Docker Compose (optional)

### Option A: Docker (recommended)

```bash
git clone https://github.com/Sajjad-Shahali/RL-Mobility-Optimizer.git
cd RL-Mobility-Optimizer
docker compose up
```

This starts the RL API on port 8000 and the React frontend on port 5173.

### Option B: Manual Setup

**RL Engine:**

```bash
pip install -r rl_engine/requirements.txt
python -m rl_engine.train                # Train the DQN (500 episodes, approximately 2 min)
uvicorn rl_engine.api:app --port 8000    # Start the API server
```

**Frontend:**

```bash
cd movewise-react
npm install
npm run dev
```

### Training Only (Docker)

```bash
docker compose --profile training run rl-train
```

### Build for Production

```bash
cd movewise-react
npm run build
npm run preview
```

---

## API Reference

All endpoints return data in the exact shape expected by the React frontend components, enabling a drop-in replacement of `mockData.js` with `fetch()` calls.

| Endpoint | Method | Description | Frontend Consumer |
|---|---|---|---|
| `/api/health` | GET | Health check and model status | -- |
| `/api/routes/{trip_type}` | GET | RL-ranked routes matching `routeOptions` shape | TripsScreen, HomeScreen |
| `/api/nudge/select` | GET | Optimal nudge matching `nudges[i]` shape | HomeScreen (NudgeBanner) |
| `/api/nudge/all` | GET | All nudges matching `nudges` array | -- |
| `/api/user/profile` | GET | Full profile matching `userProfile` shape | ProfileScreen, HomeScreen, RankingsScreen |
| `/api/carbon` | GET | Carbon budget matching `carbonData` shape | ProfileScreen, RankingsScreen |
| `/api/adoption` | GET | Adoption phases with live status | HomeScreen |
| `/api/user/trip` | POST | Record a trip, returns updated habit/phase/points | -- |
| `/api/simulation/run` | GET | Run a training simulation | -- |
| `/api/simulation/status` | GET | Training progress | -- |

### Route Response Shape

Each route in the `/api/routes/{trip_type}` response contains:

```json
{
  "id": 1,
  "title": "E-Scooter + Train + Walk",
  "label": "RL Recommended",
  "subtitle": "Personalized by AI based on your behavioral profile",
  "segments": [
    {"mode": "scooter_icon", "name": "E-Scooter", "duration": "7 min", "provider": "Voi"},
    {"mode": "train_icon", "name": "Train SFM1", "duration": "18 min", "provider": "GTT"},
    {"mode": "walk_icon", "name": "Walk", "duration": "5 min", "provider": ""}
  ],
  "totalTime": "30 min",
  "cost": "EUR 4.20",
  "co2": "-80%",
  "co2Saved": "3.4 kg",
  "reliability": "89%",
  "comfort": "High",
  "greenPoints": 50,
  "gcScore": 12.4,
  "tags": ["Seated train", "Can study", "Wi-Fi"]
}
```

---

## Training Results

Trained on Giuseppe's profile (23-year-old medical student, Caselle Torinese to Orbassano, 11 km, 3 commute days per week):

| Metric | Before RL | After 500 Episodes | Change |
|---|---|---|---|
| Green Trip Ratio | 0% | 70.5% | +70.5 pp |
| CO2 Saved (7-week sim) | 0 kg | 85.4 kg | New savings |
| Car Habit Strength | 0.70 | 0.10 | -85.7% |
| Adoption Phase | 0 (Onboarding) | 3 (Optimised) | Full journey |
| User Satisfaction | 0.50 | 0.52 | Maintained |

The training pipeline generates a 4-page PDF visualization (`rl_engine/RL_Training_Results.pdf`) with reward convergence curves, green ratio progression, CO2 savings over time, and habit decay plots.

---

## Project Structure

```text
rl_engine/                           Python RL backend
  config.py                          Mode profiles, user params, HUR constants, reward weights
  generalized_cost.py                GC function with Prospect Theory, context-dependent VOT
  environment.py                     MDP: 18-dim state, 49 actions, HUR acceptance, phased adoption
  agent.py                           Double DQN + nudge Q-network
  train.py                           Training pipeline + evaluation + PDF visualization
  api.py                             FastAPI server (matches mockData.js response shapes)
  requirements.txt                   Python dependencies
  README.md                          RL engine documentation

movewise-react/                      React frontend (Vite + Three.js + Leaflet)
  src/
    App.jsx                          Root component: consent, splash, onboarding, main routing
    main.jsx                         Entry point
    data/mockData.js                 Static data with API endpoint annotations
    components/                      12 screen components + 7 Three.js 3D components + shared UI
    styles/app.css                   All styles (3200+ lines)
  package.json                       Node.js dependencies and scripts

Dockerfile                           Python 3.11-slim, CPU-only PyTorch, health check
docker-compose.yml                   Three services: rl-engine, frontend, rl-train
.dockerignore                        Excludes .git, node_modules, model weights
.github/
  workflows/ci.yml                   CI pipeline: RL tests, frontend build, Docker build
  ISSUE_TEMPLATE/                    Bug report and feature request templates
  pull_request_template.md           PR checklist with formulation references

CHANGELOG.md                         Version history
CITATION.cff                         Citation metadata for academic use
CONTRIBUTING.md                      Development guidelines and code style
SECURITY.md                          Vulnerability reporting policy
LICENSE                              MIT License
```

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| RL Engine | Python, PyTorch, NumPy | DQN training, GC computation, behavioral modeling |
| API | FastAPI, Uvicorn, Pydantic | REST endpoints for frontend integration |
| Frontend | React 18.3, Vite 5 | Component-based UI with fast HMR |
| 3D Graphics | Three.js, React Three Fiber, Drei | Route arc, QR parallax, wallet cards, tutorial robot |
| Maps | Leaflet, React-Leaflet, OpenStreetMap | Carpool route visualization |
| Containerization | Docker, Docker Compose | Reproducible deployment |
| CI/CD | GitHub Actions | Automated testing on push and PR |

---

## Impact Summary

| Metric | Per User / Year | Scaled to 1,000 Users |
|---|---|---|
| CO2 reduced | 1,000 kg | 1,000 tonnes |
| Money saved | EUR 5,460 | EUR 5.46 million |
| Time saved | 130 hours | 130,000 hours |
| Cars removed from peak traffic | 1 | 1,000 |

---

## Troubleshooting

**Node.js not found:** Install Node.js LTS from https://nodejs.org, restart your terminal, and verify with `node -v`.

**Resetting onboarding state:** MoveWise persists consent and tutorial completion in localStorage. To see the full onboarding flow again:

```js
localStorage.removeItem("movewise_consent");
localStorage.removeItem("movewise_onboarded");
location.reload();
```

**Docker port conflicts:** Ensure ports 5173 and 8000 are not in use before running `docker compose up`.

---

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines, code style conventions, and the pull request process.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Citation

If you use this work in academic research, please cite:

```bibtex
@software{movewise2026,
  author    = {Vaezi, Ali and Shahali, Sajjad and Salimi, Kiana},
  title     = {MoveWise: Reinforcement Learning for Behaviorally-Aware Mobility-as-a-Service},
  year      = {2026},
  url       = {https://github.com/Sajjad-Shahali/RL-Mobility-Optimizer},
  version   = {0.4.0},
  institution = {Politecnico di Torino}
}
```

---

*Built for NEXUS 2026 Hackathon -- Politecnico di Torino*
