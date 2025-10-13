import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Mic, MicOff, Volume2, Home, RefreshCw, BookOpen } from "lucide-react";
import { useToast } from "../hooks/use-toast";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const API = `${BACKEND_URL}/api`;

const EnglishModule = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [speechSynthesis, setSpeechSynthesis] = useState(null);
  const [currentExercise, setCurrentExercise] = useState(null);
  const [exerciseType, setExerciseType] = useState('spelling');
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
  }, []);

  useEffect(() => {
    // Generate exercise when type changes
    generateExercise();
  }, [exerciseType]);

  const loadProgress = async (sessionId) => {
    try {
      const response = await axios.get(`${API}/progress/${sessionId}`);
      setScore(response.data.english_score || 0);
      setStreak(response.data.english_streak || 0);
    } catch (error) {
      console.warn("Could not load progress, starting fresh:", error);
    }
  };

  const generateExercise = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/english/exercises?type=${exerciseType}`);
      const exercise = response.data;
      setCurrentExercise(exercise);
      
      setTimeout(() => {
        speak(exercise.question);
      }, 500);
    } catch (error) {
      console.error("Error generating exercise:", error);
      toast({
        title: "Error",
        description: "Could not load a new exercise. Please try again.",
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
    if (!currentExercise || !sessionId) return;

    try {
      // Submit answer to backend
      const response = await axios.post(`${API}/english/answer`, {
        exercise_id: currentExercise.id,
        user_answer: transcript,
        session_id: sessionId
      });

      const { correct, feedback, next_exercise } = response.data;

      if (correct) {
        setScore(score + 1);
        setStreak(streak + 1);
        toast({
          title: "Correct! 🎉",
          description: "Great job! You got it right!",
        });
      } else {
        setStreak(0);
        toast({
          title: "Try Again! 📚",
          description: "Keep practicing, you're doing great!",
          variant: "destructive",
        });
      }

      speak(feedback);

      // Set next exercise
      if (next_exercise) {
        setTimeout(() => {
          setCurrentExercise(next_exercise);
        }, 2000);
      } else {
        setTimeout(() => {
          generateExercise();
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

  const repeatQuestion = () => {
    if (currentExercise) {
      speak(currentExercise.question);
    }
  };

  const changeExerciseType = (type) => {
    setExerciseType(type);
    speak(`Switching to ${type} exercises!`);
  };

  if (loading && !currentExercise) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          <p className="text-lg text-gray-600">Loading your English adventure...</p>
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
        <h1 className="text-3xl font-bold text-gray-800">📚 English Learning</h1>
        <div className="flex gap-2">
          <Badge variant="secondary" className="text-lg px-3 py-1">
            Score: {score}
          </Badge>
          <Badge variant="outline" className="text-lg px-3 py-1">
            Streak: {streak}
          </Badge>
        </div>
      </div>

      {/* Exercise Type Selector */}
      <Card className="bg-white/90 backdrop-blur-sm border-2 border-purple-200">
        <CardHeader className="text-center">
          <CardTitle className="text-xl text-purple-700">
            Choose Exercise Type
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center gap-4 flex-wrap">
            <Button 
              onClick={() => changeExerciseType('spelling')}
              variant={exerciseType === 'spelling' ? 'default' : 'outline'}
              className="flex items-center gap-2"
              disabled={loading}
            >
              ✏️ Spelling
            </Button>
            <Button 
              onClick={() => changeExerciseType('vocabulary')}
              variant={exerciseType === 'vocabulary' ? 'default' : 'outline'}
              className="flex items-center gap-2"
              disabled={loading}
            >
              📝 Vocabulary
            </Button>
            <Button 
              onClick={() => changeExerciseType('grammar')}
              variant={exerciseType === 'grammar' ? 'default' : 'outline'}
              className="flex items-center gap-2"
              disabled={loading}
            >
              📖 Grammar
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Current Exercise */}
      {currentExercise && (
        <Card className="bg-white/90 backdrop-blur-sm border-2 border-indigo-200">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl text-indigo-700">
              Current {exerciseType.charAt(0).toUpperCase() + exerciseType.slice(1)} Exercise
            </CardTitle>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <div className="text-xl text-gray-800 mb-4">
              {currentExercise.display && (
                <div className="text-3xl font-bold mb-2">{currentExercise.display}</div>
              )}
              <p>{currentExercise.question}</p>
            </div>
            <div className="flex justify-center gap-4">
              <Button 
                onClick={repeatQuestion}
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
          <div className="flex justify-center">
            <Button 
              onClick={generateExercise}
              disabled={loading}
              className="bg-green-500 hover:bg-green-600 text-white flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              New Exercise
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Tips */}
      <Card className="bg-yellow-50 border-2 border-yellow-200">
        <CardContent className="pt-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-3 text-center">
            💡 English Tips
          </h3>
          <div className="space-y-2 text-gray-600 text-sm">
            <p>• Listen carefully to the question</p>
            <p>• For spelling, say each letter clearly (like "C-A-T")</p>
            <p>• For vocabulary, say the answer word clearly</p>
            <p>• For grammar, choose the correct word</p>
            <p>• Click "Repeat Question" if you need to hear it again</p>
            <p>• Switch between spelling, vocabulary, and grammar exercises</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default EnglishModule;