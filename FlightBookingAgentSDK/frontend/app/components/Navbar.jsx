import Link from "next/link";
import Head from "next/head";

const Navbar = () => {
  return (
    <>
      <Head>
        {/* Google Font Embed */}
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
            <Link href="/flights">Booked Flights</Link>
          </li>
          <li className="hover:text-blue-900 hover:scale-105 transition duration-300 ease-in-out hover:underline underline-offset-4">
            <Link href="/profile">Profile</Link>
          </li>
        </ul>

        {/* CTA Button */}
        <div>
          <Link href="/agent">
            <button className="bg-blue-600 text-white px-5 py-2 rounded-full font-semibold shadow-md hover:bg-blue-700 transition duration-300">
              Talk to Agent
            </button>
          </Link>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
