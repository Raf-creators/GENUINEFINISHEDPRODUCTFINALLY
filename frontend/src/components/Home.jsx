import React, { useState } from "react";
import Header from "./Header";
import HeroSection from "./HeroSection";
import DesignBuildMaintain from "./DesignBuildMaintain";
import CategoryServices from "./CategoryServices";
import ReviewsSection from "./ReviewsSection";
import ReviewsMap from "./ReviewsMap";
import WhyChooseUs from "./WhyChooseUs";
import AreasServed from "./AreasServed";
import FAQ from "./FAQ";
import ContactSection from "./ContactSection";
import Footer from "./Footer";

const Home = () => {
  const [selectedCategory, setSelectedCategory] = useState(null);

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <HeroSection />
      <DesignBuildMaintain onCategorySelect={handleCategorySelect} />
      {selectedCategory && <CategoryServices selectedCategory={selectedCategory} />}
      <ReviewsSection />
      <ReviewsMap />
      <WhyChooseUs />
      <AreasServed />
      <FAQ />
      <ContactSection />
      <Footer />
    </div>
  );
};

export default Home;