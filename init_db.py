import os
import sys
from datetime import datetime, timedelta
import random

# Add the current directory to the path so we can import our app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Habit, HabitLog, AIInsight

def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        print("Created database tables.")
        
        # Check if we already have users
        if User.query.count() > 0:
            print("Database already contains data. Skipping sample data creation.")
            return
        
        # Create a sample user
        user = User(username="demo", email="demo@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        print(f"Created sample user: {user.username}")
        
        # Create sample habits
        habits = [
            Habit(name="Morning Meditation", description="10 minutes of mindfulness each morning", 
                  category="wellness", user_id=user.id),
            Habit(name="Read for 30 minutes", description="Read books or articles to expand knowledge", 
                  category="learning", user_id=user.id),
            Habit(name="Exercise", description="30 minutes of physical activity", 
                  category="health", user_id=user.id),
            Habit(name="Drink 8 glasses of water", description="Stay hydrated throughout the day", 
                  category="health", user_id=user.id),
            Habit(name="Plan tomorrow's tasks", description="Organize and prioritize tasks for the next day", 
                  category="productivity", user_id=user.id),
        ]
        
        for habit in habits:
            db.session.add(habit)
        
        db.session.commit()
        print(f"Created {len(habits)} sample habits")
        
        # Create sample habit logs (past 30 days)
        today = datetime.now().date()
        for i in range(30):
            date = today - timedelta(days=i)
            
            for habit in habits:
                # Randomly decide if the habit was completed on this day
                # Higher probability for more recent days and certain habits
                probability = 0.8 if i < 7 else (0.6 if i < 14 else 0.4)
                
                # Adjust probability based on habit (some habits are easier to maintain)
                if habit.name == "Drink 8 glasses of water":
                    probability += 0.15
                elif habit.name == "Morning Meditation":
                    probability += 0.1
                
                if random.random() < probability:
                    log = HabitLog(habit_id=habit.id, date=date, completed=True)
                    db.session.add(log)
        
        db.session.commit()
        print("Created sample habit logs for the past 30 days")
        
        # Create sample AI insights
        insights = [
            AIInsight(
                title="Consistency Improvement",
                message="You've been more consistent with your Morning Meditation habit. Keep it up for better focus and reduced stress.",
                type="improvement",
                confidence=92,
                user_id=user.id
            ),
            AIInsight(
                title="Habit Pattern Detected",
                message="You tend to complete your Exercise habit more often on weekdays than weekends. Consider scheduling weekend workouts at a specific time.",
                type="trend",
                confidence=85,
                user_id=user.id
            ),
            AIInsight(
                title="Progress Recognition",
                message="Great job maintaining your water intake habit! This consistency is helping your overall health and energy levels.",
                type="motivation",
                confidence=95,
                user_id=user.id
            ),
            AIInsight(
                title="Habit Stacking Opportunity",
                message="Try connecting your Reading habit with another established habit like your morning coffee to increase consistency.",
                type="suggestion",
                confidence=78,
                user_id=user.id
            ),
        ]
        
        for insight in insights:
            db.session.add(insight)
        
        db.session.commit()
        print(f"Created {len(insights)} sample AI insights")
        
        print("\nInitialization complete! You can now run the application.")
        print("Sample user credentials: username='demo', password='password'")

if __name__ == "__main__":
    init_db()