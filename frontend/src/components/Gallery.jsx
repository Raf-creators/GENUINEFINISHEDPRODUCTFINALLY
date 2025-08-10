import React, { useState } from "react";
import { galleryImages } from "../mock/data";
import { X } from "lucide-react";
import { Button } from "./ui/button";

const Gallery = () => {
  const [selectedImage, setSelectedImage] = useState(null);

  const openLightbox = (image) => {
    setSelectedImage(image);
  };

  const closeLightbox = () => {
    setSelectedImage(null);
  };

  return (
    <section id="gallery" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Our Recent Garden Transformations
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Take a look at some of our recent gardening projects in Balham and surrounding areas. 
            We take pride in transforming gardens and creating beautiful outdoor spaces.
          </p>
        </div>

        {/* Gallery Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {galleryImages.map((image) => (
            <div
              key={image.id}
              className="group relative aspect-square rounded-2xl overflow-hidden cursor-pointer shadow-lg hover:shadow-xl transition-all duration-300"
              onClick={() => openLightbox(image)}
            >
              <img
                src={image.src}
                alt={image.title}
                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="absolute bottom-0 left-0 right-0 p-4 text-white transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                <div className="font-semibold">{image.title}</div>
                <div className="text-sm opacity-90">{image.category}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom Text */}
        <div className="text-center bg-green-50 rounded-2xl p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Ready to Transform Your Garden?
          </h3>
          <p className="text-gray-600 mb-6">
            Let PNM Gardeners transform and maintain your garden to the highest standards. 
            Contact us today for reliable, high-quality gardening services in Balham.
          </p>
          <Button className="bg-green-700 hover:bg-green-800 text-white px-8 py-3">
            View All Our Work
          </Button>
        </div>
      </div>

      {/* Lightbox Modal */}
      {selectedImage && (
        <div className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4">
          <div className="relative max-w-4xl max-h-full">
            <img
              src={selectedImage.src}
              alt={selectedImage.title}
              className="max-w-full max-h-full object-contain rounded-lg"
            />
            <Button
              variant="ghost"
              size="icon"
              className="absolute top-4 right-4 text-white hover:bg-white/20"
              onClick={closeLightbox}
            >
              <X className="w-6 h-6" />
            </Button>
            <div className="absolute bottom-4 left-4 text-white">
              <div className="text-xl font-semibold">{selectedImage.title}</div>
              <div className="text-white/80">{selectedImage.category}</div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default Gallery;