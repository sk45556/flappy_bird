import streamlit as st
import random
import time

st.set_page_config(layout="centered")
st.title("🐤 Flappy Bird in Streamlit")

# --- Initialize Session State ---
if "y" not in st.session_state:
    st.session_state.y = 250
    st.session_state.vel = 0
    st.session_state.gravity = 2
    st.session_state.jump = -15
    st.session_state.pipe_x = 600
    st.session_state.pipe_gap = random.randint(100, 350)
    st.session_state.score = 0
    st.session_state.running = False
    st.session_state.jump_request = False

# --- Start Button ---
if st.button("🚀 Start / Restart Game"):
    st.session_state.y = 250
    st.session_state.vel = 0
    st.session_state.pipe_x = 600
    st.session_state.pipe_gap = random.randint(100, 350)
    st.session_state.score = 0
    st.session_state.running = True
    st.session_state.jump_request = False
    st.rerun()

# --- Jump Button ---
if st.session_state.running:
    if st.button("⬆️ Jump"):
        st.session_state.jump_request = True

# --- Game Logic ---
if st.session_state.running:
    if st.session_state.jump_request:
        st.session_state.vel = st.session_state.jump
        st.session_state.jump_request = False

    st.session_state.vel += st.session_state.gravity
    st.session_state.y += st.session_state.vel
    st.session_state.pipe_x -= 5

    # Pipe reset and scoring
    if st.session_state.pipe_x < -80:
        st.session_state.pipe_x = 600
        st.session_state.pipe_gap = random.randint(100, 350)
        st.session_state.score += 1

    # Collision detection
    if st.session_state.y < 0 or st.session_state.y > 480:
        st.session_state.running = False
    if 100 < st.session_state.pipe_x < 180:
        if not (st.session_state.pipe_gap < st.session_state.y < st.session_state.pipe_gap + 150):
            st.session_state.running = False

# --- Draw Game UI ---
game_area = st.empty()

bird_style = f"position:absolute; top:{int(st.session_state.y)}px; left:100px;"
pipe_top = f"position:absolute; top:0px; left:{st.session_state.pipe_x}px; height:{st.session_state.pipe_gap}px; width:80px; background-color:green;"
pipe_bottom = f"position:absolute; top:{st.session_state.pipe_gap+150}px; left:{st.session_state.pipe_x}px; height:{500 - st.session_state.pipe_gap - 150}px; width:80px; background-color:green;"

html = f"""
<div style='position:relative; width:600px; height:500px; background-color:skyblue; border:2px solid black; overflow:hidden'>
    <div style='{bird_style}'>🐤</div>
    <div style='{pipe_top}'></div>
    <div style='{pipe_bottom}'></div>
</div>
<p><strong>🏆 Score:</strong> {st.session_state.score}</p>
"""

game_area.markdown(html, unsafe_allow_html=True)

# --- Auto Refresh ---
if st.session_state.running:
    time.sleep(0.1)
    st.rerun()
else:
    if "y" in st.session_state:
        st.error("💥 Game Over!")
        st.success(f"🏆 Final Score: {st.session_state.score}")
