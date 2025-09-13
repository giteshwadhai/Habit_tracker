#!/usr/bin/env python3
"""
HabitTracker Pro - Run Script
A modern, interactive habit tracking application built with Flask
"""

import os
import sys
from app import app, db
from models import User, Habit, HabitLog, HabitGoal, Achievement, UserStats, AIInsight

def create_sample_data():
    """Create sample data for demonstration"""
    print("Creating sample data...")
    
    # Check if we already have users
    if User.query.first():
        print("Sample data already exists. Skipping...")
        return
    
    # Create a sample user
    user = User(
        username='demo_user',
        email='demo@example.com',
        password_hash='$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/9yQK.2K'  # password: demo123
    )
    db.session.add(user)
    db.session.commit()
    
    # Create sample habits
    habits_data = [
        {
            'name': 'Morning Exercise',
            'description': '30 minutes of cardio or strength training',
            'category': 'fitness',
            'color': '#10b981',
            'icon': 'fas fa-dumbbell',
            'frequency': 'daily'
        },
        {
            'name': 'Read for 30 minutes',
            'description': 'Read books or articles to expand knowledge',
            'category': 'learning',
            'color': '#6366f1',
            'icon': 'fas fa-book',
            'frequency': 'daily'
        },
        {
            'name': 'Meditation',
            'description': '10 minutes of mindfulness meditation',
            'category': 'mindfulness',
            'color': '#8b5cf6',
            'icon': 'fas fa-leaf',
            'frequency': 'daily'
        },
        {
            'name': 'Drink 8 glasses of water',
            'description': 'Stay hydrated throughout the day',
            'category': 'health',
            'color': '#06b6d4',
            'icon': 'fas fa-tint',
            'frequency': 'daily'
        }
    ]
    
    for habit_data in habits_data:
        habit = Habit(
            name=habit_data['name'],
            description=habit_data['description'],
            category=habit_data['category'],
            color=habit_data['color'],
            icon=habit_data['icon'],
            frequency=habit_data['frequency'],
            user_id=user.id
        )
        db.session.add(habit)
        db.session.commit()
        
        # Create initial goal for each habit
        goal = HabitGoal(
            habit_id=habit.id,
            title=f"Complete {habit.name} for 7 days",
            description=f"Build consistency by completing this habit for a full week",
            target_value=7,
            target_date='2024-12-31'
        )
        db.session.add(goal)
    
    # Create user stats
    user_stats = UserStats(
        user_id=user.id,
        total_points=0,
        level=1,
        longest_streak=0,
        total_habits_completed=0
    )
    db.session.add(user_stats)
    
    # Create some sample achievements
    achievements_data = [
        {
            'name': 'First Steps',
            'description': 'Completed your first habit!',
            'icon': 'fas fa-baby',
            'color': '#10b981'
        },
        {
            'name': 'Early Bird',
            'description': 'Completed a morning habit 5 days in a row',
            'icon': 'fas fa-sun',
            'color': '#f59e0b'
        }
    ]
    
    for achievement_data in achievements_data:
        achievement = Achievement(
            user_id=user.id,
            name=achievement_data['name'],
            description=achievement_data['description'],
            icon=achievement_data['icon'],
            color=achievement_data['color'],
            points=10
        )
        db.session.add(achievement)
    
    # Create sample AI insights
    insights_data = [
        {
            'type': 'motivation',
            'title': 'Welcome to HabitTracker Pro!',
            'message': 'You\'re off to a great start! Consistency is key to building lasting habits.',
            'confidence': 95
        },
        {
            'type': 'tip',
            'title': 'Morning Routine Tip',
            'message': 'Research shows that habits formed in the morning have a 40% higher success rate.',
            'confidence': 88
        },
        {
            'type': 'improvement',
            'title': 'Habit Stacking',
            'message': 'Try linking new habits to existing ones for better consistency.',
            'confidence': 92
        }
    ]
    
    for insight_data in insights_data:
        insight = AIInsight(
            user_id=user.id,
            type=insight_data['type'],
            title=insight_data['title'],
            message=insight_data['message'],
            confidence=insight_data['confidence']
        )
        db.session.add(insight)
    
    db.session.commit()
    print("Sample data created successfully!")
    print("Demo login: demo@example.com / demo123")

def main():
    """Main function to run the application"""
    print("🚀 Starting HabitTracker Pro...")
    print("=" * 50)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")
        
        # Create sample data if needed
        if '--demo' in sys.argv:
            create_sample_data()
    
    # Get configuration
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"🌐 Server starting on http://{host}:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print("=" * 50)
    
    if '--demo' in sys.argv:
        print("📊 Demo data loaded - Login with demo@example.com / demo123")
        print("=" * 50)
    
    # Run the application
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Shutting down HabitTracker Pro...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()