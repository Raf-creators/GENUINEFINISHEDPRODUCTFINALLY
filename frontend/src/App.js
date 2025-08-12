import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import AdminDashboard from "./components/AdminDashboard";
import ServicePhotoAlbums from "./components/ServicePhotoAlbums";
import "./App.css";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/gallery" element={<ServicePhotoAlbums />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;