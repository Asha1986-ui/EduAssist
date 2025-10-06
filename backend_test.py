#!/usr/bin/env python3
"""
EduAssist Backend API Test Suite
Tests all backend endpoints for the voice-powered learning application
"""

import requests
import json
import uuid
import time
from typing import Dict, Any

# Configuration
BASE_URL = "https://670b3075-6934-4fd6-9b6e-cd0c5d44e01c.preview.emergentagent.com/api"
SESSION_ID = str(uuid.uuid4())

class EduAssistTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session_id = SESSION_ID
        self.test_results = []
        self.current_math_problem = None
        self.current_english_exercise = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def test_health_check(self):
        """Test GET /api/ - Health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "EduAssist" in data["message"]:
                    self.log_test("Health Check", True, f"Response: {data['message']}")
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected response format: {data}")
                    return False
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False
    
    def test_math_problems(self):
        """Test GET /api/math/problems with different parameters"""
        test_cases = [
            {"params": {}, "name": "Random Math Problem"},
            {"params": {"type": "addition"}, "name": "Addition Problems"},
            {"params": {"type": "subtraction"}, "name": "Subtraction Problems"},
            {"params": {"type": "multiplication"}, "name": "Multiplication Problems"},
            {"params": {"type": "division"}, "name": "Division Problems"},
            {"params": {"difficulty": "easy"}, "name": "Easy Problems"},
            {"params": {"difficulty": "medium"}, "name": "Medium Problems"},
            {"params": {"type": "addition", "difficulty": "easy"}, "name": "Easy Addition Problems"}
        ]
        
        all_passed = True
        
        for case in test_cases:
            try:
                response = requests.get(f"{self.base_url}/math/problems", params=case["params"], timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["id", "question", "display", "answer", "type", "difficulty"]
                    
                    if all(field in data for field in required_fields):
                        # Store first problem for answer testing
                        if self.current_math_problem is None:
                            self.current_math_problem = data
                        
                        # Validate specific parameters if provided
                        valid = True
                        if "type" in case["params"] and data["type"] != case["params"]["type"]:
                            valid = False
                        if "difficulty" in case["params"] and data["difficulty"] != case["params"]["difficulty"]:
                            valid = False
                        
                        if valid:
                            self.log_test(f"Math Problems - {case['name']}", True, 
                                        f"Type: {data['type']}, Difficulty: {data['difficulty']}, Question: {data['question']}")
                        else:
                            self.log_test(f"Math Problems - {case['name']}", False, 
                                        f"Parameter mismatch. Expected: {case['params']}, Got: type={data['type']}, difficulty={data['difficulty']}")
                            all_passed = False
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_test(f"Math Problems - {case['name']}", False, f"Missing fields: {missing}")
                        all_passed = False
                else:
                    self.log_test(f"Math Problems - {case['name']}", False, f"Status code: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Math Problems - {case['name']}", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_math_answers(self):
        """Test POST /api/math/answer with correct and incorrect answers"""
        if not self.current_math_problem:
            self.log_test("Math Answer Submission", False, "No math problem available for testing")
            return False
        
        test_cases = [
            {
                "answer": self.current_math_problem["answer"],
                "name": "Correct Math Answer",
                "expected_correct": True
            },
            {
                "answer": self.current_math_problem["answer"] + 999,  # Definitely wrong
                "name": "Incorrect Math Answer", 
                "expected_correct": False
            }
        ]
        
        all_passed = True
        
        for case in test_cases:
            try:
                payload = {
                    "problem_id": self.current_math_problem["id"],
                    "user_answer": case["answer"],
                    "session_id": self.session_id
                }
                
                response = requests.post(f"{self.base_url}/math/answer", json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["correct", "feedback", "next_problem"]
                    
                    if all(field in data for field in required_fields):
                        if data["correct"] == case["expected_correct"]:
                            self.log_test(f"Math Answer - {case['name']}", True, 
                                        f"Correct: {data['correct']}, Feedback: {data['feedback'][:50]}...")
                        else:
                            self.log_test(f"Math Answer - {case['name']}", False, 
                                        f"Expected correct={case['expected_correct']}, got {data['correct']}")
                            all_passed = False
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_test(f"Math Answer - {case['name']}", False, f"Missing fields: {missing}")
                        all_passed = False
                else:
                    self.log_test(f"Math Answer - {case['name']}", False, f"Status code: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Math Answer - {case['name']}", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_english_exercises(self):
        """Test GET /api/english/exercises with different types"""
        test_cases = [
            {"params": {"type": "spelling"}, "name": "Spelling Exercises"},
            {"params": {"type": "vocabulary"}, "name": "Vocabulary Exercises"},
            {"params": {"type": "grammar"}, "name": "Grammar Exercises"},
            {"params": {"type": "spelling", "difficulty": "easy"}, "name": "Easy Spelling Exercises"}
        ]
        
        all_passed = True
        
        for case in test_cases:
            try:
                response = requests.get(f"{self.base_url}/english/exercises", params=case["params"], timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["id", "type", "question", "display", "accepted_answers", "correct_answer", "difficulty"]
                    
                    if all(field in data for field in required_fields):
                        # Store first exercise for answer testing
                        if self.current_english_exercise is None:
                            self.current_english_exercise = data
                        
                        # Validate specific parameters
                        valid = True
                        if "type" in case["params"] and data["type"] != case["params"]["type"]:
                            valid = False
                        if "difficulty" in case["params"] and data["difficulty"] != case["params"]["difficulty"]:
                            valid = False
                        
                        if valid and isinstance(data["accepted_answers"], list):
                            self.log_test(f"English Exercises - {case['name']}", True, 
                                        f"Type: {data['type']}, Question: {data['question']}")
                        else:
                            self.log_test(f"English Exercises - {case['name']}", False, 
                                        f"Parameter mismatch or invalid accepted_answers format")
                            all_passed = False
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_test(f"English Exercises - {case['name']}", False, f"Missing fields: {missing}")
                        all_passed = False
                else:
                    self.log_test(f"English Exercises - {case['name']}", False, f"Status code: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"English Exercises - {case['name']}", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_english_answers(self):
        """Test POST /api/english/answer with correct and incorrect answers"""
        if not self.current_english_exercise:
            self.log_test("English Answer Submission", False, "No English exercise available for testing")
            return False
        
        # Get a correct answer from accepted answers
        correct_answer = self.current_english_exercise["accepted_answers"][0]
        
        test_cases = [
            {
                "answer": correct_answer,
                "name": "Correct English Answer",
                "expected_correct": True
            },
            {
                "answer": "definitely_wrong_answer_12345",
                "name": "Incorrect English Answer",
                "expected_correct": False
            }
        ]
        
        all_passed = True
        
        for case in test_cases:
            try:
                payload = {
                    "exercise_id": self.current_english_exercise["id"],
                    "user_answer": case["answer"],
                    "session_id": self.session_id
                }
                
                response = requests.post(f"{self.base_url}/english/answer", json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["correct", "feedback", "next_exercise"]
                    
                    if all(field in data for field in required_fields):
                        if data["correct"] == case["expected_correct"]:
                            self.log_test(f"English Answer - {case['name']}", True, 
                                        f"Correct: {data['correct']}, Feedback: {data['feedback'][:50]}...")
                        else:
                            self.log_test(f"English Answer - {case['name']}", False, 
                                        f"Expected correct={case['expected_correct']}, got {data['correct']}")
                            all_passed = False
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_test(f"English Answer - {case['name']}", False, f"Missing fields: {missing}")
                        all_passed = False
                else:
                    self.log_test(f"English Answer - {case['name']}", False, f"Status code: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"English Answer - {case['name']}", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_session_progress(self):
        """Test GET /api/progress/{session_id} for session tracking"""
        try:
            response = requests.get(f"{self.base_url}/progress/{self.session_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["id", "session_id", "math_score", "english_score", 
                                 "math_streak", "english_streak", "problems_solved", "last_activity"]
                
                if all(field in data for field in required_fields):
                    # Verify session ID matches
                    if data["session_id"] == self.session_id:
                        # Check if progress was updated from previous answer submissions
                        total_problems = data["problems_solved"]
                        math_score = data["math_score"]
                        english_score = data["english_score"]
                        
                        self.log_test("Session Progress Tracking", True, 
                                    f"Session ID: {data['session_id']}, Problems solved: {total_problems}, "
                                    f"Math score: {math_score}, English score: {english_score}")
                        return True
                    else:
                        self.log_test("Session Progress Tracking", False, 
                                    f"Session ID mismatch. Expected: {self.session_id}, Got: {data['session_id']}")
                        return False
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Session Progress Tracking", False, f"Missing fields: {missing}")
                    return False
            else:
                self.log_test("Session Progress Tracking", False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Session Progress Tracking", False, f"Exception: {str(e)}")
            return False
    
    def test_data_initialization(self):
        """Test that database is properly initialized with problems and exercises"""
        try:
            # Test that we can get different types of problems
            math_types = ["addition", "subtraction", "multiplication", "division"]
            english_types = ["spelling", "vocabulary", "grammar"]
            
            math_problems_found = []
            english_exercises_found = []
            
            # Test math problem diversity
            for math_type in math_types:
                response = requests.get(f"{self.base_url}/math/problems", 
                                      params={"type": math_type}, timeout=10)
                if response.status_code == 200:
                    math_problems_found.append(math_type)
            
            # Test English exercise diversity
            for english_type in english_types:
                response = requests.get(f"{self.base_url}/english/exercises", 
                                      params={"type": english_type}, timeout=10)
                if response.status_code == 200:
                    english_exercises_found.append(english_type)
            
            # Check if all types are available
            math_success = len(math_problems_found) == len(math_types)
            english_success = len(english_exercises_found) == len(english_types)
            
            if math_success and english_success:
                self.log_test("Data Initialization", True, 
                            f"Math types: {math_problems_found}, English types: {english_exercises_found}")
                return True
            else:
                missing_math = [t for t in math_types if t not in math_problems_found]
                missing_english = [t for t in english_types if t not in english_exercises_found]
                self.log_test("Data Initialization", False, 
                            f"Missing math types: {missing_math}, Missing English types: {missing_english}")
                return False
                
        except Exception as e:
            self.log_test("Data Initialization", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all test suites"""
        print("=" * 60)
        print("EduAssist Backend API Test Suite")
        print("=" * 60)
        print(f"Testing against: {self.base_url}")
        print(f"Session ID: {self.session_id}")
        print("=" * 60)
        
        # Run tests in logical order
        tests = [
            ("Health Check", self.test_health_check),
            ("Data Initialization", self.test_data_initialization),
            ("Math Problems", self.test_math_problems),
            ("Math Answer Submission", self.test_math_answers),
            ("English Exercises", self.test_english_exercises),
            ("English Answer Submission", self.test_english_answers),
            ("Session Progress", self.test_session_progress)
        ]
        
        passed = 0
        total = 0
        
        for test_name, test_func in tests:
            print(f"\nRunning {test_name} Tests...")
            result = test_func()
            if result:
                passed += 1
            total += 1
            time.sleep(1)  # Brief pause between test suites
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (passed / total) * 100 if total > 0 else 0
        print(f"Test Suites Passed: {passed}/{total} ({success_rate:.1f}%)")
        
        # Detailed results
        print("\nDetailed Results:")
        for result in self.test_results:
            status = "PASS" if result["success"] else "FAIL"
            print(f"{status} {result['test']}")
            if result["details"] and not result["success"]:
                print(f"   WARNING: {result['details']}")
        
        print("\n" + "=" * 60)
        
        if passed == total:
            print("ALL TESTS PASSED! EduAssist backend is working perfectly!")
            return True
        else:
            print(f"WARNING: {total - passed} test suite(s) failed. Please check the issues above.")
            return False

def main():
    """Main test execution"""
    tester = EduAssistTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ Backend API is fully functional and ready for production!")
        exit(0)
    else:
        print("\n❌ Backend API has issues that need to be addressed.")
        exit(1)

if __name__ == "__main__":
    main()