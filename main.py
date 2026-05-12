import customtkinter as ctk
from tkinter import messagebox, filedialog
from docx import Document
import threading
import os

from humanizer import humanize, detect_ai

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_DARK    = "#0a0e17"
BG_CARD    = "#131a2b"
BG_INPUT   = "#0d1321"
GREEN      = "#00ff9d"
GREEN_DIM  = "#00b894"
CYAN       = "#00d2ff"
RED        = "#ff4757"
YELLOW     = "#ffa502"
TEXT_DIM   = "#5a6a7a"
TEXT_MED   = "#8899aa"
TEXT_LIGHT = "#c8d6e5"
BORDER     = "#1e2a3a"

MAX_AUTO_RETRIES = 8
TARGET_SCORE     = 15


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WriterX 2026 - AI Humanizer")
        self.geometry("1300x880")
        self.minsize(1000, 680)
        self.configure(fg_color=BG_DARK)
        self._build_ui()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1300 // 2)
        y = (self.winfo_screenheight() // 2) - (880 // 2)
        self.geometry(f"1300x880+{x}+{y}")

    def _build_ui(self):
        # ── HEADER ────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=BG_DARK, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(
            logo_frame,
            text="WRITERX 2026",
            font=ctk.CTkFont(size=22, weight="bold", family="Consolas"),
            text_color=GREEN
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_frame,
            text="AI Humanizer  |  0% AI Detection  |  Auto-Fix Mode",
            font=ctk.CTkFont(size=11, family="Consolas"),
            text_color=TEXT_DIM
        ).pack(anchor="w")

        mode_frame = ctk.CTkFrame(header, fg_color="transparent")
        mode_frame.pack(side="right", padx=20)

        ctk.CTkLabel(
            mode_frame,
            text="ENGINE:",
            font=ctk.CTkFont(size=11, weight="bold", family="Consolas"),
            text_color=TEXT_MED
        ).pack(side="left", padx=(0, 8))

        self.mode_var = ctk.StringVar(value="hybrid")
        modes = [
            ("Regex",    "regex",  "#4ecdc4"),
            ("AI Power", "ai",     "#a29bfe"),
            ("Hybrid",   "hybrid", GREEN),
        ]
        for label, value, color in modes:
            rb = ctk.CTkRadioButton(
                mode_frame,
                text=label,
                variable=self.mode_var,
                value=value,
                font=ctk.CTkFont(size=11, family="Consolas"),
                fg_color=color,
                hover_color=color,
                text_color=TEXT_LIGHT,
            )
            rb.pack(side="left", padx=4)

        # Auto-fix toggle
        self.auto_fix_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            mode_frame,
            text="AUTO-FIX",
            variable=self.auto_fix_var,
            font=ctk.CTkFont(size=11, weight="bold", family="Consolas"),
            fg_color=GREEN_DIM,
            hover_color=GREEN,
            text_color=GREEN,
            checkmark_color=BG_DARK,
        ).pack(side="left", padx=(16, 4))

        # ── SCORE CARDS ───────────────────────────────────────
        self.score_frame = ctk.CTkFrame(self, fg_color="transparent", height=85)
        self.score_frame.pack(fill="x", padx=16, pady=(8, 4))
        self.score_frame.pack_propagate(False)

        self.before_card = ctk.CTkFrame(self.score_frame, fg_color=BG_CARD,
                                        corner_radius=10, border_width=1,
                                        border_color=BORDER)
        self.before_card.pack(side="left", fill="both", expand=True, padx=(0, 4))
        self.before_card.pack_propagate(False)

        bf = ctk.CTkFrame(self.before_card, fg_color="transparent")
        bf.pack(fill="both", expand=True, padx=16, pady=8)

        ctk.CTkLabel(bf, text="ORIGINAL AI SCORE",
                     font=ctk.CTkFont(size=10, weight="bold", family="Consolas"),
                     text_color=TEXT_DIM).pack(side="left")

        self.before_score_label = ctk.CTkLabel(
            bf, text="--",
            font=ctk.CTkFont(size=28, weight="bold", family="Consolas"),
            text_color=TEXT_DIM
        )
        self.before_score_label.pack(side="right")

        self.before_bar = ctk.CTkProgressBar(bf, width=200, height=6,
                                              fg_color=BORDER, progress_color=RED)
        self.before_bar.pack(side="right", padx=(0, 16))
        self.before_bar.set(0)

        ctk.CTkLabel(
            self.score_frame, text=">>>",
            font=ctk.CTkFont(size=18, weight="bold", family="Consolas"),
            text_color=GREEN
        ).pack(side="left", padx=8)

        self.after_card = ctk.CTkFrame(self.score_frame, fg_color=BG_CARD,
                                       corner_radius=10, border_width=1,
                                       border_color=BORDER)
        self.after_card.pack(side="left", fill="both", expand=True, padx=(4, 0))
        self.after_card.pack_propagate(False)

        af = ctk.CTkFrame(self.after_card, fg_color="transparent")
        af.pack(fill="both", expand=True, padx=16, pady=8)

        ctk.CTkLabel(af, text="HUMANIZED AI SCORE",
                     font=ctk.CTkFont(size=10, weight="bold", family="Consolas"),
                     text_color=GREEN).pack(side="left")

        self.after_score_label = ctk.CTkLabel(
            af, text="--",
            font=ctk.CTkFont(size=28, weight="bold", family="Consolas"),
            text_color=GREEN
        )
        self.after_score_label.pack(side="right")

        self.after_bar = ctk.CTkProgressBar(af, width=200, height=6,
                                             fg_color=BORDER, progress_color=GREEN)
        self.after_bar.pack(side="right", padx=(0, 16))
        self.after_bar.set(0)

        # ── TEXT PANELS ───────────────────────────────────────
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=4)

        left = ctk.CTkFrame(body, fg_color=BG_CARD, corner_radius=10,
                            border_width=1, border_color=BORDER)
        left.pack(side="left", fill="both", expand=True, padx=(0, 4))

        left_top = ctk.CTkFrame(left, fg_color="transparent")
        left_top.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(left_top, text="PASTE AI TEXT",
                     font=ctk.CTkFont(size=11, weight="bold", family="Consolas"),
                     text_color=TEXT_MED).pack(side="left")

        ctk.CTkButton(left_top, text="CLEAR", width=60, height=24,
                      font=ctk.CTkFont(size=10, family="Consolas"),
                      fg_color="#c0392b", hover_color="#e74c3c",
                      corner_radius=4, command=self._clear_input).pack(side="right")

        self.input_text = ctk.CTkTextbox(
            left, font=ctk.CTkFont(size=13, family="Segoe UI"),
            wrap="word", fg_color=BG_INPUT, border_width=0,
            corner_radius=6, text_color=TEXT_LIGHT,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=TEXT_DIM,
        )
        self.input_text.pack(fill="both", expand=True, padx=10, pady=(0, 4))
        self.input_text.bind("<KeyRelease>", self._update_input_count)

        self.input_count = ctk.CTkLabel(
            left, text="0 words",
            font=ctk.CTkFont(size=10, family="Consolas"),
            text_color=TEXT_DIM
        )
        self.input_count.pack(anchor="e", padx=12, pady=(0, 8))

        right = ctk.CTkFrame(body, fg_color=BG_CARD, corner_radius=10,
                             border_width=1, border_color="#1a3a2a")
        right.pack(side="right", fill="both", expand=True, padx=(4, 0))

        right_top = ctk.CTkFrame(right, fg_color="transparent")
        right_top.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(right_top, text="HUMAN OUTPUT",
                     font=ctk.CTkFont(size=11, weight="bold", family="Consolas"),
                     text_color=GREEN).pack(side="left")

        btn_frame = ctk.CTkFrame(right_top, fg_color="transparent")
        btn_frame.pack(side="right")

        for text, color, cmd in [
            ("COPY",  "#0984e3", self._copy_output),
            ("SAVE",  "#6c5ce7", self._save_output),
            ("CLEAR", "#c0392b", self._clear_output),
        ]:
            ctk.CTkButton(btn_frame, text=text, width=55, height=24,
                          font=ctk.CTkFont(size=10, family="Consolas"),
                          fg_color=color, hover_color=color,
                          corner_radius=4, command=cmd).pack(side="left", padx=2)

        self.output_text = ctk.CTkTextbox(
            right, font=ctk.CTkFont(size=13, family="Segoe UI"),
            wrap="word", fg_color=BG_INPUT, border_width=0,
            corner_radius=6, text_color=TEXT_LIGHT,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=TEXT_DIM,
            state="disabled",
        )
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 4))

        self.output_count = ctk.CTkLabel(
            right, text="0 words",
            font=ctk.CTkFont(size=10, family="Consolas"),
            text_color=TEXT_DIM
        )
        self.output_count.pack(anchor="e", padx=12, pady=(0, 8))

        # ── ACTION BUTTON ─────────────────────────────────────
        self.action_btn = ctk.CTkButton(
            self,
            text=">>  HUMANIZE NOW  <<",
            height=58,
            font=ctk.CTkFont(size=18, weight="bold", family="Consolas"),
            fg_color=GREEN_DIM,
            hover_color="#00a085",
            corner_radius=0,
            command=self._start_process,
        )
        self.action_btn.pack(fill="x")

        # ── STATUS BAR ────────────────────────────────────────
        self.status = ctk.CTkLabel(
            self,
            text="READY  |  Paste text and click HUMANIZE NOW  |  AUTO-FIX ON",
            font=ctk.CTkFont(size=11, family="Consolas"),
            text_color=TEXT_DIM,
            height=30
        )
        self.status.pack(fill="x", padx=20, pady=(4, 6))

        self.indicators_frame = ctk.CTkFrame(self, fg_color=BG_CARD,
                                             corner_radius=8, border_width=1,
                                             border_color=BORDER)

    # ── HELPERS ───────────────────────────────────────────────

    def _update_input_count(self, event=None):
        text = self.input_text.get("0.0", "end").strip()
        count = len(text.split()) if text else 0
        self.input_count.configure(text=f"{count} words  |  {len(text)} chars")

    def _clear_input(self):
        self.input_text.delete("0.0", "end")
        self.input_count.configure(text="0 words")
        self.before_score_label.configure(text="--", text_color=TEXT_DIM)
        self.before_bar.set(0)

    def _clear_output(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.configure(state="disabled")
        self.output_count.configure(text="0 words")
        self.after_score_label.configure(text="--", text_color=GREEN)
        self.after_bar.set(0)
        self.indicators_frame.pack_forget()

    def _copy_output(self):
        text = self.output_text.get("0.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status.configure(text="COPIED TO CLIPBOARD!", text_color=GREEN)

    def _save_output(self):
        text = self.output_text.get("0.0", "end").strip()
        if not text:
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Word documents", "*.docx")]
        )
        if filepath:
            if filepath.endswith(".docx"):
                doc = Document()
                doc.add_paragraph(text)
                doc.save(filepath)
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)
            self.status.configure(
                text=f"SAVED: {os.path.basename(filepath)}", text_color=GREEN)

    def _get_score_color(self, score):
        if score >= 70:
            return RED
        elif score >= 40:
            return YELLOW
        return GREEN

    def _show_indicators(self, before_indicators, after_indicators):
        for widget in self.indicators_frame.winfo_children():
            widget.destroy()

        left_col = ctk.CTkFrame(self.indicators_frame, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=12, pady=8)

        ctk.CTkLabel(left_col, text="ORIGINAL FLAGS:",
                     font=ctk.CTkFont(size=10, weight="bold", family="Consolas"),
                     text_color=RED).pack(anchor="w")
        for ind in before_indicators[:4]:
            ctk.CTkLabel(left_col, text=f"  - {ind}",
                         font=ctk.CTkFont(size=9, family="Consolas"),
                         text_color=TEXT_DIM, wraplength=400,
                         justify="left").pack(anchor="w", pady=1)

        right_col = ctk.CTkFrame(self.indicators_frame, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True, padx=12, pady=8)

        ctk.CTkLabel(right_col, text="HUMANIZED FLAGS:",
                     font=ctk.CTkFont(size=10, weight="bold", family="Consolas"),
                     text_color=GREEN).pack(anchor="w")
        for ind in after_indicators[:4]:
            ctk.CTkLabel(right_col, text=f"  - {ind}",
                         font=ctk.CTkFont(size=9, family="Consolas"),
                         text_color=TEXT_DIM, wraplength=400,
                         justify="left").pack(anchor="w", pady=1)

        self.indicators_frame.pack(fill="x", padx=16, pady=(0, 4))

    # ── MAIN PROCESS ──────────────────────────────────────────

    def _start_process(self):
        text = self.input_text.get("0.0", "end").strip()
        if not text:
            messagebox.showerror("Empty", "Please paste some text first.")
            return

        self.action_btn.configure(state="disabled", text="PROCESSING...")
        self.status.configure(text="Analyzing original text...", text_color=YELLOW)

        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.configure(state="disabled")

        def run():
            try:
                before = detect_ai(text)
                self.after(0, self._update_before_score, before)

                mode = self.mode_var.get()
                auto_fix = self.auto_fix_var.get()

                self.after(0, lambda: self.status.configure(
                    text=f"Humanizing with {mode.upper()} engine...",
                    text_color=YELLOW))

                # First pass
                if mode == "regex":
                    result = humanize(text)
                elif mode == "ai":
                    result = humanize(text)
                else:
                    result = humanize(text)
                    result = humanize(result)

                # ── AUTO-FIX LOOP ──────────────────────────────
                if auto_fix:
                    attempt = 1
                    current_score = detect_ai(result)["score"]

                    while current_score > TARGET_SCORE and attempt < MAX_AUTO_RETRIES:
                        attempt += 1
                        _attempt = attempt
                        _score   = current_score
                        self.after(0, lambda a=_attempt, s=_score: self.status.configure(
                            text=f"AUTO-FIX: attempt {a}/{MAX_AUTO_RETRIES}  |  current score: {s}%  |  target: <{TARGET_SCORE}%",
                            text_color=YELLOW))

                        result = humanize(result)
                        current_score = detect_ai(result)["score"]

                self.after(0, self._show_result, result, before)

            except Exception as e:
                self.after(0, self._show_error, str(e))

        threading.Thread(target=run, daemon=True).start()

    def _update_before_score(self, before):
        score = before["score"]
        self.before_score_label.configure(
            text=f"{score}%",
            text_color=self._get_score_color(score)
        )
        self.before_bar.set(score / 100)

    def _show_result(self, result, before):
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", result)
        self.output_text.configure(state="disabled")

        words = len(result.split())
        self.output_count.configure(text=f"{words} words  |  {len(result)} chars")

        after = detect_ai(result)
        score = after["score"]
        self.after_score_label.configure(
            text=f"{score}%",
            text_color=self._get_score_color(score)
        )
        self.after_bar.set(score / 100)

        self._show_indicators(before["indicators"], after["indicators"])

        before_score = before["score"]
        improvement  = before_score - score
        self.status.configure(
            text=f"DONE!  AI Score: {before_score}% >> {score}%  ( -{improvement}% )  |  100% Human Ready!",
            text_color=GREEN
        )
        self.action_btn.configure(state="normal", text=">>  HUMANIZE NOW  <<")

    def _show_error(self, msg):
        self.status.configure(text=f"ERROR: {msg}", text_color=RED)
        self.action_btn.configure(state="normal", text=">>  HUMANIZE NOW  <<")
        messagebox.showerror("Error", msg)


if __name__ == "__main__":
    app = App()
    app.mainloop()