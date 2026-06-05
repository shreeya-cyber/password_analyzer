import tkinter as tk
from tkinter import ttk, messagebox
import zxcvbn

# ── WORDLIST GENERATOR ────────────────────────────────────────
def leetspeak(word):
    replacements = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    result = word
    for char, leet in replacements.items():
        result = result.replace(char, leet).replace(char.upper(), leet)
    return result

def generate_wordlist(name, dob, pet, output_file="wordlist.txt"):
    base_words = [name, dob, pet, name+pet, pet+name]
    years = ["2023", "2024", "2025", "123", "1234", "!"]
    wordlist = set()
    for word in base_words:
        if not word:
            continue
        variants = [word, word.lower(), word.upper(), word.capitalize(), leetspeak(word)]
        for v in variants:
            wordlist.add(v)
            for y in years:
                wordlist.add(v + y)
                wordlist.add(y + v)
    with open(output_file, "w") as f:
        for w in sorted(wordlist):
            f.write(w + "\n")
    return len(wordlist)

# ── GUI ───────────────────────────────────────────────────────
def analyze():
    password = entry_password.get()
    if not password:
        messagebox.showwarning("Oops", "Please enter a password!")
        return
    result = zxcvbn.zxcvbn(password)
    score = result['score']
    crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
    suggestions = result['feedback']['suggestions']
    labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"]
    strength_label.config(text=f"Strength: {labels[score]} ({score}/4)", fg=colors[score])
    crack_label.config(text=f"Crack Time: {crack_time}")
    progress['value'] = (score + 1) * 20
    tips_box.config(state="normal")
    tips_box.delete("1.0", tk.END)
    if suggestions:
        for tip in suggestions:
            tips_box.insert(tk.END, f"• {tip}\n")
    else:
        tips_box.insert(tk.END, "✓ Looks good! No suggestions.")
    tips_box.config(state="disabled")

def generate():
    name = entry_name.get()
    dob  = entry_dob.get()
    pet  = entry_pet.get()
    if not name and not dob and not pet:
        messagebox.showwarning("Oops", "Please fill at least one field!")
        return
    count = generate_wordlist(name, dob, pet)
    messagebox.showinfo("Done!", f"Wordlist saved as 'wordlist.txt'\n{count} entries generated!")

# ── WINDOW SETUP ──────────────────────────────────────────────
root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("500x600")
root.configure(bg="#1e1e2e")
root.resizable(False, True)

BG       = "#1e1e2e"
FG       = "#cdd6f4"
ENTRY_BG = "#313244"
FONT     = ("Segoe UI", 11)
FONT_BOLD= ("Segoe UI", 11, "bold")

# ── SCROLLABLE CANVAS ─────────────────────────────────────────
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

frame = tk.Frame(canvas, bg=BG)
canvas_window = canvas.create_window((0, 0), window=frame, anchor="nw")

def on_frame_configure(e):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_canvas_configure(e):
    canvas.itemconfig(canvas_window, width=e.width)

frame.bind("<Configure>", on_frame_configure)
canvas.bind("<Configure>", on_canvas_configure)

# mousewheel scroll
def on_mousewheel(e):
    canvas.yview_scroll(int(-1*(e.delta/120)), "units")
root.bind("<MouseWheel>", on_mousewheel)

# ── HELPERS ───────────────────────────────────────────────────
def lbl(text, font=FONT):
    return tk.Label(frame, text=text, bg=BG, fg=FG, font=font)

def ent():
    return tk.Entry(frame, bg=ENTRY_BG, fg=FG, insertbackground=FG,
                    relief="flat", font=FONT, bd=6)

# ── SECTION 1: ANALYZE ───────────────────────────────────────
lbl("🔐 Password Strength Analyzer", ("Segoe UI", 14, "bold")).pack(pady=(20,10))

lbl("Enter Password:").pack(anchor="w", padx=30)
entry_password = ent()
entry_password.pack(fill="x", padx=30, pady=(4,10))

tk.Button(frame, text="Analyze", command=analyze,
          bg="#89b4fa", fg="#1e1e2e", font=FONT_BOLD,
          relief="flat", padx=10, pady=6, cursor="hand2").pack()

strength_label = tk.Label(frame, text="Strength: —", bg=BG, fg=FG, font=FONT_BOLD)
strength_label.pack(pady=(10,2))

crack_label = tk.Label(frame, text="Crack Time: —", bg=BG, fg="#a6adc8", font=FONT)
crack_label.pack()

progress = ttk.Progressbar(frame, length=420, mode="determinate", maximum=100)
progress.pack(pady=8)

tips_box = tk.Text(frame, height=3, bg=ENTRY_BG, fg="#a6e3a1",
                   font=("Segoe UI", 10), relief="flat", bd=6, state="disabled")
tips_box.pack(fill="x", padx=30, pady=(0,16))

# ── SECTION 2: WORDLIST ───────────────────────────────────────
tk.Frame(frame, bg="#45475a", height=1).pack(fill="x", padx=30, pady=4)
lbl("🗂️ Custom Wordlist Generator", ("Segoe UI", 12, "bold")).pack(pady=(8,6))

for lbl_text, var_name in [
    ("Name:", "entry_name"),
    ("Date of Birth (e.g. 01011999):", "entry_dob"),
    ("Pet Name:", "entry_pet")
]:
    tk.Label(frame, text=lbl_text, bg=BG, fg=FG, font=FONT).pack(anchor="w", padx=30)
    e = tk.Entry(frame, bg=ENTRY_BG, fg=FG, insertbackground=FG,
                 relief="flat", font=FONT, bd=6)
    e.pack(fill="x", padx=30, pady=(2,6))
    globals()[var_name] = e

tk.Button(frame, text="Generate & Export Wordlist", command=generate,
          bg="#a6e3a1", fg="#1e1e2e", font=FONT_BOLD,
          relief="flat", padx=10, pady=6, cursor="hand2").pack(pady=(10,30))

root.mainloop()