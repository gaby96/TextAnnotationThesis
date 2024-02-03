import { useLoginStore } from '@/store/auth/login';
import { useUserStore } from '@/store/user/user';
import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL;
// let authToken;

const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 50000,
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
    },
})

// request Interceptor
axiosInstance.interceptors.request.use(async (config) => {
    const user = useUserStore()
    if (config.url === '/core/auth/refresh-token') {
        config.headers.Authorization = `Bearer ${user.accessToken}`
    } else {
        config.headers.Authorization = user.accessToken
    }
    return config
})

// response Interceptor
axiosInstance.interceptors.response.use(
    (res) => res,
    async (error) => {
        const user = useUserStore()
        const loginStore = useLoginStore()
        const originalRequest = error.config
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            try {
                user.accessToken = user.refreshToken
                const newAccessToken = await axiosInstance.post(
                    '/core/auth/refresh-token'
                )
                user.accessToken = newAccessToken.data.access_token
                return axiosInstance(originalRequest)
            } catch (error) {
                loginStore.logout()
                throw new Error(error)
            }
        }
        return Promise.reject(error)
    }
)

export default axiosInstance