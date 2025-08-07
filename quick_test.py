#!/usr/bin/env python3
"""
Quick test for answer submission endpoints
"""

import requests
import json
import uuid

BASE_URL = "https://670b3075-6934-4fd6-9b6e-cd0c5d44e01c.preview.emergentagent.com/api"
SESSION_ID = str(uuid.uuid4())

def test_answer_endpoints():
    print("Testing answer submission endpoints...")
    
    # Get a math problem first
    print("1. Getting math problem...")
    response = requests.get(f"{BASE_URL}/math/problems")
    if response.status_code == 200:
        math_problem = response.json()
        print(f"   Got problem: {math_problem['question']}")
        print(f"   Problem ID: {math_problem['id']}")
        print(f"   Correct answer: {math_problem['answer']}")
        
        # Test math answer submission
        print("2. Testing math answer submission...")
        payload = {
            "problem_id": math_problem["id"],
            "user_answer": math_problem["answer"],
            "session_id": SESSION_ID
        }
        
        response = requests.post(f"{BASE_URL}/math/answer", json=payload)
        print(f"   Status code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Math answer submission works!")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Math answer submission failed: {response.text}")
    else:
        print(f"   ❌ Failed to get math problem: {response.status_code}")
    
    # Get an English exercise
    print("\n3. Getting English exercise...")
    response = requests.get(f"{BASE_URL}/english/exercises", params={"type": "spelling"})
    if response.status_code == 200:
        english_exercise = response.json()
        print(f"   Got exercise: {english_exercise['question']}")
        print(f"   Exercise ID: {english_exercise['id']}")
        print(f"   Accepted answers: {english_exercise['accepted_answers']}")
        
        # Test English answer submission
        print("4. Testing English answer submission...")
        payload = {
            "exercise_id": english_exercise["id"],
            "user_answer": english_exercise["accepted_answers"][0],
            "session_id": SESSION_ID
        }
        
        response = requests.post(f"{BASE_URL}/english/answer", json=payload)
        print(f"   Status code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ English answer submission works!")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ English answer submission failed: {response.text}")
    else:
        print(f"   ❌ Failed to get English exercise: {response.status_code}")

if __name__ == "__main__":
    test_answer_endpoints()