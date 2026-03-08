"""
Build the final NEXUS 2026 presentation — 6-slide professional PDF-exportable HTML.
Embeds all screenshots as base64 so the file is fully self-contained.
"""

import base64
import os

PRES_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(PRES_DIR, "NEXUS_Final_6slides.html")


def b64(path):
    """Read file and return data URI."""
    with open(os.path.join(PRES_DIR, path), "rb") as f:
        data = f.read()
    ext = path.rsplit(".", 1)[1].lower()
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


# Load images
IMG = {
    "logo": b64("logo.jpg"),
    "home": b64("screenshot/home.png"),
    "route": b64("screenshot/route-planner.png"),
    "payment": b64("screenshot/qr-payment.png"),
    "carpool": b64("screenshot/carpooling.png"),
    "insurance": b64("screenshot/insurance.png"),
    "map": b64("screenshot/map.png"),
    "ali": b64("screenshot/alivaezi.jpg"),
    "sajjad": b64("screenshot/sajjadshahali.jpg"),
    "kiana": b64("screenshot/kianasalimi.jpg"),
}

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MoveWise — NEXUS 2026 Final Presentation</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
/* ═══════════════════════════════════════════════════════════
   GLOBAL RESET & DESIGN SYSTEM
   ═══════════════════════════════════════════════════════════ */
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --emerald:#059669; --emerald-l:rgba(5,150,105,.08); --emerald-b:rgba(5,150,105,.25);
  --cyan:#0891b2; --cyan-l:rgba(8,145,178,.08); --cyan-b:rgba(8,145,178,.25);
  --blue:#2563eb; --blue-l:rgba(37,99,235,.08); --blue-b:rgba(37,99,235,.25);
  --purple:#7c3aed; --purple-l:rgba(124,58,237,.08); --purple-b:rgba(124,58,237,.25);
  --orange:#d97706; --orange-l:rgba(217,119,6,.08); --orange-b:rgba(217,119,6,.25);
  --red:#dc2626;
  --slate-50:#f8fafc; --slate-100:#f1f5f9; --slate-200:#e2e8f0; --slate-300:#cbd5e1;
  --slate-400:#94a3b8; --slate-500:#64748b; --slate-600:#475569; --slate-700:#334155;
  --slate-800:#1e293b; --slate-900:#0f172a;
  --glass:rgba(255,255,255,.72); --glass-b:rgba(148,163,184,.2);
  --r:16px;
  --slide-w:1440px; --slide-h:810px;
}}
html,body{{height:100%;overflow:hidden;background:#0f172a;color:var(--slate-800);
  font-family:'Inter',system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}}

/* ═══ Export Button ═══ */
#exportBtn{{
  position:fixed;top:16px;right:20px;z-index:9999;
  padding:8px 18px;border:1px solid var(--cyan-b);border-radius:10px;
  background:rgba(15,23,42,.8);backdrop-filter:blur(12px);
  color:var(--cyan);font:600 13px 'Inter',sans-serif;cursor:pointer;
  display:flex;align-items:center;gap:7px;transition:all .2s;
}}
#exportBtn:hover{{background:rgba(8,145,178,.15);transform:translateY(-1px)}}
#exportBtn.exporting{{opacity:.5;pointer-events:none}}

/* ═══ Progress & Navigation ═══ */
#progress{{position:fixed;top:0;left:0;height:3px;z-index:100;
  background:linear-gradient(90deg,var(--cyan),var(--emerald));transition:width .45s cubic-bezier(.4,0,.2,1)}}
#nav{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:12px;z-index:100}}
.dot{{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.2);cursor:pointer;transition:all .3s}}
.dot.active{{background:var(--cyan);box-shadow:0 0 12px rgba(8,145,178,.5);transform:scale(1.4)}}
.dot:hover{{background:rgba(255,255,255,.5)}}
#slideNum{{position:fixed;bottom:22px;right:24px;font:500 11px 'JetBrains Mono',monospace;color:rgba(255,255,255,.3);z-index:100}}

/* ═══ Slide Container ═══ */
#slides{{position:relative;width:100%;height:100%}}
.slide{{
  position:absolute;top:50%;left:50%;
  width:var(--slide-w);height:var(--slide-h);
  transform:translate(-50%,-50%);
  opacity:0;pointer-events:none;
  transition:opacity .55s ease;
  overflow:hidden;
}}
.slide.active{{opacity:1;pointer-events:auto}}

/* ═══ Shared Components ═══ */
.glass{{background:var(--glass);border:1px solid var(--glass-b);border-radius:var(--r);backdrop-filter:blur(16px);padding:20px}}
.tag{{display:inline-flex;align-items:center;padding:3px 11px;border-radius:20px;font:700 10px 'Inter',sans-serif;letter-spacing:.06em;text-transform:uppercase}}
.tag-e{{background:var(--emerald-l);color:var(--emerald);border:1px solid var(--emerald-b)}}
.tag-c{{background:var(--cyan-l);color:var(--cyan);border:1px solid var(--cyan-b)}}
.tag-b{{background:var(--blue-l);color:var(--blue);border:1px solid var(--blue-b)}}
.tag-p{{background:var(--purple-l);color:var(--purple);border:1px solid var(--purple-b)}}
.tag-o{{background:var(--orange-l);color:var(--orange);border:1px solid var(--orange-b)}}
.grad-text{{background:linear-gradient(135deg,var(--cyan),var(--emerald));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}

/* phone mockup */
.phone{{width:220px;min-width:220px;border-radius:32px;border:3px solid var(--slate-300);background:#1a1f2e;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.18),0 0 0 1px rgba(255,255,255,.05)}}
.phone img{{width:100%;display:block}}

/* ═══════════════════════════════════════════════════════════
   SLIDE 1 — COVER
   ═══════════════════════════════════════════════════════════ */
#s1{{
  background:linear-gradient(135deg,#f0fdfa 0%,#ecfdf5 30%,#f0f9ff 70%,#faf5ff 100%);
  display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
  padding:40px 60px;
}}
#s1::before{{
  content:'';position:absolute;top:-120px;right:-120px;width:500px;height:500px;
  background:radial-gradient(circle,rgba(8,145,178,.08) 0%,transparent 70%);border-radius:50%;
}}
#s1::after{{
  content:'';position:absolute;bottom:-100px;left:-80px;width:400px;height:400px;
  background:radial-gradient(circle,rgba(5,150,105,.06) 0%,transparent 70%);border-radius:50%;
}}
.s1-badge{{padding:6px 18px;border-radius:20px;border:1px solid var(--glass-b);background:rgba(8,145,178,.05);
  font:700 11px 'Inter',sans-serif;letter-spacing:.14em;color:var(--slate-500);margin-bottom:14px}}
.s1-title{{font:800 64px/1.05 'Space Grotesk',sans-serif;letter-spacing:-.03em;margin-bottom:10px}}
.s1-sub{{font:400 17px/1.6 'Inter',sans-serif;color:var(--slate-500);max-width:640px;margin-bottom:24px}}
.s1-services{{display:flex;gap:14px;margin-bottom:20px;position:relative;z-index:1}}
.s1-svc{{width:100px;padding:14px 8px;border-radius:14px;display:flex;flex-direction:column;align-items:center;gap:6px;
  font:600 10px 'Inter',sans-serif;color:var(--slate-700);border:1px solid var(--glass-b);background:var(--glass);
  transition:transform .3s,box-shadow .3s}}
.s1-svc:hover{{transform:translateY(-4px);box-shadow:0 8px 30px rgba(0,0,0,.07)}}
.s1-svc .ico{{font-size:26px}}
.s1-logo{{width:90px;height:90px;border-radius:22px;object-fit:cover;box-shadow:0 4px 20px rgba(0,0,0,.1);margin-bottom:10px}}
.s1-team{{font:500 13px 'Inter',sans-serif;color:var(--slate-400);margin-top:4px}}

/* ═══════════════════════════════════════════════════════════
   SLIDE 2 — PROBLEM & CONTEXT
   ═══════════════════════════════════════════════════════════ */
#s2{{
  background:linear-gradient(180deg,#ffffff 0%,#f8fafc 100%);
  display:flex;padding:36px 48px;gap:32px;
}}
.s2-left{{flex:1.1;display:flex;flex-direction:column;gap:14px}}
.s2-right{{flex:0.9;display:flex;flex-direction:column;gap:14px}}
.s2-title{{font:800 32px/1.1 'Space Grotesk',sans-serif;letter-spacing:-.02em}}
.persona-card{{display:flex;gap:16px;padding:16px;border-radius:var(--r);background:linear-gradient(135deg,var(--cyan-l),var(--emerald-l));border:1px solid var(--cyan-b)}}
.persona-avatar{{width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,var(--cyan),var(--emerald));display:flex;align-items:center;justify-content:center;font-size:24px;color:#fff;flex-shrink:0}}
.persona-info h4{{font:700 15px 'Inter',sans-serif;color:var(--slate-800)}}
.persona-info p{{font:400 12px/1.5 'Inter',sans-serif;color:var(--slate-600)}}
.pain-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.pain{{padding:12px;border-radius:12px;background:var(--slate-50);border:1px solid var(--glass-b)}}
.pain-icon{{font-size:18px;margin-bottom:4px}}
.pain h5{{font:700 11px 'Inter',sans-serif;color:var(--slate-700);margin-bottom:2px;text-transform:uppercase;letter-spacing:.04em}}
.pain p{{font:400 11px/1.45 'Inter',sans-serif;color:var(--slate-500)}}
.stat-row{{display:flex;gap:10px}}
.stat-box{{flex:1;padding:14px 10px;border-radius:12px;text-align:center;border:1px solid var(--glass-b)}}
.stat-box.red{{background:rgba(220,38,38,.04);border-color:rgba(220,38,38,.15)}}
.stat-box.orange{{background:var(--orange-l);border-color:var(--orange-b)}}
.stat-box.cyan{{background:var(--cyan-l);border-color:var(--cyan-b)}}
.stat-val{{font:800 24px 'Space Grotesk',sans-serif}}
.stat-lbl{{font:500 9px 'Inter',sans-serif;color:var(--slate-500);text-transform:uppercase;letter-spacing:.05em;margin-top:2px}}
.context-card{{padding:14px;border-radius:12px;border:1px solid var(--glass-b);background:var(--slate-50)}}
.context-card h4{{font:700 12px 'Inter',sans-serif;color:var(--slate-700);margin-bottom:6px;text-transform:uppercase;letter-spacing:.04em}}
.context-card p{{font:400 11px/1.5 'Inter',sans-serif;color:var(--slate-500)}}
.competitors-row{{display:flex;gap:8px;margin-top:6px;flex-wrap:wrap}}
.comp{{padding:4px 10px;border-radius:8px;font:600 10px 'Inter',sans-serif;background:var(--slate-100);color:var(--slate-600);border:1px solid var(--glass-b)}}
.comp .x{{color:var(--red);margin-left:4px}}
.od-visual{{padding:14px;border-radius:12px;border:1px solid var(--emerald-b);background:linear-gradient(135deg,rgba(5,150,105,.03),rgba(8,145,178,.03))}}
.od-path{{display:flex;align-items:center;gap:8px;margin:8px 0}}
.od-dot{{width:12px;height:12px;border-radius:50%;border:2px solid}}
.od-line{{flex:1;height:2px;background:repeating-linear-gradient(90deg,var(--slate-300) 0,var(--slate-300) 6px,transparent 6px,transparent 10px)}}
.od-label{{font:700 11px 'Inter',sans-serif;color:var(--slate-700)}}

/* ═══════════════════════════════════════════════════════════
   SLIDE 3 — THE SOLUTION: APP SHOWCASE
   ═══════════════════════════════════════════════════════════ */
#s3{{
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f172a 100%);
  display:flex;padding:36px 48px;gap:24px;color:#e2e8f0;
}}
#s3::before{{
  content:'';position:absolute;top:0;left:0;right:0;bottom:0;
  background:radial-gradient(ellipse at 30% 50%,rgba(8,145,178,.08) 0%,transparent 60%),
             radial-gradient(ellipse at 80% 30%,rgba(5,150,105,.06) 0%,transparent 50%);
}}
.s3-left{{flex:1;display:flex;flex-direction:column;gap:12px;position:relative;z-index:1}}
.s3-phones{{flex:1;display:flex;align-items:center;justify-content:center;gap:16px;position:relative;z-index:1}}
.s3-title{{font:800 30px/1.1 'Space Grotesk',sans-serif;color:#f8fafc}}
.s3-subtitle{{font:400 13px/1.6 'Inter',sans-serif;color:var(--slate-400);max-width:400px}}
.feature-list{{display:flex;flex-direction:column;gap:8px}}
.feat{{display:flex;align-items:flex-start;gap:10px;padding:10px 12px;border-radius:10px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);transition:background .2s}}
.feat:hover{{background:rgba(255,255,255,.07)}}
.feat-icon{{width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}}
.feat-icon.ci{{background:var(--cyan-l);border:1px solid var(--cyan-b)}}
.feat-icon.ei{{background:var(--emerald-l);border:1px solid var(--emerald-b)}}
.feat-icon.pi{{background:var(--purple-l);border:1px solid var(--purple-b)}}
.feat-icon.oi{{background:var(--orange-l);border:1px solid var(--orange-b)}}
.feat-icon.bi{{background:var(--blue-l);border:1px solid var(--blue-b)}}
.feat h5{{font:700 12px 'Inter',sans-serif;color:#f1f5f9;margin-bottom:2px}}
.feat p{{font:400 10.5px/1.45 'Inter',sans-serif;color:var(--slate-400)}}
.phone-dark{{width:185px;min-width:185px;border-radius:28px;border:3px solid var(--slate-700);background:#0f172a;overflow:hidden;
  box-shadow:0 20px 60px rgba(0,0,0,.4),0 0 80px rgba(8,145,178,.06)}}
.phone-dark img{{width:100%;display:block}}

/* ═══════════════════════════════════════════════════════════
   SLIDE 4 — TECHNICAL ARCHITECTURE (RL + Transport Theory)
   ═══════════════════════════════════════════════════════════ */
#s4{{
  background:linear-gradient(180deg,#ffffff 0%,#f0fdfa 100%);
  display:flex;padding:36px 48px;gap:28px;
}}
.s4-left{{flex:1;display:flex;flex-direction:column;gap:12px}}
.s4-right{{flex:1;display:flex;flex-direction:column;gap:12px}}
.s4-title{{font:800 28px/1.1 'Space Grotesk',sans-serif;letter-spacing:-.02em}}
.arch-block{{padding:12px 14px;border-radius:12px;border:1px solid var(--glass-b);background:var(--slate-50)}}
.arch-block h5{{font:700 11px 'Inter',sans-serif;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}}
.arch-block p,.arch-block li{{font:400 10.5px/1.5 'Inter',sans-serif;color:var(--slate-600)}}
.arch-block ul{{padding-left:14px}}
.arch-block li{{margin-bottom:2px}}
.formula{{font:500 12px 'JetBrains Mono',monospace;color:var(--cyan);background:rgba(8,145,178,.05);padding:8px 12px;border-radius:8px;border:1px solid var(--cyan-b);margin:6px 0;overflow-x:auto;white-space:nowrap}}
.theory-flow{{display:flex;align-items:center;gap:6px;margin:8px 0;flex-wrap:wrap}}
.theory-step{{padding:6px 12px;border-radius:8px;font:700 10px 'Inter',sans-serif;text-transform:uppercase;letter-spacing:.03em}}
.theory-arrow{{font-size:14px;color:var(--slate-400)}}
.maas-levels{{display:flex;gap:6px;margin-top:6px}}
.maas-lvl{{flex:1;padding:8px 4px;border-radius:8px;text-align:center;font:600 9px 'Inter',sans-serif;border:1px solid var(--glass-b)}}
.maas-lvl.active{{border-color:var(--emerald-b);background:var(--emerald-l);color:var(--emerald)}}
.maas-lvl.inactive{{background:var(--slate-50);color:var(--slate-400)}}
.gc-table{{width:100%;border-collapse:collapse;font:400 10px 'Inter',sans-serif;margin-top:4px}}
.gc-table th{{text-align:left;font-weight:700;font-size:9px;text-transform:uppercase;letter-spacing:.05em;color:var(--slate-500);padding:4px 6px;border-bottom:1px solid var(--slate-200)}}
.gc-table td{{padding:4px 6px;border-bottom:1px solid var(--slate-100);color:var(--slate-600)}}
.gc-table tr:last-child td{{border-bottom:none}}
.highlight{{font-weight:700;color:var(--emerald)}}

/* ═══════════════════════════════════════════════════════════
   SLIDE 5 — ENVIRONMENTAL IMPACT & MEASURABLE BENEFITS
   ═══════════════════════════════════════════════════════════ */
#s5{{
  background:linear-gradient(135deg,#ecfdf5 0%,#f0fdfa 40%,#f0f9ff 100%);
  display:flex;padding:36px 48px;gap:28px;
}}
.s5-left{{flex:1;display:flex;flex-direction:column;gap:12px}}
.s5-right{{flex:1;display:flex;flex-direction:column;gap:12px}}
.s5-title{{font:800 28px/1.1 'Space Grotesk',sans-serif;letter-spacing:-.02em}}
.impact-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.impact-card{{padding:16px;border-radius:14px;text-align:center;border:1px solid var(--glass-b);background:rgba(255,255,255,.7)}}
.impact-card .val{{font:800 32px 'Space Grotesk',sans-serif;margin-bottom:2px}}
.impact-card .lbl{{font:500 10px 'Inter',sans-serif;color:var(--slate-500);text-transform:uppercase;letter-spacing:.05em}}
.impact-card .sub{{font:400 10px 'Inter',sans-serif;color:var(--slate-400);margin-top:3px}}
.adoption-phases{{display:flex;flex-direction:column;gap:6px}}
.phase{{display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:10px;border:1px solid var(--glass-b);background:rgba(255,255,255,.5)}}
.phase-num{{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:800 13px 'Space Grotesk',sans-serif;color:#fff;flex-shrink:0}}
.phase h5{{font:700 11px 'Inter',sans-serif;color:var(--slate-700)}}
.phase p{{font:400 10px/1.4 'Inter',sans-serif;color:var(--slate-500)}}
.rl-results{{padding:14px;border-radius:12px;background:linear-gradient(135deg,rgba(8,145,178,.05),rgba(5,150,105,.05));border:1px solid var(--emerald-b)}}
.rl-results h4{{font:700 12px 'Inter',sans-serif;color:var(--slate-700);margin-bottom:8px;text-transform:uppercase;letter-spacing:.04em}}
.rl-bar{{display:flex;align-items:center;gap:8px;margin-bottom:6px}}
.rl-bar-label{{width:80px;font:500 10px 'Inter',sans-serif;color:var(--slate-600);text-align:right}}
.rl-bar-track{{flex:1;height:14px;border-radius:7px;background:var(--slate-200);overflow:hidden;position:relative}}
.rl-bar-fill{{height:100%;border-radius:7px;display:flex;align-items:center;justify-content:flex-end;padding-right:6px;font:700 9px 'Inter',sans-serif;color:#fff}}
.scale-section{{padding:14px;border-radius:12px;border:1px solid var(--glass-b);background:rgba(255,255,255,.6)}}
.scale-section h4{{font:700 12px 'Inter',sans-serif;color:var(--slate-700);margin-bottom:6px;text-transform:uppercase;letter-spacing:.04em}}
.scale-row{{display:flex;gap:6px;margin-bottom:4px}}
.scale-item{{flex:1;padding:6px;border-radius:8px;text-align:center;background:var(--slate-50);border:1px solid var(--glass-b)}}
.scale-item .sv{{font:800 16px 'Space Grotesk',sans-serif;color:var(--emerald)}}
.scale-item .sl{{font:400 8px 'Inter',sans-serif;color:var(--slate-500);text-transform:uppercase;letter-spacing:.03em;margin-top:1px}}

/* ═══════════════════════════════════════════════════════════
   SLIDE 6 — TEAM & CONCLUSION
   ═══════════════════════════════════════════════════════════ */
#s6{{
  background:linear-gradient(135deg,#f8fafc 0%,#f0f9ff 50%,#faf5ff 100%);
  display:flex;padding:36px 48px;gap:28px;
}}
.s6-left{{flex:1.2;display:flex;flex-direction:column;gap:14px}}
.s6-right{{flex:0.8;display:flex;flex-direction:column;gap:14px}}
.s6-title{{font:800 28px/1.1 'Space Grotesk',sans-serif;letter-spacing:-.02em}}
.team-grid{{display:flex;gap:14px}}
.team-member{{flex:1;padding:16px 12px;border-radius:14px;text-align:center;border:1px solid var(--glass-b);background:rgba(255,255,255,.7);transition:transform .3s}}
.team-member:hover{{transform:translateY(-3px)}}
.team-photo{{width:64px;height:64px;border-radius:50%;object-fit:cover;margin:0 auto 8px;border:2px solid var(--slate-200);display:block}}
.team-member h5{{font:700 13px 'Inter',sans-serif;color:var(--slate-800);margin-bottom:2px}}
.team-member .role{{font:500 10px 'Inter',sans-serif;color:var(--cyan);text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px}}
.team-member p{{font:400 10px/1.45 'Inter',sans-serif;color:var(--slate-500);text-align:left}}
.conclusion-card{{padding:16px;border-radius:14px;background:linear-gradient(135deg,rgba(8,145,178,.06),rgba(5,150,105,.06));border:1px solid var(--emerald-b)}}
.conclusion-card h4{{font:700 13px 'Inter',sans-serif;color:var(--slate-800);margin-bottom:8px}}
.conclusion-list{{list-style:none;padding:0}}
.conclusion-list li{{display:flex;align-items:flex-start;gap:8px;margin-bottom:6px;font:400 11px/1.5 'Inter',sans-serif;color:var(--slate-600)}}
.conclusion-list .check{{color:var(--emerald);font-weight:700;font-size:13px;flex-shrink:0}}
.future-row{{display:flex;gap:8px;flex-wrap:wrap}}
.future-tag{{padding:6px 12px;border-radius:10px;font:600 10px 'Inter',sans-serif;background:var(--slate-100);color:var(--slate-600);border:1px solid var(--glass-b)}}
.s6-footer{{text-align:center;font:500 11px 'Inter',sans-serif;color:var(--slate-400);margin-top:auto;padding-top:8px}}
.s6-logo{{width:48px;height:48px;border-radius:12px;object-fit:cover;margin:0 auto 6px;display:block}}

/* ═══ Animations ═══ */
@keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes slideRight{{from{{opacity:0;transform:translateX(-30px)}}to{{opacity:1;transform:translateX(0)}}}}
@keyframes scaleIn{{from{{opacity:0;transform:scale(.9)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes pulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.05)}}}}
.slide.active .anim-1{{animation:fadeUp .6s ease .1s both}}
.slide.active .anim-2{{animation:fadeUp .6s ease .25s both}}
.slide.active .anim-3{{animation:fadeUp .6s ease .4s both}}
.slide.active .anim-4{{animation:fadeUp .6s ease .55s both}}
.slide.active .anim-5{{animation:fadeIn .6s ease .3s both}}
.slide.active .anim-slide{{animation:slideRight .6s ease .3s both}}
.slide.active .anim-scale{{animation:scaleIn .6s ease .35s both}}
</style>
</head>
<body>

<!-- Export Button -->
<button id="exportBtn" onclick="exportPDF()">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
  Export PDF
</button>

<!-- Progress Bar -->
<div id="progress" style="width:16.67%"></div>

<!-- Navigation Dots -->
<div id="nav"></div>
<div id="slideNum">1 / 6</div>

<!-- ═══════════════════════════════════════════════════════════
     SLIDE 1 — COVER
     ═══════════════════════════════════════════════════════════ -->
<div id="slides">
<div class="slide active" id="s1">
  <div class="s1-badge anim-1">NEXUS 2026 &mdash; POLITECNICO DI TORINO</div>
  <img src="{IMG['logo']}" class="s1-logo anim-2" alt="MoveWise Logo">
  <h1 class="s1-title anim-2"><span class="grad-text">MoveWise</span></h1>
  <p class="s1-sub anim-3">AI-Powered Mobility-as-a-Service &mdash; Transforming Giuseppe&rsquo;s commute through Reinforcement Learning, Generalised Cost optimisation, and behavioural nudging.</p>
  <div class="s1-services anim-4">
    <div class="s1-svc"><div class="ico">🚆</div>Route Planner</div>
    <div class="s1-svc"><div class="ico">📱</div>QR Payment</div>
    <div class="s1-svc"><div class="ico">🚗</div>Carpooling</div>
    <div class="s1-svc"><div class="ico">🏆</div>Gamification</div>
    <div class="s1-svc"><div class="ico">🛡</div>Insurance</div>
    <div class="s1-svc"><div class="ico">🧠</div>RL Engine</div>
  </div>
  <div class="s1-team anim-4">Ali Vaezi &nbsp;&bull;&nbsp; Sajjad Shahali &nbsp;&bull;&nbsp; Kiana Salimi</div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     SLIDE 2 — PROBLEM ANALYSIS & CONTEXT
     ═══════════════════════════════════════════════════════════ -->
<div class="slide" id="s2">
  <div class="s2-left">
    <span class="tag tag-c anim-1">Problem Analysis</span>
    <h2 class="s2-title anim-1">The Mobility Challenge:<br><span class="grad-text">Giuseppe&rsquo;s Daily Struggle</span></h2>

    <div class="persona-card anim-2">
      <div class="persona-avatar">👨‍⚕️</div>
      <div class="persona-info">
        <h4>Giuseppe, 23 &mdash; Medical Student</h4>
        <p>Lives in <strong>Caselle Torinese</strong>, studies in <strong>Orbassano</strong>. Commutes 3x/week as car passenger (45 min). Perceives cost as &euro;60/mo but true cost is &euro;510/mo. Wants 20-min time reduction and 30% pollution cut.</p>
      </div>
    </div>

    <div class="pain-grid anim-3">
      <div class="pain"><div class="pain-icon">⏱</div><h5>Time Waste</h5><p>45 min each way, no time for studying during commute</p></div>
      <div class="pain"><div class="pain-icon">💸</div><h5>Hidden Costs</h5><p>Perceives &euro;60/mo but true cost is &euro;510/mo (fuel + depreciation + insurance + parking)</p></div>
      <div class="pain"><div class="pain-icon">🌫</div><h5>Pollution</h5><p>4.2 kg CO&#8322; per trip &mdash; over 1 tonne/year per commuter</p></div>
      <div class="pain"><div class="pain-icon">🔒</div><h5>Car Dependency</h5><p>No integrated alternative &mdash; fragmented apps, separate tickets, habit inertia</p></div>
    </div>

    <div class="stat-row anim-4">
      <div class="stat-box red"><div class="stat-val" style="color:var(--red)">72%</div><div class="stat-lbl">Drive alone in Torino</div></div>
      <div class="stat-box orange"><div class="stat-val" style="color:var(--orange)">&euro;270B</div><div class="stat-lbl">EU congestion cost/yr</div></div>
      <div class="stat-box cyan"><div class="stat-val" style="color:var(--cyan)">30%</div><div class="stat-lbl">EU GHG from transport</div></div>
    </div>
  </div>

  <div class="s2-right">
    <div class="od-visual anim-slide">
      <h4 style="font:700 11px 'Inter',sans-serif;color:var(--slate-700);text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">📍 Origin &mdash; Destination Corridor</h4>
      <div class="od-path">
        <div class="od-dot" style="border-color:var(--emerald);background:var(--emerald-l)"></div>
        <div class="od-label">Caselle Torinese</div>
        <div class="od-line"></div>
        <div class="od-label">Orbassano</div>
        <div class="od-dot" style="border-color:var(--blue);background:var(--blue-l)"></div>
      </div>
      <p style="font:400 10px/1.5 'Inter',sans-serif;color:var(--slate-500)">~30 km suburban corridor &bull; Limited direct PT connections &bull; Car-dependent commuters &bull; O-D pair in Torino metropolitan area</p>
    </div>

    <div class="context-card anim-slide">
      <h4>🔍 Why Existing Solutions Fail</h4>
      <p>Traditional apps (Google Maps, Moovit) solve <strong>route planning only</strong>. They don&rsquo;t address: habit inertia, cost illusions, information asymmetry, fragmented ticketing, or lack of positive reinforcement.</p>
      <div class="competitors-row" style="margin-top:8px">
        <div class="comp">Google Maps <span class="x">&mdash; no nudges</span></div>
        <div class="comp">Moovit <span class="x">&mdash; no payment</span></div>
        <div class="comp">CityMapper <span class="x">&mdash; no RL</span></div>
      </div>
    </div>

    <div class="context-card anim-slide">
      <h4>🌍 Context: Transport Demand Theory</h4>
      <p>In the classical <strong>4-step model</strong> (Generation &rarr; Distribution &rarr; Mode Choice &rarr; Assignment), MoveWise targets <strong>Step 3: Mode Choice</strong>, replacing the Multinomial Logit (MNL) with a DQN agent that avoids the IIA limitation and learns personalised weights.</p>
    </div>

    <div class="context-card anim-slide">
      <h4>⚖ Giuseppe&rsquo;s Requirements</h4>
      <p style="margin-bottom:4px"><span style="color:var(--emerald);font-weight:700">\u2713</span> Reduce travel time by 20 min &nbsp; <span style="color:var(--emerald);font-weight:700">\u2713</span> Stay within &euro;75/mo budget</p>
      <p><span style="color:var(--emerald);font-weight:700">\u2713</span> Cut CO&#8322; by &ge;30% &nbsp; <span style="color:var(--emerald);font-weight:700">\u2713</span> Integrated, sustainable, safe service</p>
    </div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     SLIDE 3 — THE SOLUTION: APP SHOWCASE
     ═══════════════════════════════════════════════════════════ -->
<div class="slide" id="s3">
  <div class="s3-left">
    <span class="tag tag-e anim-1">The Solution</span>
    <h2 class="s3-title anim-1">MoveWise: <span style="color:var(--cyan)">MaaS Super-App</span></h2>
    <p class="s3-subtitle anim-2">A single platform integrating all transport modes with AI-powered personalisation, unified payment, and behavioural nudging &mdash; operating at <strong style="color:var(--cyan)">MaaS Level 3&ndash;4</strong>.</p>

    <div class="feature-list anim-3">
      <div class="feat">
        <div class="feat-icon ci">📊</div>
        <div><h5>RL-Powered Route Ranking</h5><p>DQN agent ranks routes by personalised Generalised Cost. 4 tabs: Best for You, Cheapest, Fastest, Greenest. Replaces MNL with adaptive learning.</p></div>
      </div>
      <div class="feat">
        <div class="feat-icon ei">📱</div>
        <div><h5>QR Tap-In/Tap-Out Payment</h5><p>One QR code across all modes (bus, train, e-scooter, bike). Digital wallet, 3 subscription tiers, expandable journey timeline.</p></div>
      </div>
      <div class="feat">
        <div class="feat-icon pi">🚗</div>
        <div><h5>Peer-to-Peer Carpooling</h5><p>Ride matching among university students. Live OpenStreetMap, route overlap %, cost splitting, safety ratings. Interactive map for O/D selection.</p></div>
      </div>
      <div class="feat">
        <div class="feat-icon oi">🎮</div>
        <div><h5>Gamification & Nudging</h5><p>Green Points, leaderboard, challenges, badges. Behavioural nudges: social proof, loss framing, commitment devices, streak rewards (Prospect Theory \u03BC=2.25).</p></div>
      </div>
      <div class="feat">
        <div class="feat-icon bi">🛡</div>
        <div><h5>Insurance-Linked Incentives</h5><p>Use PT 3+ days/week \u2192 15% lower car insurance premium. IVASS-compliant, GDPR anonymised via UnipolSai partnership. True Cost Calculator.</p></div>
      </div>
    </div>
  </div>

  <div class="s3-phones">
    <div class="phone-dark anim-scale" style="transform:rotate(-3deg);margin-top:30px"><img src="{IMG['home']}" alt="Home Screen"></div>
    <div class="phone-dark anim-scale" style="z-index:2;transform:scale(1.08)"><img src="{IMG['route']}" alt="Route Planner"></div>
    <div class="phone-dark anim-scale" style="transform:rotate(3deg);margin-top:30px"><img src="{IMG['payment']}" alt="QR Payment"></div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     SLIDE 4 — TECHNICAL ARCHITECTURE
     ═══════════════════════════════════════════════════════════ -->
<div class="slide" id="s4">
  <div class="s4-left">
    <span class="tag tag-b anim-1">Technical Architecture</span>
    <h2 class="s4-title anim-1">How It Works:<br><span class="grad-text">RL + Transport Theory</span></h2>

    <div class="arch-block anim-2" style="border-color:var(--cyan-b)">
      <h5 style="color:var(--cyan)">🧠 Deep Q-Network (DQN) Agent</h5>
      <ul>
        <li><strong>State</strong> (18-dim): habit strength, eco-sensitivity, loss aversion, adoption phase, weather, trip type, green streak, CO&#8322; saved, satisfaction&hellip;</li>
        <li><strong>Action</strong>: 7 transport modes &times; 7 nudge types = <strong>49 compound actions</strong></li>
        <li><strong>Reward</strong>: &minus;[w&#8321;&middot;GC + w&#8322;&middot;CO&#8322; + w&#8323;&middot;\u03A8<sub>behavior</sub> + w&#8324;&middot;\u03A6<sub>constraints</sub>] + w&#8325;&middot;Revenue</li>
      </ul>
    </div>

    <div class="arch-block anim-3" style="border-color:var(--emerald-b)">
      <h5 style="color:var(--emerald)">📐 Generalised Cost Framework</h5>
      <div class="formula">GC = VOT&middot;t + c + \u03C4&middot;transfers + (1&minus;r)&middot;\u03C1 + (1&minus;\u03BA)&middot;\u03C6 + \u03C9&middot;walk + \u03B3<sub>eco</sub>&middot;CO&#8322;&middot;SCC</div>
      <p><strong>Context-dependent VOT:</strong> Car passenger 3.7 &euro;/h (can study) vs. driver 10.0 &euro;/h (cannot) &mdash; reflecting <em>derived demand</em> theory.</p>
      <p><strong>Prospect Theory:</strong> Switching losses weighted \u03BC=2.25&times; (Kahneman & Tversky, 1979) &mdash; captures why car users resist change.</p>
    </div>

    <div class="arch-block anim-4" style="border-color:var(--purple-b)">
      <h5 style="color:var(--purple)">👥 HUR Behavioural Model</h5>
      <p><strong>H</strong>abit (H&#8320;=0.70, decays: H<sub>t</sub>=H&#8320;&middot;e<sup>&minus;\u03B1t</sup>) + <strong>U</strong>tility maximisation + bounded <strong>R</strong>ationality (regret minimisation, status quo bias). Goes beyond standard Random Utility Theory.</p>
    </div>
  </div>

  <div class="s4-right">
    <div class="arch-block anim-slide" style="border-color:var(--blue-b)">
      <h5 style="color:var(--blue)">📚 Grounded in Transport Theory</h5>
      <div class="theory-flow">
        <span class="theory-step" style="background:var(--cyan-l);color:var(--cyan)">Generation</span>
        <span class="theory-arrow">\u2192</span>
        <span class="theory-step" style="background:var(--blue-l);color:var(--blue)">Distribution</span>
        <span class="theory-arrow">\u2192</span>
        <span class="theory-step" style="background:var(--emerald-l);color:var(--emerald);border:2px solid var(--emerald)">Mode Choice \u2190 RL</span>
        <span class="theory-arrow">\u2192</span>
        <span class="theory-step" style="background:var(--purple-l);color:var(--purple)">Assignment</span>
      </div>
      <p style="margin-top:6px">Our DQN <strong>replaces the MNL</strong> (Multinomial Logit) in Step 3. Unlike MNL, it has <strong>no IIA limitation</strong> (red bus/blue bus problem), learns personalised weights, and adapts from digital Revealed Preference data (QR taps).</p>
    </div>

    <div class="arch-block anim-slide">
      <h5 style="color:var(--orange)">📶 MaaS Integration Levels (Sochor et al., 2018)</h5>
      <div class="maas-levels">
        <div class="maas-lvl inactive">L0<br><span style="font-size:7px">None</span></div>
        <div class="maas-lvl inactive">L1<br><span style="font-size:7px">Info</span></div>
        <div class="maas-lvl active">L2<br><span style="font-size:7px">Book+Pay</span></div>
        <div class="maas-lvl active" style="border-width:2px">L3<br><span style="font-size:7px">Bundles</span></div>
        <div class="maas-lvl active" style="border-width:2px;border-color:var(--cyan-b);background:var(--cyan-l);color:var(--cyan)">L4<br><span style="font-size:7px">Policy</span></div>
      </div>
      <p style="margin-top:6px">MoveWise at <strong>Level 3&ndash;4</strong>: subscription bundles + insurance-linked policy integration. Inspired by <strong>UbiGo</strong> (Gothenburg), <strong>Whim</strong> (Helsinki), <strong>myCicero</strong> (Italy).</p>
    </div>

    <div class="arch-block anim-slide">
      <h5 style="color:var(--slate-700)">💻 Technology Stack</h5>
      <table class="gc-table">
        <tr><th>Layer</th><th>Technology</th></tr>
        <tr><td>Frontend</td><td>React 18 + Vite + Three.js + Leaflet</td></tr>
        <tr><td>RL Engine</td><td>Python + PyTorch (Double DQN)</td></tr>
        <tr><td>API</td><td>FastAPI + Uvicorn (REST)</td></tr>
        <tr><td>Maps</td><td>Leaflet + OpenStreetMap + Nominatim</td></tr>
        <tr><td>CI/CD</td><td>GitHub Actions + Docker</td></tr>
        <tr><td>Privacy</td><td>GDPR consent, pseudonymisation, encryption</td></tr>
      </table>
    </div>

    <div class="arch-block anim-slide" style="border-color:var(--orange-b)">
      <h5 style="color:var(--orange)">📊 Mode Comparison (GC-Ranked)</h5>
      <table class="gc-table">
        <tr><th>Mode</th><th>Time</th><th>CO&#8322;</th><th>Cost/mo</th><th>CO&#8322; Cut</th></tr>
        <tr><td>Car (passenger)</td><td>45 min</td><td>4.20 kg</td><td>&euro;60</td><td>&mdash;</td></tr>
        <tr><td>E-Scooter+Train+Walk</td><td>30 min</td><td>0.84 kg</td><td>&euro;55</td><td class="highlight">&minus;80%</td></tr>
        <tr><td>Carpool</td><td>29 min</td><td>2.10 kg</td><td>&euro;50</td><td class="highlight">&minus;50%</td></tr>
        <tr><td>Walk+Train+Bike</td><td>40 min</td><td>0.21 kg</td><td>&euro;30</td><td class="highlight">&minus;95%</td></tr>
      </table>
    </div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     SLIDE 5 — ENVIRONMENTAL IMPACT & MEASURABLE RESULTS
     ═══════════════════════════════════════════════════════════ -->
<div class="slide" id="s5">
  <div class="s5-left">
    <span class="tag tag-e anim-1">Environmental Impact</span>
    <h2 class="s5-title anim-1">Measurable Benefits:<br><span class="grad-text">Verified by RL Simulation</span></h2>

    <div class="impact-grid anim-2">
      <div class="impact-card"><div class="val" style="color:var(--emerald)">42%</div><div class="lbl">CO&#8322; Reduction</div><div class="sub">Target was 30% &mdash; exceeded</div></div>
      <div class="impact-card"><div class="val" style="color:var(--cyan)">15 min</div><div class="lbl">Time Saved / Trip</div><div class="sub">Best mode: 29 min vs 45 min car</div></div>
      <div class="impact-card"><div class="val" style="color:var(--orange)">&euro;5,460</div><div class="lbl">Saved / Year</div><div class="sub">True car cost &euro;510 vs PT &euro;55/mo</div></div>
      <div class="impact-card"><div class="val" style="color:var(--purple)">84%</div><div class="lbl">Green Trip Ratio</div><div class="sub">After RL training (200 episodes)</div></div>
    </div>

    <div class="rl-results anim-3">
      <h4>🤖 RL Training Results (200 Episodes)</h4>
      <div class="rl-bar"><div class="rl-bar-label">Green Ratio</div><div class="rl-bar-track"><div class="rl-bar-fill" style="width:84%;background:linear-gradient(90deg,var(--emerald),var(--cyan))">84%</div></div></div>
      <div class="rl-bar"><div class="rl-bar-label">Habit Decay</div><div class="rl-bar-track"><div class="rl-bar-fill" style="width:90%;background:linear-gradient(90deg,var(--blue),var(--purple))">0.70 \u2192 0.07</div></div></div>
      <div class="rl-bar"><div class="rl-bar-label">Phase Reached</div><div class="rl-bar-track"><div class="rl-bar-fill" style="width:100%;background:linear-gradient(90deg,var(--orange),var(--red))">Phase 3/3</div></div></div>
      <div class="rl-bar"><div class="rl-bar-label">Budget</div><div class="rl-bar-track"><div class="rl-bar-fill" style="width:68%;background:linear-gradient(90deg,var(--cyan),var(--emerald))">&euro;51/mo (\u2264 &euro;75)</div></div></div>
    </div>

    <div class="arch-block anim-4" style="border-color:var(--emerald-b)">
      <h5 style="color:var(--emerald)">🌿 Sustainability Approach: Multi-Pronged</h5>
      <p><strong>1) Modal Shift</strong> via RL nudging &bull; <strong>2) True Cost Transparency</strong> (loss framing) &bull; <strong>3) Insurance-linked PT incentives</strong> (actuarially justified) &bull; <strong>4) Gamification</strong> (social norms) &bull; <strong>5) Phased Adoption</strong> (gradual behaviour change)</p>
    </div>
  </div>

  <div class="s5-right">
    <div class="adoption-phases anim-slide">
      <div style="font:700 12px 'Inter',sans-serif;color:var(--slate-700);text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">📈 Giuseppe&rsquo;s Adoption Journey</div>
      <div class="phase"><div class="phase-num" style="background:var(--slate-400)">0</div><div><h5>Onboarding</h5><p>Installs via insurance/parking services. Sees True Cost Calculator. Perceived &euro;60 vs actual &euro;510.</p></div></div>
      <div class="phase"><div class="phase-num" style="background:var(--cyan)">1</div><div><h5>Park & Ride</h5><p>Drives to P&R, takes train. &minus;50% CO&#8322;. &euro;45/mo. Still has car safety net. Loss framing nudge triggers.</p></div></div>
      <div class="phase"><div class="phase-num" style="background:var(--emerald)">2</div><div><h5>Full Multimodal</h5><p>E-Scooter \u2192 Train \u2192 Walk. &minus;80% CO&#8322;. 30 min door-to-door. Green Points accelerate. Habit < 0.50.</p></div></div>
      <div class="phase"><div class="phase-num" style="background:linear-gradient(135deg,var(--emerald),var(--cyan))">3</div><div><h5>Community Champion</h5><p>Carpools + PT. Leaderboard rank. Insurance premium &minus;15%. Nudges others. Habit = 0.07.</p></div></div>
    </div>

    <div class="scale-section anim-slide">
      <h4>📊 Scaled Impact (1,000 Users)</h4>
      <div class="scale-row">
        <div class="scale-item"><div class="sv">1,000t</div><div class="sl">CO&#8322; Saved/yr</div></div>
        <div class="scale-item"><div class="sv">&euro;5.5M</div><div class="sl">Money Saved/yr</div></div>
        <div class="scale-item"><div class="sv">130K</div><div class="sl">Hours Saved/yr</div></div>
      </div>
      <div class="scale-row" style="margin-top:6px">
        <div class="scale-item"><div class="sv">1,000</div><div class="sl">Cars Off Road</div></div>
        <div class="scale-item"><div class="sv">18M</div><div class="sl">Green Points</div></div>
        <div class="scale-item"><div class="sv">\u221E</div><div class="sl">Scalable Cities</div></div>
      </div>
    </div>

    <div class="arch-block anim-slide" style="border-color:var(--blue-b)">
      <h5 style="color:var(--blue)">⚖ Regulatory Compliance</h5>
      <p><strong>GDPR</strong> (Art. 6,7,13,17,20) &bull; <strong>French LOM Law</strong> (2019) for MaaS framework &bull; <strong>IVASS</strong> insurance intermediary &bull; <strong>EEA 2024</strong> emission factors &bull; <strong>Privacy by Design</strong> with pseudonymisation</p>
    </div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     SLIDE 6 — TEAM CONTRIBUTIONS & CONCLUSION
     ═══════════════════════════════════════════════════════════ -->
<div class="slide" id="s6">
  <div class="s6-left">
    <span class="tag tag-p anim-1">Team & Conclusion</span>
    <h2 class="s6-title anim-1">Built by Three Disciplines,<br><span class="grad-text">One Shared Vision</span></h2>

    <div class="team-grid anim-2">
      <div class="team-member">
        <img src="{IMG['ali']}" class="team-photo" alt="Ali Vaezi">
        <h5>Ali Vaezi</h5>
        <div class="role">Transport & AI Engineer</div>
        <p>\u2022 RL engine architecture (DQN + GC framework)<br>\u2022 Transport theory alignment (4-step, MNL, Wardrop)<br>\u2022 Professional repo: CI/CD, Docker, documentation<br>\u2022 Academic formulation (v3 LaTeX paper)<br>\u2022 GitHub Pages deployment</p>
      </div>
      <div class="team-member">
        <img src="{IMG['sajjad']}" class="team-photo" alt="Sajjad Shahali">
        <h5>Sajjad Shahali</h5>
        <div class="role">Full-Stack Developer</div>
        <p>\u2022 React + Three.js frontend development<br>\u2022 Interactive Leaflet map integration<br>\u2022 LocationPickerMap with geocoding<br>\u2022 TimeScrollPicker component<br>\u2022 CSS animations & responsive design<br>\u2022 Windows .exe build</p>
      </div>
      <div class="team-member">
        <img src="{IMG['kiana']}" class="team-photo" alt="Kiana Salimi">
        <h5>Kiana Salimi</h5>
        <div class="role">UX & Presentation Design</div>
        <p>\u2022 Visual presentation design<br>\u2022 User experience research<br>\u2022 Pitch deck creation and refinement<br>\u2022 App screenshot curation<br>\u2022 Presentation materials & sharing</p>
      </div>
    </div>

    <div class="conclusion-card anim-3">
      <h4>✅ Giuseppe&rsquo;s Problem: Solved</h4>
      <ul class="conclusion-list">
        <li><span class="check">\u2713</span><strong>Time:</strong> 29&ndash;30 min multimodal vs 45 min car = <strong>15 min saved</strong> per trip</li>
        <li><span class="check">\u2713</span><strong>Cost:</strong> &euro;51/mo average vs &euro;510/mo true car cost = <strong>&euro;5,460/yr saved</strong></li>
        <li><span class="check">\u2713</span><strong>CO&#8322;:</strong> 42% reduction (target 30%) = <strong>1 tonne/yr per user</strong></li>
        <li><span class="check">\u2713</span><strong>Integration:</strong> MaaS Level 3&ndash;4 with unified QR payment, subscriptions, insurance</li>
        <li><span class="check">\u2713</span><strong>Behaviour:</strong> Habit 0.70 \u2192 0.07 through RL nudging (Prospect Theory + gamification)</li>
      </ul>
    </div>
  </div>

  <div class="s6-right">
    <div class="arch-block anim-slide" style="border-color:var(--emerald-b)">
      <h5 style="color:var(--emerald)">🚀 Future Scalability</h5>
      <div class="future-row">
        <div class="future-tag">Multi-city deployment</div>
        <div class="future-tag">GTFS real-time</div>
        <div class="future-tag">Autonomous vehicles</div>
        <div class="future-tag">Carbon credit marketplace</div>
        <div class="future-tag">Demand-responsive transit</div>
        <div class="future-tag">Accessibility (universal service)</div>
        <div class="future-tag">A/B testing nudges</div>
        <div class="future-tag">Open API for operators</div>
      </div>
    </div>

    <div class="arch-block anim-slide" style="border-color:var(--purple-b)">
      <h5 style="color:var(--purple)">🎯 Why MoveWise Wins</h5>
      <p>MoveWise is not just another route planner. It is a <strong>complete behavioural intervention platform</strong> grounded in transport engineering theory:</p>
      <ul style="margin-top:6px">
        <li><strong>Creativity:</strong> First MaaS app using RL for personalised mode choice + insurance integration</li>
        <li><strong>Implementability:</strong> Working prototype with React frontend + Python RL backend + Docker + CI/CD</li>
        <li><strong>Theory:</strong> 4-step model, Generalised Cost, Prospect Theory, Wardrop, MaaS levels, GDPR</li>
        <li><strong>Impact:</strong> Verified by simulation &mdash; 42% CO&#8322; cut, 84% green ratio, full habit reversal</li>
      </ul>
    </div>

    <div style="text-align:center;margin-top:auto" class="anim-4">
      <img src="{IMG['logo']}" class="s6-logo" alt="MoveWise">
      <div class="s6-footer">
        <strong>MoveWise</strong> &mdash; Every trip planned is a step toward cleaner air.<br>
        <span style="font-size:10px;color:var(--slate-400)">NEXUS 2026 &bull; Politecnico di Torino &bull; March 2026</span><br>
        <span style="font-size:9px;color:var(--slate-400);font-family:'JetBrains Mono',monospace">github.com/Sajjad-Shahali/RL-Mobility-Optimizer</span>
      </div>
    </div>
  </div>
</div>
</div>

<script>
// ═══ Slide Navigation ═══
const TOTAL=6;
let cur=0;
const slides=document.querySelectorAll('.slide');
const nav=document.getElementById('nav');
const progress=document.getElementById('progress');
const slideNum=document.getElementById('slideNum');

for(let i=0;i<TOTAL;i++){{
  const d=document.createElement('div');
  d.className='dot'+(i===0?' active':'');
  d.onclick=()=>goTo(i);
  nav.appendChild(d);
}}

function goTo(n){{
  if(n<0||n>=TOTAL)return;
  slides[cur].classList.remove('active');
  nav.children[cur].classList.remove('active');
  cur=n;
  slides[cur].classList.add('active');
  nav.children[cur].classList.add('active');
  progress.style.width=((cur+1)/TOTAL*100)+'%';
  slideNum.textContent=(cur+1)+' / '+TOTAL;
}}

document.addEventListener('keydown',e=>{{
  if(e.key==='ArrowRight'||e.key===' ')goTo(cur+1);
  if(e.key==='ArrowLeft')goTo(cur-1);
}});

// Touch/swipe support
let tx=0;
document.addEventListener('touchstart',e=>{{tx=e.touches[0].clientX}});
document.addEventListener('touchend',e=>{{
  const dx=e.changedTouches[0].clientX-tx;
  if(Math.abs(dx)>50)goTo(cur+(dx<0?1:-1));
}});

// ═══ PDF Export ═══
async function exportPDF(){{
  const btn=document.getElementById('exportBtn');
  btn.classList.add('exporting');
  btn.innerHTML='Generating...';

  const {{jsPDF}}=window.jspdf;
  const pdf=new jsPDF({{orientation:'landscape',unit:'px',format:[1440,810]}});

  // Hide controls
  const hide=[btn,nav,progress,slideNum];
  hide.forEach(el=>el.style.display='none');

  for(let i=0;i<TOTAL;i++){{
    // Show only current slide
    slides.forEach((s,j)=>{{
      s.classList.toggle('active',j===i);
      s.style.opacity=j===i?'1':'0';
      s.style.pointerEvents=j===i?'auto':'none';
    }});

    // Remove animations for clean capture
    const animated=slides[i].querySelectorAll('[class*=anim]');
    animated.forEach(el=>el.style.animation='none');
    animated.forEach(el=>el.style.opacity='1');

    await new Promise(r=>setTimeout(r,300));

    const canvas=await html2canvas(slides[i],{{
      scale:2,
      useCORS:true,
      allowTaint:true,
      width:1440,
      height:810,
      backgroundColor:null,
    }});

    if(i>0)pdf.addPage([1440,810],'landscape');
    pdf.addImage(canvas.toDataURL('image/jpeg',0.95),'JPEG',0,0,1440,810);
  }}

  // Restore
  hide.forEach(el=>el.style.display='');
  goTo(0);

  pdf.save('MoveWise_NEXUS2026_Final.pdf');
  btn.classList.remove('exporting');
  btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>Export PDF';
}}
</script>
</body>
</html>'''

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Written: {OUT_FILE}")
print(f"Size: {len(HTML):,} bytes")
