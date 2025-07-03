'use client';

import React from 'react';
import { Poppins } from 'next/font/google';

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '600', '800'],
});

function About() {
  return (
    <section
      className={`w-screen px-10 py-20 bg-gradient-to-r from-sky-50 to-blue-100 ${poppins.className}`}
    >
      <div className="flex flex-col lg:flex-row items-center justify-between gap-12">
        
        {/* Text Section */}
        <div className="flex-1 max-w-2xl">
          <h2 className="text-4xl font-extrabold text-blue-800 mb-6">
            About <span className="text-sky-500">SkyJet Assistant</span>
          </h2>
          <p className="text-gray-700 text-lg leading-relaxed mb-8">
            SkyJet is your smart AI-powered assistant built with FastAPI. Whether you’re booking a flight, modifying a reservation, or just asking travel questions—our bot responds instantly with all the help you need.
          </p>

          <div className="space-y-5">
            {[
              {
                icon: '✈️',
                title: 'Book Flights Instantly',
                text: 'Search, compare, and book tickets in a smart chat experience.',
              },
              {
                icon: '🧾',
                title: 'Modify or Cancel',
                text: 'Cancel or reschedule with a few clicks—fully automated.',
              },
              {
                icon: '🎒',
                title: 'Travel Info On Demand',
                text: 'Get answers about baggage, visa policies, and travel rules.',
              },
              {
                icon: '⚙️',
                title: 'Powered by FastAPI',
                text: 'Secure and fast APIs power every backend interaction.',
              },
            ].map((item, idx) => (
              <div
                key={idx}
                className="bg-white p-4 rounded-xl shadow-md border-l-4 border-blue-400"
              >
                <h3 className="text-blue-700 font-semibold text-base mb-1">
                  {item.icon} {item.title}
                </h3>
                <p className="text-sm text-gray-600">{item.text}</p>
              </div>
            ))}
          </div>

          <p className="mt-10 text-sm text-gray-600">
            Designed & Built by{' '}
            <span className="text-blue-700 font-bold">Zubair Shehzad</span>
          </p>
        </div>

        {/* Image Section */}
        <div className="flex-1 flex justify-center">
          <img
            src="/3.jpg"
            alt="SkyJet"
            className="rounded-2xl shadow-xl w-[400px] h-[400px] object-cover"
          />
        </div>
      </div>
    </section>
  );
}

export default About;
