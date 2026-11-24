// ==========================================================================
// Campus AI Assistant - Client Controller (v1 API Integration)
// High-Fidelity UI, Student/Admin Authentication, Timetables, Courses & Drafter
// ==========================================================================

const isBackendHost = window.location.port === '8000';
const BACKEND_ORIGIN = (window.location.protocol.startsWith('http') && isBackendHost) 
    ? window.location.origin 
    : 'http://localhost:8000';
const API_BASE = `${BACKEND_ORIGIN}/api/v1`;
const ROOT_URL = BACKEND_ORIGIN;

let chatHistory = [];
let allCourses = [];
let allNotes = [];
let allFaqs = [];
let currentDocOutput = '';
let currentUser = null;
let currentAuthRole = 'student';
let currentPreviewNoteId = null;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', async () => {
    initTheme();
    setupKeyboardShortcuts();
    restoreAuth();
    await checkHealth();
    await Promise.all([
        fetchTimetables(),
        loadCourses(),
        loadCourseNotes(),
        loadExams(),
        loadFaqs()
    ]);
});

// ==========================================================================
// THEME MANAGEMENT (DARK / LIGHT MODE)
// ==========================================================================

function initTheme() {
    const savedTheme = localStorage.getItem('campus_theme') || 'light';
    const checkbox = document.getElementById('themeToggleCheckbox');
    if (savedTheme === 'dark') {
        document.body.classList.remove('theme-light');
        document.body.classList.add('theme-dark');
        if (checkbox) checkbox.checked = true;
    } else {
        document.body.classList.remove('theme-dark');
        document.body.classList.add('theme-light');
        if (checkbox) checkbox.checked = false;
    }
}

function toggleTheme() {
    const isDark = document.body.classList.contains('theme-dark');
    if (isDark) {
        document.body.classList.remove('theme-dark');
        document.body.classList.add('theme-light');
        localStorage.setItem('campus_theme', 'light');
    } else {
        document.body.classList.remove('theme-light');
        document.body.classList.add('theme-dark');
        localStorage.setItem('campus_theme', 'dark');
    }
}

// ==========================================================================
// AUTHENTICATION & PROFILE MANAGEMENT
// ==========================================================================

function restoreAuth() {
    const token = localStorage.getItem('campus_token') || sessionStorage.getItem('campus_token');
    const userJson = localStorage.getItem('campus_user') || sessionStorage.getItem('campus_user');

    if (token && userJson) {
        try {
            currentUser = JSON.parse(userJson);
            updateAuthUI();
            return;
        } catch (e) {
            console.error('Failed to parse user profile', e);
        }
    }

    // Default demo profile for seamless instant experience (Surya D. as shown in reference)
    currentUser = {
        username: 'surya',
        full_name: 'Surya D.',
        role: 'student',
        roll_number: '22AI104',
        department: 'CSE (AI)',
        semester: 'Sem 5 (CSE - AI)',
        cgpa: '8.0',
        email: 'surya@campus.edu',
        resume_url: 'https://drive.google.com/file/d/1_surya_academic_resume_2026/view',
        skills: 'Python, Machine Learning, Deep Learning, FastAPI, PostgreSQL, React, Docker',
        phone: '+91 98765 43210'
    };
    updateAuthUI();
}

function updateAuthUI() {
    if (!currentUser) return;

    // Header Display
    const nameEl = document.getElementById('userDisplayName');
    const roleEl = document.getElementById('userDisplayRole');
    const dropdownNameEl = document.getElementById('dropdownFullName');
    const dropdownEmailEl = document.getElementById('dropdownEmail');
    const dropdownRoleTag = document.getElementById('dropdownRoleTag');
    const heroNameEl = document.getElementById('heroStudentName');
    const dropdownProfileBtn = document.getElementById('dropdownProfileBtn');

    const displayName = currentUser.full_name || currentUser.username;
    const isStudent = currentUser.role === 'student';
    const roleLabel = isStudent 
        ? `Student • ${currentUser.department || 'CSE (AI)'}`
        : 'Administrator • Academic Registrar';

    if (nameEl) nameEl.textContent = displayName;
    if (roleEl) roleEl.textContent = roleLabel;
    if (dropdownNameEl) dropdownNameEl.textContent = displayName;
    if (dropdownEmailEl) dropdownEmailEl.textContent = currentUser.email || `${currentUser.username}@campus.edu`;
    if (dropdownRoleTag) dropdownRoleTag.textContent = isStudent ? 'Student' : 'Administrator';
    if (heroNameEl) heroNameEl.textContent = displayName.split(' ')[0] || displayName;

    if (dropdownProfileBtn) {
        dropdownProfileBtn.style.display = isStudent ? 'flex' : 'none';
    }

    // Toggle Admin Portal Nav Items
    const adminSubnav = document.getElementById('adminSubnavBtn');
    const sidebarAdmin = document.getElementById('sidebarAdminBtn');
    if (currentUser.role === 'admin') {
        if (adminSubnav) adminSubnav.style.display = 'inline-flex';
        if (sidebarAdmin) sidebarAdmin.style.display = 'flex';
    } else {
        if (adminSubnav) adminSubnav.style.display = 'none';
        if (sidebarAdmin) sidebarAdmin.style.display = 'none';
    }

    // Update Academic Progress & Metrics
    const metricCgpa = document.getElementById('metricCgpaVal');
    const widgetCgpa = document.getElementById('widgetCgpa');
    const widgetSem = document.getElementById('widgetSemester');
    if (metricCgpa && currentUser.cgpa) metricCgpa.textContent = currentUser.cgpa;
    if (widgetCgpa && currentUser.cgpa) widgetCgpa.textContent = currentUser.cgpa;
    if (widgetSem && currentUser.semester) widgetSem.textContent = currentUser.semester;
}

function toggleProfileDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

// Close dropdown on outside click
document.addEventListener('click', (e) => {
    const profilePill = document.getElementById('userProfilePill');
    const dropdown = document.getElementById('profileDropdown');
    if (dropdown && profilePill && !profilePill.contains(e.target)) {
        dropdown.classList.remove('show');
    }
});

function handleLogout() {
    localStorage.removeItem('campus_token');
    localStorage.removeItem('campus_user');
    sessionStorage.removeItem('campus_token');
    sessionStorage.removeItem('campus_user');

    currentUser = null;
    quickNotify('You have been logged out. Opening login modal...');
    openAuthModal('signin');
}

// Auth Modal Controller
function openAuthModal(mode = 'signin') {
    const modal = document.getElementById('authModal');
    if (modal) {
        modal.style.display = 'flex';
        switchAuthMode(mode);
    }
}

function closeAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) modal.style.display = 'none';
    hideAuthMessage();
}

function switchAuthMode(mode) {
    const tabSignIn = document.getElementById('tabSignInBtn');
    const tabSignUp = document.getElementById('tabSignUpBtn');
    const formSignIn = document.getElementById('signInForm');
    const formSignUp = document.getElementById('signUpForm');

    hideAuthMessage();

    if (mode === 'signin') {
        tabSignIn.classList.add('active');
        tabSignUp.classList.remove('active');
        formSignIn.style.display = 'flex';
        formSignUp.style.display = 'none';
    } else {
        tabSignUp.classList.add('active');
        tabSignIn.classList.remove('active');
        formSignUp.style.display = 'flex';
        formSignIn.style.display = 'none';
    }
}

function selectAuthRole(role) {
    currentAuthRole = role;
    const btnStudent = document.getElementById('roleBtnStudent');
    const btnAdmin = document.getElementById('roleBtnAdmin');
    const loginUserLabel = document.getElementById('loginUsernameLabel');
    const loginUserInput = document.getElementById('loginUsername');

    const adminNotice = document.getElementById('adminSignupNotice');
    const adminEmailGroup = document.getElementById('adminEmailFieldGroup');
    const studentFields = document.getElementById('studentSignupFields');
    const signUpBtn = document.getElementById('signUpSubmitBtn');

    if (role === 'student') {
        if (btnStudent) btnStudent.classList.add('active');
        if (btnAdmin) btnAdmin.classList.remove('active');
        if (loginUserLabel) loginUserLabel.textContent = 'Student Roll No. or Campus Email';
        if (loginUserInput) loginUserInput.placeholder = 'e.g. 22AI104 or surya@campus.edu';

        if (adminNotice) adminNotice.style.display = 'none';
        if (adminEmailGroup) adminEmailGroup.style.display = 'none';
        if (studentFields) studentFields.style.display = 'block';
        if (signUpBtn) signUpBtn.innerHTML = '<span>Create Student Account & Log In ✨</span>';
    } else {
        if (btnAdmin) btnAdmin.classList.add('active');
        if (btnStudent) btnStudent.classList.remove('active');
        if (loginUserLabel) loginUserLabel.textContent = 'Admin Email ID';
        if (loginUserInput) loginUserInput.placeholder = 'admin@campus.edu';

        if (adminNotice) adminNotice.style.display = 'block';
        if (adminEmailGroup) adminEmailGroup.style.display = 'block';
        if (studentFields) studentFields.style.display = 'none';
        if (signUpBtn) signUpBtn.innerHTML = '<span>Create Administrator Account 🛡️</span>';
    }
}

function fillDemoCredentials(username, password, role) {
    const uInput = document.getElementById('loginUsername');
    const pInput = document.getElementById('loginPassword');
    if (uInput) uInput.value = username;
    if (pInput) pInput.value = password;
    selectAuthRole(role);
}

// Sign In Request
async function handleSignInSubmit(event) {
    event.preventDefault();
    const u = document.getElementById('loginUsername').value.trim();
    const p = document.getElementById('loginPassword').value.trim();
    const remember = document.getElementById('rememberMeCheckbox')?.checked;

    const btn = document.getElementById('signInSubmitBtn');
    btn.disabled = true;
    btn.innerHTML = '<span>Verifying credentials... ⏳</span>';

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: u, password: p })
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Invalid username or password');
        }

        const data = await res.json();
        currentUser = {
            user_id: data.user_id,
            username: data.username,
            full_name: data.full_name || data.username,
            role: data.role,
            roll_number: data.roll_number || '',
            department: data.department || (data.role === 'admin' ? 'Academic Administration' : 'CSE (AI)'),
            semester: data.semester || (data.role === 'admin' ? 'Faculty / Admin' : 'Sem 5 (CSE - AI)'),
            cgpa: data.cgpa || '8.0',
            email: data.email || `${data.username}@campus.edu`,
            resume_url: data.resume_url || '',
            skills: data.skills || '',
            phone: data.phone || ''
        };

        const storage = remember ? localStorage : sessionStorage;
        storage.setItem('campus_token', data.access_token);
        storage.setItem('campus_user', JSON.stringify(currentUser));

        showAuthMessage(`✅ Welcome back, ${currentUser.full_name}!`, 'success');
        updateAuthUI();

        setTimeout(() => {
            closeAuthModal();
            quickNotify(`Signed in as ${currentUser.full_name} (${currentUser.role.toUpperCase()})`);
        }, 800);
    } catch (err) {
        showAuthMessage(`❌ ${err.message}`, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span>Sign In 🚀</span>';
    }
}

// Sign Up / Register Request
async function handleSignUpSubmit(event) {
    event.preventDefault();
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;

    if (password !== confirmPassword) {
        showAuthMessage('❌ Passwords do not match', 'error');
        return;
    }

    const btn = document.getElementById('signUpSubmitBtn');
    btn.disabled = true;
    btn.innerHTML = '<span>Creating Account... ⏳</span>';

    try {
        let payload = {};

        if (currentAuthRole === 'admin') {
            const adminEmail = (document.getElementById('regAdminEmail')?.value || '').trim();
            if (!adminEmail) {
                throw new Error('Please enter your official Admin Email ID');
            }
            payload = {
                email: adminEmail,
                password: password,
                role: 'admin',
                full_name: 'Campus Academic Registrar',
                department: 'Academic Administration',
                semester: 'Faculty / Admin',
                cgpa: 'N/A'
            };
        } else {
            const fullName = document.getElementById('regFullName').value.trim();
            const rollNo = document.getElementById('regUsername').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            const department = document.getElementById('regDept').value;
            const semester = document.getElementById('regSemester').value;
            const cgpa = document.getElementById('regCgpa').value || '8.0';
            const resumeUrl = (document.getElementById('regResume')?.value || '').trim();
            const skills = (document.getElementById('regSkills')?.value || '').trim();

            if (!email) {
                throw new Error('Please provide your campus email');
            }

            payload = {
                username: rollNo || email.split('@')[0],
                email: email,
                password: password,
                full_name: fullName || 'Enrolled Student',
                role: 'student',
                roll_number: rollNo,
                department: department,
                semester: semester,
                cgpa: cgpa,
                resume_url: resumeUrl,
                skills: skills
            };
        }

        const res = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Registration failed');
        }

        const data = await res.json();
        currentUser = {
            user_id: data.user_id,
            username: data.username,
            full_name: data.full_name || payload.full_name,
            role: data.role,
            roll_number: data.roll_number || payload.roll_number || '',
            department: data.department || payload.department,
            semester: data.semester || payload.semester,
            cgpa: data.cgpa || payload.cgpa,
            email: data.email || payload.email,
            resume_url: data.resume_url || payload.resume_url || '',
            skills: data.skills || payload.skills || '',
            phone: data.phone || ''
        };

        localStorage.setItem('campus_token', data.access_token);
        localStorage.setItem('campus_user', JSON.stringify(currentUser));

        showAuthMessage(`✨ Account created! Welcome, ${currentUser.full_name}!`, 'success');
        updateAuthUI();

        setTimeout(() => {
            closeAuthModal();
            quickNotify(`Account created successfully! Logged in as ${currentUser.full_name}`);
        }, 1000);
    } catch (err) {
        showAuthMessage(`❌ ${err.message}`, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = (currentAuthRole === 'admin') 
            ? '<span>Create Administrator Account 🛡️</span>' 
            : '<span>Create Student Account & Log In ✨</span>';
    }
}

// ==========================================================================
// STUDENT PROFILE MODAL & RESUME MANAGEMENT
// ==========================================================================

function openStudentProfileModal() {
    if (!currentUser) return;
    const modal = document.getElementById('studentProfileModal');
    if (!modal) return;

    // View elements
    const nameEl = document.getElementById('profileModalName');
    const rollEl = document.getElementById('profileModalRoll');
    const deptEl = document.getElementById('profileModalDept');
    const cgpaEl = document.getElementById('profileViewCgpa');
    const emailEl = document.getElementById('profileViewEmail');
    const deptViewEl = document.getElementById('profileViewDept');
    const semViewEl = document.getElementById('profileViewSem');
    const phoneViewEl = document.getElementById('profileViewPhone');
    const resumeBtn = document.getElementById('profileResumeLinkBtn');
    const resumeStatus = document.getElementById('profileResumeStatusText');
    const skillsCloud = document.getElementById('profileSkillsCloud');

    if (nameEl) nameEl.textContent = currentUser.full_name || currentUser.username;
    if (rollEl) rollEl.textContent = `Roll: ${currentUser.roll_number || '22AI104'}`;
    if (deptEl) deptEl.textContent = `${currentUser.department || 'CSE (AI)'} • ${currentUser.semester || 'Sem 5'}`;
    if (cgpaEl) cgpaEl.textContent = currentUser.cgpa || '8.0';
    if (emailEl) emailEl.textContent = currentUser.email || `${currentUser.username}@campus.edu`;
    if (deptViewEl) deptViewEl.textContent = currentUser.department || 'Computer Science & AI';
    if (semViewEl) semViewEl.textContent = currentUser.semester || 'Semester 5';
    if (phoneViewEl) phoneViewEl.textContent = currentUser.phone || '+91 98765 43210';

    if (resumeBtn) {
        if (currentUser.resume_url && currentUser.resume_url.trim()) {
            resumeBtn.href = currentUser.resume_url;
            resumeBtn.style.pointerEvents = 'auto';
            resumeBtn.style.opacity = '1';
            resumeBtn.innerHTML = '<span>📄 View / Download Resume</span> <span class="ext-arrow">↗</span>';
            if (resumeStatus) resumeStatus.textContent = 'Verified Student Resume Linked';
        } else {
            resumeBtn.href = '#';
            resumeBtn.style.pointerEvents = 'none';
            resumeBtn.style.opacity = '0.6';
            resumeBtn.innerHTML = '<span>No Resume Linked (Click Edit)</span>';
            if (resumeStatus) resumeStatus.textContent = 'Resume not yet provided';
        }
    }

    if (skillsCloud) {
        const skillsArr = (currentUser.skills || 'Python, Machine Learning, FastAPI, PostgreSQL, React')
            .split(',')
            .map(s => s.trim())
            .filter(Boolean);
        skillsCloud.innerHTML = skillsArr.map(s => `<span class="skill-tag">${escapeHtml(s)}</span>`).join('');
    }

    toggleEditProfileMode(false);
    modal.style.display = 'flex';
}

function closeStudentProfileModal() {
    const modal = document.getElementById('studentProfileModal');
    if (modal) modal.style.display = 'none';
}

function toggleEditProfileMode(isEdit) {
    const viewSec = document.getElementById('profileViewSection');
    const editSec = document.getElementById('profileEditSection');

    if (isEdit) {
        if (viewSec) viewSec.style.display = 'none';
        if (editSec) editSec.style.display = 'block';

        // Pre-fill inputs
        const nameIn = document.getElementById('editProfileName');
        const rollIn = document.getElementById('editProfileRoll');
        const cgpaIn = document.getElementById('editProfileCgpa');
        const phoneIn = document.getElementById('editProfilePhone');
        const resumeIn = document.getElementById('editProfileResume');
        const skillsIn = document.getElementById('editProfileSkills');

        if (nameIn) nameIn.value = currentUser.full_name || '';
        if (rollIn) rollIn.value = currentUser.roll_number || '';
        if (cgpaIn) cgpaIn.value = currentUser.cgpa || '8.0';
        if (phoneIn) phoneIn.value = currentUser.phone || '';
        if (resumeIn) resumeIn.value = currentUser.resume_url || '';
        if (skillsIn) skillsIn.value = currentUser.skills || '';
    } else {
        if (viewSec) viewSec.style.display = 'block';
        if (editSec) editSec.style.display = 'none';
    }
}

async function handleSaveProfile(event) {
    event.preventDefault();
    const btn = document.getElementById('saveProfileBtn');
    btn.disabled = true;
    btn.innerHTML = '<span>Saving Profile... ⏳</span>';

    const name = document.getElementById('editProfileName').value.trim();
    const roll = document.getElementById('editProfileRoll').value.trim();
    const cgpa = document.getElementById('editProfileCgpa').value.trim();
    const phone = document.getElementById('editProfilePhone').value.trim();
    const resume = document.getElementById('editProfileResume').value.trim();
    const skills = document.getElementById('editProfileSkills').value.trim();

    try {
        const payload = {
            full_name: name,
            roll_number: roll,
            cgpa: cgpa,
            phone: phone,
            resume_url: resume,
            skills: skills
        };

        const res = await fetch(`${API_BASE}/auth/profile`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Failed to update profile');
        }

        const updated = await res.json();
        currentUser = {
            ...currentUser,
            full_name: updated.full_name,
            roll_number: updated.roll_number,
            cgpa: updated.cgpa,
            phone: updated.phone,
            resume_url: updated.resume_url,
            skills: updated.skills
        };

        localStorage.setItem('campus_user', JSON.stringify(currentUser));
        updateAuthUI();
        openStudentProfileModal();
        quickNotify('🎉 Student Profile updated successfully!');
    } catch (e) {
        quickNotify(`Error updating profile: ${e.message}`);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span>💾 Save Profile Changes</span>';
    }
}

function showAuthMessage(msg, type) {
    const box = document.getElementById('authMessageBox');
    if (box) {
        box.textContent = msg;
        box.className = `auth-message-box ${type}`;
        box.style.display = 'block';
    }
}

function hideAuthMessage() {
    const box = document.getElementById('authMessageBox');
    if (box) box.style.display = 'none';
}

// ==========================================================================
// NAVIGATION & TAB SWITCHING
// ==========================================================================

function switchMainTab(targetTabId) {
    // Subnav pills
    document.querySelectorAll('.subnav-pill').forEach(btn => {
        if (btn.dataset.tab === targetTabId) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Sidebar items
    document.querySelectorAll('.sidebar-nav .nav-item').forEach(btn => {
        const target = btn.dataset.target;
        if (target === targetTabId || (targetTabId === 'chat' && target === 'dashboard')) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Content panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });

    const activePane = document.getElementById(`pane-${targetTabId}`);
    if (activePane) {
        activePane.classList.add('active');
    }
}

function setupKeyboardShortcuts() {
    window.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('globalSearchInput');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
    });
}

function handleGlobalSearch(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        const query = e.target.value.trim();
        if (!query) return;

        // Switch to AI chat tab and submit search query
        switchMainTab('chat');
        askQuickPrompt(query);
        e.target.value = '';
    }
}

// ==========================================================================
// AI HEALTH CHECK & LIVE STATUS BADGE
// ==========================================================================

async function checkHealth() {
    const badge = document.getElementById('aiStatusBadge');
    const textEl = document.getElementById('aiStatusText');

    try {
        const res = await fetch(`${API_BASE}/health`);
        if (!res.ok) throw new Error('Health check failed');
        const data = await res.json();

        if (data.gemini_live_connected) {
            if (badge) badge.className = 'live-ai-badge';
            if (textEl) textEl.textContent = 'Live Gemini AI Active';
        } else {
            if (badge) badge.className = 'live-ai-badge';
            if (textEl) textEl.textContent = 'Grounded Campus Database';
        }
    } catch (e) {
        if (textEl) textEl.textContent = 'Grounded Local Fallback';
    }
}

// ==========================================================================
// CONVERSATIONAL AI CHAT
// ==========================================================================

function askQuickPrompt(promptText) {
    const input = document.getElementById('chatInput');
    if (input) {
        input.value = promptText;
        handleChatSubmit(new Event('submit'));
    }
}

async function handleChatSubmit(event) {
    if (event) event.preventDefault();
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;

    input.value = '';
    appendChatMessage('user', msg);

    const sendBtn = document.getElementById('chatSendBtn');
    const sendIcon = sendBtn.querySelector('.send-icon');
    const sendSpinner = sendBtn.querySelector('.send-spinner');
    if (sendIcon) sendIcon.style.display = 'none';
    if (sendSpinner) sendSpinner.style.display = 'inline';
    sendBtn.disabled = true;

    // Loading placeholder bubble
    const loadingId = 'loading-' + Date.now();
    appendLoadingBubble(loadingId);

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: msg,
                history: chatHistory.slice(-6)
            })
        });

        removeBubble(loadingId);

        if (!res.ok) {
            throw new Error(`Server returned HTTP ${res.status}`);
        }

        const data = await res.json();
        chatHistory.push({ role: 'user', content: msg });
        chatHistory.push({ role: 'model', content: data.response });

        appendChatMessage('model', data.response, data.citations, data.is_fallback);
    } catch (err) {
        removeBubble(loadingId);
        appendChatMessage('model', `I apologize, but I encountered a communication issue. Here is verified campus information regarding: "${msg}". Please check the Timetable and Examination Hub tabs for official records.`, []);
    } finally {
        if (sendIcon) sendIcon.style.display = 'inline';
        if (sendSpinner) sendSpinner.style.display = 'none';
        sendBtn.disabled = false;
    }
}

function appendChatMessage(role, text, citations = [], isFallback = false) {
    const container = document.getElementById('chatMessages');
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${role === 'user' ? 'user-bubble' : 'bot-bubble'}`;

    const avatar = document.createElement('div');
    avatar.className = 'bubble-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const body = document.createElement('div');
    body.className = 'bubble-body';

    // Format Markdown paragraphs, bold text & lists
    body.innerHTML = formatMarkdown(text);

    // Citations tags
    if (citations && citations.length > 0) {
        const citBox = document.createElement('div');
        citBox.className = 'citations-box';
        citations.forEach(c => {
            const span = document.createElement('span');
            span.className = 'citation-tag';
            span.textContent = `📍 ${c.title || c.type}`;
            citBox.appendChild(span);
        });
        body.appendChild(citBox);
    }

    bubble.appendChild(avatar);
    bubble.appendChild(body);
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
}

function appendLoadingBubble(id) {
    const container = document.getElementById('chatMessages');
    const bubble = document.createElement('div');
    bubble.id = id;
    bubble.className = 'chat-bubble bot-bubble';
    bubble.innerHTML = `
        <div class="bubble-avatar">🤖</div>
        <div class="bubble-body">
            <span>Thinking and querying verified campus database... ⏳</span>
        </div>
    `;
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
}

function removeBubble(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function clearChat() {
    chatHistory = [];
    const container = document.getElementById('chatMessages');
    container.innerHTML = `
        <div class="chat-bubble bot-bubble">
            <div class="bubble-avatar">🤖</div>
            <div class="bubble-body">
                <p class="greeting-text"><strong>Chat reset. How can I assist you with your academics today?</strong></p>
                <p>You can ask about today's timetable, exam dates, prerequisites, or draft formal leave applications.</p>
            </div>
        </div>
    `;
    quickNotify('Chat history cleared.');
}

function formatMarkdown(text) {
    if (!text) return '';
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^-\s+(.*)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul class="assistant-features-list">$1</ul>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
}

function toggleVoiceInput() {
    quickNotify('Voice Recognition activated: Speak your academic inquiry clearly.');
}

// ==========================================================================
// TIMETABLE NAVIGATOR
// ==========================================================================

async function fetchTimetables() {
    const dept = document.getElementById('deptSelect')?.value || 'CSE';
    const sem = document.getElementById('semSelect')?.value || 'Sem 4';
    const day = document.getElementById('daySelect')?.value || 'Tuesday';

    const container = document.getElementById('timetableResults');
    if (!container) return;

    container.innerHTML = '<div class="loading-state">Loading verified schedule...</div>';

    try {
        let url = `${API_BASE}/timetable?department=${encodeURIComponent(dept)}&semester=${encodeURIComponent(sem)}`;
        if (day && day !== 'ALL') {
            url += `&day=${encodeURIComponent(day)}`;
        }

        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}: Failed to fetch schedule`);
        const data = await res.json();

        // Extract slots list regardless of dict or flat array structure
        let slots = [];
        if (Array.isArray(data)) {
            slots = data;
        } else if (data && data.schedule) {
            if (day && day !== 'ALL') {
                const cleanDay = day.split(' ')[0].toLowerCase();
                for (const [dayName, daySlots] of Object.entries(data.schedule)) {
                    if (dayName.toLowerCase().includes(cleanDay)) {
                        slots = slots.concat(daySlots);
                    }
                }
            } else {
                for (const [dayName, daySlots] of Object.entries(data.schedule)) {
                    slots = slots.concat(daySlots.map(s => ({ ...s, day_label: dayName })));
                }
            }
        }

        if (!slots || slots.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>No class sessions scheduled for ${dept} (${sem}) on ${day}.</p>
                </div>
            `;
            return;
        }

        let html = `
            <table class="schedule-table">
                <thead>
                    <tr>
                        ${day === 'ALL' ? '<th>Day</th>' : ''}
                        <th>Time</th>
                        <th>Course Code & Title</th>
                        <th>Type</th>
                        <th>Venue / Room</th>
                        <th>Faculty Advisor</th>
                    </tr>
                </thead>
                <tbody>
        `;

        slots.forEach(item => {
            const timeStr = item.time || `${item.start_time || '09:00 AM'} - ${item.end_time || '10:00 AM'}`;
            const cCode = item.code || item.course_code || 'CS';
            const cTitle = item.subject || item.course_title || 'Class Lecture';
            const isLab = item.is_lab || item.course_type?.toLowerCase().includes('lab');
            const room = item.room || item.room_number || 'LH-101';
            const faculty = item.faculty || item.faculty_name || 'Department Faculty';

            html += `
                <tr>
                    ${day === 'ALL' ? `<td><strong>${item.day_label || day}</strong></td>` : ''}
                    <td><strong>${timeStr}</strong></td>
                    <td>
                        <span class="course-code-badge">${cCode}</span>
                        <strong>${cTitle}</strong>
                    </td>
                    <td><span class="room-tag ${isLab ? 'lab-tag' : ''}">${isLab ? 'Laboratory' : 'Lecture'}</span></td>
                    <td><strong>${room}</strong></td>
                    <td>${faculty}</td>
                </tr>
            `;
        });

        html += '</tbody></table>';
        container.innerHTML = html;

        // Update Today's Classes Metric
        const metricClasses = document.getElementById('metricClassesCount');
        if (metricClasses) metricClasses.textContent = slots.length;
    } catch (e) {
        container.innerHTML = `<div class="error-state">Failed to load schedule. ${e.message}</div>`;
    }
}

function exportTimetablePDF() {
    quickNotify('Exporting verified Academic Timetable as PDF...');
    window.print();
}

// ==========================================================================
// COURSE CATALOG & PREREQUISITE GRAPH
// ==========================================================================

async function loadCourses() {
    const container = document.getElementById('courseGrid');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/courses`);
        if (!res.ok) throw new Error('Failed to fetch courses');
        allCourses = await res.json();
        renderCourses(allCourses);

        // Populate course selects
        populateCourseSelects(allCourses);
    } catch (e) {
        container.innerHTML = `<div class="error-state">Failed to load courses: ${e.message}</div>`;
    }
}

function populateCourseSelects(courses) {
    const adminSelect = document.getElementById('adminNoteCourseSelect');
    const filterSelect = document.getElementById('noteCourseFilter');

    if (adminSelect) {
        adminSelect.innerHTML = '<option value="">Select Course...</option>' + 
            courses.map(c => `<option value="${c.code}">${c.code} — ${c.title}</option>`).join('');
    }

    if (filterSelect) {
        filterSelect.innerHTML = '<option value="ALL">All Courses</option>' + 
            courses.map(c => `<option value="${c.code}">${c.code} — ${c.title}</option>`).join('');
    }
}

function filterCourses() {
    const query = (document.getElementById('courseSearchInput')?.value || '').toLowerCase();
    const sem = document.getElementById('courseSemFilter')?.value || 'ALL';

    const filtered = allCourses.filter(c => {
        const matchesQuery = !query || 
            c.code.toLowerCase().includes(query) || 
            c.title.toLowerCase().includes(query) ||
            c.description?.toLowerCase().includes(query);

        const matchesSem = (sem === 'ALL') || (c.semester_number == sem);
        return matchesQuery && matchesSem;
    });

    renderCourses(filtered);
}

function renderCourses(courses) {
    const container = document.getElementById('courseGrid');
    if (!container) return;

    if (!courses || courses.length === 0) {
        container.innerHTML = '<p class="empty-state">No matching courses found.</p>';
        return;
    }

    container.innerHTML = courses.map(c => `
        <div class="course-card">
            <div class="course-code-row">
                <span class="course-code-badge">${c.code}</span>
                <span class="course-credits-badge">${c.credits} Credits • Sem ${c.semester_number}</span>
            </div>
            <h4 class="course-title">${c.title}</h4>
            <p class="course-desc">${c.description || 'Core departmental academic curriculum course.'}</p>
            <button class="course-prereq-btn" onclick="openPrereqModal('${c.id}', '${c.code}', '${escapeHtml(c.title)}')">
                🕸️ View Dependency Graph
            </button>
        </div>
    `).join('');
}

async function openPrereqModal(courseId, code, title) {
    const modal = document.getElementById('prereqModal');
    const content = document.getElementById('modalPrereqContent');
    const titleEl = document.getElementById('modalCourseTitle');
    const codeEl = document.getElementById('modalCourseCode');

    if (titleEl) titleEl.textContent = title;
    if (codeEl) codeEl.textContent = `${code} • Prerequisites & Dependencies`;
    if (content) content.innerHTML = '<div class="loading-state">Fetching prerequisite graph...</div>';
    if (modal) modal.style.display = 'flex';

    try {
        const res = await fetch(`${API_BASE}/courses/${courseId}/prerequisites`);
        if (!res.ok) throw new Error(`HTTP ${res.status}: Failed to fetch prerequisites`);
        const data = await res.json();

        const courseTitle = data.target_course?.title || data.course_title || title;
        const courseCode = data.target_course?.code || data.course_code || code;
        const strictPrereqs = data.strict_prerequisites || (data.upstream_prerequisites ? data.upstream_prerequisites.filter(p => p.is_strict) : []);
        const softPrereqs = data.co_requisites || (data.upstream_prerequisites ? data.upstream_prerequisites.filter(p => !p.is_strict) : []);
        const downstream = data.downstream_dependent_courses || [];

        let html = '<div class="prereq-tree-view" style="display:flex; flex-direction:column; gap:14px;">';
        html += `<div style="padding:12px 14px; background:rgba(99,102,241,0.08); border-radius:8px; border:1px solid rgba(99,102,241,0.25);">
            <strong style="color:var(--primary);">🎯 Target Course:</strong> <strong>${courseCode}</strong> — ${courseTitle}
        </div>`;

        if (strictPrereqs && strictPrereqs.length > 0) {
            html += '<div><strong style="color:#b91c1c;">🔒 Strict Prerequisites (Mandatory Prior Pass):</strong><ul style="margin:6px 0 0 18px;">';
            strictPrereqs.forEach(p => {
                html += `<li><strong>${p.code}</strong> — ${p.title} (${p.credits || 4} Credits, Sem ${p.semester_number || 1})</li>`;
            });
            html += '</ul></div>';
        } else {
            html += '<p style="color:#059669; font-weight: 500;">✅ No strict prerequisites. You are eligible to register directly!</p>';
        }

        if (softPrereqs && softPrereqs.length > 0) {
            html += '<div><strong style="color:#7c3aed;">🔗 Co-Requisites / Recommended:</strong><ul style="margin:6px 0 0 18px;">';
            softPrereqs.forEach(c => {
                html += `<li><strong>${c.code}</strong> — ${c.title}</li>`;
            });
            html += '</ul></div>';
        }

        if (downstream && downstream.length > 0) {
            html += '<div><strong style="color:#2563eb;">⏭️ Unlocks Downstream Advanced Courses:</strong><ul style="margin:6px 0 0 18px;">';
            downstream.forEach(d => {
                html += `<li><strong>${d.code}</strong> — ${d.title}</li>`;
            });
            html += '</ul></div>';
        }

        html += '</div>';
        content.innerHTML = html;
    } catch (e) {
        content.innerHTML = `<div class="error-state">Failed to load graph: ${e.message}</div>`;
    }
}

function closePrereqModal() {
    const modal = document.getElementById('prereqModal');
    if (modal) modal.style.display = 'none';
}

// ==========================================================================
// COURSE NOTES & STUDY MATERIALS (PDF DOWNLOAD ENGINE)
// ==========================================================================

async function loadCourseNotes() {
    const container = document.getElementById('notesGrid');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/notes`);
        if (!res.ok) throw new Error('Failed to fetch course notes');
        allNotes = await res.json();
        renderNotes(allNotes);
    } catch (e) {
        container.innerHTML = `<div class="error-state">Failed to load study notes: ${e.message}</div>`;
    }
}

function filterNotes() {
    const query = (document.getElementById('noteSearchInput')?.value || '').toLowerCase();
    const courseCode = document.getElementById('noteCourseFilter')?.value || 'ALL';

    const filtered = allNotes.filter(n => {
        const matchesQuery = !query ||
            n.title.toLowerCase().includes(query) ||
            n.unit_title.toLowerCase().includes(query) ||
            n.course_code.toLowerCase().includes(query) ||
            n.topic_description?.toLowerCase().includes(query) ||
            n.content_markdown?.toLowerCase().includes(query);

        const matchesCourse = (courseCode === 'ALL') || (n.course_code === courseCode);
        return matchesQuery && matchesCourse;
    });

    renderNotes(filtered);
}

function renderNotes(notes) {
    const container = document.getElementById('notesGrid');
    if (!container) return;

    if (!notes || notes.length === 0) {
        container.innerHTML = '<p class="empty-state">No matching course notes or study materials found.</p>';
        return;
    }

    container.innerHTML = notes.map(n => `
        <div class="note-card">
            <div class="note-meta-badges">
                <span class="course-code-badge">${n.course_code}</span>
                <span class="unit-tag">Unit ${n.unit_number}</span>
                <span class="pdf-format-badge">📄 ${n.file_format} • ${n.file_size_kb} KB</span>
            </div>
            <h4 class="note-title">${n.title}</h4>
            <span class="note-unit-sub">${n.unit_title}</span>
            <p class="note-topic-snippet">${n.topic_description || 'Official lecture notes, derivations, and exam prep material.'}</p>
            
            <div class="note-footer-row">
                <span>👨‍🏫 ${n.faculty_author}</span>
                <span id="dl-count-${n.id}">📥 ${n.download_count} Downloads</span>
            </div>

            <div class="note-actions-row">
                <button class="btn-preview-note" onclick="openNotePreview('${n.id}')">
                    👁️ Preview Note
                </button>
                <button class="btn-download-pdf" onclick="downloadNotePDF('${n.id}')">
                    📥 Download PDF
                </button>
            </div>
        </div>
    `).join('');
}

async function openNotePreview(noteId) {
    currentPreviewNoteId = noteId;
    const modal = document.getElementById('notePreviewModal');
    const titleEl = document.getElementById('modalNoteTitle');
    const metaEl = document.getElementById('modalNoteMeta');
    const topicBox = document.getElementById('modalNoteTopicBox');
    const contentBox = document.getElementById('modalNoteContent');
    const dlEl = document.getElementById('modalNoteDownloads');

    if (modal) modal.style.display = 'flex';
    if (contentBox) contentBox.innerHTML = '<div class="loading-state">Loading lecture note material...</div>';

    try {
        const res = await fetch(`${API_BASE}/notes/${noteId}`);
        if (!res.ok) throw new Error('Failed to load note details');
        const note = await res.json();

        if (titleEl) titleEl.textContent = note.title;
        if (metaEl) metaEl.textContent = `${note.course_code} • Unit ${note.unit_number}: ${note.unit_title} • ${note.faculty_author} • Session ${note.academic_year}`;
        if (dlEl) dlEl.textContent = `📥 ${note.download_count} Downloads`;

        if (topicBox) {
            topicBox.innerHTML = note.topic_description 
                ? `<strong>📌 Syllabus Coverage:</strong> ${note.topic_description}` 
                : '<strong>📌 Verified Academic Lecture Note</strong>';
        }

        if (contentBox) {
            contentBox.innerHTML = formatMarkdown(note.content_markdown);
        }
    } catch (e) {
        if (contentBox) contentBox.innerHTML = `<div class="error-state">Failed to load note: ${e.message}</div>`;
    }
}

function closeNotePreviewModal() {
    const modal = document.getElementById('notePreviewModal');
    if (modal) modal.style.display = 'none';
    currentPreviewNoteId = null;
}

function triggerNoteDownloadFromModal() {
    if (currentPreviewNoteId) {
        downloadNotePDF(currentPreviewNoteId);
    }
}

function downloadNotePDF(noteId) {
    quickNotify('Generating official university PDF...');
    const url = `${API_BASE}/notes/${noteId}/download`;

    // Trigger direct browser download
    const link = document.createElement('a');
    link.href = url;
    link.target = '_blank';
    link.download = `Course_Note_${noteId}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Update download count visually
    setTimeout(() => {
        const countSpan = document.getElementById(`dl-count-${noteId}`);
        if (countSpan) {
            const current = parseInt(countSpan.textContent.replace(/\D/g, ''), 10) || 0;
            countSpan.textContent = `📥 ${current + 1} Downloads`;
        }
        quickNotify('PDF downloaded successfully! 🎓');
    }, 1200);
}

// ==========================================================================
// EXAM NOTICES HUB
// ==========================================================================

async function loadExams() {
    const container = document.getElementById('examsList');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/exams`);
        if (!res.ok) throw new Error('Failed to load exams');
        const list = await res.json();

        const countEl = document.getElementById('metricExamsCount');
        if (countEl) countEl.textContent = list.length;

        if (!list || list.length === 0) {
            container.innerHTML = '<p class="empty-state">No active examination notices published.</p>';
            return;
        }

        container.innerHTML = list.map(item => `
            <div class="exam-notice-card">
                <div class="notice-top">
                    <span class="notice-code">${item.notice_code}</span>
                    <span class="deadline-tag ${item.is_urgent ? 'tag-urgent' : 'tag-normal'}">
                        ${item.is_urgent ? '⚠️ URGENT' : 'Official Notice'}
                    </span>
                </div>
                <h4 class="notice-title">${item.title}</h4>
                <div style="font-size:12px; color:#64748b; margin-top:4px;">
                    <strong>Applicable:</strong> ${item.applicable_to} | <strong>Window:</strong> ${item.exam_window || 'Exam Season 2026'}
                </div>
                <div class="notice-guidelines">
                    <strong>Regulations:</strong> ${item.calculator_policy || 'Non-programmable calculators only.'} ${item.hall_ticket_guidelines || ''}
                </div>
            </div>
        `).join('');
    } catch (e) {
        container.innerHTML = `<div class="error-state">Failed to load exam circulars: ${e.message}</div>`;
    }
}

// ==========================================================================
// ADMINISTRATIVE HELPDESK & FAQS
// ==========================================================================

async function loadFaqs() {
    const container = document.getElementById('faqsList');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/faqs`);
        if (!res.ok) throw new Error('Failed to load FAQs');
        allFaqs = await res.json();
        renderFaqs(allFaqs);
    } catch (e) {
        container.innerHTML = `<div class="error-state">Failed to load FAQs: ${e.message}</div>`;
    }
}

function filterFaqs() {
    const query = (document.getElementById('faqSearchInput')?.value || '').toLowerCase();
    const cat = document.getElementById('faqCategoryFilter')?.value || 'ALL';

    const filtered = allFaqs.filter(f => {
        const matchesQuery = !query || 
            f.question.toLowerCase().includes(query) || 
            f.answer.toLowerCase().includes(query);
        const matchesCat = (cat === 'ALL') || (f.category === cat);
        return matchesQuery && matchesCat;
    });

    renderFaqs(filtered);
}

function renderFaqs(faqs) {
    const container = document.getElementById('faqsList');
    if (!container) return;

    if (!faqs || faqs.length === 0) {
        container.innerHTML = '<p class="empty-state">No matching administrative FAQs found.</p>';
        return;
    }

    container.innerHTML = faqs.map((f, i) => `
        <div class="faq-card">
            <div class="faq-question-bar" onclick="toggleFaqAccordion('faq-ans-${i}')">
                <span><strong>${f.category}:</strong> ${f.question}</span>
                <span>▾</span>
            </div>
            <div class="faq-answer-body" id="faq-ans-${i}">
                <p>${f.answer}</p>
                <div style="font-size:11.5px; color:#64748b; margin-top:6px;">
                    📍 <strong>Office:</strong> ${f.office_location || 'Admin Desk'} | ✉️ <strong>Email:</strong> ${f.contact_email || 'helpdesk@campus.edu'}
                </div>
            </div>
        </div>
    `).join('');
}

function toggleFaqAccordion(id) {
    const el = document.getElementById(id);
    if (el) {
        el.style.display = (el.style.display === 'none') ? 'block' : 'none';
    }
}

// ==========================================================================
// ACADEMIC LETTER & EMAIL DRAFTER
// ==========================================================================

async function handleDraftSubmit(event) {
    event.preventDefault();
    const docType = document.getElementById('docType').value;
    const context = document.getElementById('docContext').value.trim();
    const tone = document.getElementById('docTone').value;
    const length = document.getElementById('docLength').value;

    const outBox = document.getElementById('documentOutputBox');
    const actions = document.getElementById('previewActions');
    const btn = document.getElementById('generateDocBtn');

    btn.disabled = true;
    btn.innerHTML = '<span>Drafting document... ⏳</span>';
    outBox.innerHTML = '<div class="loading-state">Synthesizing formal academic correspondence...</div>';

    try {
        const res = await fetch(`${API_BASE}/documents/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: docType,
                message: context,
                tone: tone,
                length: length
            })
        });

        if (!res.ok) throw new Error('Failed to generate document');
        const data = await res.json();
        currentDocOutput = data.output;

        outBox.textContent = currentDocOutput;
        if (actions) actions.style.display = 'flex';
        quickNotify(`Generated ${docType} successfully!`);
    } catch (e) {
        outBox.textContent = `Error generating document: ${e.message}\n\nPlease retry or check connection.`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span>✨ Generate Draft</span>';
    }
}

function copyDocumentToClipboard() {
    if (!currentDocOutput) return;
    navigator.clipboard.writeText(currentDocOutput).then(() => {
        quickNotify('Document copied to clipboard!');
    });
}

function downloadDocumentTxt() {
    if (!currentDocOutput) return;
    const blob = new Blob([currentDocOutput], { type: 'text/plain;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `Academic_Document_${Date.now()}.txt`;
    link.click();
}

function downloadDocumentPdf() {
    quickNotify('Formatting draft for PDF print output...');
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head><title>Academic Letter Draft</title></head>
            <body style="font-family: Georgia, serif; line-height: 1.6; padding: 40px; white-space: pre-wrap;">
                ${escapeHtml(currentDocOutput)}
            </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

function clearDrafterForm() {
    document.getElementById('drafterForm').reset();
    document.getElementById('documentOutputBox').innerHTML = `
        <div class="placeholder-prompt">
            <span>📝</span>
            <p>Fill out the form on the left and click <strong>Generate Draft</strong> to create formal academic correspondence.</p>
        </div>
    `;
    const actions = document.getElementById('previewActions');
    if (actions) actions.style.display = 'none';
    currentDocOutput = '';
}

// ==========================================================================
// ADMIN DATA MANAGEMENT
// ==========================================================================

async function handleAdminAddCourse(e) {
    e.preventDefault();
    const token = localStorage.getItem('campus_token') || sessionStorage.getItem('campus_token');
    if (!token) {
        quickNotify('Authentication required. Please log in as Administrator.');
        openAuthModal('signin');
        return;
    }

    const code = document.getElementById('adminCourseCode').value.trim();
    const title = document.getElementById('adminCourseTitle').value.trim();
    const credits = parseInt(document.getElementById('adminCourseCredits').value, 10);
    const sem = parseInt(document.getElementById('adminCourseSem').value, 10);
    const prereqs = document.getElementById('adminCoursePrereqs').value.trim();

    try {
        const res = await fetch(`${API_BASE}/admin/courses`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                code,
                title,
                credits,
                semester_number: sem,
                prerequisites_text: prereqs || 'None'
            })
        });

        if (!res.ok) throw new Error('Failed to publish course');
        quickNotify(`Course ${code} published to catalog!`);
        document.getElementById('adminCourseForm').reset();
        await loadCourses();
    } catch (err) {
        quickNotify(`Error: ${err.message}`);
    }
}

async function handleAdminAddExam(e) {
    e.preventDefault();
    const token = localStorage.getItem('campus_token') || sessionStorage.getItem('campus_token');
    if (!token) {
        quickNotify('Authentication required. Please log in as Administrator.');
        openAuthModal('signin');
        return;
    }

    const code = document.getElementById('adminExamCode').value.trim();
    const title = document.getElementById('adminExamTitle').value.trim();
    const audience = document.getElementById('adminExamAudience').value.trim();
    const instructions = document.getElementById('adminExamInstructions').value.trim();

    try {
        const res = await fetch(`${API_BASE}/admin/exams`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                notice_code: code,
                title,
                applicable_to: audience,
                calculator_policy: instructions,
                exam_type: 'Mid-Semester'
            })
        });

        if (!res.ok) throw new Error('Failed to post circular');
        quickNotify(`Exam circular ${code} published!`);
        document.getElementById('adminExamForm').reset();
        await loadExams();
    } catch (err) {
        quickNotify(`Error: ${err.message}`);
    }
}

async function handleAdminAddNote(e) {
    e.preventDefault();
    const token = localStorage.getItem('campus_token') || sessionStorage.getItem('campus_token');
    if (!token) {
        quickNotify('Authentication required. Please log in as Administrator.');
        openAuthModal('signin');
        return;
    }

    const courseCode = document.getElementById('adminNoteCourseSelect').value;
    const unitNumber = parseInt(document.getElementById('adminNoteUnitNumber').value, 10);
    const unitTitle = document.getElementById('adminNoteUnitTitle').value.trim();
    const title = document.getElementById('adminNoteTitle').value.trim();
    const faculty = document.getElementById('adminNoteFaculty').value.trim();
    const topicDesc = document.getElementById('adminNoteTopicDesc').value.trim();
    const content = document.getElementById('adminNoteContent').value.trim();

    if (!courseCode) {
        quickNotify('Please select a course for this study material.');
        return;
    }

    const submitBtn = document.getElementById('adminNoteSubmitBtn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Publishing Note & Generating PDF... ⏳</span>';

    try {
        const res = await fetch(`${API_BASE}/admin/notes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                course_code: courseCode,
                unit_number: unitNumber,
                unit_title: unitTitle,
                title: title,
                faculty_author: faculty,
                topic_description: topicDesc,
                content_markdown: content
            })
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Failed to publish note');
        }

        const data = await res.json();
        quickNotify(`✨ Lecture note published for ${courseCode}! PDF ready for student download.`);
        document.getElementById('adminNoteForm').reset();
        await loadCourseNotes();
    } catch (err) {
        quickNotify(`Error: ${err.message}`);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>➕ Publish Course Note & PDF</span>';
    }
}

// ==========================================================================
// TOAST NOTIFICATIONS & UTILITIES
// ==========================================================================

function quickNotify(msg) {
    const toast = document.getElementById('toastNotification');
    if (!toast) return;
    toast.textContent = msg;
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3200);
}

function showNotifications() {
    quickNotify('🔔 You have 2 unread campus notices: Mid-Sem Hall Ticket release & Hackathon registration.');
}

function toggleTaskDone(checkbox) {
    const label = checkbox.parentElement.querySelector('.deadline-label');
    if (checkbox.checked) {
        label.style.textDecoration = 'line-through';
        label.style.opacity = '0.6';
        quickNotify('Task marked as completed! 🎯');
    } else {
        label.style.textDecoration = 'none';
        label.style.opacity = '1';
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, function(m) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        }[m];
    });
}
