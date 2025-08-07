// Mock data for EduAssist - will be replaced with backend integration later

export const mockMathData = {
  problems: [
    // Addition
    {
      question: "What is 3 plus 4?",
      display: "3 + 4 = ?",
      answer: 7,
      type: "addition"
    },
    {
      question: "What is 5 plus 2?",
      display: "5 + 2 = ?",
      answer: 7,
      type: "addition"
    },
    {
      question: "What is 8 plus 1?",
      display: "8 + 1 = ?",
      answer: 9,
      type: "addition"
    },
    {
      question: "What is 6 plus 3?",
      display: "6 + 3 = ?",
      answer: 9,
      type: "addition"
    },
    // Subtraction
    {
      question: "What is 10 minus 3?",
      display: "10 - 3 = ?",
      answer: 7,
      type: "subtraction"
    },
    {
      question: "What is 8 minus 2?",
      display: "8 - 2 = ?",
      answer: 6,
      type: "subtraction"
    },
    {
      question: "What is 9 minus 4?",
      display: "9 - 4 = ?",
      answer: 5,
      type: "subtraction"
    },
    // Multiplication
    {
      question: "What is 2 times 3?",
      display: "2 × 3 = ?",
      answer: 6,
      type: "multiplication"
    },
    {
      question: "What is 4 times 2?",
      display: "4 × 2 = ?",
      answer: 8,
      type: "multiplication"
    },
    {
      question: "What is 3 times 3?",
      display: "3 × 3 = ?",
      answer: 9,
      type: "multiplication"
    },
    // Division
    {
      question: "What is 10 divided by 2?",
      display: "10 ÷ 2 = ?",
      answer: 5,
      type: "division"
    },
    {
      question: "What is 8 divided by 4?",
      display: "8 ÷ 4 = ?",
      answer: 2,
      type: "division"
    }
  ]
};

export const mockEnglishData = {
  spelling: [
    {
      question: "How do you spell the word CAT?",
      display: "🐱 CAT",
      acceptedAnswers: ["c a t", "cat", "c-a-t"],
      correctAnswer: "The correct spelling is C-A-T"
    },
    {
      question: "How do you spell the word DOG?",
      display: "🐶 DOG",
      acceptedAnswers: ["d o g", "dog", "d-o-g"],
      correctAnswer: "The correct spelling is D-O-G"
    },
    {
      question: "How do you spell the word BOOK?",
      display: "📖 BOOK",
      acceptedAnswers: ["b o o k", "book", "b-o-o-k"],
      correctAnswer: "The correct spelling is B-O-O-K"
    },
    {
      question: "How do you spell the word TREE?",
      display: "🌳 TREE",
      acceptedAnswers: ["t r e e", "tree", "t-r-e-e"],
      correctAnswer: "The correct spelling is T-R-E-E"
    },
    {
      question: "How do you spell the word HOUSE?",
      display: "🏠 HOUSE",
      acceptedAnswers: ["h o u s e", "house", "h-o-u-s-e"],
      correctAnswer: "The correct spelling is H-O-U-S-E"
    }
  ],
  vocabulary: [
    {
      question: "What is a large animal with a trunk called?",
      display: "🐘 Large animal with trunk",
      acceptedAnswers: ["elephant"],
      correctAnswer: "The answer is elephant",
      explanation: "An elephant is a large animal with a long trunk."
    },
    {
      question: "What do you call the yellow fruit that monkeys like?",
      display: "🍌 Yellow fruit",
      acceptedAnswers: ["banana"],
      correctAnswer: "The answer is banana",
      explanation: "A banana is a yellow fruit that monkeys enjoy eating."
    },
    {
      question: "What do you call water falling from the sky?",
      display: "🌧️ Water from sky",
      acceptedAnswers: ["rain"],
      correctAnswer: "The answer is rain",
      explanation: "Rain is water that falls from clouds in the sky."
    },
    {
      question: "What do you call the big bright light in the sky during the day?",
      display: "☀️ Bright light in sky",
      acceptedAnswers: ["sun"],
      correctAnswer: "The answer is sun",
      explanation: "The sun is the bright star that lights up our day."
    }
  ],
  grammar: [
    {
      question: "Fill in the blank: I ___ a student. Use 'am', 'is', or 'are'.",
      display: "I ___ a student",
      acceptedAnswers: ["am"],
      correctAnswer: "The correct answer is 'am' - I am a student"
    },
    {
      question: "Fill in the blank: She ___ my friend. Use 'am', 'is', or 'are'.",
      display: "She ___ my friend",
      acceptedAnswers: ["is"],
      correctAnswer: "The correct answer is 'is' - She is my friend"
    },
    {
      question: "Fill in the blank: They ___ playing. Use 'am', 'is', or 'are'.",
      display: "They ___ playing",
      acceptedAnswers: ["are"],
      correctAnswer: "The correct answer is 'are' - They are playing"
    },
    {
      question: "What is the plural of 'cat'?",
      display: "cat → ?",
      acceptedAnswers: ["cats"],
      correctAnswer: "The plural of cat is cats"
    }
  ]
};

export default {
  mockMathData,
  mockEnglishData
};