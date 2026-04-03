// ═══════════════════════════════════════════════════════════════════════════
// Student Record Manager — Main JS
// Enterprise UI interactions and API Integrations
// ═══════════════════════════════════════════════════════════════════════════

const API = window.location.origin;
let allStudents = [];

// ── Initialization ──────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', async () => {
  if (await checkAuth()) {
    loadUserInfo();
    if(window.location.pathname === '/' || window.location.pathname === '/index.html' || window.location.pathname === '') {
      getStudents();
    } else if(window.location.pathname.includes('admin.html')) {
        getUsers();
    }
    
    // Check for success messages from login redirect
    const welcomeMsg = sessionStorage.getItem('welcomeMsg');
    if (welcomeMsg) {
      setTimeout(() => showToast(welcomeMsg, 'success'), 300);
      sessionStorage.removeItem('welcomeMsg');
    }
  }
});

// ── Auth Helpers ────────────────────────────────────────────────────────
function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
}

async function checkAuth() {
  const token = localStorage.getItem('token');
  if (!token) {
    if(!window.location.pathname.includes('login.html')) {
      window.location.href = '/login.html';
    }
    return false;
  }
  
  try {
    const res = await fetch(`${API}/api/user/`, { headers: getAuthHeaders() });
    if (res.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      if(!window.location.pathname.includes('login.html')) {
        window.location.href = '/login.html';
      }
      return false;
    }
    
    if(window.location.pathname.includes('login.html')) {
      window.location.href = '/';
      return false;
    }
    
    return true;
  } catch (error) {
    return true; // Assume offline/network error, don't force logout
  }
}

// ── User Info & UI ──────────────────────────────────────────────────────
function loadUserInfo() {
  const userStr = localStorage.getItem('user');
  if (!userStr) return;

  const user = JSON.parse(userStr);
  
  const avatar = document.getElementById('userAvatar');
  const greeting = document.getElementById('greetingText');
  const adminBadge = document.getElementById('adminBadge');
  
  if (avatar) avatar.textContent = user.username.charAt(0).toUpperCase();
  if (greeting) greeting.textContent = user.username;
  
  if (user.is_admin) {
    if(adminBadge) {
      adminBadge.textContent = "Admin";
      adminBadge.className = "badge admin";
      adminBadge.style.display = "inline-block";
    }
    const adminBtn = document.getElementById('adminPanelBtn');
    if (adminBtn) adminBtn.style.display = 'inline-flex';
    
    const theadRow = document.querySelector('#studentTable thead tr');
    if (theadRow && !document.getElementById('th-owner')) {
      const th = document.createElement('th');
      th.id = 'th-owner';
      th.textContent = 'Owner';
      theadRow.insertBefore(th, theadRow.lastElementChild);
    }
  } else {
    if(adminBadge) adminBadge.style.display = "none";
  }
}

function logout() {
  showConfirmModal('Sign Out', 'Are you sure you want to log out of your account?', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
  });
}

// ── Toasts & Modals ───────────────────────────────────────────────────
function showToast(message, type = 'info', title = null) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const icons = { success: '✓', error: '✕', info: 'i' };
  const titles = { success: 'Success', error: 'Error', info: 'Notice' };

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <div class="toast-icon">${icons[type] || icons.info}</div>
    <div>
      <div class="toast-title">${title || titles[type]}</div>
      <div class="toast-msg">${message}</div>
    </div>
    <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
  `;
  container.appendChild(toast);
  setTimeout(() => { if (toast.parentElement) toast.remove(); }, 4000);
}

function showConfirmModal(title, message, onConfirm, confirmText = 'Confirm', isDanger = false) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal">
      <h3>${title}</h3>
      <p>${message}</p>
      <div class="modal-actions">
        <button class="btn btn-outline" onclick="this.closest('.modal-overlay').remove()">Cancel</button>
        <button class="btn ${isDanger ? 'btn-danger' : 'btn-primary'}" id="modalConfirmBtn">${confirmText}</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
  overlay.querySelector('#modalConfirmBtn').addEventListener('click', () => {
    overlay.remove();
    onConfirm();
  });
}

// ── Utilities ──────────────────────────────────────────────────────────
function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function updateStats(students) {
  const totalEl = document.getElementById('totalStudents');
  if (totalEl) totalEl.textContent = students.length;

  const coursesEl = document.getElementById('totalCourses');
  if (coursesEl) {
    const unique = new Set(students.map(s => s.course.toLowerCase().trim())).size;
    coursesEl.textContent = unique;
  }
}

// ── Student Operations ────────────────────────────────────────────────
async function getStudents() {
  const tableBody = document.getElementById('studentTableBody');
  if (!tableBody) return;

  const skeletonHtml = `
    <tr><td colspan="5">
      <div style="display:flex; gap:16px; margin-bottom:12px;"><div class="skeleton" style="flex:1;"></div><div class="skeleton" style="flex:1;"></div><div class="skeleton" style="flex:1;"></div></div>
      <div style="display:flex; gap:16px; margin-bottom:12px;"><div class="skeleton" style="flex:1;"></div><div class="skeleton" style="flex:1;"></div><div class="skeleton" style="flex:1;"></div></div>
    </td></tr>`;
  
  tableBody.innerHTML = skeletonHtml;

  try {
    const res = await fetch(`${API}/api/students/`, { headers: getAuthHeaders() });
    if (res.status === 401) { logout(); return; }

    const data = await res.json();
    if (data.error) { showToast(data.error, 'error'); return; }

    allStudents = data;
    renderStudents(data);
    updateStats(data);
  } catch (error) {
    showToast('Failed to connect to the server.', 'error');
    tableBody.innerHTML = `<tr><td colspan="5"><div class="empty-state"><i>⚠</i><p>Failed to load records.</p></div></td></tr>`;
  }
}

function renderStudents(students) {
  const tableBody = document.getElementById('studentTableBody');
  if (!tableBody) return;

  tableBody.innerHTML = '';
  if (students.length === 0) {
    tableBody.innerHTML = `<tr><td colspan="5"><div class="empty-state"><i>📇</i><p>No student records found.</p></div></td></tr>`;
    return;
  }

  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const isAdmin = user.is_admin;

  students.forEach((student) => {
    const row = document.createElement('tr');
    const safeName = escapeHTML(student.name);
    const safeEmail = escapeHTML(student.email);
    const safeCourse = escapeHTML(student.course);

    let ownerCell = '';
    if (isAdmin) {
      const ownerName = escapeHTML(student.username || 'System');
      ownerCell = `<td><span class="badge user">${ownerName}</span></td>`;
    }

    row.innerHTML = `
      <td><input class="inline-edit" value="${safeName}" id="name-${student._id}" /></td>
      <td><input class="inline-edit" value="${safeEmail}" id="email-${student._id}" /></td>
      <td><input class="inline-edit" value="${safeCourse}" id="course-${student._id}" /></td>
      ${ownerCell}
      <td>
        <div class="actions-cell">
          <button class="btn-icon" onclick="updateStudent('${student._id}')" title="Save">💾</button>
          <button class="btn-icon danger" onclick="confirmDeleteStudent('${student._id}', '${safeName}')" title="Delete">🗑️</button>
        </div>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

function filterStudents() {
  const query = document.getElementById('searchInput').value.toLowerCase().trim();
  if (!query) { renderStudents(allStudents); return; }
  const filtered = allStudents.filter(s =>
    s.name.toLowerCase().includes(query) ||
    s.email.toLowerCase().includes(query) ||
    s.course.toLowerCase().includes(query)
  );
  renderStudents(filtered);
}

async function addStudent() {
  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const course = document.getElementById('course').value.trim();

  if (!name || !email || !course) {
    showToast('All fields are required.', 'error');
    return;
  }
  
  const btn = document.getElementById('addBtn');
  const origText = btn.innerHTML;
  btn.innerHTML = 'Adding...'; btn.disabled = true;

  try {
    const res = await fetch(`${API}/api/students/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ name, email, course })
    });
    const data = await res.json();
    if (data.error) { showToast(data.error, 'error'); return; }

    showToast('Record created successfully.', 'success');
    document.getElementById('addStudentForm').reset();
    getStudents();
  } catch (error) {
    showToast('Failed to add record.', 'error');
  } finally {
    btn.innerHTML = origText; btn.disabled = false;
  }
}

function confirmDeleteStudent(id, name) {
  showConfirmModal('Delete Record', `Are you sure you want to remove <strong>${name}</strong>?`, () => deleteStudent(id), 'Delete', true);
}

async function deleteStudent(id) {
  try {
    const res = await fetch(`${API}/api/students/${id}/`, { method: 'DELETE', headers: getAuthHeaders() });
    const data = await res.json();
    if (data.error) { showToast(data.error, 'error'); return; }
    showToast('Record deleted.', 'success');
    getStudents();
  } catch (e) {
    showToast('Network error on delete.', 'error');
  }
}

async function updateStudent(id) {
  const name = document.getElementById(`name-${id}`).value.trim();
  const email = document.getElementById(`email-${id}`).value.trim();
  const course = document.getElementById(`course-${id}`).value.trim();

  try {
    const res = await fetch(`${API}/api/students/${id}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ name, email, course })
    });
    const data = await res.json();
    if (data.error) { showToast(data.error, 'error'); return; }
    showToast('Record updated.', 'success');
    getStudents();
  } catch (e) {
    showToast('Network error on update.', 'error');
  }
}

// ── Admin Functions ─────────────────────────────────────────────────────
async function getUsers() {
  const tableBody = document.getElementById('usersTableBody');
  if (!tableBody) return;
  tableBody.innerHTML = `<tr><td colspan="4"><div class="skeleton"></div></td></tr>`;
  
  try {
    const res = await fetch(`${API}/api/admin/users/`, { headers: getAuthHeaders() });
    if (res.status === 403) { window.location.href = '/'; return; }
    
    const data = await res.json();
    if (data.error) { showToast(data.error, 'error'); return; }
    
    tableBody.innerHTML = '';
    if (data.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="4"><div class="empty-state"><p>No users.</p></div></td></tr>`;
      return;
    }
    
    data.forEach(user => {
      const row = document.createElement('tr');
      const safeUser = escapeHTML(user.username);
      const safeEmail = escapeHTML(user.email);
      
      const badge = user.is_admin ? '<span class="badge admin">Admin</span>' : '<span class="badge user">User</span>';
      
      row.innerHTML = `
        <td>
          <div style="font-weight: 500">${safeUser}</div>
          <div style="font-size: 0.8rem; color: var(--text-muted);">${safeEmail}</div>
        </td>
        <td>${user.student_count || 0}</td>
        <td>${badge}</td>
        <td>
          <div class="actions-cell">
            <button class="btn btn-outline btn-sm" onclick="toggleAdmin('${user._id}', ${user.is_admin})">
              ${user.is_admin ? 'Demote' : 'Promote'}
            </button>
            <button class="btn btn-danger btn-sm" onclick="deleteUser('${user._id}')">Delete</button>
          </div>
        </td>
      `;
      tableBody.appendChild(row);
    });
  } catch(e) {
    tableBody.innerHTML = `<tr><td colspan="4"><div class="empty-state"><p>Error loading.</p></div></td></tr>`;
  }
}

async function toggleAdmin(id, currentStatus) {
  try {
    const res = await fetch(`${API}/api/admin/users/${id}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ is_admin: !currentStatus })
    });
    const data = await res.json();
    if (data.error) { showToast(data.error, 'error'); return; }
    showToast('Permissions updated.', 'success');
    getUsers();
  } catch(e) { showToast('Error updating status.', 'error'); }
}

function deleteUser(id) {
  showConfirmModal('Delete User', 'Are you sure? This cannot be undone.', async () => {
    try {
      const res = await fetch(`${API}/api/admin/users/${id}/delete/`, { method: 'DELETE', headers: getAuthHeaders() });
      const data = await res.json();
      if (data.error) { showToast(data.error, 'error'); return; }
      showToast('User deleted.', 'success');
      getUsers();
    } catch(e) { showToast('Error deleting user.', 'error'); }
  }, 'Delete', true);
}
