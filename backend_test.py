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
        
        # Test creating a new review
        review_data = {
            "name": "John Smith",
            "rating": 5,
            "text": "Excellent gardening service! Very professional and thorough work on our garden maintenance.",
            "service": "Garden Maintenance"
        }
        self.test_endpoint("POST", "/reviews", data=review_data, description="Create new review")
        
        # Test invalid review (missing required fields)
        invalid_review = {
            "name": "Test User",
            "rating": 6,  # Invalid rating > 5
            "text": "Test review"
            # Missing service field
        }
        self.test_endpoint("POST", "/reviews", data=invalid_review, expected_status=422, description="Create invalid review")
        
        # 4. Quote Requests Tests
        print("\n" + "=" * 40)
        print("💬 TESTING QUOTE REQUESTS ENDPOINTS")
        print("=" * 40)
        
        self.test_endpoint("GET", "/quotes", description="Get all quote requests")
        
        # Test creating valid quote request
        quote_data = {
            "name": "Emily Johnson",
            "email": "emily.johnson@email.com",
            "phone": "07123456789",
            "service": "Garden Maintenance",
            "message": "I need regular garden maintenance for my property in Balham. Please provide a quote for weekly visits."
        }
        self.test_endpoint("POST", "/quotes", data=quote_data, description="Create valid quote request")
        
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
        
        # 5. Contact Form Tests
        print("\n" + "=" * 40)
        print("📞 TESTING CONTACT ENDPOINTS")
        print("=" * 40)
        
        self.test_endpoint("GET", "/contacts", description="Get all contacts")
        
        # Test creating valid contact
        contact_data = {
            "name": "Robert Wilson",
            "email": "robert.wilson@email.com",
            "phone": "02087654321",
            "subject": "Garden Design Consultation",
            "message": "I'm interested in a complete garden redesign for my property. Could we arrange a consultation?"
        }
        self.test_endpoint("POST", "/contact", data=contact_data, description="Create valid contact")
        
        # Test invalid contact (missing subject)
        invalid_contact = {
            "name": "Test User",
            "email": "test@email.com",
            "phone": "07123456789",
            "subject": "",  # Empty subject
            "message": "Test message"
        }
        self.test_endpoint("POST", "/contact", data=invalid_contact, expected_status=422, description="Create contact with empty subject")
        
        # 6. Gallery Tests
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
            {"phone": "07123456789", "valid": True, "desc": "Standard mobile"},
            {"phone": "02087654321", "valid": True, "desc": "London landline"},
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