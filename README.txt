# WriterX 2026 — Web App Setup Guide
## Complete beginner guide — follow every step in order!

---

## WHAT YOU'LL END UP WITH
A private website (password protected) that you and your friends can open
in any browser and use the AI humanizer. Nobody else can access it without
the password.

---

## PART 1 — SET UP YOUR COMPUTER (do this once)

### Step 1: Check that Python is installed
1. Press **Windows key + R**, type `cmd`, press Enter
2. Type this and press Enter:
   ```
   python --version
   ```
3. You should see something like `Python 3.11.0`
   - If you see an error, download Python from https://python.org/downloads
     (tick "Add Python to PATH" during install!)

### Step 2: Put all the files in one folder
Create a folder anywhere (e.g. on your Desktop called `writerx`).
Put these files inside it — they must ALL be in the same folder:

```
writerx/
├── app.py              ← from this zip
├── humanizer.py        ← your friend's original file
├── words.json          ← your friend's original file
├── requirements.txt    ← from this zip
└── templates/
    ├── login.html      ← from this zip
    └── index.html      ← from this zip
```

⚠️  Make sure `templates` is a FOLDER inside `writerx`, not a file!

### Step 3: Install Flask
1. Open Command Prompt (Windows key + R → cmd → Enter)
2. Navigate to your folder. For example if it's on your Desktop:
   ```
   cd Desktop\writerx
   ```
3. Run this command:
   ```
   pip install flask
   ```
4. Wait for it to finish (you'll see "Successfully installed flask")

---

## PART 2 — CHANGE YOUR PASSWORD (important!)

Open `app.py` in Notepad (right-click → Open with → Notepad).

Find this line near the top:
```python
PASSWORD = "writerx2026"
```

Change `writerx2026` to whatever password you want, for example:
```python
PASSWORD = "mycoolpassword123"
```

Save the file (Ctrl+S).

---

## PART 3 — RUN THE WEBSITE ON YOUR COMPUTER

### Step 4: Start the server
1. Open Command Prompt in your `writerx` folder:
   - Navigate with `cd Desktop\writerx` (adjust path as needed)
2. Run:
   ```
   python app.py
   ```
3. You'll see something like:
   ```
    * Running on http://127.0.0.1:5000
    * Running on http://0.0.0.0:5000
   ```
   **Leave this window open — closing it stops the website!**

### Step 5: Open the website
Open your browser and go to:
```
http://localhost:5000
```

You'll see the login page. Type your password and you're in!

**Your friends on the same WiFi can access it at:**
```
http://YOUR_COMPUTER_IP:5000
```
To find your IP: open Command Prompt, type `ipconfig`, look for "IPv4 Address"
(usually something like 192.168.1.xxx)

---

## PART 4 — PUT IT ONLINE (so friends anywhere can use it)

To make the website accessible from anywhere on the internet,
use **Render** (free, no credit card needed).

### Step 6: Create accounts
1. Sign up at https://github.com (free) — needed to upload your code
2. Sign up at https://render.com (free) — this hosts your website

### Step 7: Add one more file
Create a file called `Procfile` (no extension!) in your writerx folder
with exactly this content:
```
web: python app.py
```

Also open `app.py` and change the last line from:
```python
app.run(debug=True, host="0.0.0.0", port=5000)
```
to:
```python
import os
port = int(os.environ.get("PORT", 5000))
app.run(debug=False, host="0.0.0.0", port=port)
```

### Step 8: Upload to GitHub
1. Go to https://github.com → click "New repository"
2. Name it `writerx` → click "Create repository"
3. Download GitHub Desktop from https://desktop.github.com
4. Open GitHub Desktop → File → Add Local Repository → choose your writerx folder
5. Click "Publish repository" (make it **Private** so your code is hidden)

### Step 9: Deploy on Render
1. Go to https://render.com → "New" → "Web Service"
2. Connect your GitHub account and select the `writerx` repository
3. Settings:
   - **Name**: writerx (or anything)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
4. Click "Create Web Service"
5. Wait 2-3 minutes — Render will give you a URL like `https://writerx.onrender.com`

That URL is your website! Share it with your friends along with the password.

---

## HOW TO USE THE WEBSITE

1. Open the URL in any browser
2. Type the password → click ENTER
3. Paste your AI text in the left box
4. Click **HUMANIZE NOW** (or press Ctrl+Enter)
5. Wait a few seconds — you'll see the AI score go down
6. Copy the result from the right box

---

## TIPS & TRICKS

- **Auto-Fix ON** = the tool keeps re-humanizing until the AI score drops
  below 15%. Leave it on for best results.
- **The score bars**: Red = high AI detection, Green = looks human
- Each "session" lasts until you close the browser tab. Your friends need
  to log in again if they open a new tab.
- If the Render site is slow to load the first time, that's normal — free
  tier "sleeps" after 15 mins of inactivity. Just wait ~30 seconds.

---

## TROUBLESHOOTING

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: flask` | Run `pip install flask` again |
| `ModuleNotFoundError: humanizer` | Make sure `humanizer.py` and `words.json` are in the same folder as `app.py` |
| Website won't load | Make sure the `python app.py` window is still open |
| Wrong password error | Check the `PASSWORD = "..."` line in app.py |
| Render deploy fails | Make sure `requirements.txt` contains `flask` |

---

## CHANGING THE PASSWORD LATER

Just edit `app.py`, change the `PASSWORD = "..."` line, save,
and restart the server (Ctrl+C to stop, then `python app.py` again).
On Render, it redeploys automatically when you push to GitHub.
