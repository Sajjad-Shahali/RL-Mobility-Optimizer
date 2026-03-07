# MoveWise React Demo

A polished, component-based React demo for **MoveWise** (RL-powered MaaS super-app concept), rebuilt from the original HTML prototype into a cleaner, scalable architecture.

This version focuses on:
- Better UI/UX quality
- Reusable React components
- Responsive behavior for mobile and desktop
- Professional splash intro flow
- Cleaner maintainability for future expansion

---

## 1. Project Overview

MoveWise is a mobility super-app concept that combines:
- Personalized multimodal route planning
- QR tap-in/tap-out trip flow
- Behavioral nudges and gamification
- Rankings and rewards
- Insurance + profile + privacy controls

This repo provides a **demo-ready frontend** experience, preserving core interactions while significantly improving structure and presentation.

---

## 2. Key Features

### UI/UX
- Modern phone-shell demo presentation (desktop-friendly)
- Fully responsive mode for mobile viewports
- Cohesive color system, spacing, and typography
- Clear hierarchy for cards, metrics, CTAs, and navigation
- Toast feedback for user actions
- Loading state in Trips route refresh

### Product Flow
- Bottom navigation with 5 hubs:
  - Home
  - Trips
  - Pay
  - Rankings
  - Profile
- Interactive cards and CTA flows between hubs
- QR journey timeline simulation

### Splash Intro (Required)
- Branded splash screen on startup
- Displays for **exactly 2 seconds**
- Smooth transition to main app
- Includes animated progress bar

### Branding
- Uses your logo file: `public/logo.jpg`
- Logo integrated into:
  - Splash screen
  - Header branding on all major screens
  - QR center visual marker

---

## 3. Tech Stack

- **React 18**
- **Vite 5** (fast dev/build tooling)
- Plain CSS (no heavy UI framework)

Why this stack:
- Fast startup and iteration
- Lightweight bundle
- Easy for hackathon/demo changes
- Clean component separation without complexity

---

## 4. Project Structure

```text
movewise-react/
  index.html
  package.json
  vite.config.js
  public/
    logo.jpg
  src/
    main.jsx
    App.jsx
    data/
      mockData.js
    styles/
      app.css
    components/
      SplashScreen.jsx
      PhoneShell.jsx
      BottomNav.jsx
      HomeScreen.jsx
      TripsScreen.jsx
      PayScreen.jsx
      RankingsScreen.jsx
      ProfileScreen.jsx
      ui/
        Card.jsx
```

### Component Responsibilities

- `App.jsx`
  - App state container
  - Splash timing logic (2s)
  - Active tab routing between hubs
  - Global toast feedback state

- `PhoneShell.jsx`
  - Shared device frame/screen shell
  - Injects screen content + bottom nav

- `BottomNav.jsx`
  - Primary navigation actions
  - Active tab highlighting

- `SplashScreen.jsx`
  - Intro branding and transition animation visuals

- `HomeScreen.jsx`
  - Core landing hub (service tiles, nudge, suggested trip)

- `TripsScreen.jsx`
  - Route cards, loading state, carpool panel, parking/fuel assistant

- `PayScreen.jsx`
  - QR mock, timeline journey states, trip summary metrics

- `RankingsScreen.jsx`
  - Progress KPIs and leaderboard snapshot

- `ProfileScreen.jsx`
  - Insurance summary, preferences, privacy/support actions

- `ui/Card.jsx`
  - Reusable card container primitive used across screens

- `data/mockData.js`
  - Navigation and mock screen data

---

## 5. Design System Notes

### Colors
- Primary blue: `#19547B`
- Sustainability green: `#22783C`
- Payment accent orange: `#DC7814`
- Neutral background/surface tokens in `app.css`

### Typography
- Inter system stack for clarity and consistency

### Patterns
- Rounded cards
- Subtle shadows
- Pill chips for metadata
- Metric triplets for key KPIs
- Primary/secondary CTA button pair

### Motion
- Splash logo float
- Splash loader progress (2s)
- Hover/press response on buttons and tiles
- Toast fade transitions

---

## 6. Accessibility + UX Considerations

- Semantic buttons used for all actions
- Keyboard-focusable controls
- ARIA labels on icon-only controls
- Status feedback via toast (`aria-live`)
- Clear visual contrast for CTA states

---

## 7. Scripts

From `package.json`:

- `npm run dev`
  - Start local development server
- `npm run build`
  - Build production bundle
- `npm run preview`
  - Preview built app locally

---

## 8. How to Run

## Prerequisites
- Node.js 18+ (recommended Node 20 LTS)
- npm (included with Node.js)

## Install and start

```bash
cd D:\hachaton\nexus\movewise-react
npm install
npm run dev
```

Then open the URL shown in terminal (usually `http://localhost:5173`).

## Production build

```bash
cd D:\hachaton\nexus\movewise-react
npm run build
npm run preview
```

---

## 9. Troubleshooting

### Error: `npm is not recognized`
Cause:
- Node.js/npm is not installed or not on PATH.

Fix:
1. Install Node.js LTS from: https://nodejs.org/
2. Reopen terminal
3. Verify:
   ```bash
   node -v
   npm -v
   ```
4. Run install/start commands again.

### Port already in use
Use:
```bash
npm run dev -- --port 5174
```

### Logo not showing
Check file exists:
- `D:\hachaton\nexus\movewise-react\public\logo.jpg`

---

## 10. Current Scope vs Future Scope

Current scope:
- High-quality interactive frontend demo
- Mock data and client-side interactions

Not yet included:
- Backend APIs
- Authentication
- Real payment/QR scanning
- Persistent user state
- Analytics pipeline

---

## 11. Suggested Next Enhancements

1. Add React Router for URL-based navigation.
2. Add Framer Motion for richer page transitions.
3. Add API integration layer (`services/`) + async data hooks.
4. Add form validation and user preference editing UI.
5. Add i18n support (EN/IT).
6. Add dark mode token set.
7. Add tests (Vitest + React Testing Library).

---

## 12. Authoring Notes

This project was rebuilt from the original plain HTML prototype in `D:\hachaton\nexus\Demo\index.html` and aligned to your updated design direction:
- Keep MoveWise as center visual identity
- Merge unnecessary screens
- Make all key menu/buttons interactive
- Maintain demo speed and clarity for presentations
