# Quick Reference Guide

## Starting the App

```bash
./start.sh
```

App will be available at: **http://localhost:5000**

## First Time Setup

1. Run setup script:
   ```bash
   ./setup.sh
   ```

2. Edit `.env` and add your Brevo credentials:
   ```bash
   BREVO_API_KEY=xkeysib-your-api-key-here
   SENDER_EMAIL=noreply@yourdomain.com
   SENDER_NAME=Your App Name
   ```

3. Start the app:
   ```bash
   ./start.sh
   ```

## Manual Commands

### Start PostgreSQL
```bash
postgres -D ~/pgdata -p 5432 -k /tmp > ~/postgres.log 2>&1 &
```

### Create Database
```bash
psql -h localhost -U vscode -d postgres -c "CREATE DATABASE email_verification_db;"
```

### Start Flask App
```bash
source venv/bin/activate
python app.py
```

### Check PostgreSQL Status
```bash
pg_isready -h localhost -p 5432
```

### View PostgreSQL Logs
```bash
cat ~/postgres.log
```

### Access Database
```bash
psql -h localhost -U vscode -d email_verification_db
```

## Useful SQL Queries

### View all users
```sql
SELECT id, email, is_verified, created_at FROM users;
```

### Manually verify a user
```sql
UPDATE users SET is_verified = true, verified_at = NOW() WHERE email = 'user@example.com';
```

### Delete all users
```sql
TRUNCATE users CASCADE;
```

## Testing Without Email

If you haven't configured Brevo yet, you can:

1. Sign up normally (verification email will fail silently)
2. Manually verify the user in database:
   ```bash
   psql -h localhost -U vscode -d email_verification_db -c \
     "UPDATE users SET is_verified = true WHERE email = 'test@example.com';"
   ```
3. Log in and access dashboard

## Troubleshooting

### Port 5432 already in use
```bash
# Find and kill the process
lsof -ti:5432 | xargs kill -9
```

### Port 5000 already in use
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9
```

### Reset everything
```bash
# Stop PostgreSQL
pkill postgres

# Remove database
rm -rf ~/pgdata

# Re-run setup
./setup.sh
```

### View Flask logs
The Flask app outputs logs directly to the terminal where you ran it.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-secret-key...` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://vscode@localhost:5432/email_verification_db` |
| `BREVO_API_KEY` | Brevo API key | Required for emails |
| `SENDER_EMAIL` | From email address | Required for emails |
| `SENDER_NAME` | From name | `Email Verification App` |
| `APP_URL` | Base URL | `http://localhost:5000` |
| `TOKEN_EXPIRATION` | Token lifetime (seconds) | `86400` (24 hours) |

## Production Checklist

- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Use production WSGI server (Gunicorn/uWSGI)
- [ ] Enable HTTPS
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Configure proper PostgreSQL authentication
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Set up monitoring/logging
- [ ] Verify Brevo sender domain
