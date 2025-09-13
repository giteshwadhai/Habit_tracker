#!/usr/bin/env python3
"""
HabitTracker Pro - Streamlit Version
A modern, interactive habit tracking application for Streamlit Cloud
"""

import streamlit as st
import sqlite3
import hashlib
import datetime
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="HabitTracker Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .habit-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #6366f1;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.9rem;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Database functions
def init_database():
    """Initialize the SQLite database"""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            color TEXT DEFAULT '#6366f1',
            icon TEXT DEFAULT 'fas fa-check-circle',
            frequency TEXT DEFAULT 'daily',
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            date DATE DEFAULT CURRENT_DATE,
            completed BOOLEAN DEFAULT FALSE,
            notes TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total_points INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            longest_streak INTEGER DEFAULT 0,
            total_habits_completed INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT DEFAULT 'fas fa-trophy',
            color TEXT DEFAULT '#f59e0b',
            points INTEGER DEFAULT 10,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate user login"""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?', 
                   (username, password_hash))
    user = cursor.fetchone()
    
    conn.close()
    return user

def register_user(username, email, password):
    """Register a new user"""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                       (username, email, password_hash))
        user_id = cursor.lastrowid
        
        # Create user stats
        cursor.execute('INSERT INTO user_stats (user_id) VALUES (?)', (user_id,))
        
        # Create initial achievements
        achievements = [
            ('Welcome!', 'Welcome to HabitTracker Pro!', 'fas fa-baby', '#10b981'),
            ('First Steps', 'You\'re ready to start your journey!', 'fas fa-rocket', '#6366f1')
        ]
        
        for name, desc, icon, color in achievements:
            cursor.execute('INSERT INTO achievements (user_id, name, description, icon, color) VALUES (?, ?, ?, ?, ?)',
                           (user_id, name, desc, icon, color))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_habits(user_id):
    """Get all habits for a user"""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM habits WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    habits = cursor.fetchall()
    
    conn.close()
    return habits

def get_habit_logs(habit_id, days=30):
    """Get habit logs for the last N days"""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    start_date = datetime.now().date() - timedelta(days=days)
    cursor.execute('''
        SELECT date, completed FROM habit_logs 
        WHERE habit_id = ? AND date >= ? 
        ORDER BY date DESC
    ''', (habit_id, start_date))
    
    logs = cursor.fetchall()
    conn.close()
    return logs

def toggle_habit(habit_id, date):
    """Toggle habit completion for a specific date"""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    # Check if log exists
    cursor.execute('SELECT id, completed FROM habit_logs WHERE habit_id = ? AND date = ?',
                   (habit_id, date))
    log = cursor.fetchone()
    
    if log:
        # Update existing log
        cursor.execute('UPDATE habit_logs SET completed = ? WHERE id = ?',
                       (not log[1], log[0]))
    else:
        # Create new log
        cursor.execute('INSERT INTO habit_logs (habit_id, date, completed) VALUES (?, ?, ?)',
                       (habit_id, date, True))
    
    conn.commit()
    conn.close()

def add_habit(user_id, name, description, category, color, icon, frequency):
    """Add a new habit"""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO habits (name, description, category, color, icon, frequency, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, description, category, color, icon, frequency, user_id))
    
    conn.commit()
    conn.close()

def get_user_stats(user_id):
    """Get user statistics"""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    stats = cursor.fetchone()
    
    conn.close()
    return stats

def get_user_achievements(user_id):
    """Get user achievements"""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM achievements WHERE user_id = ? ORDER BY unlocked_at DESC', (user_id,))
    achievements = cursor.fetchone()
    
    conn.close()
    return achievements

# Initialize database
init_database()

# Session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Main app
def main():
    if st.session_state.user is None:
        show_auth_page()
    else:
        show_dashboard()

def show_auth_page():
    """Show authentication page"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 HabitTracker Pro</h1>
        <p>Build Better Habits, One Day at a Time</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Welcome Back!")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        st.subheader("Create Account")
        
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif register_user(username, email, password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username or email already exists")

def show_dashboard():
    """Show main dashboard"""
    user = st.session_state.user
    user_id = user[0]
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="main-header">
            <h2>Welcome back, {user[1]}! 👋</h2>
            <p>Ready to build some amazing habits today?</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("➕ Add Habit"):
            st.session_state.page = 'add_habit'
            st.rerun()
    
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.rerun()
    
    # Stats
    stats = get_user_stats(user_id)
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="stats-card">
                <h3>Level</h3>
                <h2>{}</h2>
            </div>
            """.format(stats[2]), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stats-card">
                <h3>Points</h3>
                <h2>{}</h2>
            </div>
            """.format(stats[1]), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stats-card">
                <h3>Streak</h3>
                <h2>{}</h2>
            </div>
            """.format(stats[3]), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stats-card">
                <h3>Habits</h3>
                <h2>{}</h2>
            </div>
            """.format(stats[4]), unsafe_allow_html=True)
    
    # Habits
    st.subheader("🎯 Your Habits")
    habits = get_user_habits(user_id)
    
    if habits:
        for habit in habits:
            habit_id, name, description, category, color, icon, frequency, user_id, created_at = habit
            
            # Get today's completion status
            today = datetime.now().date()
            logs = get_habit_logs(habit_id, 1)
            completed_today = any(log[1] for log in logs if log[0] == today)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="habit-card">
                    <h4>{name}</h4>
                    <p>{description or 'No description'}</p>
                    <span style="background: {color}; color: white; padding: 0.25rem 0.5rem; border-radius: 10px; font-size: 0.8rem;">{category}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✅" if completed_today else "⭕", key=f"toggle_{habit_id}"):
                    toggle_habit(habit_id, today)
                    st.rerun()
    else:
        st.info("No habits yet! Click 'Add Habit' to get started.")
    
    # Achievements
    achievements = get_user_achievements(user_id)
    if achievements:
        st.subheader("🏆 Recent Achievements")
        st.markdown(f"""
        <div class="achievement-badge">
            {achievements[2]} - {achievements[3]}
        </div>
        """, unsafe_allow_html=True)
    
    # Insights
    st.subheader("🧠 Smart Insights")
    insights = [
        "Consistency is key to building lasting habits. Try to complete your habits at the same time each day.",
        "Research shows it takes an average of 66 days to form a new habit. Keep going!",
        "Celebrate small wins to stay motivated and build momentum."
    ]
    
    insight = random.choice(insights)
    st.markdown(f"""
    <div class="insight-card">
        <h4>💡 Pro Tip</h4>
        <p>{insight}</p>
    </div>
    """, unsafe_allow_html=True)

def show_add_habit():
    """Show add habit page"""
    st.subheader("➕ Add New Habit")
    
    with st.form("add_habit_form"):
        name = st.text_input("Habit Name", placeholder="e.g., Drink 8 glasses of water")
        description = st.text_area("Description (Optional)", placeholder="Add a description...")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["health", "fitness", "learning", "productivity", "mindfulness"])
        with col2:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "custom"])
        
        col1, col2 = st.columns(2)
        with col1:
            color = st.color_picker("Color", "#6366f1")
        with col2:
            icon = st.selectbox("Icon", ["fas fa-check-circle", "fas fa-heart", "fas fa-dumbbell", "fas fa-book", "fas fa-water"])
        
        submit = st.form_submit_button("Create Habit")
        
        if submit:
            if name:
                add_habit(st.session_state.user[0], name, description, category, color, icon, frequency)
                st.success("Habit created successfully!")
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("Please enter a habit name")

# Run the app
if __name__ == "__main__":
    if st.session_state.page == 'add_habit':
        show_add_habit()
    else:
        main()
