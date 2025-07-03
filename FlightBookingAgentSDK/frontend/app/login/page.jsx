'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { Poppins } from 'next/font/google';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import Link from 'next/link';
const poppins = Poppins({
    subsets: ['latin'],
    weight: ['400', '600', '800'],
});

const page = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [token, setToken] = useState('');
    const router = useRouter();

    const handleLogin = async () => {
        if (!email || !password) {
            setMessage('⚠️ Please enter email and password.');
            return;
        }

        setLoading(true);
        setMessage('');

        try {
            const response = await axios.post('http://127.0.0.1:8000/auth/login', {
                email,
                password,
            });

            const data = response.data;
            setMessage(`✅ ${data.message}`);
            setToken(data.data.access_token);
            console.log('Access Token:', data.data.access_token);
            localStorage.setItem('access_token', data.data.access_token);
            localStorage.setItem('userDetails', data.data);
            // navigate to the home page or dashboard
            
            router.push('/');

        } catch (err) {
            const errorMsg =
                err?.response?.data?.detail || err.message || 'Login failed.';
            setMessage(`❌ ${errorMsg}`);
        } finally {
            setLoading(false);
        }
    };

    return (
  <div>
    <Navbar />
    <section
      className={`min-h-screen flex items-center justify-center bg-gradient-to-br from-sky-50 to-blue-100 px-6 py-16 ${poppins.className}`}
    >
      <div className="bg-white p-10 rounded-2xl shadow-2xl w-full max-w-md text-center">
        <h2 className="text-3xl font-extrabold text-blue-800 mb-6">
          ✈️ Login to SkyJet
        </h2>

        <div className="space-y-5">
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 border border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-700"
          />

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 border border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-700"
          />

          <button
            onClick={handleLogin}
            disabled={loading}
            className={`w-full py-3 rounded-xl text-white font-semibold transition ${
              loading
                ? 'bg-blue-300 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>

          {message && (
            <div
              className={`text-center font-medium text-sm mt-2 ${
                message.startsWith('✅')
                  ? 'text-green-600'
                  : 'text-red-600'
              }`}
            >
              {message}
            </div>
          )}
        </div>

        {/* Register link */}
        <p className="mt-6 text-sm text-gray-600">
          Don't have an account?{" "}
          <Link
            href="/signup"
            className="text-blue-600 font-semibold hover:underline"
          >
            Register here
          </Link>
        </p>
      </div>
    </section>
    <Footer />
  </div>
);
};

export default page;
