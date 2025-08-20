#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for PNM Gardeners
Tests all API endpoints with proper validation and error handling
"""

import requests
import json
import sys
import os
from datetime import datetime

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("ERROR: Could not get backend URL from frontend/.env")
    sys.exit(1)

API_URL = f"{BASE_URL}/api"
print(f"Testing API at: {API_URL}")

class APITester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def test_email_service_config(self):
        """Test SendGrid email service configuration"""
        print(f"\n🔧 Testing Email Service Configuration")
        print("=" * 50)
        
        # Check environment variables
        try:
            import os
            sendgrid_key = os.environ.get('SENDGRID_API_KEY')
            sender_email = os.environ.get('SENDER_EMAIL')
            
            if sendgrid_key:
                print(f"   ✅ SENDGRID_API_KEY: Found (length: {len(sendgrid_key)})")
                self.passed += 1
            else:
                print(f"   ❌ SENDGRID_API_KEY: Not found in environment")
                self.failed += 1
                self.errors.append("SENDGRID_API_KEY not found in environment variables")
            
            if sender_email:
                print(f"   ✅ SENDER_EMAIL: {sender_email}")
                if sender_email == "gardeningpnm@gmail.com":
                    print(f"   ✅ Sender email matches expected business email")
                    self.passed += 1
                else:
                    print(f"   ⚠️  Sender email differs from expected: gardeningpnm@gmail.com")
            else:
                print(f"   ❌ SENDER_EMAIL: Not found in environment")
                self.failed += 1
                self.errors.append("SENDER_EMAIL not found in environment variables")
                
        except Exception as e:
            print(f"   ❌ Error checking environment variables: {e}")
            self.failed += 1
            self.errors.append(f"Environment variable check failed: {e}")
        
        # Test email service import
        try:
            print(f"\n🔍 Testing Email Service Import...")
            import sys
            sys.path.append('/app/backend')
            from email_service import email_service
            
            print(f"   ✅ Email service imported successfully")
            print(f"   📧 Business email: {email_service.business_email}")
            print(f"   📧 Sender email: {email_service.sender_email}")
            
            # Verify correct phone number in email templates
            if hasattr(email_service, 'send_customer_confirmation'):
                print(f"   ✅ Customer confirmation method available")
                self.passed += 1
            else:
                print(f"   ❌ Customer confirmation method not found")
                self.failed += 1
                self.errors.append("send_customer_confirmation method not found")
                
        except Exception as e:
            print(f"   ❌ Error importing email service: {e}")
            self.failed += 1
            self.errors.append(f"Email service import failed: {e}")
    
    def test_endpoint(self, method, endpoint, data=None, expected_status=200, description=""):
        """Test an API endpoint"""
        url = f"{API_URL}{endpoint}"
        print(f"\n🧪 Testing {method} {endpoint} - {description}")
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            print(f"   Status: {response.status_code}")
            
            if response.status_code == expected_status:
                print(f"   ✅ PASS - Expected status {expected_status}")
                self.passed += 1
                
                # Try to parse JSON response
                try:
                    json_data = response.json()
                    print(f"   📄 Response: {json.dumps(json_data, indent=2)[:200]}...")
                    return json_data
                except:
                    print(f"   📄 Response: {response.text[:200]}...")
                    return response.text
                    
            else:
                print(f"   ❌ FAIL - Expected {expected_status}, got {response.status_code}")
                print(f"   📄 Response: {response.text[:200]}...")
                self.failed += 1
                self.errors.append(f"{method} {endpoint}: Expected {expected_status}, got {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ FAIL - Request error: {e}")
            self.failed += 1
            self.errors.append(f"{method} {endpoint}: Request error - {e}")
            return None
        except Exception as e:
            print(f"   ❌ FAIL - Unexpected error: {e}")
            self.failed += 1
            self.errors.append(f"{method} {endpoint}: Unexpected error - {e}")
            return None
    
    def run_all_tests(self):
        """Run comprehensive API tests"""
        print("=" * 60)
        print("🚀 STARTING PNM GARDENERS API TESTS")
        print("=" * 60)
        
        # 1. Health Check
        self.test_endpoint("GET", "/", description="Health check endpoint")
        
        # 2. Services Tests
        print("\n" + "=" * 40)
        print("🌿 TESTING SERVICES ENDPOINTS")
        print("=" * 40)
        
        services = self.test_endpoint("GET", "/services", description="Get all services")
        
        if services and isinstance(services, list) and len(services) > 0:
            # Test getting specific service
            service_id = services[0].get('id')
            if service_id:
                self.test_endpoint("GET", f"/services/{service_id}", description=f"Get service by ID: {service_id}")
            
            # Test non-existent service
            self.test_endpoint("GET", "/services/nonexistent", expected_status=404, description="Get non-existent service")
        
        # 3. Reviews Tests
        print("\n" + "=" * 40)
        print("⭐ TESTING REVIEWS ENDPOINTS")
        print("=" * 40)
        
        self.test_endpoint("GET", "/reviews", description="Get all reviews")
        
        # Test reviews with updated model (lat, lng, postcode, images, rating 1-10)
        reviews_response = self.test_endpoint("GET", "/reviews", description="Get all reviews with coordinate data")
        
        if reviews_response and isinstance(reviews_response, list):
            print(f"\n📍 TESTING UPDATED REVIEW MODEL FIELDS")
            print("=" * 50)
            
            for i, review in enumerate(reviews_response[:3]):  # Test first 3 reviews
                print(f"\n🔍 Review {i+1} Field Validation:")
                
                # Check required fields
                required_fields = ['id', 'name', 'rating', 'text', 'service', 'date']
                for field in required_fields:
                    if field in review:
                        print(f"   ✅ {field}: {review[field]}")
                    else:
                        print(f"   ❌ Missing required field: {field}")
                        self.failed += 1
                        self.errors.append(f"Review {review.get('id', 'unknown')} missing required field: {field}")
                
                # Check new coordinate fields
                coordinate_fields = ['lat', 'lng', 'postcode']
                for field in coordinate_fields:
                    if field in review and review[field] is not None:
                        print(f"   ✅ {field}: {review[field]}")
                    else:
                        print(f"   ⚠️  Optional field {field}: {review.get(field, 'None')}")
                
                # Check images field
                if 'images' in review:
                    images = review['images']
                    if isinstance(images, list):
                        print(f"   ✅ images: {len(images)} images - {images[:2] if images else 'empty list'}")
                    else:
                        print(f"   ❌ images field should be a list, got: {type(images)}")
                        self.failed += 1
                        self.errors.append(f"Review {review.get('id', 'unknown')} images field is not a list")
                else:
                    print(f"   ❌ Missing images field")
                    self.failed += 1
                    self.errors.append(f"Review {review.get('id', 'unknown')} missing images field")
                
                # Check rating range (1-10)
                rating = review.get('rating')
                if rating is not None:
                    if 1 <= rating <= 10:
                        print(f"   ✅ rating: {rating} (valid range 1-10)")
                        self.passed += 1
                    else:
                        print(f"   ❌ rating: {rating} (invalid - should be 1-10)")
                        self.failed += 1
                        self.errors.append(f"Review {review.get('id', 'unknown')} has invalid rating: {rating}")
                else:
                    print(f"   ❌ Missing rating field")
                    self.failed += 1
                    self.errors.append(f"Review {review.get('id', 'unknown')} missing rating field")
        
        # Test creating a new review with updated model
        review_data = {
            "name": "Sarah Johnson",
            "rating": 8,  # Test rating in new 1-10 range
            "text": "Excellent gardening service! Very professional and thorough work on our garden maintenance. The team was punctual and left everything spotless.",
            "service": "Garden Maintenance",
            "postcode": "SW12",
            "lat": 51.4648,
            "lng": -0.1731,
            "images": ["https://example.com/before.jpg", "https://example.com/after.jpg"]
        }
        self.test_endpoint("POST", "/reviews", data=review_data, description="Create new review with coordinates and images")
        
        # Test review with maximum rating (10)
        max_rating_review = {
            "name": "Michael Brown",
            "rating": 10,  # Test maximum rating
            "text": "Outstanding service! Completely transformed our garden.",
            "service": "Garden Clearance"
        }
        self.test_endpoint("POST", "/reviews", data=max_rating_review, description="Create review with maximum rating (10)")
        
        # Test invalid review (rating > 10)
        invalid_review = {
            "name": "Test User",
            "rating": 11,  # Invalid rating > 10
            "text": "Test review",
            "service": "Garden Maintenance"
        }
        self.test_endpoint("POST", "/reviews", data=invalid_review, expected_status=422, description="Create review with invalid rating (>10)")
        
        # Test invalid review (rating < 1)
        invalid_low_review = {
            "name": "Test User",
            "rating": 0,  # Invalid rating < 1
            "text": "Test review",
            "service": "Garden Maintenance"
        }
        self.test_endpoint("POST", "/reviews", data=invalid_low_review, expected_status=422, description="Create review with invalid rating (<1)")
        
        # 4. SendGrid Email Integration Tests
        print("\n" + "=" * 40)
        print("📧 TESTING SENDGRID EMAIL INTEGRATION")
        print("=" * 40)
        
        # Test email service configuration
        self.test_email_service_config()
        
        # 5. Quote Requests Tests with Email
        print("\n" + "=" * 40)
        print("💬 TESTING QUOTE REQUESTS WITH EMAIL")
        print("=" * 40)
        
        self.test_endpoint("GET", "/quotes", description="Get all quote requests")
        
        # Test creating valid quote request with email notifications
        quote_data = {
            "name": "Emily Johnson",
            "email": "emily.johnson@email.com",
            "phone": "07748 853590",  # Using correct phone number
            "service": "Garden Maintenance",
            "message": "I need regular garden maintenance for my property in Balham. Please provide a quote for weekly visits."
        }
        print(f"\n📧 Testing quote request with email notifications...")
        response = self.test_endpoint("POST", "/quotes", data=quote_data, description="Create quote request with email notifications")
        
        if response:
            print(f"   ✅ Quote request created successfully")
            print(f"   📧 Email notifications should be sent to:")
            print(f"      • Business: gardeningpnm@gmail.com (quote notification)")
            print(f"      • Customer: {quote_data['email']} (confirmation)")
        
        # Test another quote with different service
        quote_data_2 = {
            "name": "Michael Thompson",
            "email": "michael.thompson@email.com", 
            "phone": "07748 853590",
            "service": "Garden Clearance",
            "message": "Need complete garden clearance for overgrown back garden. Property in Balham area."
        }
        print(f"\n📧 Testing second quote request...")
        response2 = self.test_endpoint("POST", "/quotes", data=quote_data_2, description="Create second quote request with emails")
        
        if response2:
            print(f"   ✅ Second quote request created successfully")
            print(f"   📧 Additional email notifications sent")
        
        # Test invalid quote request (bad email)
        invalid_quote = {
            "name": "Test User",
            "email": "invalid-email",
            "phone": "07123456789",
            "service": "Garden Maintenance",
            "message": "Test message"
        }
        self.test_endpoint("POST", "/quotes", data=invalid_quote, expected_status=422, description="Create quote with invalid email")
        
        # Test invalid phone number
        invalid_phone_quote = {
            "name": "Test User",
            "email": "test@email.com",
            "phone": "123",  # Too short
            "service": "Garden Maintenance",
            "message": "Test message"
        }
        self.test_endpoint("POST", "/quotes", data=invalid_phone_quote, expected_status=422, description="Create quote with invalid phone")
        
        # Test empty name
        empty_name_quote = {
            "name": "",
            "email": "test@email.com",
            "phone": "07123456789",
            "service": "Garden Maintenance",
            "message": "Test message"
        }
        self.test_endpoint("POST", "/quotes", data=empty_name_quote, expected_status=422, description="Create quote with empty name")
        
        
        # 6. Contact Form Tests with Email
        print("\n" + "=" * 40)
        print("📞 TESTING CONTACT FORM WITH EMAIL")
        print("=" * 40)
        
        self.test_endpoint("GET", "/contacts", description="Get all contacts")
        
        # Test creating valid contact with email notifications
        contact_data = {
            "name": "Robert Wilson",
            "email": "robert.wilson@email.com",
            "phone": "07748 853590",  # Using correct phone number
            "subject": "Garden Design Consultation",
            "message": "I'm interested in a complete garden redesign for my property. Could we arrange a consultation?"
        }
        print(f"\n📧 Testing contact form with email notifications...")
        response = self.test_endpoint("POST", "/contact", data=contact_data, description="Create contact with email notifications")
        
        if response:
            print(f"   ✅ Contact form submitted successfully")
            print(f"   📧 Email notifications should be sent to:")
            print(f"      • Business: gardeningpnm@gmail.com (contact notification)")
            print(f"      • Customer: {contact_data['email']} (confirmation)")
        
        # Test another contact form submission
        contact_data_2 = {
            "name": "Sarah Davis",
            "email": "sarah.davis@email.com",
            "phone": "07748 853590",
            "subject": "Hedge Trimming Service",
            "message": "Need professional hedge trimming service for large garden hedge. When can you visit?"
        }
        print(f"\n📧 Testing second contact form submission...")
        response2 = self.test_endpoint("POST", "/contact", data=contact_data_2, description="Create second contact with emails")
        
        if response2:
            print(f"   ✅ Second contact form submitted successfully")
            print(f"   📧 Additional email notifications sent")
        
        # Test invalid contact (missing subject)
        invalid_contact = {
            "name": "Test User",
            "email": "test@email.com",
            "phone": "07748 853590",
            "subject": "",  # Empty subject
            "message": "Test message"
        }
        self.test_endpoint("POST", "/contact", data=invalid_contact, expected_status=422, description="Create contact with empty subject")
        
        # 7. Gallery Tests
        print("\n" + "=" * 40)
        print("🖼️ TESTING GALLERY ENDPOINTS")
        print("=" * 40)
        
        self.test_endpoint("GET", "/gallery", description="Get all gallery images")
        
        # Test creating gallery image (admin endpoint)
        gallery_data = {
            "src": "https://example.com/test-image.jpg",
            "title": "Test Garden Project",
            "category": "Garden Design"
        }
        self.test_endpoint("POST", "/gallery", data=gallery_data, description="Create gallery image")
        
        # 7. Additional Validation Tests
        print("\n" + "=" * 40)
        print("🔍 TESTING ADDITIONAL VALIDATIONS")
        print("=" * 40)
        
        # Test UK phone number variations
        uk_phone_tests = [
            {"phone": "07748 853590", "valid": True, "desc": "Business phone number"},
            {"phone": "07123456789", "valid": True, "desc": "Standard mobile"},
            {"phone": "02087654321", "valid": True, "desc": "London landline"},
            {"phone": "+447748853590", "valid": True, "desc": "International format business"},
            {"phone": "+447123456789", "valid": True, "desc": "International format"},
            {"phone": "0712345678", "valid": True, "desc": "10 digit mobile"},
            {"phone": "123", "valid": False, "desc": "Too short"},
            {"phone": "071234567890", "valid": False, "desc": "Too long"}
        ]
        
        for phone_test in uk_phone_tests:
            test_quote = {
                "name": "Phone Test User",
                "email": "phonetest@email.com",
                "phone": phone_test["phone"],
                "service": "Garden Maintenance",
                "message": f"Testing phone: {phone_test['phone']}"
            }
            expected_status = 200 if phone_test["valid"] else 422
            self.test_endpoint("POST", "/quotes", data=test_quote, expected_status=expected_status, 
                             description=f"Phone validation: {phone_test['desc']} - {phone_test['phone']}")
        
        # Print final results
        self.print_results()
    
    def print_results(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total = self.passed + self.failed
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        
        if self.failed > 0:
            print(f"\n🚨 FAILURES ({self.failed}):")
            for error in self.errors:
                print(f"   • {error}")
        
        success_rate = (self.passed / total * 100) if total > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! Backend API is working correctly.")
        else:
            print(f"\n⚠️  {self.failed} tests failed. Please review the issues above.")
        
        print("=" * 60)

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()