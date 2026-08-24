"""
ai_service.py
-------------
All calls to the AI model (OpenAI or Anthropic/Claude) live here.

Set AI_PROVIDER=openai or AI_PROVIDER=anthropic in your .env file to choose
which one is used. Everything else in the app talks to the small set of
functions below and never touches the OpenAI/Anthropic SDKs directly.

Functions:
    summarize_article(article)              -> str
    explain_article(article)                 -> str
    compare_articles(article_a, article_b)   -> str
    detect_sentiment(article)                -> dict {sentiment, confidence, explanation}
    chat_answer(history, articles, message)  -> str
"""

import os
import json
import re

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

_openai_client = None
_anthropic_client = None


class AIServiceError(Exception):
    """Raised for any AI-provider configuration or request error."""


def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise AIServiceError(
                "OPENAI_API_KEY is missing. Add it to your .env file "
                "or set AI_PROVIDER=anthropic to use Claude instead."
            )
        from openai import OpenAI  # imported lazily so the app still runs
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def _get_anthropic_client():
    global _anthropic_client
    if _anthropic_client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise AIServiceError(
                "ANTHROPIC_API_KEY is missing. Add it to your .env file "
                "or set AI_PROVIDER=openai to use OpenAI instead."
            )
        import anthropic
        _anthropic_client = anthropic.Anthropic(api_key=api_key)
    return _anthropic_client


def call_llm(system_prompt, messages, max_tokens=800, temperature=0.5):
    """
    Send a request to whichever provider is configured.

    messages: list of {"role": "user" | "assistant", "content": str}
    Returns: the assistant's reply as a plain string.
    """
    try:
        if AI_PROVIDER == "anthropic":
            client = _get_anthropic_client()
            resp = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=messages,
            )
            text_parts = [block.text for block in resp.content if block.type == "text"]
            return "".join(text_parts).strip()

        # default: openai
        client = _get_openai_client()
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=full_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()

    except AIServiceError:
        raise
    except Exception as e:
        raise AIServiceError(f"AI provider request failed: {e}")


def format_article(article, max_len=1500):
    return (
        f"Title: {article.get('title')}\n"
        f"Source: {article.get('source')}\n"
        f"Published: {article.get('publishedAt')}\n"
        f"Description: {article.get('description')}\n"
        f"Content snippet: {(article.get('content') or '')[:max_len]}\n"
        f"URL: {article.get('url')}"
    )


# ---------------------------------------------------------------------------
# Feature functions
# ---------------------------------------------------------------------------

def summarize_article(article):
    system = (
        "You are a skilled, neutral news editor for an AI News Assistant app. "
        "You write clear, accurate summaries and never invent facts that "
        "aren't in the provided article text."
    )
    user_content = (
        "Summarize the following news article for a busy reader. "
        "Respond in Markdown with:\n"
        "- 3 to 5 concise bullet points covering the key facts\n"
        "- One closing sentence titled **Why it matters**\n\n"
        f"{format_article(article)}"
    )
    return call_llm(system, [{"role": "user", "content": user_content}], max_tokens=500)


def explain_article(article):
    system = (
        "You are a friendly expert who explains news stories to people who "
        "have no background on the topic. You define jargon in plain "
        "language and give useful context without being condescending."
    )
    user_content = (
        "Explain this article to a complete beginner. Respond in Markdown with:\n"
        "- **What happened** (2-3 sentences)\n"
        "- **Background / context** a newcomer needs\n"
        "- **Key terms explained**, if any jargon appears\n"
        "- **Why it matters**\n\n"
        f"{format_article(article)}"
    )
    return call_llm(system, [{"role": "user", "content": user_content}], max_tokens=800)


def compare_articles(article_a, article_b):
    system = (
        "You are an objective media analyst for an AI News Assistant app. "
        "You compare news coverage fairly, without taking political sides, "
        "and you clearly separate facts from framing/opinion."
    )
    user_content = (
        "Compare the two articles below. Respond in Markdown with these sections:\n"
        "- **Shared facts** both articles agree on\n"
        "- **Differences** in emphasis, framing, or details\n"
        "- **Possible perspective or bias** in each (based only on wording/framing, "
        "not speculation about the outlets)\n"
        "- **What's missing** from each article\n\n"
        f"ARTICLE A:\n{format_article(article_a)}\n\n"
        f"ARTICLE B:\n{format_article(article_b)}"
    )
    return call_llm(system, [{"role": "user", "content": user_content}], max_tokens=900)


def detect_sentiment(article):
    system = (
        "You are a sentiment-analysis engine for news articles. "
        "Respond ONLY with strict, valid JSON and no other text, no markdown "
        "fences, matching exactly this shape:\n"
        '{"sentiment": "Positive" | "Negative" | "Neutral" | "Mixed", '
        '"confidence": <integer 0-100>, "explanation": "<1-2 sentence reason>"}'
    )
    user_content = f"Analyze the overall tone/sentiment of this article:\n\n{format_article(article)}"
    raw = call_llm(
        system, [{"role": "user", "content": user_content}], max_tokens=250, temperature=0.2
    )
    return _parse_sentiment_json(raw)


def _parse_sentiment_json(raw):
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        data = json.loads(cleaned)
        return {
            "sentiment": str(data.get("sentiment", "Neutral")).title(),
            "confidence": int(data.get("confidence", 50)),
            "explanation": str(data.get("explanation", "")).strip() or "No explanation provided.",
        }
    except (json.JSONDecodeError, ValueError, TypeError):
        # Fall back gracefully instead of crashing the whole request.
        match = re.search(r"positive|negative|neutral|mixed", cleaned, re.IGNORECASE)
        sentiment = match.group(0).title() if match else "Neutral"
        return {
            "sentiment": sentiment,
            "confidence": 50,
            "explanation": cleaned[:300] if cleaned else "The model did not return a parsable result.",
        }


def chat_answer(history, articles, user_message):
    """
    General Q&A. `history` is a list of {"role", "content"} from the ongoing
    conversation (already excludes the latest user message). `articles` is
    the list of articles currently known to this session, used as optional
    context so the assistant can answer questions like "what was the second
    article about?" without re-fetching anything.
    """
    context_lines = []
    for a in articles:
        context_lines.append(
            f"[{a.get('id')}] \"{a.get('title')}\" - {a.get('source')} "
            f"({a.get('publishedAt', '')[:10]}): {a.get('description', '')[:180]}"
        )
    context_block = "\n".join(context_lines) if context_lines else "No articles fetched yet."

    system = (
        "You are the 'AI News Assistant', a helpful, concise chat assistant embedded "
        "in a news reader app. You can discuss current events, answer general "
        "knowledge questions, and reference the articles the user has searched for "
        "in this session (listed below by id). When you reference a specific "
        "article, mention its title. If you're not sure about very recent events "
        "beyond the articles provided, say so honestly instead of guessing. "
        "Keep answers well-formatted in Markdown and reasonably concise.\n\n"
        f"Articles available in this session:\n{context_block}"
    )

    messages = list(history) + [{"role": "user", "content": user_message}]
    return call_llm(system, messages, max_tokens=700)
