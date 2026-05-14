from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from humanizer import humanize, detect_ai
import os

import os as _os
app = Flask(__name__, template_folder=_os.path.dirname(_os.path.abspath(__file__)))

# ── SECRET KEY ────────────────────────────────────────────────
# Change this to any random string — keeps sessions secure
app.secret_key = "change-this-to-something-random-abc123xyz"

# ── PASSWORD ──────────────────────────────────────────────────
# This is the password your friends will type to access the site
# Change it to whatever you want!
PASSWORD = "ILOVEMINECRAFT"

# ── AUTO-FIX SETTINGS ─────────────────────────────────────────
MAX_AUTO_RETRIES = 15   # Max times to re-humanize in auto-fix mode
TARGET_SCORE     = 8  # Stop when AI score drops below this %


# ──────────────────────────────────────────────────────────────
#  ROUTES
# ──────────────────────────────────────────────────────────────

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            error = "Wrong password. Try again."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/api/humanize", methods=["POST"])
def api_humanize():
    """Main API endpoint — called by the frontend JavaScript."""
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401

    data     = request.get_json(silent=True) or {}
    text     = data.get("text", "").strip()
    auto_fix = data.get("auto_fix", True)

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if len(text) > 50_000:
        return jsonify({"error": "Text too long (max 50,000 characters)"}), 400

    try:
        # Score the original text
        before = detect_ai(text)

        # First humanize pass (double = hybrid mode)
        result = humanize(text)
        result = humanize(result)

        # Auto-fix loop: keep going until score is low enough
        attempts = 0
        if auto_fix:
            current_score = detect_ai(result)["score"]
            while current_score > TARGET_SCORE and attempts < MAX_AUTO_RETRIES:
                result = humanize(result)
                current_score = detect_ai(result)["score"]
                attempts += 1

        after = detect_ai(result)

        return jsonify({
            "result":   result,
            "before":   before,
            "after":    after,
            "attempts": attempts,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ──────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
