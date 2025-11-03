# quiz_app.py
# Quiz Master Pro – Play, Learn, Compete!
# Streamlit + Pandas = Full Quiz App

import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Quiz Master Pro",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);}
    .stApp {background-color: #0f1621;}
    h1 {color: #00ff88 !important; text-align: center; font-family: 'Arial';}
    .stButton > button {background: #00ff88; color: black; font-weight: bold; border-radius: 10px; width: 100%;}
    .option-btn {padding: 15px; margin: 8px 0; border-radius: 12px; font-size: 1.1em; text-align: left;}
    .correct {background: #00ff88; color: black;}
    .wrong {background: #ff4d4d; color: white;}
    .timer {font-size: 1.5em; color: #ffd700; text-align: center; font-weight: bold;}
    .score-box {background: #16213e; padding: 20px; border-radius: 15px; text-align: center; font-size: 2em; color: #00ff88;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Quiz Master Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#aaa;'>Test your knowledge. Beat the timer. Climb the leaderboard!</p>", unsafe_allow_html=True)

# Sample Questions
QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris",
        "category": "Geography"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars",
        "category": "Science"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Van Gogh", "Picasso", "Da Vinci", "Michelangelo"],
        "answer": "Da Vinci",
        "category": "Art"
    },
    {
        "question": "What is 15 + 27?",
        "options": ["32", "42", "52", "62"],
        "answer": "42",
        "category": "Math"
    },
    {
        "question": "In which year did World War II end?",
        "options": ["1943", "1945", "1947", "1950"],
        "answer": "1945",
        "category": "History"
    }
]

# Initialize Session State
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'selected' not in st.session_state:
    st.session_state.selected = None
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

# -----------------------------
# START QUIZ
# -----------------------------
if not st.session_state.quiz_started:
    col1, col2 = st.columns(2)
    with col1:
        st.info("5 Questions")
    with col2:
        st.info("30 Seconds per Question")
    
    player_name = st.text_input("Enter your name", placeholder="Quiz Champion")
    if st.button("Start Quiz", use_container_width=True):
        if player_name.strip():
            st.session_state.player_name = player_name.strip()
            st.session_state.quiz_started = True
            st.session_state.questions = random.sample(QUESTIONS, len(QUESTIONS))
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.error("Enter your name!")

# -----------------------------
# QUIZ IN PROGRESS
# -----------------------------
if st.session_state.quiz_started and st.session_state.current_q < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current_q]
    
    # Timer
    elapsed = int(time.time() - st.session_state.start_time)
    time_left = max(30 - elapsed, 0)
    st.markdown(f"<div class='timer'>⏱ {time_left}s</div>", unsafe_allow_html=True)
    
    if time_left == 0:
        st.session_state.show_result = True
        st.rerun()
    
    st.markdown(f"### Question {st.session_state.current_q + 1}/{len(st.session_state.questions)}")
    st.markdown(f"**{q['question']}**")
    st.markdown(f"<small>Category: {q['category']}</small>", unsafe_allow_html=True)
    
    for option in q['options']:
        btn_class = ""
        if st.session_state.show_result:
            if option == q['answer']:
                btn_class = "correct"
            elif option == st.session_state.selected:
                btn_class = "wrong"
        
        if st.button(option, key=option, disabled=st.session_state.show_result, use_container_width=True):
            st.session_state.selected = option
            st.session_state.show_result = True
            if option == q['answer']:
                st.session_state.score += 1
            st.rerun()
    
    if st.session_state.show_result:
        if st.session_state.selected == q['answer']:
            st.success("Correct!")
        else:
            st.error(f"Wrong! Answer: **{q['answer']}**")
        
        if st.button("Next Question", use_container_width=True):
            st.session_state.current_q += 1
            st.session_state.selected = None
            st.session_state.show_result = False
            st.session_state.start_time = time.time()
            st.rerun()

# -----------------------------
# QUIZ COMPLETE
# -----------------------------
if st.session_state.quiz_started and st.session_state.current_q >= len(st.session_state.questions):
    st.markdown("<div class='score-box'>Quiz Complete!</div>", unsafe_allow_html=True)
    st.markdown(f"### {st.session_state.player_name}, Your Score: **{st.session_state.score}/{len(QUESTIONS)}**")
    
    # Save to Leaderboard
    st.session_state.leaderboard.append({
        'name': st.session_state.player_name,
        'score': st.session_state.score,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    leaderboard_df = pd.DataFrame(st.session_state.leaderboard).sort_values('score', ascending=False)
    
    st.markdown("### Leaderboard")
    st.dataframe(leaderboard_df, use_container_width=True, hide_index=True)
    
    if st.button("Play Again"):
        for key in ['quiz_started', 'current_q', 'score', 'selected', 'show_result', 'start_time']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# -----------------------------
# PREMIUM
# -----------------------------
st.markdown("---")
st.info("**Premium ($1.99/mo):** Create Custom Quizzes, PDF Certificates, Multiplayer, Dark Mode!")
if st.button("Unlock Pro"):
    st.balloons()

st.caption("Built with Streamlit + uv | Learn, Play, Win!")