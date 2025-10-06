import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Mic, MicOff, Volume2, Home, RefreshCw } from "lucide-react";
import { useToast } from "../hooks/use-toast";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const API = `${BACKEND_URL}/api`;

// Debug logging
console.log('BACKEND_URL:', BACKEND_URL);
console.log('API:', API);

const MathModule = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [speechSynthesis, setSpeechSynthesis] = useState(null);
  const [currentProblem, setCurrentProblem] = useState(null);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Generate session ID
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(newSessionId);

    // Initialize speech APIs
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'en-US';
      setRecognition(recognitionInstance);
    }

    if ('speechSynthesis' in window) {
      setSpeechSynthesis(window.speechSynthesis);
    }

    // Load initial data
    loadProgress(newSessionId);
    generateProblem();
  }, []);

  const loadProgress = async (sessionId) => {
    try {
      const response = await axios.get(`${API}/progress/${sessionId}`);
      setScore(response.data.math_score || 0);
      setStreak(response.data.math_streak || 0);
    } catch (error) {
      console.warn("Could not load progress, starting fresh:", error);
    }
  };

  const generateProblem = async (type = null) => {
    setLoading(true);
    try {
      const params = type ? `?type=${type}` : '';
      const response = await axios.get(`${API}/math/problems${params}`);
      const problem = response.data;
      setCurrentProblem(problem);
      
      setTimeout(() => {
        speak(`Here's a math problem: ${problem.question}`);
      }, 500);
    } catch (error) {
      console.error("Error generating problem:", error);
      toast({
        title: "Error",
        description: "Could not load a new problem. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const speak = (text) => {
    if (speechSynthesis) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.8;
      utterance.pitch = 1.1;
      utterance.volume = 0.8;
      speechSynthesis.speak(utterance);
    }
  };

  const startListening = () => {
    if (recognition) {
      setIsListening(true);
      recognition.start();
      
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript.toLowerCase();
        handleAnswer(transcript);
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
        toast({
          title: "Voice Error",
          description: "Could not hear you clearly. Please try again.",
          variant: "destructive",
        });
      };

      recognition.onend = () => {
        setIsListening(false);
      };
    }
  };

  const handleAnswer = async (transcript) => {
    if (!currentProblem || !sessionId) return;

    // Extract number from transcript
    const numberWords = {
      'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
      'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
      'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
      'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
      'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
      'eighty': 80, 'ninety': 90, 'hundred': 100
    };

    let answer = null;
    
    // Check for number words
    for (const [word, num] of Object.entries(numberWords)) {
      if (transcript.includes(word)) {
        answer = num;
        break;
      }
    }

    // Check for digits
    const digits = transcript.match(/\d+/);
    if (digits) {
      answer = parseInt(digits[0]);
    }

    if (answer === null) {
      speak("I didn't understand your answer. Please say a number.");
      return;
    }

    try {
      // Submit answer to backend
      const response = await axios.post(`${API}/math/answer`, {
        problem_id: currentProblem.id,
        user_answer: answer,
        session_id: sessionId
      });

      const { correct, feedback, next_problem } = response.data;

      if (correct) {
        setScore(score + 1);
        setStreak(streak + 1);
        toast({
          title: "Correct! 🎉",
          description: `Great job! The answer is ${answer}`,
        });
      } else {
        setStreak(0);
        toast({
          title: "Try Again! 📚",
          description: `The correct answer was ${currentProblem.answer}`,
          variant: "destructive",
        });
      }

      speak(feedback);

      // Set next problem
      if (next_problem) {
        setTimeout(() => {
          setCurrentProblem(next_problem);
        }, 2000);
      } else {
        setTimeout(() => {
          generateProblem();
        }, 2000);
      }

    } catch (error) {
      console.error("Error submitting answer:", error);
      toast({
        title: "Error",
        description: "Could not submit answer. Please try again.",
        variant: "destructive",
      });
    }
  };

  const repeatProblem = () => {
    if (currentProblem) {
      speak(currentProblem.question);
    }
  };

  if (loading && !currentProblem) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="text-lg text-gray-600">Loading your math adventure...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <Button 
          onClick={() => navigate('/')}
          variant="outline"
          className="flex items-center gap-2"
        >
          <Home className="w-4 h-4" />
          Home
        </Button>
        <h1 className="text-3xl font-bold text-gray-800">🔢 Math Learning</h1>
        <div className="flex gap-2">
          <Badge variant="secondary" className="text-lg px-3 py-1">
            Score: {score}
          </Badge>
          <Badge variant="outline" className="text-lg px-3 py-1">
            Streak: {streak}
          </Badge>
        </div>
      </div>

      {/* Current Problem */}
      {currentProblem && (
        <Card className="bg-white/90 backdrop-blur-sm border-2 border-orange-200">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl text-orange-700">
              Current Problem
            </CardTitle>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <div className="text-4xl font-bold text-gray-800 mb-4">
              {currentProblem.display}
            </div>
            <p className="text-xl text-gray-600">
              {currentProblem.question}
            </p>
            <div className="flex justify-center gap-4">
              <Button 
                onClick={repeatProblem}
                variant="outline"
                className="flex items-center gap-2"
              >
                <Volume2 className="w-4 h-4" />
                Repeat Question
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Voice Interface */}
      <Card className="bg-white/90 backdrop-blur-sm border-2 border-blue-200">
        <CardHeader className="text-center">
          <CardTitle className="text-xl text-blue-700">
            🎤 Voice Answer
          </CardTitle>
          <p className="text-gray-600">
            Click the microphone and say your answer!
          </p>
        </CardHeader>
        <CardContent className="flex justify-center">
          <Button
            onClick={startListening}
            disabled={isListening || loading}
            className={`w-20 h-20 rounded-full text-white transition-all ${
              isListening 
                ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {isListening ? <MicOff className="w-6 h-6" /> : <Mic className="w-6 h-6" />}
          </Button>
        </CardContent>
      </Card>

      {/* Controls */}
      <Card className="bg-gray-50 border-2 border-gray-200">
        <CardContent className="pt-6">
          <div className="flex justify-center gap-4 flex-wrap">
            <Button 
              onClick={() => generateProblem()}
              disabled={loading}
              className="bg-green-500 hover:bg-green-600 text-white flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              New Problem
            </Button>
            <Button 
              onClick={() => generateProblem('addition')}
              disabled={loading}
              variant="outline"
            >
              + Addition
            </Button>
            <Button 
              onClick={() => generateProblem('subtraction')}
              disabled={loading}
              variant="outline"
            >
              - Subtraction
            </Button>
            <Button 
              onClick={() => generateProblem('multiplication')}
              disabled={loading}
              variant="outline"
            >
              × Multiplication
            </Button>
            <Button 
              onClick={() => generateProblem('division')}
              disabled={loading}
              variant="outline"
            >
              ÷ Division
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Tips */}
      <Card className="bg-yellow-50 border-2 border-yellow-200">
        <CardContent className="pt-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-3 text-center">
            💡 Math Tips
          </h3>
          <div className="space-y-2 text-gray-600 text-sm">
            <p>• Listen carefully to the math problem</p>
            <p>• You can say numbers as words (like "five") or digits</p>
            <p>• Click "Repeat Question" if you need to hear it again</p>
            <p>• Choose specific problem types using the buttons above</p>
            <p>• Build your streak by getting answers right in a row!</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MathModule;