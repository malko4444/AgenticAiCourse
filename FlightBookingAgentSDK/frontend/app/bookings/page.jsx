'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const Page = () => {
    const router = useRouter();
    const [flights, setFlights] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (!token) {
            router.push('/login');
        } else {
            axios.get('http://127.0.0.1:8000/user_flights', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then((res) => {
                    setFlights(res.data?.data?.user_flights || []);
                })
                .catch((err) => {
                    console.error("Error fetching flights:", err);
                })
                .finally(() => {
                    setLoading(false);
                });
        }
    }, []);

    return (
        <div><Navbar />
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 px-6 py-10">

                <h1 className="text-3xl font-bold text-center text-blue-800 mb-8">🛫 Your Booked Flights</h1>

                {loading ? (
                    <p className="text-center text-blue-600">Loading flights...</p>
                ) : flights.length === 0 ? (
                    <p className="text-center text-gray-500">No bookings found.</p>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {flights.map((flight) => (
                            <div
                                key={flight._id}
                                className="bg-white p-6 rounded-xl shadow-md border border-blue-200"
                            >
                                <h2 className="text-xl font-bold text-blue-700 mb-2">{flight.passenger_name}</h2>
                                <p className="text-gray-700"><span className="font-semibold">Passport:</span> {flight.passport_number}</p>
                                <p className="text-gray-700"><span className="font-semibold">Route:</span> {flight.location}</p>
                                <p className="text-gray-700"><span className="font-semibold">Date:</span> {flight.date}</p>
                                <p className={`mt-2 px-3 py-1 rounded-full w-fit text-sm font-medium ${flight.status === 'cancelled'
                                        ? 'bg-red-100 text-red-600'
                                        : 'bg-green-100 text-green-700'
                                    }`}>
                                    {flight.status.toUpperCase()}
                                </p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
            <Footer/>
        </div>
    );
};

export default Page;
