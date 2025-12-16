import streamlit as st
import base64

st.set_page_config(
    page_title="Prize Draw Setup",
    page_icon="🎁",
    layout="wide"
)

# -----------------------
# Blurred Background
# -----------------------
def set_blurred_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            filter: blur(14px);
            transform: scale(1.1);
            z-index: -1;
        }}

        /* Glass effect for main content */
        [data-testid="stAppViewContainer"] > .main {{
            background: rgba(255, 255, 255, 0.75);
            border-radius: 20px;
            padding: 2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_blurred_bg("pages/PRIVA_Logo-removebg-preview.png")

# -----------------------
# Title
# -----------------------
st.title("🎁 Prize Draw Setup")

# -----------------------
# Number Range
# -----------------------
st.subheader("🔢 Number Range (1 to N)")

end_number = st.number_input(
    "Enter the maximum number",
    min_value=1,
    value=50,
    step=1
)

numbers = list(range(1, end_number + 1))

# -----------------------
# Prize Input
# -----------------------
st.subheader("🏆 Prize List (Up to 1,000 prizes)")

prize_input = st.text_area(
    "Enter ONE prize per line",
    height=300,
    placeholder="Prize 1\nPrize 2\nPrize 3\n..."
)

prizes = [p.strip() for p in prize_input.split("\n") if p.strip()]

if len(prizes) == 0:
    st.warning("Please enter at least one prize.")
elif len(prizes) > 1000:
    st.error("Maximum 1,000 prizes allowed.")

# -----------------------
# Prize Preview
# -----------------------
st.markdown("### Prize Preview")

cols_per_row = 5
rows = (len(prizes) + cols_per_row - 1) // cols_per_row

for r in range(rows):
    cols = st.columns(cols_per_row)
    for c, prize in enumerate(prizes[r*cols_per_row:(r+1)*cols_per_row]):
        with cols[c]:
            st.text_input(
                f"Prize {r*cols_per_row + c + 1}",
                value=prize,
                disabled=True
            )

# -----------------------
# Start Session
# -----------------------
if st.button("🚀 Start Draw Session", use_container_width=True):
    if len(prizes) == 0:
        st.stop()

    if len(numbers) < len(prizes):
        st.error("Number range must be greater than or equal to number of prizes.")
        st.stop()

    st.session_state["original_numbers"] = numbers[:]
    st.session_state["original_prizes"] = prizes[:]
    st.session_state["available_numbers"] = numbers[:]
    st.session_state["available_prizes"] = prizes[:]

    st.session_state["used_pairs"] = []
    st.session_state["current_draw"] = []
    st.session_state["confirm_return"] = None

    st.success(f"✅ Session started with {len(prizes)} prizes")
    st.switch_page("pages/2_🎁_Draw_Results.py")
