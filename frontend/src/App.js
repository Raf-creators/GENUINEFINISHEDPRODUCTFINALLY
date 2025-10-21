import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import AdminDashboard from "./components/AdminDashboard";
import ServicePhotoAlbums from "./components/ServicePhotoAlbums";
import ServiceGallery from "./components/ServiceGallery";
import BuildServices from "./components/BuildServices";
import MaintainServices from "./components/MaintainServices";
import "./App.css";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/gallery" element={<ServicePhotoAlbums />} />
          <Route path="/gallery/:serviceId" element={<ServiceGallery />} />
          <Route path="/build" element={<BuildServices />} />
          <Route path="/maintain" element={<MaintainServices />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;