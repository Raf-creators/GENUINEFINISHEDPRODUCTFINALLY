# PNM Gardeners - Backend Implementation Contracts

## API Endpoints

### 1. Services Management
- `GET /api/services` - Get all services
- `GET /api/services/:id` - Get specific service details

### 2. Reviews Management  
- `GET /api/reviews` - Get all customer reviews
- `POST /api/reviews` - Submit new review (optional)

### 3. Quote Requests
- `POST /api/quotes` - Submit quote request form
- `GET /api/quotes` - Get all quote requests (admin)

### 4. Contact Management
- `POST /api/contact` - Submit general contact form
- `GET /api/contacts` - Get all contact submissions (admin)

### 5. Gallery Management
- `GET /api/gallery` - Get gallery images
- `POST /api/gallery` - Upload new gallery image (admin)

## Data Models

### Service Model
```json
{
  "id": "string",
  "title": "string",
  "description": "string", 
  "image": "string",
  "features": ["string"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Review Model
```json
{
  "id": "string",
  "name": "string",
  "rating": "number",
  "date": "string",
  "text": "string", 
  "service": "string",
  "approved": "boolean",
  "created_at": "datetime"
}
```

### Quote Request Model
```json
{
  "id": "string",
  "name": "string",
  "email": "string",
  "phone": "string",
  "service": "string",
  "message": "string",
  "status": "string", // pending, contacted, quoted, completed
  "created_at": "datetime"
}
```

### Contact Model
```json
{
  "id": "string",
  "name": "string", 
  "email": "string",
  "phone": "string",
  "subject": "string",
  "message": "string",
  "status": "string", // new, read, replied
  "created_at": "datetime"
}
```

### Gallery Image Model
```json
{
  "id": "string",
  "src": "string",
  "title": "string", 
  "category": "string",
  "created_at": "datetime"
}
```

## Mock Data Replacement Plan

### Currently Mocked in `/app/frontend/src/mock/data.js`:

1. **services** array → Replace with `GET /api/services`
2. **reviews** array → Replace with `GET /api/reviews` 
3. **faqs** array → Keep as static (no backend needed)
4. **areasServed** array → Keep as static (no backend needed)
5. **galleryImages** array → Replace with `GET /api/gallery`

## Frontend Integration Changes

### 1. API Service Layer
Create `/app/frontend/src/services/api.js` with:
- Base API configuration using REACT_APP_BACKEND_URL
- Service methods for all endpoints
- Error handling

### 2. Components to Update:
- `ServicesSection.jsx` → Fetch services from API
- `ReviewsSection.jsx` → Fetch reviews from API  
- `ContactSection.jsx` → Submit to `/api/quotes` endpoint
- `Gallery.jsx` → Fetch gallery from API

### 3. State Management:
- Add loading states for API calls
- Add error handling for failed requests
- Add success messages for form submissions

## Backend Implementation Priority:

1. **Phase 1**: Core Models & Basic CRUD
   - Create MongoDB models
   - Seed initial data from mock.js
   - Basic GET endpoints

2. **Phase 2**: Form Submissions
   - Quote request endpoint
   - Contact form endpoint
   - Email notifications (optional)

3. **Phase 3**: Integration
   - Update frontend to use API endpoints
   - Replace mock data imports
   - Test all functionality

## Error Handling Strategy:
- Proper HTTP status codes
- Consistent error response format
- Frontend fallback to mock data if API fails
- Loading states and user feedback

## Security Considerations:
- Input validation for all form submissions
- Rate limiting for form endpoints
- XSS protection for user-submitted content
- Email validation for contact forms