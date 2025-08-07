from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import uuid
import random
from datetime import datetime, timedelta
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="EduAssist API", description="Voice-powered learning for primary school students")

# Create API router
api_router = APIRouter(prefix="/api")

# Enhanced Models
class MathProblem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    display: str
    answer: int
    type: str
    difficulty: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EnglishExercise(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    question: str
    display: str
    accepted_answers: List[str]
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SessionProgress(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    math_score: int = 0
    english_score: int = 0
    math_streak: int = 0
    english_streak: int = 0
    problems_solved: int = 0
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=1))

# Request Models
class MathAnswerRequest(BaseModel):
    problem_id: str
    user_answer: int
    session_id: str

class EnglishAnswerRequest(BaseModel):
    exercise_id: str
    user_answer: str
    session_id: str

# Enhanced Math Problem Generation
def generate_math_problems():
    """Generate comprehensive math problems"""
    problems = []
    
    # Addition problems (easy to medium)
    for i in range(20):
        if i < 10:  # Easy
            a, b = random.randint(1, 10), random.randint(1, 10)
            difficulty = "easy"
        else:  # Medium
            a, b = random.randint(10, 50), random.randint(1, 20)
            difficulty = "medium"
        
        answer = a + b
        problems.append(MathProblem(
            question=f"What is {a} plus {b}?",
            display=f"{a} + {b} = ?",
            answer=answer,
            type="addition",
            difficulty=difficulty
        ))
    
    # Subtraction problems
    for i in range(15):
        if i < 8:  # Easy
            a = random.randint(5, 20)
            b = random.randint(1, a)  # Ensure positive result
            difficulty = "easy"
        else:  # Medium
            a = random.randint(20, 100)
            b = random.randint(1, 50)
            difficulty = "medium"
        
        answer = a - b
        problems.append(MathProblem(
            question=f"What is {a} minus {b}?",
            display=f"{a} - {b} = ?",
            answer=answer,
            type="subtraction",
            difficulty=difficulty
        ))
    
    # Multiplication problems
    for i in range(15):
        if i < 8:  # Easy
            a, b = random.randint(1, 5), random.randint(1, 10)
            difficulty = "easy"
        else:  # Medium
            a, b = random.randint(2, 12), random.randint(2, 12)
            difficulty = "medium"
        
        answer = a * b
        problems.append(MathProblem(
            question=f"What is {a} times {b}?",
            display=f"{a} × {b} = ?",
            answer=answer,
            type="multiplication",
            difficulty=difficulty
        ))
    
    # Division problems (only with whole number results)
    division_pairs = [
        (10, 2), (15, 3), (20, 4), (25, 5), (12, 3), (18, 6), (24, 8),
        (14, 2), (21, 3), (28, 4), (35, 5), (42, 6), (49, 7), (56, 8)
    ]
    
    for a, b in division_pairs:
        answer = a // b
        problems.append(MathProblem(
            question=f"What is {a} divided by {b}?",
            display=f"{a} ÷ {b} = ?",
            answer=answer,
            type="division",
            difficulty="easy" if answer <= 10 else "medium"
        ))
    
    return problems

def generate_english_exercises():
    """Generate comprehensive English exercises"""
    exercises = []
    
    # Spelling exercises
    spelling_words = [
        ("CAT", "🐱"), ("DOG", "🐶"), ("BIRD", "🐦"), ("FISH", "🐠"),
        ("BOOK", "📖"), ("TREE", "🌳"), ("HOUSE", "🏠"), ("CAR", "🚗"),
        ("BALL", "⚽"), ("APPLE", "🍎"), ("FLOWER", "🌸"), ("MOON", "🌙"),
        ("SUN", "☀️"), ("WATER", "💧"), ("HAPPY", "😊"), ("SCHOOL", "🏫"),
        ("FRIEND", "👫"), ("FAMILY", "👨‍👩‍👧‍👦"), ("RAINBOW", "🌈"), ("BUTTERFLY", "🦋")
    ]
    
    for word, emoji in spelling_words:
        difficulty = "easy" if len(word) <= 4 else "medium"
        exercises.append(EnglishExercise(
            type="spelling",
            question=f"How do you spell the word {word}?",
            display=f"{emoji} {word}",
            accepted_answers=[
                word.lower(),
                " ".join(word.lower()),
                "-".join(word.lower())
            ],
            correct_answer=f"The correct spelling is {'-'.join(word)}",
            difficulty=difficulty
        ))
    
    # Vocabulary exercises
    vocabulary = [
        ("elephant", "🐘", "large animal with a trunk", "An elephant is a large animal with a long trunk."),
        ("banana", "🍌", "yellow fruit that monkeys like", "A banana is a yellow fruit that monkeys enjoy eating."),
        ("rain", "🌧️", "water falling from the sky", "Rain is water that falls from clouds in the sky."),
        ("sun", "☀️", "bright light in the sky during the day", "The sun is the bright star that lights up our day."),
        ("ocean", "🌊", "large body of salt water", "An ocean is a very large body of salt water."),
        ("mountain", "⛰️", "very tall land formation", "A mountain is a very tall piece of land."),
        ("doctor", "👨‍⚕️", "person who helps sick people", "A doctor is someone who helps people when they are sick."),
        ("teacher", "👩‍🏫", "person who helps children learn", "A teacher is someone who helps children learn new things.")
    ]
    
    for word, emoji, question, explanation in vocabulary:
        exercises.append(EnglishExercise(
            type="vocabulary",
            question=f"What is {question}?",
            display=f"{emoji} {question}",
            accepted_answers=[word],
            correct_answer=f"The answer is {word}",
            explanation=explanation,
            difficulty="easy"
        ))
    
    # Grammar exercises
    grammar = [
        ("I ___ a student", "am", ["am"], "The correct answer is 'am' - I am a student"),
        ("She ___ my friend", "is", ["is"], "The correct answer is 'is' - She is my friend"),
        ("They ___ playing", "are", ["are"], "The correct answer is 'are' - They are playing"),
        ("We ___ happy", "are", ["are"], "The correct answer is 'are' - We are happy"),
        ("He ___ tall", "is", ["is"], "The correct answer is 'is' - He is tall"),
        ("cat → ?", "cats", ["cats"], "The plural of cat is cats"),
        ("dog → ?", "dogs", ["dogs"], "The plural of dog is dogs"),
        ("book → ?", "books", ["books"], "The plural of book is books")
    ]
    
    for display, answer, accepted, explanation in grammar:
        exercises.append(EnglishExercise(
            type="grammar",
            question=f"Fill in the blank or complete: {display}",
            display=display,
            accepted_answers=accepted,
            correct_answer=explanation,
            difficulty="easy"
        ))
    
    return exercises

# API Endpoints
@api_router.get("/")
async def root():
    return {"message": "EduAssist API - Voice-powered learning for everyone!"}

@api_router.get("/math/problems", response_model=MathProblem)
async def get_math_problem(
    type: Optional[str] = Query(None, description="Problem type: addition, subtraction, multiplication, division"),
    difficulty: Optional[str] = Query(None, description="Difficulty: easy, medium, hard")
):
    """Get a random math problem based on type and difficulty"""
    try:
        # Build query
        query = {}
        if type and type != "all":
            query["type"] = type
        if difficulty:
            query["difficulty"] = difficulty
        
        # Get random problem from database
        pipeline = [{"$match": query}, {"$sample": {"size": 1}}]
        problems = await db.math_problems.aggregate(pipeline).to_list(1)
        
        if not problems:
            # If no problems in DB, generate some
            await initialize_data()
            problems = await db.math_problems.aggregate(pipeline).to_list(1)
        
        if problems:
            problem = problems[0]
            problem["id"] = str(problem["_id"])
            return MathProblem(**problem)
        
        raise HTTPException(status_code=404, detail="No problems found")
    
    except Exception as e:
        logger.error(f"Error getting math problem: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.post("/math/answer")
async def submit_math_answer(request: MathAnswerRequest):
    """Submit math answer and get feedback"""
    try:
        # Get the problem
        problem = await db.math_problems.find_one({"_id": request.problem_id})
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        correct = request.user_answer == problem["answer"]
        
        # Update session progress
        await update_session_progress(request.session_id, "math", correct)
        
        # Generate feedback
        if correct:
            feedback = f"Excellent! {request.user_answer} is correct! Let's try another one."
        else:
            feedback = f"Not quite right. The correct answer is {problem['answer']}. Let's try another problem."
        
        # Get next problem
        next_problem = await get_math_problem(type=problem.get("type"), difficulty=problem.get("difficulty"))
        
        return {
            "correct": correct,
            "feedback": feedback,
            "next_problem": next_problem
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting math answer: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/english/exercises", response_model=EnglishExercise)
async def get_english_exercise(
    type: Optional[str] = Query("spelling", description="Exercise type: spelling, vocabulary, grammar"),
    difficulty: Optional[str] = Query(None, description="Difficulty: easy, medium, hard")
):
    """Get a random English exercise based on type and difficulty"""
    try:
        # Build query
        query = {"type": type}
        if difficulty:
            query["difficulty"] = difficulty
        
        # Get random exercise from database
        pipeline = [{"$match": query}, {"$sample": {"size": 1}}]
        exercises = await db.english_exercises.aggregate(pipeline).to_list(1)
        
        if not exercises:
            # If no exercises in DB, generate some
            await initialize_data()
            exercises = await db.english_exercises.aggregate(pipeline).to_list(1)
        
        if exercises:
            exercise = exercises[0]
            exercise["id"] = str(exercise["_id"])
            return EnglishExercise(**exercise)
        
        raise HTTPException(status_code=404, detail="No exercises found")
    
    except Exception as e:
        logger.error(f"Error getting English exercise: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.post("/english/answer")
async def submit_english_answer(request: EnglishAnswerRequest):
    """Submit English answer and get feedback"""
    try:
        # Get the exercise
        exercise = await db.english_exercises.find_one({"_id": request.exercise_id})
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        # Check if answer is correct
        correct = any(
            accepted.lower() in request.user_answer.lower() 
            for accepted in exercise["accepted_answers"]
        )
        
        # Update session progress
        await update_session_progress(request.session_id, "english", correct)
        
        # Generate feedback
        if correct:
            explanation = exercise.get("explanation", "")
            feedback = f"Excellent! That's correct! {explanation} Let's try another one."
        else:
            feedback = f"{exercise['correct_answer']} Let's try another one."
        
        # Get next exercise
        next_exercise = await get_english_exercise(type=exercise["type"])
        
        return {
            "correct": correct,
            "feedback": feedback,
            "next_exercise": next_exercise
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting English answer: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/progress/{session_id}", response_model=SessionProgress)
async def get_progress(session_id: str):
    """Get learning progress for a session"""
    try:
        progress = await db.session_progress.find_one({"session_id": session_id})
        if not progress:
            # Create new session
            new_progress = SessionProgress(session_id=session_id)
            await db.session_progress.insert_one(new_progress.dict())
            return new_progress
        
        progress["id"] = str(progress["_id"])
        return SessionProgress(**progress)
    
    except Exception as e:
        logger.error(f"Error getting progress: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Helper Functions
async def update_session_progress(session_id: str, subject: str, correct: bool):
    """Update session progress"""
    try:
        progress = await db.session_progress.find_one({"session_id": session_id})
        
        if not progress:
            progress = SessionProgress(session_id=session_id).dict()
            progress.pop("id")  # Remove id for insertion
        
        # Update scores and streaks
        if subject == "math":
            if correct:
                progress["math_score"] = progress.get("math_score", 0) + 1
                progress["math_streak"] = progress.get("math_streak", 0) + 1
            else:
                progress["math_streak"] = 0
        else:  # english
            if correct:
                progress["english_score"] = progress.get("english_score", 0) + 1
                progress["english_streak"] = progress.get("english_streak", 0) + 1
            else:
                progress["english_streak"] = 0
        
        progress["problems_solved"] = progress.get("problems_solved", 0) + 1
        progress["last_activity"] = datetime.utcnow()
        progress["expires_at"] = datetime.utcnow() + timedelta(days=1)
        
        # Upsert progress
        await db.session_progress.replace_one(
            {"session_id": session_id}, 
            progress, 
            upsert=True
        )
    
    except Exception as e:
        logger.error(f"Error updating session progress: {e}")

async def initialize_data():
    """Initialize database with learning content"""
    try:
        # Check if data already exists
        math_count = await db.math_problems.count_documents({})
        english_count = await db.english_exercises.count_documents({})
        
        if math_count == 0:
            # Generate and insert math problems
            problems = generate_math_problems()
            problem_dicts = [p.dict() for p in problems]
            for p in problem_dicts:
                p["_id"] = p.pop("id")
            await db.math_problems.insert_many(problem_dicts)
            logger.info(f"Inserted {len(problems)} math problems")
        
        if english_count == 0:
            # Generate and insert English exercises
            exercises = generate_english_exercises()
            exercise_dicts = [e.dict() for e in exercises]
            for e in exercise_dicts:
                e["_id"] = e.pop("id")
            await db.english_exercises.insert_many(exercise_dicts)
            logger.info(f"Inserted {len(exercises)} English exercises")
    
    except Exception as e:
        logger.error(f"Error initializing data: {e}")

# Include the router
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize data on startup"""
    logger.info("EduAssist API starting up...")
    await initialize_data()
    logger.info("EduAssist API ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown"""
    client.close()
    logger.info("EduAssist API shutdown complete.")