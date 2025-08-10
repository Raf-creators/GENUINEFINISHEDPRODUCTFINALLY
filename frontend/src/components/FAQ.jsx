import React from "react";
import { faqs } from "../mock/data";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "./ui/accordion";

const FAQ = () => {
  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Frequently Asked Questions
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Got questions about our gardening services? Here are the most common questions 
            our customers ask about our services in Balham and surrounding areas.
          </p>
        </div>

        {/* FAQ Accordion */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            <Accordion type="single" collapsible className="w-full">
              {faqs.map((faq) => (
                <AccordionItem key={faq.id} value={`item-${faq.id}`} className="border-gray-200">
                  <AccordionTrigger className="px-8 py-6 text-left hover:no-underline hover:bg-green-50 transition-colors">
                    <span className="text-lg font-semibold text-gray-900">
                      {faq.question}
                    </span>
                  </AccordionTrigger>
                  <AccordionContent className="px-8 pb-6 text-gray-600 leading-relaxed">
                    {faq.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>

          {/* Additional Help */}
          <div className="text-center mt-12">
            <div className="bg-green-50 rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Still Have Questions?
              </h3>
              <p className="text-gray-600 mb-6">
                If you have any other questions about our gardening services, 
                please don't hesitate to contact us. We're here to help!
              </p>
              <div className="space-y-2 text-lg">
                <div className="font-semibold text-green-700">
                  Call us: 020 3488 1912
                </div>
                <div className="font-semibold text-green-700">
                  Email: info@pnmgardeners.co.uk
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FAQ;