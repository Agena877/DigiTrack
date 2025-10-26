# Render Free Tier Deployment Guide

## 🆓 Deploy DigiTrack on Render Free Tier

This guide is specifically for Render's **free tier**, which has some limitations but is perfect for testing and small projects.

---

## 📋 Prerequisites

- GitHub account
- Render account (free)
- Your code pushed to GitHub

---

## 🚀 Step-by-Step Deployment

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in details:
   - **Name**: `digitrack-db`
   - **Database**: Leave default (auto-generated)
   - **User**: Leave default (auto-generated)
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 16
   - **Instance Type**: **Free**
4. Click **"Create Database"**
5. Wait 1-2 minutes for provisioning

6. **Copy the Internal Database URL**:
   - Go to your database page
   - Find **"Internal Database URL"**
   - Click to copy (looks like: `postgresql://user:pass@dpg-internal-host/dbname`)
   - **Save this for Step 3!**

---

### Step 2: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Choose **"Build and deploy from a Git repository"**
3. Connect your GitHub account (if not already)
4. Select your **DigiTrack** repository
5. Fill in configuration:

**Basic Settings:**
- **Name**: `digitrack-app` (or your preferred name)
- **Region**: Same as your database
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Environment**: `Python 3`
- **Build Command**:
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_admin
  ```
- **Start Command**:
  ```bash
  gunicorn config.wsgi:application
  ```

**Instance Type:**
- Select: **Free** (0.1 CPU, 512 MB RAM)

6. Click **"Create Web Service"** (don't deploy yet - we need to add environment variables!)

---

### Step 3: Add Environment Variables

Before the first deployment, add environment variables:

1. In your Web Service page, go to **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add these variables one by one:

#### Required Variables:

**1. SECRET_KEY**
```
Key: SECRET_KEY
Value: <generate-using-command-below>
```
Generate a secure key locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**2. DEBUG**
```
Key: DEBUG
Value: False
```

**3. DATABASE_URL**
```
Key: DATABASE_URL
Value: <paste-internal-url-from-step-1>
```

**4. DJANGO_SUPERUSER_USERNAME** (for automatic admin creation)
```
Key: DJANGO_SUPERUSER_USERNAME
Value: admin
```

**5. DJANGO_SUPERUSER_EMAIL**
```
Key: DJANGO_SUPERUSER_EMAIL
Value: admin@example.com
```

**6. DJANGO_SUPERUSER_PASSWORD**
```
Key: DJANGO_SUPERUSER_PASSWORD
Value: <your-strong-password>
```
⚠️ **Choose a strong password!** This will be your admin login.

4. Click **"Save Changes"**

---

### Step 4: Deploy!

1. Render will automatically start deploying after you save environment variables
2. Or click **"Manual Deploy"** → **"Deploy latest commit"**
3. Watch the build logs (takes 2-5 minutes)
4. Look for these success messages:
   - ✅ `Collecting static files...`
   - ✅ `136 static files copied`
   - ✅ `Running migrations...`
   - ✅ `Superuser "admin" created successfully!`

---

### Step 5: Access Your App

Once deployed (status shows "Live"):

1. **Your App URL**: `https://your-app-name.onrender.com`
2. **Admin Panel**: `https://your-app-name.onrender.com/admin`

**Login Credentials:**
- Username: `admin` (or what you set in env vars)
- Password: (what you set in `DJANGO_SUPERUSER_PASSWORD`)

---

## 🆓 Free Tier Limitations

### What You Get:
- ✅ 750 hours/month web service (plenty for testing)
- ✅ 1GB PostgreSQL storage
- ✅ Automatic HTTPS
- ✅ Automatic deployments from GitHub

### Limitations:
- ⏱️ **Spins down after 15 minutes of inactivity**
  - First request after spin-down takes 30-60 seconds
  - Subsequent requests are fast
- ❌ **No Shell access** (that's why we use `create_admin` command)
- 🗄️ **97 hours/month database connection time**
  - Resets monthly
  - Plenty for small projects
- 🔄 **Database expires after 90 days of inactivity**

---

## 🔧 Updating Your App

### To Deploy Code Changes:

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
3. Render automatically deploys (if auto-deploy enabled)
4. Or manually: Dashboard → Your Service → "Manual Deploy"

### To Update Environment Variables:

1. Dashboard → Your Service → "Environment"
2. Edit or add variables
3. Click "Save Changes"
4. Render automatically redeploys

---

## 🎯 Important: Automatic Admin Creation

Since free tier doesn't have Shell access, we use a custom management command:

**File: `apps/tourism/management/commands/create_admin.py`**

This command:
- ✅ Runs automatically during build (in Build Command)
- ✅ Reads credentials from environment variables
- ✅ Creates superuser only if it doesn't exist
- ✅ Skips if admin already exists (safe to run multiple times)

**Environment Variables Used:**
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your-password
```

---

## 🆘 Troubleshooting

### Issue: Build Fails

**Check build logs for:**
- Missing dependencies → Add to `requirements.txt`
- Migration errors → Check models are correct
- Collectstatic errors → Check static files configuration

**Fix**: Review logs, make corrections, push to GitHub

---

### Issue: "Superuser not created"

**Cause**: `DJANGO_SUPERUSER_PASSWORD` not set

**Fix**: 
1. Go to Environment tab
2. Add `DJANGO_SUPERUSER_PASSWORD` variable
3. Redeploy

---

### Issue: App is slow on first request

**Cause**: Free tier spins down after 15 minutes

**This is normal!** Options:
- Wait 30-60 seconds for first request
- Upgrade to paid plan ($7/month for always-on)
- Keep app awake with uptime monitor (not recommended for free tier)

---

### Issue: Can't login to admin

**Check:**
1. Did superuser creation succeed? Check build logs for:
   ```
   Superuser "admin" created successfully!
   ```
2. Using correct password from `DJANGO_SUPERUSER_PASSWORD`?
3. Try resetting password:
   - Update `DJANGO_SUPERUSER_PASSWORD` in environment variables
   - Delete the admin user from database (use database client)
   - Redeploy to recreate

---

### Issue: "relation does not exist"

**Cause**: Migrations didn't run

**Fix**: Check Build Command includes:
```bash
python manage.py migrate
```

---

### Issue: Static files not loading (no CSS)

**Cause**: Collectstatic didn't run or WhiteNoise not configured

**Fix**: 
1. Check Build Command includes:
   ```bash
   python manage.py collectstatic --noinput
   ```
2. Verify in logs: `136 static files copied`
3. Check `config/settings.py` has WhiteNoise middleware

---

## 📊 Monitoring Your App

### View Logs:
1. Dashboard → Your Service
2. Click **"Logs"** tab
3. See real-time application logs

### Check Status:
- **Live** ✅ - App is running
- **Building** 🔨 - Deploying changes
- **Failed** ❌ - Check logs for errors
- **Suspended** ⏸️ - Sleeping (free tier)

---

## 💰 When to Upgrade

Consider paid plans ($7/month each) if you need:
- 🔄 Always-on web service (no spin-down)
- 🗄️ More database storage (10GB+)
- 💻 Shell access for debugging
- 🚀 Better performance
- 📈 Multiple background workers

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] PostgreSQL database created on Render
- [ ] Internal Database URL copied
- [ ] Web Service created and connected to GitHub
- [ ] Build Command includes: `migrate` and `create_admin`
- [ ] Start Command: `gunicorn config.wsgi:application`
- [ ] Environment variables set:
  - [ ] SECRET_KEY (generated)
  - [ ] DEBUG=False
  - [ ] DATABASE_URL (from database)
  - [ ] DJANGO_SUPERUSER_USERNAME
  - [ ] DJANGO_SUPERUSER_EMAIL
  - [ ] DJANGO_SUPERUSER_PASSWORD
- [ ] Deployed successfully
- [ ] Can access app at `.onrender.com` URL
- [ ] Can login to admin panel

---

## 🎉 You're Done!

Your DigiTrack app is now live on Render's free tier!

**Your URLs:**
- Main app: `https://your-app-name.onrender.com`
- Admin: `https://your-app-name.onrender.com/admin`

**Remember:**
- First request after inactivity takes 30-60 seconds (normal for free tier)
- Admin credentials from your environment variables
- Check logs if anything goes wrong

---

**Need help?** Check the full guide: [RENDER_SETUP.md](RENDER_SETUP.md)
