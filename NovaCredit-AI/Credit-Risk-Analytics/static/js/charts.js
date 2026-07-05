/* =========================================================
   Chart.js helpers + custom canvas risk gauge
   ========================================================= */

const CRS_PALETTE = ["#8b5cf6", "#06b6d4", "#ec4899", "#3b82f6", "#f97316", "#34d399", "#facc15", "#c084fc"];

function crsThemeColors() {
  const isDark = document.documentElement.getAttribute("data-theme") !== "light";
  return {
    text: isDark ? "#b7b3d9" : "#5b5780",
    grid: isDark ? "rgba(255,255,255,0.08)" : "rgba(30,20,70,0.08)",
  };
}

Chart.defaults.font.family = "'Inter', sans-serif";

function crsChart(canvasId, type, labels, datasets, extraOptions = {}) {
  const el = document.getElementById(canvasId);
  if (!el) return null;
  const colors = crsThemeColors();
  const ctx2d = el.getContext("2d");

  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 900, easing: "easeOutQuart" },
    plugins: {
      legend: { labels: { color: colors.text }, position: "bottom" },
      tooltip: { backgroundColor: "#1c1a3a", padding: 10, cornerRadius: 8 },
    },
    scales: type === "pie" || type === "doughnut" ? {} : {
      x: { ticks: { color: colors.text }, grid: { color: colors.grid } },
      y: { ticks: { color: colors.text }, grid: { color: colors.grid } },
    },
  };

  return new Chart(ctx2d, {
    type,
    data: {
      labels,
      datasets: datasets.map((ds, i) => {
        let bg = ds.backgroundColor || (type === "line" ? undefined : CRS_PALETTE);
        if (type === "line" && !ds.backgroundColor) {
          const gradient = ctx2d.createLinearGradient(0, 0, 0, 260);
          gradient.addColorStop(0, "rgba(139, 92, 246, 0.35)");
          gradient.addColorStop(1, "rgba(139, 92, 246, 0.0)");
          bg = gradient;
        }
        return {
          backgroundColor: bg,
          borderColor: ds.borderColor || CRS_PALETTE[i % CRS_PALETTE.length],
          borderWidth: ds.borderWidth ?? 2.5,
          borderRadius: type === "bar" ? 8 : 0,
          pointRadius: type === "line" ? 3 : undefined,
          pointBackgroundColor: type === "line" ? "#8b5cf6" : undefined,
          tension: 0.4,
          fill: type === "line",
          ...ds,
        };
      }),
    },
    options: { ...baseOptions, ...extraOptions },
  });
}

/* ---------- Donut chart with side legend + center total (like reference "Threats By Virus") ---------- */
function crsDonutWithLegend(canvasId, legendId, centerId, labels, values, colors, centerLabel) {
  const canvasEl = document.getElementById(canvasId);
  const legendEl = document.getElementById(legendId);
  const centerEl = document.getElementById(centerId);
  if (!canvasEl) return null;

  const palette = colors && colors.length ? colors : CRS_PALETTE;
  const total = values.reduce((a, b) => a + b, 0);
  const topValue = total ? Math.round((values[0] / total) * 100) : 0;

  if (legendEl) {
    legendEl.innerHTML = labels.map((label, i) => `
      <div class="legend-item">
        <span class="legend-dot" style="background:${palette[i % palette.length]}"></span>
        <span>${label}</span>
      </div>
    `).join("");
  }

  if (centerEl) {
    centerEl.innerHTML = `
      <span class="total-label">${centerLabel || "Total"}</span>
      <span class="total-value">${topValue}%</span>
    `;
  }

  return new Chart(canvasEl.getContext("2d"), {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: palette,
        borderWidth: 0,
        cutout: "72%",
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 900, easing: "easeOutQuart" },
      plugins: { legend: { display: false }, tooltip: { backgroundColor: "#1c1a3a", padding: 10, cornerRadius: 8 } },
    },
  });
}

/* ---------- Custom semi-circle risk gauge (canvas 2D) ---------- */
function drawRiskGauge(canvasId, probability, isHighRisk) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width, h = canvas.height;
  const cx = w / 2, cy = h - 10, radius = Math.min(w, h * 2) / 2 - 10;

  ctx.clearRect(0, 0, w, h);

  // Background arc
  ctx.beginPath();
  ctx.arc(cx, cy, radius, Math.PI, 2 * Math.PI);
  ctx.lineWidth = 18;
  ctx.strokeStyle = "rgba(255,255,255,0.1)";
  ctx.lineCap = "round";
  ctx.stroke();

  // Gradient value arc
  const gradient = ctx.createLinearGradient(0, 0, w, 0);
  if (isHighRisk) {
    gradient.addColorStop(0, "#fbbf24");
    gradient.addColorStop(1, "#f87171");
  } else {
    gradient.addColorStop(0, "#3ddcff");
    gradient.addColorStop(1, "#34d399");
  }

  const endAngle = Math.PI + (Math.PI * (probability / 100));
  let progress = 0;
  const target = endAngle;
  const start = Math.PI;

  function animate() {
    progress += 0.03;
    const current = start + (target - start) * Math.min(progress, 1);
    ctx.clearRect(0, 0, w, h);
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI, 2 * Math.PI);
    ctx.lineWidth = 18;
    ctx.strokeStyle = "rgba(255,255,255,0.1)";
    ctx.lineCap = "round";
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(cx, cy, radius, start, current);
    ctx.lineWidth = 18;
    ctx.strokeStyle = gradient;
    ctx.lineCap = "round";
    ctx.stroke();

    if (progress < 1) requestAnimationFrame(animate);
  }
  animate();
}
