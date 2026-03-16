import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
import threading
from scrapers.youtube_scraper import YouTubeScraper
from scrapers.bbc_scraper import BBCScraper
from db.mongo_handler import MongoHandler
from services.scraper_service import ScraperService

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#0f1117"   # main background
SURFACE   = "#1a1d27"   # card / panel background
BORDER    = "#2a2d3e"   # subtle border
ACCENT    = "#7c6af7"   # purple accent
ACCENT2   = "#5e57cc"   # darker purple (hover)
TEXT      = "#e2e8f0"   # primary text
TEXT_DIM  = "#8892a4"   # secondary text
SUCCESS   = "#4ade80"
WARNING   = "#fb923c"
DANGER    = "#f87171"
ROW_ODD   = "#1e2130"
ROW_EVEN  = "#232638"

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_HEAD   = ("Segoe UI", 10, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)

db = MongoHandler()
current_posts = []
displayed_posts = []  # מה שמוצג כרגע בטבלה (מחיפוש או מ-DB)


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_scraper(source: str):
    return YouTubeScraper() if source == "YouTube" else BBCScraper()


def posts_to_table(posts: list) -> list:
    return [
        [p.get("source", ""), p.get("keyword", ""),
         p.get("title", "")[:70], round(p.get("sentiment", 0), 2),
         str(p.get("date", ""))[:10]]
        for p in posts
    ]


def set_status(msg, color=SUCCESS):
    status_var.set(f"  {msg}")
    status_label.config(fg=color)


def update_table(rows):
    for item in tree.get_children():
        tree.delete(item)
    for i, row in enumerate(rows):
        tag = "odd" if i % 2 == 0 else "even"
        tree.insert("", "end", values=row, tags=(tag,))


# ── Loading animation ─────────────────────────────────────────────────────────
_loading_job = None

def start_loading():
    global _loading_job
    dots = ["Searching  ⠋", "Searching  ⠙", "Searching  ⠹",
            "Searching  ⠸", "Searching  ⠼", "Searching  ⠴",
            "Searching  ⠦", "Searching  ⠧", "Searching  ⠇", "Searching  ⠏"]
    idx = [0]
    def tick():
        global _loading_job
        set_status(dots[idx[0] % len(dots)], WARNING)
        idx[0] += 1
        _loading_job = root.after(100, tick)
    tick()

def stop_loading():
    global _loading_job
    if _loading_job:
        root.after_cancel(_loading_job)
        _loading_job = None


# ── Actions ───────────────────────────────────────────────────────────────────
def do_search():
    global current_posts
    keyword = keyword_var.get().strip()
    source  = source_var.get()
    limit   = int(limit_var.get())

    if not keyword:
        set_status("Please enter a keyword!", DANGER)
        return

    search_btn.config(state="disabled")
    start_loading()

    def run():
        global current_posts
        if source == "All":
            results = []
            for src in ["YouTube", "BBC"]:
                scraper = get_scraper(src)
                service = ScraperService(scraper, db)
                results += service.search_and_analyze(keyword, limit)
        else:
            scraper = get_scraper(source)
            service = ScraperService(scraper, db)
            results = service.search_and_analyze(keyword, limit)

        def on_done():
            global current_posts, displayed_posts
            current_posts = results
            displayed_posts = [{"source": p.source, "keyword": p.keyword,
                                 "title": p.title, "sentiment": p.sentiment, "date": ""}
                                for p in current_posts]
            stop_loading()
            rows = [[p.source, p.keyword, p.title[:70], round(p.sentiment, 2), ""]
                    for p in current_posts]
            update_table(rows)
            set_status(f"Found {len(current_posts)} results!", SUCCESS)
            search_btn.config(state="normal")

        root.after(0, on_done)

    threading.Thread(target=run, daemon=True).start()


def do_save():
    if not current_posts:
        set_status("No results to save!", DANGER)
        return
    saved = db.save_many(current_posts)
    set_status(f"Saved {saved} posts to MongoDB!", SUCCESS)


def do_load():
    global displayed_posts
    displayed_posts = db.get_all()
    update_table(posts_to_table(displayed_posts))
    set_status(f"Loaded {len(displayed_posts)} posts from DB", SUCCESS)


def do_filter():
    f = filter_var.get()
    if not displayed_posts:
        set_status("No data loaded — search or load from DB first", WARNING)
        return
    filtered = displayed_posts if f == "All" else [p for p in displayed_posts if p.get("source", "").lower() == f.lower()]
    update_table(posts_to_table(filtered))
    set_status(f"Showing {len(filtered)} {f} posts", SUCCESS)


def on_close():
    db.close()
    root.destroy()


# ── Button factory ────────────────────────────────────────────────────────────
def make_btn(parent, text, command, color=ACCENT, width=14):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg="white", activebackground=ACCENT2,
        activeforeground="white", relief="flat",
        font=FONT_BODY, cursor="hand2",
        padx=14, pady=7, bd=0, width=width
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT2))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


# ── Root window ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Sports Scraper")
root.geometry("1000x680")
root.resizable(True, True)
root.config(bg=BG)

# ── Header bar ────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=SURFACE, pady=14)
header.pack(fill="x")

tk.Label(header, text="⚡ Sports Scraper",
         font=FONT_TITLE, bg=SURFACE, fg=TEXT).pack(side="left", padx=24)
tk.Label(header, text="Real-time sports intelligence",
         font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM).pack(side="left", padx=4)

# ── Search card ───────────────────────────────────────────────────────────────
card = tk.Frame(root, bg=SURFACE, padx=20, pady=16)
card.pack(fill="x", padx=20, pady=(16, 0))

# Row 1: Keyword + Source
row1 = tk.Frame(card, bg=SURFACE)
row1.pack(fill="x", pady=(0, 10))

tk.Label(row1, text="KEYWORD", font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM).grid(row=0, column=0, sticky="w")
tk.Label(row1, text="SOURCE",  font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM).grid(row=0, column=2, sticky="w", padx=(24, 0))
tk.Label(row1, text="LIMIT",   font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM).grid(row=0, column=4, sticky="w", padx=(24, 0))

keyword_var = tk.StringVar()
kw_entry = tk.Entry(row1, textvariable=keyword_var, font=FONT_BODY,
                    bg=BORDER, fg=TEXT, insertbackground=TEXT,
                    relief="flat", bd=0, width=28)
kw_entry.grid(row=1, column=0, columnspan=2, ipady=7, sticky="ew", padx=(0, 0))
kw_entry.bind("<Return>", lambda e: do_search())

source_var = tk.StringVar(value="YouTube")
src_combo = ttk.Combobox(row1, textvariable=source_var,
                         values=["YouTube", "BBC", "All"],
                         width=12, state="readonly", font=FONT_BODY)
src_combo.grid(row=1, column=2, ipady=5, padx=(24, 0), sticky="w")

limit_var = tk.IntVar(value=10)
limit_label = tk.Label(row1, textvariable=limit_var,
                       font=("Segoe UI", 11, "bold"), bg=SURFACE, fg=ACCENT, width=3)
limit_label.grid(row=1, column=4, padx=(24, 4))
tk.Scale(row1, variable=limit_var, from_=5, to=50, orient="horizontal",
         length=140, bg=SURFACE, fg=TEXT, troughcolor=BORDER,
         highlightthickness=0, sliderrelief="flat",
         activebackground=ACCENT, showvalue=False).grid(row=1, column=5, padx=(0, 0))

row1.columnconfigure(1, weight=1)

# Row 2: Action buttons
row2 = tk.Frame(card, bg=SURFACE)
row2.pack(fill="x")

search_btn = make_btn(row2, "Search", do_search, ACCENT)
search_btn.pack(side="left", padx=(0, 8))
make_btn(row2, "Save to DB",  do_save,   "#2563eb").pack(side="left", padx=(0, 8))
make_btn(row2, "Load from DB",do_load,   "#059669").pack(side="left", padx=(0, 8))
make_btn(row2, "Exit",        on_close,  "#6b7280", width=10).pack(side="right")

# ── Filter bar ────────────────────────────────────────────────────────────────
filter_bar = tk.Frame(root, bg=BG, padx=20, pady=8)
filter_bar.pack(fill="x")

tk.Label(filter_bar, text="Filter:", font=FONT_BODY,
         bg=BG, fg=TEXT_DIM).pack(side="left")

filter_var = tk.StringVar(value="All")
for val in ["All", "YouTube", "BBC"]:
    rb = tk.Radiobutton(
        filter_bar, text=val, variable=filter_var, value=val,
        command=do_filter, bg=BG, fg=TEXT, selectcolor=BG,
        activebackground=BG, activeforeground=ACCENT,
        font=FONT_BODY, cursor="hand2",
        indicatoron=False, relief="flat",
        padx=12, pady=5, bd=0
    )
    rb.pack(side="left", padx=4)

# ── Results table ─────────────────────────────────────────────────────────────
table_frame = tk.Frame(root, bg=BG)
table_frame.pack(fill="both", expand=True, padx=20, pady=(4, 0))

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
    background=ROW_ODD, foreground=TEXT,
    fieldbackground=ROW_ODD,
    rowheight=30, font=FONT_BODY,
    borderwidth=0)

style.configure("Treeview.Heading",
    background=SURFACE, foreground=TEXT_DIM,
    font=FONT_HEAD, relief="flat", padding=(8, 6))

style.map("Treeview",
    background=[("selected", ACCENT)],
    foreground=[("selected", "white")])

style.map("Treeview.Heading",
    background=[("active", BORDER)])

columns = ["Source", "Keyword", "Title", "Sentiment", "Date"]
tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                    selectmode="browse")

for col, width, anchor in zip(
    columns, [90, 110, 500, 90, 100],
    ["center", "w", "w", "center", "center"]
):
    tree.heading(col, text=col.upper())
    tree.column(col, width=width, anchor=anchor, minwidth=60)

tree.tag_configure("odd",  background=ROW_ODD)
tree.tag_configure("even", background=ROW_EVEN)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
style.configure("Vertical.TScrollbar", background=BORDER,
                troughcolor=BG, arrowcolor=TEXT_DIM)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ── Status bar ────────────────────────────────────────────────────────────────
status_bar = tk.Frame(root, bg=SURFACE, pady=6)
status_bar.pack(fill="x", side="bottom")

status_var = tk.StringVar(value="  Ready")
status_label = tk.Label(status_bar, textvariable=status_var,
                        font=FONT_SMALL, bg=SURFACE, fg=SUCCESS, anchor="w")
status_label.pack(side="left", padx=12)

tk.Label(status_bar, text="Sports Scraper v2.0",
         font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM).pack(side="right", padx=12)

# ── Style comboboxes ──────────────────────────────────────────────────────────
style.configure("TCombobox",
    fieldbackground=BORDER, background=BORDER,
    foreground=TEXT, selectbackground=ACCENT,
    arrowcolor=TEXT_DIM, borderwidth=0)
style.map("TCombobox", fieldbackground=[("readonly", BORDER)])

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
