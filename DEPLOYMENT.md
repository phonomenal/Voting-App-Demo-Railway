# Free Cloud Deployment Guide

This guide shows how to deploy your voting app to various free cloud hosting services.

## Option 1: Railway (Recommended)

Railway offers the easiest deployment with built-in Redis support.

### Steps:

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select this repository
   - Railway will automatically detect the `railway.json` config

3. **Add Redis Database (Two Options)**

   **Option A: External Redis (Recommended for Free Tier)**
   - Sign up at [upstash.com](https://upstash.com) (free tier: 10K commands/day)
   - Create a free Redis database
   - Copy the Redis URL
   - In Railway: Go to Variables tab → Add `REDIS_URL=your-upstash-url`

   **Option B: Railway Redis (Requires Paid Plan)**
   - In your project dashboard, click "New" → "Database" → "Add Redis"
   - Railway will automatically set the `REDIS_URL` environment variable
   - Note: Free tier has database limitations

4. **Configure Environment Variables**
   - Go to your service → "Variables" tab
   - Add these variables:
     ```
     VOTE1VALUE=Pizza
     VOTE2VALUE=Brownie
     TITLE=My Voting App
     FLASK_ENV=production
     ```

5. **Deploy**
   - Railway will automatically build and deploy
   - Your app will be available at the generated URL

### Cost: Free tier includes 500 hours/month + $5 credit

---

## Option 2: Render

Great alternative with free PostgreSQL and Redis.

### Steps:

1. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Redis Instance**
   - Dashboard → "New" → "Redis"
   - Choose free plan (25MB)
   - Note the Redis URL from the dashboard

3. **Deploy Web Service**
   - Dashboard → "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `cd azure-vote/azure-vote && python main.py`

4. **Environment Variables**
   ```
   REDIS_URL=<your-redis-url-from-step-2>
   VOTE1VALUE=Pizza
   VOTE2VALUE=Brownie
   TITLE=My Voting App
   FLASK_ENV=production
   PORT=10000
   ```

### Cost: Free tier includes 750 hours/month

---

## Option 3: Fly.io

Docker-native platform with global deployment.

### Steps:

1. **Install Fly CLI**
   ```bash
   # macOS
   brew install flyctl
   
   # Linux/Windows
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and Initialize**
   ```bash
   fly auth login
   fly launch
   ```

3. **Configure fly.toml** (auto-generated, but verify):
   ```toml
   app = "your-app-name"
   
   [build]
   
   [http_service]
     internal_port = 5000
     force_https = true
   
   [[vm]]
     memory = '256mb'
     cpu_kind = 'shared'
     cpus = 1
   ```

4. **Add Redis with Upstash**
   - Sign up at [upstash.com](https://upstash.com)
   - Create free Redis database
   - Get connection URL

5. **Set Environment Variables**
   ```bash
   fly secrets set REDIS_URL="your-upstash-redis-url"
   fly secrets set VOTE1VALUE="Pizza"
   fly secrets set VOTE2VALUE="Brownie"
   fly secrets set TITLE="My Voting App"
   fly secrets set FLASK_ENV="production"
   ```

6. **Deploy**
   ```bash
   fly deploy
   ```

### Cost: Free tier includes 3 shared VMs

---

## Local Development

To test locally before deploying:

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis** (using Docker)
   ```bash
   docker run -d -p 6379:6379 redis:alpine
   ```

3. **Set Environment Variables**
   ```bash
   export REDIS_HOST=localhost
   export VOTE1VALUE=Pizza
   export VOTE2VALUE=Brownie
   export TITLE="Local Voting App"
   export FLASK_ENV=development
   ```

4. **Run Application**
   ```bash
   cd voting-service/voting-service
   python main.py
   ```

5. **Visit** http://localhost:5000

---

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `REDIS_URL` | Full Redis connection URL | - | Yes* |
| `REDIS_HOST` | Redis hostname | localhost | Yes* |
| `REDIS_PORT` | Redis port | 6379 | No |
| `REDIS_PASSWORD` | Redis password | - | No |
| `VOTE1VALUE` | First voting option | Pizza | No |
| `VOTE2VALUE` | Second voting option | Brownie | No |
| `TITLE` | App title | Voting App | No |
| `FLASK_ENV` | Flask environment | production | No |
| `PORT` | Server port | 5000 | No |

*Either `REDIS_URL` or `REDIS_HOST` is required

---

## Troubleshooting

### Railway "Limited Access" Error
**Problem**: Can't deploy databases on Railway free tier
**Solutions**:
1. **Use Upstash Redis** (recommended):
   - Sign up at upstash.com
   - Create free Redis database
   - Add `REDIS_URL` to Railway variables
2. **Use in-memory storage** (testing only):
   - Don't set any Redis environment variables
   - App will automatically use in-memory storage
   - Note: Data resets on each deployment
3. **Switch to Render**: Has free Redis included

### Redis Connection Issues
- Verify Redis URL format: `redis://user:password@host:port`
- Check if Redis service is running
- App will automatically fallback to in-memory storage if Redis fails

### App Won't Start
- Check Railway logs in dashboard
- Verify all environment variables are set
- Ensure port binding is correct (app uses PORT env var)

### Deployment Fails
- Check Dockerfile syntax
- Verify requirements.txt has all dependencies
- Ensure build commands are correct for your platform

### No URL Showing
- Wait for deployment to complete (green status)
- Check that service type is "Web Service"
- Verify app is listening on correct port
