"use client";
import React from 'react';
import Head from 'next/head';
import Link from 'next/link';

const Hero = () => {
  return (
    <>
      <Head>
        {/* Google Font Embed */}
        <link
          href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap"
          rel="stylesheet"
        />
      </Head>

      <section
        className="w-full min-h-[90vh] flex flex-col-reverse md:flex-row items-center justify-between px-10 py-20 bg-gradient-to-br from-sky-50 to-blue-100 rounded-3xl shadow-2xl mx-4 mt-6"
        style={{ fontFamily: "'Poppins', sans-serif" }}
      >
        {/* Left text content */}
        <div className="md:w-[50%] w-full text-center md:text-left">
          <h1 className="text-4xl md:text-6xl font-extrabold text-blue-900 leading-tight mb-6">
            Fly with <span className="text-blue-600">Confidence</span> <br />
            Book with <span className="text-sky-500">Ease</span>
          </h1>
          <p className="text-gray-700 text-lg md:text-xl opacity-90 mb-8">
            Welcome to <strong>SkyJet Bookings</strong> – your trusted partner
            for smooth, fast, and reliable flight reservations around the globe.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
            <Link href="/flights">
              <button className="bg-blue-600 text-white px-6 py-3 rounded-full font-semibold shadow-md hover:bg-blue-700 transition duration-300">
                ✈️ Book a Flight
              </button>
            </Link>
            <Link href="/agent">
              <button className="bg-white text-blue-700 border border-blue-500 px-6 py-3 rounded-full font-semibold shadow-sm hover:bg-blue-50 transition duration-300">
                💬 Talk to Agent
              </button>
            </Link>
          </div>
        </div>

        {/* Right image */}
        <div className="md:w-[45%] w-full flex justify-center mb-10 md:mb-0">
          <img
            src="/1.jpg"
            alt="Flight booking illustration"
            className="w-full max-w-md md:max-w-lg rounded-3xl shadow-xl object-cover animate-float"
          />
        </div>
      </section>

      {/* Animation style */}
      <style jsx>{`
        @keyframes float {
          0% {
            transform: translateY(0px);
          }
          50% {
            transform: translateY(-10px);
          }
          100% {
            transform: translateY(0px);
          }
        }
        .animate-float {
          animation: float 5s ease-in-out infinite;
        }
      `}</style>
    </>
  );
};

export default Hero;
