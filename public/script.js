const API = "http://localhost:8000";

window.addEventListener('DOMContentLoaded', async () => {
  if (await checkAuth()) {
    loadUserInfo();
  }
});

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
    window.location.href = 'login.html';
    return false;
  }

  try {
    const res = await fetch(`${API}/api/user/`, {
      headers: getAuthHeaders()
    });

    if (res.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = 'login.html';
      return false;
    }

    return true;
  } catch (error) {
    return true;
  }
}

function loadUserInfo() {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    const user = JSON.parse(userStr);
    const usernameEl = document.getElementById('username');
    if (usernameEl) {
      usernameEl.textContent = `👋 Welcome, ${user.username}!`;
      usernameEl.style.color = '#58a6ff';
    }
    if (user.is_admin) {
      const adminBadge = document.getElementById('adminBadge');
      if (adminBadge) {
        adminBadge.style.display = 'inline';
      }
      const adminPanelBtn = document.getElementById('adminPanelBtn');
      if (adminPanelBtn) {
        adminPanelBtn.style.display = 'inline-block';
      }
    }
  }
}

function showMessage(message, type = 'success') {
  // Remove existing messages
  const existing = document.querySelector('.message');
  if (existing) {
    existing.remove();
  }

  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  messageDiv.textContent = message;
  document.body.appendChild(messageDiv);

  setTimeout(() => {
    messageDiv.style.animation = 'slideIn 0.3s ease reverse';
    setTimeout(() => messageDiv.remove(), 300);
  }, 3000);
}

function logout() {
  if (confirm('Are you sure you want to logout?')) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
  }
}

function updateDashboardStats(count) {
  const totalStudentsEl = document.getElementById('totalStudents');
  if (totalStudentsEl) {
    totalStudentsEl.textContent = count;
    totalStudentsEl.style.transform = 'scale(1.1)';
    setTimeout(() => {
      totalStudentsEl.style.transform = 'scale(1)';
    }, 200);
  }
}

async function getStudents() {
  const isAuth = await checkAuth();
  if (!isAuth) return;

  const tableBody = document.querySelector('#studentTable tbody');
  tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px;">Loading...</td></tr>';

  try {
    const res = await fetch(`${API}/api/students/`, {
      headers: getAuthHeaders()
    });

    if (res.status === 401) {
      logout();
      return;
    }

    const data = await res.json();
    tableBody.innerHTML = '';

    if (data.error) {
      showMessage(data.error, 'error');
      tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px; color: red;">Error loading students</td></tr>';
      return;
    }

    if (data.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px; color: #666;">No students found. Add your first student above! 👆</td></tr>';
      updateDashboardStats(0);
      return;
    }

    const userStr = localStorage.getItem('user');
    const userObj = userStr ? JSON.parse(userStr) : null;
    const isAdmin = userObj && userObj.is_admin;

    const tableHeadRow = document.querySelector('#studentTable thead tr');
    if (isAdmin && !document.getElementById('th-owner')) {
      const th = document.createElement('th');
      th.id = 'th-owner';
      th.textContent = 'Owner';
      // Insert before Actions (last child)
      tableHeadRow.insertBefore(th, tableHeadRow.lastElementChild);
    }

    data.forEach(student => {
      const row = document.createElement('tr');
      // Escape HTML to prevent XSS
      const name = student.name.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
      const email = student.email.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
      const course = student.course.replace(/"/g, '&quot;').replace(/'/g, '&#39;');

      let ownerCell = '';
      if (isAdmin) {
        ownerCell = `<td style="color: #58a6ff; font-weight: 500;">${student.username || 'Unknown'}</td>`;
      }

      row.innerHTML = `
        <td><input value="${name}" id="name-${student._id}"></td>
        <td><input value="${email}" id="email-${student._id}"></td>
        <td><input value="${course}" id="course-${student._id}"></td>
        ${ownerCell}
        <td>
          <button onclick="updateStudent('${student._id}')">✏️ Update</button>
          <button onclick="deleteStudent('${student._id}')">🗑️ Delete</button>
        </td>`;
      tableBody.appendChild(row);
    });

    // Update dashboard stats
    updateDashboardStats(data.length);
  } catch (error) {
    console.error('Error fetching students:', error);
    showMessage('Error loading students', 'error');
    tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px; color: red;">Error loading students. Please refresh the page.</td></tr>';
  }
}

async function addStudent() {
  const isAuth = await checkAuth();
  if (!isAuth) return;

  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const course = document.getElementById('course').value.trim();

  if (!name || !email || !course) {
    showMessage('Please fill all fields!', 'error');
    return;
  }

  // Disable button during submission
  const submitBtn = document.querySelector('.form button[type="submit"]');
  const originalText = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = 'Adding...';

  try {
    const res = await fetch(`${API}/api/students/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ name, email, course })
    });

    if (res.status === 401) {
      logout();
      return;
    }

    const data = await res.json();
    if (data.error) {
      showMessage(data.error, 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
      return;
    }

    showMessage('Student added successfully!', 'success');
    document.getElementById('name').value = '';
    document.getElementById('email').value = '';
    document.getElementById('course').value = '';
    getStudents();
  } catch (error) {
    console.error('Error adding student:', error);
    showMessage('Error adding student. Please try again.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = originalText;
  }
}

async function deleteStudent(id) {
  const isAuth = await checkAuth();
  if (!isAuth) return;

  if (!confirm('Are you sure you want to delete this student?')) {
    return;
  }

  try {
    const res = await fetch(`${API}/api/students/${id}/`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });

    if (res.status === 401) {
      logout();
      return;
    }

    const data = await res.json();
    if (data.error) {
      showMessage(data.error, 'error');
      return;
    }

    showMessage('Student deleted successfully!', 'success');
    getStudents();
  } catch (error) {
    console.error('Error deleting student:', error);
    showMessage('Error deleting student', 'error');
  }
}

async function updateStudent(id) {
  const isAuth = await checkAuth();
  if (!isAuth) return;

  const name = document.getElementById(`name-${id}`).value;
  const email = document.getElementById(`email-${id}`).value;
  const course = document.getElementById(`course-${id}`).value;

  try {
    const res = await fetch(`${API}/api/students/${id}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ name, email, course })
    });

    if (res.status === 401) {
      logout();
      return;
    }

    const data = await res.json();
    if (data.error) {
      showMessage(data.error, 'error');
      return;
    }

    showMessage('Student updated successfully!', 'success');
    getStudents();
  } catch (error) {
    console.error('Error updating student:', error);
    showMessage('Error updating student', 'error');
  }
}

// Load students on page load
(async () => {
  const isAuth = await checkAuth();
  if (isAuth) {
    getStudents();
  }
})();
