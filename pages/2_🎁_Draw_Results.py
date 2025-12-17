import streamlit as st
import random
import math
import base64

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Draw Results", page_icon="🎁", layout="wide")

# -----------------------
# Full-Size Background (original resolution, no blur, no zoom)
# -----------------------
def set_fullsize_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        /* Main app background */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: 90%;          /* original size */
            background-position: center;    /* Centered */
            background-repeat: no-repeat;   /* No tiling */
            background-attachment: fixed;   /* Stays fixed on scroll */
        }}

        /* Glass effect for main content */
        [data-testid="stAppViewContainer"] > .main {{
            background: rgba(255, 255, 255, 0.75);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use your image file
set_fullsize_bg("pages/bgluckydraw.jpg")

# -----------------------
# Title
# -----------------------
st.markdown(
    """
    <h1 style="
        color: #FFD54F;
        text-align: center;
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.45);
        margin-bottom: 20px;
    ">
        🎁 PRIVASIA'S ARENA OF CHAMPIONS - LUCKY DRAW 🎁
    </h1>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Session Validation
# -----------------------
required_keys = ["available_numbers", "available_prizes", "original_numbers", "original_prizes"]
for key in required_keys:
    if key not in st.session_state:
        st.error("❌ Session not found. Please start from the setup page.")
        st.stop()

# -----------------------
# Initialize session state
# -----------------------
st.session_state.setdefault("used_pairs", [])
st.session_state.setdefault("current_draw", [])
st.session_state.setdefault("confirm_return", None)

# -----------------------
# Helper: render card
# -----------------------
def render_card(title, value, color, font_size, tooltip=None):
    tip = f'title="{tooltip}"' if tooltip else ""
    return f"""
    <div {tip} style="
        background:{color};
        padding:18px;
        border-radius:14px;
        text-align:center;
        color:white;
        box-shadow:0 4px 10px rgba(0,0,0,0.15);
        min-height:120px;
        font-family:Segoe UI, sans-serif;
        margin-bottom:12px;
    ">
        <div style="font-size:14px; opacity:0.85;">{title}</div>
        <div style="font-size:{font_size}px; font-weight:bold;">{value}</div>
    </div>
    """

# -----------------------
# Controls
# -----------------------
col1, col2 = st.columns(2)

with col1:
    has_returned = any(p["returned"] for p in st.session_state["used_pairs"])
    has_available = len(st.session_state["available_prizes"]) > 0

    if has_returned or has_available:
        if st.button("🎉 Draw Next Batch", use_container_width=True):

            batch_prizes = []
            returned_flag = {}

            if has_returned:
                for item in st.session_state["used_pairs"]:
                    if item["returned"]:
                        batch_prizes.append(item)
                        returned_flag[item["prize"]] = True
                        item["returned"] = False
                        item["number"] = None

            elif has_available:
                for _ in range(min(5, len(st.session_state["available_prizes"]))):
                    prize_name = st.session_state["available_prizes"].pop(0)
                    batch_prizes.append({"prize": prize_name, "number": None, "returned": False})
                    returned_flag[prize_name] = False

            if len(st.session_state["available_numbers"]) < len(batch_prizes):
                st.error("Not enough numbers left for this batch.")
                st.stop()

            batch_numbers = random.sample(st.session_state["available_numbers"], len(batch_prizes))
            for item, num in zip(batch_prizes, batch_numbers):
                item["number"] = num
                st.session_state["available_numbers"].remove(num)
                if item not in st.session_state["used_pairs"]:
                    st.session_state["used_pairs"].append(item)

            for item in batch_prizes:
                item["was_returned"] = returned_flag.get(item["prize"], False)

            st.session_state["current_draw"] = batch_prizes
            st.balloons()
    else:
        st.markdown(
            """<div style="background:#E53935;color:white;padding:14px;border-radius:8px;text-align:center;font-weight:bold;">
            ❌ No More Prizes Left For This Draw
            </div>""",
            unsafe_allow_html=True
        )

with col2:
    if st.button("🆕 New Session", use_container_width=True):
        st.session_state["available_numbers"] = st.session_state["original_numbers"][:]
        st.session_state["available_prizes"] = st.session_state["original_prizes"][:]
        st.session_state["used_pairs"] = []
        st.session_state["current_draw"] = []
        st.session_state["confirm_return"] = None
        st.rerun()

# -----------------------
# Session Info
# -----------------------
remaining_prizes = len(st.session_state["available_prizes"]) + sum(p["returned"] for p in st.session_state["used_pairs"])
st.markdown(f"### 🧾 Session Info\n*Remaining Prizes:* {remaining_prizes}")

# -----------------------
# Current Draw
# -----------------------
if st.session_state["current_draw"]:
    st.markdown("---")
    st.subheader("🏆 Current Draw")

    num_cols = max(len(st.session_state["current_draw"]), 1)
    cols = st.columns(num_cols)
    for i, item in enumerate(st.session_state["current_draw"]):
        prize = item["prize"]
        number = item["number"]
        color = "#FF9800" if item.get("was_returned") else "#1E88E5"
        with cols[i]:
            st.markdown(render_card(prize, number, color, 34), unsafe_allow_html=True)

# -----------------------
# Numbers Already Drawn
# -----------------------
if st.session_state["used_pairs"]:
    st.markdown("---")
    st.subheader("🚫 Numbers Already Drawn")

    used_sorted = sorted(st.session_state["used_pairs"], key=lambda x: x["returned"])
    rows = math.ceil(len(used_sorted) / 10)

    for r in range(rows):
        cols = st.columns(10)
        for c, item in enumerate(used_sorted[r*10:(r+1)*10]):
            with cols[c]:
                prize = item["prize"]
                number = item["number"]
                returned = item["returned"]

                if returned:
                    st.markdown(render_card(prize, number, "#9E9E9E", 20, tooltip="Prize Returned"), unsafe_allow_html=True)
                else:
                    if st.button(f"{prize}\n{number}", key=f"select_{r}_{c}", use_container_width=True):
                        st.session_state["confirm_return"] = item
                        st.rerun()

# -----------------------
# Return Confirmation Modal
# -----------------------
if st.session_state["confirm_return"]:
    item = st.session_state["confirm_return"]
    st.markdown("---")
    st.warning(f"⚠️ Return prize *{item['prize']}* to next draw?")

    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("✅ Yes", use_container_width=True):
            item["returned"] = True
            st.session_state["confirm_return"] = None
            st.rerun()
    with col_no:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state["confirm_return"] = None
            st.rerun()
