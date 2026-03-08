# MoveWise RL Engine (rl_engine)

Python backend for route recommendation, behavior simulation, and API serving.
This module contains the reinforcement learning logic that powers MoveWise decisions.

## Purpose

The RL engine models behavior shift from car-heavy travel to multimodal travel using:
- generalized cost modeling,
- a DQN-based policy,
- acceptance dynamics (habit + nudges + context),
- phased adoption constraints.

It supports both offline training and online serving via FastAPI.

## Tech Stack

- Python 3.10+
- PyTorch (DQN models)
- NumPy
- FastAPI + Uvicorn
- Matplotlib (training report PDF)

## Core Modules

```text
rl_engine/
  config.py             # user profile, mode definitions, rewards, RL hyperparameters
  generalized_cost.py   # generalized cost decomposition and ranking
  environment.py        # MDP environment and transition simulation
  agent.py              # DQN agent, replay buffer, target network
  train.py              # training loop, evaluation, plot generation
  api.py                # REST API consumed by movewise-react
  requirements.txt
```

## RL Formulation (Current Implementation)

### State

18-dimensional vector including:
- behavioral terms: habit, eco-sensitivity, loss aversion, car status,
- context: phase, week, trip type, weather, time of day,
- engagement: green streak, points, satisfaction, app engagement,
- budget and response tracking.

### Action

Compound action space:
- 7 transport modes x 7 nudge types = 49 actions.

### Reward

Weighted combination of:
- generalized cost,
- emissions effect,
- behavior penalty,
- constraint penalties,
- platform revenue,
- plus sustainable-choice and nudge bonuses.

### Transition

- user recommendation acceptance is probabilistic,
- rejected recommendations fall back to car behavior,
- habit decays with repeated green trips,
- phase progresses when behavioral milestones are met,
- weekly schedule simulates commute/errand/leisure trips.

## Training Flow

`train.py` pipeline:

1. Build environment + agent.
2. Roll out episodes and store transitions in replay buffer.
3. Train DQN on mini-batches (Double DQN target logic).
4. Decay epsilon and track episode metrics.
5. Evaluate trained policy without exploration.
6. Generate `RL_Training_Results.pdf`.

### Run Training

From repo root:

```bash
python -m rl_engine.train
```

Artifacts saved in this folder:
- `movewise_dqn.pth` (model checkpoint)
- `RL_Training_Results.pdf` (plots)

## API Flow

`api.py` exposes RL outputs for the frontend.

Typical runtime flow:
1. API starts and initializes environment and agent.
2. If `movewise_dqn.pth` exists, weights are loaded.
3. Frontend requests routes/nudges/profile.
4. Trip submissions update environment state in memory.

### Run API

From this folder:

```bash
uvicorn api:app --reload --port 8000
```

### Main Endpoints

- `GET /api/health`
- `GET /api/routes/{trip_type}`
- `GET /api/nudge/select`
- `GET /api/nudge/all`
- `GET /api/user/profile`
- `GET /api/carbon`
- `GET /api/adoption`
- `POST /api/user/trip`
- `GET /api/simulation/run`
- `GET /api/simulation/status`

## Setup

Install dependencies:

```bash
pip install -r rl_engine/requirements.txt
```

## Integration With Frontend

1. Start API on port 8000.
2. In `movewise-react`, replace mock-data reads with fetch calls to `/api/...`.
3. Keep payload shapes aligned with frontend component expectations.

## Configuration

Most tunables are in `config.py`:
- mode profiles and costs,
- user profile parameters,
- reward weights,
- RL hyperparameters (gamma, epsilon, buffer size, batch size, etc.).

## Developer Notes

- Use deterministic seeds for reproducible experiments.
- Keep reward terms normalized when adjusting weights.
- Validate endpoint contracts after any environment/state schema changes.
- If behavior changes, retrain and regenerate `movewise_dqn.pth`.
