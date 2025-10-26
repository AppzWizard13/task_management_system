/**
 * Authentication and JWT Token Management
 */

const AUTH_STORAGE_KEY = 'auth_tokens';
const USER_STORAGE_KEY = 'user_data';

// Token management
const AuthManager = {
    // Save tokens to localStorage
    saveTokens(tokens) {
        localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(tokens));
    },

    // Get access token
    getAccessToken() {
        const tokens = this.getTokens();
        return tokens ? tokens.access : null;
    },

    // Get refresh token
    getRefreshToken() {
        const tokens = this.getTokens();
        return tokens ? tokens.refresh : null;
    },

    // Get all tokens
    getTokens() {
        const tokens = localStorage.getItem(AUTH_STORAGE_KEY);
        return tokens ? JSON.parse(tokens) : null;
    },

    // Save user data
    saveUser(user) {
        localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
    },

    // Get user data
    getUser() {
        const user = localStorage.getItem(USER_STORAGE_KEY);
        return user ? JSON.parse(user) : null;
    },

    // Check if user is authenticated
    isAuthenticated() {
        return this.getAccessToken() !== null;
    },

    // Clear all auth data
    clearAuth() {
        localStorage.removeItem(AUTH_STORAGE_KEY);
        localStorage.removeItem(USER_STORAGE_KEY);
    },

    // Parse JWT token to get expiry
    parseJwt(token) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
            return JSON.parse(jsonPayload);
        } catch (e) {
            return null;
        }
    },

    // Check if token is expired
    isTokenExpired(token) {
        const decoded = this.parseJwt(token);
        if (!decoded || !decoded.exp) return true;
        
        const currentTime = Date.now() / 1000;
        return decoded.exp < currentTime;
    },

    // Refresh access token
    async refreshAccessToken() {
        const refreshToken = this.getRefreshToken();
        if (!refreshToken) {
            return false;
        }

        try {
            const response = await fetch('/api/accounts/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });

            if (response.ok) {
                const data = await response.json();
                const tokens = this.getTokens();
                tokens.access = data.access;
                if (data.refresh) {
                    tokens.refresh = data.refresh;
                }
                this.saveTokens(tokens);
                return true;
            } else {
                // Refresh token is invalid, clear auth
                this.clearAuth();
                return false;
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            this.clearAuth();
            return false;
        }
    }
};

// Export for use in other files
window.AuthManager = AuthManager;
