import axios from 'axios';

export const sendOtpToEmail = async (email) => {
  console.log(`Sending OTP to email: ${email}`);

  try {
    const response = await axios.post('http://127.0.0.1:8000/auth/otp', {
      email: email,
    });

    console.log('Response:', response.data);
    return response.data.message || "OTP sent to your email";
  } catch (error) {
    console.error('Error sending OTP:', error.message);
    throw new Error("Failed to send OTP. Please try again later.");
  }
};

export const registerUser = async (user) => {
  const data = JSON.stringify({
    email: user.email,
    otp: user.otp,
    password: user.password,
    first_name: user.firstName,
    last_name: user.lastName,
    phone_number: user.phoneNumber,
  });

  const config = {
    method: 'post',
    maxBodyLength: Infinity,
    url: 'http://127.0.0.1:8000/auth/register',
    headers: {
      'Content-Type': 'application/json',
    },
    data: data,
  };

  try {
    const response = await axios.request(config);
    console.log('✅ Backend Response:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Register Error:', error?.response?.data || error.message);
    throw error;
  }
};
