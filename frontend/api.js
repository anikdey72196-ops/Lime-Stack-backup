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

    getUserId() {
        return localStorage.getItem('user_id');
    },

    setUserId(userId) {
        localStorage.setItem('user_id', userId);
    },

    clearUserId() {
        localStorage.removeItem('user_id');
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
            let errorText;
            if (typeof data === 'object' && !data.error && !data.message) {
                // Extract Marshmallow validation errors
                const messages = [];
                for (const [field, errs] of Object.entries(data)) {
                    messages.push(`${field}: ${errs.join(', ')}`);
                }
                errorText = messages.join(' | ');
            } else {
                errorText = data.error || data.message || JSON.stringify(data);
            }
            throw new Error(errorText);
        }

        return data;
    },

    async login(email, password) {
        const data = await this.request('/SignIn', 'POST', { email, password });
        if (data.access_token) {
            this.setToken(data.access_token);
        }
        if (data.user_id) {
            this.setUserId(data.user_id);
        }
        return data;
    },

    async register(username, email, password) {
        return await this.request('/registration', 'POST', { username, email, password });
    },

    async getUserProfile() {
        return await this.request('/user/me', 'GET');
    },

    async updateProfile(bio) {
        return await this.request('/user/me', 'PUT', { Bio: bio });
    },

    async uploadProfilePicture(file) {
        const formData = new FormData();
        formData.append('profile_picture', file);
        
        const token = this.getToken();
        const response = await fetch(`${API_URL}/user/profile_picture`, {
            method: 'POST',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {},
            body: formData
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.message || 'Upload failed');
        return data;
    },

    async fetchPosts() {
        return await this.request('/archive', 'GET');
    },

    async getPost(id) {
        return await this.request(`/post/${id}`, 'GET');
    },

    async createPost(title, content) {
        return await this.request('/post/new', 'POST', { title, content });
    },
    
    async deletePost(id) {
        return await this.request(`/post/${id}`, 'DELETE');
    },

    async editPost(id, title, content) {
        return await this.request(`/post/${id}`, 'PUT', { title, content });
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

function enforceAuth() {
    const protectedPages = ['new_post.html', 'edit_post.html', 'account.html'];
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    if (protectedPages.includes(currentPage) && !api.isLoggedIn()) {
        window.location.href = 'auth.html';
    }
}

function logout() {
    api.clearToken();
    api.clearUserId();
    window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', () => {
    updateNav();
    enforceAuth();
});
