"""The Night Shift — interactive presentation about sleep (Streamlit).

Run locally:   streamlit run app.py
Pages:
  /                 → the presentation (full screen)
  /?vote=1          → phone survey (what the QR code opens)
  /?reset=nightshift → clears all survey answers (do this before your talk)

Answers are stored in static/results.json, which Streamlit serves at
/app/static/results.json — the presentation reads it every 2.5 s.
"""
import json
import threading
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent
STATIC = ROOT / "static"
RESULTS = STATIC / "results.json"
STATIC.mkdir(exist_ok=True)
if not RESULTS.exists():
    RESULTS.write_text("[]", encoding="utf-8")

st.set_page_config(page_title="The Night Shift · Why Sleep Matters", page_icon="🌙",
                   layout="wide", initial_sidebar_state="collapsed")


@st.cache_resource
def write_lock():
    return threading.Lock()


def load():
    try:
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    except Exception:
        return []


def save(data):
    with write_lock():
        tmp = RESULTS.with_name("results.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        tmp.replace(RESULTS)


def add_vote(vote):
    with write_lock():
        data = load()
        data.append(vote)
        tmp = RESULTS.with_name("results.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        tmp.replace(RESULTS)
    return len(data)


qp = st.query_params

# ------------------------------------------------------------------ reset
if qp.get("reset") == "nightshift":
    save([])
    st.success("All survey answers cleared. Open the main page to present.")
    st.stop()

# ------------------------------------------------------------------ phone survey
if "vote" in qp:
    st.markdown(
        """
        <style>
          #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stHeader"] {display:none !important;}
          .stApp {background: radial-gradient(120% 70% at 50% 0%, #2a2a6e, #0b1026 65%); color:#f6ecd2;}
          .block-container {max-width: 480px; padding-top: 1.6rem;}
          h1, h2, h3, p, label, span, div {color:#f6ecd2;}
          .stButton > button, .stFormSubmitButton > button {width:100%; background:#ffcf8a !important; color:#1b1530 !important; border:none; border-radius:14px; padding:.8rem; font-weight:700; font-size:1.05rem;}
          .moon {width:64px;height:64px;border-radius:50%;box-shadow: inset -18px -6px 0 0 #f6ecd2; transform:rotate(-24deg); margin-bottom:.6rem;}
        </style>
        <div class="moon"></div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### 🌙 The Night Shift\n**How did you sleep last night?** Anonymous · 20 seconds")

    if st.session_state.get("voted"):
        h = st.session_state["voted"]
        st.success(f"Thanks! You slept **{h} h**. Teens need 8–10 h, adults 7+ h.")
        st.markdown("👀 **Now look at the big screen.**")
        st.stop()

    with st.form("survey"):
        bed = st.select_slider(
            "1 · What time did you go to bed?",
            options=["21:00", "21:30", "22:00", "22:30", "23:00", "23:30", "00:00", "00:30", "01:00", "01:30", "02:00+"],
            value="00:00",
        )
        hours = st.slider("2 · How many hours did you actually sleep?", 3.0, 12.0, 7.0, 0.5)
        phone = st.radio("3 · Did you use your phone in bed?", ["yes", "no"], horizontal=True)
        feel = st.radio("4 · How do you feel right now?", ["😵 tired", "😐 ok", "😊 fresh"], horizontal=True)
        if st.form_submit_button("Send ☾"):
            add_vote({"bed": bed, "h": hours, "phone": phone == "yes",
                      "feel": feel.split(" ")[1], "t": int(time.time())})
            st.session_state["voted"] = hours
            st.rerun()
    st.stop()

# ------------------------------------------------------------------ presentation
st.markdown(
    """
    <style>
      #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
      [data-testid="stStatusWidget"], [data-testid="stHeader"] {display:none !important;}
      .stApp, .main, .block-container {padding:0 !important; margin:0 !important; max-width:100% !important; background:#0b1026;}
      iframe {position:fixed !important; inset:0 !important; width:100vw !important; height:100vh !important; border:0 !important; z-index:9999;}
    </style>
    """,
    unsafe_allow_html=True,
)
components.html((ROOT / "site.html").read_text(encoding="utf-8"), height=900, scrolling=False)
