import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: `${window.location.protocol}//${window.location.hostname}:${import.meta.env.VITE_BACKEND_PORT}/api/`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
