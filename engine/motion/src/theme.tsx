// DENKMUSTER-Look: weißes Whiteboard, schwarzer Marker, Rot nur zur Betonung, Blau/Orange sparsam; Handschrift (Caveat);
// alles wirkt live gezeichnet (leicht zittriger Strich), Zahlen werden rot eingekreist. Keine Schatten, keine Glows.
import React from "react";
import {AbsoluteFill, useCurrentFrame, interpolate} from "remotion";
import {s, clamp, ease} from "./lib";

const INK = "#1D1D1F", RED = "#D7263D", BLUE = "#1F5FBF", ORANGE = "#E39B17", BOARD = "#FBFBF8", GREY = "#8A8A90";
const HAND = "Caveat, cursive";
const sketch: React.CSSProperties = {background: "#FFFFFF", border: `4px solid ${INK}`, borderRadius: "14px 22px 12px 26px / 24px 12px 22px 14px"};

const Bg: React.FC<{children?: React.ReactNode; hot?: boolean}> = ({children, hot}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: BOARD}}>
      <svg width={0} height={0} style={{position: "absolute"}}>
        <filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed={Math.floor(f / 4) % 3} /><feDisplacementMap in="SourceGraphic" scale="3.2" /></filter>
      </svg>
      <AbsoluteFill style={{background: "radial-gradient(ellipse at 30% 20%, rgba(0,0,0,0.025) 0%, transparent 40%), radial-gradient(ellipse at 75% 80%, rgba(0,0,0,0.03) 0%, transparent 35%)"}} />
      {hot && <AbsoluteFill style={{background: "radial-gradient(ellipse at 50% 50%, rgba(215,38,61,0.06) 0%, transparent 60%)"}} />}
      <AbsoluteFill style={{filter: "url(#rough)"}}>{children}</AbsoluteFill>
      <AbsoluteFill style={{background: "radial-gradient(ellipse at center, transparent 70%, rgba(0,0,0,0.06) 100%)"}} />
    </AbsoluteFill>
  );
};

/** Handschrift erscheint Buchstabe für Buchstabe wie mit dem Marker geschrieben (keine Marker-Sounds – Laurin) */
const Write: React.FC<{text: string; at: number; style?: React.CSSProperties}> = ({text, at, style}) => {
  const f = useCurrentFrame(); if (f < s(at)) return null;
  const n = Math.min(text.length, ((f - s(at)) / 30) * 16);
  return <span style={{fontFamily: HAND, fontWeight: 700, ...style}}>
    {text.split("").map((c, i) => <span key={i} style={{opacity: Math.max(0, Math.min(1, n - i))}}>{c}</span>)}
  </span>;
};

const Label: React.FC<{text?: string}> = ({text}) => {
  const f = useCurrentFrame(); if (!text) return null;
  const u = interpolate(f, [s(0.2 + text.length / 16), s(0.5 + text.length / 16)], [0, 1], {...clamp, easing: ease});
  return <div style={{position: "absolute", left: 90, top: 50}}>
    <Write text={text} at={0.1} style={{fontSize: 54, color: INK}} />
    <svg width={text.length * 26 + 30} height={20} style={{display: "block"}}><path d={`M4 10 Q ${text.length * 13} ${4} ${text.length * 26 + 20} 12`} stroke={RED} strokeWidth={5} fill="none" strokeLinecap="round"
      strokeDasharray={text.length * 30} strokeDashoffset={text.length * 30 * (1 - u)} /></svg>
  </div>;
};

/** Marker-Pfeil (schwarz), wird gezogen */
const Thread: React.FC<{x1: number; y1: number; x2: number; y2: number; p: number; straight?: boolean}> = ({x1, y1, x2, y2, p, straight}) => {
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - (straight ? 0 : Math.hypot(x2 - x1, y2 - y1) * 0.18);
  const len = Math.hypot(x2 - x1, y2 - y1) * 1.25; const a = Math.atan2(y2 - my, x2 - mx);
  return <g><path d={`M${x1},${y1} Q${mx},${my} ${x2},${y2}`} fill="none" stroke={INK} strokeWidth={4.5} strokeLinecap="round" strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
    {p > 0.95 && <path d={`M${x2 - 22 * Math.cos(a - 0.45)},${y2 - 22 * Math.sin(a - 0.45)} L${x2},${y2} L${x2 - 22 * Math.cos(a + 0.45)},${y2 - 22 * Math.sin(a + 0.45)}`} fill="none" stroke={INK} strokeWidth={4.5} strokeLinecap="round" />}</g>;
};
/** roter Marker-Punkt mit Kringel */
const Pin: React.FC<{x: number; y: number; k: number}> = ({x, y, k}) => (
  <g transform={`translate(${x},${y}) scale(${k})`}><circle r={7} fill={RED} /><circle r={16} fill="none" stroke={RED} strokeWidth={3} strokeDasharray="90 12" /></g>
);


/* ---- Denkmuster-eigene Symbole: Kritzel-Doodles statt Piktogramme (Strichmännchen, Gesichter, Gedankenwolken) ---- */
const doodle = (st: any) => ({...st, strokeWidth: 5});
const icons: Record<string, (st: any, c: string) => React.ReactNode> = {
  person: (st) => <g {...doodle(st)}><circle cx={50} cy={22} r={13} {...doodle(st)} /><path d="M50 35 L50 66 M50 44 L32 58 M50 44 L68 56 M50 66 L36 90 M50 66 L64 90" {...doodle(st)} /><path d="M45 21 h1 M55 21 h1 M45 27 q5 4 10 0" {...doodle(st)} /></g>,
  sad: (st) => <g><circle cx={50} cy={22} r={13} {...doodle(st)} /><path d="M45 29 q5 -4 10 0 M50 35 Q48 50 50 66 M50 46 L38 64 M50 46 L62 64 M50 66 L42 90 M50 66 L58 90" {...doodle(st)} /></g>,
  happy: (st) => <g><circle cx={50} cy={22} r={13} {...doodle(st)} /><path d="M44 26 q6 6 12 0 M50 35 L50 66 M50 44 L30 30 M50 44 L70 30 M50 66 L36 90 M50 66 L64 90" {...doodle(st)} /></g>,
  think: (st) => <g><circle cx={42} cy={44} r={20} {...doodle(st)} /><path d="M36 52 h12 M70 12 q10 0 10 9 q0 7 -9 10 v6 M71 46 v1" {...doodle(st)} /></g>,
  heart: (st) => <path d="M50 84 C22 64 8 46 18 30 C27 16 44 20 50 34 C56 20 74 15 82 30 C92 47 78 64 50 84 Z M30 34 q4 -6 10 -4" {...doodle(st)} />,
  brain: (st) => <path d="M50 20 C38 8 18 16 20 32 C8 38 10 58 22 62 C20 78 40 86 50 74 C60 86 80 78 78 62 C90 58 92 38 80 32 C82 16 62 8 50 20 Z M50 22 Q44 48 50 74 M30 40 q8 4 12 -2 M60 50 q8 -6 14 2" {...doodle(st)} />,
  phone: (st) => <g><rect x={30} y={10} width={40} height={80} rx={8} {...doodle(st)} /><path d="M40 30 h20 M40 42 h14 M40 54 h18 M74 18 l8 -6 M76 30 l10 -2" {...doodle(st)} /></g>,
  clock: (st) => <g><circle cx={50} cy={52} r={34} {...doodle(st)} /><path d="M50 30 V52 L64 62 M20 16 l8 8 M80 16 l-8 8" {...doodle(st)} /></g>,
  doc: (st) => <path d="M26 10 H64 L76 24 V90 H26 Z M34 36 q10 -4 34 0 M34 50 q12 3 30 -1 M34 64 q8 -3 24 0" {...doodle(st)} />,
  eye: (st) => <g><path d="M8 50 Q50 10 92 50 Q50 90 8 50 Z" {...doodle(st)} /><circle cx={50} cy={50} r={11} fill={st.stroke} /></g>,
  lock: (st) => <g><rect x={24} y={46} width={52} height={40} rx={8} {...doodle(st)} /><path d="M36 46 V32 q14 -22 28 0 V46" {...doodle(st)} /></g>,
  money: (st) => <g><ellipse cx={50} cy={60} rx={30} ry={10} {...doodle(st)} /><path d="M20 60 v-12 M80 60 v-12" {...doodle(st)} /><ellipse cx={50} cy={46} rx={30} ry={10} {...doodle(st)} /></g>,
  idea: (st) => <g><path d="M50 12 C30 12 22 30 30 44 C36 54 38 58 38 66 H62 C62 58 64 54 70 44 C78 30 70 12 50 12 Z M40 76 h20 M42 86 h16" {...doodle(st)} /><path d="M14 30 l8 2 M86 30 l-8 2 M50 2 v4" {...doodle(st)} /></g>,
};
/** Gedankenwolke statt Kasten */
const Node: React.FC<{hot?: boolean; children?: React.ReactNode}> = ({hot, children}) => (
  <div style={{position: "relative", width: 220, height: 180, display: "flex", alignItems: "center", justifyContent: "center"}}>
    <svg width={220} height={180} style={{position: "absolute", left: 0, top: 0}}><path d="M60 150 C20 152 8 116 30 96 C6 76 24 38 58 46 C64 14 112 6 128 34 C150 10 196 24 190 60 C218 74 210 128 172 132 C168 160 120 166 104 148 C92 162 70 162 60 150 Z"
      fill="#FFFFFF" stroke={hot ? RED : INK} strokeWidth={hot ? 6 : 4.5} /><circle cx={40} cy={170} r={6} fill="none" stroke={hot ? RED : INK} strokeWidth={3.5} /></svg>
    <div style={{position: "relative"}}>{children}</div>
  </div>
);
/** Raster: Strichmännchen ohne Kasten, betroffene in Rot und gebeugt */
const Tile: React.FC<{hot?: boolean; icon?: string}> = ({hot, icon}) => {
  const st = {fill: "none", stroke: hot ? RED : INK, strokeWidth: 5, strokeLinecap: "round" as const, strokeLinejoin: "round" as const};
  const fn = icon === "person" || !icon ? (hot ? icons.sad : icons.person) : (icons[icon] || icons.person);
  return <svg width={64} height={64} viewBox="0 0 100 100">{fn(st, st.stroke)}</svg>;
};

export const T = {
  c: {ink: INK, muted: GREY, accent: BLUE, hot: RED, land: "#FFFFFF", border: INK, dot: ORANGE, hl: (o: number) => `rgba(215,38,61,${0.12 + 0.3 * o})`,
      track: "#C9C9CC", panelAccent: BLUE, nodeInk: INK, panelInk: INK, cardInk: INK, cardHotInk: RED, tileInk: INK, bubble: BLUE, sheetInk: INK, sheetLine: "#D9D9DC"},
  font: {head: HAND, body: HAND, num: HAND, mono: "DejaVu Sans Mono, monospace"},
  headWeight: 700, headStyle: {letterSpacing: 0} as React.CSSProperties, iconStroke: 5, iconFilter: undefined as string | undefined, mapFilter: undefined as string | undefined,
  glow: false, borderW: 1.4, tileJitter: 8, gridRows: false, num: {sep: ".", decSep: ","},
  Bg, Write, Label, Thread, Pin, icons, Node, Tile, stepSize: 40, stackStep: 0.45, counterPad: "50px 120px 90px",
  phoneFrame: {background: "#FFFFFF", border: `5px solid ${INK}`, boxShadow: "none", padding: 10} as React.CSSProperties,
  phoneScreen: {background: "#FFFFFF", border: `3px solid ${INK}`} as React.CSSProperties,
  phoneHead: {color: INK, fontFamily: HAND, fontSize: 40, borderBottom: `3px solid ${INK}`} as React.CSSProperties,
  phoneBubble: {fontFamily: HAND, fontSize: 32, color: "#FFFFFF"} as React.CSSProperties,
  tag: {background: "#FFFFFF", border: `3px solid ${INK}`, borderRadius: 10, padding: "0 14px"} as React.CSSProperties, tagText: {color: INK, fontSize: 38} as React.CSSProperties,
  panel: {border: `6px solid ${RED}`, borderRadius: "50% 46% 52% 48% / 55% 50% 48% 52%", padding: "30px 90px 56px", background: "transparent"} as React.CSSProperties,
  node: {...sketch} as React.CSSProperties,
  nodeHot: {...sketch, border: `5px solid ${RED}`} as React.CSSProperties,
  card: {...sketch, transform: "rotate(-1.5deg)"} as React.CSSProperties,
  cardTop: " ", cardTopStyle: {left: 250, top: -18, width: 120, height: 34, background: "rgba(31,95,191,0.25)", transform: "rotate(-3deg)"} as React.CSSProperties,
  cardHot: {...sketch, border: `6px solid ${RED}`} as React.CSSProperties,
  tile: {...sketch, border: `3px solid ${INK}`} as React.CSSProperties,
  tileHot: {...sketch, border: `4px solid ${RED}`, background: "#FDECEE"} as React.CSSProperties,
  sheet: {...sketch, background: "#FFFDF4"} as React.CSSProperties,
  bar: {background: "repeating-linear-gradient(135deg, #1D1D1F 0 4px, transparent 4px 12px)", border: `4px solid ${INK}`, borderRadius: 6} as React.CSSProperties,
  barHot: {background: "repeating-linear-gradient(135deg, #D7263D 0 5px, transparent 5px 11px)", border: `4px solid ${RED}`, borderRadius: 6} as React.CSSProperties,
};
