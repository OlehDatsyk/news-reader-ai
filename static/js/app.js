/* ==========================================================================
   AI News Assistant - Frontend logic
   No build step, no frameworks: plain JS talking to the Flask API.
   ========================================================================== */

(() => {
  "use strict";

  // ---- Element references ----
  const sidebar = document.getElementById("sidebar");
  const sidebarOverlay = document.getElementById("sidebarOverlay");
  const openSidebarBtn = document.getElementById("openSidebarBtn");
  const closeSidebarBtn = document.getElementById("closeSidebarBtn");

  const searchForm = document.getElementById("searchForm");
  const searchInput = document.getElementById("searchInput");
  const categoryChips = document.getElementById("categoryChips");
  const resultsList = document.getElementById("resultsList");
  const resultsLabel = document.getElementById("resultsLabel");

  const compareBar = document.getElementById("compareBar");
  const compareCount = document.getElementById("compareCount");
  const compareBtn = document.getElementById("compareBtn");

  const chatWindow = document.getElementById("chatWindow");
  const welcome = document.getElementById("welcome");
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendBtn");
  const suggestedPromptsEl = document.getElementById("suggestedPrompts");
  const resetBtn = document.getElementById("resetBtn");

  // ---- State ----
  let articles = [];               // articles currently shown in the sidebar
  const selectedForCompare = new Set();

  // ---- Markdown rendering (falls back to escaped text if marked.js fails to load) ----
  function renderMarkdown(text) {
    try {
      if (window.marked) return window.marked.parse(text);
    } catch (e) {
      /* fall through */
    }
    return escapeHtml(text).replace(/\n/g, "<br>");
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // ==========================================================================
  // Sidebar (mobile) open/close
  // ==========================================================================

  function openSidebar() {
    sidebar.classList.add("open");
    sidebarOverlay.classList.add("open");
  }

  function closeSidebar() {
    sidebar.classList.remove("open");
    sidebarOverlay.classList.remove("open");
  }

  openSidebarBtn?.addEventListener("click", openSidebar);
  closeSidebarBtn?.addEventListener("click", closeSidebar);
  sidebarOverlay?.addEventListener("click", closeSidebar);

  // ==========================================================================
  // Search & headlines
  // ==========================================================================

  searchForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;
    setActiveChip(null);
    runSearch({ query, mode: "search" });
  });

  categoryChips.addEventListener("click", (e) => {
    const btn = e.target.closest(".chip");
    if (!btn) return;
    searchInput.value = "";
    setActiveChip(btn);
    runSearch({ category: btn.dataset.category, mode: "headlines" });
  });

  function setActiveChip(activeBtn) {
    document.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
    if (activeBtn) activeBtn.classList.add("active");
  }

  async function runSearch(payload) {
    resultsList.innerHTML = `<div class="results-loading">Searching...</div>`;
    resultsLabel.textContent = "Searching...";
    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Search failed.");

      articles = data.articles || [];
      selectedForCompare.clear();
      updateCompareBar();
      renderResults();
      resultsLabel.textContent = articles.length
        ? `${articles.length} article${articles.length === 1 ? "" : "s"} found`
        : "No articles found";
      renderSuggestedPrompts();

      // Close sidebar automatically on mobile after a search
      if (window.innerWidth <= 900) closeSidebar();
    } catch (err) {
      resultsList.innerHTML = "";
      resultsLabel.textContent = "Search failed";
      addMessage("assistant", `⚠️ ${err.message}`, true);
    }
  }

  function renderResults() {
    resultsList.innerHTML = "";
    articles.forEach((article) => {
      resultsList.appendChild(buildArticleCard(article));
    });
  }

  function buildArticleCard(article) {
    const card = document.createElement("div");
    card.className = "article-card";

    const img = article.urlToImage
      ? `<img src="${escapeHtml(article.urlToImage)}" alt="" loading="lazy" onerror="this.style.display='none'">`
      : "";

    const published = article.publishedAt ? new Date(article.publishedAt).toLocaleDateString() : "";

    card.innerHTML = `
      ${img}
      <a class="title" href="${escapeHtml(article.url)}" target="_blank" rel="noopener">
        ${escapeHtml(article.title)}
      </a>
      <div class="meta">${escapeHtml(article.source)}${published ? " • " + published : ""}</div>
      <div class="desc">${escapeHtml(article.description || "No description available.")}</div>
      <div class="article-actions">
        <button class="action-btn" data-action="summarize">📝 Summarize</button>
        <button class="action-btn" data-action="explain">💡 Explain</button>
        <button class="action-btn" data-action="sentiment">📊 Sentiment</button>
        <label class="compare-label">
          <input type="checkbox" class="compare-checkbox" />
          Compare
        </label>
      </div>
    `;

    card.querySelectorAll(".action-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        sendAction(btn.dataset.action, article.id);
      });
    });

    const checkbox = card.querySelector(".compare-checkbox");
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) {
        if (selectedForCompare.size >= 2) {
          checkbox.checked = false;
          return;
        }
        selectedForCompare.add(article.id);
      } else {
        selectedForCompare.delete(article.id);
      }
      updateCompareBar();
    });

    return card;
  }

  function updateCompareBar() {
    const n = selectedForCompare.size;
    compareCount.textContent = `${n} selected`;
    compareBtn.disabled = n !== 2;
    compareBar.classList.toggle("hidden", articles.length === 0);
  }

  compareBtn.addEventListener("click", () => {
    const [idA, idB] = Array.from(selectedForCompare);
    if (idA === undefined || idB === undefined) return;
    sendAction("compare", idA, idB);
  });

  // ==========================================================================
  // Chat
  // ==========================================================================

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;
    chatInput.value = "";
    autoResize();
    sendChat(text);
  });

  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chatForm.requestSubmit();
    }
  });

  chatInput.addEventListener("input", autoResize);
  function autoResize() {
    chatInput.style.height = "auto";
    chatInput.style.height = Math.min(chatInput.scrollHeight, 140) + "px";
  }

  async function sendChat(message) {
    hideWelcome();
    addMessage("user", message);
    const typingEl = showTyping();
    setSending(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "chat", message }),
      });
      const data = await res.json();
      removeTyping(typingEl);
      if (!res.ok) throw new Error(data.error || "Something went wrong.");
      addMessage("assistant", data.reply);
    } catch (err) {
      removeTyping(typingEl);
      addMessage("assistant", `⚠️ ${err.message}`, true);
    } finally {
      setSending(false);
    }
  }

  async function sendAction(action, articleId, articleId2) {
    hideWelcome();
    const article = articles.find((a) => a.id === articleId);
    const labelMap = {
      summarize: `📝 Summarize: "${article?.title ?? ""}"`,
      explain: `💡 Explain: "${article?.title ?? ""}"`,
      sentiment: `📊 Sentiment of: "${article?.title ?? ""}"`,
      compare: `⚖️ Compare 2 selected articles`,
    };
    addMessage("user", labelMap[action] || action);

    const typingEl = showTyping();
    setSending(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action,
          article_id: articleId,
          article_id_2: articleId2,
        }),
      });
      const data = await res.json();
      removeTyping(typingEl);
      if (!res.ok) throw new Error(data.error || "Something went wrong.");
      addMessage("assistant", data.reply);
    } catch (err) {
      removeTyping(typingEl);
      addMessage("assistant", `⚠️ ${err.message}`, true);
    } finally {
      setSending(false);
    }
  }

  function setSending(isSending) {
    sendBtn.disabled = isSending;
  }

  function hideWelcome() {
    if (welcome) welcome.style.display = "none";
  }

  function addMessage(role, content, isError = false) {
    const msg = document.createElement("div");
    msg.className = `msg ${role}${isError ? " error" : ""}`;

    const avatar = role === "user" ? "🧑" : "🤖";
    const time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    msg.innerHTML = `
      <div class="avatar">${avatar}</div>
      <div class="bubble-wrap">
        <div class="bubble">${role === "user" ? escapeHtml(content) : renderMarkdown(content)}</div>
        <div class="timestamp">${time}</div>
      </div>
    `;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return msg;
  }

  function showTyping() {
    const msg = document.createElement("div");
    msg.className = "msg assistant";
    msg.innerHTML = `
      <div class="avatar">🤖</div>
      <div class="bubble-wrap">
        <div class="bubble typing"><span></span><span></span><span></span></div>
      </div>
    `;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return msg;
  }

  function removeTyping(el) {
    el?.remove();
  }

  // ==========================================================================
  // Suggested prompts
  // ==========================================================================

  const DEFAULT_PROMPTS = [
    "What's happening in the world today?",
    "Explain a recent tech trend to me simply",
    "What should I search for to learn about climate news?",
  ];

  function renderSuggestedPrompts() {
    suggestedPromptsEl.innerHTML = "";
    const prompts = [...DEFAULT_PROMPTS];

    if (articles.length > 0) {
      const first = articles[0];
      prompts.unshift(`Summarize "${truncate(first.title, 40)}"`);
      prompts.unshift(`What's the sentiment of the top article?`);
      if (articles.length > 1) {
        prompts.unshift(`Compare the first two articles`);
      }
    }

    prompts.slice(0, 5).forEach((p) => {
      const chip = document.createElement("button");
      chip.className = "prompt-chip";
      chip.type = "button";
      chip.textContent = p;
      chip.addEventListener("click", () => {
        if (p.startsWith("Summarize") && articles[0]) {
          sendAction("summarize", articles[0].id);
        } else if (p.startsWith("What's the sentiment") && articles[0]) {
          sendAction("sentiment", articles[0].id);
        } else if (p.startsWith("Compare the first two") && articles.length > 1) {
          sendAction("compare", articles[0].id, articles[1].id);
        } else {
          sendChat(p);
        }
      });
      suggestedPromptsEl.appendChild(chip);
    });
  }

  function truncate(str, n) {
    return str && str.length > n ? str.slice(0, n - 1) + "..." : str;
  }

  // ==========================================================================
  // Reset / new conversation
  // ==========================================================================

  resetBtn.addEventListener("click", async () => {
    try {
      await fetch("/api/reset", { method: "POST" });
    } catch (e) {
      /* ignore network errors on reset */
    }
    chatWindow.innerHTML = "";
    chatWindow.appendChild(welcome);
    welcome.style.display = "block";
    articles = [];
    selectedForCompare.clear();
    resultsList.innerHTML = "";
    resultsLabel.textContent = "Search for news to get started";
    updateCompareBar();
    renderSuggestedPrompts();
  });

  // ==========================================================================
  // Restore previous conversation on page load
  // ==========================================================================

  async function loadHistory() {
    try {
      const res = await fetch("/api/history");
      const data = await res.json();
      if (data.history && data.history.length > 0) {
        hideWelcome();
        data.history.forEach((m) => addMessage(m.role, m.content));
      }
    } catch (e) {
      /* first run, nothing to restore */
    }
  }

  // ---- Init ----
  renderSuggestedPrompts();
  updateCompareBar();
  loadHistory();
})();
