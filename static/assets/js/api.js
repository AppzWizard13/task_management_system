/**
 * API Request Handler with JWT Authentication
 */

const API_BASE_URL = '/api';

const API = {
    // Make authenticated API request
    async request(endpoint, options = {}) {
        // Default headers
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        // Add authorization header if user is authenticated
        const accessToken = AuthManager.getAccessToken();
        if (accessToken) {
            // Check if token is expired
            if (AuthManager.isTokenExpired(accessToken)) {
                const refreshed = await AuthManager.refreshAccessToken();
                if (!refreshed) {
                    // Token refresh failed, redirect to login
                    showAlert('Session expired. Please login again.', 'warning');
                    logout();
                    return null;
                }
            }
            headers['Authorization'] = `Bearer ${AuthManager.getAccessToken()}`;
        }

        // Build request options
        const config = {
            ...options,
            headers
        };

        try {
            showLoading(true);
            const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
            const data = await response.json();
            showLoading(false);

            if (!response.ok) {
                // Handle error responses
                throw {
                    status: response.status,
                    data: data
                };
            }

            return data;
        } catch (error) {
            showLoading(false);
            throw error;
        }
    },

    // GET request
    async get(endpoint) {
        return this.request(endpoint, {
            method: 'GET'
        });
    },

    // POST request
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    // PUT request
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    // PATCH request
    async patch(endpoint, data) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    },

    // DELETE request
    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    },

    // Upload file (multipart/form-data)
    async upload(endpoint, formData) {
        const accessToken = AuthManager.getAccessToken();
        const headers = {};
        
        if (accessToken) {
            headers['Authorization'] = `Bearer ${accessToken}`;
        }

        try {
            showLoading(true);
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: headers,
                body: formData
            });
            const data = await response.json();
            showLoading(false);

            if (!response.ok) {
                throw {
                    status: response.status,
                    data: data
                };
            }

            return data;
        } catch (error) {
            showLoading(false);
            throw error;
        }
    }
};

// Export for use in other files
window.API = API;
