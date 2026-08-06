/* ==========================================================================
   Lucè Packaging — site script
   --------------------------------------------------------------------------
   Do NOT put contact details in this file. They live in config.py and are
   rendered into the page by build.py, which also hands the few values this
   script needs to `window.LUCE`. Edit config.py, then run:

       python build.py

   ========================================================================== */

// Injected by templates/base.html. The fallback only matters if this file is
// opened outside a built page.
const CONFIG = Object.assign(
  { whatsapp: '', email: '', company: 'Lucè Packaging', waValid: false },
  window.LUCE || {}
);

/* ========================================================================== */

(function () {
  'use strict';

  document.documentElement.classList.remove('no-js');

  const $  = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  /* ------------------------------------------------------------------- header
     Shadow once scrolled, and keep anchor jumps clear of the sticky bar.
     (The mobile drawer positions itself against the header in CSS, so there
     is no offset to track here.)                                          */
  function initHeader() {
    const head = $('#siteHead');
    if (!head) return;

    const setScrollPadding = () => {
      document.documentElement.style.scrollPaddingTop = `${head.offsetHeight + 18}px`;
    };
    setScrollPadding();
    window.addEventListener('resize', setScrollPadding, { passive: true });

    const onScroll = () => head.classList.toggle('is-stuck', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* --------------------------------------------------------------- mobile nav */
  function initNav() {
    const burger = $('#burger');
    const nav = $('#nav');
    if (!burger || !nav) return;

    const close = () => {
      nav.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Open menu');
      document.body.classList.remove('nav-open');
    };

    burger.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('nav-open', open);
    });

    // Tapping any nav link should close the drawer behind you.
    $$('a', nav).forEach(a => a.addEventListener('click', close));

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        close();
        burger.focus();
      }
    });

    // If the viewport grows back to desktop, drop the mobile state entirely.
    window.addEventListener('resize', () => {
      if (window.innerWidth > 940) close();
    }, { passive: true });
  }

  /* ------------------------------------------------------- active nav link */
  function initActiveLink() {
    const links = $$('.nav > a[href^="#"]:not(.btn)');
    if (!links.length || !('IntersectionObserver' in window)) return;

    const sections = links
      .map(a => ({ link: a, el: $(a.getAttribute('href')) }))
      .filter(pair => pair.el);

    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const match = sections.find(p => p.el === entry.target);
        if (!match) return;
        links.forEach(l => l.classList.remove('is-active'));
        match.link.classList.add('is-active');
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });

    sections.forEach(p => io.observe(p.el));
  }

  /* --------------------------------------------------------- scroll reveal */
  function initReveal() {
    const items = $$('.reveal');
    if (!items.length) return;

    // No observer support, or motion is unwelcome → just show everything.
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !('IntersectionObserver' in window)) {
      items.forEach(el => el.classList.add('is-in'));
      return;
    }

    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        obs.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });

    // Stagger siblings so grids cascade instead of popping in as one block.
    items.forEach(el => {
      const sibs = Array.from(el.parentElement ? el.parentElement.children : []);
      const i = sibs.indexOf(el);
      el.style.transitionDelay = `${Math.min(i, 6) * 70}ms`;
      io.observe(el);
    });
  }

  /* ------------------------------------------------------- counting numbers */
  function initCounters() {
    const nums = $$('[data-count]');
    if (!nums.length) return;

    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !('IntersectionObserver' in window)) return;

    const run = el => {
      const target = parseInt(el.dataset.count, 10);
      if (!Number.isFinite(target)) return;
      const duration = 1100;
      const start = performance.now();

      const tick = now => {
        const p = Math.min((now - start) / duration, 1);
        // ease-out so it decelerates into the final number
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = String(Math.round(target * eased));
        if (p < 1) requestAnimationFrame(tick);
        else el.textContent = String(target);
      };
      requestAnimationFrame(tick);
    };

    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        run(entry.target);
        obs.unobserve(entry.target);
      });
    }, { threshold: .6 });

    nums.forEach(el => io.observe(el));
  }

  /* ------------------------------------------------------------------- form */
  function initForm() {
    const form = $('#quoteForm');
    if (!form) return;

    const status = $('#formStatus');
    const required = ['qName', 'qPhone'];

    const showError = (id, msg) => {
      const input = $('#' + id);
      const slot = $(`[data-err-for="${id}"]`);
      if (!input) return;
      input.setAttribute('aria-invalid', msg ? 'true' : 'false');
      if (slot) slot.textContent = msg || '';
    };

    const validate = () => {
      let firstBad = null;

      const name = $('#qName');
      if (name && name.value.trim().length < 2) {
        showError('qName', 'Please enter your name.');
        firstBad = firstBad || name;
      } else {
        showError('qName', '');
      }

      const phone = $('#qPhone');
      if (phone) {
        const digits = phone.value.replace(/\D/g, '');
        if (digits.length < 8) {
          showError('qPhone', 'Enter a valid phone number so we can reply.');
          firstBad = firstBad || phone;
        } else {
          showError('qPhone', '');
        }
      }

      if (firstBad) {
        firstBad.focus();
        if (status) status.textContent = '';
        return false;
      }
      return true;
    };

    // Clear an error as soon as the field is being fixed.
    required.forEach(id => {
      const el = $('#' + id);
      if (el) el.addEventListener('input', () => showError(id, ''));
    });

    const val = id => {
      const el = $('#' + id);
      return el ? el.value.trim() : '';
    };

    /* Build a readable enquiry, skipping anything left blank. */
    const buildMessage = () => {
      const dims = [val('qL'), val('qB'), val('qH')].filter(Boolean).join(' × ');

      const rows = [
        ['Name',      val('qName')],
        ['Company',   val('qCompany')],
        ['Phone',     val('qPhone')],
        ['Product',   val('qProduct')],
        ['Box size',  dims],
        ['Quantity',  val('qQty')],
        ['Ply',       val('qPly')],
        ['Notes',     val('qMsg')]
      ].filter(([, v]) => v);

      const body = rows.map(([k, v]) => `${k}: ${v}`).join('\n');
      return `New packaging enquiry — ${CONFIG.company}\n\n${body}`;
    };

    const send = mode => {
      if (!validate()) return;
      const message = buildMessage();

      // No usable WhatsApp number configured — send by email rather than
      // opening a wa.me link that goes nowhere.
      if (mode === 'whatsapp' && !CONFIG.waValid) mode = 'email';

      if (mode === 'whatsapp') {
        const url = `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(message)}`;
        window.open(url, '_blank', 'noopener');
        if (status) status.textContent = 'Opening WhatsApp with your enquiry…';
      } else {
        const subject = `Packaging enquiry — ${val('qName')}`;
        const url = `mailto:${CONFIG.email}?subject=${encodeURIComponent(subject)}`
                  + `&body=${encodeURIComponent(message)}`;
        window.location.href = url;
        if (status) status.textContent = 'Opening your email app…';
      }
    };

    // Submit (and Enter in a text field) goes to WhatsApp.
    form.addEventListener('submit', e => {
      e.preventDefault();
      send('whatsapp');
    });

    const emailBtn = $('[data-send="email"]', form);
    if (emailBtn) emailBtn.addEventListener('click', () => send('email'));
  }

  /* ------------------------------------------------------------------- boot
     Contact details, the copyright year and the WhatsApp link fallback are all
     resolved by build.py at build time, so there is nothing to patch here. */
  function init() {
    initHeader();
    initNav();
    initActiveLink();
    initReveal();
    initCounters();
    initForm();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
