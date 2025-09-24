#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Camera Management System
Tests all backend functionality including authentication, CRUD operations, 
role-based access control, maintenance logging, and statistics.
"""

import requests
import json
from datetime import datetime, timedelta
import uuid
import sys
import os

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        return "https://asset-tracker-delphi.preview.emergentagent.com"
    return "https://asset-tracker-delphi.preview.emergentagent.com"

BASE_URL = get_backend_url() + "/api"
print(f"Testing backend at: {BASE_URL}")

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.admin_token = None
        self.manager_token = None
        self.user_token = None
        self.viewer_token = None
        self.test_camera_id = None
        self.test_user_id = None
        self.results = {
            "authentication": {"passed": 0, "failed": 0, "errors": []},
            "camera_crud": {"passed": 0, "failed": 0, "errors": []},
            "user_management": {"passed": 0, "failed": 0, "errors": []},
            "maintenance": {"passed": 0, "failed": 0, "errors": []},
            "statistics": {"passed": 0, "failed": 0, "errors": []}
        }

    def log_result(self, category, test_name, success, error_msg=None):
        if success:
            self.results[category]["passed"] += 1
            print(f"✅ {test_name}")
        else:
            self.results[category]["failed"] += 1
            self.results[category]["errors"].append(f"{test_name}: {error_msg}")
            print(f"❌ {test_name}: {error_msg}")

    def test_authentication(self):
        print("\n🔐 Testing Authentication System...")
        
        # Test 1: Login with default admin credentials
        try:
            response = requests.post(f"{self.base_url}/auth/login", json={
                "username": "admin",
                "password": "admin123"
            })
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data["access_token"]
                self.log_result("authentication", "Admin login", True)
            else:
                self.log_result("authentication", "Admin login", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("authentication", "Admin login", False, str(e))

        # Test 2: Register new users with different roles
        test_users = [
            {"username": "test_manager", "email": "manager@test.com", "password": "manager123", "role": "manager"},
            {"username": "test_user", "email": "user@test.com", "password": "user123", "role": "user"},
            {"username": "test_viewer", "email": "viewer@test.com", "password": "viewer123", "role": "viewer"}
        ]

        for user_data in test_users:
            try:
                response = requests.post(f"{self.base_url}/auth/register", json=user_data)
                if response.status_code == 200:
                    self.log_result("authentication", f"Register {user_data['role']}", True)
                    
                    # Login with the new user
                    login_response = requests.post(f"{self.base_url}/auth/login", json={
                        "username": user_data["username"],
                        "password": user_data["password"]
                    })
                    if login_response.status_code == 200:
                        token = login_response.json()["access_token"]
                        if user_data["role"] == "manager":
                            self.manager_token = token
                        elif user_data["role"] == "user":
                            self.user_token = token
                        elif user_data["role"] == "viewer":
                            self.viewer_token = token
                        self.log_result("authentication", f"Login {user_data['role']}", True)
                    else:
                        self.log_result("authentication", f"Login {user_data['role']}", False, f"Status: {login_response.status_code}")
                else:
                    self.log_result("authentication", f"Register {user_data['role']}", False, f"Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_result("authentication", f"Register {user_data['role']}", False, str(e))

        # Test 3: Test JWT token validation
        if self.admin_token:
            try:
                headers = {"Authorization": f"Bearer {self.admin_token}"}
                response = requests.get(f"{self.base_url}/auth/me", headers=headers)
                if response.status_code == 200:
                    user_data = response.json()
                    if user_data["username"] == "admin" and user_data["role"] == "admin":
                        self.log_result("authentication", "JWT token validation", True)
                    else:
                        self.log_result("authentication", "JWT token validation", False, "Invalid user data returned")
                else:
                    self.log_result("authentication", "JWT token validation", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("authentication", "JWT token validation", False, str(e))

        # Test 4: Test invalid credentials
        try:
            response = requests.post(f"{self.base_url}/auth/login", json={
                "username": "invalid",
                "password": "invalid"
            })
            if response.status_code == 401:
                self.log_result("authentication", "Invalid credentials rejection", True)
            else:
                self.log_result("authentication", "Invalid credentials rejection", False, f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log_result("authentication", "Invalid credentials rejection", False, str(e))

    def test_camera_crud(self):
        print("\n📹 Testing Camera CRUD Operations...")
        
        if not self.admin_token:
            self.log_result("camera_crud", "All camera tests", False, "No admin token available")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test 1: Create camera
        camera_data = {
            "name": "Security Camera 001",
            "model": "Sony FX1000",
            "serial_number": f"SN{uuid.uuid4().hex[:8].upper()}",
            "arrival_date": datetime.now().isoformat(),
            "location": "Main Entrance",
            "warranty_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "notes": "Primary entrance monitoring camera"
        }
        
        try:
            response = requests.post(f"{self.base_url}/cameras", json=camera_data, headers=headers)
            if response.status_code == 200:
                camera = response.json()
                self.test_camera_id = camera["id"]
                self.log_result("camera_crud", "Create camera", True)
            else:
                self.log_result("camera_crud", "Create camera", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("camera_crud", "Create camera", False, str(e))

        # Test 2: Get all cameras
        try:
            response = requests.get(f"{self.base_url}/cameras", headers=headers)
            if response.status_code == 200:
                cameras = response.json()
                if isinstance(cameras, list) and len(cameras) > 0:
                    self.log_result("camera_crud", "Get all cameras", True)
                else:
                    self.log_result("camera_crud", "Get all cameras", False, "No cameras returned")
            else:
                self.log_result("camera_crud", "Get all cameras", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("camera_crud", "Get all cameras", False, str(e))

        # Test 3: Get specific camera
        if self.test_camera_id:
            try:
                response = requests.get(f"{self.base_url}/cameras/{self.test_camera_id}", headers=headers)
                if response.status_code == 200:
                    camera = response.json()
                    if camera["id"] == self.test_camera_id:
                        self.log_result("camera_crud", "Get specific camera", True)
                    else:
                        self.log_result("camera_crud", "Get specific camera", False, "Wrong camera returned")
                else:
                    self.log_result("camera_crud", "Get specific camera", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("camera_crud", "Get specific camera", False, str(e))

        # Test 4: Update camera
        if self.test_camera_id:
            try:
                update_data = {
                    "status": "maintenance",
                    "location": "Storage Room",
                    "notes": "Moved for maintenance"
                }
                response = requests.put(f"{self.base_url}/cameras/{self.test_camera_id}", json=update_data, headers=headers)
                if response.status_code == 200:
                    updated_camera = response.json()
                    if updated_camera["status"] == "maintenance":
                        self.log_result("camera_crud", "Update camera", True)
                    else:
                        self.log_result("camera_crud", "Update camera", False, "Camera not updated properly")
                else:
                    self.log_result("camera_crud", "Update camera", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("camera_crud", "Update camera", False, str(e))

        # Test 5: Search cameras
        try:
            response = requests.get(f"{self.base_url}/cameras?search=Security", headers=headers)
            if response.status_code == 200:
                cameras = response.json()
                if isinstance(cameras, list):
                    self.log_result("camera_crud", "Search cameras", True)
                else:
                    self.log_result("camera_crud", "Search cameras", False, "Invalid response format")
            else:
                self.log_result("camera_crud", "Search cameras", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("camera_crud", "Search cameras", False, str(e))

        # Test 6: Filter cameras by status
        try:
            response = requests.get(f"{self.base_url}/cameras?status=maintenance", headers=headers)
            if response.status_code == 200:
                cameras = response.json()
                if isinstance(cameras, list):
                    self.log_result("camera_crud", "Filter cameras by status", True)
                else:
                    self.log_result("camera_crud", "Filter cameras by status", False, "Invalid response format")
            else:
                self.log_result("camera_crud", "Filter cameras by status", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("camera_crud", "Filter cameras by status", False, str(e))

        # Test 7: Test serial number uniqueness
        try:
            duplicate_camera = {
                "name": "Duplicate Camera",
                "model": "Test Model",
                "serial_number": camera_data["serial_number"],  # Same serial number
                "arrival_date": datetime.now().isoformat()
            }
            response = requests.post(f"{self.base_url}/cameras", json=duplicate_camera, headers=headers)
            if response.status_code == 400:
                self.log_result("camera_crud", "Serial number uniqueness validation", True)
            else:
                self.log_result("camera_crud", "Serial number uniqueness validation", False, f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_result("camera_crud", "Serial number uniqueness validation", False, str(e))

    def test_role_based_access(self):
        print("\n👥 Testing Role-Based Access Control...")
        
        # Test manager permissions
        if self.manager_token and self.test_camera_id:
            headers = {"Authorization": f"Bearer {self.manager_token}"}
            
            # Manager should be able to create cameras
            try:
                camera_data = {
                    "name": "Manager Camera",
                    "model": "Manager Model",
                    "serial_number": f"MNG{uuid.uuid4().hex[:8].upper()}",
                    "arrival_date": datetime.now().isoformat()
                }
                response = requests.post(f"{self.base_url}/cameras", json=camera_data, headers=headers)
                if response.status_code == 200:
                    self.log_result("user_management", "Manager can create cameras", True)
                else:
                    self.log_result("user_management", "Manager can create cameras", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("user_management", "Manager can create cameras", False, str(e))

            # Manager should be able to update cameras
            try:
                update_data = {"notes": "Updated by manager"}
                response = requests.put(f"{self.base_url}/cameras/{self.test_camera_id}", json=update_data, headers=headers)
                if response.status_code == 200:
                    self.log_result("user_management", "Manager can update cameras", True)
                else:
                    self.log_result("user_management", "Manager can update cameras", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("user_management", "Manager can update cameras", False, str(e))

            # Manager should NOT be able to delete cameras (admin only)
            try:
                response = requests.delete(f"{self.base_url}/cameras/{self.test_camera_id}", headers=headers)
                if response.status_code == 403:
                    self.log_result("user_management", "Manager cannot delete cameras", True)
                else:
                    self.log_result("user_management", "Manager cannot delete cameras", False, f"Expected 403, got {response.status_code}")
            except Exception as e:
                self.log_result("user_management", "Manager cannot delete cameras", False, str(e))

        # Test viewer permissions
        if self.viewer_token:
            headers = {"Authorization": f"Bearer {self.viewer_token}"}
            
            # Viewer should be able to read cameras
            try:
                response = requests.get(f"{self.base_url}/cameras", headers=headers)
                if response.status_code == 200:
                    self.log_result("user_management", "Viewer can read cameras", True)
                else:
                    self.log_result("user_management", "Viewer can read cameras", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("user_management", "Viewer can read cameras", False, str(e))

            # Viewer should NOT be able to create cameras
            try:
                camera_data = {
                    "name": "Viewer Camera",
                    "model": "Viewer Model",
                    "serial_number": f"VW{uuid.uuid4().hex[:8].upper()}",
                    "arrival_date": datetime.now().isoformat()
                }
                response = requests.post(f"{self.base_url}/cameras", json=camera_data, headers=headers)
                if response.status_code == 403:
                    self.log_result("user_management", "Viewer cannot create cameras", True)
                else:
                    self.log_result("user_management", "Viewer cannot create cameras", False, f"Expected 403, got {response.status_code}")
            except Exception as e:
                self.log_result("user_management", "Viewer cannot create cameras", False, str(e))

    def test_maintenance_system(self):
        print("\n🔧 Testing Maintenance System...")
        
        if not self.user_token or not self.test_camera_id:
            self.log_result("maintenance", "All maintenance tests", False, "Missing user token or camera ID")
            return

        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # Test 1: Create maintenance log
        try:
            maintenance_data = {
                "camera_id": self.test_camera_id,
                "maintenance_type": "routine",
                "description": "Regular cleaning and inspection",
                "next_maintenance": (datetime.now() + timedelta(days=30)).isoformat(),
                "cost": 50.0
            }
            response = requests.post(f"{self.base_url}/maintenance", json=maintenance_data, headers=headers)
            if response.status_code == 200:
                maintenance_log = response.json()
                self.log_result("maintenance", "Create maintenance log", True)
            else:
                self.log_result("maintenance", "Create maintenance log", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("maintenance", "Create maintenance log", False, str(e))

        # Test 2: Get maintenance history
        try:
            response = requests.get(f"{self.base_url}/maintenance/{self.test_camera_id}", headers=headers)
            if response.status_code == 200:
                maintenance_logs = response.json()
                if isinstance(maintenance_logs, list):
                    self.log_result("maintenance", "Get maintenance history", True)
                else:
                    self.log_result("maintenance", "Get maintenance history", False, "Invalid response format")
            else:
                self.log_result("maintenance", "Get maintenance history", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("maintenance", "Get maintenance history", False, str(e))

        # Test 3: Create maintenance log for non-existent camera
        try:
            maintenance_data = {
                "camera_id": "non-existent-id",
                "maintenance_type": "repair",
                "description": "Test maintenance"
            }
            response = requests.post(f"{self.base_url}/maintenance", json=maintenance_data, headers=headers)
            if response.status_code == 404:
                self.log_result("maintenance", "Maintenance for non-existent camera validation", True)
            else:
                self.log_result("maintenance", "Maintenance for non-existent camera validation", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_result("maintenance", "Maintenance for non-existent camera validation", False, str(e))

    def test_statistics(self):
        print("\n📊 Testing Statistics API...")
        
        if not self.admin_token:
            self.log_result("statistics", "All statistics tests", False, "No admin token available")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test 1: Get dashboard statistics
        try:
            response = requests.get(f"{self.base_url}/stats", headers=headers)
            if response.status_code == 200:
                stats = response.json()
                required_fields = ["total_cameras", "active_cameras", "maintenance_cameras", "status_distribution", "expiring_warranty"]
                if all(field in stats for field in required_fields):
                    self.log_result("statistics", "Get dashboard statistics", True)
                else:
                    missing_fields = [field for field in required_fields if field not in stats]
                    self.log_result("statistics", "Get dashboard statistics", False, f"Missing fields: {missing_fields}")
            else:
                self.log_result("statistics", "Get dashboard statistics", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("statistics", "Get dashboard statistics", False, str(e))

        # Test 2: Verify statistics accuracy
        try:
            # Get cameras count
            cameras_response = requests.get(f"{self.base_url}/cameras", headers=headers)
            stats_response = requests.get(f"{self.base_url}/stats", headers=headers)
            
            if cameras_response.status_code == 200 and stats_response.status_code == 200:
                cameras = cameras_response.json()
                stats = stats_response.json()
                
                actual_total = len(cameras)
                reported_total = stats["total_cameras"]
                
                if actual_total == reported_total:
                    self.log_result("statistics", "Statistics accuracy verification", True)
                else:
                    self.log_result("statistics", "Statistics accuracy verification", False, f"Actual: {actual_total}, Reported: {reported_total}")
            else:
                self.log_result("statistics", "Statistics accuracy verification", False, "Failed to get data for comparison")
        except Exception as e:
            self.log_result("statistics", "Statistics accuracy verification", False, str(e))

    def cleanup_test_data(self):
        """Clean up test data created during testing"""
        print("\n🧹 Cleaning up test data...")
        
        if self.admin_token and self.test_camera_id:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            try:
                response = requests.delete(f"{self.base_url}/cameras/{self.test_camera_id}", headers=headers)
                if response.status_code == 200:
                    print("✅ Test camera deleted successfully")
                else:
                    print(f"⚠️ Failed to delete test camera: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Error during cleanup: {e}")

    def run_all_tests(self):
        print("🚀 Starting Camera Management System Backend Tests")
        print("=" * 60)
        
        self.test_authentication()
        self.test_camera_crud()
        self.test_role_based_access()
        self.test_maintenance_system()
        self.test_statistics()
        
        # Clean up test data
        self.cleanup_test_data()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        
        total_passed = 0
        total_failed = 0
        
        for category, results in self.results.items():
            passed = results["passed"]
            failed = results["failed"]
            total_passed += passed
            total_failed += failed
            
            status = "✅ PASS" if failed == 0 else "❌ FAIL"
            print(f"{category.upper()}: {status} ({passed} passed, {failed} failed)")
            
            if results["errors"]:
                for error in results["errors"]:
                    print(f"  ❌ {error}")
        
        print("-" * 60)
        print(f"OVERALL: {total_passed} passed, {total_failed} failed")
        
        if total_failed == 0:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️ Some tests failed. Check the errors above.")
            return False

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)