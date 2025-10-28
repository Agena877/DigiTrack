# Render PostgreSQL Setup Guide

## Overview
Your Django app is already configured to work with Render's PostgreSQL. Here's how to set it up properly.

## Step-by-Step Setup on Render

### 1. Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure your database:
   - **Name**: `digitrack-db` (or any name you prefer)
   - **Database**: `digitrack` (will be created automatically)
   - **User**: `digitrack_user` (will be created automatically)
   - **Region**: Choose closest to your users
   - **PostgreSQL Version**: 16 (or latest)
   - **Plan**: Free (or paid based on needs)
4. Click **"Create Database"**
5. Wait for database to provision (1-2 minutes)

### 2. Get Database Connection Details

After creation, Render provides:
- **Internal Database URL**: For connecting from Render services
- **External Database URL**: For connecting from your local machine
- **PSQL Command**: For direct database access

**Important**: Copy the **Internal Database URL** - it looks like:
```
postgresql://digitrack_user:password@dpg-xxxxx.oregon-postgres.render.com/digitrack
```

### 3. Create Web Service on Render

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository (push your code first)
3. Configure your web service:
   - **Name**: `digitrack-app` (or any name)
   - **Environment**: `Python 3`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application`
   - **Plan**: Free (or paid)

### 4. Set Environment Variables on Render

In your Web Service settings, go to **"Environment"** tab and add:

```env
# Required
SECRET_KEY=generate-a-strong-secret-key-here-use-djangos-secret-key-generator
DEBUG=False
DATABASE_URL=<paste-internal-database-url-from-step-2>

# Optional (Render sets this automatically)
# RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com
```

**Generate SECRET_KEY**: Run this locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Deploy

1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Watch the build logs
3. Once deployed, your app will be live at: `https://your-app.onrender.com`

---

## Local Development with Render PostgreSQL

If you want to connect to Render's PostgreSQL from your local machine:

### Option 1: Connect to Render PostgreSQL (Recommended for Testing)

Update your local `.env` file:
```env
SECRET_KEY=django-insecure-local-dev-key-12345
DEBUG=True
DATABASE_URL=<paste-external-database-url-from-render>
```

**Note**: The External Database URL is different from Internal and accessible from anywhere.

### Option 2: Use Local SQLite (Recommended for Development)

Keep your local `.env` as is:
```env
SECRET_KEY=django-insecure-local-dev-key-12345
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

This is faster for local development and doesn't require internet connection.

### Option 3: Use Local PostgreSQL

If you have PostgreSQL installed locally:
```env
SECRET_KEY=django-insecure-local-dev-key-12345
DEBUG=True
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/digitrack_local
```

---

## Database Migrations on Render

### Initial Setup (First Deploy)
The build command already includes migrations:
```bash
python manage.py migrate
```

### After Model Changes
1. Create migrations locally: `python manage.py makemigrations`
2. Commit and push migrations files to GitHub
3. Render will auto-deploy and run migrations

### Manual Migration (if needed)
1. Go to Render Dashboard → Your Web Service
2. Click **"Shell"** tab
3. Run: `python manage.py migrate`

---

## Create Superuser on Render

### Method 1: Using Django Management Command Script (Recommended for Free Tier)

Since the Shell tab isn't available on free tier, create a superuser automatically during deployment:

1. **Create a management command** (already done in your project):
   Create file: `apps/tourism/management/commands/create_admin.py`

2. **Add to Build Command**:
   Update your Render build command to:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_admin
   ```

3. **Set Environment Variables** for admin credentials:
   ```env
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=YourStrongPassword123!
   ```

4. The superuser will be created automatically on first deployment!

### Method 2: Via Shell Tab (Paid Plans Only)

After first deployment, create an admin user:

1. Go to Render Dashboard → Your Web Service
2. Click **"Shell"** tab (requires paid plan)
3. Run:
```bash
python manage.py createsuperuser
```
4. Follow prompts to create username, email, and password

Or use this one-liner:
```bash
python manage.py shell -c "from apps.tourism.models import CustomUser; CustomUser.objects.create_superuser('admin', 'admin@example.com', 'your-strong-password')"
```

### Method 3: Create Locally Then Migrate Database (Alternative)

---

## Environment Variables Reference

### Required for Production (Render)
```env
SECRET_KEY=<strong-secret-key>
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Optional but Recommended
```env
# Render sets this automatically, but you can override
RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com

# For email (if needed later)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
```

---

## How Your Settings Work

Your `config/settings.py` is already configured perfectly:

```python
# DATABASE_URL is read from environment variable
DATABASES = {
    'default': dj_database_url.config(
        default=config(
            'DATABASE_URL',
            default='postgresql://digitrack_user:12345@localhost:5432/digitrack_db'
        ),
        conn_max_age=600  # Connection pooling for better performance
    )
}
```

**This means**:
1. ✅ Render automatically provides `DATABASE_URL` env var
2. ✅ `dj_database_url` parses it and configures Django
3. ✅ `conn_max_age=600` keeps connections alive for 10 minutes (improves performance)
4. ✅ Falls back to default if `DATABASE_URL` not set (for local dev)

---

## Troubleshooting

### Issue: "relation does not exist" error
**Solution**: Migrations didn't run. In Render Shell:
```bash
python manage.py migrate
```

### Issue: "could not connect to server"
**Solution**: Check DATABASE_URL is correct. Make sure you're using:
- **Internal URL** for Render Web Service
- **External URL** for local development

### Issue: Static files not loading
**Solution**: Check collectstatic ran during build:
```bash
python manage.py collectstatic --noinput
```

### Issue: 500 Server Error
**Solution**: Check logs in Render Dashboard → Your Service → Logs tab

---

## Security Checklist for Production

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY` (not the default)
- [ ] Use Render's Internal Database URL (not External)
- [ ] Enable HTTPS (Render does this automatically)
- [ ] Review `ALLOWED_HOSTS` (automatically set from `RENDER_EXTERNAL_HOSTNAME`)
- [ ] Set `CSRF_TRUSTED_ORIGINS` (already configured)

---

## Cost Considerations

### Free Tier Limits:
- **PostgreSQL**: 1GB storage, 97 hours/month connection time
- **Web Service**: Spins down after 15 minutes of inactivity
- **First request after spin-down**: Takes 30-60 seconds

### Upgrading:
If you need 24/7 uptime or more storage:
- Upgrade PostgreSQL: $7/month (10GB)
- Upgrade Web Service: $7/month (always on)

---

## Quick Start Checklist

- [ ] Push your code to GitHub
- [ ] Create PostgreSQL database on Render
- [ ] Copy Internal Database URL
- [ ] Create Web Service on Render
- [ ] Set environment variables (SECRET_KEY, DATABASE_URL)
- [ ] Deploy
- [ ] Create superuser via Shell
- [ ] Access admin at: `https://your-app.onrender.com/admin`

---

**Your app is ready for Render!** 🚀

The setup is already done in your code - you just need to configure it on Render's dashboard.
