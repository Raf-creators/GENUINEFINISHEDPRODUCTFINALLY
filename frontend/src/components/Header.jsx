import React, { useState, useEffect } from 'react';
import { Phone, Mail, MapPin, Menu, X } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setIsMenuOpen(false);
    }
  };

  return (
    <header className={`fixed w-full top-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-white shadow-lg' : 'bg-white/95 backdrop-blur-sm'}`}>
      {/* Top Bar */}
      <div className="bg-green-800 text-white py-2">
        <div className="container mx-auto px-4 flex flex-wrap justify-between items-center text-sm">
          <div className="flex items-center gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <Phone className="w-4 h-4" />
              <span>07340 833142</span>
            </div>
            <div className="flex items-center gap-2">
              <Mail className="w-4 h-4" />
              <span>contact@pnmgardening.com</span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4" />
            <span>Serving South West London & Surrounding Areas</span>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="container mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            <img
              src="https://customer-assets.emergentagent.com/job_green-thumbs-balham/artifacts/qsdqvwf5_IMG_7243.jpeg" 
              alt="PNM Gardeners Logo" 
              className="h-12 w-12 rounded-full object-cover"
            />
            <div>
              <h1 className="text-xl font-bold text-green-800">PNM GARDENING</h1>
              <p className="text-xs text-gray-600">Professional Garden Services</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-6">
            <Link to="/" className="text-gray-700 hover:text-green-700 font-medium transition-colors">
              Home
            </Link>
            <button onClick={() => scrollToSection('services')} className="text-gray-700 hover:text-green-700 font-medium transition-colors">
              Services
            </button>
            <Link to="/gallery" className="text-gray-700 hover:text-green-700 font-medium transition-colors">
              Gallery
            </Link>
            <button onClick={() => scrollToSection('reviews')} className="text-gray-700 hover:text-green-700 font-medium transition-colors">
              Reviews
            </button>
            <button onClick={() => scrollToSection('contact')} className="text-gray-700 hover:text-green-700 font-medium transition-colors">
              Contact
            </button>
            <Button
              onClick={() => scrollToSection('contact')}
              className="bg-green-700 hover:bg-green-800 text-white"
            >
              Get a Quote
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="lg:hidden p-2 text-gray-700 hover:text-green-700"
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="lg:hidden absolute top-full left-0 w-full bg-white shadow-lg border-t">
            <div className="container mx-auto px-4 py-4 flex flex-col gap-3">
              <Link
                to="/"
                onClick={() => setIsMenuOpen(false)}
                className="text-gray-700 hover:text-green-700 font-medium py-2 transition-colors"
              >
                Home
              </Link>
              <button
                onClick={() => {
                  scrollToSection('services');
                  setIsMenuOpen(false);
                }}
                className="text-gray-700 hover:text-green-700 font-medium py-2 transition-colors text-left"
              >
                Services
              </button>
              <Link
                to="/gallery"
                onClick={() => setIsMenuOpen(false)}
                className="text-gray-700 hover:text-green-700 font-medium py-2 transition-colors"
              >
                Gallery
              </Link>
              <button
                onClick={() => {
                  scrollToSection('reviews');
                  setIsMenuOpen(false);
                }}
                className="text-gray-700 hover:text-green-700 font-medium py-2 transition-colors text-left"
              >
                Reviews
              </button>
              <button
                onClick={() => {
                  scrollToSection('contact');
                  setIsMenuOpen(false);
                }}
                className="text-gray-700 hover:text-green-700 font-medium py-2 transition-colors text-left"
              >
                Contact
              </button>
              <div className="pt-3 border-t flex flex-col gap-2">
                <div className="flex items-center gap-2 text-sm">
                  <Phone className="w-4 h-4" />
                  <span>07340 833142</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Mail className="w-4 h-4" />
                  <span>contact@pnmgardening.com</span>
                </div>
              </div>
              <Button
                onClick={() => {
                  scrollToSection('contact');
                  setIsMenuOpen(false);
                }}
                className="bg-green-700 hover:bg-green-800 text-white w-full"
              >
                Get a Quote
              </Button>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;