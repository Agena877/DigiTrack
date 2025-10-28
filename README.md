# DigiTrack - Tourism Management System

A Django-based tourism management system for tracking tourists, homestays, bookings, and rooms.

## Features

- Tourist registration and tracking
- Homestay management
- Room booking system
- User authentication with custom user model
- Admin dashboard for tourism officers
- CSV export functionality
- Calendar integration for bookings

## Project Structure

```
DigiTrack/
├── manage.py                    # Django management script
├── Procfile                     # Render deployment configuration
├── requirements.txt             # Python dependencies
├── requirements-test.txt        # Test dependencies
├── pytest.ini                   # Pytest configuration
├── create_sample_bookings.py    # Sample data generator
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment variables template
├── config/                      # Django project settings
│   ├── __init__.py
│   ├── settings.py              # Main settings file
│   ├── urls.py                  # URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
├── apps/                        # Django applications
│   └── tourism/                 # Tourism application
│       ├── models.py            # Database models
│       ├── views.py             # View functions
│       ├── urls.py              # App URL patterns
│       ├── admin.py             # Admin configuration
│       ├── forms.py             # Form definitions
│       ├── templates/           # HTML templates
│       ├── static/              # Static files (CSS, JS, images)
│       ├── migrations/          # Database migrations
│       └── tests/               # Test files
└── staticfiles/                 # Collected static files (generated)
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 12+

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DigiTrack
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up the database**
   - Create a PostgreSQL database
   - Update DATABASE_URL in .env
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test tourism.tests.test_models

# Run with pytest
pytest
```

## Deployment to Render

**📖 See detailed setup guide: [RENDER_SETUP.md](RENDER_SETUP.md)**

### Quick Deploy Steps:

1. **Create PostgreSQL Database on Render**
   - New + → PostgreSQL
   - Copy the Internal Database URL

2. **Create Web Service on Render**
   - Connect your GitHub repository
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application`

3. **Set Environment Variables**:
   ```env
   SECRET_KEY=<generate-strong-key>
   DEBUG=False
   DATABASE_URL=<internal-database-url-from-render>
   ```

4. **Deploy and Create Superuser**
   - Deploy from Render Dashboard
   - Use Shell to run: `python manage.py createsuperuser`

For complete instructions, see [RENDER_SETUP.md](RENDER_SETUP.md)

## Environment Variables

- `SECRET_KEY`: Django secret key (required)
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: PostgreSQL database URL
- `RENDER_EXTERNAL_HOSTNAME`: External hostname on Render (auto-set)

## API Endpoints

- `/api/booking/` - Booking management
- `/api/room/` - Room operations
- `/api/rooms/` - Room list
- `/api/tourist-list/` - Tourist listing
- `/api/register-tourist/` - Tourist registration
- `/api/homestay-search/` - Search homestays
- `/api/export-tourists/` - Export tourist data to CSV
- Additional endpoints documented in `tourism/urls.py`

## Technologies Used

- **Backend**: Django 5.2.5
- **Database**: PostgreSQL
- **Static Files**: WhiteNoise
- **Deployment**: Gunicorn, Render
- **Testing**: pytest, pytest-django

## License

[Add your license information here]

## Contributors

[Add contributor information here]
