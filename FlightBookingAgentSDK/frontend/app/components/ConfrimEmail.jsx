'use client';

import React, { useState } from 'react';
import { sendOtpToEmail } from '../utils/helperFunction';
import { Poppins } from 'next/font/google';

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '600', '800'],
});

function ConfirmEmail() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);
  const [loading, setLoading] = useState(false);

  const isValidEmail = (email) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isValidEmail(email)) {
      setMessage('Please enter a valid email address.');
      setIsError(true);
      return;
    }

    setLoading(true);
    setMessage('');
    setIsError(false);

    try {
      const response = await sendOtpToEmail(email);
      setMessage(response || 'OTP sent to your email.');
      setIsError(false);
    } catch (err) {
      setMessage('❌ Failed to send OTP. Please try again.');
      setIsError(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`bg-white shadow-xl rounded-2xl p-8 w-full max-w-md ${poppins.className}`}>
      <div className="text-center mb-4">
        <div className="text-4xl mb-1">📮</div>
        <h1 className="text-2xl font-extrabold text-blue-800">Email Verification</h1>
        <p className="text-gray-600 text-sm mt-1">
          We'll send you a One-Time Password (OTP) to verify your email.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className={`px-4 py-2 rounded-xl border ${
            isError ? 'border-red-400' : 'border-blue-300'
          } focus:outline-none focus:ring-2 ${
            isError ? 'focus:ring-red-400' : 'focus:ring-blue-400'
          } text-gray-700 text-sm`}
        />

        <button
          type="submit"
          disabled={loading}
          className={`py-2 rounded-xl text-white font-semibold transition duration-300 ${
            loading
              ? 'bg-blue-300 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {loading ? 'Sending OTP...' : 'Send OTP'}
        </button>
      </form>

      {message && (
        <div
          className={`mt-4 text-center text-sm font-medium ${
            isError ? 'text-red-600' : 'text-green-600'
          }`}
        >
          {message}
        </div>
      )}
    </div>
  );
}

export default ConfirmEmail;
