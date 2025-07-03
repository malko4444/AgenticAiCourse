'use client';

import React from 'react';

function Footer() {
  return (
    <footer className="bg-gradient-to-r from-blue-100 via-white to-sky-100 px-6 py-10 mt-16 border-t border-blue-200 text-sm text-blue-800">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
        
        {/* Left: Brand */}
        <div className="text-center md:text-left">
          <h2 className="text-xl font-bold text-blue-800 mb-1">🛫 SkyJet Bookings</h2>
          <p className="text-blue-600">&copy; {new Date().getFullYear()} All rights reserved</p>
        </div>

        {/* Center: Navigation */}
        <ul className="flex flex-wrap justify-center gap-6 font-medium text-blue-700">
          <li className="hover:text-blue-900 hover:underline underline-offset-4 transition">Home</li>
          <li className="hover:text-blue-900 hover:underline underline-offset-4 transition">Booked Flights</li>
          <li className="hover:text-blue-900 hover:underline underline-offset-4 transition">Talk to Agent</li>
          <li className="hover:text-blue-900 hover:underline underline-offset-4 transition">Profile</li>
        </ul>

        {/* Right: Credit */}
        <div className="text-center md:text-right text-blue-600 font-semibold">
          Designed & Developed by <span className="text-blue-800">Zubair Shehzad</span> 💼
        </div>
      </div>
    </footer>
  );
}

export default Footer;
