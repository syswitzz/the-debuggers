/* Lightweight client-side validation and fetch submission for the registration form. */
(() => {
  const form = document.querySelector('#form');
  const success = document.querySelector('.success');
  const note = form.querySelector('.note');
  const submitBtn = form.querySelector('button[type="submit"]');

  const ALLOWED_BRANCHES = new Set(['CSE','EEE','ME','CE','B.ARCH','MNC']);
  const ALLOWED_YEARS = new Set(['1st Year','2nd Year','3rd Year','4th Year']);

  const rules = {
    name: (value) => value.trim().length > 1 || 'Enter your full name.',
    email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value) || 'Enter a valid email address.',
    phone: (value) => {
      const v = value.replace(/\s|-/g, '');
      return /^(?:\+91|0)?[6-9]\d{9}$/.test(v) || 'Enter a valid Indian mobile number (e.g. +91 9876543210).';
    },
    studentId: (value) =>
      /^(\d{11}|\d{2}\/[A-Z]{2,10}\/\d{1,4})$/.test(value.trim()) ||
      'Use an 11-digit registration ID or YY/BRANCH/ROLL (e.g. 25/CSE/68).',
    branch: () => true,
    year: () => true,
  };

  function clearErrors() {
    form.querySelectorAll('label.invalid').forEach((l) => l.classList.remove('invalid'));
    form.querySelectorAll('label i').forEach((i) => (i.textContent = ''));
    if (note) note.textContent = 'We will only use this to contact you about The Debuggers.';
  }

  function validate(field) {
    if (!rules[field.name]) return true;

    if (field.name === 'studentId') {
      field.value = field.value.toUpperCase().replace(/\s/g, '');
    }

    if (field.name === 'branch') {
      // normalize select value to expected casing
      field.value = String(field.value || '').trim();
    }

    const result = rules[field.name](field.value);
    const label = field.parentElement;
    label.classList.toggle('invalid', result !== true);
    const info = label.querySelector('i');
    if (info) info.textContent = result === true ? '' : result;
    return result === true;
  }

  form.querySelectorAll('input, select, textarea').forEach((field) => {
    field.addEventListener('blur', () => validate(field));
    field.addEventListener('input', () => {
      if (field.parentElement.classList.contains('invalid')) validate(field);
    });
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearErrors();

    const fields = [...form.querySelectorAll('input, select, textarea')];
    const isValid = fields.map(validate).every(Boolean);

    if (!isValid) {
      const firstInvalid = form.querySelector('.invalid input, .invalid select, .invalid textarea');
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    const payload = {
      name: (form.elements.name && form.elements.name.value || '').trim(),
      email: (form.elements.email && form.elements.email.value || '').trim(),
      phone: (form.elements.phone && form.elements.phone.value || '').trim(),
      studentId: (form.elements.studentId && form.elements.studentId.value || '').trim(),
      branch: (form.elements.branch && form.elements.branch.value || '').trim(),
      year: (form.elements.year && form.elements.year.value || '').trim(),
      interest: (form.elements.interest && form.elements.interest.value || '').trim(),
    };

    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending…';

    try {
      const API_BASE =
        window.location.hostname === 'localhost'
          ? 'http://localhost:8000'
          : 'https://api.sayam.eu.org';

      const resp = await fetch(`${API_BASE}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (resp.ok) {
        form.hidden = true;
        success.hidden = false;
        return;
      }

      const data = await resp.json().catch(() => null);

      if (data && data.detail) {
        // Handle Pydantic style errors (array) or string details
        if (Array.isArray(data.detail)) {
          data.detail.forEach((err) => {
            const loc = Array.isArray(err.loc) ? err.loc : [];
            const fieldName = loc.length ? loc[loc.length - 1] : null;
            if (fieldName && form.elements[fieldName]) {
              const fld = form.elements[fieldName];
              const label = fld.parentElement;
              label.classList.add('invalid');
              const info = label.querySelector('i');
              if (info) info.textContent = err.msg || JSON.stringify(err);
            }
          });
          if (note) note.textContent = 'Please correct the highlighted fields.';
        } else if (typeof data.detail === 'string') {
          if (resp.status === 409) {
            if (note) note.textContent = data.detail;
          } else {
            if (note) note.textContent = data.detail;
          }
        }
      } else {
        if (note) note.textContent = 'Registration failed. Please try again.';
      }
    } catch (err) {
      if (note) note.textContent = 'Network error. Check your connection and try again.';
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Connect with the club →';
    }
  });
})();
