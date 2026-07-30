/* Lightweight client-side validation for the interest form. */
(() => {
  const form = document.querySelector('#form');
  const success = document.querySelector('.success');
  const rules = {
    name: (value) => value.trim().length > 1 || 'Enter your full name.',
    email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value) || 'Enter a valid email address.',
    branch: (value) => value || 'Select your branch.',
    year: (value) => value || 'Select your year.',
  };

  function validate(field) {
    if (!rules[field.name]) return true;

    const result = rules[field.name](field.value);
    const label = field.parentElement;
    label.classList.toggle('invalid', result !== true);
    label.querySelector('i').textContent = result === true ? '' : result;
    return result === true;
  }

  form.querySelectorAll('input, select').forEach((field) => {
    field.addEventListener('blur', () => validate(field));
    field.addEventListener('input', () => {
      if (field.parentElement.classList.contains('invalid')) validate(field);
    });
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const fields = [...form.querySelectorAll('input, select')];
    const isValid = fields.map(validate).every(Boolean);

    if (!isValid) {
      form.querySelector('.invalid input, .invalid select').focus();
      return;
    }

    form.hidden = true;
    success.hidden = false;
  });
})();
