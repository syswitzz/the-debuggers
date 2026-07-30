/* Home page interactions. */
(() => {
  const select = (selector) => document.querySelector(selector);
  const selectAll = (selector) => [...document.querySelectorAll(selector)];

  const header = select('.site-header');
  const menu = select('.nav-menu');
  const menuToggle = select('.menu-toggle');

  addEventListener('load', () => select('.loader').classList.add('done'));

  menuToggle.addEventListener('click', () => {
    const isOpen = menu.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', isOpen);
  });

  selectAll('.nav-menu a').forEach((link) => {
    link.addEventListener('click', () => menu.classList.remove('open'));
  });

  addEventListener(
    'scroll',
    () => header.classList.toggle('scrolled', scrollY > 18),
    { passive: true },
  );

  const glow = select('.cursor-glow');
  addEventListener(
    'pointermove',
    (event) => {
      glow.style.left = `${event.clientX}px`;
      glow.style.top = `${event.clientY}px`;
    },
    { passive: true },
  );

  const phrases = ['learn the basics.', 'ask better questions.', 'build with confidence.'];
  let phraseIndex = 0;
  let characterIndex = 0;
  let isDeleting = false;

  function typeHeroLine() {
    const phrase = phrases[phraseIndex];
    select('#hero-typing').textContent = phrase.slice(0, characterIndex);
    characterIndex += isDeleting ? -1 : 1;

    let delay = isDeleting ? 30 : 55;
    if (!isDeleting && characterIndex > phrase.length) {
      isDeleting = true;
      delay = 1350;
    }
    if (isDeleting && characterIndex < 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      characterIndex = 0;
      delay = 220;
    }
    setTimeout(typeHeroLine, delay);
  }

  const terminalSteps = [
    ['echo "hello, GCE Gaya"', 'A place to start learning.'],
    ['open monthly-session', 'Seminars and workshops, every month.'],
    ['npm run grow', '✓ Learning together.'],
  ];
  let terminalIndex = 0;

  function playTerminal() {
    const [command, output] = terminalSteps[terminalIndex];
    const commandElement = select('#terminal-command');
    const outputElement = select('#terminal-output');
    let index = 0;

    commandElement.textContent = '';
    outputElement.textContent = '';

    function typeCommand() {
      commandElement.textContent = command.slice(0, index++);
      if (index <= command.length) {
        setTimeout(typeCommand, 42);
        return;
      }
      setTimeout(() => {
        outputElement.textContent = output;
        terminalIndex = (terminalIndex + 1) % terminalSteps.length;
        setTimeout(playTerminal, 2200);
      }, 400);
    }

    typeCommand();
  }

  typeHeroLine();
  playTerminal();

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('show');
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.14 },
  );

  selectAll('.reveal').forEach((element) => observer.observe(element));

  selectAll('.ripple').forEach((button) => {
    button.addEventListener('click', (event) => {
      const ripple = document.createElement('i');
      const bounds = button.getBoundingClientRect();
      ripple.className = 'ripple-effect';
      ripple.style.left = `${event.clientX - bounds.left}px`;
      ripple.style.top = `${event.clientY - bounds.top}px`;
      button.append(ripple);
      setTimeout(() => ripple.remove(), 650);
    });
  });
})();
