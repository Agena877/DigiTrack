# Render PostgreSQL - Quick Reference

## 🚀 Current Setup Status

✅ Your Django app is **already configured** for Render PostgreSQL!
✅ No code changes needed
✅ Just need to configure on Render Dashboard

---

## 📋 Environment Variables Needed

### For Local Development (.env file):
```env
SECRET_KEY=django-insecure-local-dev-key-12345
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### For Render Production:
```env
SECRET_KEY=<strong-generated-key>
DEBUG=False
DATABASE_URL=<render-provides-this-automatically>
```

---

## 🗄️ How It Works

Your `config/settings.py` uses `dj_database_url` which:
1. Reads `DATABASE_URL` from environment
2. Automatically parses the PostgreSQL connection string
3. Configures Django's DATABASES setting

**On Render**: DATABASE_URL is automatically set when you create a PostgreSQL database and link it to your web service.

---

## 🔗 Render PostgreSQL URLs

### Two Types:

1. **Internal Database URL** (Use this for Render Web Services)
   ```
   postgresql://user:pass@dpg-internal-host/dbname
   ```
   - Only accessible from Render services
   - Faster connection
   - Free bandwidth

2. **External Database URL** (Use this for local development)
   ```
   postgresql://user:pass@dpg-external-host/dbname
   ```
   - Accessible from anywhere
   - Use for testing from local machine
   - Counts toward connection time limits

---

## ⚙️ Render Build Commands

Your current setup:
```bash
# Build Command (one line):
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

# Start Command:
gunicorn config.wsgi:application
```

What this does:
1. Installs Python dependencies
2. Collects static files (CSS, JS, images)
3. Runs database migrations
4. Starts Gunicorn WSGI server

---

## 🔐 Generate SECRET_KEY

Run this command locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as SECRET_KEY on Render.

---

## 📝 Step-by-Step Checklist

### On Render Dashboard:

- [ ] **Step 1**: Create PostgreSQL Database
  - Go to Dashboard → New + → PostgreSQL
  - Name it (e.g., `digitrack-db`)
  - Wait for provisioning
  - Copy Internal Database URL

- [ ] **Step 2**: Create Web Service
  - Go to Dashboard → New + → Web Service
  - Connect GitHub repo
  - Set Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
  - Set Start Command: `gunicorn config.wsgi:application`

- [ ] **Step 3**: Add Environment Variables
  - Go to Web Service → Environment
  - Add `SECRET_KEY` (generate new one)
  - Add `DEBUG=False`
  - Add `DATABASE_URL` (paste Internal URL from Step 1)

- [ ] **Step 4**: Deploy
  - Click "Manual Deploy" → "Deploy latest commit"
  - Wait for build to complete

- [ ] **Step 5**: Create Admin User
  - Go to Web Service → Shell
  - Run: `python manage.py createsuperuser`

- [ ] **Step 6**: Access Your App
  - Visit: `https://your-app.onrender.com`
  - Admin: `https://your-app.onrender.com/admin`

---

## 💡 Tips

### Development Workflow:
1. **Local**: Use SQLite for fast development
2. **Testing**: Use Render External URL to test with production database
3. **Production**: Render uses Internal URL automatically

### Database Management:
```bash
# Connect to Render PostgreSQL from local machine
psql <external-database-url>

# Backup database
pg_dump <external-database-url> > backup.sql

# Restore database
psql <external-database-url> < backup.sql
```

### Logs:
- View logs: Render Dashboard → Your Service → Logs tab
- Debug issues: Check for migration errors or missing static files

---

## 🆘 Common Issues

### "No module named 'config'"
- Fix: Make sure you pushed all code to GitHub
- Check: `manage.py` has `DJANGO_SETTINGS_MODULE = 'config.settings'`

### "relation does not exist"
- Fix: Run migrations via Render Shell: `python manage.py migrate`

### Static files not loading
- Fix: Check collectstatic in build command
- Verify: `STATIC_ROOT` and `STATICFILES_DIRS` in settings

### Database connection failed
- Fix: Verify DATABASE_URL is correct
- Use Internal URL for Render services
- Use External URL for local development

---

## 📚 More Info

- Full Guide: [RENDER_SETUP.md](RENDER_SETUP.md)
- Project Docs: [README.md](README.md)
- Render Docs: https://render.com/docs

---

**Your app is ready to deploy!** 🎉
