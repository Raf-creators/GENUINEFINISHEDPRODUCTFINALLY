import React, { useState } from "react";
import { Phone, Mail, MapPin, Menu, X } from "lucide-react";
import { Button } from "./ui/button";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b">
      {/* Top Bar */}
      <div className="bg-green-800 text-white py-2">
        <div className="container mx-auto px-4">
          <div className="flex justify-center md:justify-between items-center text-sm">
            <div className="hidden md:flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <Phone className="w-4 h-4" />
                <span>020 3488 1912</span>
              </div>
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4" />
                <span>info@pnmgardeners.co.uk</span>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <MapPin className="w-4 h-4" />
              <span>Serving Balham, London & Surrounding Areas</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <img 
              src="https://customer-assets.emergentagent.com/job_green-thumbs-balham/artifacts/qsdqvwf5_IMG_7243.jpeg" 
              alt="PNM Gardeners Logo" 
              className="h-14 w-14 mr-3"
            />
            <div>
              <h1 className="text-3xl font-bold text-green-800">PNM Gardeners</h1>
              <div className="hidden md:block text-sm text-gray-600">
                Professional Gardening Services
              </div>
            </div>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#services" className="text-gray-700 hover:text-green-800 font-medium transition-colors">
              Services
            </a>
            <a href="#about" className="text-gray-700 hover:text-green-800 font-medium transition-colors">
              About
            </a>
            <a href="#areas" className="text-gray-700 hover:text-green-800 font-medium transition-colors">
              Areas
            </a>
            <a href="#gallery" className="text-gray-700 hover:text-green-800 font-medium transition-colors">
              Gallery
            </a>
            <a href="#contact" className="text-gray-700 hover:text-green-800 font-medium transition-colors">
              Contact
            </a>
            <Button className="bg-green-700 hover:bg-green-800 text-white px-6 py-2">
              Get Free Quote
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 pb-4">
            <div className="flex flex-col space-y-4">
              <a href="#services" className="text-gray-700 hover:text-green-800 font-medium">
                Services
              </a>
              <a href="#about" className="text-gray-700 hover:text-green-800 font-medium">
                About
              </a>
              <a href="#areas" className="text-gray-700 hover:text-green-800 font-medium">
                Areas
              </a>
              <a href="#gallery" className="text-gray-700 hover:text-green-800 font-medium">
                Gallery
              </a>
              <a href="#contact" className="text-gray-700 hover:text-green-800 font-medium">
                Contact
              </a>
              <Button className="bg-green-700 hover:bg-green-800 text-white w-full">
                Get Free Quote
              </Button>
              <div className="pt-4 border-t flex flex-col space-y-2 text-sm">
                <div className="flex items-center space-x-2 text-green-700">
                  <Phone className="w-4 h-4" />
                  <span>020 3488 1912</span>
                </div>
                <div className="flex items-center space-x-2 text-green-700">
                  <Mail className="w-4 h-4" />
                  <span>info@pnmgardeners.co.uk</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;