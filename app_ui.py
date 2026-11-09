"""
Siisti puhelinnäkymä: ottelukortit, tumma teema, yksi napautus avaa tiedot.
Lukee results.json:n (muoto alla). Jos tiedostoa ei ole, näyttää esimerkkidatan.
Aja: streamlit run app_ui.py   | lisää myös .streamlit/config.toml (ks. alla)
"""
import json
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Value bets", page_icon="📈", layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container {padding:1.2rem 1rem 4rem; max-width:560px;}
h1 {font-size:1.5rem !important; font-weight:700; letter-spacing:-.02em; margin-bottom:.2rem;}
.card {background:#131a22; border:1px solid #1f2a36; border-radius:16px; padding:14px 16px; margin:10px 0 2px;}
.meta {color:#7d8a99; font-size:.75rem; text-transform:uppercase; letter-spacing:.06em;}
.teams {font-size:1.1rem; font-weight:600; margin:4px 0 10px;}
.teams span {color:#7d8a99; font-weight:400; font-size:.85rem; margin:0 4px;}
.bar {display:flex; height:8px; border-radius:6px; overflow:hidden; gap:2px;}
.bar div:nth-child(1){background:#3b82f6;} .bar div:nth-child(2){background:#4b5563;} .bar div:nth-child(3){background:#f59e0b;}
.probs {display:flex; justify-content:space-between; color:#aab4c0; font-size:.8rem; margin:6px 0 10px;}
.pick {display:inline-block; padding:6px 12px; border-radius:999px; font-weight:600; font-size:.9rem;}
.pos {background:rgba(34,197,94,.15); color:#22c55e;}
.none {background:#1b232d; color:#7d8a99;}
div[data-testid="stExpander"] {border:none; background:transparent;}
div[data-testid="stExpander"] summary {color:#7d8a99; font-size:.8rem;}
</style>
""", unsafe_allow_html=True)

SAMPLE = [
    {"league": "Valioliiga", "kickoff": "La 14.11. 18:30", "home": "Man City", "away": "Fulham",
     "probs": [0.55, 0.23, 0.22], "odds": [1.62, 4.20, 5.40],
     "pick": {"market": "Man City", "odds": 1.62, "ev": 0.011},
     "form": "City xG 1.45 / xGA 1.60, Fulham xG 1.30 / xGA 1.10",
     "alert": "City on saanut 4 pistettä yli xPTS:n, regressioriski.",
     "missing": "Fulham: ykköskärki poissa (xG/90 0.42)", "referee": "M. Oliver (korttikerroin 1.08)"},
    {"league": "Valioliiga", "kickoff": "Su 15.11. 16:00", "home": "Brighton", "away": "Everton",
     "probs": [0.41, 0.28, 0.31], "odds": [2.30, 3.40, 3.60],
     "pick": {"market": "Everton", "odds": 3.60, "ev": 0.116},
     "form": "Brighton xG 1.50 / xGA 1.40, Everton xG 1.15 / xGA 1.20",
     "alert": "Everton on alisuorittanut pisteissä 3.1.", "missing": "-", "referee": "Ei vielä julkaistu"},
    {"league": "Serie B", "kickoff": "La 14.11. 15:00", "home": "Palermo", "away": "Bari",
     "probs": [0.48, 0.28, 0.24], "odds": [1.95, 3.30, 4.10],
     "pick": None, "form": "-", "alert": "-", "missing": "-", "referee": "-"},
]

path = Path("results.json")
matches = json.loads(path.read_text(encoding="utf-8")) if path.exists() else SAMPLE

st.title("Value bets")
if not path.exists():
    st.caption("Esimerkkidata. Luo results.json niin oikeat ottelut näkyvät.")

only_ev = st.toggle("Vain +EV", value=False)
leagues = sorted({m["league"] for m in matches})
tabs = st.tabs(["Kaikki"] + leagues)

for tab, lg in zip(tabs, ["Kaikki"] + leagues):
    with tab:
        items = [m for m in matches if lg == "Kaikki" or m["league"] == lg]
        if only_ev:
            items = [m for m in items if m.get("pick") and m["pick"]["ev"] > 0]
        items.sort(key=lambda m: m["pick"]["ev"] if m.get("pick") else -1, reverse=True)
        if not items:
            st.info("Ei otteluita.")
        for i, m in enumerate(items):
            h, d, a = [round(p * 100) for p in m["probs"]]
            pick = m.get("pick")
            pill = (f'<span class="pick pos">+{pick["ev"]:.1%} EV · {pick["market"]} @ {pick["odds"]:.2f}</span>'
                    if pick and pick["ev"] > 0 else '<span class="pick none">Ei arvoa</span>')
            st.markdown(f"""
<div class="card">
  <div class="meta">{m['league']} · {m['kickoff']}</div>
  <div class="teams">{m['home']} <span>vs</span> {m['away']}</div>
  <div class="bar"><div style="width:{h}%"></div><div style="width:{d}%"></div><div style="width:{a}%"></div></div>
  <div class="probs"><span>{h}%</span><span>{d}%</span><span>{a}%</span></div>
  {pill}
</div>""", unsafe_allow_html=True)
            with st.expander("Tiedot"):
                st.markdown(f"**Muoto:** {m['form']}  \n**Hälytys:** {m['alert']}  \n"
                            f"**Poissa:** {m['missing']}  \n**Tuomari:** {m['referee']}  \n"
                            f"**Kertoimet:** {m['odds'][0]} / {m['odds'][1]} / {m['odds'][2]}")

# .streamlit/config.toml:
# [theme]
# base = "dark"
# primaryColor = "#22c55e"
# backgroundColor = "#0b0f14"
# secondaryBackgroundColor = "#131a22"
# textColor = "#e6edf3"
# [client]
# toolbarMode = "minimal"
