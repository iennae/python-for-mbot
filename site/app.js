(function () {
  "use strict";

  const STORAGE_KEY = "ares_vii_mbot_mission_metrics_v1";
  const missions = Array.isArray(window.MISSIONS_DATA) ? window.MISSIONS_DATA : [];
  let activeMissionIndex = 0;
  let savedChecks = loadChecks();

  function loadChecks() {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (_err) {
      return {};
    }
  }

  function saveChecks() {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(savedChecks));
    } catch (_err) {
      // Ignore storage errors in restricted file:// contexts
    }
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatInlineMarkdown(text) {
    let html = escapeHtml(text);
    // Links: [label](url)
    html = html.replace(
      /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
    );
    // Bold: **text**
    html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    // Italic: *text*
    html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
    // Inline code: `code`
    html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
    return html;
  }

  function renderRichText(markdownText) {
    const lines = String(markdownText || "").split("\n");
    const out = [];
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
      const trimmed = lines[i].trim();
      if (!trimmed) {
        if (inList) {
          out.push("</ul>");
          inList = false;
        }
        continue;
      }
      if (trimmed.startsWith("- ") || /^\d+\.\s+/.test(trimmed)) {
        if (!inList) {
          out.push('<ul class="bullet-list">');
          inList = true;
        }
        const content = trimmed.replace(/^(-|\d+\.)\s+/, "");
        out.push("<li>" + formatInlineMarkdown(content) + "</li>");
      } else if (inList && (lines[i].startsWith("  ") || lines[i].startsWith("\t"))) {
        const prev = out.pop() || "<li></li>";
        out.push(
          prev.replace(/<\/li>$/, "<br>" + formatInlineMarkdown(trimmed) + "</li>")
        );
      } else {
        if (inList) {
          out.push("</ul>");
          inList = false;
        }
        out.push("<p>" + formatInlineMarkdown(trimmed) + "</p>");
      }
    }
    if (inList) {
      out.push("</ul>");
    }
    return out.join("\n");
  }

  function getMissionCompletion(mission) {
    const total = (mission.successMetrics || []).length;
    const checks = savedChecks[mission.id] || {};
    let done = 0;
    for (let i = 0; i < total; i++) {
      if (checks[i]) {
        done++;
      }
    }
    return { done: done, total: total, complete: total > 0 && done === total };
  }

  function updateOverallProgress() {
    let totalDone = 0;
    let totalMetrics = 0;
    missions.forEach(function (m) {
      const stats = getMissionCompletion(m);
      totalDone += stats.done;
      totalMetrics += stats.total;
    });
    const el = document.getElementById("overall-progress-badge");
    if (el) {
      el.textContent =
        "Telemetry Checkpoints: " + totalDone + " / " + totalMetrics + " Verified";
    }
  }

  function renderSidebar() {
    const listEl = document.getElementById("mission-nav-list");
    if (!listEl) return;
    listEl.innerHTML = "";

    missions.forEach(function (mission, idx) {
      const stats = getMissionCompletion(mission);
      const li = document.createElement("li");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.id = "nav-btn-" + mission.id;
      btn.className = "mission-nav-btn" + (idx === activeMissionIndex ? " active" : "");
      btn.innerHTML =
        '<div class="mission-nav-left">' +
        '<span class="mission-nav-num">MISSION ' +
        escapeHtml(mission.number) +
        "</span>" +
        '<span class="mission-nav-title">' +
        escapeHtml(mission.title) +
        "</span>" +
        "</div>" +
        '<span class="mission-nav-status' +
        (stats.complete ? " complete" : "") +
        '">' +
        (stats.complete ? "✓ CLEAR" : stats.done + "/" + stats.total) +
        "</span>";

      btn.addEventListener("click", function () {
        activeMissionIndex = idx;
        renderAll();
        window.scrollTo({ top: 0, behavior: "smooth" });
      });

      li.appendChild(btn);
      listEl.appendChild(li);
    });
  }

  function copyTextToClipboard(text, buttonEl) {
    const showCopied = function () {
      const original = buttonEl.textContent;
      buttonEl.textContent = "✓ Copied to Clipboard";
      setTimeout(function () {
        buttonEl.textContent = original;
      }, 1800);
    };

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(showCopied).catch(function () {
        fallbackCopy(text, showCopied);
      });
    } else {
      fallbackCopy(text, showCopied);
    }
  }

  function fallbackCopy(text, callback) {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand("copy");
      callback();
    } catch (_err) {
      // Ignore
    }
    document.body.removeChild(ta);
  }

  function renderActiveMission() {
    const container = document.getElementById("mission-stage-container");
    if (!container || !missions.length) return;

    const mission = missions[activeMissionIndex];
    const stats = getMissionCompletion(mission);
    const powerTag = mission.requiresBattery
      ? '<span class="tag tag-battery">⚡ Requires Battery Switch ON + USB Cable</span>'
      : '<span class="tag tag-usb">🔌 Works on USB Cable Power</span>';

    const objectivesHtml = (mission.objectives || [])
      .map(function (item) {
        return "<li>" + formatInlineMarkdown(item) + "</li>";
      })
      .join("");

    const systemsHtml = (mission.systemsCheck || [])
      .map(function (item) {
        return "<li>" + formatInlineMarkdown(item) + "</li>";
      })
      .join("");

    let starterCodeSection = "";
    if (mission.starterCode) {
      starterCodeSection =
        '<div class="code-header">' +
        '<span class="code-filename">💻 Starter Bootstrap Template: ' +
        escapeHtml(mission.scriptPath || mission.scriptName) +
        "</span>" +
        '<button type="button" id="copy-starter-btn" class="btn-secondary">Copy Starter Template</button>' +
        "</div>" +
        '<pre class="code-block" id="starter-code-pre">' +
        escapeHtml(mission.starterCode) +
        "</pre>";
    }

    const hintsHtml = (mission.hints || [])
      .map(function (hint, hIdx) {
        const parts = hint.split(":");
        const summaryLabel =
          parts.length > 1 ? parts[0] : "Hint #" + (hIdx + 1);
        const bodyText =
          parts.length > 1 ? parts.slice(1).join(":").trim() : hint;
        return (
          '<details class="hint-item" id="hint-' +
          mission.id +
          "-" +
          hIdx +
          '">' +
          "<summary>💡 " +
          formatInlineMarkdown(summaryLabel) +
          "</summary>" +
          '<div class="hint-body">' +
          formatInlineMarkdown(bodyText) +
          "</div>" +
          "</details>"
        );
      })
      .join("");

    const missionChecks = savedChecks[mission.id] || {};
    const metricsHtml = (mission.successMetrics || [])
      .map(function (metric, mIdx) {
        const isChecked = Boolean(missionChecks[mIdx]);
        return (
          '<label class="metric-item' +
          (isChecked ? " checked" : "") +
          '" for="metric-' +
          mission.id +
          "-" +
          mIdx +
          '">' +
          '<input type="checkbox" id="metric-' +
          mission.id +
          "-" +
          mIdx +
          '" data-metric-idx="' +
          mIdx +
          '"' +
          (isChecked ? " checked" : "") +
          ">" +
          '<span class="metric-label">' +
          formatInlineMarkdown(metric) +
          "</span>" +
          "</label>"
        );
      })
      .join("");

    const hasNext = activeMissionIndex < missions.length - 1;
    const completeBannerHtml = stats.complete
      ? '<div class="mission-complete-banner">' +
        "<span>🟢 All Mission " +
        escapeHtml(mission.number) +
        " Success Metrics Verified! Ready for next deployment.</span>" +
        (hasNext
          ? '<button type="button" id="next-mission-btn" class="btn-primary">Advance to Mission ' +
            escapeHtml(missions[activeMissionIndex + 1].number) +
            " →</button>"
          : "") +
        "</div>"
      : "";

    const debriefRowsHtml = (mission.debrief || [])
      .map(function (row) {
        return (
          "<tr>" +
          "<td><code>" +
          escapeHtml(row.command) +
          "</code></td>" +
          "<td>" +
          formatInlineMarkdown(row.translation) +
          "</td>" +
          "</tr>"
        );
      })
      .join("");

    container.innerHTML =
      '<section class="card">' +
      '<div class="mission-header-meta">' +
      '<span class="tag">🛰️ ' +
      escapeHtml(mission.badge) +
      "</span>" +
      powerTag +
      "</div>" +
      '<h2 class="mission-title">' +
      escapeHtml(mission.fullTitle) +
      "</h2>" +
      '<div class="story-box">' +
      formatInlineMarkdown(mission.story) +
      "</div>" +
      "</section>" +
      '<div class="grid-two">' +
      '<section class="card">' +
      '<h3 class="section-title">🎯 Primary Objectives</h3>' +
      '<ul class="bullet-list">' +
      objectivesHtml +
      "</ul>" +
      "</section>" +
      '<section class="card">' +
      '<h3 class="section-title">⚙️ Systems Check & Engineering Tools</h3>' +
      '<ul class="bullet-list">' +
      systemsHtml +
      "</ul>" +
      "</section>" +
      "</div>" +
      '<section class="card">' +
      '<h3 class="section-title">🚀 Field Challenge & Starter Template</h3>' +
      '<div class="challenge-prose">' +
      renderRichText(mission.challenge) +
      "</div>" +
      starterCodeSection +
      "</section>" +
      '<section class="card">' +
      '<h3 class="section-title">💡 Progressive Field Hints <span>(Click to expand if stuck)</span></h3>' +
      '<div class="hints-list">' +
      hintsHtml +
      "</div>" +
      "</section>" +
      '<section class="card">' +
      '<h3 class="section-title">✅ Mission Success Metrics <span>(' +
      stats.done +
      " / " +
      stats.total +
      " Verified)</span></h3>" +
      '<div class="metrics-list" id="metrics-list-container">' +
      metricsHtml +
      "</div>" +
      completeBannerHtml +
      "</section>" +
      '<section class="card">' +
      '<h3 class="section-title">🧠 Flight Engineer Debrief: What Just Happened?</h3>' +
      '<div class="debrief-table-wrap">' +
      '<table class="debrief-table">' +
      "<thead><tr><th>Code / Component</th><th>Real-World Translation</th></tr></thead>" +
      "<tbody>" +
      debriefRowsHtml +
      "</tbody>" +
      "</table>" +
      "</div>" +
      "</section>";

    const copyBtn = document.getElementById("copy-starter-btn");
    if (copyBtn && mission.starterCode) {
      copyBtn.addEventListener("click", function () {
        copyTextToClipboard(mission.starterCode, copyBtn);
      });
    }

    const checkboxes = container.querySelectorAll("input[data-metric-idx]");
    checkboxes.forEach(function (cb) {
      cb.addEventListener("change", function (e) {
        const idx = Number(e.target.getAttribute("data-metric-idx"));
        if (!savedChecks[mission.id]) {
          savedChecks[mission.id] = {};
        }
        savedChecks[mission.id][idx] = Boolean(e.target.checked);
        saveChecks();
        renderAll();
      });
    });

    const nextBtn = document.getElementById("next-mission-btn");
    if (nextBtn && hasNext) {
      nextBtn.addEventListener("click", function () {
        activeMissionIndex++;
        renderAll();
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    }
  }

  function renderAll() {
    updateOverallProgress();
    renderSidebar();
    renderActiveMission();
  }

  function setupModal() {
    const openBtn = document.getElementById("open-add-mission-modal-btn");
    const closeBtn = document.getElementById("close-add-mission-modal-btn");
    const modal = document.getElementById("add-mission-modal");
    if (!openBtn || !closeBtn || !modal) return;

    openBtn.addEventListener("click", function () {
      modal.removeAttribute("hidden");
    });
    closeBtn.addEventListener("click", function () {
      modal.setAttribute("hidden", "true");
    });
    modal.addEventListener("click", function (e) {
      if (e.target === modal) {
        modal.setAttribute("hidden", "true");
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    setupModal();
    renderAll();
  });
})();
