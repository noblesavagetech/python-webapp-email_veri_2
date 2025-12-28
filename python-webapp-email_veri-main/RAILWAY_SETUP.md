# Python WebApp with Email Verification - Railway Deployment Guide

## How This Works

### 1. **Local Development (GitHub Codespaces)**
- Use `docker-compose.yml` to spin up PostgreSQL locally
- Develop and test your schema changes
- Database runs in a container alongside your app

### 2. **Railway Deployment (Automated)**
When you push to Railway:

1. **Service Discovery**: Railway detects `docker-compose.yml` and automatically provisions a managed PostgreSQL database
2. **Environment Variables**: Railway automatically injects `DATABASE_URL` pointing to the managed database
3. **Schema Sync**: The `preDeployCommand` in `railway.json` runs `python init_db.py` to create/update tables
4. **App Start**: Your app starts with the database already initialized

## Local Development Setup

1. **Start the development environment:**
   ```bash
   docker-compose up
   ```
   This starts both PostgreSQL and your Flask app.

2. **Access the app:**
   - App: http://localhost:5000
   - PostgreSQL: localhost:5432

3. **Initialize database manually (if needed):**
   ```bash
   python init_db.py
   ```

## Railway Deployment

### First Time Setup

1. **Connect Repository**: Link this GitHub repo to Railway
2. **Railway Auto-Detects**: 
   - Sees `docker-compose.yml` 
   - Provisions managed PostgreSQL service
   - Sets `DATABASE_URL` environment variable automatically

3. **Set Environment Variables** in Railway Dashboard:
   - `SECRET_KEY` - Generate a random secret key
   - `BREVO_API_KEY` - Your Brevo API key
   - `SENDER_EMAIL` - Your verified sender email
   - `SENDER_NAME` - Your app name
   - `APP_URL` - Your Railway app URL (e.g., https://yourapp.up.railway.app)

### Every Deployment (git push)

1. You push code to GitHub
2. Railway detects the push
3. Runs `python init_db.py` (from `railway.json` preDeployCommand)
4. Starts your app with `gunicorn`

## Database Schema Changes

1. **Modify** [models.py](models.py) in Codespaces
2. **Test** locally with `docker-compose up`
3. **Commit and push** to GitHub
4. **Railway automatically** runs migrations via `init_db.py`

## File Structure

- `docker-compose.yml` - Local development & Railway service discovery
- `railway.json` - Deployment configuration with preDeployCommand
- `init_db.py` - Database initialization/migration script
- `Dockerfile` - Container image definition
- `models.py` - SQLAlchemy database models
- `config.py` - Configuration (handles DATABASE_URL dynamically)

## No Manual Database Creation Required

Railway automatically:
- ✓ Provisions PostgreSQL from docker-compose.yml
- ✓ Injects DATABASE_URL
- ✓ Runs schema migrations before deployment
- ✓ Manages database backups and scaling

Just push your code and everything works.
