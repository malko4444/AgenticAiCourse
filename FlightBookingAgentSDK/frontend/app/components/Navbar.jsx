'use client';

import Link from "next/link";
import Head from "next/head";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const Navbar = () => {
  const router = useRouter();
  const [accessToken, setAccessToken] = useState(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem("access_token");
      setAccessToken(token);
    }
  }, []);

  const logOut = () => {
    localStorage.removeItem("access_token");
    setAccessToken(null);
    router.push("/");
  };

  return (
    <>
      <Head>
        <link
          href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap"
          rel="stylesheet"
        />
      </Head>

      <nav
        className="m-4 px-8 py-4 rounded-3xl shadow-xl bg-gradient-to-r from-sky-100 via-white to-blue-100 
                   flex justify-between items-center backdrop-blur-md border border-blue-200"
        style={{ fontFamily: "'Poppins', sans-serif" }}
      >
        {/* Brand */}
        <div className="text-2xl font-extrabold text-blue-800 flex items-center gap-2">
          🛫 <span>SkyJet Bookings</span>
        </div>

        {/* Navigation Links */}
        <ul className="flex gap-10 text-blue-700 font-semibold text-[17px]">
          <li className="hover:text-blue-900 hover:scale-105 transition duration-300 ease-in-out hover:underline underline-offset-4">
            <Link href="/">Home</Link>
          </li>
          <li className="hover:text-blue-900 hover:scale-105 transition duration-300 ease-in-out hover:underline underline-offset-4">
            <Link href="/bookings">Booked Flights</Link>
          </li>
          <li className="hover:text-blue-900 hover:scale-105 transition duration-300 ease-in-out hover:underline underline-offset-4">
            <Link href="/profile">Profile</Link>
          </li>
        </ul>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <Link href="/agent">
            <button className="bg-blue-600 text-white px-5 py-2 rounded-full font-semibold shadow-md hover:bg-blue-700 transition duration-300">
              Talk to Agent
            </button>
          </Link>

          {!accessToken ? (
            <>
              
              <Link href="/login">
                <button className="bg-white text-blue-600 px-4 py-2 border border-blue-500 rounded-full font-semibold shadow-md hover:bg-blue-100 transition duration-300">
                  Login
                </button>
              </Link>
            </>
          ) : (
            <button
              onClick={logOut}
              className="bg-red-500 text-white px-5 py-2 rounded-full font-semibold shadow-md hover:bg-red-600 transition duration-300"
            >
              Logout
            </button>
          )}
        </div>
      </nav>
    </>
  );
};

export default Navbar;
