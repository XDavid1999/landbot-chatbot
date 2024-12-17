import axios from 'axios';

// Create an Axios instance
const axiosInstance = axios.create({
  baseURL: '/api', // Adjust the baseURL according to your backend API path
  headers: {
    'Content-Type': 'application/json',
  },
  // You can set other default configurations here
});

export default axiosInstance;
