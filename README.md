# PNM Gardeners Website

Professional gardening services website built with React, FastAPI, and MongoDB.

## Features

- Responsive React frontend with modern UI
- FastAPI backend with REST API
- MongoDB database integration  
- Contact and quote forms with email notifications
- Interactive photo gallery with 750+ real project photos
- Customer reviews and ratings display
- Interactive map with service areas
- Professional service showcase

## Tech Stack

**Frontend:**
- React 18
- Tailwind CSS
- Shadcn UI components
- Axios for API calls

**Backend:**
- FastAPI
- MongoDB with Motor (async driver)
- SendGrid for email notifications
- Google Drive API for photo management

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
python server.py
```

### Frontend  
```bash
cd frontend
yarn install
yarn start
```

### Environment Variables

Create `.env` files in both frontend and backend directories:

**backend/.env:**
```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="pnm_gardeners"
SENDGRID_API_KEY="your_sendgrid_api_key"
SENDER_EMAIL="your_sender_email@domain.com"
CORS_ORIGINS="*"
```

**frontend/.env:**
```
REACT_APP_BACKEND_URL="http://localhost:8001"
```

## Deployment

The application is designed to be deployed on any platform supporting React and FastAPI applications.

## Contact

Professional gardening services in Balham, London.
Phone: 07748 853590
Email: gardeningpnm@gmail.com