import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const axiosServices = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json'
    }
});

axiosServices.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        console.error('Request error:', error);
        return Promise.reject(error);
    }
);

axiosServices.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            const status = error.response.status;
            const message = error.response.data?.error || error.response.data?.message || 'An error occurred';

            switch (status) {
                case 401:
                    localStorage.removeItem('token');
                    if (window.location.pathname !== '/auth/login') {
                        window.location.href = '/auth/login';
                    }
                    break;
                case 403:
                    console.error('Access forbidden');
                    break;
                case 404:
                    console.error('Resource not found');
                    break;
                case 500:
                    console.error('Server error');
                    break;
                default:
                    console.error('Error:', message);
            }

            return Promise.reject({
                status,
                message,
                data: error.response.data
            });
        } else if (error.request) {
            console.error('Network error - no response received');
            return Promise.reject({
                message: 'Network error. Please check your connection.'
            });
        } else {
            console.error('Request setup error:', error.message);
            return Promise.reject({
                message: 'An unexpected error occurred'
            });
        }
    }
);

export default axiosServices;
