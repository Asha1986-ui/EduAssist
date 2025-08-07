import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Mic, MicOff, Volume2, BookOpen, Calculator } from "lucide-react";
import { useToast } from "../hooks/use-toast";

const HomePage = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [speechSynthesis, setSpeechSynthesis] = useState(null);

  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'en-US';
      setRecognition(recognitionInstance);
    }

    // Initialize speech synthesis
    if ('speechSynthesis' in window) {
      setSpeechSynthesis(window.speechSynthesis);
    }
  }, []);

  const startListening = () => {
    if (recognition) {
      setIsListening(true);
      recognition.start();
      
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript.toLowerCase();
        handleVoiceCommand(transcript);
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
    } else {
      toast({
        title: "Voice Not Supported",
        description: "Your browser doesn't support voice recognition.",
        variant: "destructive",
      });
    }
  };

  const handleVoiceCommand = (transcript) => {
    speak(`You said: ${transcript}`);
    
    if (transcript.includes('math') || transcript.includes('calculate') || transcript.includes('plus') || transcript.includes('minus')) {
      setTimeout(() => {
        speak("Taking you to math learning!");
        navigate('/math');
      }, 2000);
    } else if (transcript.includes('english') || transcript.includes('spell') || transcript.includes('word')) {
      setTimeout(() => {
        speak("Taking you to english learning!");
        navigate('/english');
      }, 2000);
    } else {
      setTimeout(() => {
        speak("Say math for math learning, or english for english learning!");
      }, 2000);
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

  const handleWelcome = () => {
    speak("Welcome to EduAssist! I'm here to help you learn math and english. Click the microphone and say math or english to get started!");
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-4xl w-full space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-6xl font-bold text-gray-800">
            🎓 EduAssist
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Your friendly voice-powered learning companion for math and English!
          </p>
          <Button 
            onClick={handleWelcome}
            className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 text-lg"
          >
            <Volume2 className="w-5 h-5 mr-2" />
            Welcome Message
          </Button>
        </div>

        {/* Voice Interface */}
        <Card className="bg-white/80 backdrop-blur-sm border-2 border-green-200">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl text-gray-700">
              🎤 Voice Learning
            </CardTitle>
            <p className="text-gray-600">
              Click the microphone and say "math" or "english" to start learning!
            </p>
          </CardHeader>
          <CardContent className="flex justify-center">
            <Button
              onClick={startListening}
              disabled={isListening}
              className={`w-24 h-24 rounded-full text-white transition-all ${
                isListening 
                  ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                  : 'bg-blue-500 hover:bg-blue-600'
              }`}
            >
              {isListening ? <MicOff className="w-8 h-8" /> : <Mic className="w-8 h-8" />}
            </Button>
          </CardContent>
        </Card>

        {/* Learning Options */}
        <div className="grid md:grid-cols-2 gap-6">
          <Card 
            className="bg-orange-50 border-2 border-orange-200 cursor-pointer hover:shadow-lg transition-all hover:scale-105"
            onClick={() => navigate('/math')}
          >
            <CardHeader className="text-center">
              <Calculator className="w-12 h-12 mx-auto text-orange-600 mb-2" />
              <CardTitle className="text-2xl text-orange-700">Math Learning</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 text-center">
                Practice addition, subtraction, multiplication and division with voice!
              </p>
              <p className="text-sm text-gray-500 text-center mt-2">
                Try: "What is 7 plus 5?"
              </p>
            </CardContent>
          </Card>

          <Card 
            className="bg-purple-50 border-2 border-purple-200 cursor-pointer hover:shadow-lg transition-all hover:scale-105"
            onClick={() => navigate('/english')}
          >
            <CardHeader className="text-center">
              <BookOpen className="w-12 h-12 mx-auto text-purple-600 mb-2" />
              <CardTitle className="text-2xl text-purple-700">English Learning</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 text-center">
                Learn spelling, vocabulary and simple grammar with voice!
              </p>
              <p className="text-sm text-gray-500 text-center mt-2">
                Try: "How do you spell cat?"
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Instructions */}
        <Card className="bg-yellow-50 border-2 border-yellow-200">
          <CardContent className="pt-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-3 text-center">
              📋 How to Use EduAssist
            </h3>
            <div className="space-y-2 text-gray-600">
              <p>• Click the microphone button to start voice recognition</p>
              <p>• Say "math" to practice math problems</p>
              <p>• Say "english" to practice english skills</p>
              <p>• Speak clearly and wait for the response</p>
              <p>• All learning happens in your browser - no internet needed!</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default HomePage;