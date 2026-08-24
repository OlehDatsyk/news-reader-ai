# 📖 INSTRUCTION.md - Complete Beginner's Guide

Welcome! This guide assumes you have **never used** Python, Visual Studio
Code, Git, a terminal, a virtual environment, or an API key before. Every
step is spelled out - just follow along from top to bottom. Nothing here
requires prior programming experience.

> 💡 This guide is intentionally more detailed than `README.md`. If you get
> stuck on any single step, this is the file to come back to.

---

## Table of Contents

1. [What you're installing, and why](#1-what-youre-installing-and-why)
2. [Install Python](#2-install-python)
3. [Install Git](#3-install-git)
4. [Install Visual Studio Code](#4-install-visual-studio-code)
5. [Install the recommended VS Code extensions](#5-install-the-recommended-vs-code-extensions)
6. [Open the project in VS Code](#6-open-the-project-in-vs-code)
7. [Create a virtual environment](#7-create-a-virtual-environment)
8. [Activate the virtual environment](#8-activate-the-virtual-environment)
9. [Install the project dependencies](#9-install-the-project-dependencies)
10. [Create your `.env` file and add API keys](#10-create-your-env-file-and-add-api-keys)
11. [Run the application](#11-run-the-application)
12. [Test that everything works](#12-test-that-everything-works)
13. [Using every feature](#13-using-every-feature)
14. [Troubleshooting](#14-troubleshooting)
15. [FAQ](#15-faq)
16. [Common mistakes beginners make](#16-common-mistakes-beginners-make)
17. [Security recommendations](#17-security-recommendations)
18. [Next learning steps](#18-next-learning-steps)

---

## 1. What you're installing, and why

This project ("AI News Assistant") is a small website that runs on your own
computer. To make it run, you need four things:

| Tool | What it's for |
|---|---|
| **Python** | The programming language the app (`app.py` and friends) is written in. |
| **Git** *(optional)* | Lets you download projects from GitHub and track changes to code. Not required if you already have the project folder. |
| **Visual Studio Code (VS Code)** | A free code editor - where you'll open the project, edit the `.env` file, and run terminal commands. |
| **A terminal** | A text-based way to type commands to your computer. VS Code has one built in, so you don't need a separate app. |

You'll also need two kinds of **API keys** (free to obtain) - explained in
detail in [Step 10](#10-create-your-env-file-and-add-api-keys).

---

## 2. Install Python

Python is the language this app is written in. You need version **3.9 or
newer**.

### Check if you already have it

1. Open Visual Studio Code (install it first if you don't have it yet - see
   [Step 4](#4-install-visual-studio-code) - then come back here).
2. Open a terminal: menu **Terminal -> New Terminal**.
3. Type:
   ```bash
   python --version
   ```
   If nothing happens, try:
   ```bash
   python3 --version
   ```
4. If you see something like `Python 3.12.1`, you already have Python -
   skip to [Step 3](#3-install-git).

### Install it

**Windows:**
1. Go to <https://www.python.org/downloads/>
2. Click the big yellow **Download Python** button.
3. Run the installer.
4. ⚠️ On the very first screen, tick the checkbox **"Add python.exe to
   PATH"** at the bottom before clicking **Install Now**. This is the
   single most common mistake beginners make - if you skip it, your
   computer won't be able to find Python later.
5. When it finishes, **fully close and reopen VS Code** (not just the
   window - quit the app completely).
6. Open a new terminal and run `python --version` to confirm.

**macOS:**
1. Go to <https://www.python.org/downloads/>
2. Download the macOS installer and run it, clicking through the prompts.
3. Fully quit and reopen VS Code.
4. In a new terminal, run `python3 --version` to confirm.

**Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
python3 --version
```

> 💡 On Windows the command is usually `python`. On macOS/Linux it's
> usually `python3`. If a command below doesn't work, try the other one.

---

## 3. Install Git

Git is only needed if you're downloading this project from GitHub (using
`git clone`) or want to track your own changes with version control. If you
already have the project as a folder on your computer (e.g. unzipped from a
`.zip` file), **you can skip this step**.

**Check first:**
```bash
git --version
```

**If it's missing:**
- **Windows:** <https://git-scm.com/download/win> - accept all default
  options during installation.
- **macOS:** <https://git-scm.com/download/mac>, or run
  `xcode-select --install` in a terminal.
- **Linux:** `sudo apt install git`

---

## 4. Install Visual Studio Code

1. Go to <https://code.visualstudio.com/>
2. Click **Download** for your operating system.
3. Run the installer and accept the default options.
4. Open VS Code once to confirm it launches.

---

## 5. Install the recommended VS Code extensions

Extensions add extra features to VS Code. These two make working with this
project much easier:

1. Click the **Extensions** icon in the left sidebar (it looks like four
   squares, one detached), or press `Ctrl+Shift+X` (`Cmd+Shift+X` on Mac).
2. Search for and install:
   - **Python** (by Microsoft) - adds Python syntax highlighting,
     IntelliSense, and lets VS Code recognize your virtual environment.
   - **Pylance** (by Microsoft) - usually installs automatically with the
     Python extension; provides smarter autocomplete and error checking.
3. *(Optional, nice to have)*: **DotENV** (by mikestead) - adds syntax
   highlighting to `.env` files so they're easier to read.

You don't need to configure anything else - VS Code will pick up your
Python installation automatically once these are installed.

---

## 6. Open the project in VS Code

1. Open VS Code.
2. Go to **File -> Open Folder...**
3. Select the `news-reader-ai` folder (the one containing `app.py`).
4. Click **Select Folder** (Windows/Linux) or **Open** (macOS).

You should now see files like `app.py`, `templates/`, and `static/` in the
Explorer panel on the left.

---

## 7. Create a virtual environment

A **virtual environment** ("venv") is a private, isolated folder that holds
this project's Python packages separately from everything else on your
computer, so different projects never conflict with each other. This is
standard practice for every Python project, not something specific to this
app.

Open a terminal in VS Code (**Terminal -> New Terminal**) and make sure
you're inside the `news-reader-ai` folder, then run:

```bash
python -m venv venv
```

(Use `python3` instead of `python` if that's what worked in Step 2.)

Nothing dramatic happens on screen - after a few seconds, a new `venv`
folder will appear in the Explorer panel. That's expected.

---

## 8. Activate the virtual environment

You need to "activate" the virtual environment **every time** you open a
new terminal to work on this project. This tells the terminal to use the
isolated packages inside `venv/` instead of your system-wide Python.

**Windows (PowerShell - the VS Code default):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### How to know it worked

Your terminal prompt should now begin with `(venv)`, for example:
```
(venv) PS C:\Users\You\news-reader-ai>
```

If you see `(venv)`, you're ready for the next step.

### If PowerShell blocks the activation script

You may see an error like:
```
File ... cannot be loaded because running scripts is disabled on this system.
```
Run this once (it only changes a setting for your own user account):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Type `Y` and press Enter if asked, then try activating again.

---

## 9. Install the project dependencies

With `(venv)` showing in your terminal prompt, run:

```bash
pip install -r requirements.txt
```

This installs everything listed in `requirements.txt`:

- **Flask** - the web framework that runs the app
- **python-dotenv** - loads your secret keys from `.env`
- **requests** - used to call the NewsAPI
- **openai** - official OpenAI SDK
- **anthropic** - official Anthropic (Claude) SDK

This can take one to two minutes. You'll know it worked when you see a line
like `Successfully installed Flask-... anthropic-... openai-... ...`.

---

## 10. Create your `.env` file and add API keys

The app needs two kinds of secret keys, stored in a file called `.env`
(never shared, never committed to Git - `.gitignore` already protects it).

### 10a. Copy the template

In the VS Code terminal:
```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

### 10b. Get a free NewsAPI key (always required)

1. Go to <https://newsapi.org/register> and create a free account.
2. Your key appears on your account page, also at
   <https://newsapi.org/account>.
3. Copy it.

> The free "Developer" plan has a daily request limit - that's fine for
> running this project locally.

### 10c. Get an AI provider key - pick ONE

You only need **one** of the following two, not both.

**Option 1 - OpenAI:**
1. Sign up / log in at <https://platform.openai.com/signup>
2. Go to <https://platform.openai.com/api-keys>
3. Click **Create new secret key**, name it, and copy it immediately (it's
   only shown once).
4. You'll need billing enabled on your OpenAI account (usage on this
   project typically costs only a few cents).

**Option 2 - Anthropic (Claude):**
1. Sign up / log in at <https://console.anthropic.com/>
2. Go to **API Keys -> Create Key**.
3. Copy the generated key.

### 10d. Fill in `.env`

Open the new `.env` file in VS Code and fill in your real values:

```env
AI_PROVIDER=openai

OPENAI_API_KEY=sk-proj-your-real-key-here
OPENAI_MODEL=gpt-4o-mini

ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

NEWS_API_KEY=your-real-newsapi-key-here

FLASK_SECRET_KEY=any-random-string-you-make-up
FLASK_DEBUG=True
PORT=8000
```

- Set `AI_PROVIDER` to whichever provider you got a key for (`openai` or
  `anthropic`). You only need to fill in the matching key - the other one
  can stay as placeholder text.
- `FLASK_SECRET_KEY` can be any random string you type - it just needs to
  be non-empty and private (don't reuse a password).
- Save the file (`Ctrl+S` / `Cmd+S`).

> 🔒 Never share your `.env` file, screenshot it, or commit it to Git. It
> contains secrets that could let someone else spend your API credits.

---

## 11. Run the application

With `(venv)` active and `.env` filled in, run:

```bash
python app.py
```

You should see something like:
```
* Serving Flask app 'app'
* Running on http://127.0.0.1:8000
Press CTRL+C to quit
```

That means it worked. Alternatively, once you're set up, you can double-click
**`Start App.bat`** (Windows) or **`Start App (Mac).command`** (macOS) any
time you want to launch the app without typing commands - see
[Section 13](#13-using-every-feature) below for details on those scripts.

---

## 12. Test that everything works

1. Open your browser and go to `http://127.0.0.1:8000`.
2. You should see the **AI News Assistant** chat interface.
3. Type a topic like `electric vehicles` into the search box and click
   **Search**. Articles should appear in the sidebar within a couple of
   seconds.
4. Click **📝 Summarize** on any article card. A summary should appear in
   the chat panel within a few seconds.
5. Type a question in the chat box at the bottom (e.g. `What's happening in
   tech today?`) and press Enter.

If all four steps work, your setup is complete. If any step fails, jump to
[Troubleshooting](#14-troubleshooting).

---

## 13. Using every feature

| Feature | How to use it |
|---|---|
| **Search news** | Type a topic in the sidebar search box and click **Search**. |
| **Browse by category** | Click one of the category chips (Top, Tech, Business, Science, Health, Sports, Entertainment) instead of searching. |
| **Summarize** | Click **📝 Summarize** on any article card for a bullet-point summary. |
| **Explain** | Click **💡 Explain** for a plain-language explanation aimed at someone new to the topic. |
| **Sentiment** | Click **📊 Sentiment** to see whether an article's tone is Positive, Negative, Neutral, or Mixed. |
| **Compare two articles** | Tick the **Compare** checkbox on two different article cards, then click **Compare Selected** at the bottom of the sidebar. |
| **General chat** | Type any question in the chat box at the bottom - you can ask about articles you've already searched for, or general questions. |
| **Suggested prompts** | Click one of the chips above the chat box for a quick, pre-written question. |
| **New conversation** | Click **🗑️ New conversation** at the top of the chat panel to clear your history and start over. |
| **Mobile view** | On narrow screens, tap the ☰ icon to open the search sidebar, and ✕ to close it. |

### The two startup scripts

Once you've completed Steps 2-10 (installed Python, created the venv,
installed dependencies, and filled in `.env`) **one time**, you can use
these scripts to launch the app going forward without typing any commands:

- **Windows:** double-click `Start App.bat`
- **macOS:** double-click `Start App (Mac).command`

Both scripts automatically check for Python, create/reuse your virtual
environment, install any missing dependencies, verify `.env` exists, and
then start the server - showing clear status messages the whole way, and
staying open if something goes wrong so you can read the error.

> On macOS, the first time you double-click `Start App (Mac).command` you
> may need to right-click it and choose **Open** instead (see
> Troubleshooting below) because of Apple's Gatekeeper security check.

---

## 14. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `'python' is not recognized...` | Python isn't installed, or wasn't added to PATH | Reinstall Python and tick **"Add python.exe to PATH"** (see [Step 2](#2-install-python)) |
| `ModuleNotFoundError: No module named 'flask'` | Virtual environment isn't activated, or dependencies aren't installed | Run the activation command from [Step 8](#8-activate-the-virtual-environment), then `pip install -r requirements.txt` again |
| `(venv)` doesn't appear after activating | Wrong folder, or the activation command failed silently | Make sure you're inside `news-reader-ai`, then re-run the correct command for your OS |
| PowerShell: `running scripts is disabled on this system` | Windows security policy | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, confirm with `Y` |
| `NEWS_API_KEY is not configured on the server` | `.env` is missing or the key is blank | Confirm the file is named exactly `.env` (not `.env.txt`), and `NEWS_API_KEY=` has your real key with no quotes |
| `No AI API key configured` | Neither `OPENAI_API_KEY` nor `ANTHROPIC_API_KEY` is filled in | Fill in the key matching your `AI_PROVIDER`, then restart the app |
| `AuthenticationError` / `401` | Invalid, expired, or unbilled API key | Regenerate the key on the provider's dashboard and confirm billing/credits are active |
| `Address already in use` / port 8000 busy | Another program is using port 8000 | Stop it, or change `PORT=8000` to `PORT=5050` in `.env`, then visit `http://127.0.0.1:5050` |
| Page loads with no styling | Server isn't finding `static/` | Confirm you're running `python app.py` from inside the `news-reader-ai` folder and the folder structure hasn't changed |
| "AI provider request failed" in chat | Provider outage, expired key, or no internet | Check your connection and the provider's status/billing page |
| Search returns nothing | NewsAPI daily limit hit, or a typo in the key | Wait for the daily reset, or verify the key at newsapi.org/account |
| macOS: "cannot be opened because it is from an unidentified developer" | Gatekeeper blocking the `.command` script | Right-click `Start App (Mac).command` -> **Open** -> confirm **Open** in the dialog (only needed once) |
| macOS: double-click does nothing / opens as text | The file isn't marked executable yet | In Terminal: `chmod +x "Start App (Mac).command"`, then double-click again |
| Terminal closed and `(venv)` disappeared | Normal - activation only lasts for that terminal session | Repeat [Step 8](#8-activate-the-virtual-environment) each time you open a new terminal |

---

## 15. FAQ

**Do I need to know how to code to use this app?**
No - following this guide only requires typing the exact commands shown.
Understanding the code itself is optional.

**Do I need both an OpenAI key and an Anthropic key?**
No, just one. Set `AI_PROVIDER` in `.env` to match whichever you have.

**Is this free to run?**
NewsAPI's free tier and small amounts of OpenAI/Anthropic usage are very
low-cost, but not $0 - AI provider usage is billed per request once you
have credits/billing set up on their platform. Check current pricing on
each provider's site.

**Do I need to activate the virtual environment every single time?**
Yes, once per new terminal session - but the `Start App.bat` /
`Start App (Mac).command` scripts do this for you automatically.

**Can I run this on my phone?**
The app itself only runs on a computer (it needs Python), but once it's
running you can open `http://<your-computer's-local-IP>:8000` from a phone
on the same Wi-Fi network to view it in a mobile browser.

**Will my chat history be saved if I restart the server?**
No - conversation history is stored in memory while the server runs and is
cleared when the server restarts (see `README.md` for why, and what a
production version would do differently).

---

## 16. Common mistakes beginners make

1. **Forgetting to tick "Add python.exe to PATH"** during Python
   installation on Windows - the #1 cause of `'python' is not recognized`.
2. **Running `pip install` without activating the venv first** - packages
   get installed globally instead of into the project's isolated
   environment, or the app can't find them at all.
3. **Naming the file `.env.txt` instead of `.env`** - Windows sometimes
   hides file extensions, so a rename can silently keep the `.txt` on the
   end. Make sure "File name extensions" is enabled in File Explorer's
   View options if you're unsure.
4. **Leaving placeholder text in `.env`** (e.g. `your_openai_api_key_here`)
   instead of a real key, then wondering why the AI features fail.
5. **Committing `.env` to Git** by force-adding it or misconfiguring
   `.gitignore` - always double check `git status` doesn't show `.env`
   before pushing.
6. **Closing the terminal and expecting `(venv)` to still be active** next
   time - it needs to be reactivated per session.
7. **Running `python app.py` from the wrong folder** - always make sure
   your terminal is inside `news-reader-ai/` first.

---

## 17. Security recommendations

- **Never commit `.env` to Git or share it** - it contains live API keys.
- **Set `FLASK_DEBUG=False`** in `.env` if you ever run this app anywhere
  other than your own `localhost` (e.g., on a shared network or a server).
  The default `True` value enables Flask's interactive debugger, which can
  allow arbitrary code execution if the app is reachable by anyone else.
- **Always set a real, unique `FLASK_SECRET_KEY`** - don't leave it blank.
- **Rotate any API key immediately if it's ever exposed** (e.g., pasted
  into a public chat, committed to Git, or shown in a screenshot) - both
  OpenAI and Anthropic let you revoke and regenerate keys from their
  dashboards.
- **Keep dependencies up to date** periodically with
  `pip install -r requirements.txt --upgrade` inside your activated venv,
  and check for any security advisories on the packages you use.
- See `PROJECT_REVIEW.md` for a fuller security review of this codebase.

---

## 18. Next learning steps

Once you're comfortable running this project, here are natural next steps:

1. **Read through `app.py`** - it's the shortest file and shows how a web
   request becomes a response. Try adding a `print()` statement inside a
   route and watch it appear in your terminal when you use that feature.
2. **Learn Flask basics** - the [official Flask tutorial](https://flask.palletsprojects.com/en/latest/tutorial/)
   walks through building a small app from scratch.
3. **Learn about environment variables and `.env` files** - understanding
   *why* secrets are kept out of source code is a foundational skill for
   any real-world project.
4. **Try modifying a prompt** in `ai_service.py` (e.g., change the
   `summarize_article` prompt to ask for 2 bullet points instead of 3-5)
   and see how the AI's replies change.
5. **Learn Git basics** - even for solo projects, `git init`, `git add`,
   `git commit` are worth learning early. GitHub has a
   [free beginner guide](https://docs.github.com/en/get-started).
6. **Explore adding a test** - try writing one small `pytest` test that
   checks `/api/search` returns an error when `NEWS_API_KEY` is missing.
   This is a gentle first step into automated testing.

Good luck, and enjoy building! 🚀
