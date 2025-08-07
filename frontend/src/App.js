import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import MathModule from "./components/MathModule";
import EnglishModule from "./components/EnglishModule";
import { Toaster } from "./components/ui/toaster";

function App() {
  return (
    <div className="App min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/math" element={<MathModule />} />
          <Route path="/english" element={<EnglishModule />} />
        </Routes>
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;