from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(200))  # URL to avatar image
    timezone = db.Column(db.String(50), default='UTC')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    habits = db.relationship('Habit', backref='user', lazy=True, cascade='all, delete-orphan')
    insights = db.relationship('AIInsight', backref='user', lazy=True, cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', backref='user', lazy=True, cascade='all, delete-orphan')
    stats = db.relationship('UserStats', backref='user', lazy=True, cascade='all, delete-orphan', uselist=False)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(20), default='daily')  # daily, weekly, custom
    target_days = db.Column(db.Integer, default=1)  # days per week for weekly habits
    color = db.Column(db.String(7), default='#6366f1')  # hex color for UI
    icon = db.Column(db.String(50), default='fas fa-check-circle')  # FontAwesome icon
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    logs = db.relationship('HabitLog', backref='habit', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('HabitGoal', backref='habit', lazy=True, cascade='all, delete-orphan')
    
    @property
    def streak(self):
        # Calculate current streak
        logs = HabitLog.query.filter_by(habit_id=self.id, completed=True).order_by(HabitLog.date.desc()).all()
        if not logs:
            return 0
            
        streak = 1
        for i in range(len(logs) - 1):
            if (logs[i].date - logs[i+1].date).days == 1:
                streak += 1
            else:
                break
                
        return streak
    
    @property
    def completion_rate(self):
        # Calculate weekly completion rate
        today = datetime.utcnow().date()
        week_ago = today - datetime.timedelta(days=7)
        
        logs = HabitLog.query.filter(
            HabitLog.habit_id == self.id,
            HabitLog.date >= week_ago,
            HabitLog.date <= today
        ).all()
        
        if not logs:
            return 0
            
        completed = sum(1 for log in logs if log.completed)
        return int((completed / len(logs)) * 100)
    
    @property
    def completed_today(self):
        today = datetime.utcnow().date()
        log = HabitLog.query.filter_by(habit_id=self.id, date=today).first()
        return log.completed if log else False
    
    def __repr__(self):
        return f"Habit('{self.name}', '{self.category}')"

class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f"HabitLog(Habit ID: {self.habit_id}, Date: {self.date}, Completed: {self.completed})"

class HabitGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    target_value = db.Column(db.Integer, nullable=False)  # target number of completions
    current_value = db.Column(db.Integer, default=0)
    target_date = db.Column(db.Date)
    is_achieved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min(int((self.current_value / self.target_value) * 100), 100)
    
    def __repr__(self):
        return f"HabitGoal('{self.title}', {self.current_value}/{self.target_value})"

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default='fas fa-trophy')
    color = db.Column(db.String(7), default='#f59e0b')
    points = db.Column(db.Integer, default=10)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Achievement('{self.name}')"

class UserStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    longest_streak = db.Column(db.Integer, default=0)
    total_habits_completed = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def next_level_points(self):
        return self.level * 100
    
    @property
    def progress_to_next_level(self):
        if self.next_level_points == 0:
            return 0
        return min(int((self.total_points % self.next_level_points) / self.next_level_points * 100), 100)
    
    def __repr__(self):
        return f"UserStats(User: {self.user_id}, Level: {self.level}, Points: {self.total_points})"

class AIInsight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # motivation, improvement, trend, tip
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.Integer, nullable=False)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"AIInsight('{self.type}', '{self.title}')"