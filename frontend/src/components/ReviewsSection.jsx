import React, { useState } from "react";
import { reviews } from "../mock/data";
import { Star, ChevronLeft, ChevronRight } from "lucide-react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";

const ReviewsSection = () => {
  const [currentReview, setCurrentReview] = useState(0);

  const nextReview = () => {
    setCurrentReview((prev) => (prev + 1) % reviews.length);
  };

  const prevReview = () => {
    setCurrentReview((prev) => (prev - 1 + reviews.length) % reviews.length);
  };

  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        {/* Google Reviews Header */}
        <div className="text-center mb-16">
          <div className="bg-white rounded-2xl p-8 shadow-lg max-w-md mx-auto">
            <div className="flex items-center justify-center mb-4">
              <img 
                src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" 
                alt="Google" 
                className="w-8 h-8 mr-2"
              />
              <span className="text-lg font-semibold">Google Reviews</span>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-gray-900 mb-2">4.9</div>
              <div className="flex justify-center mb-2">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-6 h-6 text-yellow-400 fill-current" />
                ))}
              </div>
              <div className="text-gray-600">Based on 238+ reviews</div>
            </div>
          </div>
        </div>

        {/* Reviews Carousel */}
        <div className="relative max-w-4xl mx-auto">
          <Card className="border-0 shadow-xl bg-white">
            <CardContent className="p-8">
              <div className="text-center mb-6">
                <div className="flex justify-center mb-4">
                  {[...Array(reviews[currentReview].rating)].map((_, i) => (
                    <Star key={i} className="w-6 h-6 text-yellow-400 fill-current" />
                  ))}
                </div>
                <Badge variant="outline" className="text-green-700 border-green-200">
                  {reviews[currentReview].service}
                </Badge>
              </div>
              
              <blockquote className="text-lg text-gray-700 leading-relaxed mb-6 italic text-center">
                "{reviews[currentReview].text}"
              </blockquote>
              
              <div className="text-center">
                <div className="font-semibold text-gray-900">
                  {reviews[currentReview].name}
                </div>
                <div className="text-sm text-gray-500">
                  {reviews[currentReview].date}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Navigation Buttons */}
          <Button
            variant="outline"
            size="icon"
            className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white border-green-200 hover:bg-green-50"
            onClick={prevReview}
          >
            <ChevronLeft className="w-5 h-5" />
          </Button>
          
          <Button
            variant="outline"
            size="icon"
            className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white border-green-200 hover:bg-green-50"
            onClick={nextReview}
          >
            <ChevronRight className="w-5 h-5" />
          </Button>
        </div>

        {/* Review Dots */}
        <div className="flex justify-center mt-8 space-x-2">
          {reviews.map((_, index) => (
            <button
              key={index}
              className={`w-3 h-3 rounded-full transition-colors ${
                index === currentReview ? 'bg-green-700' : 'bg-gray-300'
              }`}
              onClick={() => setCurrentReview(index)}
            />
          ))}
        </div>

        {/* Bottom Text */}
        <div className="text-center mt-12">
          <p className="text-gray-600 mb-4">
            THE Balham Gardeners FOR professional gardening services
          </p>
          <p className="text-gray-600 max-w-3xl mx-auto">
            We offer a comprehensive range of gardening services across Balham and surrounding London areas, 
            tailored to meet the diverse needs of our clients. Whether you need regular garden maintenance 
            or a one-off tidy-up, our skilled gardeners are committed to delivering exceptional results every time.
          </p>
        </div>
      </div>
    </section>
  );
};

export default ReviewsSection;