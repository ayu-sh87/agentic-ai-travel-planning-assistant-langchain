import streamlit as st
from agents.travel_agent import TravelAgent


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="VoyagerAI – Smart Travel Planner",
    page_icon="🛩️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

if "result"    not in st.session_state: st.session_state.result    = None
if "generated" not in st.session_state: st.session_state.generated = False


# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --gold:     #C9963A;
    --gold-l:   #E8B84B;
    --gold-dim: rgba(201,150,58,0.15);
    --bg:       #0A0D12;
    --card:     rgba(255,255,255,0.035);
    --border:   rgba(255,255,255,0.075);
    --border2:  rgba(255,255,255,0.13);
    --t1:       #F0EDE8;
    --t2:       rgba(240,237,232,0.55);
    --t3:       rgba(240,237,232,0.28);
    --green:    #2ECC8F;
    --red:      #E05C5C;
}

/* ── FULL PAGE DARK BG ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main,
section.main > div { background: var(--bg) !important; color: var(--t1) !important; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stSidebar"]  { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"]   { display: none !important; }

/* ── ZERO OUT DEFAULT PAGE PADDING SO NAVBAR GOES EDGE-TO-EDGE ── */
[data-testid="stMain"] > div:first-child { padding-top: 0 !important; }
.block-container {
    padding-top: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}

/* ── FONT DEFAULTS ── */
html, body, p, div, span, label, [data-testid] {
    font-family: 'DM Sans', sans-serif !important;
}

/* ── TEXT INPUTS ── */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 0.5px solid var(--border2) !important;
    border-radius: 11px !important;
    color: var(--t1) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 13px 14px !important;
    height: 48px !important;
    transition: border-color 0.18s, background 0.18s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--gold) !important;
    background: rgba(201,150,58,0.06) !important;
    box-shadow: none !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: rgba(240,237,232,0.18) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 400 !important;
    font-size: 13px !important;
}
[data-testid="stTextInput"] label {
    color: var(--t3) !important;
    font-size: 10px !important;
    font-weight: 500 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--gold) !important;
}
[data-testid="stSlider"] [data-testid="stTickBar"] { display: none !important; }
[data-testid="stSlider"] label {
    color: var(--t3) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

/* ── BUTTON ── */
[data-testid="stButton"] > button {
    background: var(--gold) !important;
    color: #0A0D12 !important;
    border: none !important;
    border-radius: 12px !important;
    width: 100% !important;
    height: 50px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 800 !important;
    letter-spacing: 0.4px !important;
    transition: opacity 0.18s, transform 0.12s !important;
}
[data-testid="stButton"] > button:hover  { opacity: 0.88 !important; transform: translateY(-1px) !important; }
[data-testid="stButton"] > button:active { transform: scale(0.98) !important; }

/* ── TABS ── */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 0.5px solid var(--border) !important;
    gap: 4px !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    color: var(--t3) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    padding: 13px 16px !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
}
[data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
}
[data-baseweb="tab-highlight"],
[data-baseweb="tab-border"] { display: none !important; }

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 0.5px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] p {
    font-size: 10px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--t3) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    color: var(--t1) !important;
}
[data-testid="stMetricDelta"] { display: none !important; }

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; margin: 18px 0 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 4px; }

/* ── LEFT COL RIGHT BORDER ── */
[data-testid="stHorizontalBlock"] > div:first-child {
    border-right: 0.5px solid var(--border) !important;
    padding-right: 28px !important;
}
[data-testid="stHorizontalBlock"] > div:last-child {
    padding-left: 28px !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _card(inner: str, accent: bool = False) -> str:
    bg  = "rgba(201,150,58,0.07)"  if accent else "rgba(255,255,255,0.035)"
    bdr = "rgba(201,150,58,0.25)"  if accent else "rgba(255,255,255,0.075)"
    return (
        f'<div style="background:{bg};border:0.5px solid {bdr};'
        f'border-radius:16px;padding:20px;margin-bottom:0;">{inner}</div>'
    )

def _price_badge(text: str) -> str:
    return (
        f'<span style="display:inline-block;background:rgba(201,150,58,0.14);'
        f'color:#E8B84B;padding:5px 13px;border-radius:18px;'
        f'font-family:\'Syne\',sans-serif;font-size:14px;font-weight:700;">'
        f'{text}</span>'
    )

def _label(text: str) -> str:
    return (
        f'<p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;'
        f'color:rgba(240,237,232,0.28);margin-bottom:10px;">{text}</p>'
    )

def _success_bar() -> str:
    return (
        '<div style="background:rgba(46,204,143,0.08);border:0.5px solid rgba(46,204,143,0.25);'
        'border-radius:10px;padding:11px 16px;margin-bottom:20px;font-size:12px;'
        'color:rgba(240,237,232,0.6);display:flex;align-items:center;gap:8px;">'
        '<span style="color:#2ECC8F;font-size:15px;">✓</span>'
        'Trip plan generated successfully</div>'
    )


# ─────────────────────────────────────────────
# FULL-WIDTH NAVBAR  (outside columns)
# ─────────────────────────────────────────────

st.markdown("""
<div style="
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 32px;
    border-bottom: 0.5px solid rgba(255,255,255,0.075);
    margin-bottom: 0;
    box-sizing: border-box;
">
  <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:17px;
              letter-spacing:-0.3px;display:flex;align-items:center;gap:8px;color:#F0EDE8;">
    <div style="width:22px;height:22px;border-radius:50%;border:1.5px solid #C9963A;
                display:flex;align-items:center;justify-content:center;">
      <div style="width:8px;height:8px;border-radius:50%;background:#C9963A;"></div>
    </div>
    VOYAGER<span style="color:#C9963A;">AI</span>
  </div>
  <div style="display:flex;gap:8px;">
    <span style="font-size:12px;padding:5px 14px;border-radius:20px;
                 background:#C9963A;color:#0A0D12;font-weight:600;">Plan</span>
    <span style="font-size:12px;padding:5px 14px;border-radius:20px;
                 border:0.5px solid rgba(255,255,255,0.09);
                 color:rgba(240,237,232,0.38);">Explore</span>
    <span style="font-size:12px;padding:5px 14px;border-radius:20px;
                 border:0.5px solid rgba(255,255,255,0.09);
                 color:rgba(240,237,232,0.38);">History</span>
  </div>
  <div style="display:flex;align-items:center;gap:6px;font-size:11px;
              color:rgba(240,237,232,0.3);letter-spacing:0.5px;">
    <div style="width:5px;height:5px;border-radius:50%;background:#2ECC8F;"></div>
    AI agent ready
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN  4 : 1  SPLIT
# left = form (1 part)   right = results (4 parts)
# ─────────────────────────────────────────────

left, right = st.columns([1.32, 3.5])


# ══════════════════════════════════════════════
# LEFT — form panel (always visible)
# ══════════════════════════════════════════════

with left:

    st.markdown("""
    <div style="padding: 28px 0 0;">
      <p style="font-size:10px;letter-spacing:2.5px;text-transform:uppercase;
                color:#C9963A;font-weight:500;margin-bottom:10px;">AI-powered planning</p>
      <h2 style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;
                 letter-spacing:-1px;line-height:1.15;color:#F0EDE8;margin-bottom:8px;">
        Plan your<br><span style="color:#C9963A;">perfect</span> trip
      </h2>
      <p style="font-size:13px;color:rgba(240,237,232,0.32);font-weight:300;
                line-height:1.65;margin-bottom:24px;">
        Smart routing, real-time weather &amp; curated itineraries — in seconds.
      </p>
    </div>
    """, unsafe_allow_html=True)

    source      = st.text_input("Departure city",   placeholder="e.g. Delhi", key="source")
    destination = st.text_input("Destination city", placeholder="e.g. Goa",   key="destination")

    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin:2px 0 10px;">
      <div style="flex:1;height:0.5px;background:rgba(255,255,255,0.075);"></div>
      <div style="width:28px;height:28px;border-radius:50%;
                  border:0.5px solid rgba(201,150,58,0.35);
                  background:rgba(201,150,58,0.1);color:#C9963A;
                  display:flex;align-items:center;justify-content:center;font-size:13px;">⇅</div>
      <div style="flex:1;height:0.5px;background:rgba(255,255,255,0.075);"></div>
    </div>
    """, unsafe_allow_html=True)

    days = st.slider("Duration (days)", min_value=1, max_value=7, value=3, key="days")

    st.markdown(
        f'<div style="display:flex;justify-content:flex-end;margin:-6px 0 18px;">'
        f'<span style="font-family:\'Syne\',sans-serif;font-size:26px;'
        f'font-weight:800;color:#C9963A;">{days}</span>'
        f'<span style="font-size:11px;color:rgba(240,237,232,0.3);'
        f'align-self:flex-end;margin-left:4px;margin-bottom:3px;">days</span></div>',
        unsafe_allow_html=True,
    )

    generate = st.button("✦  Generate Trip Plan", use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(_label("Popular routes"), unsafe_allow_html=True)
    for frm, to in [("Delhi","Goa"),("Hyderabad","Goa"),("Bangalore","Goa"),("Delhi","Kolkata")]:
        st.markdown(
            f'<div style="padding:9px 13px;background:rgba(255,255,255,0.025);'
            f'border:0.5px solid rgba(255,255,255,0.075);border-radius:9px;'
            f'font-size:12px;color:rgba(240,237,232,0.38);margin-bottom:6px;">'
            f'{frm} → {to}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;flex-wrap:wrap;gap:6px;">'
        + "".join(
            f'<span style="font-size:10px;padding:4px 10px;border-radius:6px;'
            f'border:0.5px solid rgba(255,255,255,0.075);color:rgba(240,237,232,0.3);'
            f'display:flex;align-items:center;gap:5px;">'
            f'<span style="width:5px;height:5px;border-radius:50%;background:#2ECC8F;display:inline-block;"></span>'
            f'{t}</span>'
            for t in ["LangChain","Streamlit","Weather API","JSON datasets"]
        )
        + "</div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════
# RIGHT — results panel (hidden until cities filled)
# ══════════════════════════════════════════════

with right:

    both_filled = bool(source.strip() and destination.strip())

    # ── IDLE ────────────────────────────────────
    if not both_filled and not st.session_state.generated:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;
                    justify-content:center;min-height:72vh;text-align:center;padding:40px;">
          <div style="width:80px;height:80px;border-radius:50%;
                      border:1px solid rgba(255,255,255,0.09);
                      display:flex;align-items:center;justify-content:center;margin:0 auto 20px;">
            <div style="width:50px;height:50px;border-radius:50%;
                        border:0.5px solid rgba(201,150,58,0.18);
                        display:flex;align-items:center;justify-content:center;
                        font-size:22px;color:rgba(240,237,232,0.18);">🌍</div>
          </div>
          <h3 style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
                     color:rgba(240,237,232,0.28);margin-bottom:9px;">Ready for takeoff</h3>
          <p style="font-size:13px;color:rgba(240,237,232,0.2);line-height:1.7;">
            Enter a departure city and destination on the left<br>to unlock your trip plan.
          </p>
        </div>
        """, unsafe_allow_html=True)

    else:

        # ── VALIDATION ERROR ─────────────────────
        if generate and (not source.strip() or not destination.strip()):
            st.markdown(
                '<div style="background:rgba(224,92,92,0.1);border:0.5px solid rgba(224,92,92,0.3);'
                'border-radius:11px;padding:13px 18px;margin-bottom:16px;font-size:13px;color:#F09595;">'
                '⚠️  Please fill in both the departure and destination city.</div>',
                unsafe_allow_html=True,
            )

        # ── RUN AGENT ────────────────────────────
        if generate and source.strip() and destination.strip():
            with st.spinner("✦ AI agent planning your trip…"):
                agent  = TravelAgent()
                result = agent.generate_trip_plan(source, destination, days)
            st.session_state.result    = result
            st.session_state.generated = True

        result = st.session_state.result

        # ── CITIES FILLED BUT NOT YET GENERATED ──
        if result is None:
            st.markdown("""
            <div style="display:flex;align-items:center;justify-content:center;
                        min-height:72vh;text-align:center;padding:40px;">
              <p style="font-size:13px;color:rgba(240,237,232,0.3);line-height:1.7;">
                Cities ready — hit
                <strong style="color:#C9963A;">Generate Trip Plan</strong>
                to continue.
              </p>
            </div>
            """, unsafe_allow_html=True)

        # ── ERROR ────────────────────────────────
        elif result.get("status") == "error":
            st.markdown(
                f'<div style="background:rgba(224,92,92,0.1);border:0.5px solid rgba(224,92,92,0.3);'
                f'border-radius:14px;padding:20px 22px;margin-bottom:16px;">'
                f'<p style="color:#F09595;font-weight:600;margin-bottom:6px;">Route not found</p>'
                f'<p style="color:rgba(240,237,232,0.45);font-size:13px;line-height:1.6;">'
                f'{result.get("message","An unexpected error occurred.")}</p></div>'
                f'<div style="background:rgba(255,255,255,0.03);border:0.5px solid rgba(255,255,255,0.075);'
                f'border-radius:12px;padding:16px 20px;">'
                f'<p style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;'
                f'color:rgba(240,237,232,0.25);margin-bottom:9px;">Available routes</p>'
                f'<p style="font-size:13px;color:rgba(240,237,232,0.45);line-height:1.8;">'
                f'Hyderabad → Goa &nbsp;·&nbsp; Bangalore → Goa &nbsp;·&nbsp; Delhi → Kolkata</p></div>',
                unsafe_allow_html=True,
            )

        # ── RESULTS ──────────────────────────────
        else:
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "  Summary", "✈  Flight & Hotel",
                "  Weather",  "  Itinerary", "  Budget"
            ])

            # ── TAB 1 — SUMMARY ──────────────────
            with tab1:
                st.markdown(_success_bar(), unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("Departure",   result["trip_summary"]["source"])
                with c2: st.metric("Destination", result["trip_summary"]["destination"])
                with c3: st.metric("Duration",    f'{result["trip_summary"]["days"]} days')
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    _card(
                        '<p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;'
                        'color:#C9963A;font-weight:500;margin-bottom:9px;">✦ AI reasoning</p>'
                        f'<p style="font-size:13px;line-height:1.75;color:rgba(240,237,232,0.55);'
                        f'font-weight:300;">{result["reasoning"]}</p>',
                        accent=True,
                    ),
                    unsafe_allow_html=True,
                )

            # ── TAB 2 — FLIGHT + HOTEL ────────────
            with tab2:
                st.markdown(_success_bar(), unsafe_allow_html=True)
                f, h = result["flight"], result["hotel"]
                stars = "★" * int(h["stars"]) + "☆" * (5 - int(h["stars"]))
                amens = "".join(
                    f'<span style="font-size:11px;padding:3px 9px;border-radius:5px;'
                    f'background:rgba(255,255,255,0.05);border:0.5px solid rgba(255,255,255,0.075);'
                    f'color:rgba(240,237,232,0.4);margin:3px;">{a}</span>'
                    for a in h["amenities"]
                )
                col_f, col_h = st.columns(2)
                with col_f:
                    st.markdown(_card(
                        f'<p style="font-size:10px;letter-spacing:1.8px;text-transform:uppercase;'
                        f'color:rgba(240,237,232,0.3);margin-bottom:12px;">✈ Selected flight</p>'
                        f'<h3 style="font-family:\'Syne\',sans-serif;font-size:19px;font-weight:700;'
                        f'color:#F0EDE8;margin-bottom:14px;">{f["airline"]}</h3>'
                        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:11px;">'
                        f'<span style="font-size:13px;font-weight:500;color:#F0EDE8;">{f["from"]}</span>'
                        f'<div style="flex:1;height:0.5px;background:rgba(255,255,255,0.075);"></div>'
                        f'<span style="font-size:13px;font-weight:500;color:#F0EDE8;">{f["to"]}</span></div>'
                        + _price_badge(f'₹{f["price"]:,}') +
                        f'<div style="margin-top:14px;">'
                        f'<div style="display:flex;justify-content:space-between;padding:8px 0;'
                        f'border-bottom:0.5px solid rgba(255,255,255,0.06);font-size:12px;">'
                        f'<span style="color:rgba(240,237,232,0.3);">Departure</span>'
                        f'<span style="color:#F0EDE8;font-weight:500;">{f["departure_time"]}</span></div>'
                        f'<div style="display:flex;justify-content:space-between;padding:8px 0;font-size:12px;">'
                        f'<span style="color:rgba(240,237,232,0.3);">Arrival</span>'
                        f'<span style="color:#F0EDE8;font-weight:500;">{f["arrival_time"]}</span></div></div>'
                    ), unsafe_allow_html=True)
                with col_h:
                    st.markdown(_card(
                        f'<p style="font-size:10px;letter-spacing:1.8px;text-transform:uppercase;'
                        f'color:rgba(240,237,232,0.3);margin-bottom:12px;"> Recommended hotel</p>'
                        f'<h3 style="font-family:\'Syne\',sans-serif;font-size:19px;font-weight:700;'
                        f'color:#F0EDE8;margin-bottom:9px;">{h["name"]}</h3>'
                        f'<p style="color:#C9963A;font-size:15px;letter-spacing:2px;margin-bottom:9px;">{stars}</p>'
                        + _price_badge(f'₹{h["price_per_night"]:,}/night') +
                        f'<div style="margin-top:14px;">'
                        f'<div style="display:flex;justify-content:space-between;padding:8px 0;'
                        f'border-bottom:0.5px solid rgba(255,255,255,0.06);font-size:12px;">'
                        f'<span style="color:rgba(240,237,232,0.3);">City</span>'
                        f'<span style="color:#F0EDE8;font-weight:500;">{h["city"]}</span></div></div>'
                        f'<div style="margin-top:12px;display:flex;flex-wrap:wrap;gap:4px;">{amens}</div>'
                    ), unsafe_allow_html=True)

            # ── TAB 3 — WEATHER ───────────────────
            with tab3:
                st.markdown(_success_bar(), unsafe_allow_html=True)
                wd   = result["weather"]
                cols = st.columns(len(wd))
                for w, col in zip(wd, cols):
                    ico = "☀️" if w["temperature"] > 32 else ("⛅" if w["temperature"] > 27 else "🌤️")
                    lbl = "Hot" if w["temperature"] > 32 else ("Warm" if w["temperature"] > 27 else "Pleasant")
                    with col:
                        st.markdown(
                            f'<div style="background:rgba(255,255,255,0.035);'
                            f'border:0.5px solid rgba(255,255,255,0.075);'
                            f'border-radius:12px;padding:16px 10px;text-align:center;">'
                            f'<p style="font-size:10px;color:rgba(240,237,232,0.3);margin-bottom:9px;">{w["date"]}</p>'
                            f'<div style="font-size:28px;margin-bottom:7px;">{ico}</div>'
                            f'<p style="font-family:\'Syne\',sans-serif;font-size:22px;font-weight:700;'
                            f'color:#C9963A;margin-bottom:3px;">{w["temperature"]}°</p>'
                            f'<p style="font-size:10px;color:rgba(240,237,232,0.28);">{lbl}</p></div>',
                            unsafe_allow_html=True,
                        )

            # ── TAB 4 — ITINERARY ─────────────────
            with tab4:
                st.markdown(_success_bar(), unsafe_allow_html=True)
                col_it, col_at = st.columns([3, 2])
                with col_it:
                    st.markdown(_label("Day-by-day plan"), unsafe_allow_html=True)
                    for day, places in result["itinerary"].items():
                        rows = "".join(
                            f'<div style="display:flex;align-items:flex-start;gap:10px;'
                            f'padding:9px 0;border-bottom:0.5px solid rgba(255,255,255,0.05);">'
                            f'<div style="width:7px;height:7px;border-radius:50%;background:#C9963A;'
                            f'margin-top:4px;flex-shrink:0;"></div>'
                            f'<span style="font-size:13px;color:rgba(240,237,232,0.55);">{p}</span></div>'
                            for p in places
                        )
                        st.markdown(
                            f'<div style="margin-bottom:20px;">'
                            f'<p style="font-family:\'Syne\',sans-serif;font-size:13px;font-weight:700;'
                            f'color:#C9963A;margin-bottom:9px;">{day}</p>{rows}</div>',
                            unsafe_allow_html=True,
                        )
                with col_at:
                    st.markdown(_label("Top attractions"), unsafe_allow_html=True)
                    for p in result["places"]:
                        st.markdown(
                            _card(
                                f'<p style="font-size:13px;font-weight:500;color:#F0EDE8;margin-bottom:5px;">{p["name"]}</p>'
                                f'<p style="font-size:11px;color:rgba(240,237,232,0.35);">'
                                f'<span style="color:#C9963A;">★</span> {p["rating"]} · {p["type"]}</p>'
                            ),
                            unsafe_allow_html=True,
                        )
                        st.markdown("<div style='height:9px;'></div>", unsafe_allow_html=True)

            # ── TAB 5 — BUDGET ────────────────────
            with tab5:
                st.markdown(_success_bar(), unsafe_allow_html=True)
                b = result["budget"]
                st.markdown(
                    f'<div style="background:rgba(201,150,58,0.07);'
                    f'border:0.5px solid rgba(201,150,58,0.25);'
                    f'border-radius:16px;padding:30px;text-align:center;margin-bottom:18px;">'
                    f'<p style="font-size:10px;letter-spacing:2px;text-transform:uppercase;'
                    f'color:#C9963A;font-weight:500;margin-bottom:9px;">Total estimated cost</p>'
                    f'<p style="font-family:\'Syne\',sans-serif;font-size:46px;font-weight:800;'
                    f'color:#F0EDE8;letter-spacing:-1.5px;">₹{b["total_cost"]:,}</p></div>',
                    unsafe_allow_html=True,
                )
                items = [
                    ("🛩️", "Flight",           b["flight_cost"],        False),
                    ("🏬", "Hotel",            b["hotel_cost"],         False),
                    ("🍟🍟", "Food & transport",  b["food_and_transport"], False),
                    ("🧾", "Grand total",      b["total_cost"],         True),
                ]
                r1, r2 = st.columns(2)
                for col, (ico, lbl, val, acc) in zip([r1, r2, r1, r2], items):
                    bg  = "rgba(201,150,58,0.07)"  if acc else "rgba(255,255,255,0.035)"
                    bdr = "rgba(201,150,58,0.25)"  if acc else "rgba(255,255,255,0.075)"
                    with col:
                        st.markdown(
                            f'<div style="background:{bg};border:0.5px solid {bdr};'
                            f'border-radius:12px;padding:16px;display:flex;align-items:center;'
                            f'gap:12px;margin-bottom:10px;">'
                            f'<div style="width:36px;height:36px;border-radius:9px;'
                            f'background:rgba(201,150,58,0.1);display:flex;align-items:center;'
                            f'justify-content:center;font-size:16px;flex-shrink:0;">{ico}</div>'
                            f'<div><p style="font-size:10px;color:rgba(240,237,232,0.3);margin-bottom:3px;">{lbl}</p>'
                            f'<p style="font-family:\'Syne\',sans-serif;font-size:17px;'
                            f'font-weight:700;color:#F0EDE8;">₹{val:,}</p></div></div>',
                            unsafe_allow_html=True,
                        )