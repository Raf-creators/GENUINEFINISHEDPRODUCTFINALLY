import React from 'react';
import { Phone, Mail, MapPin, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <img
                src="https://customer-assets.emergentagent.com/job_green-thumbs-balham/artifacts/qsdqvwf5_IMG_7243.jpeg" 
                alt="PNM Gardeners Logo" 
                className="h-12 w-12 rounded-full object-cover"
              />
              <div>
                <h3 className="text-xl font-bold text-white">PNM GARDENING</h3>
              </div>
            </div>
            <p className="text-sm leading-relaxed">
              Your trusted local gardening experts serving South West London & Surrounding Areas
            </p>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-white font-semibold mb-4">Contact Us</h4>
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-3">
                <Phone className="w-5 h-5 text-green-400" />
                <span>07340 833142</span>
              </div>
              <div className="flex items-start gap-3">
                <Mail className="w-5 h-5 text-green-400" />
                <span>contact@pnmgardening.com</span>
              </div>
              <div className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-green-400" />
                <span>South West London</span>
              </div>
              <div className="flex items-start gap-3">
                <Clock className="w-5 h-5 text-green-400" />
                <div>
                  <div>Mon - Sat: 7:00 AM - 7:00 PM</div>
                  <div>Sun: 8:00 AM - 4:00 PM</div>
                </div>
              </div>
            </div>
          </div>

          {/* Service Areas */}
          <div>
            <h4 className="text-white font-semibold mb-4">Service Areas</h4>
            <ul className="space-y-2 text-sm">
              <li>South West London</li>
              <li>Tooting</li>
              <li>Wandsworth</li>
              <li>Clapham</li>
              <li>Streatham</li>
              <li>Brixton</li>
              <li>Wimbledon</li>
              <li>Battersea</li>
              <li>Stockwell</li>
              <li>& Surrounding Areas</li>
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="hover:text-green-400 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <a href="#services" className="hover:text-green-400 transition-colors">
                  Our Services
                </a>
              </li>
              <li>
                <Link to="/gallery" className="hover:text-green-400 transition-colors">
                  Gallery
                </Link>
              </li>
              <li>
                <a href="#reviews" className="hover:text-green-400 transition-colors">
                  Reviews
                </a>
              </li>
              <li>
                <a href="#contact" className="hover:text-green-400 transition-colors">
                  Contact
                </a>
              </li>
              <li>
                <a href="#faq" className="hover:text-green-400 transition-colors">
                  FAQ
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 text-sm text-center">
          <p className="mb-2">
            &copy; {new Date().getFullYear()} PNM GARDENING. All rights reserved.
          </p>
          <p className="text-gray-500">
            Professional gardening services in South West London. Specializing in garden maintenance, 
            landscaping, and garden design.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;