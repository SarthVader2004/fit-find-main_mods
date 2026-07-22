// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Chatbot from "./components/Chatbot";
import BodyType from "./components/BodyType";
import VirtualTryOn from "./components/VirtualTryOn"; // 👗 Virtual Try-On Page
import BackgroundVideo from "./components/BackgroundVideo";
import "./App.css";

const App = () => {
  return (
    <>
      {/* 🎥 Persistent Background Video */}
      <BackgroundVideo />

      {/* 🧭 Application Routing */}
      <Router>
        <Navbar />

        {/* Main Page Content */}
        <div className="page-content">
          <Routes>
            {/* 🏠 Home Page */}
            <Route path="/" element={<Home />} />

            {/* 💬 AI Chatbot */}
            <Route path="/chatbot" element={<Chatbot />} />

            {/* 🧍 Body Type Recommender */}
            <Route path="/bodytype" element={<BodyType />} />

            {/* 👗 Virtual Try-On Page */}
            <Route path="/tryon" element={<VirtualTryOn />} />

            {/* ✨ Fallback — 404 Page */}
            <Route
              path="*"
              element={
                <div className="min-h-screen flex flex-col items-center justify-center text-gray-600">
                  <h1 className="text-2xl font-semibold mb-2">
                    404 — Page Not Found
                  </h1>
                  <p>Try navigating using the menu above.</p>
                </div>
              }
            />
          </Routes>
        </div>
      </Router>
    </>
  );
};

export default App;
