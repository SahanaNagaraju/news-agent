# Render Deployment Guide for News Agent

This guide provides step-by-step instructions for deploying the News Agent to Render.

## Prerequisites

1. **Render Account**: Create a free account at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Newdata.io API Key**: Get your API key from newdata.io

## Deployment Methods

### Method 1: Deploy from GitHub (Recommended)

#### Step 1: Prepare Your Repository

Ensure your repository contains:
- `requirements.txt` - Python dependencies
- `app/` directory - Application code
- `.env.example` - Example environment variables
- `Procfile` (optional) - Render will auto-detect Python apps

#### Step 2: Connect to Render

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** button
3. Select **"Web Service"**
4. Connect your GitHub account if not already connected
5. Select your `news-agent` repository

#### Step 3: Configure Web Service

Fill in the following settings:

- **Name**: `news-agent` (or your preferred name)
- **Region**: Choose the closest region to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave blank (unless your app is in a subdirectory)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Step 4: Set Environment Variables

In the **Environment** section, add the following variables:

| Key | Value |
|-----|-------|
| `NEWDATA_API_KEY` | Your actual newdata.io API key |
| `ENV` | `production` |
| `ALLOWED_ORIGINS` | `*` (or specific origins) |
| `PORT` | `8080` (Render will override this) |

#### Step 5: Choose Plan

- **Free Plan**: 
  - 512 MB RAM
  - Spins down after 15 minutes of inactivity
  - Perfect for testing and development
  
- **Starter Plan ($7/month)**:
  - 512 MB RAM
  - Always running
  - Better for production use

#### Step 6: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start your application
   - Provide you with a URL (e.g., `https://news-agent.onrender.com`)

### Method 2: Deploy from Render Dashboard (Manual)

1. Click **"New +"** → **"Web Service"**
2. Choose **"Build and deploy from a Git repository"**
3. Follow steps from Method 1

## Post-Deployment

### Verify Deployment

1. Wait for the deployment to complete (usually 2-5 minutes)
2. Access your service URL: `https://your-app-name.onrender.com`
3. Test the health endpoint:
   ```bash
   curl https://your-app-name.onrender.com/health
   ```

### Access API Documentation

Visit these URLs to explore the API:
- **Interactive Docs**: `https://your-app-name.onrender.com/docs`
- **ReDoc**: `https://your-app-name.onrender.com/redoc`
- **Root Endpoint**: `https://your-app-name.onrender.com/`

## Configuration

### Update Environment Variables

1. Go to your service in Render Dashboard
2. Navigate to **"Environment"** tab
3. Add/Edit variables
4. Changes will trigger an automatic redeployment

### Custom Domain

1. In Render Dashboard, go to **"Settings"**
2. Scroll to **"Custom Domain"** section
3. Click **"Add Custom Domain"**
4. Follow DNS configuration instructions
5. Render provides free SSL certificates automatically

## Monitoring and Logs

### View Logs

1. In Render Dashboard, go to your service
2. Click on the **"Logs"** tab
3. View real-time logs or search historical logs

### Metrics

1. Go to **"Metrics"** tab to see:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

### Alerts

Set up email alerts in **"Settings"** → **"Notifications"**:
- Deployment failures
- Service health issues
- High resource usage

## Scaling and Performance

### Vertical Scaling

Upgrade your plan for more resources:
1. Go to **"Settings"**
2. Click **"Change Plan"**
3. Select higher tier (up to 16 GB RAM available)

### Horizontal Scaling

For paid plans, you can add more instances:
1. Go to **"Settings"**
2. Adjust **"Instance Count"**
3. Render will load balance across instances

## Auto-Deploy

### Enable Auto-Deploy

By default, Render automatically deploys when you push to your branch:
1. Push changes to your GitHub repository
2. Render detects the push
3. Automatically builds and deploys
4. Zero-downtime deployments

### Disable Auto-Deploy

If you want manual control:
1. Go to **"Settings"**
2. Find **"Auto-Deploy"** section
3. Toggle off
4. Use **"Manual Deploy"** button when ready

## Troubleshooting

### Application Won't Start

**Check Build Logs:**
1. Go to **"Logs"** tab
2. Look for errors during build phase
3. Common issues:
   - Missing dependencies in `requirements.txt`
   - Python version mismatch
   - Incorrect start command

**Solution:**
```bash
# Ensure requirements.txt is up to date
pip freeze > requirements.txt
```

### 503 Service Unavailable

**Free Tier Spin Down:**
- Free services spin down after 15 minutes of inactivity
- First request after spin down takes 30-60 seconds
- Solution: Upgrade to Starter plan or use a cron job to keep it warm

### Memory Issues

**Symptoms:**
- Application crashes
- Out of memory errors in logs

**Solution:**
1. Optimize your application
2. Upgrade to a larger plan
3. Implement caching

### Environment Variable Changes Not Applied

**Solution:**
1. After changing environment variables
2. Click **"Manual Deploy"** or
3. Trigger a redeployment by pushing a commit

## Best Practices

### 1. Use Environment Variables
Never commit secrets to your repository:
```bash
# .gitignore should include:
.env
*.pyc
__pycache__/
```

### 2. Health Checks
Ensure your `/health` endpoint works correctly:
```python
@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

### 3. Logging
Use proper logging for debugging:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Application started")
```

### 4. CORS Configuration
For production, specify allowed origins:
```bash
ALLOWED_ORIGINS=https://yourfrontend.com,https://app.yourfrontend.com
```

### 5. Keep Dependencies Updated
Regularly update your dependencies:
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

## Cost Optimization

### Free Tier Limits
- 750 hours/month free compute
- Spins down after 15 minutes inactivity
- Great for development and testing

### Minimize Costs
1. Use free tier for development
2. Only upgrade production services
3. Monitor usage in Dashboard
4. Delete unused services

## Useful Commands

### Local Testing Before Deploy
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python run.py

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/api/news?query=technology
```

### Force Redeploy
```bash
# Trigger redeploy by pushing an empty commit
git commit --allow-empty -m "Trigger redeploy"
git push origin main
```

## External Integration

Once deployed, your service can be called from external applications:

```python
import requests

# Your Render URL
NEWS_AGENT_URL = "https://news-agent.onrender.com"

# Fetch news
response = requests.get(f"{NEWS_AGENT_URL}/api/news", params={"query": "technology"})
print(response.json())

# Get headlines
response = requests.get(f"{NEWS_AGENT_URL}/api/headlines", params={"country": "us"})
print(response.json())
```

## Support and Resources

- [Render Documentation](https://render.com/docs)
- [Render Community Forum](https://community.render.com)
- [Python on Render Guide](https://render.com/docs/deploy-fastapi)
- [Render Status Page](https://status.render.com)

## Migration from BTP to Render

If migrating from BTP:
1. Export environment variables from BTP
2. Set them in Render Dashboard
3. Update any BTP-specific configurations
4. Test thoroughly before switching traffic
5. Use custom domain for seamless transition