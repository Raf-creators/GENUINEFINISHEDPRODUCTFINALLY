import React from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "./ui/card";

const DesignBuildMaintain = () => {
  const navigate = useNavigate();

  const sections = [
    {
      id: "design",
      title: "DESIGN",
      image: "https://images.unsplash.com/photo-1523726491678-bf852e717f6a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw1fHxnYXJkZW4lMjBkZXNpZ24lMjBwbGFufGVufDB8fHx8MTc2MTEwNzAwNXww&ixlib=rb-4.1.0&q=85",
      description: "Using our designers to create innovative ideas and visualize your dream garden",
      clickable: false,
    },
    {
      id: "build",
      title: "BUILD",
      image: "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw3fHxnYXJkZW4lMjBjb25zdHJ1Y3Rpb258ZW58MHx8fHwxNzYxMTA3MDA1fDA&ixlib=rb-4.1.0&q=85",
      description: "Bringing bespoke designs to life with precision and quality craftsmanship",
      clickable: true,
      route: "/build",
    },
    {
      id: "maintain",
      title: "MAINTAIN",
      image: "https://images.unsplash.com/photo-1592419044706-39796d40f98c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYXJkZW5lciUyMHRyaW1taW5nJTIwaGVkZ2V8ZW58MHx8fHwxNzYxMTA3MDA1fDA&ixlib=rb-4.1.0&q=85",
      description: "Ongoing expert gardening to keep your outdoor space perfect year-round",
      clickable: true,
      route: "/maintain",
    },
  ];

  const handleCardClick = (section) => {
    if (section.clickable) {
      navigate(section.route);
    }
  };

  return (
    <section className="py-20 bg-gradient-to-b from-gray-50 to-white">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-4">
            Our Complete Garden Service
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            From concept to completion and ongoing care — we handle every aspect of your garden
          </p>
        </div>

        {/* Three Column Grid */}
        <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {sections.map((section) => (
            <Card
              key={section.id}
              onClick={() => handleCardClick(section)}
              className={`group relative overflow-hidden border-0 shadow-xl ${
                section.clickable
                  ? "cursor-pointer hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
                  : ""
              }`}
            >
              {/* Image Container */}
              <div className="relative h-80 overflow-hidden">
                <img
                  src={section.image}
                  alt={section.title}
                  className={`w-full h-full object-cover ${
                    section.clickable ? "group-hover:scale-110 transition-transform duration-500" : ""
                  }`}
                />
                {/* Dark Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
                
                {/* Content Overlay */}
                <div className="absolute inset-0 flex flex-col justify-end p-6 text-white">
                  <h3 className="text-3xl font-bold mb-3 tracking-wider">
                    {section.title}
                  </h3>
                  <p className="text-base leading-relaxed opacity-90">
                    {section.description}
                  </p>
                  
                  {/* Clickable Indicator */}
                  {section.clickable && (
                    <div className="mt-4 flex items-center text-sm font-semibold group-hover:translate-x-2 transition-transform duration-300">
                      <span>Explore Services</span>
                      <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default DesignBuildMaintain;
