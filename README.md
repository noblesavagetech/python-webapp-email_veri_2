# Python Web App - Email Verification

A Flask web application with email verification using PostgreSQL and Brevo (Sendinblue) Transactional Email API.

## Features

- ✅ User registration with email verification
- ✅ Secure password hashing (PBKDF2)
- ✅ Time-limited verification tokens (24 hours)
- ✅ PostgreSQL database backend
- ✅ Brevo transactional email delivery
- ✅ Protected dashboard access control
- ✅ Session management with Flask-Login

## Tech Stack

- **Runtime**: Python 3.12
- **Framework**: Flask 3.0
- **Database**: PostgreSQL 17
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Token Security**: itsdangerous
- **Email**: Brevo (Sendinblue) API v3

## Quick Start

### 1. Configure Environment Variables

Edit `.env` and add your Brevo API credentials:

```bash
BREVO_API_KEY=your-actual-brevo-api-key
SENDER_EMAIL=noreply@yourdomain.com
SENDER_NAME=Your App Name
```

### 2. Start the Application

```bash
./start.sh
```

Or manually:

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python app.py
```

### 3. Access the App

Open your browser to: **http://localhost:5000**

## Project Structure

```
.
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── models.py              # User model with SQLAlchemy
├── routes/
│   ├── auth.py           # Authentication routes
│   └── main.py           # Main application routes
├── utils/
│   ├── decorators.py     # Custom decorators
│   ├── email.py          # Brevo email sending
│   └── tokens.py         # Token generation/verification
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   └── unverified.html
├── .env                  # Environment variables
└── requirements.txt      # Python dependencies
```

## User Flow

1. **Sign Up** → User creates account with email & password
2. **Pending State** → Account created with `is_verified = False`
3. **Email Sent** → Verification link sent via Brevo API
4. **Click Link** → User clicks link: `/verify/<token>`
5. **Verified** → `is_verified` flag set to `True`
6. **Dashboard Access** → User can now access protected routes

## Security Features

- **Password Hashing**: PBKDF2-SHA256 via Werkzeug
- **Signed Tokens**: URLSafeTimedSerializer with salt
- **Token Expiration**: 24-hour default (configurable)
- **Session Security**: HTTP-only, secure cookies
- **Access Control**: Decorator-based route protection

## Brevo Setup

1. Create account at [brevo.com](https://www.brevo.com)
2. Verify your sender domain (DNS records required)
3. Get API key from Settings → SMTP & API
4. Add to `.env` file

## Database

PostgreSQL is automatically initialized and managed. The database includes:

- **users** table with columns:
  - `id` (Primary Key)
  - `email` (Unique, Indexed)
  - `password_hash`
  - `is_verified` (Boolean, default False)
  - `created_at` (Timestamp)
  - `verified_at` (Timestamp, nullable)

## Development

The app runs in debug mode by default. For production:

1. Set `FLASK_ENV=production` in `.env`
2. Change `SECRET_KEY` to a strong random value
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Enable HTTPS and set `SESSION_COOKIE_SECURE=True`

## Routes

- `/` - Home page
- `/signup` - User registration
- `/login` - User login
- `/logout` - User logout
- `/verify/<token>` - Email verification
- `/unverified` - Pending verification page
- `/dashboard` - Protected dashboard (requires verification)

## License

MIT
