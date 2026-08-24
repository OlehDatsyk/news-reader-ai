"""
AI News Assistant - Flask backend
-----------------------------------
This file wires together:
  - news_service.py  -> talks to NewsAPI.org to fetch articles
  - ai_service.py     -> talks to OpenAI or Anthropic (Claude) to generate
                          summaries, explanations, comparisons, sentiment,
                          and general chat answers
  - templates/index.html + static/ -> the chat UI served to the browser

Conversation history and fetched articles are kept server-side, in memory,
keyed by a per-browser session id (stored in a signed cookie). This is
intentionally simple for a learning project - see README.md for details
and limitations (history resets if the server restarts).
"""

import os
import uuid
from datetime import datetime

from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

import news_service
import ai_service

# Load variables from .env into the environment (OPENAI_API_KEY, etc.)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# ---------------------------------------------------------------------------
# In-memory "database". Structure:
# {
#   "<session-id>": {
#       "history": [ {role, content, timestamp}, ... ],
#       "articles": { <id:int>: {title, description, url, ...}, ... }
#   }
# }
# ---------------------------------------------------------------------------
SESSIONS = {}


def get_session_data():
    """Return (and create if needed) the storage bucket for this browser."""
    sid = session.get("sid")
    if not sid:
        sid = str(uuid.uuid4())
        session["sid"] = sid
    if sid not in SESSIONS:
        SESSIONS[sid] = {"history": [], "articles": {}}
    return SESSIONS[sid]


def add_message(data, role, content):
    data["history"].append(
        {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().strftime("%H:%M"),
        }
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def api_search():
    """Search NewsAPI for articles, or fetch top headlines by category."""
    body = request.get_json(force=True, silent=True) or {}
    query = (body.get("query") or "").strip()
    category = body.get("category")
    mode = body.get("mode", "search")

    if not NEWS_API_KEY:
        return (
            jsonify(
                {
                    "error": "NEWS_API_KEY is not configured on the server. "
                    "Add it to your .env file and restart the app."
                }
            ),
            500,
        )

    data = get_session_data()
    start_id = len(data["articles"])

    try:
        if mode == "headlines" or (category and not query):
            articles = news_service.top_headlines(NEWS_API_KEY, category=category)
        else:
            if not query:
                return jsonify({"error": "Please enter a search term."}), 400
            articles = news_service.search_news(NEWS_API_KEY, query)
    except news_service.NewsAPIError as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:  # pragma: no cover - network/edge errors
        return jsonify({"error": f"Unexpected error fetching news: {e}"}), 500

    # Give every article a globally unique id within this session so the
    # frontend can reference it later for summarize/explain/compare actions.
    result = []
    for i, art in enumerate(articles):
        gid = start_id + i
        art["id"] = gid
        data["articles"][gid] = art
        result.append(art)

    return jsonify({"articles": result})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Handle every AI-powered action: chat, summarize, explain, compare, sentiment."""
    body = request.get_json(force=True, silent=True) or {}
    action = body.get("action", "chat")
    message = (body.get("message") or "").strip()
    article_id = body.get("article_id")
    article_id_2 = body.get("article_id_2")

    data = get_session_data()

    if not (os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")):
        return (
            jsonify(
                {
                    "error": "No AI API key configured. Add OPENAI_API_KEY "
                    "(or ANTHROPIC_API_KEY) to your .env file and restart the app."
                }
            ),
            500,
        )

    try:
        if action == "summarize":
            article = data["articles"].get(article_id)
            if not article:
                return jsonify({"error": "Article not found. Try searching again."}), 404
            add_message(data, "user", f'Summarize this article: "{article["title"]}"')
            reply = ai_service.summarize_article(article)

        elif action == "explain":
            article = data["articles"].get(article_id)
            if not article:
                return jsonify({"error": "Article not found. Try searching again."}), 404
            add_message(data, "user", f'Explain this article: "{article["title"]}"')
            reply = ai_service.explain_article(article)

        elif action == "sentiment":
            article = data["articles"].get(article_id)
            if not article:
                return jsonify({"error": "Article not found. Try searching again."}), 404
            add_message(
                data, "user", f'What is the sentiment of this article: "{article["title"]}"'
            )
            result = ai_service.detect_sentiment(article)
            reply = (
                f"**Sentiment: {result['sentiment']}** (confidence: {result['confidence']}%)\n\n"
                f"{result['explanation']}"
            )

        elif action == "compare":
            article_a = data["articles"].get(article_id)
            article_b = data["articles"].get(article_id_2)
            if not article_a or not article_b:
                return jsonify({"error": "Please select two valid articles to compare."}), 404
            add_message(
                data,
                "user",
                f'Compare these articles: "{article_a["title"]}" vs "{article_b["title"]}"',
            )
            reply = ai_service.compare_articles(article_a, article_b)

        else:  # plain chat / general question
            if not message:
                return jsonify({"error": "Please type a message."}), 400
            add_message(data, "user", message)
            # last 10 turns (excluding the message we just added) for context
            history_for_llm = [
                {"role": m["role"], "content": m["content"]}
                for m in data["history"][:-1][-10:]
                if m["role"] in ("user", "assistant")
            ]
            recent_articles = list(data["articles"].values())[-8:]
            reply = ai_service.chat_answer(history_for_llm, recent_articles, message)

        add_message(data, "assistant", reply)
        return jsonify({"reply": reply, "history": data["history"]})

    except ai_service.AIServiceError as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:  # pragma: no cover
        return jsonify({"error": f"Unexpected error: {e}"}), 500


@app.route("/api/history", methods=["GET"])
def api_history():
    data = get_session_data()
    return jsonify({"history": data["history"]})


@app.route("/api/reset", methods=["POST"])
def api_reset():
    data = get_session_data()
    data["history"] = []
    data["articles"] = {}
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
