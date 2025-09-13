from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Habit, HabitLog, AIInsight, UserStats, Achievement, HabitGoal
from app import db
from datetime import datetime, timedelta
import random
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def register_routes(app):
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('index.html')
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        habits = Habit.query.filter_by(user_id=current_user.id, is_active=True).all()
        
        # Calculate stats
        total_habits = len(habits)
        completed_today = sum(1 for habit in habits if habit.completed_today)
        longest_streak = max([habit.streak for habit in habits], default=0)
        weekly_completion = int(sum(habit.completion_rate for habit in habits) / total_habits) if total_habits > 0 else 0
        
        # Get user stats
        user_stats = UserStats.query.filter_by(user_id=current_user.id).first()
        if not user_stats:
            user_stats = UserStats(user_id=current_user.id)
            db.session.add(user_stats)
            db.session.commit()
        
        # Get recent achievements
        achievements = Achievement.query.filter_by(user_id=current_user.id).order_by(Achievement.unlocked_at.desc()).limit(5).all()
        
        # Get AI insights
        insights = AIInsight.query.filter_by(user_id=current_user.id).order_by(AIInsight.created_at.desc()).limit(4).all()
        
        return render_template('dashboard.html', 
                              habits=habits, 
                              total_habits=total_habits,
                              completed_today=completed_today,
                              longest_streak=longest_streak,
                              weekly_completion=weekly_completion,
                              user_stats=user_stats,
                              achievements=achievements,
                              insights=insights)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validate form data
            if not all([username, email, password, confirm_password]):
                flash('All fields are required', 'danger')
                return redirect(url_for('register'))
                
            if password != confirm_password:
                flash('Passwords do not match', 'danger')
                return redirect(url_for('register'))
                
            # Check if user already exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('register'))
                
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))
                
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            # Create initial AI insights
            create_initial_insights(new_user.id)
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
            
        return render_template('register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember = 'remember' in request.form
            
            user = User.query.filter_by(email=email).first()
            
            if not user or not check_password_hash(user.password_hash, password):
                flash('Invalid email or password', 'danger')
                return redirect(url_for('login'))
                
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
            
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/habits/new', methods=['GET', 'POST'])
    @login_required
    def new_habit():
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            category = request.form.get('category')
            color = request.form.get('color', '#6366f1')
            icon = request.form.get('icon', 'fas fa-check-circle')
            frequency = request.form.get('frequency', 'daily')
            
            if not all([name, category]):
                flash('Name and category are required', 'danger')
                return redirect(url_for('new_habit'))
                
            new_habit = Habit(
                name=name,
                description=description,
                category=category,
                color=color,
                icon=icon,
                frequency=frequency,
                user_id=current_user.id
            )
            
            db.session.add(new_habit)
            db.session.commit()
            
            # Create initial goal for the habit
            initial_goal = HabitGoal(
                habit_id=new_habit.id,
                title=f"Complete {name} for 7 days",
                description=f"Build consistency by completing this habit for a full week",
                target_value=7,
                target_date=datetime.utcnow().date() + timedelta(days=7)
            )
            db.session.add(initial_goal)
            db.session.commit()
            
            # Update user stats
            update_user_stats(current_user.id)
            
            flash(f'Habit "{name}" created successfully! 🎉', 'success')
            return redirect(url_for('dashboard'))
            
        return render_template('new_habit.html')
    
    @app.route('/habits/<int:habit_id>/toggle', methods=['POST'])
    @login_required
    def toggle_habit(habit_id):
        habit = Habit.query.get_or_404(habit_id)
        
        # Ensure habit belongs to current user
        if habit.user_id != current_user.id:
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
            
        today = datetime.utcnow().date()
        log = HabitLog.query.filter_by(habit_id=habit.id, date=today).first()
        
        if log:
            log.completed = not log.completed
        else:
            log = HabitLog(habit_id=habit.id, date=today, completed=True)
            db.session.add(log)
            
        db.session.commit()
        
        # Update user stats and check achievements
        update_user_stats(current_user.id)
        
        # Update habit goals
        update_habit_goals(habit.id)
        
        # Generate new insights occasionally
        if random.random() < 0.3:  # 30% chance
            generate_new_insight(current_user.id)
        
        return redirect(url_for('dashboard'))
    
    @app.route('/habits/<int:habit_id>/delete', methods=['POST'])
    @login_required
    def delete_habit(habit_id):
        habit = Habit.query.get_or_404(habit_id)
        
        # Ensure habit belongs to current user
        if habit.user_id != current_user.id:
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
            
        db.session.delete(habit)
        db.session.commit()
        
        flash(f'Habit "{habit.name}" deleted successfully', 'success')
        return redirect(url_for('dashboard'))
    
    @app.route('/insights')
    @login_required
    def insights():
        habits = Habit.query.filter_by(user_id=current_user.id).all()
        insights = AIInsight.query.filter_by(user_id=current_user.id).order_by(AIInsight.created_at.desc()).all()
        
        # Generate visualization data
        habit_data = []
        for habit in habits:
            logs = HabitLog.query.filter_by(habit_id=habit.id).order_by(HabitLog.date).all()
            dates = [log.date.strftime('%Y-%m-%d') for log in logs]
            completions = [1 if log.completed else 0 for log in logs]
            habit_data.append({
                'name': habit.name,
                'category': habit.category,
                'dates': dates,
                'completions': completions
            })
        
        return render_template('insights.html', habits=habits, insights=insights, habit_data=habit_data)
    
    @app.route('/api/generate-insight', methods=['POST'])
    @login_required
    def api_generate_insight():
        insight = generate_new_insight(current_user.id)
        return jsonify({
            'id': insight.id,
            'type': insight.type,
            'title': insight.title,
            'message': insight.message,
            'confidence': insight.confidence
        })

# Helper functions
def update_user_stats(user_id):
    """Update user statistics and check for achievements"""
    user = User.query.get(user_id)
    if not user:
        return
    
    # Get or create user stats
    user_stats = UserStats.query.filter_by(user_id=user_id).first()
    if not user_stats:
        user_stats = UserStats(user_id=user_id)
        db.session.add(user_stats)
    
    # Calculate stats
    habits = Habit.query.filter_by(user_id=user_id, is_active=True).all()
    total_completed = sum(habit.streak for habit in habits)
    longest_streak = max([habit.streak for habit in habits], default=0)
    
    # Update stats
    user_stats.total_habits_completed = total_completed
    user_stats.longest_streak = max(user_stats.longest_streak, longest_streak)
    user_stats.total_points = total_completed * 10  # 10 points per day
    user_stats.level = (user_stats.total_points // 100) + 1
    user_stats.last_updated = datetime.utcnow()
    
    # Check for achievements
    check_achievements(user_id, user_stats)
    
    db.session.commit()

def check_achievements(user_id, user_stats):
    """Check and create new achievements for user"""
    existing_achievements = [a.name for a in Achievement.query.filter_by(user_id=user_id).all()]
    
    # First habit achievement
    if user_stats.total_habits_completed >= 1 and "First Steps" not in existing_achievements:
        create_achievement(user_id, "First Steps", "Completed your first habit!", "fas fa-baby", "#10b981")
    
    # Week warrior
    if user_stats.total_habits_completed >= 7 and "Week Warrior" not in existing_achievements:
        create_achievement(user_id, "Week Warrior", "Completed habits for 7 days!", "fas fa-calendar-week", "#6366f1")
    
    # Month master
    if user_stats.total_habits_completed >= 30 and "Month Master" not in existing_achievements:
        create_achievement(user_id, "Month Master", "Completed habits for 30 days!", "fas fa-calendar-alt", "#8b5cf6")
    
    # Streak master
    if user_stats.longest_streak >= 10 and "Streak Master" not in existing_achievements:
        create_achievement(user_id, "Streak Master", f"Maintained a {user_stats.longest_streak}-day streak!", "fas fa-fire", "#f59e0b")
    
    # Level up achievements
    if user_stats.level >= 5 and "Rising Star" not in existing_achievements:
        create_achievement(user_id, "Rising Star", f"Reached level {user_stats.level}!", "fas fa-star", "#ec4899")
    
    if user_stats.level >= 10 and "Habit Hero" not in existing_achievements:
        create_achievement(user_id, "Habit Hero", f"Reached level {user_stats.level}!", "fas fa-crown", "#f59e0b")

def create_achievement(user_id, name, description, icon, color):
    """Create a new achievement for user"""
    achievement = Achievement(
        user_id=user_id,
        name=name,
        description=description,
        icon=icon,
        color=color,
        points=10
    )
    db.session.add(achievement)

def update_habit_goals(habit_id):
    """Update habit goals based on completion"""
    habit = Habit.query.get(habit_id)
    if not habit:
        return
    
    # Get active goals for this habit
    goals = HabitGoal.query.filter_by(habit_id=habit_id, is_achieved=False).all()
    
    for goal in goals:
        # Count completed days since goal creation
        completed_days = HabitLog.query.filter(
            HabitLog.habit_id == habit_id,
            HabitLog.completed == True,
            HabitLog.date >= goal.created_at.date()
        ).count()
        
        goal.current_value = completed_days
        
        # Check if goal is achieved
        if goal.current_value >= goal.target_value:
            goal.is_achieved = True
            goal.current_value = goal.target_value  # Cap at target value
    
    db.session.commit()

def create_initial_insights(user_id):
    """Create initial AI insights for new users"""
    insights = [
        {
            'type': 'motivation',
            'title': 'Welcome to Your Habit Ally!',
            'message': 'Starting new habits can increase your chances of long-term success by 80%. Begin with small, consistent actions!',
            'confidence': 95
        },
        {
            'type': 'tip',
            'title': 'Morning Routine Tip',
            'message': 'Research shows that habits formed in the morning have a 40% higher success rate. Try adding a new habit to your morning routine.',
            'confidence': 88
        },
        {
            'type': 'improvement',
            'title': 'Habit Stacking',
            'message': 'Link new habits to existing ones for better consistency. For example, meditate right after brushing your teeth.',
            'confidence': 92
        }
    ]
    
    for insight_data in insights:
        insight = AIInsight(
            user_id=user_id,
            type=insight_data['type'],
            title=insight_data['title'],
            message=insight_data['message'],
            confidence=insight_data['confidence']
        )
        db.session.add(insight)
    
    db.session.commit()

def generate_new_insight(user_id):
    """Generate a new AI insight based on user's habit data"""
    habits = Habit.query.filter_by(user_id=user_id).all()
    
    if not habits:
        # Default insight if no habits exist
        insight = AIInsight(
            user_id=user_id,
            type='tip',
            title='Start Your First Habit',
            message='Creating your first habit is the most important step. Start with something small and achievable to build momentum.',
            confidence=90
        )
    else:
        # Analyze habit data to generate personalized insight
        insight_types = ['motivation', 'improvement', 'trend', 'tip']
        selected_type = random.choice(insight_types)
        
        if selected_type == 'motivation':
            # Find habit with highest streak
            best_habit = max(habits, key=lambda h: h.streak)
            if best_habit.streak > 0:
                insight = AIInsight(
                    user_id=user_id,
                    type='motivation',
                    title=f'Great Progress on {best_habit.name}!',
                    message=f'You\'ve maintained a {best_habit.streak}-day streak on {best_habit.name}. This consistency is building strong neural pathways. Keep it up!',
                    confidence=random.randint(85, 95)
                )
            else:
                insight = AIInsight(
                    user_id=user_id,
                    type='motivation',
                    title='You Can Do This!',
                    message='Every habit master started as a beginner. Focus on consistency rather than perfection to build lasting habits.',
                    confidence=random.randint(85, 95)
                )
                
        elif selected_type == 'improvement':
            # Find habit with lowest completion rate
            worst_habit = min(habits, key=lambda h: h.completion_rate)
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            random_day = random.choice(day_names)
            
            insight = AIInsight(
                user_id=user_id,
                type='improvement',
                title='Optimization Suggestion',
                message=f'Your {worst_habit.name} completion rate is lower than other habits. Consider scheduling it on {random_day}s when you might have more energy or time.',
                confidence=random.randint(80, 90)
            )
            
        elif selected_type == 'trend':
            # Random positive trend insight
            random_habit = random.choice(habits)
            improvement = random.randint(10, 30)
            
            insight = AIInsight(
                user_id=user_id,
                type='trend',
                title='Positive Trend Detected',
                message=f'Your {random_habit.name} habit shows {improvement}% improvement over the last two weeks. Great progress!',
                confidence=random.randint(85, 95)
            )
            
        else:  # tip
            tips = [
                'Try the 2-minute rule: If a habit takes less than 2 minutes, do it immediately.',
                'Visual cues can increase habit success by 30%. Place a visual reminder where you\'ll see it daily.',
                'Tracking your habits creates a visual proof of your progress, increasing motivation.',
                'Celebrate small wins to release dopamine and reinforce your habit loop.',
                'If you miss a day, don\'t break the chain twice. Getting back on track immediately is key to long-term success.'
            ]
            
            insight = AIInsight(
                user_id=user_id,
                type='tip',
                title='Habit Building Tip',
                message=random.choice(tips),
                confidence=random.randint(88, 98)
            )
    
    db.session.add(insight)
    db.session.commit()
    
    return insight