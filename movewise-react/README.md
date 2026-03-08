# MoveWise Frontend (movewise-react)

React + Vite application for the MoveWise Mobility-as-a-Service demo UI.
This folder contains the full client experience: onboarding, route planning, payment, rankings, profile, insurance, and carpooling.

## Purpose

This app is the user-facing layer of the project. It can run in two modes:
- Mock mode: uses local data in `src/data/mockData.js`.
- API mode: fetches live recommendations from `../rl_engine/api.py`.

## Tech Stack

- React 18
- Vite 5
- Three.js via `@react-three/fiber` and `@react-three/drei`
- Leaflet + OpenStreetMap (`react-leaflet`)
- CSS modules via single app stylesheet (`src/styles/app.css`)
- Desktop packaging with `@yao-pkg/pkg`

## App Flow

1. Consent gate (`ConsentPrompt`) and legal acceptance.
2. Splash screen (`SplashScreen`).
3. First-run tutorial (`OnboardingTutorial`).
4. Main shell (`PhoneShell`) with tab navigation (`BottomNav`).
5. Feature screens:
- `HomeScreen`: overview, adoption journey, quick actions.
- `TripsScreen`: route options and recommendation views.
- `PayScreen`: QR payment and wallet/subscriptions.
- `RankingsScreen`: gamification, badges, rewards.
- `ProfileScreen` / `UserProfileScreen`: preferences and behavior profile.
- `InsuranceScreen`: policy and coverage simulation.
- `CarpoolScreen`: ride matching and map.

## Data Flow

- Current default source: `src/data/mockData.js`.
- To use backend data, point frontend calls to `http://localhost:8000/api/...`.
- API responses are designed to match the mock data shape for minimal UI changes.

## Project Structure

```text
movewise-react/
  src/
    App.jsx
    main.jsx
    styles/app.css
    data/mockData.js
    components/
      HomeScreen.jsx
      TripsScreen.jsx
      PayScreen.jsx
      RankingsScreen.jsx
      ProfileScreen.jsx
      UserProfileScreen.jsx
      InsuranceScreen.jsx
      CarpoolScreen.jsx
      ConsentPrompt.jsx
      SplashScreen.jsx
      OnboardingTutorial.jsx
      PhoneShell.jsx
      BottomNav.jsx
      ui/
      three/
  public/
  server.cjs
  package.json
```

## Setup

From this folder:

```bash
npm install
```

## Development

```bash
npm run dev
```

Default Vite URL: `http://localhost:5173`

## Production Build

```bash
npm run build
npm run preview
```

## Desktop EXE Packaging

This repo uses a lightweight local server + static build package strategy.

```bash
npm run package
```

What this does (from `package.json`):
1. Builds Vite assets into `dist/`.
2. Packages `server.cjs` into `../MoveWise.exe`.
3. Copies `dist/` to `../dist`.

Important:
- `MoveWise.exe` must stay next to `dist/`.
- Run from Windows; browser opens to local server (`http://localhost:3456`).

## Integration With RL Engine

1. Start backend:

```bash
cd ../rl_engine
uvicorn api:app --reload --port 8000
```

2. In frontend, replace mock data reads with fetch calls:
- `GET /api/routes/{trip_type}`
- `GET /api/nudge/select`
- `GET /api/user/profile`
- `POST /api/user/trip`
- `GET /api/carbon`

## Useful Scripts

- `npm run dev`: local development
- `npm run build`: production web build
- `npm run preview`: preview production build
- `npm run package`: build + generate `MoveWise.exe`

## Troubleshooting

- If packaging fails with `EPERM unlink ... MoveWise.exe`, close running `MoveWise.exe` and delete old exe before rerunning.
- If map tiles do not load, check network access for OpenStreetMap.
- If 3D scenes lag, reduce post-processing and heavy geometry counts.

## Notes for Contributors

- Keep UI contracts stable with backend response shapes.
- Prefer small reusable components in `components/ui` and `components/three`.
- Preserve mobile-first behavior (the app is designed around a phone shell layout).
