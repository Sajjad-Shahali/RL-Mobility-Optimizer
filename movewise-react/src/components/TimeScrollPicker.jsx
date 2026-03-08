import { useState, useRef, useEffect, useCallback } from "react";

const HOURS = Array.from({ length: 24 }, (_, i) => String(i).padStart(2, "0"));
const MINUTES = Array.from({ length: 60 }, (_, i) => String(i).padStart(2, "0"));
const ITEM_H = 40;
const VISIBLE = 5;
const HALF = Math.floor(VISIBLE / 2);

function WheelColumn({ items, selected, onChange }) {
  const ref = useRef(null);
  const suppressScroll = useRef(false);
  const scrollTimer = useRef(null);
  const idx = items.indexOf(selected);

  useEffect(() => {
    if (!ref.current) return;
    suppressScroll.current = true;
    ref.current.scrollTop = idx * ITEM_H;
    requestAnimationFrame(() => { suppressScroll.current = false; });
  }, []);

  const snapTo = useCallback((i) => {
    const clamped = Math.max(0, Math.min(i, items.length - 1));
    onChange(items[clamped]);
    if (ref.current) {
      suppressScroll.current = true;
      ref.current.scrollTo({ top: clamped * ITEM_H, behavior: "smooth" });
      setTimeout(() => { suppressScroll.current = false; }, 200);
    }
  }, [items, onChange]);

  const handleScroll = useCallback(() => {
    if (suppressScroll.current || !ref.current) return;
    clearTimeout(scrollTimer.current);
    scrollTimer.current = setTimeout(() => {
      if (!ref.current) return;
      const i = Math.round(ref.current.scrollTop / ITEM_H);
      snapTo(i);
    }, 80);
  }, [snapTo]);

  return (
    <div className="tsp-column">
      <div ref={ref} className="tsp-scroll" onScroll={handleScroll}>
        <div style={{ height: HALF * ITEM_H }} />
        {items.map((item, i) => {
          const dist = Math.abs(i - idx);
          const scale = dist === 0 ? 1 : dist === 1 ? 0.85 : 0.7;
          const opacity = dist === 0 ? 1 : dist === 1 ? 0.55 : 0.25;
          return (
            <div
              key={item}
              className="tsp-item"
              style={{
                height: ITEM_H,
                transform: `scale(${scale})`,
                opacity,
                fontWeight: dist === 0 ? 700 : 400,
              }}
              onClick={() => snapTo(i)}
            >
              {item}
            </div>
          );
        })}
        <div style={{ height: HALF * ITEM_H }} />
      </div>
    </div>
  );
}

export default function TimeScrollPicker({ value = "07:30", onChange, accentColor = "#22c55e" }) {
  const [open, setOpen] = useState(false);
  const [tempH, setTempH] = useState(null);
  const [tempM, setTempM] = useState(null);

  const [h, m] = value.split(":");
  const hour = HOURS.includes(h) ? h : "07";
  const minute = MINUTES.includes(m) ? m : "00";

  const openPicker = () => {
    setTempH(hour);
    setTempM(minute);
    setOpen(true);
  };

  const handleDone = () => {
    onChange(`${tempH || hour}:${tempM || minute}`);
    setOpen(false);
  };

  return (
    <>
      <button className="tsp-trigger" onClick={openPicker} type="button">
        <span className="tsp-trigger-icon">{"\u{1F552}"}</span>
        <span className="tsp-trigger-time">{hour}:{minute}</span>
      </button>

      {open && (
        <div className="tsp-overlay" onClick={() => setOpen(false)}>
          <div className="tsp-popup" onClick={(e) => e.stopPropagation()}>
            <div className="tsp-handle" />
            <div className="tsp-header">
              <span>Select Time</span>
              <button className="tsp-done" style={{ color: accentColor }} onClick={handleDone}>Done</button>
            </div>
            <div className="tsp-wheels">
              <WheelColumn items={HOURS} selected={tempH || hour} onChange={setTempH} />
              <div className="tsp-colon">:</div>
              <WheelColumn items={MINUTES} selected={tempM || minute} onChange={setTempM} />
            </div>
            <div className="tsp-highlight-row" style={{ borderColor: accentColor }} />
          </div>
        </div>
      )}
    </>
  );
}
