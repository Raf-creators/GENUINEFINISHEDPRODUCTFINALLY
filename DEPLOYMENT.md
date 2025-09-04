# Deployment Guide

## Quick Start

### 1. Environment Setup
Copy `.env.example` files and configure:
- `backend/.env` - Add your MongoDB URL and SendGrid API key
- `frontend/.env` - Set your backend URL

### 2. Install Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend  
cd frontend
yarn install
```

### 3. Run Development
```bash
# Terminal 1 - Backend
cd backend
python server.py

# Terminal 2 - Frontend
cd frontend
yarn start
```

### 4. Production Build
```bash
cd frontend
yarn build
```

## Database
- MongoDB connection required
- Database will auto-seed with sample data on first run
- No manual setup needed

## Email Setup
- Get SendGrid API key from sendgrid.com
- Add to `backend/.env` as `SENDGRID_API_KEY`
- Set sender email as `SENDER_EMAIL`

The website will be available at `http://localhost:3000` (development) or your production domain.