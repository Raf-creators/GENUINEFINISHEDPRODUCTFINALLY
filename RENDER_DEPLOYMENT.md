# 🚀 Deploy PNM Gardeners to Render.com - Simple Guide

## Step 1: Create MongoDB Atlas Database (Free)

1. Go to https://www.mongodb.com/atlas/database
2. Sign up for free account
3. Create a new cluster (choose the free tier)
4. Create database user:
   - Username: `pnm-user`
   - Password: Choose a strong password
5. Get connection string (looks like):
   ```
   mongodb+srv://pnm-user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/pnm_gardeners
   ```

## Step 2: Deploy to Render.com

1. Go to https://render.com and sign up
2. Connect your GitHub repository
3. Create **Backend Web Service**:
   - **Name**: `pnm-gardeners-backend`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python server.py`
   - **Environment Variables**:
     ```
     MONGO_URL=mongodb+srv://pnm-user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/pnm_gardeners
     DB_NAME=pnm_gardeners
     CORS_ORIGINS=*
     SENDGRID_API_KEY=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
     SENDER_EMAIL=gardeningpnm@gmail.com
     PORT=8001
     ```

4. Create **Frontend Static Site**:
   - **Name**: `pnm-gardeners-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `./frontend/build`
   - **Environment Variables**:
     ```
     REACT_APP_BACKEND_URL=https://pnm-gardeners-backend.onrender.com
     ```

## Step 3: Update Domain (Optional)

1. In Render dashboard, go to your frontend service
2. Click "Settings" → "Custom Domain"
3. Add your domain name
4. Update DNS records as instructed

## That's It! 🎉

Your website will be live at:
- **Backend**: `https://pnm-gardeners-backend.onrender.com`
- **Frontend**: `https://pnm-gardeners-frontend.onrender.com`

## Free Tier Limitations

- Backend may sleep after 15 minutes of inactivity
- 750 hours/month limit (enough for 24/7 operation)
- Database: 512MB storage limit (plenty for your needs)

## Cost

- **Free**: $0/month (perfect for getting started)
- **Paid**: $7/month for always-on service (no sleeping)