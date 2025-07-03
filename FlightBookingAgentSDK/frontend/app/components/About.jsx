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
      className={`w-full px-6 py-20 bg-gradient-to-br from-sky-50 to-blue-100 rounded-3xl shadow-2xl mx-4 mt-8 ${poppins.className}`}
    >
      <div className="max-w-6xl mx-auto text-center">
        <h2 className="text-4xl md:text-5xl font-extrabold text-blue-800 mb-6">
          About <span className="text-sky-600">SkyJet Booking Agent</span>
        </h2>
        <p className="text-lg text-gray-700 mb-14 leading-relaxed max-w-3xl mx-auto">
          SkyJet is an AI-powered flight assistant built with FastAPI and integrated into a friendly chatbot interface. Whether you're booking a flight, making changes, or just asking travel questions, our assistant helps you do it all in seconds.
        </p>

        {/* Feature Boxes */}
        <div className="flex flex-col md:flex-row md:flex-wrap justify-center gap-8">
          {/* Feature Item */}
          <div className="bg-white p-6 md:w-[45%] w-full rounded-2xl shadow-lg hover:shadow-xl transition duration-300">
            <h3 className="text-blue-700 text-xl font-semibold mb-3">✈️ Book Flights Instantly</h3>
            <p className="text-gray-600 leading-relaxed">
              Our intelligent assistant helps you search, compare, and book flights with a simple conversation.
            </p>
          </div>

          <div className="bg-white p-6 md:w-[45%] w-full rounded-2xl shadow-lg hover:shadow-xl transition duration-300">
            <h3 className="text-blue-700 text-xl font-semibold mb-3">🧾 Modify or Cancel</h3>
            <p className="text-gray-600 leading-relaxed">
              Need to cancel or change your flight? Just ask the bot, and it will handle the rest through our FastAPI backend.
            </p>
          </div>

          <div className="bg-white p-6 md:w-[45%] w-full rounded-2xl shadow-lg hover:shadow-xl transition duration-300">
            <h3 className="text-blue-700 text-xl font-semibold mb-3">🎒 Travel Info On Demand</h3>
            <p className="text-gray-600 leading-relaxed">
              Ask about baggage limits, visa policies, or airline rules—your agent knows it all and answers instantly.
            </p>
          </div>

          <div className="bg-white p-6 md:w-[45%] w-full rounded-2xl shadow-lg hover:shadow-xl transition duration-300">
            <h3 className="text-blue-700 text-xl font-semibold mb-3">⚙️ FastAPI Powered</h3>
            <p className="text-gray-600 leading-relaxed">
              All flight actions are handled through a scalable and secure FastAPI backend that processes requests reliably.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default About;
