import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API Service Functions
export const apiService = {
  // Services
  async getServices() {
    try {
      const response = await apiClient.get('/services');
      return response.data;
    } catch (error) {
      console.error('Error fetching services:', error);
      throw error;
    }
  },

  async getService(id) {
    try {
      const response = await apiClient.get(`/services/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching service ${id}:`, error);
      throw error;
    }
  },

  // Reviews
  async getReviews() {
    try {
      const response = await apiClient.get('/reviews');
      return response.data;
    } catch (error) {
      console.error('Error fetching reviews:', error);
      throw error;
    }
  },

  async createReview(reviewData) {
    try {
      const response = await apiClient.post('/reviews', reviewData);
      return response.data;
    } catch (error) {
      console.error('Error creating review:', error);
      throw error;
    }
  },

  // Quote Requests
  async createQuoteRequest(quoteData) {
    try {
      const response = await apiClient.post('/quotes', quoteData);
      return response.data;
    } catch (error) {
      console.error('Error creating quote request:', error);
      throw error;
    }
  },

  async getQuoteRequests() {
    try {
      const response = await apiClient.get('/quotes');
      return response.data;
    } catch (error) {
      console.error('Error fetching quote requests:', error);
      throw error;
    }
  },

  // Contact
  async createContact(contactData) {
    try {
      const response = await apiClient.post('/contact', contactData);
      return response.data;
    } catch (error) {
      console.error('Error creating contact:', error);
      throw error;
    }
  },

  async getContacts() {
    try {
      const response = await apiClient.get('/contacts');
      return response.data;
    } catch (error) {
      console.error('Error fetching contacts:', error);
      throw error;
    }
  },

  // Gallery
  async getGalleryImages() {
    try {
      const response = await apiClient.get('/gallery');
      return response.data;
    } catch (error) {
      console.error('Error fetching gallery images:', error);
      throw error;
    }
  },

  async createGalleryImage(imageData) {
    try {
      const response = await apiClient.post('/gallery', imageData);
      return response.data;
    } catch (error) {
      console.error('Error creating gallery image:', error);
      throw error;
    }
  }
};

// Error handling helper
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    const message = error.response.data?.error || error.response.data?.message || 'Server error occurred';
    return {
      message,
      status: error.response.status,
      type: 'server_error'
    };
  } else if (error.request) {
    // Network error
    return {
      message: 'Unable to connect to server. Please check your internet connection.',
      status: 0,
      type: 'network_error'
    };
  } else {
    // Other error
    return {
      message: error.message || 'An unexpected error occurred',
      status: 0,
      type: 'unknown_error'
    };
  }
};

export default apiService;