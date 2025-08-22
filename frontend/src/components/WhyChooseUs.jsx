import React from "react";
import { Shield, Award, Clock, Star, Wrench, Recycle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

const WhyChooseUs = () => {
  const benefits = [
    {
      icon: Award,
      title: "Specialised",
      description: "We specialise in gardening services in Balham and ensure all work is done to the highest standards."
    },
    {
      icon: Shield,
      title: "Licensed & Insured",
      description: "We are fully insured with comprehensive Public Liability Insurance to work on domestic and commercial properties."
    },
    {
      icon: Star,
      title: "Dependable Services",
      description: "We take pride in our work. Each garden is completed on time, within budget, and to your complete satisfaction."
    },
    {
      icon: Clock,
      title: "Flexible Scheduling",
      description: "We schedule appointments to suit you, ensuring our gardeners arrive on time as agreed, every time."
    },
    {
      icon: Wrench,
      title: "Free Quotations",
      description: "We offer fast and competitive quotes which include free disposal of green waste with all our gardening services."
    },
    {
      icon: Recycle,
      title: "Reputable Company",
      description: "We hold an outstanding reputation for our garden services, reliability and commitment to excellence in Balham."
    }
  ];

  return (
    <section id="about" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Why Book Your Gardening Services With Us?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            At PNM Gardeners, we deliver exceptional gardening services with a personal touch. 
            Our small but dedicated team of garden specialists ensures your garden receives the highest level of care.
          </p>
        </div>

        {/* Benefits Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {benefits.map((benefit, index) => {
            const IconComponent = benefit.icon;
            return (
              <Card key={index} className="group border-0 shadow-lg hover:shadow-xl transition-all duration-300 bg-white">
                <CardHeader className="text-center pb-4">
                  <div className="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center group-hover:bg-green-200 transition-colors">
                    <IconComponent className="w-8 h-8 text-green-700" />
                  </div>
                  <CardTitle className="text-xl font-bold text-gray-900 group-hover:text-green-700 transition-colors">
                    {benefit.title}
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-center pt-0">
                  <p className="text-gray-600 leading-relaxed">
                    {benefit.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Additional Info Section */}
        <div className="mt-20 bg-green-50 rounded-2xl p-8 lg:p-12">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h3 className="text-3xl font-bold text-gray-900">
                Your Local Trustworthy Balham Gardeners
              </h3>
              <p className="text-gray-600 leading-relaxed">
                At PNM Gardeners, we deliver exceptional gardening services to all types of gardens 
                in Balham and surrounding London areas. Our small but dedicated team of garden 
                specialists is professional, friendly, and reliable, ensuring that your garden 
                receives the highest level of care and attention.
              </p>
              
              <div className="space-y-4">
                <h4 className="text-xl font-semibold text-gray-900">Why Choose Us?</h4>
                <ul className="space-y-2">
                  <li className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-700 rounded-full"></div>
                    <span className="text-gray-700">Comprehensive Public Liability Insurance</span>
                  </li>
                  <li className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-700 rounded-full"></div>
                    <span className="text-gray-700">Experienced & Fully Insured</span>
                  </li>
                  <li className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-700 rounded-full"></div>
                    <span className="text-gray-700">Reliable, Professional and Trusted</span>
                  </li>
                  <li className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-700 rounded-full"></div>
                    <span className="text-gray-700">Fully Equipped with Tools and Machinery</span>
                  </li>
                </ul>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-md text-center">
                <div className="text-3xl font-bold text-green-700 mb-2">20+</div>
                <div className="text-gray-600">Years of Experience</div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md text-center">
                <div className="text-3xl font-bold text-green-700 mb-2">50+</div>
                <div className="text-gray-600">Happy Customers</div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md text-center">
                <div className="text-3xl font-bold text-green-700 mb-2">4.9</div>
                <div className="text-gray-600">Average Rating</div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md text-center">
                <div className="text-3xl font-bold text-green-700 mb-2">50+</div>
                <div className="text-gray-600">Checkatrade Reviews</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default WhyChooseUs;