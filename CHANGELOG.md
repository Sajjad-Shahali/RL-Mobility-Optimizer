# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.4.0] - 2026-03-08

### Added
- API response shapes now match React frontend `mockData.js` for drop-in replacement
- New endpoints: `/api/carbon`, `/api/adoption`, `/api/nudge/all`
- Mode display metadata with segment icons, durations, and provider names
- Dynamic nudge text personalization (carbon budget %, streak count)
- Full `userProfile` shape with 14 preference toggles and behavioral parameters

### Fixed
- `comfort` attribute error in API routes endpoint (now `comfort_score`)
- `transfers` attribute error (now `num_transfers`)
- `green_trips_total` reference (now `green_trips`)
- `peak` parameter correctly mapped to `time_of_day`
- Added missing `monthly_budget` and `co2_target_monthly` to UserProfile

## [0.3.0] - 2026-03-07

### Added
- Docker support: `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- Three services: rl-engine (port 8000), frontend (port 5173), rl-train (training profile)
- Improved docstrings across all RL engine modules with v3 section and equation references
- RL Engine Implementation section in main README with architecture and training results

### Changed
- All module-level docstrings now reference specific v3 formulation sections

## [0.2.0] - 2026-03-06

### Added
- Complete RL engine: `config.py`, `generalized_cost.py`, `environment.py`, `agent.py`, `train.py`, `api.py`
- Generalized Cost function with Prospect Theory (loss aversion mu = 2.25)
- HUR behavioral acceptance model with habit decay
- Double DQN with separate nudge Q-network
- 7 transport modes x 7 nudge types = 49 compound actions
- 18-dimensional state space
- 5-component reward function
- FastAPI backend with CORS for React integration
- Training pipeline with PDF visualization output

### Training Results
- Green trip ratio: 0% to 70.5%
- CO2 saved (7-week simulation): 85.4 kg
- Car habit strength: 0.70 to 0.10
- Adoption phase: 0 (Onboarding) to 3 (Optimised)

## [0.1.0] - 2026-03-01

### Added
- React 18.3 + Vite 5 frontend with Three.js 3D graphics
- 12 React components: Home, Trips, Pay, Rankings, Profile, Insurance, Carpool, UserProfile, Consent, Onboarding, Splash, PhoneShell
- Leaflet/OpenStreetMap integration for carpool route visualization
- QR tap-in/tap-out payment flow with journey timeline
- Gamification system: Green Points, leaderboard, challenges, badges
- GDPR-compliant consent prompt with 6 legal articles
- 9-step interactive onboarding tutorial with 3D robot assistant
- Mock data layer with API endpoint annotations for production readiness
