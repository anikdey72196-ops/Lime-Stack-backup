const API_URL = 'http://127.0.0.1:5000';

const api = {
    getToken() {
        return localStorage.getItem('access_token');
    },

    setToken(token) {
        localStorage.setItem('access_token', token);
    },

    clearToken() {
        localStorage.removeItem('access_token');
    },

    isLoggedIn() {
        return !!this.getToken();
    },

    async request(endpoint, method = 'GET', body = null) {
        const headers = {
            'Content-Type': 'application/json'
        };

        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method,
            headers
        };

        if (body) {
            config.body = JSON.stringify(body);
        }

        const response = await fetch(`${API_URL}${endpoint}`, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || JSON.stringify(data));
        }

        return data;
    },

    async login(email, password) {
        const data = await this.request('/SignIn', 'POST', { email, password });
        if (data.access_token) {
            this.setToken(data.access_token);
        }
        return data;
    },

    async register(username, email, password) {
        return await this.request('/registration', 'POST', { username, email, password });
    },

    async fetchPosts() {
        return await this.request('/archive', 'GET');
    },

    async createPost(title, content) {
        return await this.request('/post/new', 'POST', { title, content });
    },
    
    async deletePost(id) {
        return await this.request(`/post/${id}`, 'DELETE');
    }
};

// UI Helpers
function updateNav() {
    const authLinks = document.getElementById('auth-links');
    const userLinks = document.getElementById('user-links');
    
    if (!authLinks || !userLinks) return;

    if (api.isLoggedIn()) {
        authLinks.classList.add('hidden');
        userLinks.classList.remove('hidden');
    } else {
        authLinks.classList.remove('hidden');
        userLinks.classList.add('hidden');
    }
}

function logout() {
    api.clearToken();
    window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', updateNav);
