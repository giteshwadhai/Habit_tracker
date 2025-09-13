# 🚀 Deployment Guide - HabitTracker Pro

This guide covers multiple deployment options for HabitTracker Pro.

## 📋 Pre-Deployment Checklist

- [ ] All tests pass
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Static files collected (if needed)
- [ ] Security settings configured
- [ ] Production database configured

## 🌐 Deployment Options

### 1. Heroku (Recommended for beginners)

#### Prerequisites
- Heroku CLI installed
- Git repository

#### Steps

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-habit-tracker-pro
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set FLASK_ENV=production
   heroku config:set DATABASE_URL=postgresql://...
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Run Database Migrations**
   ```bash
   heroku run python -c "from app import db; db.create_all()"
   ```

### 2. Docker Deployment

#### Using Docker Compose (Recommended)

1. **Clone and Navigate**
   ```bash
   git clone <your-repo>
   cd habit-tracker-pro
   ```

2. **Configure Environment**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

3. **Build and Run**
   ```bash
   docker-compose up -d
   ```

4. **Initialize Database**
   ```bash
   docker-compose exec web python -c "from app import db; db.create_all()"
   ```

#### Using Docker Only

1. **Build Image**
   ```bash
   docker build -t habit-tracker-pro .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     --name habit-tracker \
     -p 5000:5000 \
     -e SECRET_KEY=your-secret-key \
     -e DATABASE_URL=sqlite:///app/instance/habits.db \
     habit-tracker-pro
   ```

### 3. VPS/Cloud Server (Ubuntu/Debian)

#### Prerequisites
- Ubuntu 20.04+ server
- Root or sudo access
- Domain name (optional)

#### Steps

1. **Update System**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Python and Dependencies**
   ```bash
   sudo apt install python3.9 python3.9-venv python3-pip nginx postgresql postgresql-contrib -y
   ```

3. **Create Application User**
   ```bash
   sudo adduser --system --group habit-tracker
   sudo mkdir -p /opt/habit-tracker
   sudo chown habit-tracker:habit-tracker /opt/habit-tracker
   ```

4. **Clone and Setup Application**
   ```bash
   cd /opt/habit-tracker
   sudo -u habit-tracker git clone <your-repo> .
   sudo -u habit-tracker python3 -m venv venv
   sudo -u habit-tracker ./venv/bin/pip install -r requirements.txt
   ```

5. **Configure PostgreSQL**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE habit_tracker;
   CREATE USER habit_tracker WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE habit_tracker TO habit_tracker;
   \q
   ```

6. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/habit-tracker.service
   ```

   ```ini
   [Unit]
   Description=HabitTracker Pro
   After=network.target

   [Service]
   User=habit-tracker
   Group=habit-tracker
   WorkingDirectory=/opt/habit-tracker
   Environment="PATH=/opt/habit-tracker/venv/bin"
   ExecStart=/opt/habit-tracker/venv/bin/gunicorn --workers 3 --bind unix:/opt/habit-tracker/habit-tracker.sock app:app
   ExecReload=/bin/kill -s HUP $MAINPID

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Service**
   ```bash
   sudo systemctl start habit-tracker
   sudo systemctl enable habit-tracker
   ```

8. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/habit-tracker
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           include proxy_params;
           proxy_pass http://unix:/opt/habit-tracker/habit-tracker.sock;
       }
   }
   ```

   ```bash
   sudo ln -s /etc/nginx/sites-available/habit-tracker /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### 4. Railway

1. **Connect GitHub Repository**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub account
   - Select your repository

2. **Configure Environment Variables**
   - Add `SECRET_KEY`
   - Add `DATABASE_URL` (Railway provides PostgreSQL)

3. **Deploy**
   - Railway automatically detects the Flask app
   - Deploys on every push to main branch

### 5. Render

1. **Create New Web Service**
   - Go to [Render](https://render.com)
   - Connect GitHub repository

2. **Configure Settings**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Set Environment Variables**
   - Add required environment variables

4. **Deploy**
   - Render handles the rest automatically

## 🔧 Production Configuration

### Environment Variables

```bash
# Required
SECRET_KEY=your-very-secure-secret-key-here
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:port/database

# Optional
DEBUG=False
HOST=0.0.0.0
PORT=5000
```

### Security Considerations

1. **Change Secret Key**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Use HTTPS**
   - Configure SSL certificates
   - Redirect HTTP to HTTPS

3. **Database Security**
   - Use strong passwords
   - Restrict database access
   - Regular backups

4. **Environment Variables**
   - Never commit `.env` files
   - Use secure secret management

### Performance Optimization

1. **Database Indexing**
   ```sql
   CREATE INDEX idx_habit_logs_date ON habit_logs(date);
   CREATE INDEX idx_habits_user_id ON habits(user_id);
   ```

2. **Caching**
   - Consider Redis for session storage
   - Implement caching for frequently accessed data

3. **CDN**
   - Use CloudFlare or similar for static assets
   - Enable gzip compression

## 📊 Monitoring

### Health Checks

1. **Application Health**
   ```bash
   curl -f http://your-domain.com/health
   ```

2. **Database Health**
   ```bash
   # Add to your app
   @app.route('/health')
   def health():
       try:
           db.session.execute('SELECT 1')
           return {'status': 'healthy'}, 200
       except:
           return {'status': 'unhealthy'}, 500
   ```

### Logging

1. **Configure Logging**
   ```python
   import logging
   from logging.handlers import RotatingFileHandler
   
   if not app.debug:
       file_handler = RotatingFileHandler('logs/habit-tracker.log', maxBytes=10240, backupCount=10)
       file_handler.setFormatter(logging.Formatter(
           '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
       ))
       file_handler.setLevel(logging.INFO)
       app.logger.addHandler(file_handler)
   ```

## 🔄 Updates and Maintenance

### Database Migrations

1. **Create Migration**
   ```bash
   flask db migrate -m "Description of changes"
   ```

2. **Apply Migration**
   ```bash
   flask db upgrade
   ```

### Application Updates

1. **Pull Changes**
   ```bash
   git pull origin main
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Restart Service**
   ```bash
   sudo systemctl restart habit-tracker
   ```

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL format
   - Verify database server is running
   - Check firewall settings

2. **Static Files Not Loading**
   - Check nginx configuration
   - Verify file permissions
   - Check CDN settings

3. **Memory Issues**
   - Increase server memory
   - Optimize database queries
   - Implement caching

### Logs

1. **Application Logs**
   ```bash
   sudo journalctl -u habit-tracker -f
   ```

2. **Nginx Logs**
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

3. **Database Logs**
   ```bash
   sudo tail -f /var/log/postgresql/postgresql-*.log
   ```

## 📞 Support

If you encounter issues during deployment:

1. Check the logs first
2. Verify all environment variables
3. Test locally with production settings
4. Check server resources (CPU, memory, disk)
5. Contact support with detailed error messages

---

**Happy Deploying! 🚀**
