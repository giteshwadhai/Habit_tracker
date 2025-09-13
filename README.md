


## 🏗️ Project Structure

```
habit-tracker-pro/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── routes.py              # Application routes
├── run.py                 # Application runner
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── main.js        # JavaScript functionality
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Main dashboard
│   ├── new_habit.html     # Habit creation
│   └── insights.html      # Analytics page
└── instance/
    └── habits.db          # SQLite database
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-Login**: User authentication
- **Flask-WTF**: Form handling and CSRF protection
- **Pandas**: Data analysis and manipulation
- **Scikit-learn**: Machine learning for insights

### Frontend
- **Bootstrap 5**: CSS framework
- **Font Awesome**: Icons
- **Custom CSS**: Modern styling with CSS variables
- **Vanilla JavaScript**: Interactive functionality
- **Chart.js**: Data visualization (coming soon)

### Database
- **SQLite**: Development database
- **PostgreSQL**: Production database (configurable)


```

### Database Configuration
The application uses SQLite by default. For production, update the `DATABASE_URL` in your environment variables.

## 📊 Database Schema

### Users
- User authentication and profile information
- Points, level, and achievement tracking

### Habits
- Habit definitions with categories, colors, and icons
- Frequency settings (daily, weekly, custom)

### Habit Logs
- Daily completion tracking
- Notes and timestamps

### Goals
- Habit-specific targets and progress tracking
- Achievement status and deadlines

### Achievements
- Gamification elements
- Unlock conditions and rewards

### AI Insights
- Generated recommendations and tips
- Confidence scores and categorization

website  = https://habittrackerbygiteshwadhai.streamlit.app/

