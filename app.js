// Application Data - Using provided JSON data
const appData = {
    universities: [
        {
            id: 1,
            name: "Indian Institute of Technology Delhi",
            code: "IITD",
            state: "Delhi",
            region: "North",
            placementRate: "95%",
            faculties: 450,
            departments: 16
        },
        {
            id: 2,
            name: "Indian Institute of Science Bangalore",
            code: "IISc",
            state: "Karnataka",
            region: "South",
            placementRate: "98%",
            faculties: 350,
            departments: 14
        },
        {
            id: 3,
            name: "University of Delhi",
            code: "DU",
            state: "Delhi",
            region: "North",
            placementRate: "82%",
            faculties: 1200,
            departments: 90
        }
    ],
    students: [
        {
            id: 1,
            name: "Drishti Sharma",
            email: "drishti@example.com",
            universityId: 1,
            course: "B.Tech Computer Science",
            year: "3rd Year",
            creditScore: 85
        },
        {
            id: 2,
            name: "Rahul Kumar",
            email: "rahul@example.com",
            universityId: 2,
            course: "B.Tech Mechanical",
            year: "4th Year",
            creditScore: 92
        }
    ],
    alumni: [
        {
            id: 1,
            name: "Priya Singh",
            email: "priya@example.com",
            universityId: 1,
            graduationYear: "2020",
            currentCompany: "Google",
            expertise: ["Software Development", "Machine Learning"],
            mentorshipAvailable: true
        },
        {
            id: 2,
            name: "Arjun Patel",
            email: "arjun@example.com",
            universityId: 2,
            graduationYear: "2019",
            currentCompany: "Microsoft",
            expertise: ["Data Science", "Cloud Computing"],
            mentorshipAvailable: true
        }
    ],
    organizations: [
        {
            id: 1,
            name: "TechCorp India",
            industry: "Information Technology",
            website: "www.techcorp.com",
            verificationStatus: "Verified"
        },
        {
            id: 2,
            name: "InnovateLabs",
            industry: "Research & Development",
            website: "www.innovatelabs.in",
            verificationStatus: "Verified"
        }
    ],
    certificates: [
        {
            id: "CERT001",
            studentId: 1,
            type: "Course Completion",
            status: "Approved",
            uploadDate: "2024-01-15",
            approvalDate: "2024-01-20"
        },
        {
            id: "CERT002",
            studentId: 1,
            type: "Internship Certificate",
            status: "Pending",
            uploadDate: "2024-02-01"
        },
        {
            id: "CERT003",
            studentId: 2,
            type: "Project Certificate",
            status: "Rejected",
            uploadDate: "2024-01-25",
            rejectionReason: "Invalid signature"
        }
    ],
    events: [
        {
            id: 1,
            title: "Tech Career Fair 2024",
            organizerId: 1,
            date: "2024-03-15",
            location: "Delhi",
            maxParticipants: 500,
            description: "Annual career fair with top tech companies"
        },
        {
            id: 2,
            title: "Alumni Networking Event",
            organizerId: 2,
            date: "2024-03-20",
            location: "Bangalore",
            maxParticipants: 200,
            description: "Connect with alumni from various institutions"
        }
    ],
    notifications: [
        {
            id: 1,
            title: "New Course Registration Open",
            content: "Registration for summer courses is now open",
            targetAudience: "students",
            sentAt: "2024-02-01"
        },
        {
            id: 2,
            title: "Alumni Meet Announcement",
            content: "Annual alumni meet scheduled for March 2024",
            targetAudience: "alumni",
            sentAt: "2024-02-05"
        }
    ]
};

// Application State
let currentUser = null;
let currentUserType = null;
let currentPage = 'landing-page';

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    // Show landing page by default
    showPage('landing-page');
    
    // Check if user is already logged in (for demo purposes)
    const savedUser = localStorage.getItem('adhyayan_user');
    if (savedUser) {
        try {
            const userData = JSON.parse(savedUser);
            currentUser = userData.user;
            currentUserType = userData.userType;
            showDashboard(currentUserType);
        } catch (e) {
            console.log('Invalid saved user data');
        }
    }
}

function setupEventListeners() {
    // Login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Search functionality
    const searchInput = document.getElementById('university-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(performSearch, 300));
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchUniversities();
            }
        });
    }
    
    // Modal close on outside click
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            hideModals();
        }
    });
    
    // Escape key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            hideModals();
        }
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 16px;
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-base);
        box-shadow: var(--shadow-lg);
        z-index: 1100;
        max-width: 300px;
        animation: slideIn 0.3s ease-out;
    `;
    
    if (type === 'success') {
        notification.style.borderColor = 'var(--color-success)';
        notification.style.backgroundColor = 'rgba(var(--color-success-rgb), 0.1)';
    } else if (type === 'error') {
        notification.style.borderColor = 'var(--color-error)';
        notification.style.backgroundColor = 'rgba(var(--color-error-rgb), 0.1)';
    }
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Page Navigation
function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show target page
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
        currentPage = pageId;
    }
}

function showDashboard(userType) {
    const dashboardMap = {
        'student': 'student-dashboard',
        'alumni': 'alumni-dashboard',
        'admin': 'admin-dashboard',
        'organization': 'organization-dashboard'
    };
    
    const dashboardId = dashboardMap[userType];
    if (dashboardId) {
        showPage(dashboardId);
    }
}

// Modal Management
function showModal(modalId) {
    hideModals(); // Hide any open modals first
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        // Focus first input
        const firstInput = modal.querySelector('input, select, textarea, button');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    }
}

function hideModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.add('hidden');
    });
}

function showLoginModal() {
    showModal('login-modal');
}

function showRegisterModal() {
    showModal('register-modal');
}

function showUploadModal() {
    showModal('upload-modal');
}

// User Type Switching in Login
function switchUserType(userType) {
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update form placeholder based on user type
    const emailInput = document.getElementById('login-email');
    const placeholderMap = {
        'student': 'Student ID or Email',
        'alumni': 'Email Address',
        'admin': 'Admin ID',
        'organization': 'Organization Email'
    };
    
    if (emailInput) {
        emailInput.placeholder = placeholderMap[userType] || 'Email or ID';
    }
}

// Login Handling
function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const activeTab = document.querySelector('.tab-btn.active');
    
    if (!activeTab) {
        showNotification('Please select a user type', 'error');
        return;
    }
    
    const userType = getUserTypeFromTab(activeTab);
    
    // Simple demo authentication
    if (authenticateUser(email, password, userType)) {
        hideModals();
        showNotification('Login successful!', 'success');
        currentUserType = userType;
        
        // Save user session (for demo)
        localStorage.setItem('adhyayan_user', JSON.stringify({
            user: currentUser,
            userType: currentUserType
        }));
        
        // Redirect to appropriate dashboard
        showDashboard(userType);
    } else {
        showNotification('Invalid credentials. Try: drishti@example.com / password', 'error');
    }
}

function getUserTypeFromTab(tabElement) {
    const tabText = tabElement.textContent.toLowerCase();
    if (tabText.includes('student')) return 'student';
    if (tabText.includes('alumni')) return 'alumni';
    if (tabText.includes('admin')) return 'admin';
    if (tabText.includes('organization')) return 'organization';
    return 'student';
}

function authenticateUser(email, password, userType) {
    // Demo authentication - accept any password for demo users
    const userDataMap = {
        'student': appData.students,
        'alumni': appData.alumni,
        'organization': appData.organizations
    };
    
    if (userType === 'admin') {
        // Admin login
        if (email.includes('admin') || email.includes('iit')) {
            currentUser = { id: 1, name: 'College Admin', email: email };
            return true;
        }
    } else {
        const userData = userDataMap[userType];
        if (userData) {
            const user = userData.find(u => u.email === email);
            if (user) {
                currentUser = user;
                return true;
            }
        }
    }
    
    return false;
}

function logout() {
    currentUser = null;
    currentUserType = null;
    localStorage.removeItem('adhyayan_user');
    showPage('landing-page');
    showNotification('Logged out successfully', 'success');
}

// University Search
function searchUniversities() {
    const query = document.getElementById('university-search').value.toLowerCase();
    const resultsContainer = document.getElementById('search-results');
    
    if (!query.trim()) {
        resultsContainer.innerHTML = '';
        return;
    }
    
    const results = appData.universities.filter(uni => 
        uni.name.toLowerCase().includes(query) ||
        uni.code.toLowerCase().includes(query) ||
        uni.state.toLowerCase().includes(query) ||
        uni.region.toLowerCase().includes(query)
    );
    
    displaySearchResults(results, resultsContainer);
}

function performSearch() {
    const query = document.getElementById('university-search').value.toLowerCase();
    if (query.length >= 2) {
        searchUniversities();
    }
}

function displaySearchResults(results, container) {
    if (results.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--color-text-secondary);">No universities found</p>';
        return;
    }
    
    container.innerHTML = results.map(uni => `
        <div class="university-result">
            <div class="university-info">
                <h4>${uni.name} (${uni.code})</h4>
                <p>${uni.state} • ${uni.region} India</p>
            </div>
            <div class="university-stats">
                <p>Placement Rate: <strong>${uni.placementRate}</strong></p>
                <p>${uni.faculties} Faculty • ${uni.departments} Departments</p>
            </div>
        </div>
    `).join('');
}

// Scroll to Features
function scrollToFeatures() {
    document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
}

// Dashboard Tab Switching
function switchStudentTab(tabName) {
    switchTab('student', tabName);
}

function switchAdminTab(tabName) {
    switchTab('admin', tabName);
}

function switchAlumniTab(tabName) {
    switchTab('alumni', tabName);
}

function switchOrgTab(tabName) {
    switchTab('org', tabName);
}

function switchTab(userType, tabName) {
    // Update nav items
    const dashboard = document.getElementById(`${userType}-dashboard`);
    if (!dashboard) return;
    
    dashboard.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Find and activate the clicked nav item
    const navItems = dashboard.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        if (item.onclick && item.onclick.toString().includes(tabName)) {
            item.classList.add('active');
        }
    });
    
    // Update tab content
    dashboard.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    const targetTab = document.getElementById(`${userType}-${tabName}`);
    if (targetTab) {
        targetTab.classList.add('active');
    }
}

// Certificate Management
function uploadCertificate() {
    // Simulate certificate upload
    const newCertId = `CERT${String(appData.certificates.length + 1).padStart(3, '0')}`;
    
    const newCert = {
        id: newCertId,
        studentId: currentUser.id,
        type: "New Certificate",
        status: "Pending",
        uploadDate: new Date().toISOString().split('T')[0]
    };
    
    appData.certificates.push(newCert);
    
    hideModals();
    showNotification('Certificate uploaded successfully! Awaiting approval.', 'success');
    
    // Refresh certificates list if on certificates tab
    if (currentPage === 'student-dashboard') {
        updateCertificatesList();
    }
}

function updateCertificatesList() {
    const userCerts = appData.certificates.filter(cert => cert.studentId === currentUser.id);
    const container = document.querySelector('#student-certificates .certificates-list');
    
    if (container) {
        container.innerHTML = userCerts.map(cert => `
            <div class="certificate-item card">
                <div class="certificate-info">
                    <h4>${cert.type}</h4>
                    <p>ID: ${cert.id}</p>
                    <small>Uploaded: ${formatDate(cert.uploadDate)}</small>
                </div>
                <div class="certificate-status">
                    <span class="status status--${getStatusClass(cert.status)}">${cert.status}</span>
                </div>
            </div>
        `).join('');
    }
}

function getStatusClass(status) {
    const statusMap = {
        'Approved': 'success',
        'Pending': 'warning',
        'Rejected': 'error'
    };
    return statusMap[status] || 'info';
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Admin Certificate Approval
function approveCertificate(certId) {
    const cert = appData.certificates.find(c => c.id === certId);
    if (cert) {
        cert.status = 'Approved';
        cert.approvalDate = new Date().toISOString().split('T')[0];
        showNotification(`Certificate ${certId} approved successfully!`, 'success');
        updateApprovalsList();
    }
}

function rejectCertificate(certId) {
    const reason = prompt('Enter rejection reason:');
    if (reason) {
        const cert = appData.certificates.find(c => c.id === certId);
        if (cert) {
            cert.status = 'Rejected';
            cert.rejectionReason = reason;
            showNotification(`Certificate ${certId} rejected.`, 'error');
            updateApprovalsList();
        }
    }
}

function updateApprovalsList() {
    const pendingCerts = appData.certificates.filter(cert => cert.status === 'Pending');
    const container = document.querySelector('#admin-certificates .approval-list');
    
    if (container) {
        if (pendingCerts.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--color-text-secondary);">No pending certificate approvals</p>';
        } else {
            container.innerHTML = pendingCerts.map(cert => {
                const student = appData.students.find(s => s.id === cert.studentId);
                return `
                    <div class="approval-item card">
                        <div class="approval-info">
                            <h4>${cert.type}</h4>
                            <p>Student: ${student ? student.name : 'Unknown'} (ID: ${cert.id})</p>
                            <small>Submitted: ${formatDate(cert.uploadDate)}</small>
                        </div>
                        <div class="approval-actions">
                            <button class="btn btn--primary btn--sm" onclick="approveCertificate('${cert.id}')">Approve</button>
                            <button class="btn btn--outline btn--sm" onclick="rejectCertificate('${cert.id}')">Reject</button>
                        </div>
                    </div>
                `;
            }).join('');
        }
    }
}

// Notification System
function sendNotification() {
    const title = document.getElementById('notification-title').value;
    const content = document.getElementById('notification-content').value;
    const audience = document.getElementById('notification-audience').value;
    
    if (!title || !content) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    const newNotification = {
        id: appData.notifications.length + 1,
        title: title,
        content: content,
        targetAudience: audience,
        sentAt: new Date().toISOString().split('T')[0]
    };
    
    appData.notifications.push(newNotification);
    
    // Clear form
    document.getElementById('notification-title').value = '';
    document.getElementById('notification-content').value = '';
    
    showNotification(`Notification sent to ${audience}!`, 'success');
}

// Certificate Verification (Organization)
function verifyCertificate() {
    const certId = document.getElementById('verify-cert-id').value.trim();
    const resultContainer = document.getElementById('verification-result');
    
    if (!certId) {
        showNotification('Please enter a certificate ID', 'error');
        return;
    }
    
    const cert = appData.certificates.find(c => c.id === certId);
    
    if (cert && cert.status === 'Approved') {
        const student = appData.students.find(s => s.id === cert.studentId);
        const university = appData.universities.find(u => u.id === student?.universityId);
        
        resultContainer.className = 'verification-result success';
        resultContainer.innerHTML = `
            <h4>✓ Certificate Verified</h4>
            <p><strong>Type:</strong> ${cert.type}</p>
            <p><strong>Student:</strong> ${student ? student.name : 'Unknown'}</p>
            <p><strong>University:</strong> ${university ? university.name : 'Unknown'}</p>
            <p><strong>Approved Date:</strong> ${formatDate(cert.approvalDate)}</p>
        `;
    } else if (cert && cert.status === 'Pending') {
        resultContainer.className = 'verification-result error';
        resultContainer.innerHTML = `
            <h4>⚠ Certificate Pending Approval</h4>
            <p>This certificate is still under review by the institution.</p>
        `;
    } else if (cert && cert.status === 'Rejected') {
        resultContainer.className = 'verification-result error';
        resultContainer.innerHTML = `
            <h4>✗ Certificate Rejected</h4>
            <p>This certificate was rejected by the institution.</p>
            <p><strong>Reason:</strong> ${cert.rejectionReason || 'Not specified'}</p>
        `;
    } else {
        resultContainer.className = 'verification-result error';
        resultContainer.innerHTML = `
            <h4>✗ Certificate Not Found</h4>
            <p>No certificate found with ID: ${certId}</p>
        `;
    }
}

// Event Management
function showJobPostModal() {
    // For demo purposes, just show an alert
    alert('Job posting form would open here. This would include fields for job title, description, requirements, salary, location, etc.');
}

function showEventModal() {
    // For demo purposes, just show an alert
    alert('Event creation form would open here. This would include fields for event name, date, time, location, description, max participants, etc.');
}

// Mobile Navigation Toggle
function toggleMobileNav() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('mobile-open');
    }
}

// Initialize dashboard data when switching to dashboards
function initializeDashboardData() {
    if (currentUserType === 'student' && currentUser) {
        updateCertificatesList();
    } else if (currentUserType === 'admin') {
        updateApprovalsList();
    }
}

// Additional utility functions for enhanced interactivity
function toggleMentorshipAvailability() {
    const checkbox = document.getElementById('mentorship-available');
    if (checkbox && currentUser) {
        const isAvailable = checkbox.checked;
        showNotification(
            `Mentorship availability ${isAvailable ? 'enabled' : 'disabled'}`,
            'success'
        );
    }
}

// Add event listeners for dynamic content
document.addEventListener('click', function(e) {
    // Handle mentorship availability toggle
    if (e.target.id === 'mentorship-available') {
        toggleMentorshipAvailability();
    }
    
    // Handle certificate verification clear
    if (e.target.closest('.verification-tool')) {
        const input = document.getElementById('verify-cert-id');
        if (input && !input.value) {
            const result = document.getElementById('verification-result');
            if (result) {
                result.style.display = 'none';
            }
        }
    }
});

// Initialize dashboard data when page loads
window.addEventListener('load', function() {
    initializeDashboardData();
});

// Simulated real-time updates (for demo purposes)
setInterval(function() {
    // Simulate receiving new notifications, certificate approvals, etc.
    if (currentUserType === 'admin' && Math.random() > 0.98) {
        // Very rarely add a new pending certificate for demo
        // This is just for demonstration of real-time updates
    }
}, 5000);

// Add CSS animation keyframes dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .mobile-open {
        position: fixed !important;
        top: 0;
        left: 0;
        height: 100vh;
        z-index: 1000;
        background-color: var(--color-surface);
    }
    
    @media (max-width: 768px) {
        .mobile-nav-toggle {
            display: block;
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1001;
            background: var(--color-primary);
            color: white;
            border: none;
            border-radius: var(--radius-base);
            padding: var(--space-8);
            cursor: pointer;
        }
    }
`;
document.head.appendChild(style);

// Error handling for missing elements
function safeQuerySelector(selector) {
    try {
        return document.querySelector(selector);
    } catch (e) {
        console.warn(`Element not found: ${selector}`);
        return null;
    }
}

// Export functions for global access (if needed)
window.adhyayanSathi = {
    showLoginModal,
    showRegisterModal,
    hideModals,
    switchUserType,
    searchUniversities,
    scrollToFeatures,
    logout,
    switchStudentTab,
    switchAdminTab,
    switchAlumniTab,
    switchOrgTab,
    uploadCertificate,
    approveCertificate,
    rejectCertificate,
    sendNotification,
    verifyCertificate,
    showUploadModal,
    showJobPostModal,
    showEventModal
};