import React, { useState } from "react";
import { services } from "../mock/data";
import { Phone, Mail, MapPin, Send } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { useToast } from "../hooks/use-toast";

const ContactSection = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    service: "",
    message: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleServiceChange = (value) => {
    setFormData((prev) => ({
      ...prev,
      service: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Mock form submission
    toast({
      title: "Quote Request Sent!",
      description: "Thank you for your inquiry. We'll get back to you within 24 hours with your free quote.",
    });
    // Reset form
    setFormData({
      name: "",
      email: "",
      phone: "",
      service: "",
      message: "",
    });
  };

  return (
    <section id="contact" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Get Your Free Quote Today
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Ready to transform your garden? Fill in the form below or call us directly for a 
            fast, free, and competitive quote for all your gardening needs in Balham.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-12">
          {/* Contact Form */}
          <div className="lg:col-span-2">
            <Card className="border-0 shadow-xl bg-white">
              <CardHeader className="text-center pb-8">
                <CardTitle className="text-2xl font-bold text-gray-900">
                  Request Your Free Quote
                </CardTitle>
                <p className="text-gray-600">
                  Fill out the form below and we'll get back to you with a competitive quote
                </p>
              </CardHeader>
              <CardContent className="px-8 pb-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Full Name *
                      </label>
                      <Input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        placeholder="Enter your full name"
                        required
                        className="border-gray-300 focus:border-green-700"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Email Address *
                      </label>
                      <Input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        placeholder="Enter your email"
                        required
                        className="border-gray-300 focus:border-green-700"
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Phone Number *
                      </label>
                      <Input
                        type="tel"
                        name="phone"
                        value={formData.phone}
                        onChange={handleInputChange}
                        placeholder="Enter your phone number"
                        required
                        className="border-gray-300 focus:border-green-700"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Service Required *
                      </label>
                      <Select onValueChange={handleServiceChange} required>
                        <SelectTrigger className="border-gray-300 focus:border-green-700">
                          <SelectValue placeholder="Choose a service" />
                        </SelectTrigger>
                        <SelectContent>
                          {services.map((service) => (
                            <SelectItem key={service.id} value={service.title}>
                              {service.title}
                            </SelectItem>
                          ))}
                          <SelectItem value="Other">Other</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Message / Project Details
                    </label>
                    <Textarea
                      name="message"
                      value={formData.message}
                      onChange={handleInputChange}
                      placeholder="Tell us about your garden project, preferred dates, or any specific requirements..."
                      rows={5}
                      className="border-gray-300 focus:border-green-700"
                    />
                  </div>

                  <Button
                    type="submit"
                    className="w-full bg-green-700 hover:bg-green-800 text-white py-4 text-lg"
                  >
                    <Send className="w-5 h-5 mr-2" />
                    Send Quote Request
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Contact Info */}
          <div className="space-y-8">
            {/* Contact Details */}
            <Card className="border-0 shadow-xl bg-green-700 text-white">
              <CardContent className="p-8">
                <h3 className="text-2xl font-bold mb-6">Contact Information</h3>
                
                <div className="space-y-6">
                  <div className="flex items-start space-x-4">
                    <Phone className="w-6 h-6 mt-1 flex-shrink-0" />
                    <div>
                      <div className="font-semibold mb-1">Phone & WhatsApp</div>
                      <div className="text-green-100">020 3488 1912</div>
                      <div className="text-sm text-green-100 mt-1">
                        Available 7 days a week, 8am - 6pm
                      </div>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <Mail className="w-6 h-6 mt-1 flex-shrink-0" />
                    <div>
                      <div className="font-semibold mb-1">Email</div>
                      <div className="text-green-100">info@pnmgardeners.co.uk</div>
                      <div className="text-sm text-green-100 mt-1">
                        Send photos for accurate quotes
                      </div>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <MapPin className="w-6 h-6 mt-1 flex-shrink-0" />
                    <div>
                      <div className="font-semibold mb-1">Service Area</div>
                      <div className="text-green-100">Balham, London</div>
                      <div className="text-sm text-green-100 mt-1">
                        & surrounding South London areas
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-8 pt-8 border-t border-green-600">
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold">FREE</div>
                      <div className="text-sm text-green-100">Quotes & Advice</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold">24HR</div>
                      <div className="text-sm text-green-100">Response Time</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Stats */}
            <Card className="border-0 shadow-xl bg-white">
              <CardContent className="p-8">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Why Choose PNM Gardeners?</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-700 rounded-full"></div>
                    <span className="text-gray-700">5+ years serving Balham</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-700 rounded-full"></div>
                    <span className="text-gray-700">1000+ satisfied customers</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-700 rounded-full"></div>
                    <span className="text-gray-700">4.9/5 star Google rating</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-700 rounded-full"></div>
                    <span className="text-gray-700">Fully licensed & insured</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-700 rounded-full"></div>
                    <span className="text-gray-700">Free waste disposal included</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;