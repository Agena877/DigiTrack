# DigiTrack - New File Structure Guide

## Overview

The DigiTrack project has been reorganized into a clean, standard Django structure that follows best practices and is easier to understand and maintain.

## New Directory Structure

```
DigiTrack/                          # Project root
│
├── manage.py                       # Django CLI tool
├── Procfile                        # Render deployment config
├── requirements.txt                # Production dependencies
├── requirements-test.txt           # Testing dependencies
├── pytest.ini                      # Pytest configuration
├── create_sample_bookings.py       # Utility script
├── .gitignore                      # Git ignore rules
├── .env.example                    # Environment variables template
├── README.md                       # Project documentation
├── CHANGELOG.md                    # Change history
│
├── config/                         # Django project configuration
│   ├── __init__.py
│   ├── settings.py                 # Main Django settings
│   ├── urls.py                     # Root URL configuration
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application
│
├── apps/                           # All Django apps live here
│   ├── __init__.py
│   └── tourism/                    # Tourism management app
│       ├── __init__.py
│       ├── apps.py                 # App configuration
│       ├── models.py               # Database models
│       ├── views.py                # View functions
│       ├── urls.py                 # App-specific URLs
│       ├── admin.py                # Admin interface config
│       ├── admin_custom_user.py    # Custom user admin
│       ├── admin_log_api.py        # Admin logging API
│       ├── admin_log_users_api.py  # User logging API
│       ├── forms.py                # Django forms
│       ├── models_custom_user.py   # Custom user model
│       ├── templates/              # HTML templates
│       │   └── tourism/
│       │       ├── admin.html
│       │       ├── home.html
│       │       ├── homestay.html
│       │       └── mtoadmin.html
│       ├── static/                 # Static files (CSS, JS, images)
│       │   └── tourism/
│       │       └── images/
│       ├── migrations/             # Database migrations
│       │   ├── __init__.py
│       │   ├── 0001_initial.py
│       │   └── ...
│       ├── tests/                  # Unit tests
│       │   ├── __init__.py
│       │   ├── test_models.py
│       │   ├── test_views.py
│       │   ├── test_forms.py
│       │   ├── test_search.py
│       │   └── test_contact_validation.py
│       └── management/             # Custom management commands
│           └── commands/
│               ├── cleanup_duplicates.py
│               └── set_homestay_owner.py
│
└── staticfiles/                    # Collected static files (auto-generated)
    ├── admin/                      # Django admin static files
    └── tourism/                    # Tourism app static files
```

## Key Changes from Old Structure

### Before (Confusing Nested Structure):
```
DigiTrack/
└── DigiTrackProject/
    ├── DigiTrackProject/           ← Double nesting!
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── tourism/
```

### After (Clean Standard Structure):
```
DigiTrack/
├── config/                         ← Clear purpose
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    └── tourism/                    ← Organized apps
```

## Module Paths

### Old Import Paths:
```python
# Settings module
DJANGO_SETTINGS_MODULE = 'DigiTrackProject.DigiTrackProject.settings'

# URLs
ROOT_URLCONF = 'DigiTrackProject.DigiTrackProject.urls'

# WSGI
WSGI_APPLICATION = 'DigiTrackProject.DigiTrackProject.wsgi.application'

# Apps
INSTALLED_APPS = ['DigiTrackProject.tourism']

# URL includes
path('', include('DigiTrackProject.tourism.urls'))
```

### New Import Paths:
```python
# Settings module
DJANGO_SETTINGS_MODULE = 'config.settings'

# URLs
ROOT_URLCONF = 'config.urls'

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# Apps
INSTALLED_APPS = ['apps.tourism']

# URL includes
path('', include('apps.tourism.urls'))
```

## Benefits of New Structure

### 1. **Clarity**
- `config/` clearly indicates project configuration
- `apps/` clearly indicates where applications live
- No confusing double-nested directories

### 2. **Scalability**
- Easy to add new apps: just create `apps/new_app/`
- Clear separation between config and application code
- Follows Django best practices

### 3. **Maintainability**
- Shorter import paths
- Easier to navigate for new developers
- Standard structure recognized by Django developers

### 4. **Deployment**
- Simpler Procfile: `gunicorn config.wsgi:application`
- Cleaner environment variable names
- Easier to configure CI/CD pipelines

## Migration Guide for Developers

If you have local changes, update your imports:

1. **Import statements** - Replace:
   ```python
   # Old
   from DigiTrackProject.tourism import models
   
   # New
   from apps.tourism import models
   ```

2. **Settings references** - Replace:
   ```python
   # Old
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DigiTrackProject.DigiTrackProject.settings')
   
   # New
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
   ```

3. **URL configurations** - Replace:
   ```python
   # Old
   path('', include('DigiTrackProject.tourism.urls'))
   
   # New
   path('', include('apps.tourism.urls'))
   ```

## Verification

After restructuring, all Django commands work correctly:

```bash
# System check
python manage.py check
# ✅ System check identified no issues (0 silenced).

# Static files collection
python manage.py collectstatic
# ✅ 136 static files copied to 'staticfiles'

# Migrations check
python manage.py makemigrations --check
# ✅ No changes detected
```

## Questions?

For any questions about the new structure:
1. Check this document
2. Review the updated README.md
3. Check CHANGELOG.md for detailed change history

---

**Last Updated**: October 26, 2025
**Structure Version**: 2.0 (Clean & Standard)
