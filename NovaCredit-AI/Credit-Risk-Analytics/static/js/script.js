/* =========================================================
   Global UI behaviour: theme toggle, sidebar, multi-step form
   ========================================================= */

// ---------- Theme (dark/light) with localStorage ----------
(function initTheme() {
  const saved = localStorage.getItem("crs-theme") || "dark";
  document.documentElement.setAttribute("data-theme", saved);
})();

function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  html.setAttribute("data-theme", next);
  localStorage.setItem("crs-theme", next);
  const icon = document.getElementById("theme-icon");
  if (icon) icon.textContent = next === "dark" ? "🌙" : "☀️";
}

document.addEventListener("DOMContentLoaded", () => {
  const icon = document.getElementById("theme-icon");
  if (icon) {
    icon.textContent = document.documentElement.getAttribute("data-theme") === "dark" ? "🌙" : "☀️";
  }

  initSidebarToggle();
  initAnimatedCounters();
  initMultiStepForm();
  initHistoryToolbar();
});

// ---------- Mobile sidebar ----------
function initSidebarToggle() {
  const btn = document.getElementById("hamburger-btn");
  const sidebar = document.getElementById("sidebar");
  if (!btn || !sidebar) return;
  btn.addEventListener("click", () => sidebar.classList.toggle("open"));
  document.addEventListener("click", (e) => {
    if (!sidebar.contains(e.target) && !btn.contains(e.target)) {
      sidebar.classList.remove("open");
    }
  });
}

// ---------- Animated stat counters ----------
function initAnimatedCounters() {
  const counters = document.querySelectorAll("[data-counter]");
  counters.forEach((el) => {
    const target = parseFloat(el.getAttribute("data-counter"));
    const duration = 1200;
    const start = performance.now();
    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const value = target * progress;
      el.textContent = Number.isInteger(target) ? Math.floor(value).toLocaleString() : value.toFixed(1);
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString();
    }
    requestAnimationFrame(step);
  });
}

// ---------- Multi-step prediction form ----------
function initMultiStepForm() {
  const form = document.getElementById("predict-form");
  if (!form) return;

  const steps = Array.from(form.querySelectorAll(".form-step"));
  const dots = Array.from(document.querySelectorAll(".step-dot"));
  let currentStep = 0;

  // IMPORTANT: browsers validate ALL "required" fields on submit, even ones
  // hidden on inactive steps (display:none), which silently blocks the form
  // with no visible error. We fix this by toggling the `required` attribute
  // on/off as steps change, so only the visible step's fields are required
  // at any given time.
  function syncRequiredAttributes(activeIndex) {
    steps.forEach((step, i) => {
      step.querySelectorAll("input, select").forEach((field) => {
        if (field.dataset.required === "true") {
          field.required = i === activeIndex;
        }
      });
    });
  }

  // Mark which fields were originally required, before we start toggling.
  steps.forEach((step) => {
    step.querySelectorAll("input[required], select[required]").forEach((field) => {
      field.dataset.required = "true";
    });
  });

  function showStep(index) {
    steps.forEach((s, i) => s.classList.toggle("active", i === index));
    dots.forEach((d, i) => {
      d.classList.toggle("active", i === index);
      d.classList.toggle("done", i < index);
    });
    currentStep = index;
    syncRequiredAttributes(index);
    window.scrollTo({ top: form.offsetTop - 100, behavior: "smooth" });
  }

  function validateStep(index) {
    const fields = steps[index].querySelectorAll("input[data-required='true'], select[data-required='true']");
    let valid = true;
    fields.forEach((field) => {
      const errorEl = field.parentElement.querySelector(".error-msg");
      const value = (field.value || "").trim();
      if (!value) {
        field.classList.add("invalid");
        if (errorEl) errorEl.textContent = "This field is required.";
        valid = false;
      } else if (field.type === "number" && isNaN(Number(value))) {
        field.classList.add("invalid");
        if (errorEl) errorEl.textContent = "Must be a valid number.";
        valid = false;
      } else if (field.min !== "" && field.min !== undefined && Number(value) < Number(field.min)) {
        field.classList.add("invalid");
        if (errorEl) errorEl.textContent = `Minimum value is ${field.min}.`;
        valid = false;
      } else {
        field.classList.remove("invalid");
        if (errorEl) errorEl.textContent = "";
      }
    });
    return valid;
  }

  form.querySelectorAll(".btn-next").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (validateStep(currentStep) && currentStep < steps.length - 1) {
        showStep(currentStep + 1);
      }
    });
  });

  form.querySelectorAll(".btn-prev").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (currentStep > 0) showStep(currentStep - 1);
    });
  });

  form.addEventListener("submit", (e) => {
    try {
      if (!validateStep(currentStep)) {
        e.preventDefault();
        showFormAlert(form, "Please fix the highlighted fields before submitting.");
        return;
      }
      const overlay = document.getElementById("loading-overlay");
      if (overlay) overlay.classList.add("active");
      // let the form submit normally (do NOT preventDefault here)
    } catch (err) {
      // Never let a JS error silently swallow the submit click.
      console.error("Prediction form error:", err);
      e.preventDefault();
      showFormAlert(form, "Something went wrong while submitting. Please try again.");
    }
  });

  showStep(0);
}

function showFormAlert(form, message) {
  let alertEl = form.querySelector(".form-alert");
  if (!alertEl) {
    alertEl = document.createElement("div");
    alertEl.className = "flash error form-alert";
    form.prepend(alertEl);
  }
  alertEl.textContent = message;
  alertEl.scrollIntoView({ behavior: "smooth", block: "center" });
}

// ---------- History page toolbar (debounced search auto-submit) ----------
function initHistoryToolbar() {
  const searchInput = document.getElementById("search-input");
  const filterForm = document.getElementById("filter-form");
  if (!searchInput || !filterForm) return;

  let timeout;
  searchInput.addEventListener("input", () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => filterForm.submit(), 500);
  });

  document.querySelectorAll("[data-auto-submit]").forEach((el) => {
    el.addEventListener("change", () => filterForm.submit());
  });
}

// ---------- Delete confirmation ----------
function confirmDelete(formId) {
  if (confirm("Are you sure you want to delete this record? This cannot be undone.")) {
    document.getElementById(formId).submit();
  }
}
