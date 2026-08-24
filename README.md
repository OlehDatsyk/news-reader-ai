# 📰 AI News Assistant (News Reader V3)

An AI-powered news chat assistant built with **Python**, **Flask**, the
**OpenAI API (or Anthropic/Claude API)**, and **NewsAPI**.

Search the news, then chat with an AI that can **summarize**, **explain**,
**compare**, and **detect the sentiment** of articles - or just answer your
questions about current events, right inside a modern chat interface.

This README is written for someone who has **never run a Python project
before** and has only installed **Visual Studio Code**. Follow it top to
bottom and you will have the app running locally. Take your time - every
step is explained, including what to type and what you should see.

---

## Table of Contents

1. [What this app does](#1-what-this-app-does)
2. [Project folder structure](#2-project-folder-structure)
3. [Step 1 - Install Python](#step-1--install-python)
4. [Step 2 - Install Git (optional but recommended)](#step-2--install-git-optional-but-recommended)
5. [Step 3 - Get the project into VS Code](#step-3--get-the-project-into-vs-code)
6. [Step 4 - Open a terminal inside VS Code](#step-4--open-a-terminal-inside-vs-code)
7. [Step 5 - Create a virtual environment](#step-5--create-a-virtual-environment)
8. [Step 6 - Activate the virtual environment](#step-6--activate-the-virtual-environment)
9. [Step 7 - Install the project dependencies](#step-7--install-the-project-dependencies)
10. [Step 8 - Get your API keys](#step-8--get-your-api-keys)
11. [Step 9 - Create your `.env` file](#step-9--create-your-env-file)
12. [Step 10 - Run the application](#step-10--run-the-application)
13. [Step 11 - Use the app](#step-11--use-the-app)
14. [Common Errors & Solutions](#common-errors--solutions)
15. [How the app works (short technical overview)](#how-the-app-works-short-technical-overview)
16. [Stopping the server / running it again later](#stopping-the-server--running-it-again-later)
17. [License & credits](#license--credits)

---

## 1. What this app does

- 🔎 **News search** - search any topic, or browse top headlines by category
  (Technology, Business, Science, Health, Sports, Entertainment).
- 🤖 **AI summaries** - get a bullet-point summary of any article.
- 💡 **AI explains articles** - plain-language explanations with background
  and jargon defined, great for unfamiliar topics.
- ⚖️ **AI compares articles** - select two articles and see how their
  coverage, framing, and facts differ.
- 📊 **AI sentiment detection** - see whether an article's tone is positive,
  negative, neutral, or mixed, with a short explanation.
- 💬 **AI answers your questions** - ask anything about the news you've
  searched for, or general questions, in a normal chat.
- 🕘 **Conversation history** - your chat is remembered as you use the app.
- ✨ **Suggested prompts** - quick-click suggestions to get you started.
- 📱 **Responsive design** - works on desktop, tablet, and mobile screens.

---

## 2. Project folder structure

Once everything is set up, your project folder will look like this:

```
news-reader-ai/
│
├── app.py # Main Flask application (routes / API endpoints)
├── ai_service.py # Talks to OpenAI or Anthropic (Claude) API
├── news_service.py # Talks to NewsAPI.org
├── requirements.txt # List of Python packages this project needs
├── .env.example # Template for your secret keys (safe to share)
├── .env # YOUR real secret keys (you will create this - never share it)
├── .gitignore # Tells Git which files to ignore
├── README.md # This file
│
├── templates/
│   └── index.html # The single HTML page for the chat interface
│
└── static/
    ├── css/
    │   └── style.css # All the styling (modern dark chat UI)
    └── js/
        └── app.js # Frontend logic (search, chat, buttons)
```

You do not need to create any of these files by hand - they are already
included in the project. This section just helps you understand what each
file is for.

---

## Step 1 - Install Python

The app is written in Python, so your computer needs Python installed
(version **3.9 or newer** is recommended).

### Check if Python is already installed

1. Open **Visual Studio Code**.
2. Open a terminal inside VS Code: click the menu **Terminal -> New Terminal**
   (or press `` Ctrl+` `` on Windows/Linux, `` Cmd+` `` on Mac).
3. In the terminal, type:

   ```bash
   python --version
   ```

   If that doesn't work, try:

   ```bash
   python3 --version
   ```

4. If you see something like `Python 3.11.4`, Python is already installed -
   skip to [Step 2](#step-2--install-git-optional-but-recommended).

   If you see an error like `command not found` or `'python' is not
   recognized`, you need to install Python - continue below.

### Installing Python

**Windows:**

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click the big **"Download Python 3.x.x"** button.
3. Run the downloaded installer.
4. ⚠️ **VERY IMPORTANT:** On the first installer screen, check the box that
   says **"Add python.exe to PATH"** at the bottom, *before* clicking
   Install. This step is the #1 cause of problems for beginners - don't
   skip it.
5. Click **Install Now** and wait for it to finish.
6. Close and reopen VS Code (fully quit, not just close the window) so it
   picks up the new PATH.
7. Open a new terminal in VS Code and run `python --version` again to
   confirm it worked.

**macOS:**

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the macOS installer and run it, following the prompts.
3. Close and reopen VS Code.
4. In a new terminal, run `python3 --version` to confirm.

**Linux (Ubuntu/Debian example):**

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

Then confirm with:

```bash
python3 --version
```

> 💡 **Tip:** On Windows the command is usually `python`, while on macOS and
> Linux it's usually `python3`. If a command in this guide doesn't work,
> try the other version. From here on, this guide will use `python`, but
> substitute `python3` if that's what works on your machine.

---

## Step 2 - Install Git (optional but recommended)

Git is only needed if you plan to download this project from a Git
repository (e.g., GitHub) or want version control. If you already have the
project folder on your computer (e.g., extracted from a ZIP file), you can
**skip this step**.

**Check if Git is installed:**

```bash
git --version
```

If you see a version number, you're done. If not:

- **Windows:** Download and install from [https://git-scm.com/download/win](https://git-scm.com/download/win)
  (accept the default options during installation).
- **macOS:** Install via [https://git-scm.com/download/mac](https://git-scm.com/download/mac),
  or run `xcode-select --install` in the terminal.
- **Linux:** `sudo apt install git`

---

## Step 3 - Get the project into VS Code

You should already have a folder called **`news-reader-ai`** containing all
the project files (this is what was generated for you). Open it in VS Code:

1. Open **VS Code**.
2. Go to **File -> Open Folder...**
3. Select the `news-reader-ai` folder.
4. Click **Select Folder** (Windows/Linux) or **Open** (Mac).

You should now see the file list (`app.py`, `templates/`, `static/`, etc.)
in the Explorer panel on the left.

---

## Step 4 - Open a terminal inside VS Code

All the remaining commands are typed into a terminal **inside VS Code**, so
you don't need any other program.

1. Click **Terminal** in the top menu bar.
2. Click **New Terminal**.
3. A panel opens at the bottom of VS Code with a command prompt. Make sure
   it opened in your project folder - it should show something like:

   ```
   PS C:\Users\YourName\news-reader-ai>
   ```

   or on Mac/Linux:

   ```
   yourname@YourMac news-reader-ai %
   ```

   If it shows a different folder, type `cd path/to/news-reader-ai` and
   press Enter to move into the correct folder.

---

## Step 5 - Create a virtual environment

A **virtual environment** (or "venv") is an isolated folder that keeps this
project's Python packages separate from everything else on your computer.
This avoids version conflicts and is standard practice for every Python
project.

In the VS Code terminal, run:

```bash
python -m venv venv
```

This creates a new folder called `venv/` inside your project. Nothing
visible will happen for a few seconds - that's normal. When it's done,
you'll see a new `venv` folder appear in the Explorer panel on the left.

> If `python` doesn't work, try `python3 -m venv venv`.

---

## Step 6 - Activate the virtual environment

You must "activate" the virtual environment every time you open a new
terminal to work on this project. Activating it tells your terminal to use
the isolated Python packages instead of your system-wide Python.

**Windows (PowerShell - the default VS Code terminal):**

```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt, if you're using `cmd` instead of PowerShell):**

```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### How do I know it worked?

Your terminal prompt should now start with `(venv)`, like this:

```
(venv) PS C:\Users\YourName\news-reader-ai>
```

or

```
(venv) yourname@YourMac news-reader-ai %
```

If you see `(venv)` at the start of the line, you're good to go!

### ⚠️ PowerShell "running scripts is disabled" error

If you're on Windows and see an error like:

```
File ... cannot be loaded because running scripts is disabled on this system.
```

Run this command once (it changes a security setting for your user only,
not the whole system), then try activating again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Type `Y` and press Enter if it asks for confirmation.

---

## Step 7 - Install the project dependencies

With your virtual environment **activated** (you should see `(venv)` in the
prompt), install all required Python packages with one command:

```bash
pip install -r requirements.txt
```

This reads the `requirements.txt` file and installs:

- **Flask** - the web framework that powers the app
- **python-dotenv** - loads your secret keys from the `.env` file
- **requests** - used to call the NewsAPI
- **openai** - the official OpenAI Python SDK
- **anthropic** - the official Anthropic (Claude) Python SDK

You should see a stream of text ending in something like:

```
Successfully installed Flask-3.0.3 anthropic-0.34.2 openai-1.51.2 python-dotenv-1.0.1 requests-2.32.3 ...
```

This can take one to two minutes depending on your internet connection.

---

## Step 8 - Get your API keys

This app needs **two** kinds of API keys:

1. A **NewsAPI** key (always required) - used to fetch news articles.
2. **Either** an **OpenAI** key **or** an **Anthropic (Claude)** key - used
   to power the AI features. You only need one of the two, not both.

### 8a. Get a free NewsAPI key

1. Go to [https://newsapi.org/register](https://newsapi.org/register)
2. Fill in the form and create a free account.
3. After registering, your API key is shown on your account page (also
   available any time at [https://newsapi.org/account](https://newsapi.org/account)).
4. Copy this key - you'll paste it into the `.env` file in the next step.

> **Note:** NewsAPI's free "Developer" plan is for local development/testing
> and has a limit on daily requests - that's perfectly fine for running this
> project.

### 8b. Get an OpenAI API key (option 1)

1. Go to [https://platform.openai.com/signup](https://platform.openai.com/signup)
   and create an account (or log in).
2. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
3. Click **Create new secret key**, give it a name, and copy the key
   immediately - OpenAI only shows it once.
4. You'll need billing set up on your OpenAI account for API calls to work
   (even small amounts of usage on this project cost only a few cents).

### 8c. Get an Anthropic (Claude) API key (option 2 - alternative to OpenAI)

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
   and create an account (or log in).
2. Go to **API Keys** in the console and click **Create Key**.
3. Copy the generated key.

> You only need **one** of 8b or 8c. Pick whichever provider you have (or
> want) an account with - the app supports both.

---

## Step 9 - Create your `.env` file

The `.env` file stores your secret API keys so they never get hard-coded
into the source code (and are never uploaded to Git, thanks to
`.gitignore`).

1. In the VS Code Explorer panel, find the file **`.env.example`**.
2. Right-click it and choose **Copy**, then right-click the folder and
   choose **Paste**. This creates a copy called `.env.example copy` or
   similar.
3. Rename the copy to exactly: **`.env`** (no `.txt`, no extra characters -
   just a file named `.env`).

   *Alternative (faster) method - in the VS Code terminal:*

   ```bash
   # Windows (PowerShell)
   Copy-Item .env.example .env

   # macOS / Linux
   cp .env.example .env
   ```

4. Open the new `.env` file in VS Code (click it in the Explorer panel) and
   fill in your real keys. It should look like this when you're done
   (example values shown - use your own real keys):

   ```env
   AI_PROVIDER=openai

   OPENAI_API_KEY=sk-proj-abc123yourrealkeyhere
   OPENAI_MODEL=gpt-4o-mini

   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

   NEWS_API_KEY=abcd1234yourrealnewsapikeyhere

   FLASK_SECRET_KEY=any-random-string-you-like-12345
   FLASK_DEBUG=True
   PORT=8000
   ```

   - Set `AI_PROVIDER` to `openai` if you got an OpenAI key, or `anthropic`
     if you got a Claude key.
   - You only need to fill in the key that matches your chosen provider -
     it's fine to leave the other one as the placeholder text.
   - `FLASK_SECRET_KEY` can be any random string - mash your keyboard, it
     just needs to be non-empty and private.

5. **Save the file** (`Ctrl+S` / `Cmd+S`).

> 🔒 **Never share your `.env` file or commit it to Git/GitHub.** It
> contains secret keys that can be used to run up charges on your account.
> The included `.gitignore` file already prevents this by default.

---

## Step 10 - Run the application

With your virtual environment activated (`(venv)` visible in the terminal
prompt) and your `.env` file filled in, start the Flask server:

```bash
python app.py
```

You should see output similar to this in the terminal:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://192.168.1.23:8000
Press CTRL+C to quit
```

This means the server is running successfully! 🎉

---

## Step 11 - Use the app

1. Hold `Ctrl` (or `Cmd` on Mac) and click the `http://127.0.0.1:8000` link
   in the terminal - or just open your web browser and go to:

   ```
   http://127.0.0.1:8000
   ```

2. You should see the **AI News Assistant** chat interface load.
3. Try it out:
   - Type a topic (e.g., `electric vehicles`) into the search box on the
     left and click **Search**.
   - Click **📝 Summarize**, **💡 Explain**, or **📊 Sentiment** on any
     article card.
   - Check two article checkboxes and click **Compare Selected**.
   - Type a question in the chat box at the bottom and press Enter.
   - Click one of the **suggested prompt** chips above the chat box for a
     quick start.
4. To stop the server, click back into the VS Code terminal and press
   `Ctrl+C`.

---

## Common Errors & Solutions

| Error message | What it means | How to fix it |
|---|---|---|
| `'python' is not recognized as an internal or external command` | Python isn't installed, or wasn't added to PATH | Reinstall Python and check **"Add python.exe to PATH"** during setup (see [Step 1](#step-1--install-python)) |
| `ModuleNotFoundError: No module named 'flask'` | Dependencies aren't installed, or your virtual environment isn't activated | Run the activate command from [Step 6](#step-6--activate-the-virtual-environment), then `pip install -r requirements.txt` again |
| `(venv)` doesn't appear in your terminal prompt after activating | The activation command didn't run correctly, or you're in the wrong folder | Make sure you're inside the `news-reader-ai` folder, then re-run the correct activation command for your OS |
| `running scripts is disabled on this system` (Windows) | PowerShell's security policy blocks the activation script | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, confirm with `Y`, then try activating again |
| `NEWS_API_KEY is not configured on the server` (shown in the app) | Your `.env` file is missing or the key wasn't filled in | Double-check the file is named exactly `.env` (not `.env.txt`) and that `NEWS_API_KEY=` has your real key with no quotes |
| `No AI API key configured` (shown in the app) | Neither `OPENAI_API_KEY` nor `ANTHROPIC_API_KEY` is set | Fill in the key matching your `AI_PROVIDER` setting in `.env`, then restart the server |
| `AuthenticationError` / `401` from OpenAI or Anthropic | The API key is invalid, expired, or has no billing set up | Regenerate the key on the provider's dashboard and make sure billing/credits are active on your account |
| `Address already in use` / `Port 8000 is in use` | Another program (or another copy of this app) is already using port 8000 | Stop the other program, or change `PORT=8000` to `PORT=5050` in `.env` and restart, then visit `http://127.0.0.1:5050` |
| Page loads but styling looks broken / plain HTML | The Flask server isn't finding the `static/` folder, or files were moved | Make sure the folder structure matches [Project folder structure](#2-project-folder-structure) exactly, and that you're running `python app.py` from inside `news-reader-ai/` |
| Chat says "AI provider request failed" | The AI API might be temporarily down, your key ran out of credits, or you're offline | Check your internet connection and your API usage/billing dashboard for the provider you're using |
| Nothing happens when you click Search | The NewsAPI free plan may have hit its daily request limit, or there's a typo in the key | Wait for the daily limit to reset, or verify the key on [newsapi.org/account](https://newsapi.org/account) |
| Terminal closed and you lost your `(venv)` session | This is normal - activation only lasts for the current terminal session | Just repeat [Step 6](#step-6--activate-the-virtual-environment) (`source venv/bin/activate` or the Windows equivalent) each time you open a new terminal |

---

## How the app works (short technical overview)

- **`app.py`** is the Flask application. It defines these routes:
  - `GET /` - serves the chat page (`templates/index.html`)
  - `POST /api/search` - fetches articles from NewsAPI (search or headlines)
  - `POST /api/chat` - handles all AI actions: `chat`, `summarize`,
    `explain`, `sentiment`, `compare`
  - `GET /api/history` - returns the current conversation for this browser
  - `POST /api/reset` - clears the conversation and fetched articles
- **`news_service.py`** wraps NewsAPI's `/v2/everything` and
  `/v2/top-headlines` endpoints and normalizes the response.
- **`ai_service.py`** builds prompts and calls either the OpenAI or
  Anthropic chat completion API, depending on `AI_PROVIDER` in your `.env`.
- **`templates/index.html`**, **`static/css/style.css`**, and
  **`static/js/app.js`** make up the frontend - a single-page chat UI with
  no build tools required, using `marked.js` (loaded from a CDN) to render
  the AI's Markdown-formatted replies.
- Conversation history and fetched articles are stored **server-side, in
  memory**, keyed to a private session cookie set in your browser. This
  keeps things simple for local development - restarting the server (or
  running on a different machine/host) will clear the history. For a
  production deployment you'd swap this for a real database, but that's
  outside the scope of this learning project.

---

## Stopping the server / running it again later

**To stop the server:** click into the terminal running it and press
`Ctrl+C`.

**To run it again later** (e.g., after restarting your computer or
reopening VS Code), you only need to repeat two steps - Python, the venv,
and your dependencies are already set up:

```bash
# 1. Activate the virtual environment (from inside the news-reader-ai folder)
# Windows PowerShell:
venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# 2. Run the app
python app.py
```

Then open `http://127.0.0.1:8000` in your browser again.

---

## License & credits

This project was generated as a learning/demo application. It uses:

- [Flask](https://flask.palletsprojects.com/) - web framework
- [NewsAPI](https://newsapi.org/) - news data
- [OpenAI API](https://platform.openai.com/docs) and/or
  [Anthropic API](https://docs.anthropic.com/) - AI features
- [marked.js](https://marked.js.org/) - Markdown rendering in the browser

Feel free to modify, extend, and use this project as a starting point for
your own AI-powered applications.
