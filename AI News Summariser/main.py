import tkinter as tk
from textblob import TextBlob
from newspaper import Article

def summarise():
    url = utext.get("1.0", "end").strip()

    article = Article(url)

    try:
        article.download()
        article.parse()
        article.nlp()
    except Exception as e:
        for widget in [title, author, publication, summary, sentiment]:
            widget.config(state="normal")
            widget.delete("1.0", "end")
            widget.insert("1.0", f"Error: {e}")
            widget.config(state="disabled")
        return

    for widget in [title, author, publication, summary, sentiment]:
        widget.config(state="normal")
        widget.delete("1.0", "end")

    title.insert("1.0", str(article.title) if article.title else "Title not available")
    author.insert("1.0", ", ".join(article.authors) if article.authors else "Authors not available")
    publication.insert("1.0", str(article.publish_date) if article.publish_date else "Publish date not available")
    summary.insert("1.0", article.summary if article.summary else "Summary not available")

    if article.text:
        analysis = TextBlob(article.text)
        sentiment_text = f"Polarity: {analysis.polarity:.2f}, Sentiment: {'positive' if analysis.polarity > 0 else 'negative' if analysis.polarity < 0 else 'neutral'}"
    else:
        sentiment_text = "No article text available for sentiment analysis"

    sentiment.insert("1.0", sentiment_text)

    for widget in [title, author, publication, summary, sentiment]:
        widget.config(state="disabled")

# === GUI SETUP ===
root = tk.Tk()
root.title("News Summariser")
root.geometry("1240x640")
root.configure(bg="#000000")  # Black background

# Outer neon blue frame
outer_frame = tk.Frame(root, bg="#00FFFF", padx=4, pady=4)  # Neon Blue
outer_frame.pack(padx=8, pady=8, fill="both", expand=True)

# Inner neon yellow frame
glow_frame = tk.Frame(outer_frame, bg="#FFFF33", padx=4, pady=4)  # Neon Yellow
glow_frame.pack(fill="both", expand=True)

# Main content area
main_frame = tk.Frame(glow_frame, bg="#1e1e1e")
main_frame.pack(fill="both", expand=True)

# Label styling
label_style = {"bg": "#1e1e1e", "fg": "#FFFF33", "font": ("Helvetica", 10, "bold")}

# Output text styling (changed to bold white)
output_text_style = {
    "bg": "#9D00FF", "fg": "#FFFFFF", "font": ("Helvetica", 10, "bold"),
    "insertbackground": "#FFFFFF", "bd": 2, "relief": "solid",
    "highlightbackground": "#FFFF33", "highlightcolor": "#FFFF33",
    "state": "disabled"
}

# Input text styling (changed to bold yellow)
input_text_style = {
    "bg": "#000000", "fg": "#FFFF33", "font": ("Helvetica", 10, "bold"),
    "insertbackground": "#FFFF33", "bd": 2, "relief": "solid",
    "highlightbackground": "#FFFF33", "highlightcolor": "#FFFF33"
}

# === UI Components ===
def add_label_text(label_text, text_widget):
    label = tk.Label(main_frame, text=label_text, **label_style)
    label.pack()
    text_widget.pack()

tlabel = tk.Label(main_frame, text="Title", **label_style)
tlabel.pack()
title = tk.Text(main_frame, height=1, width=140, **output_text_style)
title.pack()

alabel = tk.Label(main_frame, text="Author", **label_style)
alabel.pack()
author = tk.Text(main_frame, height=1, width=140, **output_text_style)
author.pack()

plabel = tk.Label(main_frame, text="Publishing Date", **label_style)
plabel.pack()
publication = tk.Text(main_frame, height=1, width=140, **output_text_style)
publication.pack()

slabel = tk.Label(main_frame, text="Summary", **label_style)
slabel.pack()
summary = tk.Text(main_frame, height=20, width=140, **output_text_style)
summary.pack()

selabel = tk.Label(main_frame, text="Sentiment Analysis", **label_style)
selabel.pack()
sentiment = tk.Text(main_frame, height=1, width=140, **output_text_style)
sentiment.pack()

ulabel = tk.Label(main_frame, text="URL", **label_style)
ulabel.pack()
utext = tk.Text(main_frame, height=1, width=140, **input_text_style)
utext.pack()

# === Neon Hover Button ===
def on_enter(e):
    btn.config(bg="#FFFF33", fg="#1e1e1e")

def on_leave(e):
    btn.config(bg="#9D00FF", fg="#FFFF33")

btn = tk.Button(
    main_frame,
    text="Summarise",
    command=summarise,
    bg="#9D00FF",
    fg="#FFFF33",
    font=("Helvetica", 10, "bold"),
    activebackground="#FFFF33",
    activeforeground="#1e1e1e",
    bd=2,
    relief="groove",
    padx=20,
    pady=5
)
btn.pack(pady=10)
btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

root.mainloop()