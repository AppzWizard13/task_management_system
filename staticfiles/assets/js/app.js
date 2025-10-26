/**
 * Main Application Logic
 */

// Initialize app on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
function initializeApp() {
    if (AuthManager.isAuthenticated()) {
        showAuthenticatedUI();
        showProfile();
    } else {
        showUnauthenticatedUI();
        showLogin();
    }
}

// Show/hide sections
function showSection(sectionId) {
    const sections = ['login-section', 'register-section', 'profile-section', 'tasks-section'];
    sections.forEach(section => {
        document.getElementById(section).classList.add('hidden');
    });
    document.getElementById(sectionId).classList.remove('hidden');
}

function showLogin() {
    showSection('login-section');
}

function showRegister() {
    showSection('register-section');
}

function showProfile() {
    showSection('profile-section');
    loadProfile();
}

function showTasks() {
    showSection('tasks-section');
    // Load tasks functionality will be added later
}

// UI state management
function showAuthenticatedUI() {
    document.getElementById('nav-login').classList.add('hidden');
    document.getElementById('nav-register').classList.add('hidden');
    document.getElementById('nav-profile').classList.remove('hidden');
    document.getElementById('nav-tasks').classList.remove('hidden');
    document.getElementById('nav-logout').classList.remove('hidden');
}

function showUnauthenticatedUI() {
    document.getElementById('nav-login').classList.remove('hidden');
    document.getElementById('nav-register').classList.remove('hidden');
    document.getElementById('nav-profile').classList.add('hidden');
    document.getElementById('nav-tasks').classList.add('hidden');
    document.getElementById('nav-logout').classList.add('hidden');
}

// Alert management
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    const alertId = 'alert-' + Date.now();
    
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHTML);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alertElement = document.getElementById(alertId);
        if (alertElement) {
            alertElement.remove();
        }
    }, 5000);
}

// Loading spinner
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

// Handle registration
async function handleRegister(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Remove empty fields
    Object.keys(data).forEach(key => {
        if (data[key] === '') {
            delete data[key];
        }
    });
    
    try {
        const response = await API.post('/accounts/register/', data);
        
        // Save tokens and user data
        AuthManager.saveTokens(response.tokens);
        AuthManager.saveUser(response.user);
        
        showAlert('Registration successful!', 'success');
        showAuthenticatedUI();
        showProfile();
        form.reset();
    } catch (error) {
        console.error('Registration error:', error);
        const errorMessage = formatErrorMessage(error.data);
        showAlert(errorMessage, 'danger');
    }
}

// Handle login
async function handleLogin(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await API.post('/accounts/login/', data);
        
        // Save tokens and user data
        AuthManager.saveTokens(response.tokens);
        AuthManager.saveUser(response.user);
        
        showAlert('Login successful!', 'success');
        showAuthenticatedUI();
        showProfile();
        form.reset();
    } catch (error) {
        console.error('Login error:', error);
        const errorMessage = formatErrorMessage(error.data);
        showAlert(errorMessage, 'danger');
    }
}

// Handle logout
async function logout() {
    const refreshToken = AuthManager.getRefreshToken();
    
    if (refreshToken) {
        try {
            await API.post('/accounts/logout/', { refresh: refreshToken });
        } catch (error) {
            console.error('Logout error:', error);
        }
    }
    
    AuthManager.clearAuth();
    showAlert('Logged out successfully', 'info');
    showUnauthenticatedUI();
    showLogin();
}

// Load profile
async function loadProfile() {
    try {
        const profile = await API.get('/accounts/profile/');
        displayProfile(profile);
    } catch (error) {
        console.error('Error loading profile:', error);
        showAlert('Error loading profile', 'danger');
    }
}

// Display profile in form
function displayProfile(profile) {
    const profileForm = document.getElementById('profile-form');
    
    const genderOptions = {
        'M': 'Male',
        'F': 'Female',
        'O': 'Other',
        'P': 'Prefer not to say'
    };
    
    profileForm.innerHTML = `
        <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" class="form-control" value="${profile.username}" disabled>
        </div>
        <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" value="${profile.email}" disabled>
        </div>
        <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input type="text" class="form-control" name="full_name" value="${profile.full_name || ''}">
        </div>
        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="form-label">Date of Birth</label>
                <input type="date" class="form-control" name="date_of_birth" value="${profile.date_of_birth || ''}">
            </div>
            <div class="col-md-6 mb-3">
                <label class="form-label">Gender</label>
                <select class="form-control" name="gender">
                    <option value="">Select Gender</option>
                    <option value="M" ${profile.gender === 'M' ? 'selected' : ''}>Male</option>
                    <option value="F" ${profile.gender === 'F' ? 'selected' : ''}>Female</option>
                    <option value="O" ${profile.gender === 'O' ? 'selected' : ''}>Other</option>
                    <option value="P" ${profile.gender === 'P' ? 'selected' : ''}>Prefer not to say</option>
                </select>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label">Mobile Number</label>
            <input type="tel" class="form-control" name="mobile_number" value="${profile.mobile_number || ''}">
        </div>
        <div class="mb-3">
            <label class="form-label">Address</label>
            <textarea class="form-control" name="address" rows="3">${profile.address || ''}</textarea>
        </div>
        ${profile.age ? `<div class="mb-3"><strong>Age:</strong> ${profile.age} years</div>` : ''}
        <button type="submit" class="btn btn-primary">Update Profile</button>
    `;
}

// Handle profile update
async function handleProfileUpdate(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Remove empty fields
    Object.keys(data).forEach(key => {
        if (data[key] === '') {
            delete data[key];
        }
    });
    
    try {
        const response = await API.patch('/accounts/profile/', data);
        AuthManager.saveUser(response);
        showAlert('Profile updated successfully!', 'success');
        displayProfile(response);
    } catch (error) {
        console.error('Profile update error:', error);
        const errorMessage = formatErrorMessage(error.data);
        showAlert(errorMessage, 'danger');
    }
}

// Handle password change
async function handlePasswordChange(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    try {
        await API.post('/accounts/change-password/', data);
        showAlert('Password changed successfully!', 'success');
        form.reset();
    } catch (error) {
        console.error('Password change error:', error);
        const errorMessage = formatErrorMessage(error.data);
        showAlert(errorMessage, 'danger');
    }
}

// Format error messages
function formatErrorMessage(errorData) {
    if (typeof errorData === 'string') {
        return errorData;
    }
    
    if (errorData.detail) {
        return errorData.detail;
    }
    
    if (errorData.message) {
        return errorData.message;
    }
    
    // Handle field-specific errors
    const errors = [];
    for (const [field, messages] of Object.entries(errorData)) {
        if (Array.isArray(messages)) {
            errors.push(`${field}: ${messages.join(', ')}`);
        } else {
            errors.push(`${field}: ${messages}`);
        }
    }
    
    return errors.length > 0 ? errors.join('<br>') : 'An error occurred';
}
