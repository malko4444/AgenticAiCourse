'use client';

import React, { useState } from 'react';
import ConfirmEmail from '../components/ConfrimEmail';
import { registerUser } from '../utils/helperFunction';
import { Poppins } from 'next/font/google';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '600', '800'],
});

const page = () => {
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    if (!email || !otp || !firstName || !lastName || !password || !phoneNumber) {
      setMessage('⚠️ Please fill all the fields.');
      return;
    }

    const user = {
      email,
      otp,
      firstName,
      lastName,
      password,
      phoneNumber,
    };

    setLoading(true);
    setMessage('');
    try {
      const res = await registerUser(user);
      setMessage(`✅ ${res.message || 'User registered successfully'}`);
    } catch (err) {
      const errorMsg = err?.response?.data?.detail || err.message || 'Registration failed';
      setMessage(`❌ ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Navbar />
    <section className={`min-h-screen bg-gradient-to-br from-sky-50 to-blue-100 py-5 px-1 ${poppins.className}`}>
      
      <div className="max-w-xl mx-auto flex flex-col gap-8 items-center">

        {/* Smaller Confirm Email */}
        
        <div className="w-full max-w-sm scale-80">
          <ConfirmEmail />
        </div>

        {/* Signup Form */}
        <div className="w-full bg-white shadow-2xl rounded-2xl p-8">
          <h2 className="text-2xl font-bold text-blue-800 text-center mb-6">Create Your Account</h2>

          <div className="space-y-4">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border border-blue-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              className="w-full px-4 py-2 border border-blue-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="First Name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="w-full px-4 py-2 border border-blue-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="Last Name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="w-full px-4 py-2 border border-blue-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border border-blue-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="Phone Number"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              className="w-full px-4 py-2 border border-blue-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            <button
              onClick={handleRegister}
              disabled={loading}
              className={`w-full py-3 text-white rounded-xl font-semibold transition ${
                loading ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {loading ? 'Registering...' : 'Register'}
            </button>

            {message && (
              <div
                className={`text-center text-sm font-medium mt-2 ${
                  message.startsWith('✅') ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {message}
              </div>
            )}
          </div>
        </div>
        
      </div>
    </section>
    <Footer/>
    </div>
  );
};

export default page;
