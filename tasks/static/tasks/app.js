function getCsrfToken() {
  const name = 'csrftoken=';
  const parts = document.cookie.split(';');
  for (let i = 0; i < parts.length; i++) {
    let c = parts[i].trim();
    if (c.indexOf(name) === 0) return decodeURIComponent(c.substring(name.length));
  }
  return '';
}

function setupLiveSearchAndFilter() {
  const taskList = document.getElementById('task-list');
  if (!taskList) return;
  const searchInput = document.querySelector('form.controls input[name="q"]');
  const statusSelect = document.querySelector('form.controls select[name="status"]');

  function applyFilters() {
    const q = (searchInput?.value || '').trim().toLowerCase();
    const status = (statusSelect?.value || '').toLowerCase();
    const items = taskList.querySelectorAll('li[data-task-id]');
    items.forEach((li) => {
      const inTitle = (li.dataset.title || '').includes(q);
      const inDesc = (li.dataset.desc || '').includes(q);
      const matchesQuery = !q || inTitle || inDesc;
      const matchesStatus = !status || (li.dataset.status === status);
      li.style.display = (matchesQuery && matchesStatus) ? '' : 'none';
    });
  }

  searchInput?.addEventListener('input', applyFilters);
  statusSelect?.addEventListener('change', applyFilters);
}

function setupAsyncToggle() {
  const taskList = document.getElementById('task-list');
  if (!taskList) return;
  taskList.addEventListener('click', async (e) => {
    const anchor = e.target.closest('a.toggle-task');
    if (!anchor) return;
    e.preventDefault();
    const li = anchor.closest('li[data-task-id]');
    if (!li) return;
    const apiUrl = anchor.getAttribute('data-api-url');
    anchor.textContent = 'Working...';
    try {
      const res = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrfToken(),
          'X-Requested-With': 'XMLHttpRequest',
        },
      });
      const data = await res.json();
      if (data && data.ok) {
        li.dataset.status = data.completed ? 'completed' : 'pending';
        const statusSpan = li.querySelector('.task-status');
        if (statusSpan) {
          statusSpan.textContent = data.completed ? ' — ✅ Completed' : ' — ⏳ Pending';
        }
        anchor.textContent = data.completed ? 'Mark Incomplete' : 'Mark Complete';
      } else {
        anchor.textContent = 'Try Again';
      }
    } catch (err) {
      anchor.textContent = 'Error, retry?';
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  setupLiveSearchAndFilter();
  setupAsyncToggle();
});


