# EduAssist API Contracts

## Overview
This document defines the API contracts and integration plan for EduAssist backend development.

## Current Mock Data to Replace
- `mockMathData.problems` - Math problems with answers
- `mockEnglishData.spelling/vocabulary/grammar` - English exercises

## Backend API Endpoints

### 1. Math Learning APIs

#### GET /api/math/problems
- **Purpose**: Get random math problems based on difficulty
- **Query Params**: 
  - `type`: "addition", "subtraction", "multiplication", "division", "all"
  - `difficulty`: "easy", "medium", "hard"
- **Response**:
```json
{
  "id": "unique_id",
  "question": "What is 7 plus 5?",
  "display": "7 + 5 = ?",
  "answer": 12,
  "type": "addition",
  "difficulty": "easy"
}
```

#### POST /api/math/answer
- **Purpose**: Submit math answer and get feedback
- **Request**:
```json
{
  "problem_id": "unique_id",
  "user_answer": 12,
  "session_id": "browser_session"
}
```
- **Response**:
```json
{
  "correct": true,
  "feedback": "Excellent! 12 is correct!",
  "next_problem": {...}
}
```

### 2. English Learning APIs

#### GET /api/english/exercises
- **Purpose**: Get English exercises by type
- **Query Params**:
  - `type`: "spelling", "vocabulary", "grammar"
  - `difficulty`: "easy", "medium", "hard"
- **Response**:
```json
{
  "id": "unique_id",
  "type": "spelling",
  "question": "How do you spell the word CAT?",
  "display": "🐱 CAT",
  "accepted_answers": ["c a t", "cat", "c-a-t"],
  "correct_answer": "The correct spelling is C-A-T"
}
```

#### POST /api/english/answer
- **Purpose**: Submit English answer and get feedback
- **Request**:
```json
{
  "exercise_id": "unique_id",
  "user_answer": "c a t",
  "session_id": "browser_session"
}
```
- **Response**:
```json
{
  "correct": true,
  "feedback": "Excellent! That's correct!",
  "next_exercise": {...}
}
```

### 3. Learning Progress APIs (Optional Enhancement)

#### GET /api/progress/{session_id}
- **Purpose**: Get learning progress for a browser session
- **Response**:
```json
{
  "math_score": 15,
  "english_score": 12,
  "math_streak": 3,
  "english_streak": 5,
  "problems_solved": 25
}
```

## Frontend Integration Plan

### Files to Update:
1. **MathModule.jsx** - Replace `mockMathData` usage with API calls
2. **EnglishModule.jsx** - Replace `mockEnglishData` usage with API calls
3. **Remove** - `mockData.js` file after integration

### Integration Points:
- Replace `generateProblem()` with API call to `/api/math/problems`
- Replace `handleAnswer()` with API call to `/api/math/answer`
- Replace `generateExercise()` with API call to `/api/english/exercises`
- Add error handling for offline scenarios
- Maintain local scoring while session is active

## Database Models

### MathProblem Collection
```
{
  _id: ObjectId,
  question: String,
  display: String,
  answer: Number,
  type: String,
  difficulty: String,
  created_at: Date
}
```

### EnglishExercise Collection
```
{
  _id: ObjectId,
  type: String,
  question: String,
  display: String,
  accepted_answers: [String],
  correct_answer: String,
  explanation: String,
  difficulty: String,
  created_at: Date
}
```

### SessionProgress Collection (Browser Session Tracking)
```
{
  _id: ObjectId,
  session_id: String,
  math_score: Number,
  english_score: Number,
  math_streak: Number,
  english_streak: Number,
  problems_solved: Number,
  last_activity: Date,
  expires_at: Date
}
```

## Implementation Notes
- No user authentication required (privacy-focused)
- Use browser-generated session IDs for progress tracking
- Sessions expire after 24 hours of inactivity
- All sensitive processing stays in browser (voice recognition/synthesis)
- Backend only handles educational content generation and basic progress tracking