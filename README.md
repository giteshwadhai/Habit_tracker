# HabitTracker Pro 🚀

A modern, interactive habit tracking application built with Python Flask. Track your daily habits, build consistency, and achieve your goals with AI-powered insights and gamification features.

![HabitTracker Pro](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎯 Core Functionality
- **Habit Tracking**: Create and manage daily, weekly, or custom frequency habits
- **Progress Visualization**: Beautiful charts and progress bars to track your journey
- **Streak Tracking**: Build momentum with streak counters and fire animations
- **Goal Setting**: Set specific targets for each habit with progress tracking

### 🎮 Gamification
- **Points System**: Earn points for completing habits
- **Levels**: Level up as you build consistency
- **Achievements**: Unlock badges and achievements for milestones
- **Leaderboards**: Compare your progress with others (coming soon)

### 🤖 Smart Features
- **AI Insights**: Get personalized recommendations and tips
- **Pattern Recognition**: Identify trends in your habit completion
- **Smart Suggestions**: Optimize your routine based on your data
- **Motivational Messages**: Stay motivated with encouraging insights

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark/Light Mode**: Toggle between themes
- **Interactive Animations**: Smooth transitions and hover effects
- **Customizable Habits**: Choose colors, icons, and categories

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd habit-tracker-pro
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the application**
   Open your browser and go to `http://127.0.0.1:5000`

### Demo Mode
To run with sample data:
```bash
python run.py --demo
```
Login with: `demo@example.com` / `demo123`

## 📱 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)
*Clean, modern dashboard with habit cards and progress tracking*

### Habit Creation
![New Habit](screenshots/new-habit.png)
*Interactive habit creation with color and icon selection*

### Insights
![Insights](screenshots/insights.png)
*Detailed analytics and AI-powered insights*

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

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///habits.db
DEBUG=True
HOST=127.0.0.1
PORT=5000
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

## 🎨 Customization

### Themes
The application supports light and dark themes. Themes are defined using CSS variables in `static/css/style.css`.

### Colors
Customize the color scheme by modifying the CSS variables:
```css
:root {
    --primary: #6366f1;
    --secondary: #10b981;
    --accent: #f59e0b;
    --motivation: #ec4899;
}
```

### Icons
Habits support Font Awesome icons. Choose from thousands of available icons.

## 🚀 Deployment

### Heroku
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Set environment variables in Heroku dashboard

3. Deploy:
   ```bash
   git push heroku main
   ```

### Docker
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
   ```

2. Build and run:
   ```bash
   docker build -t habit-tracker-pro .
   docker run -p 5000:5000 habit-tracker-pro
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Bootstrap team for the responsive CSS framework
- Font Awesome for the beautiful icons
- All contributors who help improve this project

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## 🔮 Roadmap

### Version 2.0
- [ ] Advanced analytics and reporting
- [ ] Social features and sharing
- [ ] Mobile app (React Native)
- [ ] API for third-party integrations
- [ ] Advanced AI insights with machine learning

### Version 2.1
- [ ] Habit templates and presets
- [ ] Team and group challenges
- [ ] Export data functionality
- [ ] Advanced goal setting
- [ ] Integration with fitness trackers

---

**Built with ❤️ for better habits and a better you!**