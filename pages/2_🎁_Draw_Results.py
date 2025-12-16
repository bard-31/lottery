
You said:
import streamlit as st

st.set_page_config(
    page_title="Prize Draw Setup",
    page_icon="🎁",
    layout="wide"
)

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

# Generate numbers automatically
numbers = list(range(1, end_number + 1))

# -----------------------
# Prize Input (textarea for reliability)
# -----------------------
st.subheader("🏆 Prize List (Up to 1,000 prizes)")

prize_input = st.text_area(
    "Enter ONE prize per line",
    height=300,
    placeholder="Prize 1\nPrize 2\nPrize 3\n..."
)

# Parse prizes
prizes = [p.strip() for p in prize_input.split("\n") if p.strip()]

if len(prizes) == 0:
    st.warning("Please enter at least one prize.")
elif len(prizes) > 1000:
    st.error("Maximum 1,000 prizes allowed.")

# -----------------------
# Display in “old style” multiple input look
# -----------------------
st.markdown("### Prize Preview")
cols_per_row = 5
rows = (len(prizes) + cols_per_row - 1) // cols_per_row

for r in range(rows):
    cols = st.columns(cols_per_row)
    for c, prize in enumerate(prizes[r*cols_per_row:(r+1)*cols_per_row]):
        with cols[c]:
            st.text_input(f"Prize {r*cols_per_row+c+1}", value=prize, disabled=True)

# -----------------------
# Start Session
# -----------------------
if st.button("🚀 Start Draw Session", use_container_width=True):
    if len(prizes) == 0:
        st.stop()

    if len(numbers) < len(prizes):
        st.error("Number range must be greater than or equal to number of prizes.")
        st.stop()

    # Save originals
    st.session_state["original_numbers"] = numbers[:]
    st.session_state["original_prizes"] = prizes.copy()
    st.session_state["available_numbers"] = st.session_state["original_numbers"][:]
    st.session_state["available_prizes"] = st.session_state["original_prizes"][:]

    # Reset draw state
    st.session_state["used_pairs"] = []
    st.session_state["current_draw"] = []
    st.session_state["confirm_return"] = None

    st.success(f"✅ Session started with {len(prizes)} prizes")
    st.switch_page("pages/2_🎁_Draw_Results.py")
